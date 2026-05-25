---
status: pending
priority: p2
issue_id: "005"
tags: [code-review, security]
dependencies: []
---

# <use href="data:..."/> and <image href="https://..."/> not blocked

## Problem Statement
The `<use>` external-href pattern requires `(?:https?:)?//`, missing:
- `<use href="data:image/svg+xml;base64,...">` — Firefox has historically executed scripts in `data:` SVG fragments loaded via `<use>`; even when blocked, `data:` is a known active-content sink.
- `<image href="https://attacker/track.png"/>` — silent third-party HTTP request; tracking pixel / IP leakage when the wrapped HTML is shared and opened.

Empirically verified MISS for both.

## Findings
- **security-sentinel**: P2 — both confirmed
- **prior /code-review (Findings 4, 10)**: same
- **simplicity-reviewer**: argued for *removing* the `<use>` pattern entirely as speculative — but security audit confirms it's needed for hand-authored / third-party SVGs in the threat model.

## Proposed Solutions

### Option A — Broaden to "non-fragment href on <use>/<image>" (Recommended)
Replace narrow `(?:https?:)?//` check with a pattern that rejects any `<use>`/`<image>` whose `href`/`xlink:href` is not `#fragment`.
- Pros: Catches data:, file:, ftp:, bare paths, and external in one shot.
- Cons: Rejects legitimate same-origin `<use href="./icons.svg#foo">` references — but the threat model assumes single-file inlining, so this is acceptable.
- Effort: Small (1 pattern replacement)
- Risk: Low

### Option B — Enumerate blocked schemes
Add separate patterns for `data:`, `file:`, `ftp:`, `https?:`, `//` on `<use>` and `<image>`.
- Pros: Explicit allowlist.
- Cons: Pattern proliferation; misses new schemes.
- Effort: Small
- Risk: Medium

## Recommended Action
Option A.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:32-33` (current `<use>` pattern)

## Acceptance Criteria
- [ ] `<use href="data:..."/>` rejected
- [ ] `<image href="https://..."/>` rejected
- [ ] `<image xlink:href="..."/>` rejected
- [ ] `<use href="#fragment"/>` accepted (same-document reference)
- [ ] Regression tests added

## Work Log
_(empty)_
