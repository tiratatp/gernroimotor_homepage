"""Structural tests for template.html and style.css.

Guards:
  * visible FAQ Q&A pairs in <section id="faq"> stay in lockstep with the
    FAQPage JSON-LD mainEntity.
  * the header call anchor exposes a persistent accessible name, because on
    mobile only the icon is rendered (.call-text { display:none }).
  * style.css defines a sticky-anchor offset, so in-page anchors do not land
    beneath the sticky header.
  * template.html carries no inline style="..." attributes — all styling
    lives in style.css.
  * every images/... path referenced by template.html or style.css exists.
  * the hero Google Maps link matches the JSON-LD hasMap URL and its
    destination coordinates match the JSON-LD geo coordinates.

All contracts must pass before deployment.
"""

from __future__ import annotations

import html.parser
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template.html"
STYLESHEET_PATH = REPO_ROOT / "style.css"

_WHITESPACE_RE = re.compile(r"\s+")
_HEADER_CALL_RE = re.compile(r'<a\b[^>]*class="header-call"[^>]*>', re.DOTALL)
_ATTR_RE = re.compile(r'''([\w-]+)\s*=\s*"([^"]*)"''')
_DECL_NAME_RE = re.compile(r"([\w-]+)\s*:")
_INLINE_STYLE_RE = re.compile(r"\sstyle\s*=\s*[\"']")
_IMAGE_REF_RE = re.compile(r"images/[A-Za-z0-9._-]+")
_HERO_MAPS_HREF_RE = re.compile(r'href="(https://www\.google\.com/maps/dir/[^"]+)"')
_DESTINATION_RE = re.compile(r"destination=([^&]+)")


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


class _FaqVisitor(html.parser.HTMLParser):
    """Walk the visible FAQ and collect (question, answer) pairs from
    <div class="faq-item"><h3>...</h3><p>...</p></div> blocks.

    Tracks nesting depth so an inner <div> inside a <p> does not close the
    outer faq-item prematurely.
    """

    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[str, str]] = []
        self._depth = 0  # nesting depth of <div> inside a faq-item
        self._buf: dict[str, str] = {"q": "", "a": ""}
        self._capture: str | None = None
        self._q_set = False
        self._a_set = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        if self._depth == 0 and tag == "div" and "faq-item" in classes:
            self._depth = 1
            self._buf = {"q": "", "a": ""}
            self._capture = None
            self._q_set = False
            self._a_set = False
            return
        if self._depth > 0:
            if tag == "div":
                self._depth += 1
            if tag == "h3" and not self._q_set:
                self._capture = "q"
            elif tag == "p" and not self._a_set:
                self._capture = "a"

    def handle_endtag(self, tag: str) -> None:
        if self._depth == 0:
            return
        if self._capture == "q" and tag == "h3":
            self._capture = None
            self._q_set = True
        elif self._capture == "a" and tag == "p":
            self._capture = None
            self._a_set = True
        if tag == "div":
            self._depth -= 1
            if self._depth == 0 and self._q_set and self._a_set:
                self.items.append((self._buf["q"], self._buf["a"]))

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._buf[self._capture] += data


def _parse_visible_faq(text: str) -> list[tuple[str, str]]:
    visitor = _FaqVisitor()
    visitor.feed(text)
    return visitor.items


def _jsonld_blocks(text: str) -> list[dict]:
    return [
        json.loads(raw)
        for raw in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            text, flags=re.DOTALL,
        )
    ]


