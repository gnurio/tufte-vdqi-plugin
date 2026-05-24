---
name: assess-graphical-excellence
description: Evaluate a data graphic against Tufte's nine criteria, quantify any visual distortion (lie factor), and return prioritised, concrete fixes. Use whenever someone asks whether a chart is good, what is wrong with a chart, how to clean up or declutter a chart, whether a graphic is misleading, or for any Tufte-style critique of an existing visualization.
---

# Assess Graphical Excellence

This is the assessment hub of the Tufte toolkit. It scores an existing graphic,
explains why, and — most importantly — hands back the exact remedy for every
problem so the reader (or a follow-up render step) knows precisely what to change.

It also absorbs lie-factor analysis, which used to be a separate skill: distortion
is just the integrity criterion, so it is computed here directly.

## What you need from the user

A description (or image, or file) of the graphic, and ideally its purpose and
audience. If something essential is missing, infer reasonably and state the
assumption rather than stalling.

## How to assess

Read `references/tufte-principles.md`. Part A lists the nine criteria, their
weights, and the remedy each maps to; Part B holds the remedy procedures.

1. Score each of the nine criteria 0–10. Justify every score with a specific
   observation about *this* graphic — never a generic statement. Unsupported
   scores are the main failure mode of a weak assessment.
2. If any magnitude looks exaggerated (truncated axis, 3-D/area encoding, a
   dramatic-looking small change), compute the **lie factor** per remedy B1:
   `lie_factor = visual_change_% / data_change_%`, acceptable only in 0.95–1.05.
   Report the number and what it means.
3. Compute the weighted overall score (integrity 3×, proportionality 2×,
   data-ink 2×, typography 0.5×, the rest 1×).
4. Translate each weak score into a recommendation, and tag it with the remedy
   number from Part B (e.g. "B1 — zero the bar baseline", "B4 — move the legend
   onto the lines"). The tag is how the model and the user know *how* to fix it,
   and it is what a downstream `render-tufte-chart` step follows.

If the graphic plots a multi-year currency series, check remedy B7: nominal
dollars across years are an integrity/context problem, and you can use
`scripts/deflate.py` (in this skill folder) to produce the real-terms values.

## Output format

```
## Assessment: <graphic>
Context: <purpose / audience, or stated assumption>

### Scores
<one line per criterion: name — score/10 — specific justification>

### Distortion check
Lie factor: <value or "n/a"> — <interpretation>

### Overall: <weighted score>/10 — <one-sentence verdict>

### Fixes (highest impact first)
1. <remedy tag> — <concrete change>
2. ...
```

## What good looks like

All nine criteria scored with chart-specific evidence; distortion quantified when
present; recommendations ordered by impact and each tied to a named remedy the
reader can act on. Avoid vague praise and avoid listing problems without their fix.

## Related skills
- `render-tufte-chart` — rebuild the graphic so it satisfies these criteria.
- `orchestrate-tufte-vdqi` — routes here for evaluation, then to render for the fix.
