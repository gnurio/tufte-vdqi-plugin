---
name: orchestrate-tufte-vdqi
description: Intelligent router for the Tufte VDQI skill network. Analyzes data visualization requests and routes to the right entry-point skill for assessment, design, or optimization. Use whenever you need help with data visualization and aren't sure which specific Tufte skill to invoke.
---

# Orchestrate Tufte VDQI

Intelligent router for Tufte's Visual Display of Quantitative Information skills.

## How It Works

1. **Detects intent** — Assessment, design, or optimization?
2. **Routes to skills** — Picks the right entry-point skill
3. **Chains workflows** — Connects multiple skills for complex tasks
4. **Accumulates context** — Maintains coherence across iterations

## Skill Network (8 Skills)

### Assessment Skills
- `assess-graphical-excellence` — Evaluate against 9 Tufte criteria
- `calculate-lie-factor` — Detect visual distortion

### Design Skills
- `construct-small-multiples` — Create comparative grids
- `generate-range-frames` — Trim axes to data bounds
- `integrate-text-and-graphic` — Merge labels into graphics

### Optimization Skills
- `erase-non-data-ink` — Remove decorative elements
- `erase-redundant-data-ink` — Remove duplicate encodings
- `standardize-monetary-units` — Adjust for inflation

## Routing Logic

```
IF user wants to EVALUATE a graphic:
  → assess-graphical-excellence
  → calculate-lie-factor (if distortion suspected)

IF user wants to DESIGN a graphic:
  → construct-small-multiples (if comparing categories)
  → generate-range-frames (for axes)
  → integrate-text-and-graphic (for labeling)

IF user wants to OPTIMIZE a graphic:
  → erase-non-data-ink (remove decoration)
  → erase-redundant-data-ink (remove duplication)
  → standardize-monetary-units (if time-series money)

IF user is UNSURE:
  → Start with assess-graphical-excellence
```

## Workflows

### "Is this graphic any good?"
```
assess-graphical-excellence → calculate-lie-factor → recommendations
```

### "I need to design a time-series"
```
standardize-monetary-units (if monetary) → generate-range-frames → integrate-text-and-graphic
```

### "This chart feels cluttered"
```
assess-graphical-excellence → erase-non-data-ink → erase-redundant-data-ink → reassess
```

## Implementation

```python
def orchestrate_tufte_vdqi(request, graphic_description=None, data=None):
    """
    Route visualization requests to appropriate Tufte VDQI skills.
    
    Returns workflow recommendation and skill sequence.
    """
    request_lower = request.lower()
    
    # Detect intent
    is_assessment = any(word in request_lower for word in ["evaluate", "assess", "check", "review", "good", "bad"])
    is_design = any(word in request_lower for word in ["design", "create", "build", "make", "new"])
    is_optimize = any(word in request_lower for word in ["optimize", "improve", "fix", "clean", "declutter", "better"])
    
    # Check for specific needs
    has_money = any(word in request_lower for word in ["money", "dollar", "revenue", "cost", "price", "inflation"])
    has_time = any(word in request_lower for word in ["time", "year", "month", "trend", "series"])
    has_comparison = any(word in request_lower for word in ["compare", "multiple", "category", "region", "group"])
    
    workflow = []
    
    if is_assessment:
        workflow.append("assess-graphical-excellence")
        if graphic_description and ("distort" in request_lower or "3D" in str(graphic_description)):
            workflow.append("calculate-lie-factor")
    
    elif is_design:
        if has_comparison:
            workflow.append("construct-small-multiples")
        if has_money and has_time:
            workflow.append("standardize-monetary-units")
        workflow.append("generate-range-frames")
        workflow.append("integrate-text-and-graphic")
    
    elif is_optimize:
        workflow.append("assess-graphical-excellence")
        workflow.append("erase-non-data-ink")
        workflow.append("erase-redundant-data-ink")
        if has_money and has_time:
            workflow.append("standardize-monetary-units")
        workflow.append("assess-graphical-excellence")  # Re-assess
    
    else:
        # Default: assessment
        workflow.append("assess-graphical-excellence")
    
    return {
        "detected_intent": "assessment" if is_assessment else "design" if is_design else "optimization" if is_optimize else "unknown",
        "recommended_workflow": workflow,
        "rationale": f"Based on keywords in request: intent={is_assessment or is_design or is_optimize}"
    }
```
