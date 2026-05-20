# Writing Workflow

Write Markdown posts in:

```text
posts/<year>/<slug>.md
```

Each post starts with front matter:

```md
---
title: My First Post
date: 2026-05-20
summary: A short summary of this post.
slug: my-first-post
---

Post body goes here.
```

Generate HTML once:

```bash
python3 scripts/build_posts.py
```

Preview locally:

```bash
python3 scripts/serve.py 8000
```

Auto-rebuild while writing:

```bash
python3 scripts/watch_posts.py
```

With the watcher running, save any file under `posts/`, then refresh the browser.
