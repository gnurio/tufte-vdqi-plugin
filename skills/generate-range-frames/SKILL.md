---
name: generate-range-frames
description: Convert non-data axes into elements that explicitly show the data's minimum and maximum
---

# Generate Range Frames

## Quick Start
Invoke with: `/generate-range-frames` and provide the required inputs.

## Purpose
Convert non-data axes into elements that explicitly show the data's minimum and maximum

## Inputs
- **x_min** (`number`): Minimum x-axis data value
- **x_max** (`number`): Maximum x-axis data value
- **y_min** (`number`): Minimum y-axis data value
- **y_max** (`number`): Maximum y-axis data value
- **axis_description** (`string`): Current axis configuration

## Outputs
- **range_framed_axes** (`description`): Axes trimmed to data bounds

## Decision Logic

1. **Extract data bounds**: x_min, x_max, y_min, y_max from dataset
2. **Check for single point**: If min == max, retain standard axes (needs context)
3. **Check for bar chart**: If y_min == 0 and bars present, preserve zero baseline
4. **Trim axes**: Set axis start = data min, axis end = data max
5. **Convert to range-frame**: Axis lines now explicitly show data range

**Benefits:**
- Increases data-ink ratio (axes now carry data information)
- Reduces empty space
- Makes data range immediately visible
- Enables more detail in plotting area

**Rule:** Graphic dimensions should match data dimensions (no padding beyond data)

## Success Criteria
Axis line lengths perfectly match exact range of plotted data

## Failure Modes
- Miscalculating min/max
- Creating floating frames without zero-baseline
- Overlapping frames with data points

## Edge Cases
- Datasets with extreme outliers
- Bar charts requiring zero baseline

## Examples

### Example 1: Scatterplot
Input: data X:20-80, Y:15-65, axes:0-100
Output: Range-frame X:20-80, Y:15-65

### Example 2: Time Series (narrow Y range)
Input: Y data:95-105, axis:0-120
Output: Range-frame Y:95-105 (better use of space)

## Implementation

```python
def generate_range_frames(x_min, x_max, y_min, y_max, axis_description):
    """
    Convert standard axes to range-frames showing exact data bounds.
    
    Returns description of range-framed axes.
    """
    desc_lower = axis_description.lower()
    
    # Check for bar chart (preserve zero baseline)
    is_bar_chart = "bar" in desc_lower
    
    # Check for single point (needs context)
    single_point = (x_min == x_max) or (y_min == y_max)
    
    if single_point:
        return {
            "range_framed_axes": "Standard axes retained - single point requires context"
        }
    
    # For bar charts, preserve Y zero baseline
    if is_bar_chart and y_min == 0:
        y_display_min = 0
    else:
        y_display_min = y_min
    
    # Generate range-frame description
    range_frame = f"Range-frame: X-axis {x_min}-{x_max}, Y-axis {y_display_min}-{y_max}"
    
    if is_bar_chart and y_min == 0:
        range_frame += " (must preserve zero baseline)"
    elif y_display_min == y_min:
        range_frame += " (zoomed to data range)"
    
    return {
        "range_framed_axes": range_frame
    }
```

## Related Skills
- erase-non-data-ink
- assess-graphical-excellence
- construct-small-multiples
- integrate-text-and-graphic
