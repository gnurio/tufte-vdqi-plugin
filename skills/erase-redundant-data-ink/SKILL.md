---
name: erase-redundant-data-ink
description: Strip away visual markers that depict the exact same data point multiple ways
---

# Erase Redundant Data Ink

## Quick Start
Invoke with: `/erase-redundant-data-ink` and provide the required inputs.

## Purpose
Strip away visual markers that depict the exact same data point multiple ways

## Inputs
- **pruned_graphic** (`description`): Graphic already cleared of non-data-ink
- **visual_encodings** (`array`): How data maps to visual attributes

## Outputs
- **minimal_graphic** (`description`): Graphic stripped of redundancy
- **redundancy_reduced** (`boolean`): Whether redundancy was found and removed

## Decision Logic

1. **Identify all visual encodings** used to represent data
2. **Group by data attribute**: Which encodings show the same information?
3. **Apply Tufte's rule**: If N encodings show the same datum, remove N-1
4. **Preserve clarity**: Never reduce to ambiguity

**Common redundancies to eliminate:**
- Bar height + shading + border + label (keep height, remove rest)
- Bilateral symmetry in box plots (show half)
- Line + points + labels (keep line, minimal markers)
- Color + pattern + shape (choose one)

**Protected from removal:**
- Primary encoding (usually position)
- Accessibility encodings (colorblind-friendly)
- Cyclical redundancy (train schedules repeating)

## Success Criteria
Each data point represented by minimum necessary visual markers

## Failure Modes
- Erasing too much causing ambiguity
- Missing implicit redundancy
- Removing necessary orientation cues

## Edge Cases
- Cyclical time-series where redundancy aids tracking

## Examples

### Example 1: Bar with Multiple Encodings
Input: Bar showing value via height, shading, border, label
Output: Keep height only, remove shading/border/label (or label key points)

### Example 2: Symmetric Box Plot  
Input: Full bilateral box plot
Output: Asymmetric half-box showing same statistics

## Implementation

```python
def erase_redundant_data_ink(pruned_graphic, visual_encodings):
    """
    Remove redundant encodings where same data is shown multiple ways.
    
    Returns minimal graphic description and whether redundancy was reduced.
    """
    desc_lower = pruned_graphic.lower()
    encodings = [e.lower() for e in visual_encodings]
    
    redundancy_found = False
    reductions = []
    
    # Check for bar height + shading + border + label redundancy
    if "bar" in desc_lower:
        if "height" in encodings and ("shading" in encodings or "color" in encodings):
            redundancy_found = True
            reductions.append("Remove shading - height already encodes value")
        if "height" in encodings and "border" in encodings:
            redundancy_found = True
            reductions.append("Remove border - unnecessary frame")
        if "height" in encodings and "label" in encodings:
            redundancy_found = True
            reductions.append("Reduce to key point labels only")
    
    # Check for line + points + labels redundancy
    if "line" in desc_lower or "chart" in desc_lower:
        if "line" in encodings and "point" in encodings:
            redundancy_found = True
            reductions.append("Remove point markers - line shows path")
        if "line" in encodings and "label" in encodings:
            redundancy_found = True
            reductions.append("Label only key inflection points")
    
    # Check for symmetric/bilateral redundancy
    if "symmetric" in desc_lower or "bilateral" in desc_lower or "full box" in desc_lower:
        redundancy_found = True
        reductions.append("Convert to asymmetric half-box")
    
    # Check for color + pattern redundancy
    if "color" in encodings and "pattern" in encodings:
        redundancy_found = True
        reductions.append("Use color OR pattern, not both")
    
    # Build minimal graphic description
    if redundancy_found:
        minimal = f"Minimal version: {pruned_graphic}. " + "; ".join(reductions)
    else:
        minimal = "No changes needed - already minimal encoding"
    
    return {
        "minimal_graphic": minimal,
        "redundancy_reduced": redundancy_found
    }
```

## Related Skills
- erase-non-data-ink
- assess-graphical-excellence
- generate-range-frames
- construct-small-multiples
