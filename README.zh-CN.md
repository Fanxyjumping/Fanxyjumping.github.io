<div align="center">

# Academic Homepage Template

### 一个纯静态个人学术主页模板，包含个人主页、论文展示和基于 Markdown 的 Writing 页面。

[English README](README.md) · [在线预览](https://fanxyjumping.github.io/Xiaoyuf-homepage-template/) · [使用此模板](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template/generate)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-c2714f?style=flat-square)](https://fanxyjumping.github.io/Xiaoyuf-homepage-template/)
[![Template Ready](https://img.shields.io/badge/Template-Ready-3d3929?style=flat-square)](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template/generate)
[![Stack](https://img.shields.io/badge/Stack-HTML%20%7C%20CSS%20%7C%20Python-e28a67?style=flat-square)](https://github.com/Fanxyjumping/Xiaoyuf-homepage-template)
[![License](https://img.shields.io/badge/License-MIT-8c8577?style=flat-square)](./LICENSE.md)

</div>

`Academic Homepage Template` 是一个纯静态个人学术主页模板，包含两个独立页面：

- `Main`：个人简介、教育经历、研究经历、动态、论文和项目。
- `Writing`：基于 Markdown 的轻量博客页面，支持按年份导航。

模板使用 HTML、CSS 和少量 Python 脚本，不依赖前端框架。

## 本地预览

```bash
python3 scripts/serve.py
```

然后打开：

```text
http://localhost:8000/
```

## 如何修改

优先修改这些文件：

- `index.html`：主页内容。
- `assets/css/theme-luka.css`：颜色、布局和字体样式。
- `assets/img/profile.svg`：头像占位图。
- `assets/img/institution.svg`：机构 logo 占位图。
- `assets/cv/CV.pdf`：如果需要提供简历，可以把文件放到这里。

## Writing 写作流程

把文章写成 Markdown 文件，放在：

```text
posts/<year>/<slug>.md
```

每篇文章需要 front matter：

```md
---
title: Example Post Title
date: 2026-02-01
summary: A short summary for the writing index.
slug: example-post
---
```

完整日期用于排序。页面上会显示为 `Feb 2026`。

生成 Writing 页面：

```bash
python3 scripts/build_posts.py
```

自动监听并重新生成：

```bash
python3 scripts/watch_posts.py
```

## 参考来源与署名

本模板基于以下项目二次开发：

- Luka Homepage Template: https://github.com/wzsyyh/luka-homepage-template

Writing 页面组织方式参考：

- Nicholas Carlini 的 Writing 页面: https://nicholas.carlini.com/writing/

详细说明见 `NOTICE.md`。

## 许可证

本模板以 MIT License 发布，并在 `LICENSE.md` 中保留上游 MIT license notice。
