---
name: erase-non-data-ink
description: Remove non-essential structural or decorative ink that does not represent statistical information
---

# Erase Non Data Ink

## Quick Start
Invoke with: `/erase-non-data-ink` and provide the required inputs.

## Purpose
Remove non-essential structural or decorative ink that does not represent statistical information

## Inputs
- **graphic_description** (`string`): Description of the graphic elements
- **data_elements** (`array`): List of elements that represent data

## Outputs
- **pruned_graphic** (`description`): Graphic with non-data-ink removed
- **removed_elements** (`array`): List of removed non-data elements

## Decision Logic

1. Identify all elements in the graphic
2. Classify each element as:
   - **Data-ink**: Represents statistical information (bars, lines, points, labels)
   - **Non-data-ink**: Structural/decorative (grids, borders, backgrounds, effects)
3. For each non-data element, ask: "Does removing this erase data information?"
4. If NO data loss → mark for removal
5. Preserve essential structure (axes needed for reading)

**Priority removal targets:**
- Heavy grid lines → thin/lighten or remove
- Background colors → make white/transparent  
- 3D effects/shadows → flatten
- Decorative borders → remove
- Cross-hatching/moire → replace with solid fills
- Gradient fills → use flat colors

**Protected elements:**
- Data representations (bars, lines, points)
- Essential labels
- Axis lines (may thin but preserve)
- Lookup table grids (if precision needed)

## Success Criteria
Data-ink ratio approaches 1.0 without compromising legibility

## Failure Modes
- Erasing vital axes
- Over-pruning
- Leaving orphaned labels

## Edge Cases
- Lookup tables requiring precise grid lines

## Examples

### Example 1: Heavy Grid Removal
Input: Bar chart with thick black grid, dark background, 3D effects
Output: pruned_graphic="Bars with light/minimal grid, white background, flat", removed=["thick grid", "dark bg", "3D"]

### Example 2: Already Minimal
Input: Clean line chart with thin line, no grid
Output: pruned_graphic="Unchanged", removed=[]

### Example 3: Preserve Lookup Table
Input: Precise lookup table with fine grid
Output: pruned_graphic="Preserved with grid", removed=[] (grid is necessary)

## Implementation

```python
def erase_non_data_ink(graphic_description, data_elements):
    """
    Remove non-data ink from a graphic while preserving data information.
    
    Returns pruned graphic description and list of removed elements.
    """
    desc_lower = graphic_description.lower()
    removed = []
    
    # Define non-data ink patterns to remove
    removal_patterns = {
        "thick black grid lines": ["thick grid", "heavy grid", "black grid"],
        "dark gray background": ["dark background", "gray background", "colored background"],
        "decorative border": ["border", "frame", "bounding box"],
        "3D shadow effects": ["3D", "shadow", "drop shadow", "perspective"],
        "gradient fills": ["gradient", "gradient fill"],
        "patterned textures": ["pattern", "texture", "cross-hatched", "moire"],
        "unnecessary legend box": ["legend box", "separate legend"],
        "vibrating patterns": ["vibration", "moire", "cross-hatch"]
    }
    
    # Define protected elements (should not remove)
    protected = set(elem.lower() for elem in data_elements)
    
    # Check for lookup table exception
    is_lookup_table = "lookup" in desc_lower and "precise" in desc_lower
    
    for element_name, patterns in removal_patterns.items():
        for pattern in patterns:
            if pattern in desc_lower:
                # Check if this is protected
                if any(prot in pattern for prot in protected):
                    continue
                # Check lookup table exception for grids
                if is_lookup_table and "grid" in pattern:
                    continue
                removed.append(element_name)
                break
    
    # Build pruned description
    pruned = graphic_description
    replacements = {
        "thick black grid lines": "thin light gray grid or no grid",
        "dark gray background": "white background",
        "decorative border": "",
        "3D shadow effects": "flat design",
        "gradient fills": "flat color fills",
        "patterned textures": "solid fills",
        "cross-hatched shading": "solid gray fills"
    }
    
    for removed_item in removed:
        if removed_item in replacements:
            replacement = replacements[removed_item]
            if replacement:
                pruned = pruned.replace(removed_item.split()[0], replacement.split()[0] if replacement else "")
    
    # Clean up description
    pruned = pruned.replace("  ", " ").strip()
    
    if not removed:
        pruned = "Graphic unchanged - already minimal data-ink ratio"
    
    return {
        "pruned_graphic": pruned,
        "removed_elements": list(set(removed))  # deduplicate
    }
```

## Related Skills
- erase-redundant-data-ink
- assess-graphical-excellence
- calculate-lie-factor
- generate-range-frames
