#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"
WRITING_DIR = ROOT / "writing"
AUTHOR = "Xiaoyu Fan"
TAGLINE = "I and the world, is a frame of moment."


@dataclass
class Post:
    title: str
    date: str
    summary: str
    slug: str
    year: str
    source: Path
    body_html: str


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("Post must start with YAML-style front matter.")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Front matter must end with a line containing only ---.")

    raw_meta = text[4:end].strip()
    body = text[end + 5 :].strip()
    meta: dict[str, str] = {}

    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front matter line: {line}")
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")

    return meta, body


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "post"


def display_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%b %Y")
    except ValueError:
        return value


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    text = text.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br>").replace("&lt;br /&gt;", "<br>")
    text = re.sub(r"!\[\[([^\]]+)\]\]", r'<img src="assets/\1" alt="\1">', text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def render_markdown(md: str) -> str:
    lines = md.splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    ordered_items: list[str] = []
    quote_lines: list[str] = []
    table_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            blocks.append("<ul>\n" + "\n".join(list_items) + "\n</ul>")
            list_items = []

    def flush_ordered_list() -> None:
        nonlocal ordered_items
        if ordered_items:
            blocks.append("<ol>\n" + "\n".join(ordered_items) + "\n</ol>")
            ordered_items = []

    def flush_quote() -> None:
        nonlocal quote_lines
        if quote_lines:
            quote = " ".join(quote_lines)
            blocks.append(f"<blockquote><p>{inline_markdown(quote)}</p></blockquote>")
            quote_lines = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        if len(table_lines) < 2:
            paragraph.extend(table_lines)
            table_lines = []
            return
        rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table_lines]
        header = rows[0]
        body_rows = rows[2:] if re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", table_lines[1]) else rows[1:]
        head_html = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in header)
        body_html = "\n".join(
            "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
            for row in body_rows
        )
        blocks.append(f"<table>\n<thead><tr>{head_html}</tr></thead>\n<tbody>\n{body_html}\n</tbody>\n</table>")
        table_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        code = html.escape("\n".join(code_lines))
        blocks.append(f"<pre><code>{code}</code></pre>")
        code_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_quote()
            flush_table()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_table()
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_quote()
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_quote()
            table_lines.append(stripped)
            continue

        flush_table()

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_quote()
            blocks.append("<hr>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_quote()
            level = len(heading.group(1))
            text = inline_markdown(heading.group(2))
            blocks.append(f"<h{level}>{text}</h{level}>")
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            quote_lines.append(stripped.lstrip(">").strip())
            continue

        list_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if list_match:
            flush_paragraph()
            flush_ordered_list()
            flush_quote()
            list_items.append(f"<li>{inline_markdown(list_match.group(1))}</li>")
            continue

        ordered_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered_match:
            flush_paragraph()
            flush_list()
            flush_quote()
            ordered_items.append(f"<li>{inline_markdown(ordered_match.group(1))}</li>")
            continue

        flush_list()
        flush_ordered_list()
        flush_quote()
        paragraph.append(stripped)

    flush_table()
    flush_paragraph()
    flush_list()
    flush_ordered_list()
    flush_quote()
    if in_code:
        flush_code()

    return "\n".join(blocks)


def load_posts() -> list[Post]:
    posts: list[Post] = []
    for source in sorted(POSTS_DIR.glob("*/*.md")):
        year = source.parent.name
        meta, body = parse_front_matter(source.read_text(encoding="utf-8"))
        title = meta.get("title")
        date = meta.get("date")
        summary = meta.get("summary", "")
        slug = meta.get("slug") or slugify(title or source.stem)
        if not title or not date:
            raise ValueError(f"{source} must define title and date.")
        posts.append(
            Post(
                title=title,
                date=date,
                summary=summary,
                slug=slug,
                year=year,
                source=source,
                body_html=render_markdown(body),
            )
        )

    return sorted(posts, key=lambda post: post.date, reverse=True)


def page_template(title: str, description: str, body: str, depth: int) -> str:
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - {AUTHOR}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">

  <link rel="stylesheet" href="{prefix}assets/css/font_sans_serif.css">
  <link rel="stylesheet" href="{prefix}assets/css/theme-luka.css">
</head>
<body class="theme-luka">
  <nav class="top-nav">
    <div class="nav-container">
      <a class="nav-title" href="{prefix}index.html">{AUTHOR}</a>
      <div class="nav-links fancy" aria-label="Primary navigation">
        <a href="{prefix}index.html">Main</a>
        <a class="active" href="{prefix}writing/index.html">Writing</a>
      </div>
    </div>
  </nav>

{body}

  <script src="{prefix}assets/js/scale.fix.js"></script>
</body>
</html>
"""


def render_post(post: Post) -> str:
    footer = render_footer(depth=2)
    body = f"""  <div class="wrapper writing-layout">
    <main class="boxed">
      <article>
        <header class="article-header">
          <h1 class="article-title">{html.escape(post.title)}</h1>
          <p class="article-meta">
            by <strong>{AUTHOR}</strong>
            <span class="article-date">{html.escape(display_date(post.date))}</span>
          </p>
        </header>

        <hr>

        <div class="article-body fancy">
{post.body_html}
        </div>
      </article>
    </main>

{footer}
  </div>"""
    return page_template(post.title, post.summary, body, depth=2)


def render_footer(depth: int) -> str:
    prefix = "../" * depth
    return f"""    <footer class="site-footer">
      <p>
        &copy; 2026 {AUTHOR}. All rights reserved.
        <br>
        <span class="template-credit"><a href="https://github.com/Fanxyjumping/Xiaoyuf-homepage-template">Xiaoyuf Homepage Template</a> by <a href="{prefix}index.html">Xiaoyu Fan</a></span>
      </p>
    </footer>"""


def render_index(posts: list[Post]) -> str:
    years = sorted({post.year for post in posts}, reverse=True)
    year_links = "\n".join(f'          <a href="#{year}">{year}</a>' for year in years)

    sections: list[str] = []
    for year in years:
        year_posts = [post for post in posts if post.year == year]
        items = []
        for post in year_posts:
            href = f"{post.year}/{post.slug}.html"
            items.append(
                f"""            <li class="post-item">
              <p class="post-title fancy"><a href="{href}">{html.escape(post.title)}</a></p>
              <p class="post-date">{html.escape(display_date(post.date))}</p>
              <p class="post-summary">{html.escape(post.summary)}</p>
            </li>"""
            )
        sections.append(
            f"""        <section id="{year}" class="section">
          <h2 class="section-title">{year}</h2>
          <ol class="post-list">
{chr(10).join(items)}
          </ol>
        </section>"""
        )

    footer = render_footer(depth=1)
    body = f"""  <div class="wrapper writing-layout">
    <div class="writing-grid">
      <aside class="year-sidebar boxed">
        <div class="year-sidebar-title">By Year</div>
        <nav class="year-sidebar-links fancy" aria-label="Writing by year">
{year_links}
        </nav>
      </aside>

      <main class="boxed writing-content">
        <h1 class="page-title">Writing</h1>

        <p class="writing-intro">
          {html.escape(TAGLINE)}
        </p>

{chr(10).join(sections)}
      </main>
    </div>

{footer}
  </div>"""
    return page_template("Writing", f"Writing by {AUTHOR}.", body, depth=1)


def build() -> None:
    posts = load_posts()
    if not posts:
        raise SystemExit("No posts found under posts/<year>/*.md")

    for post in posts:
        out_dir = WRITING_DIR / post.year
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{post.slug}.html").write_text(render_post(post), encoding="utf-8")

    (WRITING_DIR / "index.html").write_text(render_index(posts), encoding="utf-8")

    for assets_dir in POSTS_DIR.glob("*/assets"):
        target = WRITING_DIR / assets_dir.parent.name / "assets"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(assets_dir, target)


if __name__ == "__main__":
    build()
