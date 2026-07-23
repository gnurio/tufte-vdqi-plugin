"""Shared helpers for the render-* scripts.

Centralises the escaping policy applied to user/data-controlled text that
flows into SVG <text> nodes.
"""
import math
from html import escape


def svg_text(value: object) -> str:
    """Escape an arbitrary value for safe inclusion inside an SVG <text> node.

    Coerces None and non-strings via str() so callers (notebooks, pipelines)
    don't crash on optional/numeric labels.
    """
    return escape("" if value is None else str(value), quote=True)


def require_numeric(values, what: str) -> None:
    """Raise ValueError unless every value is a finite real number (bool excluded).

    json.loads accepts bare NaN/Infinity by default; those pass isinstance(v,
    float) but break min/max/scaling downstream, so they're rejected here too.
    """
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"{what} must be finite numbers, got {v!r}")
