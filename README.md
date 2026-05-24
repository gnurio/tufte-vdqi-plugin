# Chartwright

> Give your AI agents the skill of visualizing data the way Edward Tufte intended.

<p align="center">
  <img src="https://www.edwardtufte.com/wp-content/uploads/2023/09/edward-tufte-visual-display-of-quantitative-information.jpg" alt="The Visual Display of Quantitative Information — Edward Tufte" width="260" />
</p>

*Based on Edward Tufte's* The Visual Display of Quantitative Information

---

Every chart your agent produces gets scored against Tufte's principles — lie factor measured, chartjunk stripped, redundant ink removed, labels moved inline, axes replaced with range-frames, monetary values inflation-adjusted, and the result rendered as a clean SVG. Not as a suggestion. As a workflow.

---

## Before / After

<table>
<tr>
<th align="center">Before</th>
<th align="center">After</th>
</tr>
<tr>
<td><img src="examples/before-1.webp" alt="Before: colorful bar chart with bird illustrations, inconsistent colors, decorative clutter" width="380" /></td>
<td><img src="examples/after-1.svg" alt="After: Tufte-styled Cleveland dot plot on a log scale, minimal ink, data speaks for itself" width="380" /></td>
</tr>
<tr>
<td><img src="examples/before-2.webp" alt="Before: colorful bar chart of SWE-bench scores with arbitrary color coding and no confidence intervals shown" width="380" /></td>
<td><img src="examples/after-2.svg" alt="After: Cleveland dot plot with 95% confidence intervals — the overlapping ranges tell the real story" width="380" /></td>
</tr>
</table>

Same data, both times. No decorative bars, no arbitrary colors. Cleveland dot plots that let the actual signal — and the uncertainty — speak for itself.

---

## Install

**Individual (Claude Code)**

1. Open Claude Desktop → switch to the Cowork tab
2. Go to **Plugins**
3. Add this repo as a plugin source
4. Upload the ZIP file

**Organization (admin)**

1. Go to Organization Settings → Plugins
2. Select **GitHub** as the source
3. Paste this repo URL
4. Set market preference: Required / Available / Default

*Requires a paid Claude plan (Pro, Max, Team, or Enterprise) with Cowork enabled.*

---

## Skills

Three skills, one shared reference. The router picks between the two action skills; the principles file is the canonical encoding of every Tufte technique (lie factor, range frames, small multiples, integrated labels, non-data-ink, redundant ink, monetary deflation) and is read by both actions.

| Skill | What it does |
|-------|-------------|
| `orchestrate-tufte-vdqi` | Routes a request to assess, render, or both. Use it when you're unsure where to start. |
| `assess-graphical-excellence` | Scores a graphic against Tufte's nine criteria, computes the lie factor, and returns prioritised fixes tagged with the remedy (B1–B7) needed to apply them. |
| `render-tufte-chart` | Produces an actual SVG using range-frame axes, direct end labels, no gridlines, and honest proportions. Ships a working `render_line_svg.py` for line charts and a build checklist for bars / scatters / small multiples. |

Ships with helper scripts and the [tufte-css](https://github.com/edwardtufte/tufte-css) typography bundle (MIT, vendored under `skills/render-tufte-chart/assets/tufte-css/`):

- `assess-graphical-excellence/scripts/deflate.py` — inflation adjustment for monetary time series. Requires real CPI values; errors on a missing year rather than guessing.
- `render-tufte-chart/scripts/render_line_svg.py` — Tufte-style SVG line chart with range-frame axes and direct end labels.
- `render-tufte-chart/scripts/wrap_html.py` — wraps any SVG in a Tufte-styled HTML page using the vendored ET Book typography; copies the stylesheet and fonts next to the output so it opens in any browser with no network.

---

## Usage

Start with the orchestrator — it detects your intent and routes you:

```
/orchestrate-tufte-vdqi
```

Or invoke an action skill directly:

```
/assess-graphical-excellence
/render-tufte-chart
```

---

## Common workflows

### "Is this chart any good?"
```
assess-graphical-excellence   → nine-criteria scores, lie factor, prioritised fixes (B1–B7)
```

### "Fix this cluttered or misleading chart"
```
assess-graphical-excellence   → diagnose and emit remedies
render-tufte-chart            → rebuild honoring those remedies
```

### "Design a chart from scratch"
```
render-tufte-chart            → produces an SVG that bakes in B1–B7 by construction
assess-graphical-excellence   → (optional) confirm the result scores well
```

### "My data is currency across multiple years"
```
deflate.py (B7)               → convert to real <base-year> dollars first
render-tufte-chart            → plot the real-terms series with a labelled axis
```

### "Give me a shareable Tufte-styled web page, not just an SVG"
```
render-tufte-chart            → produces chart.svg
wrap_html.py                  → wraps it in a tufte-css page (ET Book typography)
                                → outputs chart.html + ./tufte-assets/ siblings
```

---

## License

Concepts in this project were inspired by *The Visual Display of Quantitative Information* by Edward Tufte. No text has been reproduced.
