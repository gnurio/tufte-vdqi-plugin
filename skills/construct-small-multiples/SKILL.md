---
name: construct-small-multiples
description: Create a high-density comparative grid of shrunken graphics sharing the exact same design
---

# Construct Small Multiples

## Quick Start
Invoke with: `/construct-small-multiples` and provide the required inputs.

## Purpose
Create a high-density comparative grid of shrunken graphics sharing the exact same design

## Inputs
- **dataset** (`array`): High-dimensional dataset
- **index_variable** (`string`): Dimension to split by (time, category, geography)
- **base_design** (`object`): Design parameters for each multiple

## Outputs
- **small_multiples_grid** (`description`): Matrix of mini-charts
- **grid_dimensions** (`string`): Layout of the grid

## Decision Logic

1. **Split dataset** by index variable (time, category, geography)
2. **Apply base design identically** to each subset (NO variations)
3. **Shrink each graphic** using Tufte's Shrink Principle
4. **Arrange in logical grid** (chronological, alphabetical, geographic)
5. **Ensure invariant design**: Same scales, colors, markers across all frames

**Key principles:**
- Design must be absolutely constant (forces attention to data changes)
- Shared axes for comparability
- Shrink to increase data density
- Logical ordering (time→left-to-right, geography→N-to-S)

**Grid layout:**
- 2-4 multiples: 1 row or column
- 5-9 multiples: 2-3 rows
- 10+ multiples: 3+ rows, consider pagination

## Success Criteria
Design remains invariant across all frames, attention forced onto data variation

## Failure Modes
- Varying axes between multiples
- Shrinking too much causing illegibility
- Inconsistent spacing

## Edge Cases
- Highly disparate data ranges making shared axis obscure local trends
- Missing data in subsets

## Examples

### Example 1: Time Series by Year
Input: 24 months of data, split by year
Output: 2 line charts (2018, 2019), same design, 2x1 grid

### Example 2: Geographic Comparison  
Input: Sales by region across 4 quarters
Output: 2x2 grid of bar charts, identical axes, invariant design

## Implementation

```python
def construct_small_multiples(dataset, index_variable, base_design):
    """
    Create a grid of shrunken graphics with invariant design.
    
    Returns grid description and dimensions.
    """
    # Group data by index variable
    groups = {}
    for record in dataset:
        key = record.get(index_variable)
        if key not in groups:
            groups[key] = []
        groups[key].append(record)
    
    num_multiples = len(groups)
    keys = sorted(groups.keys())
    
    # Determine grid dimensions
    if num_multiples <= 2:
        rows, cols = num_multiples, 1
    elif num_multiples <= 4:
        rows, cols = 2, 2
    elif num_multiples <= 6:
        rows, cols = 2, 3
    elif num_multiples <= 9:
        rows, cols = 3, 3
    else:
        rows, cols = 3, (num_multiples + 2) // 3
    
    # Check for missing data
    has_missing = any(
        any(record.get(k) is None for k in record if k != index_variable)
        for group in groups.values()
        for record in group
    )
    
    chart_type = base_design.get("chart_type", "line")
    
    # Build grid description
    grid_desc = f"{rows}x{cols} grid of {chart_type} charts: " + ", ".join(str(k) for k in keys)
    
    # Add design invariants note
    invariants = []
    if "y_range" in base_design:
        invariants.append(f"Y-axis {base_design['y_range']}")
    if "x_range" in base_design:
        invariants.append(f"X-axis {base_design['x_range']}")
    if "colors" in base_design:
        invariants.append(f"colors {base_design['colors']}")
    
    if invariants:
        grid_desc += " - ALL with identical " + ", ".join(invariants)
    
    if has_missing:
        grid_desc += ", handling missing data with gaps"
    
    return {
        "small_multiples_grid": grid_desc,
        "grid_dimensions": f"{rows} row{'s' if rows > 1 else ''} x {cols} column{'s' if cols > 1 else ''}"
    }
```

## Related Skills
- assess-graphical-excellence
- erase-non-data-ink
- integrate-text-and-graphic
- generate-range-frames
