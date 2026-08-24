"""Structural tests for template.html and style.css.

Guards:
  * visible FAQ Q&A pairs in <section id="faq"> stay in lockstep with the
    FAQPage JSON-LD mainEntity.
  * the header-call anchor is absent from both template and stylesheet (it
    was removed in the mobile-first header redesign).
  * the hero contains a semantic, high-priority <img> with explicit
    dimensions and Thai alt text.
  * the hero LINE CTA uses the {{LINE_ID}} token in href and image alt,
    with target="_blank" rel="noopener".
  * style.css defines a sticky-anchor offset, so in-page anchors do not land
    beneath the sticky header.
  * template.html carries no inline style="..." attributes — all styling
    lives in style.css.
  * every images/... path referenced by template.html or style.css exists.
  * the contact-section directions link matches the JSON-LD hasMap URL and
    its destination coordinates match the JSON-LD geo coordinates.

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
_ATTR_RE = re.compile(r'''([\w-]+)\s*=\s*"([^"]*)"''')
_DECL_NAME_RE = re.compile(r"([\w-]+)\s*:")
_INLINE_STYLE_RE = re.compile(r"\sstyle\s*=\s*[\"']")
_IMAGE_REF_RE = re.compile(r"images/[A-Za-z0-9._-]+")
_ALL_MAPS_HREFS_RE = re.compile(r'href="(https://www\.google\.com/maps/dir/[^"]+)"')
_DESTINATION_RE = re.compile(r"destination=([^&]+)")
_HERO_SECTION_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>(.*?)</section>',
    re.DOTALL,
)
_THAI_CHAR_RE = re.compile(r"[\u0E00-\u0E7F]")


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def _extract_hero(text: str) -> str:
    """Return the inner HTML of <section class="hero">, or empty string."""
    m = _HERO_SECTION_RE.search(text)
    return m.group(1) if m else ""


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


# Given: the header was redesigned to remove the call button.
# When:  template.html and style.css are scanned for header-call.
# Then:  no header-call, call-icon, or call-text class remains in either file.
class TestNoHeaderCall(_TemplateMixin, unittest.TestCase):
    def test_header_call_absent_from_template(self) -> None:
        self.assertNotIn("header-call", self.text,
                         msg="header-call markup must be removed from template.html.")

    def test_header_call_absent_from_stylesheet(self) -> None:
        for dead in (".header-call", ".call-icon", ".call-text"):
            self.assertNotIn(dead, self.style,
                             msg=f"{dead} CSS must be removed from style.css.")


# Given: the hero was redesigned to use a semantic <img> above the text.
# When:  the hero section is extracted and its <img> is parsed.
# Then:  the image uses images/shop-front.jpg with width=1200, height=900,
#        loading=eager, fetchpriority=high, and Thai alt text.
class TestHeroImage(_TemplateMixin, unittest.TestCase):
    def test_hero_has_semantic_high_priority_image(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No <section class='hero'> found in template.")
        m = re.search(r"<img\b[^>]*>", hero, re.DOTALL)
        self.assertIsNotNone(m, msg="Hero must contain a semantic <img>.")
        attrs = dict(_ATTR_RE.findall(m.group(0)))
        self.assertEqual(attrs.get("src"), "images/shop-front.jpg",
                         msg="Hero image must use images/shop-front.jpg.")
        self.assertEqual(attrs.get("width"), "1200",
                         msg="Hero image must declare width=1200.")
        self.assertEqual(attrs.get("height"), "900",
                         msg="Hero image must declare height=900.")
        self.assertEqual(attrs.get("loading"), "eager",
                         msg="Hero image must use loading=eager for LCP.")
        self.assertEqual(attrs.get("fetchpriority"), "high",
                         msg="Hero image must use fetchpriority=high for LCP.")
        alt = attrs.get("alt", "")
        self.assertTrue(alt, msg="Hero image must have alt text.")
        self.assertIsNotNone(_THAI_CHAR_RE.search(alt),
                        msg="Hero image alt must contain Thai text.")


# Given: the hero has a single LINE CTA using the {{LINE_ID}} token.
# When:  the hero section is extracted and its LINE anchor is inspected.
# Then:  the href uses @{{LINE_ID}}, the wrapped <img> alt exposes
#        @{{LINE_ID}} with Thai text (the accessible name replaces the
#        legacy visible-text rendering), and the link opens safely with
#        target=_blank rel=noopener.
class TestHeroLineCta(_TemplateMixin, unittest.TestCase):
    def test_hero_line_cta_uses_line_id_token(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No <section class='hero'> found in template.")
        self.assertIn('href="https://line.me/R/ti/p/@{{LINE_ID}}"', hero,
                      msg="Hero LINE CTA href must use @{{LINE_ID}} token.")
        self.assertIn('target="_blank"', hero,
                      msg="Hero LINE CTA must open in a new tab.")
        self.assertIn('rel="noopener"', hero,
                      msg="Hero LINE CTA must use rel=noopener.")
        m = re.search(r'<a\b[^>]*class="line-cta"[^>]*>(.*?)</a>', hero, re.DOTALL)
        self.assertIsNotNone(m, msg="Hero must contain a .line-cta anchor.")
        img = re.search(r"<img\b[^>]*>", m.group(1), re.DOTALL)
        self.assertIsNotNone(img, msg="Hero .line-cta must wrap an <img>.")
        alt = dict(_ATTR_RE.findall(img.group(0))).get("alt", "")
        self.assertIn("@{{LINE_ID}}", alt,
                      msg="Hero LINE CTA image alt must expose @{{LINE_ID}} as the accessible name.")
        self.assertIsNotNone(_THAI_CHAR_RE.search(alt),
                        msg="Hero LINE CTA image alt must contain Thai text.")


# Given: the hero tagline contains Thai words/phrases that must not split.
# When:  the tagline <p> is extracted and its nowrap spans are parsed.
# Then:  the .nowrap class exists in style.css, and the tagline wraps each
#        logical group in <span class="nowrap"> so Thai line-breaking cannot
#        split protected words like ยามาฮ่า or phrases like
#        มีบริการหลังการขายครบวงจร.
class TestHeroTaglineNoBreak(_TemplateMixin, unittest.TestCase):
    def test_nowrap_class_defined_in_stylesheet(self) -> None:
        self.assertIn(".nowrap", self.style,
                      msg="style.css must define a reusable .nowrap class.")
        self.assertIn("white-space: nowrap", self.style,
                      msg=".nowrap class must use white-space: nowrap.")

    def test_hero_tagline_protects_logical_groups(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No <section class='hero'> found in template.")
        m = re.search(r'<p class="hero-tagline">(.*?)</p>', hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No .hero-tagline paragraph found in hero.")
        tagline_html = m.group(1)
        for phrase in ("ฮอนด้า ยามาฮ่า", "มีบริการหลังการขายครบวงจร"):
            self.assertIn(f'<span class="nowrap">{phrase}</span>', tagline_html,
                          msg=f"Tagline must wrap '{phrase}' in <span class='nowrap'>.")

    def test_hero_tagline_preserves_full_sentence(self) -> None:
        hero = _extract_hero(self.text)
        m = re.search(r'<p class="hero-tagline">(.*?)</p>', hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No .hero-tagline paragraph found in hero.")
        visible = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        expected = "ร้านขายมอเตอร์ไซค์ ทุกรุ่น ทุกยี่ห้อ ฮอนด้า ยามาฮ่า ฟรีดาวน์ มีบริการหลังการขายครบวงจร"
        self.assertEqual(_normalize(visible), _normalize(expected),
                         msg="Hero tagline wording must not change.")


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


# Given: the contact-section "นำทางไปร้าน" maps link and the MotorcycleDealer JSON-LD.
# When:  all maps directions hrefs are collected (HTML entities unescaped).
# Then:  exactly one exists (the hero no longer has a maps link), the href
#        equals JSON-LD hasMap, and the destination coordinates equal the
#        JSON-LD geo latitude/longitude.
class TestDirectionsConsistency(_TemplateMixin, unittest.TestCase):
    def test_directions_link_matches_jsonld(self) -> None:
        raw_hrefs = _ALL_MAPS_HREFS_RE.findall(self.text)
        self.assertEqual(len(raw_hrefs), 1,
                         msg="Expected exactly one maps directions link (in #contact); "
                             "hero must not contain one.")
        href = html.unescape(raw_hrefs[0])
        dealer = _parse_dealer_jsonld(self.text)
        self.assertEqual(href, dealer["hasMap"],
                         msg="Directions link drifted from JSON-LD hasMap.")

        dest = _DESTINATION_RE.search(href)
        self.assertIsNotNone(dest, msg="Directions link has no destination= parameter.")
        lat, lng = unquote(dest.group(1)).split(",")
        geo = dealer["geo"]
        self.assertEqual((lat, lng), (geo["latitude"], geo["longitude"]),
                         msg="Maps destination coordinates drifted from JSON-LD geo.")


if __name__ == "__main__":
    unittest.main()