def _parse_faq_jsonld(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for data in _jsonld_blocks(text):
        if data.get("@type") != "FAQPage":
            continue
        for entry in data.get("mainEntity", []):
            name = entry["name"]
            answer = entry["acceptedAnswer"]["text"]
            pairs.append((name, answer))
    return pairs


def _parse_dealer_jsonld(text: str) -> dict:
    for data in _jsonld_blocks(text):
        if data.get("@type") == "MotorcycleDealer":
            return data
    raise AssertionError("No MotorcycleDealer JSON-LD block found in template.")


def _css_rules(style: str) -> list[tuple[str, set[str]]]:
    """Yield (selector, declaration-names) for every CSS rule in style.

    A 'rule' is any `selector { decls }` chunk. Media queries (which nest
    braces) are not parsed — this test only needs the top-level contract.
    """
    rules: list[tuple[str, set[str]]] = []
    for chunk in style.split("}"):
        body_idx = chunk.find("{")
        if body_idx == -1:
            continue
        selector = chunk[:body_idx].strip()
        body = chunk[body_idx + 1:]
        names = {m.group(1).strip() for m in _DECL_NAME_RE.finditer(body)}
        if selector and names:
            rules.append((selector, names))
    return rules


def _has_anchor_offset(style: str) -> bool:
    """Contract: html has scroll-padding-top OR some selector has scroll-margin-top."""
    for selector, decls in _css_rules(style):
        selectors = {s.strip().split()[0] for s in selector.split(",")}
        if "html" in selectors and "scroll-padding-top" in decls:
            return True
        if "scroll-margin-top" in decls:
            return True
    return False


class _TemplateMixin:
    """Load template.html and style.css once per test class."""

    text: str
    style: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")
        cls.style = STYLESHEET_PATH.read_text(encoding="utf-8")


# Given: the visible FAQ and the FAQPage JSON-LD in template.html.
# When:  both lists are parsed and whitespace-normalized.
# Then:  ordered (question, answer) pairs are equal in count and content.
class TestFaqSchemaSync(_TemplateMixin, unittest.TestCase):
    def test_visible_faq_matches_faqpage_jsonld(self) -> None:
        visible = _parse_visible_faq(self.text)
        schema = _parse_faq_jsonld(self.text)
        self.assertGreater(len(visible), 0,
                           msg="No visible FAQ items parsed; template structure changed.")
        self.assertEqual(len(visible), len(schema),
                         msg=f"FAQ count drift: visible={len(visible)} schema={len(schema)}")
        nv = [(_normalize(q), _normalize(a)) for q, a in visible]
        ns = [(_normalize(q), _normalize(a)) for q, a in schema]
        self.assertEqual(nv, ns,
                         msg="Visible FAQ drifted from FAQPage JSON-LD mainEntity.")


# Given: header call anchor whose .call-text span is hidden on mobile.
# When:  the anchor's opening tag is inspected.
# Then:  an aria-label attribute exists and contains {{PHONE_DISPLAY}},
#        so the accessible name survives display:none on .call-text.
class TestHeaderCallAccessibleName(_TemplateMixin, unittest.TestCase):
    def test_header_call_has_aria_label_with_phone_token(self) -> None:
        m = _HEADER_CALL_RE.search(self.text)
        self.assertIsNotNone(m, msg='Missing <a class="header-call"> in template.')
        attrs = dict(_ATTR_RE.findall(m.group(0)))
        self.assertIn("aria-label", attrs,
                      msg="Mobile users see only an icon; aria-label must provide the accessible name.")
        self.assertIn("{{PHONE_DISPLAY}}", attrs["aria-label"],
                      msg="aria-label must reference {{PHONE_DISPLAY}} so variables.txt stays the phone source of truth.")


# Given: a sticky header (min-height 64px) and html { scroll-behavior: smooth }.
# When:  style.css is scanned for an anchor-offset property.
# Then:  either html { scroll-padding-top: ... } or any selector with
#        scroll-margin-top is present, so anchors land below the sticky bar.
class TestStickyAnchorOffset(_TemplateMixin, unittest.TestCase):
    def test_stylesheet_defines_sticky_anchor_offset(self) -> None:
        self.assertTrue(
            _has_anchor_offset(self.style),
            msg="Sticky header clips in-page anchors. Add `scroll-padding-top` on html, "
                "or `scroll-margin-top` on the anchor targets.",
        )


# Given: the convention that all styling lives in style.css.
# When:  template.html is scanned for inline style attributes.
# Then:  no style="..." attribute exists anywhere in the template.
class TestNoInlineStyles(_TemplateMixin, unittest.TestCase):
    def test_template_has_no_inline_style_attributes(self) -> None:
        m = _INLINE_STYLE_RE.search(self.text)
        self.assertIsNone(
            m,
            msg="Inline style attribute found in template.html. "
                "All styling belongs in style.css (edit the :root variables to recolor).",
        )


# Given: image paths referenced by template.html and style.css.
# When:  each images/... path is resolved against the repo root.
# Then:  the file exists, so no broken image ships to the live site.
class TestReferencedImagesExist(_TemplateMixin, unittest.TestCase):
    def test_referenced_images_exist(self) -> None:
        refs = set(_IMAGE_REF_RE.findall(self.text)) | set(_IMAGE_REF_RE.findall(self.style))
        self.assertGreater(len(refs), 0, msg="No images/... references found; template changed?")
        missing = sorted(ref for ref in refs if not (REPO_ROOT / ref).is_file())
        self.assertEqual(missing, [],
                         msg=f"Referenced image(s) missing from disk: {missing}")


# Given: the hero "นำทางไปร้าน" maps link and the MotorcycleDealer JSON-LD.
# When:  both are parsed (HTML entities unescaped).
# Then:  the href equals JSON-LD hasMap, and the destination coordinates
#        equal the JSON-LD geo latitude/longitude.
class TestMapsConsistency(_TemplateMixin, unittest.TestCase):
    def test_hero_maps_link_matches_jsonld(self) -> None:
        m = _HERO_MAPS_HREF_RE.search(self.text)
        self.assertIsNotNone(m, msg="No hero Google Maps directions link found in template.")
        href = html.unescape(m.group(1))
        dealer = _parse_dealer_jsonld(self.text)
        self.assertEqual(href, dealer["hasMap"],
                         msg="Hero maps link drifted from JSON-LD hasMap.")

        dest = _DESTINATION_RE.search(href)
        self.assertIsNotNone(dest, msg="Hero maps link has no destination= parameter.")
        lat, lng = unquote(dest.group(1)).split(",")
        geo = dealer["geo"]
        self.assertEqual((lat, lng), (geo["latitude"], geo["longitude"]),
                         msg="Maps destination coordinates drifted from JSON-LD geo.")


if __name__ == "__main__":
    unittest.main()
