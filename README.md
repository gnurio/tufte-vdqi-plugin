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

### Claude Code

**Individual**

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

### Codex

This repository also ships Codex plugin metadata:

- `.agents/plugins/marketplace.json` as the repo-local marketplace
- `plugins/tufte-vdqi/.codex-plugin/plugin.json` as the Codex plugin manifest
- `plugins/tufte-vdqi/skills/` as the Codex plugin skill payload

Install from a local checkout:

```
codex plugin marketplace add /path/to/tufte-vdqi-plugin
codex plugin add tufte-vdqi@tufte-vdqi-local
```

For a separate Codex profile, set `CODEX_HOME` for both commands:

```
CODEX_HOME=/path/to/codex-home codex plugin marketplace add /path/to/tufte-vdqi-plugin
CODEX_HOME=/path/to/codex-home codex plugin add tufte-vdqi@tufte-vdqi-local
```

Start a new Codex thread after installation so the plugin skills are loaded.

---

## Skills

Three skills, one VDQI-sourced reference. The router picks between the two action skills; the principles file (mirrored into both skills) is the source-grounded encoding of Tufte's specific techniques — nine criteria with numeric anchors, ten chart genres with construction recipes, a chartjunk taxonomy, and 13+14 named anti-pattern/exemplar catalogues — all cited to VDQI by page.

| Skill | What it does |
|-------|-------------|
| `orchestrate-tufte-vdqi` | Routes a request to assess, render, or both. Use it when you're unsure where to start. |
| `assess-graphical-excellence` | Scores a graphic against Tufte's nine criteria with VDQI numeric anchors, names the chartjunk species present (moiré, dreaded grid, duck, decoration), computes lie factor and compares to VDQI's catalogue (14.8 NYT MPG, 59.4 TIME barrel "a record", etc.), checks whether the data wants a different genre (table for ≤20 numbers, small multiples for many series, range frame instead of bordered scatter), and emits fixes tagged with remedy / genre / anti-pattern resemblance / exemplar to emulate. |
| `render-tufte-chart` | Produces an actual SVG using Tufte's specific genres. Ships per-genre scripts for time-series, small multiples, the quartile plot (Tufte's stripped-down box plot), and range-frame scatter (with optional dot-dash marginals), plus an HTML wrapper using the bundled tufte-css. |

Ships with helper scripts and the [tufte-css](https://github.com/edwardtufte/tufte-css) typography bundle (MIT, vendored under `skills/render-tufte-chart/assets/tufte-css/`):

- `assess-graphical-excellence/scripts/deflate.py` — inflation adjustment for monetary time series. Requires real CPI values; errors on a missing year rather than guessing.
- `render-tufte-chart/scripts/render_line_svg.py` — Tufte-style time-series line chart (VDQI C10).
- `render-tufte-chart/scripts/small_multiples.py` — grid of identical mini-charts sharing one scale (VDQI C5).
- `render-tufte-chart/scripts/quartile_plot.py` — Tufte's stripped-down box plot (VDQI C1, pp.124–125).
- `render-tufte-chart/scripts/range_frame.py` — scatterplot with axis lines spanning only the data range (VDQI C2, pp.130–132); pass `--marginal-dash` for the dot-dash plot (C3, p.133).
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

### "I have many series to compare"
```
small_multiples.py            → grid of identical mini-charts, shared scales
                                ("inevitably comparative, deftly multivariate" — VDQI p.170)
```

### "I want to compare distributions across groups"
```
quartile_plot.py              → Tufte's stripped-down box plot (VDQI pp.124–125)
                                erased box; offset IQR; median tick
```

### "I want a scatter that doesn't lie about the data range"
```
range_frame.py                → axis lines span only data min..max (VDQI pp.130–132)
range_frame.py --marginal-dash → adds dot-dash marginals (VDQI p.133)
```

---

## License

Concepts in this project were inspired by *The Visual Display of Quantitative Information* by Edward Tufte. No text has been reproduced.
