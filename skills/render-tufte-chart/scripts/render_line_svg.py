#!/usr/bin/env python3
"""
Render a Tufte-style line chart as a standalone SVG file. REAL, runnable code —
it replaces the old skill's undefined stubs (estimate_total_ink, generate_line_chart).

Tufte choices baked in (see references): white background, one thin line, NO
gridlines, a range-frame value axis (the axis line spans only data min..max, with
those two values labelled), the year span labelled at the ends of the x-axis, and
the series labelled directly at its right endpoint instead of a legend.

Usage:
  python render_line_svg.py \
    --data '[{"x":2000,"y":12.1},{"x":2010,"y":18.4},{"x":2023,"y":22.9}]' \
    --title "Revenue (real 2023 USD, millions)" \
    --series "Revenue" \
    --out chart.svg
  # or read data from a file with --data-file path.json
"""
import argparse, json, sys

from _svg_text import TRUSTED_MARKER, svg_text


def render(data, title, series="", subtitle="", width=760, height=420):
    pts = sorted(data, key=lambda d: d["x"])
    if len(pts) < 2:
        raise ValueError("need at least two data points")
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    if xmax == xmin or ymax == ymin:
        raise ValueError("x and y must each span a range")

    # margins leave room for axis-end labels and the direct series label
    ml, mr, mt, mb = 64, 96, 56, 48
    pw, ph = width - ml - mr, height - mt - mb

    def sx(x): return ml + (x - xmin) / (xmax - xmin) * pw
    def sy(y): return mt + (ymax - y) / (ymax - ymin) * ph

    poly = " ".join(f"{sx(p['x']):.1f},{sy(p['y']):.1f}" for p in pts)
    end = pts[-1]
    fmt = (lambda v: f"{v:g}")

    svg = [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
      f'font-family="et-book, ET-Bembo, Palatino, Georgia, serif" font-size="13">',
      TRUSTED_MARKER,
      f'<rect width="{width}" height="{height}" fill="white"/>',
      f'<text x="{ml}" y="28" font-size="17">{svg_text(title)}</text>',
    ]
    if subtitle:
        svg.append(f'<text x="{ml}" y="46" font-size="12" fill="#666">{svg_text(subtitle)}</text>')

    # range-frame value (y) axis: line spans only data min..max, both ends labelled
    svg += [
      f'<line x1="{ml:.1f}" y1="{sy(ymin):.1f}" x2="{ml:.1f}" y2="{sy(ymax):.1f}" '
      f'stroke="#333" stroke-width="1"/>',
      f'<text x="{ml-8:.1f}" y="{sy(ymax)+4:.1f}" text-anchor="end">{fmt(ymax)}</text>',
      f'<text x="{ml-8:.1f}" y="{sy(ymin)+4:.1f}" text-anchor="end">{fmt(ymin)}</text>',
      # x range frame: line spans data, ends labelled (the year span)
      f'<line x1="{sx(xmin):.1f}" y1="{height-mb:.1f}" x2="{sx(xmax):.1f}" '
      f'y2="{height-mb:.1f}" stroke="#333" stroke-width="1"/>',
      f'<text x="{sx(xmin):.1f}" y="{height-mb+18:.1f}" text-anchor="middle">{fmt(xmin)}</text>',
      f'<text x="{sx(xmax):.1f}" y="{height-mb+18:.1f}" text-anchor="middle">{fmt(xmax)}</text>',
      # the data line: thin, dark, no markers, no grid
      f'<polyline points="{poly}" fill="none" stroke="#222" stroke-width="1.4"/>',
    ]
    if series:
        svg.append(
          f'<text x="{sx(end["x"])+6:.1f}" y="{sy(end["y"])+4:.1f}" fill="#222">{svg_text(series)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data"); p.add_argument("--data-file")
    p.add_argument("--title", default="")
    p.add_argument("--series", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    try:
        raw = open(a.data_file).read() if a.data_file else a.data
        if not raw:
            raise ValueError("provide --data or --data-file")
        data = json.loads(raw)
        svg = render(data, a.title, a.series, a.subtitle)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
    with open(a.out, "w") as f:
        f.write(svg)
    print(f"wrote {a.out} ({len(svg)} bytes, {a.out.rsplit('.',1)[-1]})")


if __name__ == "__main__":
    main()
