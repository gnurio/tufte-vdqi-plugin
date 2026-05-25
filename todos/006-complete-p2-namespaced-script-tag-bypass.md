---
status: pending
priority: p2
issue_id: "006"
tags: [code-review, security, defense-in-depth]
dependencies: []
---

# Namespace-prefixed element tags bypass the regex

## Problem Statement
The `<script>` and `<foreignObject>` patterns require the literal tag name immediately after `<`. Namespaced forms like `<svg:script>alert(1)</svg:script>` are not matched. Inline-HTML-SVG parsing mostly ignores namespace prefixes for execution, but defense-in-depth requires the guard to honor its stated promise.

Empirically verified MISS for `<svg:script>alert(1)</svg:script>`.

## Findings
- **security-sentinel**: P1 — recommends prefix-tolerant pattern
- **prior /code-review (Finding 5)**: same

## Proposed Solutions

### Option A — Prefix-tolerant regex (Recommended)
Change each element pattern to `r"<\s*(?:[A-Za-z][\w.-]*:)?<element>\b"`. Apply to script, foreignObject, use, image, animate, set, etc.
- Pros: One-pattern fix that doesn't enumerate all namespace prefixes.
- Cons: Slightly less readable.
- Effort: Small
- Risk: Low

### Option B — Real parser
See [[003-pending-p1-javascript-url-entity-encoding-bypass]] Option C.

## Recommended Action
Option A — pair with [[002]] when adding SMIL patterns.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:25-30`

## Acceptance Criteria
- [ ] `<svg:script>` rejected
- [ ] `<xhtml:script>` rejected (any prefix)
- [ ] Same for `<svg:foreignObject>`, `<svg:use>`, etc.
- [ ] Regression test added

## Work Log
_(empty)_
