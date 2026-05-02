---
name: render-tufte-chart
description: Render data visualizations using Tufte's visual style with the Tufte CSS library. Creates publication-ready charts with minimal ink, proper typography, and elegant data presentation. Use when you need to generate actual visual output following Tufte principles.
---

# Render Tufte Chart

## Quick Start
Invoke with: `/render-tufte-chart` and provide chart specification

## Purpose
Generate publication-ready charts using the Tufte CSS library that embody Edward Tufte's principles of graphical excellence:
- Minimal chartjunk
- Maximum data-ink ratio
- Elegant typography
- Clear, uncluttered presentation

## Inputs
- **chart_type** (`string`): Type of chart (line, bar, scatter, small-multiples)
- **data** (`array`): Array of data points with x/y values
- **title** (`string`): Chart title
- **subtitle** (`string`, optional): Subtitle or caption
- **x_label** (`string`, optional): X-axis label
- **y_label** (`string`, optional): Y-axis label
- **show_grid** (`boolean`, default: false): Whether to show minimal grid
- **color_scheme** (`string`, default: "monochrome"): "monochrome", "subtle", or "minimal"
- **width** (`number`, default: 800): Chart width in pixels
- **height** (`number`, default: 400): Chart height in pixels

## Outputs
- **html_output** (`string`): Complete HTML with embedded Tufte CSS
- **css_classes** (`array`): Tufte CSS classes used
- **data_ink_ratio** (`number`): Calculated data-ink ratio
- **file_path** (`string`, optional): Path to saved HTML file

## Decision Logic
1. Select appropriate Tufte CSS chart type
2. Apply minimal styling (no chartjunk)
3. Use typography from ET-Bembo or similar
4. Calculate and report data-ink ratio
5. Generate clean, printable HTML

## CSS Classes Applied
- `.tufte-chart` — Base chart container
- `.chart-line` — Line charts (thin, elegant)
- `.chart-bar` — Bar charts (minimal bars)
- `.chart-scatter` — Scatter plots (small dots)
- `.chart-multiples` — Small multiples grid
- `.range-frame` — Trimmed axes
- `.data-label` — Direct labels (no legends)

## Examples

### Example 1: Simple Line Chart
```yaml
chart_type: "line"
data: [{x: 2018, y: 100}, {x: 2019, y: 120}, {x: 2020, y: 115}]
title: "Revenue Trends"
subtitle: "Annual revenue in thousands"
show_grid: false
color_scheme: "monochrome"
```

Output: Clean HTML with thin line, minimal axes, elegant typography

### Example 2: Small Multiples
```yaml
chart_type: "small-multiples"
data: [
  {region: "North", values: [{x: 1, y: 10}, {x: 2, y: 15}]},
  {region: "South", values: [{x: 1, y: 12}, {x: 2, y: 18}]}
]
title: "Regional Comparison"
```

Output: 1×2 grid with identical design across frames

## Implementation

```python
def render_tufte_chart(chart_type, data, title, **options):
    """
    Render chart using Tufte CSS library.
    
    Returns HTML with embedded CSS and calculated data-ink ratio.
    """
    # Tufte CSS base styles
    tufte_css = """
    .tufte-chart {
      font-family: "ET-Bembo", "Palatino Linotype", serif;
      max-width: 100%;
      margin: 0 auto;
    }
    .tufte-chart svg {
      background: transparent;
    }
    .chart-line {
      stroke: #333;
      stroke-width: 1.5;
      fill: none;
    }
    .chart-bar {
      fill: #666;
      stroke: none;
    }
    .chart-scatter circle {
      fill: #333;
      r: 2;
    }
    .axis line, .axis path {
      stroke: #888;
      stroke-width: 0.5;
    }
    .axis text {
      font-size: 11px;
      fill: #333;
    }
    .chart-title {
      font-size: 16px;
      font-weight: normal;
      margin-bottom: 0.5rem;
    }
    .chart-subtitle {
      font-size: 13px;
      color: #666;
      margin-bottom: 1rem;
    }
    .range-frame line {
      stroke: #333;
      stroke-width: 1;
    }
    """
    
    # Generate SVG based on chart type
    if chart_type == "line":
        svg = generate_line_chart(data, options)
    elif chart_type == "bar":
        svg = generate_bar_chart(data, options)
    elif chart_type == "scatter":
        svg = generate_scatter_chart(data, options)
    elif chart_type == "small-multiples":
        svg = generate_small_multiples(data, options)
    
    # Calculate data-ink ratio
    data_ink_ratio = calculate_data_ink_ratio(svg)
    
    # Assemble HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>{tufte_css}</style>
</head>
<body>
<div class="tufte-chart">
  <div class="chart-title">{title}</div>
  {f'<div class="chart-subtitle">{options.get("subtitle")}</div>' if options.get("subtitle") else ''}
  {svg}
</div>
</body>
</html>"""
    
    return {
        "html_output": html,
        "css_classes": ["tufte-chart", f"chart-{chart_type}"],
        "data_ink_ratio": round(data_ink_ratio, 2),
        "file_path": options.get("output_path")
    }

def calculate_data_ink_ratio(svg):
    """Calculate data-ink ratio from SVG."""
    # Simplified calculation
    # In real implementation, would analyze SVG elements
    total_ink = estimate_total_ink(svg)
    data_ink = estimate_data_ink(svg)
    return data_ink / total_ink if total_ink > 0 else 0
```

## Success Criteria
- HTML renders correctly in browsers
- Data-ink ratio > 0.7 (Tufte standard)
- No chartjunk (3D, heavy grids, decorative elements)
- Typography follows Tufte conventions
- Responsive design

## Related Skills
- assess-graphical-excellence (validate output)
- calculate-lie-factor (check for distortion)
- erase-non-data-ink (remove any added chartjunk)
- construct-small-multiples (for multiple charts)

## Tufte CSS Library
Uses principles from:
- ET-Bembo typography
- Minimal ink philosophy
- Range-frame axes
- Direct labeling

## Output Example
```html
<!DOCTYPE html>
<html>
<head>
<style>
  .tufte-chart { font-family: "ET-Bembo", serif; }
  .chart-line { stroke: #333; stroke-width: 1.5; fill: none; }
</style>
</head>
<body>
<div class="tufte-chart">
  <div class="chart-title">Revenue Trends</div>
  <svg viewBox="0 0 800 400">
    <!-- Minimal, elegant chart -->
  </svg>
</div>
</body>
</html>
```
