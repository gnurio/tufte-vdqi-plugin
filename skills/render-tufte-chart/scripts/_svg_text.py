"""Shared helpers for the render-* scripts.

Centralises the escaping policy applied to user/data-controlled text that
flows into SVG <text> nodes, and the provenance marker the renderers emit so
wrap_html.py can tell trusted output from arbitrary third-party SVG.
"""
from html import escape

TRUSTED_MARKER = "<!-- tufte-vdqi: trusted -->"


def svg_text(value: object) -> str:
    """Escape an arbitrary value for safe inclusion inside an SVG <text> node.

    Coerces None and non-strings via str() so callers (notebooks, pipelines)
    don't crash on optional/numeric labels.
    """
    return escape("" if value is None else str(value), quote=True)
