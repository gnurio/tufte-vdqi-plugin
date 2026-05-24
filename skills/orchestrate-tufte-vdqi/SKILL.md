---
name: orchestrate-tufte-vdqi
description: Router for the Tufte data-visualization toolkit. Use whenever someone has a chart or data-visualization request and you are not sure which Tufte skill to use — it decides between assessing an existing graphic, producing a new one, or fixing a cluttered/misleading one, and chains them when needed.
---

# Orchestrate Tufte VDQI

You are the router. Read the request, decide the intent, and invoke the right
skill. You are doing this by understanding, not by matching keywords — the
previous version was a brittle keyword function and it is gone.

## The toolkit (three skills + one reference)

- `assess-graphical-excellence` — evaluate an existing graphic against Tufte's
  nine criteria, quantify distortion (lie factor is built in here), and return
  prioritised fixes. The default when intent is unclear.
- `render-tufte-chart` — produce an actual chart file (SVG/HTML) that obeys the
  principles. The only skill that outputs a chart.
- `assess-graphical-excellence/references/tufte-principles.md` — the canonical
  encoding of every Tufte technique. The seven former micro-skills (lie factor,
  range frames, small multiples, integrate text, erase non-data-ink, erase
  redundant ink, standardize monetary units) were folded into this one file as
  remedies B1–B7; both action skills consult it. There is nothing else to route
  to for those techniques — apply them via assess (to recommend) or render (to build).

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

Earlier this toolkit had nine skills. Benchmarking showed most encoded a single
Tufte idea the model already applies, so separate routing targets only added
latency and risk. Assessment and rendering are the two actions that genuinely
benefit from a skill; everything else is shared knowledge in the principles
reference. Keep routing to these two actions and let the reference carry the rest.
