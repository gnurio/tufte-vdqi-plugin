---
status: pending
priority: p1
issue_id: "004"
tags: [code-review, quality, regression]
dependencies: []
---

# Renderer render() functions now crash on None/non-str title/subtitle/series

## Problem Statement
The escape fix wraps `title`, `subtitle`, `series`, and `name` with `html.escape(value, quote=True)` unconditionally. `html.escape` requires a string and raises `AttributeError: 'NoneType' object has no attribute 'replace'` (or similar for int/float). The pre-patch f-string silently stringified `None` to `'None'` and numerics to their `str()` representation.

Empirically verified:
```
render_line_svg.render([{'x':1,'y':2},{'x':2,'y':3}], title=None)
→ AttributeError: 'NoneType' object has no attribute 'replace'

render_line_svg.render([{'x':1,'y':2},{'x':2,'y':3}], title=2024)
→ AttributeError: 'int' object has no attribute 'replace'
```

CLI users are unaffected (argparse default `""`). Library callers — notebooks, future scripts, callers passing pandas/numpy scalars — regress.

## Findings
- **kieran-python-reviewer**: P1 — recommends centralized helper for None-safety
- **prior /code-review (Findings 6–9)**: same regression flagged across all 4 renderers
- **simplicity-reviewer**: agrees `escape(str(name), quote=True)` for facet/group names is correct defensive

## Proposed Solutions

### Option A — Extract a shared helper module (Recommended; pairs with [[007]])
Create `skills/render-tufte-chart/scripts/_svg_text.py`:
```python
from html import escape

def svg_text(value: object) -> str:
    """Escape arbitrary value for safe inclusion in an SVG <text> node."""
    return escape("" if value is None else str(value), quote=True)
```
Route all 12 escape sites in the 4 renderers through `svg_text(...)`. Restores `None → ""` (slightly different from old behavior where None → 'None', but cleaner output).
- Pros: Fixes regression + DRY violation in one shot; one place to evolve the policy.
- Cons: Adds a tiny shared module; old behavior printed literal 'None'.
- Effort: Small
- Risk: Low

### Option B — Defensive str() at each call site
Replace `escape(title, quote=True)` with `escape(str(title or ""), quote=True)` (or `str(title)` if literal 'None' is wanted) at every site.
- Pros: No new file.
- Cons: 12 edits; bakes in the DRY violation.
- Effort: Small
- Risk: Low

## Recommended Action
Option A — combine with [[007-extract-svg-text-escape-helper]].

## Technical Details
- `skills/render-tufte-chart/scripts/render_line_svg.py:47,50,68`
- `skills/render-tufte-chart/scripts/range_frame.py:43,45`
- `skills/render-tufte-chart/scripts/quartile_plot.py:58,60,82`
- `skills/render-tufte-chart/scripts/small_multiples.py:70,72,80`

## Acceptance Criteria
- [ ] `render(..., title=None)` does not raise in any of the 4 renderers
- [ ] `render(..., title=2024)` does not raise (renders as "2024")
- [ ] Regression test per renderer asserting None tolerance
- [ ] All existing escape tests still pass

## Work Log
_(empty)_
