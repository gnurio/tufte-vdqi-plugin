# Tufte Principles Reference (sourced from VDQI)

This file is the canonical Tufte knowledge for both action skills, sourced from
Edward Tufte's *The Visual Display of Quantitative Information* (1983 / 2001).
Page numbers reference the 2nd edition. Where a concept comes from one of
Tufte's later books (*Envisioning Information*, *Visual Explanations*, *Beautiful
Evidence*) it is explicitly marked — VDQI is the scope of source-grounded claims
here. In particular **"1+1=3 effect", "prison-bar shading", "sparklines", and
"slopegraph" are NOT in VDQI** and are flagged as such where they appear.

When you diagnose a problem in Part A, name the matching remedy (Part B) AND
the matching genre to switch to (Part C). When the graphic resembles a famous
failure or success, name the resemblance (Parts E/F) — that beats "looks wrong."

Both skills read this file:
- `assess-graphical-excellence` uses Parts A, D, E to score and diagnose, and
  Parts C and F to recommend.
- `render-tufte-chart` uses Parts B and C as a construction checklist and
  per-genre recipe, and Part G as numeric defaults.

---

## Part A — The nine criteria for graphical excellence

Score each 0–10 with a chart-specific observation. The weights reflect that
honesty matters more than elegance. Numeric anchors come from VDQI.

| # | Criterion | Wt | Low-score signal | VDQI anchor | Remedy |
|---|-----------|:--:|------------------|-------------|--------|
| 1 | Integrity | 3× | Truncated axis, distorted area, missing baseline, cherry-picked range | Lie factor outside 0.95–1.05 is "substantial distortion" (p.57) | B1, E |
| 2 | Proportionality | 2× | Visual ≠ data; 1-D quantity drawn as 2-D area or 3-D volume | Tufte's catalogued worst cases: 14.8 (NYT MPG, p.57), 9.5 (WaPo derricks, p.62), **59.4** (TIME 3-D barrel, "a record", p.71) | B1, D-Dimensionality |
| 3 | Data-ink ratio | 2× | Heavy grid, background, border, 3-D, shadows dominate marks | Tufte reaches 0.7 redesigning a scatterplot (p.95) and 0.9 a periodic chart (p.103); editing routinely lifts ratio from 0.1–0.2 to ~1.0 (p.136) | B5 / D-Grid |
| 4 | Redundant ink | 1× | Same datum encoded multiple ways (fill + border + label + height) | Tufte erased ~65% of original ink in one bar-chart redesign with zero data loss (p.101) | B6 |
| 5 | Data density | 1× | Tiny payload of numbers occupies a large area | "Social Indicators, 1973" managed only **0.15 numbers/in²** and was "overwrought" (p.162); excellent graphics reach **181/in²** (NYT weather, p.30), **9,000/in²** (French communes), **110,000/in²** (galaxy map, "the current record", p.166) | B3, C-Tables |
| 6 | Integration | 1× | Separate legend box; labels detached from marks | — | B4 |
| 7 | Context | 1× | No baseline, no comparison, no time frame; nominal currency | For ≤20 numbers, a **table** is usually better than a graphic (p.56) — "a table is nearly always better than a dumb pie chart" | B2, B7, C-Tables |
| 8 | Clarity | 1× | Ambiguous, congested, unlabeled | — | B4 |
| 9 | Typography | 0.5× | Decorative or illegible type; labels stranded in a key | — | B4 |

**Overall score** = weighted average. Prioritise fixes by impact: integrity and
proportionality first, then data-ink, then the rest.

**Tufte's master integrity rule** (VDQI p.71): "The number of information-
carrying (variable) dimensions depicted should not exceed the number of
dimensions in the data." Encoding a 1-D quantity with 2-D area or 3-D volume is
the single largest cause of inflated lie factors.

**Common grading mistake**: do not confuse a *design flaw* (ugly but honest)
with an *integrity violation* (the graphic misleads). Reserve the lowest
integrity scores for graphics that cause the reader to misread the numbers.

