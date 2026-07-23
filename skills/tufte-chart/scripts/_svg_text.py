"""Shared helpers for the render-* scripts.

Centralises the escaping policy applied to user/data-controlled text that
flows into SVG <text> nodes.
"""
from html import escape


def svg_text(value: object) -> str:
    """Escape an arbitrary value for safe inclusion inside an SVG <text> node.

    Coerces None and non-strings via str() so callers (notebooks, pipelines)
    don't crash on optional/numeric labels.
    """
    return escape("" if value is None else str(value), quote=True)


def require_numeric(values, what: str) -> None:
    """Raise ValueError unless every value is a real number (bool excluded)."""
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"{what} must be numbers, got {v!r}")
