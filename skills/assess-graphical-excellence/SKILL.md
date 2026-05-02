---
name: assess-graphical-excellence
description: Evaluate a graphic against Tufte's nine criteria for graphical excellence
---

# Assess Graphical Excellence

## Quick Start
Invoke with: `/assess-graphical-excellence` and provide the required inputs.

## Purpose
Evaluate a graphic against Tufte's nine criteria for graphical excellence

## Inputs
- **graphic_description** (`string`): Description of the graphic to evaluate
- **context** (`string`): Purpose and audience of the graphic

## Outputs
- **scores** (`object`): Scores (0-10) for each of 9 criteria
- **overall_score** (`number`): Weighted overall score
- **recommendations** (`array`): Priority-ordered improvements

## Decision Logic

Evaluate the graphic against Tufte's 9 criteria, scoring each 0-10:

1. **Integrity** (weight: 3x) — Truthful, proportional representation?
   - Check for lie factor violations
   - Truncated axes
   - Missing context

2. **Data-Ink Ratio** (weight: 2x) — Maximize data-carrying ink?
   - Remove chartjunk
   - Eliminate redundant encoding

3. **Data Density** (weight: 1x) — High information per square inch?
   - Small multiples
   - Compact display

4. **Clarity** (weight: 1x) — Unambiguous display?
   - Clear labels
   - Readable typography

5. **Proportionality** (weight: 2x) — Visual magnitude = data magnitude?
   - Accurate scaling
   - No 2D/3D area distortions

6. **Context** (weight: 1x) — Data in appropriate context?
   - Full time series shown
   - Comparisons provided

7. **Minimal Ink** (weight: 1x) — No redundant encoding?
   - Each datum encoded once
   - Range frames vs full boxes

8. **Typography** (weight: 0.5x) — Clear, readable labels?
   - Font choices
   - Label placement

9. **Integration** (weight: 1x) — Words, numbers, pictures combined?
   - Direct labeling
   - No separate legends

Overall score = weighted average of all criteria.
Recommendations prioritized by impact on integrity and data-ink ratio.

## Success Criteria
All 9 criteria assessed with specific observations justifying scores

## Failure Modes
- Missing criteria in assessment
- Scores not justified
- Confusing design flaws with integrity violations

## Edge Cases
- Graphics with unconventional but effective designs
- Culturally specific visualization norms

## Examples

### Example 1: Excellent Chart
Input: Time-series with thin line, range-frame, no grid, direct labels
Output: scores={integrity:10, data_ink_ratio:9, ...}, overall_score:8.9, recommendations:[]

### Example 2: Chart with Lie Factor Violation
Input: Bar chart showing 53% as 783% visual increase
Output: scores={integrity:2, proportionality:1, ...}, overall_score:4.1, recommendations:["Fix lie factor", "Show full axis"]

## Implementation

```python
def assess_graphical_excellence(graphic_description, context):
    """
    Assess a graphic against Tufte's 9 criteria for graphical excellence.
    
    Returns scores (0-10), overall weighted score, and recommendations.
    """
    # Keywords for detection
    integrity_issues = ["truncated", "lie factor", "3D", "distorted", "misleading"]
    high_data_ink = ["thin line", "range-frame", "no grid", "minimal"]
    low_data_ink = ["heavy grid", "3D", "shadow", "decorative", "chartjunk"]
    
    scores = {
        "integrity": 10,
        "data_ink_ratio": 5,
        "data_density": 5,
        "clarity": 5,
        "proportionality": 10,
        "context": 5,
        "minimal_ink": 5,
        "typography": 5,
        "integration": 5
    }
    
    desc_lower = graphic_description.lower()
    
    # Assess integrity
    if any(issue in desc_lower for issue in ["truncated", "lie factor", "783"]):
        scores["integrity"] = 2
        scores["proportionality"] = 1
    elif "3D" in graphic_description:
        scores["integrity"] = 5
        scores["proportionality"] = 4
    
    # Assess data-ink ratio
    if any(feature in desc_lower for feature in high_data_ink):
        scores["data_ink_ratio"] = 9
        scores["minimal_ink"] = 9
    elif any(feature in desc_lower for feature in low_data_ink):
        scores["data_ink_ratio"] = 3
        scores["minimal_ink"] = 3
    
    # Assess clarity and integration
    if "direct label" in desc_lower or "integrated" in desc_lower:
        scores["clarity"] = 9
        scores["integration"] = 9
    elif "legend" in desc_lower and "separate" in desc_lower:
        scores["integration"] = 4
    
    # Assess data density
    if "small multiples" in desc_lower or "high density" in desc_lower:
        scores["data_density"] = 9
    
    # Assess typography
    if "clear" in desc_lower or "readable" in desc_lower:
        scores["typography"] = 8
    
    # Assess context
    if "context" in desc_lower or "full series" in desc_lower:
        scores["context"] = 8
    
    # Calculate weighted overall score
    weights = {
        "integrity": 3,
        "data_ink_ratio": 2,
        "data_density": 1,
        "clarity": 1,
        "proportionality": 2,
        "context": 1,
        "minimal_ink": 1,
        "typography": 0.5,
        "integration": 1
    }
    
    total_weight = sum(weights.values())
    overall = sum(scores[k] * weights[k] for k in scores) / total_weight
    
    # Generate recommendations based on low scores
    recommendations = []
    if scores["integrity"] < 5:
        recommendations.append("Fix lie factor - show proportional visual change")
        recommendations.append("Use consistent scale")
    if scores["data_ink_ratio"] < 5:
        recommendations.append("Remove chartjunk")
        recommendations.append("Increase data-ink ratio")
    if scores["integration"] < 5:
        recommendations.append("Move labels onto data")
    
    return {
        "scores": scores,
        "overall_score": round(overall, 1),
        "recommendations": recommendations
    }
```

## Related Skills
- calculate-lie-factor
- erase-non-data-ink
- construct-small-multiples
- integrate-text-and-graphic
