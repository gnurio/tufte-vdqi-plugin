---
status: pending
priority: p3
issue_id: "011"
tags: [code-review, agent-native, dx]
dependencies: []
---

# Add stable error code tags for agent-dispatchable error handling

## Problem Statement
Agents reading script stderr today have to substring-match on human phrases like "refusing to wrap" or "cannot read SVG" to dispatch on failure type. A stable error code tag would let agents branch deterministically.

## Findings
- **agent-native-reviewer**: P3 — recommends `ERROR[active-svg]:`, `ERROR[svg-read]:`, `ERROR[missing-assets]:` for symmetry

## Proposed Solutions

### Option A — Tagged ERROR prefixes (Recommended)
- `wrap_html.py:131`: `print(f"ERROR[svg-read]: cannot read SVG {a.svg}: {e}", ...)`
- `wrap_html.py:137`: `print(f"ERROR[active-svg]: {e}", ...)`
- `wrap_html.py:144`: `print(f"ERROR[missing-assets]: {e}", ...)`
- Apply same pattern to other scripts' error sites
- Pros: Agent-dispatchable; backward-compatible (still starts with `ERROR:` prefix grep)
- Cons: 3-4 line changes per script
- Effort: Small
- Risk: Low

## Recommended Action
Option A.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:131,137,144`
- File: All four renderer scripts' error-printing sites for consistency

## Acceptance Criteria
- [ ] wrap_html.py error sites use `ERROR[<tag>]:` format
- [ ] All four renderers use the same convention
- [ ] Tags documented in SKILL.md (link from [[010]])

## Work Log
_(empty)_
