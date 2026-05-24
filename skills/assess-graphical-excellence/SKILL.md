---
name: assess-graphical-excellence
description: Evaluate a data graphic against Edward Tufte's nine criteria, name the chartjunk species present, compute lie factor, compare against VDQI's named-failure catalogue, and return prioritised fixes tagged with the specific Tufte remedy (B1–B7), genre to switch to (C1–C10), and exemplar to emulate. Use whenever someone asks whether a chart is good, what is wrong with a chart, how to clean up or declutter a chart, whether a graphic is misleading, or for any Tufte-style critique of an existing visualization.
---

# Assess Graphical Excellence

This is the assessment hub of the Tufte toolkit. Its job is to score an existing
graphic, **name what's wrong using Tufte's vocabulary** (the duck, the dreaded
grid, moiré vibration, dimensionality violation, etc.), and hand back the exact
remedy plus the genre to switch to and an exemplar to emulate.

The output is concrete and source-grounded because the model reasons over a
single principles file (`references/tufte-principles.md`) that quotes VDQI by
page. Generic "improve data-ink ratio" advice is the failure mode this skill is
designed to avoid.

## What you need from the user

A description (or image, or file) of the graphic, and ideally its purpose and
audience. If something essential is missing, infer reasonably and state the
assumption rather than stalling.

## How to assess (six-step workflow)

Read `references/tufte-principles.md` first. The workflow uses every part of it.

1. **Score the nine criteria** (Part A). 0–10 each, with a chart-specific
   observation. Use VDQI's numeric anchors: e.g. data-ink ratio "0.1–0.2 is
   typical, edit toward 1.0" (p.136); data density 0.15 numbers/in² is
   "overwrought" (p.162). Unsupported scores are the main failure mode.

2. **Compute the lie factor when proportionality looks suspicious** (Part B,
   B1). Formula: `(visual change %) / (data change %)`. Acceptable 0.95–1.05.
   Report the number and **compare to VDQI's catalogue** (Part E) — anchor the
   verdict in a named case: "this is essentially the 1979 TIME barrel
   (lie factor 59.4)" or "in the league of the LA Times shrinking-doctor
   (lie factor 2.8)" rather than a free-floating number.

3. **Identify chartjunk species present** (Part D). Walk the four named
   offenses and name each one the chart exhibits, citing Tufte's named offender
   when the resemblance is close:
   - **Moiré vibration** (cross-hatching, dense stippling, gradients)
   - **Dreaded grid** (grid darker than the data marks)
   - **Duck** (decoration drives the chart; visual style > data; dimensionality
     exceeds data dimensionality)
   - **Decoration** (ornament that carries no information)

4. **Check chart-genre fit** (Part C, Part G). Could this graphic be:
   - A **table** instead? (≤20 numbers ⇒ default to table; "a table is nearly
     always better than a dumb pie chart" — VDQI p.56)
   - **Small multiples** instead? (many series; "inevitably comparative")
   - A **range frame** instead of a bordered scatter? (scatter/line on padded
     axes)
   - A **quartile plot** instead of a boxed box plot?
   - A **white-grid bar chart** instead of gridded bars?
   Name the genre to switch to, and cite the VDQI page.

5. **Compute the weighted overall score**. Weights: integrity 3×,
   proportionality 2×, data-ink 2×, typography 0.5×, the rest 1×.

6. **Translate scores into ranked fixes**. Each fix gets up to four tags:
   - **Remedy**: B1–B7 (the technique).
   - **Genre**: C1–C10 (the form to switch to). Optional.
   - **Anti-pattern resemblance**: name a Part-E case the graphic looks like.
     Optional.
   - **Exemplar to emulate**: name a Part-F graphic the redesign should
     resemble. Optional.

If the graphic plots a multi-year currency series, check B7. Use
`scripts/deflate.py` (requires real CPI values; refuses to guess).

## Output format

```
## Assessment: <graphic>
Context: <purpose / audience, or stated assumption>

### Scores
<one line per criterion: name — score/10 — chart-specific observation>

### Chartjunk species present
<list any of: moiré, dreaded grid, duck, decoration — each with the detected signature, and Tufte's named offender it most resembles>

### Distortion check
Lie factor: <value or "n/a"> — <interpretation>
Resembles: <named VDQI case from Part E, or "no close analogue">

### Genre fit
Current form: <bar/line/pie/scatter/infographic>
Better form per VDQI: <Part C genre + page, or "current form is appropriate">

### Overall: <weighted score>/10 — <one-sentence verdict>

### Fixes (highest impact first)
1. [B?, C?, resembles E?, emulate F?] — <concrete change>
2. ...
```

## What good looks like

All nine criteria scored with chart-specific evidence; chartjunk species named
where present; distortion quantified and anchored in a VDQI case; the genre
question explicitly considered; recommendations ordered by impact, each tied to
a remedy AND (when applicable) a genre switch / a famous case to avoid / a
famous case to emulate. The reader should leave with a concrete picture of what
to build next, not a list of vague improvements.

## Related skills
- `render-tufte-chart` — rebuild the graphic so it satisfies these criteria,
  using the per-genre scripts named in your fixes.
- `orchestrate-tufte-vdqi` — routes here for evaluation, then to render for the
  fix.
