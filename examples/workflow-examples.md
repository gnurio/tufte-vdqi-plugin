# Tufte VDQI Skills - Workflow Examples

Real-world scenarios showing skills working together.

---

## Example 1: Fixing a Misleading Sales Chart

### Scenario
Marketing team shows a bar chart of quarterly revenue that looks like growth is exploding.

### Input
- Chart: 3D bar chart, dark background, grid lines
- Data: Q1=$100K, Q2=$110K, Q3=$105K, Q4=$115K
- Visual: Q4 bar is 3x taller than Q1 bar (300% visual vs 15% actual)

### Workflow

**Step 1: Assess the graphic**
```
/assess-graphical-excellence
  "3D bar chart with dark background, heavy grid, Q1-Q4 revenue data"
```
Result: integrity=2/10, data_ink_ratio=3/10, recommendations=["Fix lie factor", "Remove 3D", "Remove grid"]

**Step 2: Calculate the distortion**
```
/calculate-lie-factor
  visual_change=300, data_change=15
```
Result: lie_factor=20.0, is_distorted=true (severe)

**Step 3: Fix the distortion**
```
/erase-non-data-ink
  "3D bar chart with dark background, heavy grid, decorative borders"
  data_elements=["bars", "axis labels"]
```
Result: removed=["3D effects", "dark background", "heavy grid", "borders"]

**Step 4: Verify improvement**
```
/assess-graphical-excellence
  "Clean bar chart with flat bars on white background, no grid"
```
Result: integrity=9/10, data_ink_ratio=9/10

### Outcome
- Fixed 20x lie factor → 1.0 (accurate)
- Removed all chartjunk
- Chart now honestly shows modest 15% growth

---

## Example 2: Designing Multi-Year Financial Report

### Scenario
CFO needs to show 10 years of revenue vs costs for board presentation.

### Input
- Data: 2014-2023 annual revenue and costs
- Revenue: [$10M, $11M, $12M... $18M]
- Costs: [$8M, $8.5M, $9M... $12M]
- Region: US

### Workflow

**Step 1: Standardize monetary units**
```
/standardize-monetary-units
  nominal_values=[10000000, 11000000, ..., 18000000]
  years=[2014, 2015, ..., 2023]
  currency_region="US"
```
Result: real_values adjusted to 2023 dollars

**Step 2: Generate range-frames**
```
/generate-range-frames
  x_min=2014, x_max=2023
  y_min=8000000, y_max=18000000
  axis_description="Time series line chart"
```
Result: axes trimmed to data bounds

**Step 3: Integrate text**
```
/integrate-text-and-graphic
  chart_description="Line chart with revenue and cost lines"
  data_labels=["Revenue", "Costs"]
  explanatory_text="10-year financial trends (inflation-adjusted)"
```
Result: direct labels at line endpoints

### Outcome
- Accurate year-over-year comparison (inflation-adjusted)
- Maximized data-ink ratio
- Clear labeling without legend

---

## Example 3: Comparing Regional Performance

### Scenario
Product team needs to compare user engagement across 6 geographic regions.

### Input
- Regions: North America, Europe, Asia, LATAM, MEA, Oceania
- Metric: Daily active users over 12 months
- Current: Single cluttered chart with 6 lines

### Workflow

**Step 1: Use small multiples**
```
/construct-small-multiples
  dataset=[{region: "NA", month: 1, dau: 1000}, ...]
  index_variable="region"
  base_design={
    chart_type: "line",
    x_axis: "month",
    y_range: [0, 2000],
    colors: ["blue"]
  }
```
Result: 2×3 grid of line charts, invariant design

**Step 2: Assess the grid**
```
/assess-graphical-excellence
  "2×3 grid of line charts showing DAU by region"
```
Result: data_density=10/10, clarity=9/10

**Step 3: Remove any remaining junk**
```
/erase-non-data-ink
  "Grid with light grid lines, white background"
  data_elements=["lines", "axes"]
```
Result: minimal clean design

### Outcome
- Each region clearly visible in own frame
- Easy comparison across regions
- High data density (6 charts in same space)

---

## Example 4: Academic Research Visualization

### Scenario
Researcher needs to publish scatterplot of experimental results with outliers noted.

### Input
- 100 data points showing correlation
- 3 extreme outliers at (10, 200), (50, 5), (90, 180)
- Current: Basic scatterplot with legend

### Workflow

**Step 1: Generate range-frame**
```
/generate-range-frames
  x_min=0, x_max=100
  y_min=0, y_max=200
  axis_description="Scatterplot of experimental results"
```
Result: axes show exact data range

**Step 2: Integrate outlier annotations**
```
/integrate-text-and-graphic
  chart_description="Scatterplot with 3 extreme outliers"
  data_labels=["Outlier A: measurement error", "Outlier B: equipment fault", "Outlier C: valid extreme"]
  explanatory_text="Experimental results with anomaly annotations"
```
Result: each outlier directly labeled with explanation

**Step 3: Remove redundancy**
```
/erase-redundant-data-ink
  pruned_graphic="Scatterplot with points and outlier labels"
  visual_encodings=["point position", "outlier labels"]
```
Result: no duplicate encodings

### Outcome
- Clean scatterplot with zoomed axes
- Outliers directly explained on chart
- No separate legend needed
- Publication-ready quality

---

## Example 5: Quick Assessment via Orchestrator

### Scenario
Designer unsure if their infographic follows Tufte principles.

### Simple Approach
```
/orchestrate-tufte-vdqi
  "Is this infographic any good? It has icons, bright colors, and 3D pie charts."
```

### Result
- Intent detected: assessment
- Workflow triggered:
  1. assess-graphical-excellence → scores low on data-ink, integrity
  2. calculate-lie-factor → detects pie chart distortion
  3. Recommendations generated:
     - Replace 3D pie with bar chart
     - Remove decorative icons
     - Use color only for data

---

## Summary Table

| Example | Skills Used | Goal |
|---------|-------------|------|
| 1 | assess, lie-factor, erase-non-data | Fix misleading chart |
| 2 | standardize, range-frames, integrate | Design accurate time-series |
| 3 | small-multiples, assess, erase | Compare categories clearly |
| 4 | range-frames, integrate, erase-redundant | Publication-ready scatterplot |
| 5 | orchestrate (all) | Quick assessment |

---

## Key Takeaways

1. **Start with assessment** — Know what you're fixing
2. **Check lie factor** — Verify proportional representation  
3. **Erase in sequence** — Non-data first, then redundancy
4. **Integrate text** — Eliminate separate legends
5. **Use small multiples** — For category comparison
6. **Standardize money** — For time-series financial data
7. **Re-assess** — Verify improvements worked

---

See `USAGE_GUIDE.md` for detailed skill reference.
