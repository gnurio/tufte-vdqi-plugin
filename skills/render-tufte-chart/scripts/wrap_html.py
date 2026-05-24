#!/usr/bin/env python3
"""
Wrap a Tufte-style SVG in an HTML page that uses tufte-css typography
(ET Book font, generous margins, optional margin notes).

Inputs an existing .svg file (typically produced by render_line_svg.py or
written by hand following the build checklist). Outputs an .html page that
inlines the SVG inside an <article>/<figure class="fullwidth"> and links to
the vendored tufte.css next to it. Copies tufte.css + the et-book/ fonts into
a sibling `tufte-assets/` directory the first time so the page renders
correctly when opened locally with no network.

Usage:
  python wrap_html.py \
    --svg chart.svg --out chart.html \
    --title "Revenue (real 2023 USD, M)" \
    --caption "Inflation-adjusted using BLS CPI-U." \
    [--intro "Optional lede paragraph above the figure."]

Add `--no-assets` to skip the asset copy (use when the page is being served
from a site that already publishes tufte.css at the expected path).
"""
import argparse, os, shutil, sys
from html import escape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VENDORED_CSS_DIR = SCRIPT_DIR.parent / "assets" / "tufte-css"
ASSETS_SUBDIR = "tufte-assets"


def ensure_assets(out_html: Path) -> str:
    """Copy tufte.css and et-book/ next to the output HTML if missing. Returns
    the relative href to use in the <link> tag."""
    dest = out_html.parent / ASSETS_SUBDIR
    dest.mkdir(parents=True, exist_ok=True)
    css_src = VENDORED_CSS_DIR / "tufte.css"
    fonts_src = VENDORED_CSS_DIR / "et-book"
    if not css_src.exists() or not fonts_src.exists():
        raise FileNotFoundError(
            f"Vendored tufte-css not found at {VENDORED_CSS_DIR}. "
            "The skill ships these assets — reinstall the plugin or restore them.")
    css_dest = dest / "tufte.css"
    if not css_dest.exists():
        shutil.copy2(css_src, css_dest)
    fonts_dest = dest / "et-book"
    if not fonts_dest.exists():
        shutil.copytree(fonts_src, fonts_dest)
    return f"{ASSETS_SUBDIR}/tufte.css"


def strip_xml_decl(svg: str) -> str:
    """Inlined SVG must not carry a <?xml ...?> processing instruction."""
    s = svg.lstrip()
    if s.startswith("<?xml"):
        end = s.find("?>")
        if end != -1:
            s = s[end + 2:].lstrip()
    return s


def build_html(title: str, intro: str, svg: str, caption: str, css_href: str) -> str:
    intro_html = f'<p>{escape(intro)}</p>' if intro else ""
    caption_html = f'<figcaption>{escape(caption)}</figcaption>' if caption else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title) if title else 'Tufte chart'}</title>
<link rel="stylesheet" href="{escape(css_href)}">
<style>
  /* let the chart breathe inside tufte-css's narrow column */
  figure.fullwidth svg {{ display: block; width: 100%; height: auto; }}
</style>
</head>
<body>
<article>
{f'<h1>{escape(title)}</h1>' if title else ''}
{intro_html}
<figure class="fullwidth">
{svg}
{caption_html}
</figure>
</article>
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--svg", required=True, help="path to the SVG to wrap")
    p.add_argument("--out", required=True, help="path to write the .html file")
    p.add_argument("--title", default="", help="page title and <h1>")
    p.add_argument("--caption", default="", help="figcaption text under the chart")
    p.add_argument("--intro", default="", help="optional lede paragraph above the figure")
    p.add_argument("--no-assets", action="store_true",
                   help="skip copying tufte.css and et-book/ next to the output")
    a = p.parse_args()

    try:
        svg_text = Path(a.svg).read_text()
    except OSError as e:
        print(f"ERROR: cannot read SVG {a.svg}: {e}", file=sys.stderr)
        sys.exit(1)

    out_html = Path(a.out)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    try:
        css_href = (f"{ASSETS_SUBDIR}/tufte.css" if a.no_assets
                    else ensure_assets(out_html))
    except (OSError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    html = build_html(a.title, a.intro, strip_xml_decl(svg_text), a.caption, css_href)
    out_html.write_text(html)
    print(f"wrote {out_html} ({len(html)} bytes)")
    if not a.no_assets:
        print(f"assets at {out_html.parent / ASSETS_SUBDIR}/  (open the HTML in any browser)")


if __name__ == "__main__":
    main()
