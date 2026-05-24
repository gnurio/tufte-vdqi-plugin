# Tufte Principles Reference

This file is the canonical encoding of the Tufte techniques that used to live in
seven separate skills (calculate-lie-factor, generate-range-frames,
construct-small-multiples, integrate-text-and-graphic, erase-non-data-ink,
erase-redundant-data-ink, standardize-monetary-units). They were merged here
because each one held a single idea the model already applies well; keeping them
as separate routing targets added latency and brittle code without raising answer
quality. The *knowledge* is preserved in full below.

Two skills consult this file:
- `assess-graphical-excellence` uses Part A to score a graphic and Part B to turn
  each violation into a concrete remedy.
- `render-tufte-chart` uses Part B as a build checklist so it never introduces
  these problems in the first place.

When you diagnose a problem in Part A, name the matching remedy from Part B by its
number so the reader knows exactly what to change.

---

## Part A — The nine criteria for graphical excellence

Score each 0–10 and justify the score with a specific observation. The weights
reflect that honesty matters more than elegance.

| # | Criterion | Weight | What a low score looks like | Remedy (Part B) |
|---|-----------|:------:|-----------------------------|-----------------|
| 1 | Integrity | 3× | Truncated axis, distorted areas, missing baseline, cherry-picked range | B1 |
| 2 | Proportionality | 2× | Visual magnitude ≠ data magnitude; 2-D/3-D area or volume distortion | B1 |
| 3 | Data-ink ratio | 2× | Heavy grids, backgrounds, borders, 3-D, shadows dominate the data marks | B5 |
| 4 | Minimal/redundant ink | 1× | The same datum encoded several ways (height + color + label + border) | B6 |
| 5 | Data density | 1× | One sparse chart where small multiples would pack far more comparison | B3 |
| 6 | Integration | 1× | Separate legend the eye must dart to; labels detached from their marks | B4 |
| 7 | Context | 1× | No baseline, no comparison, no time frame; monetary series left nominal | B2, B7 |
| 8 | Clarity | 1× | Ambiguous, congested, or unlabeled; reader cannot tell what they see | B4 |
| 9 | Typography | 0.5× | Decorative or illegible type; labels stranded in a key | B4 |

Overall score = weighted average. Prioritise recommendations by impact: fix
integrity and proportionality first, then data-ink, then the rest.

Common grading mistake: do not confuse a *design flaw* (ugly but honest) with an
*integrity violation* (the graphic misleads). Reserve the lowest integrity scores
for graphics that cause the reader to misread the numbers.

---

## Part B — The remedies (the seven merged techniques)

### B1 — Lie factor (was: calculate-lie-factor)

The lie factor measures how far the visual exaggerates or understates the data.

    lie_factor = (percentage change shown in the graphic) / (percentage change in the data)

- Acceptable range: **0.95 to 1.05**. Outside it, the graphic distorts.
- > 1 overstates the data; < 1 understates it.
- Use absolute values; direction does not matter for the ratio.
- If the data change is 0, the ratio is undefined — say so rather than dividing.

Dimensional trap: if a quantity is encoded by an *area*, doubling the data must
double the area, not the side length (2× length = 4× area). For *volume*,
2× length = 8× volume. Encoding a 1-D quantity with a 2-D or 3-D object is a
classic proportionality violation.

Bar charts: the bar length encodes magnitude from zero, so the baseline **must**
be zero. A non-zero bar baseline is an automatic integrity failure (this is the
single most common real-world distortion). Line charts may use a non-zero range
(see B2) because they encode change, not magnitude.

Worked example: standards rise 18 → 27.5 mpg (+53%) but the drawn line grows
783%. lie_factor = 783 / 53 ≈ 14.8 → severe overstatement.

### B2 — Range frames (was: generate-range-frames)

Trim each axis line so it spans exactly the data's minimum to maximum, and let the
axis endpoints state those values. This turns dead structural ink into
data-carrying ink and stops the data from being squashed into a corner.

- Scatter/line: set axis bounds to the exact data range. **Do not add padding or
  round outward** — padded bounds (e.g. data 20–80 shown on 15–85) defeat the
  purpose. The whole point is that the frame reports the true extent.
