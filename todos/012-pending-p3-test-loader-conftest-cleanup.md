---
status: pending
priority: p3
issue_id: "012"
tags: [code-review, quality, tests]
dependencies: []
---

# Test loader uses importlib hack; switch to conftest.py + sys.path

## Problem Statement
`tests/test_text_escaping.py` loads each renderer module via `importlib.util.spec_from_file_location` because `scripts/` is not a package and the parent dir `tufte-chart` has a hyphen (not a valid Python identifier). It works but is verbose and will be repeated in every new test file.

## Findings
- **kieran-python-reviewer**: P2 — suggests `conftest.py` with `sys.path.insert(0, str(SCRIPTS_DIR))` so tests can use plain `import render_line_svg`
- **simplicity-reviewer**: agrees `importlib` is the "minimum viable loader" given the hyphenated parent dir, but conftest.py path-insert is cleaner

## Proposed Solutions

### Option A — conftest.py + sys.path (Recommended)
Add `skills/tufte-chart/tests/conftest.py`:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
```
Then tests use `import render_line_svg, small_multiples, ...` directly.
- Pros: Idiomatic pytest; shrinks each test file; new test files just import.
- Cons: Mutates sys.path (scoped to test runs only).
- Effort: Small
- Risk: Low

### Option B — Leave as-is
Keep the importlib loader; document the hyphen-dir constraint.
- Effort: None
- Risk: Drift if more test files appear

## Recommended Action
Option A — do when adding the next test file (e.g., for [[009]]).

## Technical Details
- New file: `skills/tufte-chart/tests/conftest.py`
- Refactor: `skills/tufte-chart/tests/test_text_escaping.py:18-34` (remove `_load` helper)

## Acceptance Criteria
- [ ] `conftest.py` exists and prepends scripts dir to sys.path
- [ ] `_load()` helper removed
- [ ] Tests import modules with `import <name>` and pass

## Work Log
_(empty)_
