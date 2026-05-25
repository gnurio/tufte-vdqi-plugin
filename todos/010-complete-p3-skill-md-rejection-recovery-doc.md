---
status: pending
priority: p3
issue_id: "010"
tags: [code-review, docs, agent-native]
dependencies: []
---

# SKILL.md needs a recovery paragraph for wrap_html.py rejection error

## Problem Statement
When `wrap_html.py` rejects an SVG (active content), the agent receives `ERROR: SVG contains <...>; refusing to wrap...`. The current `skills/render-tufte-chart/SKILL.md` "Optional: Tufte-styled HTML page" section doesn't tell the agent what to do next. Agents that wrap a hand-built SVG (a path explicitly endorsed in lines 130-135) will hit the guard and may not know to regenerate from a trusted renderer.

## Findings
- **agent-native-reviewer**: P3 — agent/human parity gap; one-paragraph doc fix

## Proposed Solutions

### Option A — Add recovery paragraph + B8 checklist item (Recommended)
In `SKILL.md` "Optional: Tufte-styled HTML page" section:
> If `wrap_html.py` exits with `ERROR: SVG contains <...>; refusing to wrap`, the SVG you produced contains script-bearing constructs. Either remove them, or regenerate the SVG using one of the trusted renderers above (`render_line_svg.py`, `small_multiples.py`, `quartile_plot.py`, `range_frame.py`), which never emit active content.

Add to Build checklist:
> **B8. Inert SVG.** No `<script>`, no event-handler attributes, no `javascript:` URLs, no `<foreignObject>` — `wrap_html.py` will refuse to wrap them.

## Recommended Action
Option A.

## Technical Details
- File: `skills/render-tufte-chart/SKILL.md` (lines 137-156 area, plus build checklist)

## Acceptance Criteria
- [ ] Recovery paragraph added to HTML wrapper section
- [ ] B8 inert-SVG item added to build checklist

## Work Log
_(empty)_
