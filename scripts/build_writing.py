#!/usr/bin/env python3
"""Build writing/*.html from the Markdown posts in content/.

Needs the markdown package. Run from the repo root: python3 scripts/build_writing.py
"""
import html
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

PAGE = """<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}, Yash Bishnoi</title>
  <meta name="description" content="{summary}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{summary}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://yashb98.github.io/writing/{slug}.html">
  <link rel="canonical" href="https://yashb98.github.io/writing/{slug}.html">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,600;1,400&family=Hepta+Slab:wght@450;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="band hero">
    <div class="margin">
      <p class="who"><a href="../index.html">Yash Bishnoi</a></p>
      <p class="where"><time datetime="{iso}">{published}</time></p>
    </div>
    <div class="main">
      <h1>{title}</h1>
    </div>
  </header>
  <main>
    <section class="band">
      <div class="margin"><p><a href="../index.html#writing">All writing</a></p></div>
      <div class="main article">
{body}
      </div>
    </section>
  </main>
  <footer class="band">
    <div class="margin"><h2><a href="../index.html">Back to home</a></h2></div>
    <div class="main">
      <p class="closing">If you're hiring for LLM training, kernels or inference, <a href="mailto:bishnoiyash274@gmail.com">email me</a>.</p>
    </div>
  </footer>
</body>
</html>
"""


def parse(path):
    _, front, body = path.read_text().split("---\n", 2)
    fields = dict(re.findall(r'^(\w+): "(.*)"$', front, flags=re.M))
    return fields, body


def build(path):
    fields, body = parse(path)
    day = date.fromisoformat(fields["date"])
    article = markdown.markdown(body, extensions=["fenced_code", "tables"])
    page = PAGE.format(
        title=html.escape(fields["title"]),
        summary=html.escape(fields["summary"], quote=True),
        slug=path.stem,
        iso=fields["date"],
        published=f"{day.day} {day:%B %Y}",
        body=article,
    )
    (ROOT / "writing" / f"{path.stem}.html").write_text(page)


def main():
    (ROOT / "writing").mkdir(exist_ok=True)
    for path in sorted((ROOT / "content").glob("*.md")):
        build(path)


if __name__ == "__main__":
    main()
