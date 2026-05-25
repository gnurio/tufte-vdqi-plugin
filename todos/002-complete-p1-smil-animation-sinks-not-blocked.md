---
status: pending
priority: p1
issue_id: "002"
tags: [code-review, security, xss]
dependencies: []
---

# SMIL animation elements (<animate>, <set>) bypass the guard

## Problem Statement
`reject_active_svg()` has no pattern for SMIL animation elements. An attacker can mutate an `href` to `javascript:` at runtime using `<animate attributeName="href" to="javascript:alert(1)"/>` inside an `<a>` tag — the regex never sees a literal `javascript:` because the value is supplied dynamically. Firefox and Safari honor SMIL on `<a>`/`<image>`/`<use>` and execute the resulting URL on click (or self-trigger via `begin="0s"`).

## Findings
- **security-sentinel**: P1 with concrete exploit. Verified bypass.
- **prior /code-review (Finding 1)**: confirmed via regex test.

Empirical regex check:
```
MISS [[]] SMIL animation: <animate attributeName="href" to="javascript:alert(1)"/>
```

## Proposed Solutions

### Option A — Add SMIL elements to _ACTIVE_SVG_PATTERNS (Recommended)
Add: `re.compile(r"<\s*(?:[A-Za-z][\w.-]*:)?(animate|animateTransform|animateMotion|set)\b", re.IGNORECASE)`
- Pros: One pattern, blocks all SMIL animation sinks (also handles namespaced prefixes — see issue 006).
- Cons: Rejects legitimate uses of SMIL (rare in static Tufte charts; the trusted renderers never emit SMIL).
- Effort: Small
- Risk: Low

### Option B — Element/attribute allowlist via real XML parser
Parse SVG with `xml.etree.ElementTree`, walk tree, allowlist known-safe elements/attributes only.
- Pros: Closes whole classes of bypass at once (also fixes issues 003, 005, 006).
- Cons: Larger change, requires careful allowlist design, may need iteration on legitimate complex SVGs.
- Effort: Medium
- Risk: Medium (could reject valid hand-authored SVGs the user wants to wrap)

## Recommended Action
Option A as immediate fix. Consider Option B if more bypasses surface — track it under issue [[strategic-sanitizer-redesign]] if created.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:23-39` (`_ACTIVE_SVG_PATTERNS`)

## Acceptance Criteria
- [ ] `<animate attributeName="href" to="javascript:alert(1)"/>` rejected
- [ ] `<set attributeName="href" to="javascript:..."/>` rejected
- [ ] `<animateTransform>` and `<animateMotion>` rejected
- [ ] Regression test added

## Work Log
_(empty)_
