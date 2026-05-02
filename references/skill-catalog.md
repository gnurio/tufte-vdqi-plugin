# Tufte-VDQI Skill Catalog

Complete reference of all 10 skills in the tufte-vdqi plugin.

## Router

| Skill | Trigger Phrase | Purpose |
|-------|----------------|---------|
| **orchestrate-tufte-vdqi** | "Help me with this graphic" "Apply Tufte" "I don't know where to start" | Intelligent router: detects intent, picks entry-point skill, chains workflows |

## Assessment

| Skill | Trigger Phrase | Purpose |
|-------|----------------|---------|
| **assess-graphical-excellence** | "Is this chart any good?" "Review my graphic" | Score a graphic against Tufte's nine criteria of graphical excellence |
| **calculate-lie-factor** | "Is this chart lying?" "Measure distortion" | Compute the ratio of visual effect to data effect (acceptable range: 0.95–1.05) |

## Design

| Skill | Trigger Phrase | Purpose |
|-------|----------------|---------|
| **construct-small-multiples** | "Small multiples" "Panel grid" "Compare across categories" | Compose paneled graphics sharing design, varying one indexed variable |
| **generate-range-frames** | "Replace the frame" "Range-frame" "Trim axes to data" | Replace rectangular plot frame with axis segments spanning observed min–max |
| **integrate-text-and-graphic** | "Where should labels go?" "Direct labeling" "Merge caption into chart" | Place captions and labels in the plotting field |
| **render-tufte-chart** | "Render this chart" "Generate HTML chart" "Tufte-styled output" | Generate publication-ready HTML charts using Tufte CSS styling |

## Optimization

| Skill | Trigger Phrase | Purpose |
|-------|----------------|---------|
| **erase-non-data-ink** | "Remove decoration" "Erase grid" "Too much ink" "Declutter" | Identify and remove ink that does not encode data |
| **erase-redundant-data-ink** | "This encodes the same number twice" "Simplify the encoding" | Remove ink re-encoding the same datum multiple times |
| **standardize-monetary-units** | "Inflation-adjust these values" "Nominal to real dollars" | Convert nominal-dollar time series to standardized, deflated units |

---

## Quick Start Workflows

### "Is this graphic any good?"
1. `assess-graphical-excellence` — Score against nine criteria
2. `calculate-lie-factor` — Check for distortion
3. `erase-non-data-ink` / `erase-redundant-data-ink` — Declutter

### "I need to design a chart"
1. `construct-small-multiples` — If comparing categories
2. `generate-range-frames` — Clean axes
3. `integrate-text-and-graphic` — Direct labeling
4. `render-tufte-chart` — Generate output

### "Fix this cluttered chart"
1. `assess-graphical-excellence` — Identify what's wrong
2. `erase-non-data-ink` — Remove decoration
3. `erase-redundant-data-ink` — Simplify encoding
4. `standardize-monetary-units` — If time-series money data

---

**All skills follow Tufte's principles:** minimize chartjunk, maximize data-ink ratio, show data variation not design variation, ensure proportional representation, and integrate words with numbers and pictures.
