---
status: pending
priority: p2
issue_id: "008"
tags: [code-review, quality, tests]
dependencies: []
---

# Tests use substring assertions instead of structural XML checks

## Problem Statement
`_assert_no_injection` does a substring check (`"<script>" not in svg`). This catches the canonical payload but misses:
- Partial escaping (e.g. if a future renderer escapes `<` but forgets `"`)
- Attribute-injection payloads (a payload that becomes an `onload=` attribute would still pass)
- Future renderers that put user text inside attributes instead of element bodies

## Findings
- **kieran-python-reviewer**: P2 — recommends `xml.etree.ElementTree.fromstring(svg)` + assert no `script`/`foreignObject` element + no `on*` attribute anywhere

## Proposed Solutions

### Option A — Parse + structural assertions (Recommended)
```python
import xml.etree.ElementTree as ET

def _assert_no_injection(test, svg):
    root = ET.fromstring(svg)
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]  # strip namespace
        test.assertNotIn(tag.lower(), {"script", "foreignobject"})
        for attr in el.attrib:
            test.assertFalse(attr.lower().startswith("on"))
```
Add a quote-bearing payload (`PAYLOAD2 = '" onload="alert(1)" x="'`) to catch attribute-injection regressions.
- Pros: Catches partial-escape and attribute-injection.
- Cons: Slightly more setup per test.
- Effort: Small
- Risk: Low

### Option B — Keep substring + add quote-payload tests
Less complete but cheaper.
- Effort: Smaller
- Risk: Medium (won't catch all regressions)

## Recommended Action
Option A.

## Technical Details
- File: `skills/tufte-chart/tests/test_text_escaping.py:44-48` (`_assert_no_injection`)

## Acceptance Criteria
- [ ] `_assert_no_injection` parses SVG and asserts structurally
- [ ] Quote-bearing payload added: `'" onload="alert(1)" x="'`
- [ ] Tests still pass on current code
- [ ] Helper also asserts no `on*` attribute anywhere in the tree

## Work Log
_(empty)_
