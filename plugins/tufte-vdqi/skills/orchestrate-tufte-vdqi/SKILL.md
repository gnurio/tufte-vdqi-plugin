---
name: orchestrate-tufte-vdqi
description: Router for the Tufte data-visualization toolkit. Use whenever someone has a chart or data-visualization request and you are not sure which Tufte skill to use — it decides between assessing an existing graphic, producing a new one, or fixing a cluttered/misleading one, and chains them when needed.
---

# Orchestrate Tufte VDQI

You are the router. Read the request, decide the intent, and invoke the right
skill. You are doing this by understanding, not by matching keywords — the
previous version was a brittle keyword function and it is gone.

## The toolkit (three skills + one VDQI-sourced reference)

- `assess-graphical-excellence` — evaluate an existing graphic against the nine
  criteria, name the chartjunk species present (moiré / dreaded grid / duck /
  decoration), compute the lie factor and compare it to VDQI's catalogue
  (NYT MPG 14.8, TIME barrel 59.4, etc.), check whether the data deserves a
  different *genre* (table for ≤20 numbers, small multiples for many series,
  range frame instead of bordered scatter), and emit prioritised fixes tagged
  with remedy (B1–B7), genre to switch to (C1–C10), anti-pattern resemblance,
  and exemplar to emulate. The default when intent is unclear.
- `render-tufte-chart` — produce an actual chart file. Ships per-genre scripts:
  `render_line_svg.py` (time-series C10), `small_multiples.py` (C5),
  `quartile_plot.py` (C1), `range_frame.py` (C2, optional C3 dot-dash
  marginals), plus `wrap_html.py` for a tufte-css HTML page. The only skill
  that outputs a chart.
- `references/tufte-principles.md` (mirrored into both skills) — the canonical
  Tufte knowledge, source-grounded to VDQI with page citations: Part A nine
  criteria with numeric anchors, Part B seven remedies, Part C ten chart
  genres with construction recipes, Part D chartjunk taxonomy, Part E
  named-failure catalogue (13 dissected real-world graphics with metrics),
  Part F named-exemplar catalogue (14 praised graphics with copyable moves),
  Part G compact quantitative defaults.

## Routing

- **Evaluate / critique** ("is this chart any good?", "what's wrong with this?",
  "is this misleading?") → `assess-graphical-excellence`.
- **Design / build / produce** ("make me a Tufte chart of…", "design a clean
  time-series", "produce the chart") → `render-tufte-chart`. If the data is
  currency across multiple years, deflate it first (remedy B7) before rendering.
- **Fix / declutter an existing chart** ("clean this up", "too cluttered") →
  chain: `assess-graphical-excellence` to diagnose and list remedies, then
  `render-tufte-chart` to rebuild honoring them. The assessment's remedy tags
  (B1–B7) are the instructions render follows.
- **Unsure** → start with `assess-graphical-excellence`.

## Why this shape

Earlier this toolkit had ten skills. Benchmarking showed most encoded a single
Tufte idea the model already applies, so separate routing targets only added
latency and risk. Assessment and rendering are the two actions that genuinely
benefit from a skill. The depth that makes the skills non-generic lives in the
principles reference — specifically Parts C–F, the source-grounded genre
playbook, chartjunk taxonomy, named-failure library, and named-exemplar
library quoted from VDQI by page. Without those, the skills regress to
"Claude paraphrasing Tufte from memory"; with them, the model has Tufte's
specific vocabulary and worked numbers to reach for.
