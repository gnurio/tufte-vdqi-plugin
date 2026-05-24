---
name: render-tufte-chart
description: Produce a real, publication-ready data graphic (SVG or HTML) that obeys Tufte's principles — minimal ink, range-frame axes, direct labels, honest proportions. Use whenever someone wants to design, build, create, draw, or actually produce a chart the Tufte way, or to rebuild a chart after assessment found problems. This is the only skill in the toolkit that outputs an actual chart file.
---

# Render Tufte Chart

This skill produces an actual chart file. It is the toolkit's output stage: the
router sends "design / build / produce a chart" requests here, and an
optimisation workflow ends here (assess to diagnose, render to rebuild).

The old version of this skill shipped Python that called undefined functions and
could not run. It is replaced by a working script plus clear construction guidance.

## Build checklist (apply every time)

These bake in the principles from `references/tufte-principles.md` so the chart
never needs cleanup afterwards. Read that file for the full reasoning.

- **Honest proportions (B1).** Bars/columns start at a zero baseline. Encode a
  1-D quantity with length or position, never with 2-D area or 3-D volume.
- **Range-frame axes (B2).** Axis lines span exactly the data range, ends
  labelled; no outward padding. Exception: keep zero baseline for bar value axes.
- **Direct labels (B4).** Label lines at their endpoints and bars beside the bars;
  do not emit a separate legend.
- **Minimal ink (B5).** White background, no gridlines (or faint hairlines at
  major ticks only), no border box, no 3-D, no shadows, no gradients.
- **One encoding per datum (B6).** Don't restate a value with fill + border +
  label; keep the strongest channel.
- **Many series → small multiples (B3).** Repeat one shrunken design with shared
  scales rather than overplotting; order frames meaningfully.
- **Money over time (B7).** If the series is currency across years, convert to
  real terms first (use `assess-graphical-excellence/scripts/deflate.py` with
  retrieved CPI) and label the axis "real <base-year> <currency>".

## Pick the genre first

Before writing any code, check `references/tufte-principles.md` Part C and
choose Tufte's genre that fits the data shape. The toolkit ships a working
script for the four genres below; for the rest, build the SVG by hand
following Part C's recipe.

| Data shape | Tufte genre (Part C) | Script |
|---|---|---|
| 1 × N over time | C10 time-series | `render_line_svg.py` |
| K series indexed by a category | C5 small multiples | `small_multiples.py` |
| Distributions of K groups | C1 quartile plot | `quartile_plot.py` |
| Bivariate / scatter | C2 range frame (+ optional C3 dot-dash marginals) | `range_frame.py` |
| Categorical 1-value | C9 white-grid bar / C6 supertable | hand-build SVG |
| ≤20 numbers total | C6 supertable | hand-build HTML/SVG |
| Many variables, geographic | F (Minard / Snow / Cancer Atlas) | hand-build SVG |

If the data is ≤20 numbers, **prefer a table** (VDQI p.56) — say so to the user
before rendering. If forced to graph, use C6 supertable, not pie/bar.

## Multi-render rule (when to produce N alternatives)

When the assess step flagged a "Multi-render trigger" (data shape with more
than one correct Tufte answer), **render both alternatives side-by-side** in
one output, then let the user pick. This is the discipline that prevents
quiet defaulting to the obvious genre.

| Data shape | Render BOTH |
|---|---|
| 1 number / single ratio | (a) a one-sentence prose statement with the number inline, and (b) a tiny inline visual — a one-row proportion bar or a small two-color dot square |
| ≤20 numbers | (a) a C6 supertable (with optional table-graphic sparkline column), and (b) a single Tufte chart (C8 + C2 range-frame dot plot, or C9 white-grid bar) |
| Many series of one x | (a) a C5 small-multiples grid, and (b) an overplotted line/dot chart with direct end-labels |
| Distributions across groups | (a) a C1 quartile plot, and (b) a strip plot or histogram |
| Bivariate scatter | (a) a C2 range frame, and (b) the C3 dot-dash variant adding marginals |

