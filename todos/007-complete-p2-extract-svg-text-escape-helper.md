---
status: pending
priority: p2
issue_id: "007"
tags: [code-review, quality, dry]
dependencies: ["004"]
---

# Extract shared SVG-text-escape helper across the 4 renderers

## Problem Statement
The pattern `from html import escape` + `escape(value, quote=True)` is duplicated across 4 sibling renderer scripts at 12 call sites. When the policy evolves (e.g., to handle None-safety per [[004]], strip control chars, or allow specific markup), the change has to be made in 4 places. Classic "duplication beats premature abstraction… until it doesn't."

## Findings
- **kieran-python-reviewer**: P2 — recommends `_svg_text.py` helper module
- **simplicity-reviewer**: notes the current 12-site repetition is acceptable for a security fix, but agrees centralization is reasonable if paired with the None-fix

## Proposed Solutions

### Option A — `_svg_text.py` shared module (Recommended)
```python
# skills/render-tufte-chart/scripts/_svg_text.py
"""Shared SVG text-node helpers for the render-* scripts."""
from html import escape

def svg_text(value: object) -> str:
    """Escape arbitrary user-supplied text for safe inclusion in an SVG <text> node."""
    return escape("" if value is None else str(value), quote=True)
```
Each renderer: `from _svg_text import svg_text` and `svg_text(title)`, `svg_text(name)`, etc.
- Pros: Single place to evolve the policy; fixes [[004]] in one shot.
- Cons: One new file; scripts are no longer fully self-contained.
- Effort: Small
- Risk: Low

### Option B — Leave as-is
Keep the duplication; document the contract.
- Pros: Each script remains standalone.
- Cons: Future policy changes drift across files.
- Effort: None
- Risk: Medium over time

## Recommended Action
Option A — implement alongside [[004]].

## Technical Details
- New file: `skills/render-tufte-chart/scripts/_svg_text.py`
- Replace 12 escape call sites across `render_line_svg.py`, `small_multiples.py`, `quartile_plot.py`, `range_frame.py`

## Acceptance Criteria
- [ ] `_svg_text.py` exists with `svg_text()` helper
- [ ] All 4 renderers import and use the helper
- [ ] Test loader handles the new module (import resolves)
- [ ] All existing escape tests still pass

## Work Log
_(empty)_
