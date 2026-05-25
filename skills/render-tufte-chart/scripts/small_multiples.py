#!/usr/bin/env python3
"""
Render a Tufte-style small-multiples grid of line charts as a standalone SVG.
Implements VDQI's small-multiples recipe (pp.42, 170, 175): the same graphical
design structure is repeated for each frame, so attention is devoted entirely
to shifts in the data. Shared scales, invariant style, direct frame labels, no
legend, range-frame axes per frame, no gridlines.

Input data is a flat list of records, each with three keys: the facet, the x,
and the y. Facets are sorted by total y descending unless --order is supplied.

Usage:
  python small_multiples.py \\
    --data '[{"facet":"NA","x":1,"y":1000},{"facet":"NA","x":2,"y":1050},
             {"facet":"EU","x":1,"y":900}, {"facet":"EU","x":2,"y":920}]' \\
    --facet-key facet --x-key x --y-key y \\
    --title "Daily active users by region" \\
    --cols 3 --out chart.svg
"""
import argparse, json, math, sys
from pathlib import Path

from _svg_text import TRUSTED_MARKER, svg_text


def render(data, facet_key, x_key, y_key, title, subtitle, cols, order, width):
    facets = {}
    for d in data:
        facets.setdefault(d[facet_key], []).append((d[x_key], d[y_key]))
    for k in facets:
        facets[k].sort(key=lambda p: p[0])
    if not facets:
        raise ValueError("no facets in data")

    if order:
        names = [n for n in order if n in facets]
        names += [n for n in facets if n not in names]
    else:
        names = sorted(facets, key=lambda n: -sum(y for _, y in facets[n]))

    n = len(names)
    cols = max(1, min(cols, n))
    rows = math.ceil(n / cols)

    xs_all = [x for pts in facets.values() for x, _ in pts]
    ys_all = [y for pts in facets.values() for _, y in pts]
    xmin, xmax, ymin, ymax = min(xs_all), max(xs_all), min(ys_all), max(ys_all)
    if xmax == xmin or ymax == ymin:
        raise ValueError("x and y must each span a range across the dataset")

    pad_top, pad_bot, pad_lr = 64, 36, 32
    cell_w = (width - 2 * pad_lr) / cols
    cell_h = cell_w * 0.62
    height = pad_top + pad_bot + rows * cell_h + (rows - 1) * 18

    inset_l, inset_r, inset_t, inset_b = 36, 16, 22, 22

    def cell_origin(i):
        r, c = divmod(i, cols)
        return pad_lr + c * cell_w, pad_top + r * (cell_h + 18)

    def sx(cx, x): return cx + inset_l + (x - xmin) / (xmax - xmin) * (cell_w - inset_l - inset_r)
    def sy(cy, y): return cy + inset_t + (ymax - y) / (ymax - ymin) * (cell_h - inset_t - inset_b)

    fmt = (lambda v: f"{v:g}")

    parts = [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {int(height)}" '
      f'font-family="et-book, ET-Bembo, Palatino, Georgia, serif" font-size="12">',
      TRUSTED_MARKER,
      f'<rect width="{width}" height="{int(height)}" fill="white"/>',
      f'<text x="{pad_lr}" y="28" font-size="17">{svg_text(title)}</text>',
    ]
    if subtitle:
        parts.append(f'<text x="{pad_lr}" y="46" font-size="12" fill="#666">{svg_text(subtitle)}</text>')

    for i, name in enumerate(names):
        cx, cy = cell_origin(i)
        pts = facets[name]
        poly = " ".join(f"{sx(cx, x):.1f},{sy(cy, y):.1f}" for x, y in pts)
        parts += [
          f'<text x="{cx + inset_l:.1f}" y="{cy + 14:.1f}" font-size="12" fill="#222">{svg_text(name)}</text>',
          # range-frame y axis (data min..max only)
          f'<line x1="{cx + inset_l:.1f}" y1="{sy(cy, ymin):.1f}" '
          f'x2="{cx + inset_l:.1f}" y2="{sy(cy, ymax):.1f}" stroke="#444" stroke-width="0.8"/>',
          # range-frame x axis (data min..max only)
          f'<line x1="{sx(cx, xmin):.1f}" y1="{cy + cell_h - inset_b:.1f}" '
          f'x2="{sx(cx, xmax):.1f}" y2="{cy + cell_h - inset_b:.1f}" stroke="#444" stroke-width="0.8"/>',
          # one thin data line, no markers
          f'<polyline points="{poly}" fill="none" stroke="#222" stroke-width="1.1"/>',
        ]
        # axis end labels — only on the first frame to avoid repeating
        if i == 0:
            parts += [
              f'<text x="{cx + inset_l - 4:.1f}" y="{sy(cy, ymax) + 3:.1f}" '
              f'text-anchor="end" font-size="10" fill="#666">{fmt(ymax)}</text>',
              f'<text x="{cx + inset_l - 4:.1f}" y="{sy(cy, ymin) + 3:.1f}" '
              f'text-anchor="end" font-size="10" fill="#666">{fmt(ymin)}</text>',
              f'<text x="{sx(cx, xmin):.1f}" y="{cy + cell_h - inset_b + 12:.1f}" '
              f'text-anchor="middle" font-size="10" fill="#666">{fmt(xmin)}</text>',
              f'<text x="{sx(cx, xmax):.1f}" y="{cy + cell_h - inset_b + 12:.1f}" '
              f'text-anchor="middle" font-size="10" fill="#666">{fmt(xmax)}</text>',
            ]
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data"); p.add_argument("--data-file")
    p.add_argument("--facet-key", default="facet")
    p.add_argument("--x-key", default="x")
    p.add_argument("--y-key", default="y")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--order", help="comma-separated facet order (overrides default ranking)")
    p.add_argument("--width", type=int, default=820)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    try:
        raw = Path(a.data_file).read_text() if a.data_file else a.data
        if not raw:
            raise ValueError("provide --data or --data-file")
        data = json.loads(raw)
        order = [s.strip() for s in a.order.split(",")] if a.order else None
        svg = render(data, a.facet_key, a.x_key, a.y_key, a.title, a.subtitle,
                     a.cols, order, a.width)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
    Path(a.out).write_text(svg)
    print(f"wrote {a.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
