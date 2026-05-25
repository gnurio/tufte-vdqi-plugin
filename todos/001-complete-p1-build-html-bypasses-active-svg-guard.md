---
status: pending
priority: p1
issue_id: "001"
tags: [code-review, security, defense-in-depth]
dependencies: []
---

# build_html() bypasses the reject_active_svg guard

## Problem Statement
`reject_active_svg()` only runs in `main()` of `wrap_html.py`. The public `build_html()` function takes its `svg` argument and interpolates it verbatim into the HTML page. Any library caller that imports `wrap_html` and calls `build_html(...)` directly — tests, notebooks, future glue scripts — silently skips the security guard.

Empirically verified: `wrap_html.build_html('t','','<svg><script>alert(1)</script></svg>','c','x.css')` returns HTML with a live `<script>` element.

The contract "every caller of build_html must first call reject_active_svg" is informal and easy to forget.

## Findings
- **security-sentinel**: P1 — confirmed bypass with a direct call producing live `<script>` in output.
- **prior /code-review (Finding 3)**: confirmed empirically.

## Proposed Solutions

### Option A — Move guard inside build_html (Recommended)
Call `reject_active_svg(svg)` as the first line of `build_html()`. The `main()` call becomes redundant but harmless (or can be removed for clarity).
- Pros: Defense-in-depth; impossible for future callers to forget.
- Cons: ValueError now propagates through `build_html`; callers need to handle it.
- Effort: Small (1 line)
- Risk: Low

### Option B — Document the precondition + add type guard
Leave the guard in main() and add a docstring + assertion noting the precondition.
- Pros: No behavior change.
- Cons: Relies on every caller reading the docstring.
- Effort: Small
- Risk: Medium (humans skip docs)

## Recommended Action
Option A.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:87` (build_html)
- File: `skills/render-tufte-chart/scripts/wrap_html.py:134` (only existing call to reject_active_svg)

## Acceptance Criteria
- [ ] `wrap_html.build_html(..., svg='<svg><script>alert(1)</script></svg>', ...)` raises `ValueError`
- [ ] Existing CLI path still exits 1 with stderr message on rejection
- [ ] Add a regression test calling `build_html` directly with an active SVG

## Work Log
_(empty)_
