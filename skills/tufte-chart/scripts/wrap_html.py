#!/usr/bin/env python3
"""
Wrap a Tufte-style SVG in an HTML page that uses tufte-css typography
(ET Book font, generous margins, optional margin notes).

Inputs an existing .svg file (typically produced by render_line_svg.py or
written by hand following the build checklist). Outputs an .html page that
inlines the SVG inside an <article>/<figure class="fullwidth"> and links to
the vendored tufte.css next to it. Copies tufte.css + the et-book/ fonts into
a sibling `tufte-assets/` directory the first time so the page renders
correctly when opened locally with no network.

Every SVG is inspected before inlining: anything script-bearing (<script>,
event handlers, SMIL animation, external hrefs, javascript: URLs) is refused
with ERROR[active-svg]. The fix is to produce inert SVG — the four local
renderers always do.

Usage:
  python3 wrap_html.py \
    --svg chart.svg --out chart.html \
    --title "Revenue (real 2023 USD, M)" \
    --caption "Inflation-adjusted using BLS CPI-U." \
    [--intro "Optional lede paragraph above the figure."]

Add `--no-assets` to skip the asset copy (use when the page is being served
from a site that already publishes tufte.css at the expected path).
"""
import argparse, re, shutil, sys
from html import escape, unescape
from pathlib import Path

# Patterns for SVG features that execute script or load external content.
# wrap_html.py emits an HTML page that browsers will parse, so any of these
# in an inlined SVG would run in the page's origin. Every SVG goes through
# this check, no exceptions.
# ponytail: regex rejector, not a parser — a full XML parser would also catch
# active tags outside this denylist sandwiched between two <svg>...</svg>
# blocks; swap to one if this ever routinely wraps hostile third-party SVG.
_NS_PREFIX = r"(?:[A-Za-z][\w.-]*:)?"

# Known browser-recognized event-handler attribute names (HTML DOM + SVG +
# SMIL). Matching only these — not an open "on[a-zA-Z]+" — avoids false
# positives on ordinary chart text that happens to start with "on" (e.g. a
# title reading "Online = 87%"), since an unrecognized on*= attribute name
# never executes in a browser regardless of spelling.
_EVENT_HANDLER_NAMES = (
    "abort activate afterprint animationcancel animationend animationiteration "
    "animationstart auxclick beforecopy beforecut beforeinput beforepaste "
    "beforeprint beforeunload begin blur cancel canplay canplaythrough change "
    "click close contextmenu copy cuechange cut dblclick drag dragend "
    "dragenter dragleave dragover dragstart drop durationchange emptied end "
    "ended error focus focusin focusout formdata fullscreenchange "
    "fullscreenerror gotpointercapture hashchange input invalid keydown "
    "keypress keyup load loadeddata loadedmetadata loadstart "
    "lostpointercapture message mousedown mouseenter mouseleave mousemove "
    "mouseout mouseover mouseup mousewheel offline online open pagehide "
    "pageshow paste pause play playing pointercancel pointerdown "
    "pointerenter pointerleave pointermove pointerout pointerover pointerup "
    "popstate progress ratechange repeat reset resize scroll scrollend "
    "securitypolicyviolation seeked seeking select selectionchange "
    "selectstart slotchange stalled storage submit suspend timeupdate "
    "toggle touchcancel touchend touchmove touchstart transitioncancel "
    "transitionend transitionrun transitionstart unhandledrejection unload "
    "volumechange waiting webkitanimationend webkitanimationiteration "
    "webkitanimationstart webkittransitionend wheel"
).split()

# URL-bearing attributes checked for a javascript: value below — href /
# xlink:href (also checked separately for <use>/<image>, more strictly),
# plus the HTML equivalents an embedded-but-not-actually-SVG tag could use.
# Matched only when the value is actually "javascript:" (see the pattern
# below), not on bare presence — "background" and "data" are ordinary
# English words a chart title could legitimately contain.
_URL_ATTRS = r"(?:href|xlink:href|src|data|action|formaction|poster|background)"

