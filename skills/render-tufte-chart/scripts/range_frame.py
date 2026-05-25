#!/usr/bin/env python3
"""
Render a Tufte-style range-frame scatterplot (VDQI pp.130-132) as a standalone
SVG. 'The frame lines should extend only to the measured limits of the data
rather than ... to some arbitrary point like the next round number' (Tufte).
Axis lines span exactly the data range with both endpoints labelled.

Optional --marginal-dash adds a dot-dash plot (VDQI p.133): marginal frequency
dashes along each axis, framing the bivariate distribution.

Usage:
  python range_frame.py \\
    --data '[{"x":1.2,"y":3.4},{"x":2.1,"y":4.5},{"x":3.8,"y":5.1}]' \\
    --title "Body mass vs. wing span" \\
    [--marginal-dash] --out chart.svg
"""
import argparse, json, sys
from pathlib import Path

from _svg_text import TRUSTED_MARKER, svg_text


def render(data, title, subtitle, marginal_dash, width, height):
    pts = [(d["x"], d["y"]) for d in data]
    if len(pts) < 2:
        raise ValueError("need at least two points")
    xs, ys = zip(*pts)
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    if xmax == xmin or ymax == ymin:
        raise ValueError("x and y must each span a range")

    ml, mr, mt, mb = 56, 36, 56, 56
    pw, ph = width - ml - mr, height - mt - mb

    def sx(x): return ml + (x - xmin) / (xmax - xmin) * pw
    def sy(y): return mt + (ymax - y) / (ymax - ymin) * ph

    fmt = (lambda v: f"{v:g}")

    parts = [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
      f'font-family="et-book, ET-Bembo, Palatino, Georgia, serif" font-size="13">',
      TRUSTED_MARKER,
      f'<rect width="{width}" height="{height}" fill="white"/>',
      f'<text x="{ml}" y="28" font-size="17">{svg_text(title)}</text>',
    ]
    if subtitle:
        parts.append(f'<text x="{ml}" y="46" font-size="12" fill="#666">{svg_text(subtitle)}</text>')

    # range-frame axes — span only the data range
    parts += [
      f'<line x1="{ml:.1f}" y1="{sy(ymin):.1f}" x2="{ml:.1f}" y2="{sy(ymax):.1f}" '
      f'stroke="#333" stroke-width="1"/>',
      f'<line x1="{sx(xmin):.1f}" y1="{height-mb:.1f}" x2="{sx(xmax):.1f}" y2="{height-mb:.1f}" '
      f'stroke="#333" stroke-width="1"/>',
      # axis endpoint labels
      f'<text x="{ml-8:.1f}" y="{sy(ymax)+4:.1f}" text-anchor="end" font-size="11" fill="#666">{fmt(ymax)}</text>',
      f'<text x="{ml-8:.1f}" y="{sy(ymin)+4:.1f}" text-anchor="end" font-size="11" fill="#666">{fmt(ymin)}</text>',
      f'<text x="{sx(xmin):.1f}" y="{height-mb+16:.1f}" text-anchor="middle" font-size="11" fill="#666">{fmt(xmin)}</text>',
      f'<text x="{sx(xmax):.1f}" y="{height-mb+16:.1f}" text-anchor="middle" font-size="11" fill="#666">{fmt(xmax)}</text>',
    ]

    # data points
    for x, y in pts:
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="2.5" fill="#222"/>')

    # optional marginal dashes (dot-dash plot, VDQI p.133)
    if marginal_dash:
        dash_len = 6
        # x-axis marginal: dashes below the x-axis at each unique x
        y_dash_top = height - mb + 4
        for x, _ in pts:
            parts.append(f'<line x1="{sx(x):.1f}" y1="{y_dash_top:.1f}" '
                         f'x2="{sx(x):.1f}" y2="{y_dash_top + dash_len:.1f}" '
                         f'stroke="#666" stroke-width="0.8"/>')
        # y-axis marginal: dashes left of the y-axis at each unique y
        x_dash_right = ml - 4
        for _, y in pts:
            parts.append(f'<line x1="{x_dash_right - dash_len:.1f}" y1="{sy(y):.1f}" '
                         f'x2="{x_dash_right:.1f}" y2="{sy(y):.1f}" '
                         f'stroke="#666" stroke-width="0.8"/>')

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data"); p.add_argument("--data-file")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--marginal-dash", action="store_true",
                   help="add marginal frequency dashes (dot-dash plot, VDQI p.133)")
    p.add_argument("--width", type=int, default=720)
    p.add_argument("--height", type=int, default=480)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    try:
        raw = Path(a.data_file).read_text() if a.data_file else a.data
        if not raw:
            raise ValueError("provide --data or --data-file")
        data = json.loads(raw)
        svg = render(data, a.title, a.subtitle, a.marginal_dash, a.width, a.height)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
    Path(a.out).write_text(svg)
    print(f"wrote {a.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
