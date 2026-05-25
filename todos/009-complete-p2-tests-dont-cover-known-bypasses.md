---
status: pending
priority: p2
issue_id: "009"
tags: [code-review, quality, tests, security]
dependencies: ["001", "002", "003", "005", "006"]
---

# Tests don't cover the confirmed bypasses

## Problem Statement
`WrapHtmlActiveContentTests` only assert the patterns the implementation already catches. When fixes for issues [[001]]–[[006]] land, regression tests must lock them in. Currently no test covers:
- `build_html()` direct-call bypass (issue 001)
- SMIL animation sinks (issue 002)
- Entity-encoded `javascript:` URLs (issue 003)
- `<use href="data:..."/>` (issue 005)
- `<image href="https://..."/>` (issue 005)
- `<svg:script>` namespaced bypass (issue 006)

## Findings
- **security-sentinel**: P3 — recommends negative tests for each confirmed bypass

## Proposed Solutions

### Option A — Add one negative test per bypass (Recommended)
For each bypass, add a test asserting `wrap_html.reject_active_svg(svg)` raises `ValueError` (or that `build_html(svg=...)` raises, post-fix).

## Recommended Action
Option A. Implement after the underlying fixes land.

## Technical Details
- File: `skills/render-tufte-chart/tests/test_text_escaping.py`

## Acceptance Criteria
- [ ] Test: `build_html(svg=<active>)` raises
- [ ] Test: `<animate attributeName="href" to="javascript:..."/>` rejected
- [ ] Test: `<set attributeName="href" to="javascript:..."/>` rejected
- [ ] Test: `<a href="&#106;avascript:..."/>` rejected (post-fix)
- [ ] Test: `<use href="data:..."/>` rejected
- [ ] Test: `<image href="https://..."/>` rejected
- [ ] Test: `<svg:script>` rejected
- [ ] Test: `<svg:foreignObject>` rejected

## Work Log
_(empty)_
