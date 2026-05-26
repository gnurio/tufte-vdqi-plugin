"""Shared helpers for the render-* scripts.

Centralises the escaping policy applied to user/data-controlled text that
flows into SVG <text> nodes, and the in-memory provenance type the renderers
return so wrap_html.py can distinguish renderer output from file-loaded SVG.
"""
from html import escape

TRUSTED_MARKER = "<!-- tufte-vdqi: trusted -->"


class TrustedSVG(str):
    """In-memory SVG produced by this package's renderer functions."""


def trusted_svg(svg: str) -> TrustedSVG:
    """Mark renderer-produced SVG as trusted without relying on file contents."""
    return TrustedSVG(svg)


def svg_text(value: object) -> str:
    """Escape an arbitrary value for safe inclusion inside an SVG <text> node.

    Coerces None and non-strings via str() so callers (notebooks, pipelines)
    don't crash on optional/numeric labels.
    """
    return escape("" if value is None else str(value), quote=True)
