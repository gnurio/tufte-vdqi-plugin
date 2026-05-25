#!/usr/bin/env python3
"""
Regression tests for the SVG/HTML injection fix.

Codex Security Review flagged that the renderer scripts were interpolating
user-controlled text (titles, subtitles, series, facet/group names) directly
into SVG <text> nodes without escaping, letting a crafted label break out
of <text> and inject markup. These tests render each chart with an injection
payload as the label and assert the payload survives as escaped text, not
as live markup.

Run from the repo root:
    python -m unittest skills.render-tufte-chart.tests.test_text_escaping
or directly:
    python skills/render-tufte-chart/tests/test_text_escaping.py
"""
import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
# Put scripts dir on sys.path so renderer modules can `from _svg_text import ...`
# when loaded via spec_from_file_location below.
sys.path.insert(0, str(SCRIPTS_DIR))


def _load(name: str):
    """Load a script module by file path (the scripts dir is not a package)."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


render_line_svg = _load("render_line_svg")
small_multiples = _load("small_multiples")
quartile_plot = _load("quartile_plot")
range_frame = _load("range_frame")
wrap_html = _load("wrap_html")

PAYLOAD = '</text><script>alert(1)</script><text>'
ESCAPED_OPEN_TAG = "&lt;script&gt;"
ESCAPED_CLOSE_TEXT = "&lt;/text&gt;"
TRUSTED_MARKER = "<!-- tufte-vdqi: trusted -->"


def _assert_no_injection(test: unittest.TestCase, svg: str) -> None:
    test.assertNotIn("<script>", svg)
    test.assertNotIn("</text><script", svg)
    test.assertIn(ESCAPED_OPEN_TAG, svg)
    test.assertIn(ESCAPED_CLOSE_TEXT, svg)


class LineSvgTests(unittest.TestCase):
    DATA = [{"x": 1, "y": 2}, {"x": 2, "y": 3}]

    def test_title_is_escaped(self):
        svg = render_line_svg.render(self.DATA, title=PAYLOAD, series="Revenue")
        _assert_no_injection(self, svg)

    def test_subtitle_is_escaped(self):
        svg = render_line_svg.render(self.DATA, title="t", subtitle=PAYLOAD)
        _assert_no_injection(self, svg)

    def test_series_is_escaped(self):
        svg = render_line_svg.render(self.DATA, title="t", series=PAYLOAD)
        _assert_no_injection(self, svg)


class SmallMultiplesTests(unittest.TestCase):
    def _data(self, facet):
        return [
            {"facet": facet, "x": 1, "y": 1},
            {"facet": facet, "x": 2, "y": 2},
        ]

    def test_title_is_escaped(self):
        svg = small_multiples.render(
            self._data("NA"), "facet", "x", "y", PAYLOAD, "", 2, None, 820)
        _assert_no_injection(self, svg)

    def test_subtitle_is_escaped(self):
        svg = small_multiples.render(
            self._data("NA"), "facet", "x", "y", "t", PAYLOAD, 2, None, 820)
        _assert_no_injection(self, svg)

    def test_facet_name_is_escaped(self):
        svg = small_multiples.render(
            self._data(PAYLOAD), "facet", "x", "y", "t", "", 2, None, 820)
        _assert_no_injection(self, svg)


class QuartilePlotTests(unittest.TestCase):
    VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_title_is_escaped(self):
        svg = quartile_plot.render({"A": self.VALUES}, PAYLOAD, "", 720)
        _assert_no_injection(self, svg)

    def test_subtitle_is_escaped(self):
        svg = quartile_plot.render({"A": self.VALUES}, "t", PAYLOAD, 720)
        _assert_no_injection(self, svg)

    def test_group_name_is_escaped(self):
        svg = quartile_plot.render({PAYLOAD: self.VALUES}, "t", "", 720)
        _assert_no_injection(self, svg)


class RangeFrameTests(unittest.TestCase):
    DATA = [{"x": 1.0, "y": 2.0}, {"x": 2.0, "y": 3.0}]

    def test_title_is_escaped(self):
        svg = range_frame.render(self.DATA, title=PAYLOAD, subtitle="",
                                 marginal_dash=False, width=720, height=480)
        _assert_no_injection(self, svg)

    def test_subtitle_is_escaped(self):
        svg = range_frame.render(self.DATA, title="t", subtitle=PAYLOAD,
                                 marginal_dash=False, width=720, height=480)
        _assert_no_injection(self, svg)


class RendererProvenanceTests(unittest.TestCase):
    """Every trusted renderer must stamp the tufte-vdqi marker so wrap_html
    can distinguish its own output from arbitrary third-party SVG."""

    def test_line_svg_emits_marker(self):
        svg = render_line_svg.render(
            [{"x": 1, "y": 2}, {"x": 2, "y": 3}], title="t")
        self.assertIn(TRUSTED_MARKER, svg)

    def test_small_multiples_emits_marker(self):
        svg = small_multiples.render(
            [{"facet": "A", "x": 1, "y": 1}, {"facet": "A", "x": 2, "y": 2}],
            "facet", "x", "y", "t", "", 2, None, 820)
        self.assertIn(TRUSTED_MARKER, svg)

    def test_quartile_plot_emits_marker(self):
        svg = quartile_plot.render({"A": [1, 2, 3, 4, 5]}, "t", "", 720)
        self.assertIn(TRUSTED_MARKER, svg)

    def test_range_frame_emits_marker(self):
        svg = range_frame.render(
            [{"x": 1.0, "y": 2.0}, {"x": 2.0, "y": 3.0}],
            title="t", subtitle="", marginal_dash=False, width=720, height=480)
        self.assertIn(TRUSTED_MARKER, svg)


class RendererNoneToleranceTests(unittest.TestCase):
    """render() must not crash on None/numeric title-like inputs; CLI callers
    are safe via argparse defaults but library callers (notebooks, pipelines)
    used to pass None and got the literal string 'None'."""

    def test_line_svg_none_title(self):
        render_line_svg.render(
            [{"x": 1, "y": 2}, {"x": 2, "y": 3}], title=None)

    def test_line_svg_numeric_title(self):
        svg = render_line_svg.render(
            [{"x": 1, "y": 2}, {"x": 2, "y": 3}], title=2024)
        self.assertIn(">2024<", svg)

    def test_range_frame_none_title(self):
        range_frame.render(
            [{"x": 1.0, "y": 2.0}, {"x": 2.0, "y": 3.0}],
            title=None, subtitle="", marginal_dash=False, width=720, height=480)

    def test_quartile_plot_none_title(self):
        quartile_plot.render({"A": [1, 2, 3, 4, 5]}, None, "", 720)

    def test_small_multiples_none_title(self):
        small_multiples.render(
            [{"facet": "A", "x": 1, "y": 1}, {"facet": "A", "x": 2, "y": 2}],
            "facet", "x", "y", None, None, 2, None, 820)


class WrapHtmlActiveContentTests(unittest.TestCase):
    """wrap_html.py must reject SVGs that carry executable content."""

    BENIGN_SVG = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
        '<rect width="10" height="10" fill="white"/></svg>'
    )

    def test_accepts_benign_svg(self):
        wrap_html.reject_active_svg(self.BENIGN_SVG)  # should not raise

    def test_rejects_script_element(self):
        svg = self.BENIGN_SVG.replace("</svg>", "<script>alert(1)</script></svg>")
        with self.assertRaisesRegex(ValueError, "script"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_foreign_object(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<foreignObject><div xmlns="http://www.w3.org/1999/xhtml"/></foreignObject></svg>')
        with self.assertRaisesRegex(ValueError, "foreignObject"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_event_handler_attribute(self):
        svg = self.BENIGN_SVG.replace("<rect", '<rect onload="alert(1)"')
        with self.assertRaisesRegex(ValueError, "event-handler"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_javascript_url(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<a href="javascript:alert(1)"><text>x</text></a></svg>')
        with self.assertRaisesRegex(ValueError, "javascript"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_xlink_javascript_url(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<a xlink:href="javascript:alert(1)"><text>x</text></a></svg>')
        with self.assertRaisesRegex(ValueError, "javascript"):
            wrap_html.reject_active_svg(svg)

    # --- regression coverage for the issues found in /compound-engineering:ce-review ---

    def test_rejects_namespaced_script(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", "<svg:script>alert(1)</svg:script></svg>")
        with self.assertRaisesRegex(ValueError, "script"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_namespaced_foreign_object(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>",
            '<svg:foreignObject><div xmlns="http://www.w3.org/1999/xhtml"/></svg:foreignObject></svg>')
        with self.assertRaisesRegex(ValueError, "foreignObject"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_smil_animate(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>",
            '<a><animate attributeName="href" to="javascript:alert(1)" begin="0s"/>'
            '<text>x</text></a></svg>')
        with self.assertRaisesRegex(ValueError, "SMIL"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_smil_set(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>",
            '<a><set attributeName="href" to="javascript:alert(1)"/><text>x</text></a></svg>')
        with self.assertRaisesRegex(ValueError, "SMIL"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_use_data_uri(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<use href="data:image/svg+xml;base64,PHN2Zz48L3N2Zz4="/></svg>')
        with self.assertRaisesRegex(ValueError, "use.*image"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_image_external_https(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<image href="https://attacker.example/track.png"/></svg>')
        with self.assertRaisesRegex(ValueError, "use.*image"):
            wrap_html.reject_active_svg(svg)

    def test_rejects_use_relative_path(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<use href="./payload.svg#x"/></svg>')
        with self.assertRaisesRegex(ValueError, "use.*image"):
            wrap_html.reject_active_svg(svg)

    def test_accepts_use_same_doc_fragment(self):
        svg = self.BENIGN_SVG.replace(
            "</svg>", '<defs><g id="x"><rect/></g></defs><use href="#x"/></svg>')
        wrap_html.reject_active_svg(svg)  # should not raise


class BuildHtmlGuardTests(unittest.TestCase):
    """build_html() must invoke reject_active_svg on untrusted SVGs so library
    callers (not just the CLI main) can't bypass the active-content check."""

    def test_build_html_rejects_untrusted_with_script(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        with self.assertRaisesRegex(ValueError, "script"):
            wrap_html.build_html("t", "", svg, "c", "x.css")

    def test_build_html_accepts_trusted_svg(self):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg">{TRUSTED_MARKER}'
               '<rect width="10" height="10" fill="white"/></svg>')
        html = wrap_html.build_html("t", "", svg, "c", "x.css")
        self.assertIn("<rect", html)

    def test_build_html_accepts_untrusted_benign_svg(self):
        # Benign untrusted SVG (no marker, no active content) — build_html
        # runs the rejector but it does not raise.
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"/></svg>'
        html = wrap_html.build_html("t", "", svg, "c", "x.css")
        self.assertIn("<rect", html)


class TrustMarkerTests(unittest.TestCase):
    def test_is_trusted_detects_marker(self):
        self.assertTrue(wrap_html.is_trusted(f"<svg>{TRUSTED_MARKER}</svg>"))

    def test_is_trusted_rejects_missing_marker(self):
        self.assertFalse(wrap_html.is_trusted("<svg></svg>"))


if __name__ == "__main__":
    unittest.main()