_ACTIVE_SVG_PATTERNS = [
    (re.compile(r"<!DOCTYPE", re.IGNORECASE),
     "<!DOCTYPE declaration (possible XXE/entity injection)"),
    (re.compile(rf"<\s*{_NS_PREFIX}script\b", re.IGNORECASE),
     "<script> element"),
    (re.compile(rf"<\s*{_NS_PREFIX}foreignObject\b", re.IGNORECASE),
     "<foreignObject> element"),
    # HTML embedding/active-content tags: not valid SVG, but wrap_html
    # inlines the raw string into an HTML page without validating SVG-ness,
    # so a "chart.svg" containing one of these renders as live HTML anyway.
    (re.compile(r"<\s*(?:iframe|embed|object|img|meta|link|base|style)\b", re.IGNORECASE),
     "HTML embedding/active-content element (iframe/embed/object/img/meta/link/base/style)"),
    (re.compile(rf"<\s*{_NS_PREFIX}(?:animate(?:Transform|Motion)?|set)\b",
                re.IGNORECASE),
     "SMIL animation element (<animate>/<set>)"),
    # <use>/<image> with anything other than a same-document #fragment href.
    # Catches data:, http(s):, file:, ftp:, relative paths — all of which
    # reach out beyond the wrapped document. The negative lookahead has to
    # see through the optional quote so `href="#x"` stays accepted.
    (re.compile(rf"<\s*{_NS_PREFIX}(?:use|image)\b[^>]*?\b(?:xlink:)?href\s*=(?!\s*['\"]?\s*#)",
                re.IGNORECASE),
     "<use>/<image> with non-fragment href"),
    (re.compile(r"\bon(?:" + "|".join(_EVENT_HANDLER_NAMES) + r")\s*=", re.IGNORECASE),
     "event-handler attribute (on*=)"),
]

# Checked separately (see reject_active_svg): a real attribute value only
# ever exists in raw markup between a LITERAL quote character right after
# "attr=" — svg_text() escapes every quote character, so this can never be
# satisfied by legitimately-escaped chart text no matter what words the
# text contains (a title reading 'the URL was href="javascript:..."' is
# stored as the harmless text 'href=&quot;javascript:...&quot;', which has
# no literal quote next to "href="). Only the captured value between real
# quotes is then decoded and normalized to catch java&#9;script:-style
# obfuscation, since a browser applies both normalizations to an
# attribute's VALUE before parsing its URL scheme.
_URL_ATTR_VALUE_PATTERN = re.compile(
    rf"\b{_URL_ATTRS}\s*=\s*(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)

# Unquoted form (<a href=javascript:...>, no quotes at all) is valid HTML
# the pattern above won't catch. Requiring the match to sit inside an open
# "<...>" tag span (nothing but non-">" chars since the last "<") keeps it
# from firing on escaped chart text: svg_text() escapes literal "<", so
# prose mentioning "href=javascript:..." inside a <text> element is always
# preceded by the ">" that closed the enclosing tag, never a "<".
_UNQUOTED_URL_ATTR_VALUE_PATTERN = re.compile(
    rf"<[^>]*?\b{_URL_ATTRS}\s*=\s*(?!['\"])([^\s>/]+)", re.IGNORECASE)
_JAVASCRIPT_SCHEME_PATTERN = re.compile(r"^\s*javascript:", re.IGNORECASE)


def _strip_url_whitespace(s: str) -> str:
    """Remove TAB/LF/CR — browsers strip these from URLs before parsing the
    scheme, so "java&#9;script:" decodes to "java<TAB>script:", which still
    executes even though it isn't the contiguous string "javascript:"."""
    return s.translate({0x09: None, 0x0A: None, 0x0D: None})


def _refuse(label: str) -> None:
    raise ValueError(
        f"SVG contains {label}; refusing to wrap. "
        "Produce inert SVG — the local renderers (render_line_svg.py, "
        "small_multiples.py, quartile_plot.py, range_frame.py) always do."
    )


def reject_active_svg(svg: str) -> None:
    """Raise ValueError if the SVG contains script-bearing constructs.

    Tag/attribute-name/DOCTYPE patterns are checked against the raw text
    only. Real URL-attribute values (quoted or unquoted) are additionally
    checked with HTML entities decoded and TAB/LF/CR stripped, to catch
    java&#9;script:-style scheme obfuscation — see _URL_ATTR_VALUE_PATTERN's
    comment for why this stays scoped to real attribute values only.
    """
    for pattern, label in _ACTIVE_SVG_PATTERNS:
        if pattern.search(svg):
            _refuse(label)

    for match in _URL_ATTR_VALUE_PATTERN.finditer(svg):
        raw_value = match.group(2)
        candidates = {raw_value, unescape(raw_value)}
        candidates |= {_strip_url_whitespace(c) for c in list(candidates)}
        if any(_JAVASCRIPT_SCHEME_PATTERN.search(c) for c in candidates):
            _refuse("javascript: URL")

    for match in _UNQUOTED_URL_ATTR_VALUE_PATTERN.finditer(svg):
        raw_value = match.group(1)
        candidates = {raw_value, unescape(raw_value)}
        candidates |= {_strip_url_whitespace(c) for c in list(candidates)}
        if any(_JAVASCRIPT_SCHEME_PATTERN.search(c) for c in candidates):
            _refuse("javascript: URL (unquoted attribute)")

    # Check against the prolog-stripped text: a leading <?xml?> declaration
    # (which strip_xml_decl removes before inlining) is benign and must not
    # count as "content before the <svg> root".
    trimmed = strip_xml_decl(svg).strip()
    if not (re.match(rf"<{_NS_PREFIX}svg\b", trimmed, re.IGNORECASE)
            and re.search(r"</svg\s*>\s*\Z", trimmed, re.IGNORECASE)):
        raise ValueError(
            "SVG must be a single <svg>...</svg> document with nothing before "
            "or after it; refusing to wrap. Produce inert SVG — the local "
            "renderers (render_line_svg.py, small_multiples.py, quartile_plot.py, "
            "range_frame.py) always do."
        )


SCRIPT_DIR = Path(__file__).resolve().parent
VENDORED_CSS_DIR = SCRIPT_DIR.parent / "assets" / "tufte-css"
ASSETS_SUBDIR = "tufte-assets"


def ensure_assets(out_html: Path) -> str:
    """Copy tufte.css and et-book/ next to the output HTML if missing. Returns
    the relative href to use in the <link> tag."""
    dest = out_html.parent / ASSETS_SUBDIR
    dest.mkdir(parents=True, exist_ok=True)
    css_src = VENDORED_CSS_DIR / "tufte.css"
    fonts_src = VENDORED_CSS_DIR / "et-book"
    if not css_src.exists() or not fonts_src.exists():
        raise FileNotFoundError(
            f"Vendored tufte-css not found at {VENDORED_CSS_DIR}. "
            "The skill ships these assets — reinstall the plugin or restore them.")
    css_dest = dest / "tufte.css"
    if not css_dest.exists():
        shutil.copy2(css_src, css_dest)
    fonts_dest = dest / "et-book"
    if not fonts_dest.exists():
        shutil.copytree(fonts_src, fonts_dest)
    return f"{ASSETS_SUBDIR}/tufte.css"


def strip_xml_decl(svg: str) -> str:
    """Inlined SVG must not carry a <?xml ...?> processing instruction."""
    s = svg.lstrip()
    if s.startswith("<?xml"):
        end = s.find("?>")
        if end != -1:
            s = s[end + 2:].lstrip()
    return s


def build_html(title: str, intro: str, svg: str, caption: str, css_href: str) -> str:
    # The check lives here (not only in main) so library callers can't
    # bypass it.
    reject_active_svg(svg)
    intro_html = f'<p>{escape(intro)}</p>' if intro else ""
    caption_html = f'<figcaption>{escape(caption)}</figcaption>' if caption else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title) if title else 'Tufte chart'}</title>
