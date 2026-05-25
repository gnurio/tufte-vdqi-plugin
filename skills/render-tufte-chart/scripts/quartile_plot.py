#!/usr/bin/env python3
"""
Render Tufte's redesigned box plot (VDQI pp.124-125: 'quartile plot') as a
standalone SVG. The box is erased; what remains is a single vertical stroke per
group spanning the full range, with the interquartile half OFFSET horizontally
from the median, and a small median tick. 'The straightedge need only be placed
on the paper once to draw the quartile plot' (Tufte).

Input: {group_name: [values, ...]} JSON.

Usage:
  python quartile_plot.py \\
    --data '{"A":[1,2,3,4,5,6,7,8,9,10],"B":[3,4,4,5,6,6,7,7,8,9]}' \\
    --title "Reaction time (ms) by condition" \\
    --out chart.svg
"""
import argparse, json, sys
from pathlib import Path

from _svg_text import TRUSTED_MARKER, svg_text


def quartiles(xs):
    xs = sorted(xs)
    n = len(xs)
    if n < 2:
        raise ValueError("each group needs at least 2 values")
    def pct(p):
        i = (n - 1) * p
        lo, hi = int(i), min(int(i) + 1, n - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
    return min(xs), pct(0.25), pct(0.5), pct(0.75), max(xs)


def render(groups, title, subtitle, width):
    items = list(groups.items())
    if not items:
        raise ValueError("no groups")
    stats = [(name, quartiles(vals)) for name, vals in items]
    ymin = min(s[1][0] for s in stats)
    ymax = max(s[1][4] for s in stats)
    if ymax == ymin:
        raise ValueError("data has no vertical range")

    ml, mr, mt, mb = 60, 24, 56, 56
    height = 460
    plot_h = height - mt - mb
    plot_w = width - ml - mr
    band = plot_w / len(stats)

    def sy(y): return mt + (ymax - y) / (ymax - ymin) * plot_h

    offset = 6  # horizontal offset of the IQR half-line, in px

    parts = [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
      f'font-family="et-book, ET-Bembo, Palatino, Georgia, serif" font-size="13">',
      TRUSTED_MARKER,
      f'<rect width="{width}" height="{height}" fill="white"/>',
      f'<text x="{ml}" y="28" font-size="17">{svg_text(title)}</text>',
    ]
    if subtitle:
        parts.append(f'<text x="{ml}" y="46" font-size="12" fill="#666">{svg_text(subtitle)}</text>')

    # range-frame y axis: line spans only data min..max, both ends labelled
    parts += [
      f'<line x1="{ml:.1f}" y1="{sy(ymin):.1f}" x2="{ml:.1f}" y2="{sy(ymax):.1f}" '
      f'stroke="#333" stroke-width="1"/>',
      f'<text x="{ml-8:.1f}" y="{sy(ymax)+4:.1f}" text-anchor="end" font-size="11" fill="#666">{ymax:g}</text>',
      f'<text x="{ml-8:.1f}" y="{sy(ymin)+4:.1f}" text-anchor="end" font-size="11" fill="#666">{ymin:g}</text>',
    ]
    for i, (name, (lo, q1, med, q3, hi)) in enumerate(stats):
        cx = ml + band * (i + 0.5)
        # full-range straightedge
        parts.append(f'<line x1="{cx:.1f}" y1="{sy(lo):.1f}" x2="{cx:.1f}" y2="{sy(hi):.1f}" '
                     f'stroke="#222" stroke-width="1"/>')
        # IQR: offset half-line emphasising the middle half
        parts.append(f'<line x1="{cx+offset:.1f}" y1="{sy(q1):.1f}" x2="{cx+offset:.1f}" y2="{sy(q3):.1f}" '
                     f'stroke="#222" stroke-width="2.2"/>')
        # median tick
        parts.append(f'<line x1="{cx-4:.1f}" y1="{sy(med):.1f}" x2="{cx+4:.1f}" y2="{sy(med):.1f}" '
                     f'stroke="#222" stroke-width="1.4"/>')
        # group label
        parts.append(f'<text x="{cx:.1f}" y="{height - mb + 18:.1f}" text-anchor="middle" font-size="12">{svg_text(name)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data"); p.add_argument("--data-file")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--width", type=int, default=720)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    try:
        raw = Path(a.data_file).read_text() if a.data_file else a.data
        if not raw:
            raise ValueError("provide --data or --data-file")
        groups = json.loads(raw)
        if not isinstance(groups, dict):
            raise ValueError("--data must be a JSON object mapping group name -> list of values")
        svg = render(groups, a.title, a.subtitle, a.width)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
    Path(a.out).write_text(svg)
    print(f"wrote {a.out} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