For all other data shapes, render one canonical Tufte form (don't manufacture
alternatives when one obviously dominates). When emitting both alternatives,
state in one sentence why each exists and what to look at in each — the goal
is letting the reader see the toolkit's range, not flooding them with
near-duplicates.

## How to render

### Line / time-series (C10)

```
python scripts/render_line_svg.py \
  --data '[{"x":2000,"y":12.1},{"x":2023,"y":22.9}]' \
  --title "Revenue (real 2023 USD, M)" --series "Revenue" --out chart.svg
```

(Pass `--data-file path.json` for larger data. For monetary series, deflate the
values before passing them in.)

### Small multiples (C5) — "inevitably comparative, deftly multivariate"

Input is a flat list of records keyed by facet, x, and y:

```
python scripts/small_multiples.py \
  --data '[{"facet":"NA","x":1,"y":1000},{"facet":"EU","x":1,"y":900}, ...]' \
  --facet-key facet --x-key x --y-key y \
  --title "Daily active users by region" --cols 3 --out chart.svg
```

Frames are sorted by total y (descending) unless `--order "A,B,C"` is passed.
All frames share scales; axis end-labels appear only on the first frame to
avoid repeating ink.

### Quartile plot (C1) — Tufte's stripped-down box plot

Input is a JSON object mapping group name to list of values:

```
python scripts/quartile_plot.py \
  --data '{"Control":[2.3,2.5,...],"TreatmentA":[1.8,2.0,...]}' \
  --title "Reaction time (s) by condition" --out chart.svg
```

The box is erased; what remains is a single vertical stroke per group spanning
the full range, the IQR offset horizontally from it, and a median tick.

### Range-frame scatter (C2) — and optional dot-dash plot (C3)

```
python scripts/range_frame.py \
  --data '[{"x":1.2,"y":3.4},{"x":2.1,"y":4.5},...]' \
  --title "Body mass vs. wing span" \
  [--marginal-dash] --out chart.svg
```

`--marginal-dash` adds Tufte's dot-dash plot (VDQI p.133): marginal frequency
dashes along each axis framing the bivariate distribution.

### Other genres (bar, supertable, multivariate map, etc.)

Write the SVG/HTML directly, following Part C's recipe and the build checklist
above. Keep it a single self-contained file. A minimal pattern: white canvas,
thin dark data marks, range-frame axis lines with end labels, category/series
text placed on the marks, no grid/box.

## Optional: Tufte-styled HTML page

For a page that surrounds the chart with ET Book typography (and optional lede
text or caption), wrap the SVG with `scripts/wrap_html.py`. It uses the bundled
tufte-css (`assets/tufte-css/`, MIT-licensed) and copies the stylesheet and
fonts into a sibling `tufte-assets/` directory the first time so the result
opens correctly in any browser with no network:

```
python scripts/wrap_html.py \
  --svg chart.svg --out chart.html \
  --title "Revenue, 2000–2023" \
  --caption "Inflation-adjusted to 2023 USD using BLS CPI-U."
```

Use the SVG output when you need a portable single file (charts in a paper, a
slide deck, another site). Use the HTML wrapper when you want a self-contained,
browser-ready Tufte page (sharing a link, hosting a report). Pass `--no-assets`
if the page will be served from a site that already publishes `tufte.css` at
the expected path.

Always save the file and tell the user its path. Where useful, follow up with
`assess-graphical-excellence` to confirm the result scores well.

## What good looks like

A file that renders in a browser, carries no chartjunk, labels data directly, uses
honest proportions, and would itself pass an `assess-graphical-excellence` review.

## Related skills
- `assess-graphical-excellence` — diagnose a chart and get the remedies to apply here.
- `orchestrate-tufte-vdqi` — routes design/produce/fix requests to this skill.
