#!/usr/bin/env python3
"""Render data/results.json into index.html between the results markers.

Run from the repo root after changing the data: python3 scripts/render_results.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data/results.json").read_text())
LOW, HIGH = DATA["domain"]
BLOB = f"https://github.com/{DATA['repo']}/blob/{DATA['commit']}/"


def pct(x):
    return f"{(x - LOW) / (HIGH - LOW) * 100:.2f}%"


def signed(x, places):
    return f"{x:+.{places}f}".replace("-", "−")


def clears_zero(cell):
    return cell["ci"][0] > 0 or cell["ci"][1] < 0


def interval(cell):
    return f"{signed(cell['ci'][0], 3)} to {signed(cell['ci'][1], 3)}"


def kind_of(cell):
    return "effect" if clears_zero(cell) else "null"


def plot(cell, corpus, name):
    lo, hi = cell["ci"]
    kind = kind_of(cell)
    width = (hi - lo) / (HIGH - LOW) * 100
    label = f"{corpus}: {signed(cell['value'], 3)}, 95% interval {interval(cell)}"
    seeds = "".join(f'<i class="fp-seed" style="left:{pct(s)}"></i>' for s in cell["seeds"])
    return (
        f'<span class="fp-plot cell-{name}" role="img" aria-label="{label}" title="{label}">'
        f'<i class="fp-ci {kind}" style="left:{pct(lo)};width:{width:.2f}%"></i>'
        f'<i class="fp-pt {kind}" style="left:{pct(cell["value"])}"></i>'
        f"{seeds}</span>"
    )


def seed_list(cell):
    return ", ".join(signed(s, 3) for s in cell["seeds"])


def source_links(item):
    links = [f'<a href="{BLOB}{item["source"]}">Results file</a>']
    for link in item.get("links", []):
        base = f"https://github.com/{DATA['repo']}/blob/{link.get('commit', DATA['commit'])}/"
        links.append(f'<a href="{base}{link["path"]}">{link["label"]}</a>')
    return " and ".join(links)


def row(item):
    english, code = item["english"], item["code"]
    return f"""<details class="fp-row" data-english="{kind_of(english)}" data-code="{kind_of(code)}">
  <summary>
    <span class="fp-name">{html.escape(item["name"])}<small>{html.escape(item["budget"])}</small></span>
    {plot(english, "English", "english")}
    <span class="fp-val cell-english">{signed(english["value"], 3)}</span>
    {plot(code, "Code", "code")}
    <span class="fp-val cell-code">{signed(code["value"], 3)}</span>
  </summary>
  <div class="fp-note">
    <p>{html.escape(item["note"])}</p>
    <p class="fp-source">English {signed(english["value"], 3)}, interval {interval(english)}, seeds {seed_list(english)}.</p>
    <p class="fp-source">Code {signed(code["value"], 3)}, interval {interval(code)}, seeds {seed_list(code)}.</p>
    <p class="fp-source">{source_links(item)}</p>
  </div>
</details>"""


def axis():
    ticks = "".join(
        f'<span class="fp-tick" style="left:{pct(t)}">{t:g}</span>' for t in DATA["ticks"]
    )
    return f"""<div class="fp-head" aria-hidden="true">
  <span class="fp-name"></span>
  <span class="fp-axis cell-english"><b>English text</b>{ticks}</span>
  <span class="fp-val cell-english"></span>
  <span class="fp-axis cell-code"><b>Python code</b>{ticks}</span>
  <span class="fp-val cell-code"></span>
</div>"""


def table_row(item):
    cells = "".join(
        f"<td>{signed(c['value'], 4)}</td><td>{signed(c['ci'][0], 4)} to {signed(c['ci'][1], 4)}</td>"
        for c in (item["english"], item["code"])
    )
    return (
        f'<tr><th scope="row">{html.escape(item["name"])}</th>'
        f'<td>{html.escape(item["budget"])}</td>{cells}'
        f'<td><a href="{BLOB}{item["source"]}">Results file</a></td></tr>'
    )


def table():
    body = "\n".join(table_row(item) for item in DATA["rows"])
    return f"""<details class="fp-table">
  <summary>Show these results as a table</summary>
  <div class="fp-table-scroll">
  <table>
    <thead><tr><th scope="col">Change</th><th scope="col">Budget</th><th scope="col">English</th><th scope="col">95% interval</th><th scope="col">Code</th><th scope="col">95% interval</th><th scope="col">Source</th></tr></thead>
    <tbody>
{body}
    </tbody>
  </table>
  </div>
</details>"""


def main():
    zero = pct(0)
    rows = "\n".join(row(item) for item in DATA["rows"])
    block = f"""<!-- results:start -->
<div class="fp" style="--zero:{zero}">
{axis()}
{rows}
</div>
{table()}
<!-- results:end -->"""
    page = ROOT / "index.html"
    text = page.read_text()
    updated, count = re.subn(
        r"<!-- results:start -->.*<!-- results:end -->",
        lambda _: block,
        text,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("results markers not found in index.html")
    page.write_text(updated)


if __name__ == "__main__":
    main()
