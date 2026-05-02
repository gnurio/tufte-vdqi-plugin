---
name: integrate-text-and-graphic
description: Merge explanatory text and labels directly into the graphic to eliminate separate legends
---

# Integrate Text And Graphic

## Quick Start
Invoke with: `/integrate-text-and-graphic` and provide the required inputs.

## Purpose
Merge explanatory text and labels directly into the graphic to eliminate separate legends

## Inputs
- **chart_description** (`string`): Description of chart layout
- **data_labels** (`array`): Labels for data series/points
- **explanatory_text** (`string`): Contextual information to integrate

## Outputs
- **integrated_graphic** (`description`): Chart with embedded text
- **text_positions** (`array`): Positions of integrated text elements

## Decision Logic

1. **Identify all text elements**: Labels, legends, titles, annotations
2. **Locate data elements**: Find positions of series, points, regions
3. **Map text to nearest data**: Place each label adjacent to its referent
4. **Eliminate legend boxes**: Replace with direct labels on data
5. **Handle dense areas**: Use leader lines, compact marginal labels

**Integration strategies:**
- Line charts: Label at line endpoints
- Bar charts: Values on bars, categories below
- Scatterplots: Label key outliers, annotate clusters
- Maps: Place labels within regions or at centroids

**Rules:**
- Minimize eye movement (no darting to legends)
- Delete separate legend boxes when possible
- Place explanatory text adjacent to relevant data
- For dense areas: compromise with compact marginal key

## Success Criteria
Viewer can comprehend graphic without referencing external legend

## Failure Modes
- Overcrowding data space
- Obtrusive font sizes
- Illegible text over dark elements

## Edge Cases
- Highly dense scatterplots where direct labeling impossible

## Examples

### Example 1: Line Chart
Input: 3 lines with separate color legend
Output: Each line labeled at endpoint, legend removed

### Example 2: Scatterplot with Outlier
Input: Generic scatterplot, outlier mentioned in caption
Output: Outlier directly labeled on plot, explanation adjacent

## Implementation

```python
def integrate_text_and_graphic(chart_description, data_labels, explanatory_text):
    """
    Merge text and labels directly into graphic to eliminate separate legends.
    
    Returns integrated graphic description and text positions.
    """
    desc_lower = chart_description.lower()
    text_positions = []
    
    # Determine chart type and integration strategy
    is_line_chart = "line" in desc_lower
    is_bar_chart = "bar" in desc_lower
    is_scatter = "scatter" in desc_lower
    is_dense = "dense" in desc_lower or "500+" in chart_description
    
    has_separate_legend = "separate legend" in desc_lower or "legend in the corner" in desc_lower
    has_separate_table = "separate table" in desc_lower
    
    # Build integrated description
    integrated = chart_description
    
    if is_line_chart and has_separate_legend:
        integrated = integrated.replace("separate color legend in the corner", "direct labels at line endpoints")
        for label in data_labels:
            text_positions.append(f"end of {label} line")
    
    elif is_bar_chart and has_separate_table:
        integrated = integrated.replace("numeric values shown in separate table below", "values labeled directly on each bar")
        for label in data_labels:
            text_positions.append(f"on {label.split(':')[0]} bar")
    
    elif is_scatter and "outlier" in desc_lower:
        integrated = integrated.replace("generic title", f"title with note: {explanatory_text}")
        integrated = integrated.replace("one extreme outlier point", f"outlier labeled '{data_labels[0]}'")
        text_positions.append("at outlier point")
        text_positions.append("near outlier with arrow")
    
    elif is_dense:
        # Dense scatterplot compromise
        integrated = integrated.replace("impossible to label individually", "cluster labels at centroids")
        for label in data_labels:
            text_positions.append(f"near {label} centroid")
    
    # Add any remaining labels
    for label in data_labels:
        if not any(label in pos for pos in text_positions):
            text_positions.append(f"adjacent to {label}")
    
    # Add title/annotation position
    if explanatory_text:
        text_positions.append("chart title area")
    
    return {
        "integrated_graphic": integrated,
        "text_positions": text_positions
    }
```

## Related Skills
- erase-non-data-ink
- erase-redundant-data-ink
- assess-graphical-excellence
- construct-small-multiples
