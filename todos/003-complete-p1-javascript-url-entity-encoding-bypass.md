---
status: pending
priority: p1
issue_id: "003"
tags: [code-review, security, xss]
dependencies: []
---

# javascript: URL detection bypassed by HTML entity encoding

## Problem Statement
The `javascript:` URL pattern is a byte-literal regex on raw SVG text. Browsers decode HTML entities in `href`/`xlink:href` attribute values **before** URL parsing. So `<a href="&#106;avascript:alert(1)">` does not match `javascript:` in the raw text but the browser sees `javascript:alert(1)` and executes it on click. Same applies to whitespace-in-scheme like `<a href="java&#9;script:alert(1)">` — the URL parser strips control chars before matching the scheme.

This is the fundamental limitation of regex-based sanitization the wrap_html.py docstring already acknowledges.

## Findings
- **security-sentinel**: P2 — recommends decode-then-check or real parser.
- **prior /code-review (Finding 2)**: confirmed via regex test.

Empirical:
```
MISS [[]] entity encoded js URL: <a href="&#106;avascript:alert(1)">
MISS [[]] tab in scheme name (encoded): <a href="java&#9;script:alert(1)">
```

## Proposed Solutions

### Option A — Provenance-tagged trusted SVGs (Recommended)
Have each renderer emit a `<!-- tufte-vdqi: trusted -->` marker as the first child of `<svg>`. wrap_html accepts tagged SVGs by default; require `--untrusted` flag to run the (acknowledged best-effort) `reject_active_svg`. Matches the original Codex spec's "only accept SVGs produced by the trusted local renderers" option.
- Pros: Matches the plugin's scope (chart rendering, not general SVG sanitizer); no new deps; turns the regex into an explicit fallback.
- Cons: Users wrapping third-party SVGs need to know to pass `--untrusted` (or `--trusted` if we invert).
- Effort: Small (marker emit in 4 renderers + flag in wrap_html)
- Risk: Low

### Option B — Decode entities then re-check
Use `html.unescape()` on attribute values before checking against `javascript:`.
- Pros: Targeted fix for this specific bypass.
- Cons: Need to identify attribute values first (still a parsing problem); other encodings (UTF-7, etc.) still bypass; arms race continues.
- Effort: Medium
- Risk: High (regex-with-decode is still leaky)

### Option C — Use a real HTML/SVG sanitizer
Adopt `nh3` (Rust-backed) or `bleach` with an SVG allowlist.
- Pros: Closes whole classes of bypass.
- Cons: New runtime dependency; learning-curve on allowlist tuning.
- Effort: Medium
- Risk: Low for correctness, medium for dependency/maintenance overhead.

## Recommended Action
Option A — provenance-tag trusted SVGs.

## Technical Details
- File: `skills/render-tufte-chart/scripts/wrap_html.py:37` (javascript: URL pattern)
- File: All 4 renderers — emit `<!-- tufte-vdqi: trusted -->` as first child of `<svg>`

## Acceptance Criteria
- [ ] All 4 renderers emit the trusted-provenance marker
- [ ] wrap_html accepts trusted-tagged SVGs without running reject_active_svg
- [ ] wrap_html with `--untrusted` flag runs reject_active_svg on untagged input
- [ ] Untagged input without `--untrusted` flag is rejected with a clear error
- [ ] Documentation updated in SKILL.md (see [[skill-md-rejection-recovery-doc]])

## Work Log
_(empty)_
