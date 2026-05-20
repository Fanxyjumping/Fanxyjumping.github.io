<div align="center">

# Academic Homepage Template

### A static academic homepage template with a personal profile, publication section, and Markdown-based writing page.

[中文说明](README.zh-CN.md) · [Live Demo](https://fanxyjumping.github.io/Xiaoyuf-homepage-template/) · [Use This Template](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template/generate)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-c2714f?style=flat-square)](https://fanxyjumping.github.io/Xiaoyuf-homepage-template/)
[![Template Ready](https://img.shields.io/badge/Template-Ready-3d3929?style=flat-square)](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template/generate)
[![Stack](https://img.shields.io/badge/Stack-HTML%20%7C%20CSS%20%7C%20Python-e28a67?style=flat-square)](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template)
[![License](https://img.shields.io/badge/License-MIT-8c8577?style=flat-square)](./LICENSE.md)

</div>

`Academic Homepage Template` is a static personal academic homepage template with a two-page structure:

- `Main`: profile, education, experience, news, publications, and projects.
- `Writing`: a lightweight Markdown-based blog with year navigation.

The template is plain HTML, CSS, and Python scripts. It does not require a frontend framework.

## Preview Locally

```bash
python3 scripts/serve.py
```

Then open:

```text
http://localhost:8000/
```

## Customize

Edit these files first:

- `index.html`: main homepage content.
- `assets/css/theme-luka.css`: colors, layout, and typography.
- `assets/img/profile.svg`: profile image placeholder.
- `assets/img/institution.svg`: institution logo placeholder.
- `assets/cv/CV.pdf`: your CV file, if you want to provide one.

## Writing Workflow

Write posts as Markdown files under:

```text
posts/<year>/<slug>.md
```

Each post needs front matter:

```md
---
title: Example Post Title
date: 2026-02-01
summary: A short summary for the writing index.
slug: example-post
---
```

The full date is used for sorting. Pages display dates as `Feb 2026`.

Build writing pages:

```bash
python3 scripts/build_posts.py
```

Or watch and rebuild automatically:

```bash
python3 scripts/watch_posts.py
```

## Structure

```text
.
├── index.html
├── writing/
├── posts/
├── scripts/
├── assets/
│   ├── css/
│   ├── cv/
│   ├── img/
│   └── js/
├── LICENSE.md
├── NOTICE.md
└── README.md
```

## Attribution

This template is adapted from:

- Luka Homepage Template: https://github.com/wzsyyh/luka-homepage-template

The writing page organization is inspired by:

- Nicholas Carlini's writing page: https://nicholas.carlini.com/writing/

See `NOTICE.md` for details.

## License

Released under the MIT License. The upstream MIT notice is preserved in `LICENSE.md`.
