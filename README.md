# yashb98.github.io

Yash Bishnoi's portfolio. A static site with no build step, served by GitHub Pages from the root of `main`.

Edit `index.html` for text and `styles.css` for design. The results chart is generated, so change it in `data/results.json` and then run:

```bash
python3 scripts/render_results.py
```

Posts live in `content/`. After changing one, run this, which needs the `markdown` package:

```bash
python3 scripts/build_writing.py
```

To preview locally:

```bash
python3 -m http.server 8000
```