---

## Part B — The seven remedies

### B1 — Lie factor + dimensionality
Formula: `lie_factor = (percentage change shown in the graphic) / (percentage change in the data)`. Acceptable range **0.95–1.05** (VDQI p.57). Outside it, the graphic distorts; > 1 overstates, < 1 understates. Use absolute values.

Bar charts must start at a **zero baseline** — the bar length encodes magnitude from zero, so a non-zero baseline is an automatic integrity failure. Line charts may use a non-zero range (see B2) because they encode change, not magnitude.

Dimensional trap (Tufte's primary rule, p.71): a quantity encoded by **area** must scale areas proportionally (2× data ⇒ 2× area, **not** 2× side length, which gives 4× area); a quantity encoded by **volume**, 2× data ⇒ 2× volume not 8×. Worked VDQI example: NYT 1978 MPG chart drew an 18→27.5 mpg increase (+53%) as a line growing from 0.6 to 5.3 inches (+783%) → **lie factor 14.8** (p.57). TIME 1979 oil-barrel chart drew a 454% price increase as 27,000% in 3-D volume → **lie factor 59.4**, which Tufte calls "a record" (p.71).

### B2 — Range frames (Tufte's name, VDQI pp.130–132)
"The frame lines should extend only to the measured limits of the data rather than ... to some arbitrary point like the next round number ... That part of the frame exceeding the limits of the observed data is trimmed off." The trimmed frame "explicitly shows the maximum and minimum of both variables plotted." Tufte: range frames "should replace the non-data-bearing frame in many graphical applications."

- Scatter/line: axis bounds = exact data range. **Do not pad outward.**
- Mark min and max at the axis ends; interior ticks only if earned.
- Exception: bar/column charts keep a zero baseline (see B1).
- Single point (min == max): conventional axes instead.

### B3 — Small multiples (Tufte's name, VDQI p.42, pp.170, 175)
"Small multiples resemble the frames of a movie: a series of graphics, showing the same combination of variables, indexed by changes in another variable." Properties: "inevitably comparative, deftly multivariate, shrunken, high-density graphics, drawn almost entirely with data-ink." Construction:

- **Invariant design**: identical scales, colors, line weight, markers, size across every frame. Shared axes are non-negotiable.
- Shrink each frame to raise data density; verify legibility at target size.
- Order frames meaningfully (by rank, geography, time) — never alphabetically by accident.
- Label each frame directly (B4); no shared legend.
- Sizing rule of thumb: 2–4 frames → one row/column; 5–9 → 2–3 rows; 10+ → 3+ rows. Six frames → 2×3 or 3×2.

### B4 — Integrate text and graphic
Put labels on the data, not in a remote key.
- Line charts: label each line at its right-hand endpoint, in the line's color.
- Bar charts: category names beside/under the bars; value on a bar only if the exact figure matters.
- Scatter: label notable points/clusters directly; annotate outliers in place.
- Delete the legend box, its border, and its swatches once labels are direct.

### B5 — Erase non-data-ink (and beware the dreaded grid)
For each element ask: "does removing this delete any data?" If no, lighten or remove.
- Remove/flatten: heavy gridlines, background fills, borders, 3-D effects, shadows, gradients, decorative textures, moiré-prone patterns.
- VDQI p.114: "Dark grid lines are chartjunk. They carry no information, clutter up the graphic, and generate graphic activity unrelated to data information." Even Marey's classic train schedule has an "active" grid that competes with the data (p.115).
- Preserve: data marks, essential axis lines (thinned), labels.
- Exception: lookup tables that need fine rules for precise reading may keep them.

### B6 — Erase redundant data-ink
If one datum is encoded N ways, remove N−1. Keep the strongest single encoding (position on a common scale beats area beats color).

### B7 — Standardize monetary units
`real_value(t) = nominal_value(t) × (CPI[base] / CPI[year_t])`.
- **Do not hardcode CPI.** Retrieve actual indices (US: CPI-U from BLS; UK: CPI; EU: HICP). Use `scripts/deflate.py`, which errors on missing data rather than silently guessing.
- Always label the axis "real <base-year> <currency>".
- Short spans (1–2 years) with negligible inflation: note that no adjustment is needed.
- Hyperinflation (>100%/yr): use monthly or daily indices.

---

## Part C — Chart genres Tufte endorses (VDQI)

For each: Tufte's own name, the VDQI page, the construction recipe (quoted where possible), and when to use it. A render script ships for several; the rest you build directly in SVG following the recipe.

### C1 — Quartile plot (Tufte's redesigned box plot) — VDQI pp.124–125
**Tufte's term**: "quartile plot."
**Recipe**: "The straightedge need only be placed on the paper once to draw the quartile plot." Erase the box around the interquartile range; leave a single straightedge spanning the full range, with the middle half emphasized by **offsetting** it from the median line (or by line-weight change). "An erased version requires only 10 verticals to show the same information."
**Use**: informal/exploratory data analysis; side-by-side distribution comparison.
**Script**: `render-tufte-chart/scripts/quartile_plot.py`.

### C2 — Range-frame plot (redesigned scatter) — VDQI pp.130–132
**Tufte's term**: "range-frame."
**Recipe**: See B2. Trim each axis line to span only data min..max; label both endpoints.
**Use**: "should replace the non-data-bearing frame in many graphical applications."
**Script**: `render-tufte-chart/scripts/range_frame.py`.

### C3 — Dot-dash plot — VDQI p.133
**Tufte's term**: "dot-dash-plot."
**Recipe**: "Framing the bivariate scatter with the marginal distribution of each variable" using simple dash marks along the axes. "Combines the two fundamental graphical designs used in statistical analysis, the marginal frequency distribution and the bivariate distribution."
**Use**: any scatter where the marginals add insight; "make routine what good data analysts do already."
**Script**: `range_frame.py --marginal-dash`.

### C4 — Rugplot — VDQI p.135
**Tufte's term**: "rugplot."
**Recipe**: Sequence of dot-dash plots sharing fringe distributions: "The fringe of dashes in the dot-dash-plot can connect a series of bivariate scatters in a rugplot." Traces "the quantitative history of a single observation ... through a series of one- and two-dimensional contexts."
**Use**: tracing complex relationships across multiple variables in sequence.

### C5 — Small multiples — VDQI p.42, pp.170, 175
See B3 for the construction rules. Tufte's exemplar in VDQI: McRae et al.'s LA air pollutant maps.
**Use**: "inevitably comparative, deftly multivariate."
**Script**: `render-tufte-chart/scripts/small_multiples.py`.

### C6 — Supertable / text-table / table-graphic — VDQI pp.145, 159, 178–179
**Tufte's terms**: "text-table," "supertable," "table-graphic."
**Recipe**: "Arrange the type to facilitate comparisons" (text-table). Supertable: "Horizontal rules divide the data into topical paragraphs; the rows are ordered so as to tell an ordered story." Table-graphic: numbers placed to "yield an internal grid, a rare example of data as grid," or sloped/lined to be read across and down.
**Use**: "Tables are clearly the best way to show exact numerical values ... Tables are preferable to graphics for many small data sets. A table is nearly always better than a dumb pie chart" (p.56). **The 20-number rule**: at ≤20 numbers, default to a table. "One supertable is far better than a hundred little bar charts."

### C7 — Stem-and-leaf plot — VDQI p.140 (Tukey, championed by Tufte)
**Recipe**: "Constructs the distribution of a variable with numbers themselves." Tukey, quoted: "If we are going to make a mark, it may as well be a meaningful one. The simplest—and most useful—meaningful mark is a digit."
**Use**: distributions where exact values matter; the data IS the data measure.

### C8 — Relational graphic (scatterplot) — VDQI pp.46–47
**Tufte's term**: "relational graphic." His verdict: "the greatest of all graphical designs."
**Recipe**: Abandon physical coordinates; plot any variable against any other.
**Use**: "Links at least two variables, encouraging and even imploring the viewer to assess the possible causal relationship ... confronts causal theories that X causes Y with empirical evidence." (Pair with C2 range-frame for the axes.)

### C9 — White-grid bar chart — VDQI pp.126–129
**Recipe**: Erase the surrounding box; erase the vertical axis line; erase the ticks; finally erase **part of the data measures themselves** so the gaps form a "white grid." "The white grid eliminates the tick marks, since the numerical labels on the vertical are tied directly to the white lines." Keep a thin baseline.
**Use**: cleaner alternative to gridded bar/histogram for printed work.

### C10 — Time-series — VDQI pp.28–30
**Recipe**: One dimension marches at a regular cadence (seconds → millennia).
**Tufte's use rule**: "Time-series displays are at their best for big data sets with real variability." **Do not** use a time-series for simple linear changes: "Why waste the power of data graphics on simple linear changes, which can usually be better summarized in one or two numbers? ... graphics should be reserved for the richer, more complex, more difficult statistical material."
**Script**: `render-tufte-chart/scripts/render_line_svg.py`.

**Note on absences**: **sparklines** and **slopegraphs** are NOT in VDQI — Tufte introduced sparklines in *Beautiful Evidence*. Add those sources to the notebook before claiming VDQI coverage of them.

---

## Part D — Chartjunk taxonomy (VDQI)

VDQI catalogues **three named species** of chartjunk plus a generic "decoration" critique: "Like weeds, many varieties of chartjunk flourish. Here three widespread types ... are catalogued — unintentional optical art, the dreaded grid, and the self-promoting graphical duck" (p.107). Detect each by its specific signature; cite Tufte's named offenders when matching.

> **Not in VDQI**: "1+1=3 effect," "prison-bar shading," "dischronologic series."
> Those are from *Envisioning Information* and later books. If you cite them,
> mark them as such, not as VDQI.

### D-Moiré — Unintentional optical art (VDQI p.108)
"Contemporary optical art relies on moiré effects, in which the design interacts with the physiological tremor of the eye to produce the distracting appearance of vibration and movement." Tufte calls it "probably the most common form of graphical clutter ... inevitably bad art and bad data graphics."
- **Detect**: cross-hatched fills, dense parallel patterns, fine stippling, dark gradients on bars, strobing intersections.
- **Tufte's named offenders**: Instituto de Expansão Commercial Brazil "TECIDOS DE ALGODÃO" (1929, p.108); Kouchoukos et al. "Severity of Aortic Regurgitation" 3-D pyramids (p.109); Kuznicki & McCutcheon [14C]-glucose bar chart (p.109); JASA style-sheet "vibrating chartjunk" example (p.110).

### D-Grid — The dreaded grid (VDQI pp.112–115)
"The grid should usually be muted or completely suppressed so that its presence is only implicit — lest it compete with the data ... Dark grid lines are chartjunk. They carry no information, clutter up the graphic, and generate graphic activity unrelated to data information."
- **Detect**: grid darker than data marks; intersections that strobe; backgrounds that draw the eye away from the line/dot.
- **Tufte's named offenders**: INSEE "Population of France, by Age and Sex" age-sex pyramid where the grid camouflages the profile (p.113); Tukey & Tukey multiwindow particle-physics plot where intersections show optical white dots (p.114); even Marey's beloved Paris-Lyon train schedule has an "active" grid (p.115).
- **Remedy**: see B5; for a positive example use Playfair's "data-based grid" (p.34).

### D-Duck — Self-promoting graphic (VDQI p.116)
"When a graphic is taken over by decorative forms or computer debris, when the data measures and structures become Design Elements, when the overall design purveys Graphical Style rather than quantitative information, then that graphic may be called a duck in honor of the duck-form store, 'Big Duck'." Named after the literal Big Duck building in Flanders, NY (the photograph is reproduced on p.117).
- **Detect**: chart elements doing decoration; visual style outpacing visual content; dimensionality > data dimensionality.
- **Tufte's named offenders**: *American Education* magazine 3-D "AGE STRUCTURE OF COLLEGE ENROLLMENT" with "only five pieces of data" (p.118); *The California Water Atlas* "superbly produced duck" (p.119); Miller et al. "PERCENT CRITICAL ARTICLES" — the "We-Used-A-Computer-To-Build-A-Duck Syndrome" (p.120).

### D-Decoration — Generic interior decoration (VDQI p.108)
"The interior decoration of graphics generates a lot of ink that does not tell the viewer anything new. The purpose of decoration varies — to make the graphic appear more scientific and precise, to enliven the display ... it is all non-data-ink or redundant data-ink, and it is often chartjunk."
- **Tufte's named offender**: NYT "REQUIRED FUEL ECONOMY STANDARDS" — an ornate border of leaves, statues, and crests, "many decorations but no lies" (p.59).

---

## Part E — Named anti-patterns from VDQI (failure comparison library)

When assessing a graphic, compare it to these named cases. Saying "this is essentially the 1979 TIME barrel — lie factor likely 50+" is more diagnostic than "looks distorted." All citations are VDQI page numbers.

| Source | Date | Failure | Metric (Tufte) | p. |
|---|---|---|---|---|
| NYT, "Fuel Economy Standards" | 1978-08-09 | Shrinking perspective; 1-D quantity drawn with 2-D area; date sizes constant while road shrinks | **Lie factor 14.8** (53% data → 783% visual) | 57–58 |
| TIME, "IN THE BARREL" | 1979-04-09 | Oil prices on 3-D barrels | **Lie factor 9.4 (area) / 59.4 (volume), "a record"** | 62, 71 |
| Washington Post, "OPEC Benchmark Prices" | 1979-03-28 | Varying-size oil derricks | **Lie factor 9.5** (708% data → 6,700% visual) | 62 |
| LA Times, "The Shrinking Family Doctor" | 1979-08-05 | 2-D area for 1-D data + perspective + wrong horizontal spacing | **Lie factor 2.8** | 69 |
| NYT, "Commission Payments to Travel Agents" | 1978-08-08 | Plotted half-years next to full years ("the lie repeated four times over") | — | 54 |
| Day Mines, Inc., Annual Report | 1974 | Hidden baseline at ≈ −$4.2 M disguises a 1970 loss | — | 54 |
| NSF, *Science Indicators* Nobel Prizes chart | 1976 | Irregular x-axis: seven 10-year intervals, then one 4-year — fakes a decline | — | 60 |
| NYT, OPEC Oil Prices | 1978-12-19 | Five different vertical scales; same value appears 15.1× different | 15.1× variation | 61 |
| NYT, "NY State Total Budget Expenditures" | 1976-02-01 | Fake 3-D + raw dollars to imply explosive growth | — | 66–68 |
| Fiorina, *Congress: Keystone of the Washington Establishment* | 1977 | No deflation, tall-thin shape, political distortion | Aspect 2.7:1 (taller than wide) | 66 |
| Satet, *Les Graphiques* | 1932 | Men of varying sizes representing export growth (areas for 1-D data) | — | 69 |
| Pittsburgh Civic Commission report | 1911 | Buildings sized by height, ignoring area | — | 55 |
| Dewey & Dakin, *Cycles: The Science of Prediction* | 1947 | "Solar Radiation and Stock Prices" — implies causation | "A silly theory means a silly graphic" | 15 |

---

## Part F — Named exemplars from VDQI (success comparison library)

When recommending a redesign, name an exemplar to emulate. "This data calls for the Marey treatment" beats "use direct labels."

| Graphic | Creator / Date | Tufte's praise | Move to copy | p. |
|---|---|---|---|---|
| Napoleon-in-Russia march | Charles Joseph Minard, 1869 | "It may well be the best statistical graphic ever drawn" | Plot 6 variables (army size, x, y, direction, temp, date) so viewers are "hardly aware they are looking into a world of four or five dimensions" | — |
| Cholera map | Dr. John Snow, 1854 | "Graphical analysis testifies about the data far more efficiently than calculation" | Dot the events on the geography; let pattern reveal cause | — |
| Train schedule Paris-Lyon | E.J. Marey, 1885 | "Giving a context and order to complexity ... aesthetic balance" | Slope = speed; intersections = time + place; mute grid to gray | — |
| *Commercial and Political Atlas* | William Playfair, 1786 | Playfair "invented or improved upon nearly all the fundamental graphical designs" | Eliminate non-data detail; "data-based grids" that serve rather than fight the data | — |
| NYC Weather History | NYT, 1981-01-11 | "Successfully organizes a large collection of numbers, makes comparisons ... tells a story" | 181 numbers/in² density; reserve graphics for rich material | 30, 164 |
| Map of 1.3 Million Galaxies | Seldner et al., 1977 | "No other method for the display of statistical information is so powerful" | 110,000 numbers/in² (record); varying greys not colors | 166 |
| Atlas of Cancer Mortality | Hoover et al., 1975 | "Attention has been directed toward exploring the substantive content of the data rather than ... methodology" | Massive data in small space; small multiples on geography | — |
| LA Air Pollutants small multiples | McRae et al., 1979 | "Inevitably comparative, deftly multivariate, efficient in interpretation" | Repeat one design; shift only the data | — |
| Thermal Conductivity of Cu/W | Ho/Powell/Liley, 1974 | "Effectively organizes a vast amount of data ... enforcing comparisons" | Double-functioning marks: coordinate labels ARE the data measures | — |
| "Living" Histogram | Joiner, 1975 | "The data form the data measure" | Make the data its own mark (photos of students arrayed by height) | — |
| Japanese Beetle life cycle | L. H. Newman, 1965 | "Ingeniously mixes space and time on the horizontal axis" | Space + time on one axis | — |
| Hannibal Campaign Map | Minard, 1869 | "Refined use of color ... calm, transparent colors" | Transparent flow colors over a visible base grid | — |
| Lambert's evaporation rate | J.H. Lambert, 1765 | "Most remarkable early ... non-analogical relational graphic" | Plot abstract quantity vs abstract quantity | — |
| Consumer Reports reliability | 1982 | "Particularly ingenious mix of table and graphic" | Hybrid table-graphic for multi-variable comparison | — |

---

## Part G — Quantitative rules of thumb (VDQI, compiled)

Quick-reference card pulled from across the book.

- **Lie factor**: `(visual change %) / (data change %)`. Acceptable **0.95–1.05** (p.57). Tufte's catalogued worst cases: **14.8** (NYT MPG), **9.4–9.5** (oil derricks / barrels in 2-D), **59.4** (oil barrel in 3-D, "a record").
- **Data-ink ratio**: `data-ink / total ink`, equivalently `1.0 − proportion erasable without data loss` (p.93). Editing routinely lifts ratio from **0.1–0.2 to ~1.0** (p.136).
- **Data density** (`entries / area`): 0.15 numbers/in² is "overwrought" (p.162); aim for ≥ a few/in² for ordinary work; Tufte's record exemplars reach 110,000–250,000/in² (p.166–168).
- **Dimensionality rule** (p.71): "The number of information-carrying dimensions depicted should not exceed the number of dimensions in the data." 1-D quantity ⇒ 1-D encoding (length/position); never area or volume.
- **Tables vs graphics**: for **≤ 20 numbers**, default to a table (p.56). "A table is nearly always better than a dumb pie chart."
- **Aspect ratio**: graphics should generally be wider than tall — "move toward horizontal graphics about 50 percent wider than tall" (p.190). Golden Rectangle ≈ **1.618** (p.189).
- **Redundant-ink budget**: in one worked redesign Tufte erased **~65%** of original ink with zero data loss (p.101). Most production charts have plenty to give back.
- **Monetary time series**: deflate to real <base-year> units before plotting (B7). VDQI calls out Fiorina (p.66) for failing to do this.
