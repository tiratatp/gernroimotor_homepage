from __future__ import annotations

import html
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template.html"
STYLESHEET_PATH = REPO_ROOT / "style.css"

_ATTR_RE = re.compile(r'''([\w-]+)\s*=\s*"([^"]*)"''')
_THAI_CHAR_RE = re.compile(r"[\u0E00-\u0E7F]")
_SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.DOTALL)


def _jsonld_blocks(text: str) -> list[dict]:
    return [
        json.loads(raw)
        for raw in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            text, flags=re.DOTALL,
        )
    ]


def _parse_dealer_jsonld(text: str) -> dict:
    for data in _jsonld_blocks(text):
        if data.get("@type") == "MotorcycleDealer":
            return data
    raise AssertionError("No MotorcycleDealer JSON-LD block found in template.")


class _TemplateMixin:
    text: str
    style: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")
        cls.style = STYLESHEET_PATH.read_text(encoding="utf-8")


# Given/When/Then: iframe src uses {{MAPS_EMBED_URL}}, no visible anchor uses
# {{BUSINESS_PROFILE_URL}} (it lives only in JSON-LD sameAs), no
# .contact-reviews-link CSS rule remains, and the coordinate directions link
# + JSON-LD hasMap are unchanged.
class TestMapEmbedContract(_TemplateMixin, unittest.TestCase):
    def test_iframe_src_uses_embed_token(self) -> None:
        m = re.search(r"<iframe\b[^>]*>", self.text, re.DOTALL)
        self.assertIsNotNone(m, msg="No <iframe> found in template.")
        attrs = dict(_ATTR_RE.findall(m.group(0)))
        self.assertEqual(
            attrs.get("src"), "{{MAPS_EMBED_URL}}",
            msg="Map iframe src must use the {{MAPS_EMBED_URL}} token.",
        )

    def test_no_visible_anchor_uses_business_profile_token(self) -> None:
        link_re = re.compile(
            r'<a\b[^>]*href="\{\{BUSINESS_PROFILE_URL\}\}"[^>]*>.*?</a>',
            re.DOTALL,
        )
        self.assertIsNone(
            link_re.search(self.text),
            msg="No visible <a href=\"{{BUSINESS_PROFILE_URL}}\"> may remain in "
                "the template; the token lives only in JSON-LD sameAs.",
        )

    def test_no_contact_reviews_link_css_rule(self) -> None:
        self.assertFalse(
            bool(re.search(r"\.contact-reviews-link\s*\{", self.style)),
            msg="style.css must not define a .contact-reviews-link rule "
                "(the visible reviews link was removed).",
        )

    def test_same_as_includes_business_profile_token(self) -> None:
        dealer = _parse_dealer_jsonld(self.text)
        same_as = dealer.get("sameAs", [])
        self.assertIn(
            "{{BUSINESS_PROFILE_URL}}", same_as,
            msg="MotorcycleDealer sameAs must include the Business Profile token.",
        )

    def test_directions_link_and_hasmap_unchanged(self) -> None:
        dirs_re = re.compile(
            r'href="(https://www\.google\.com/maps/dir/[^"]+)"',
        )
        raw_hrefs = dirs_re.findall(self.text)
        self.assertEqual(
            len(raw_hrefs), 1,
            msg="Expected exactly one coordinate directions link (unchanged).",
        )
        href = html.unescape(raw_hrefs[0])
        dealer = _parse_dealer_jsonld(self.text)
        self.assertEqual(
            href, dealer["hasMap"],
            msg="Directions link must still match JSON-LD hasMap.",
        )


# Given/When/Then: iframe has class/title/loading/allowfullscreen/referrerpolicy
# with approved values, and no width/height/style attributes.
class TestIframeAttributes(_TemplateMixin, unittest.TestCase):
    def setUp(self) -> None:
        m = re.search(r"<iframe\b[^>]*>", self.text, re.DOTALL)
        self.assertIsNotNone(m, msg="No <iframe> found in template.")
        self.attrs = dict(_ATTR_RE.findall(m.group(0)))

    def test_iframe_has_no_width_or_height(self) -> None:
        self.assertNotIn(
            "width", self.attrs,
            msg="Map iframe must not set a width attribute (CSS handles sizing).",
        )
        self.assertNotIn(
            "height", self.attrs,
            msg="Map iframe must not set a height attribute (CSS handles sizing).",
        )

    def test_iframe_has_no_inline_style(self) -> None:
        self.assertNotIn(
            "style", self.attrs,
            msg="Map iframe must not have an inline style attribute.",
        )

    def test_iframe_keeps_class_title_loading(self) -> None:
        self.assertEqual(
            self.attrs.get("class"), "map-embed",
            msg="Map iframe must keep class='map-embed'.",
        )
        title = self.attrs.get("title", "")
        self.assertTrue(title, msg="Map iframe must keep a descriptive title.")
        self.assertIsNotNone(
            _THAI_CHAR_RE.search(title),
            msg="Map iframe title must be Thai.",
        )
        self.assertEqual(
            self.attrs.get("loading"), "lazy",
            msg="Map iframe must keep loading='lazy'.",
        )

    def test_iframe_adds_allowfullscreen(self) -> None:
        m = re.search(r"<iframe\b[^>]*>", self.text, re.DOTALL)
        self.assertIsNotNone(m)
        self.assertIn(
            "allowfullscreen", m.group(0),
            msg="Map iframe must add allowfullscreen.",
        )

    def test_iframe_uses_strict_referrerpolicy(self) -> None:
        self.assertEqual(
            self.attrs.get("referrerpolicy"),
            "strict-origin-when-cross-origin",
            msg="Map iframe must use referrerpolicy='strict-origin-when-cross-origin'.",
        )


# Given/When/Then: a non-JSON-LD script near body end selects .header-nav a,
# unchecks #nav-toggle on click, and the checkbox hack markup is retained.
class TestNavCloseScript(_TemplateMixin, unittest.TestCase):
    def _non_jsonld_scripts(self) -> list[str]:
        scripts: list[str] = []
        for m in _SCRIPT_RE.finditer(self.text):
            attrs_str = m.group(1)
            if 'type="application/ld+json"' in attrs_str:
                continue
            scripts.append(m.group(2))
        return scripts

    def test_non_jsonld_script_exists(self) -> None:
        scripts = self._non_jsonld_scripts()
        self.assertGreaterEqual(
            len(scripts), 1,
            msg="At least one non-JSON-LD <script> must exist for the nav-close behavior.",
        )

    def test_script_selects_header_nav_links(self) -> None:
        scripts = self._non_jsonld_scripts()
        self.assertTrue(
            any(".header-nav a" in s for s in scripts),
            msg="The nav-close script must select '.header-nav a' links.",
        )

    def test_script_unchecks_nav_toggle(self) -> None:
        scripts = self._non_jsonld_scripts()
        self.assertTrue(
            any("nav-toggle" in s and "checked" in s and "false" in s
                for s in scripts),
            msg="The nav-close script must set #nav-toggle.checked = false.",
        )

    def test_checkbox_hack_retained(self) -> None:
        self.assertIn(
            'id="nav-toggle"', self.text,
            msg="The #nav-toggle checkbox must remain (checkbox hack retained).",
        )
        self.assertIn(
            'class="nav-hamburger"', self.text,
            msg="The .nav-hamburger label must remain (checkbox hack retained).",
        )


if __name__ == "__main__":
    unittest.main()
