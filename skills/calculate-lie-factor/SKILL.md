---
name: calculate-lie-factor
description: Calculate the mathematical distortion of a graphic by comparing visual effect size to data effect size.
---

# Calculate Lie Factor

## Quick Start
Invoke with: `/calculate-lie-factor` and provide the required inputs.

## Purpose
Calculate the mathematical distortion of a graphic by comparing visual effect size to data effect size

## Inputs
- **visual_change_percent** (`number`): Percentage change in visual representation
- **data_change_percent** (`number`): Percentage change in numerical data

## Outputs
- **lie_factor** (`number`): Ratio representing degree of visual distortion
- **is_distorted** (`boolean`): True if outside 0.95-1.05 range
- **distortion_type** (`string`): Type of distortion detected

## Decision Logic
1. Calculate lie_factor = visual_change_percent / data_change_percent
2. Handle edge cases:
   - If data_change_percent is 0: return null lie_factor, is_distorted=true, with error message
   - Use absolute values for negative changes (direction doesn't matter for ratio)
3. Determine is_distorted: true if lie_factor < 0.95 or lie_factor > 1.05
4. Valid range is 0.95-1.05 (Tufte's threshold for acceptable representation)

## Success Criteria
Accurate math, correct identification of base vs new value

## Failure Modes
- Division by zero
- Misidentifying visual boundaries
- Wrong base value selection

## Edge Cases
- Logarithmic scales
- 3D volume vs 2D area measurement

## Examples

### Example 1: Accurate Representation
Input: visual_change_percent=50, data_change_percent=50
Output: lie_factor=1.0, is_distorted=false

### Example 2: Severe Overstatement (Tufte's example)
Input: visual_change_percent=783, data_change_percent=53
Output: lie_factor=14.77, is_distorted=true
This is a severe distortion where the visual shows 783% change for 53% data change.

### Example 3: Division by Zero
Input: visual_change_percent=10, data_change_percent=0
Output: lie_factor=null, is_distorted=true, error="Cannot compute: zero data change"

## Related Skills
- assess-graphical-excellence
- erase-non-data-ink

## Implementation

```python
def calculate_lie_factor(visual_change_percent, data_change_percent, dimension=None):
    """
    Calculate the lie factor for a graphic.
    
    Lie Factor = Visual Change / Data Change
    
    Args:
        visual_change_percent: Percentage change in visual representation
        data_change_percent: Percentage change in actual data
        dimension: Optional - "length", "area", or "volume" for special handling
    
    Returns:
        dict with lie_factor, is_distorted, and optional error/note
    """
    # Handle division by zero
    if data_change_percent == 0:
        return {
            "lie_factor": None,
            "is_distorted": True,
            "error": "Cannot compute: zero data change"
        }
    
    # Calculate using absolute values (direction doesn't matter for ratio)
    lie_factor = abs(visual_change_percent) / abs(data_change_percent)
    
    # Determine if distorted (outside 0.95-1.05 range)
    is_distorted = lie_factor < 0.95 or lie_factor > 1.05
    
    result = {
        "lie_factor": round(lie_factor, 2),
        "is_distorted": is_distorted
    }
    
    # Add note for area/volume dimensions
    if dimension in ["area", "volume"]:
        result["note"] = f"2x length = 4x area" if dimension == "area" else "2x length = 8x volume"
    
    return result
```