<link rel="stylesheet" href="{escape(css_href)}">
<style>
  /* let the chart breathe inside tufte-css's narrow column */
  figure.fullwidth svg {{ display: block; width: 100%; height: auto; }}
</style>
</head>
<body>
<article>
{f'<h1>{escape(title)}</h1>' if title else ''}
{intro_html}
<figure class="fullwidth">
{svg}
{caption_html}
</figure>
</article>
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--svg", required=True, help="path to the SVG to wrap")
    p.add_argument("--out", required=True, help="path to write the .html file")
    p.add_argument("--title", default="", help="page title and <h1>")
    p.add_argument("--caption", default="", help="figcaption text under the chart")
    p.add_argument("--intro", default="", help="optional lede paragraph above the figure")
    p.add_argument("--no-assets", action="store_true",
                   help="skip copying tufte.css and et-book/ next to the output")
    a = p.parse_args()

    try:
        svg_text_content = Path(a.svg).read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR[svg-read]: cannot read SVG {a.svg}: {e}", file=sys.stderr)
        sys.exit(1)

    # Fail fast, before any disk writes: reject script-bearing SVG up front
    # rather than after copying assets and creating the output directory.
    try:
        reject_active_svg(svg_text_content)
    except ValueError as e:
        print(f"ERROR[active-svg]: {e}", file=sys.stderr)
        sys.exit(1)

    out_html = Path(a.out)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    try:
        css_href = (f"{ASSETS_SUBDIR}/tufte.css" if a.no_assets
                    else ensure_assets(out_html))
    except (OSError, FileNotFoundError) as e:
        print(f"ERROR[missing-assets]: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        html = build_html(a.title, a.intro, strip_xml_decl(svg_text_content),
                          a.caption, css_href)
    except ValueError as e:
        print(f"ERROR[active-svg]: {e}", file=sys.stderr)
        sys.exit(1)

    out_html.write_text(html, encoding="utf-8")
    print(f"wrote {out_html} ({len(html)} bytes)")
    if not a.no_assets:
        print(f"assets at {out_html.parent / ASSETS_SUBDIR}/  (open the HTML in any browser)")


if __name__ == "__main__":
    main()