- Mark the min and max values at the ends of the axis; interior ticks only if they
  earn their place.
- Exception: bar/column charts keep a zero baseline (see B1) — do not range-frame
  the value axis of bars.
- Single point (min == max): keep conventional axes; a range frame needs a range.

Worked example: scatter with X 20–80, Y 15–65 on 0–100 axes → trim to exactly
X 20–80, Y 15–65.

### B3 — Small multiples (was: construct-small-multiples)

To compare many series, repeat one small graphic with an **invariant design** so
the only thing that changes between frames is the data.

- Identical scales, colors, line weight, markers, and size across every frame.
  Shared axes are non-negotiable; per-frame auto-scaling destroys comparability.
- Shrink each frame to raise data density; verify legibility at target size.
- Order frames logically: by a meaningful rank (e.g. descending total) or by
  geography/time, never alphabetically by accident.
- Grid sizing: 2–4 frames → one row/column; 5–9 → 2–3 rows; 10+ → 3+ rows,
  consider pagination. (Six frames → 2×3 or 3×2.)
- Label each frame directly (B4); do not add a shared legend.

### B4 — Integrate text and graphic (was: integrate-text-and-graphic)

Put labels on the data, not in a remote key, so the eye never has to dart away and
back.

- Line charts: label each line at its right-hand endpoint, in the line's color;
  stagger or use a short leader if endpoints collide.
- Bar charts: category names beside/under the bars; a value on a bar only if the
  exact figure matters and cannot be read from the axis.
- Scatter: label notable points/clusters directly; annotate outliers in place.
- Delete the legend box, its border, and its swatches once labels are direct.
- Only when direct labeling is truly impossible (very dense scatter) fall back to a
  compact marginal key, kept as close to the data as possible.

### B5 — Erase non-data-ink (was: erase-non-data-ink)

Remove ink that carries no statistical information. For each element ask: "does
removing this delete any data?" If no, remove or lighten it.

- Remove/flatten: heavy gridlines (drop or reduce to faint hairlines at major
  ticks only), background fills (make white/transparent), chart borders/boxes,
  3-D effects, drop shadows, gradients, decorative textures and moiré.
- Preserve: the data marks (bars, lines, points), essential axis lines (may be
  thinned), and the labels that let the reader read values.
- Exception: a lookup table that needs fine rules for precise reading may keep them.

### B6 — Erase redundant data-ink (was: erase-redundant-data-ink)

If one datum is encoded N ways, remove N−1. Keep the single strongest encoding.

- Position along a common scale (bar height, point location) is the most precise
  channel — keep it.
- Drop duplicate encodings of the same value: fill shading that mirrors height,
  per-bar borders, and labels that merely restate what the axis already shows.
- Keep a second encoding only when it adds information the first cannot (e.g. one
  precise value label on a bar a reader must know exactly), not for decoration.
- Do not reduce so far that the graphic becomes ambiguous.

### B7 — Standardize monetary units (was: standardize-monetary-units)

A currency series spanning several years mixes dollars of different purchasing
power. Convert to real terms before plotting or comparing.

    real_value(t) = nominal_value(t) × (CPI[base_year] / CPI[year_t])

- **Do not hardcode a CPI table.** Retrieve the actual index for the region and
  years you need (US: CPI-U from BLS; UK: CPI; EU: HICP) — values are revised and
  any embedded table goes stale and has gaps. Use `scripts/deflate.py`, which
  requires you to pass real CPI values and refuses to silently guess a missing
  year.
- Base year = the year you want to express everything in (commonly the most
  recent). Leave the base year's value unchanged.
- Always label the axis/output "real <base-year> dollars" or "inflation-adjusted".
- Short spans (one or two years) where inflation is negligible can note that no
  meaningful adjustment is needed rather than over-engineering.
- Hyperinflation (>100%/yr): use monthly or daily indices instead of annual.

Worked example (US, base 2023; CPI-U annual averages ≈ 2005:195.3, 2015:237.0,
2023:304.7): $40,000 (2005) → 40000 × 304.7/195.3 ≈ $62,400; $50,000 (2015) →
50000 × 304.7/237.0 ≈ $64,300; $60,000 (2023) → $60,000.
