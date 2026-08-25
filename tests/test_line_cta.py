"""Structural tests for the official LINE Add Friend image CTA contract.

Guards:
  * exactly five .line-cta conversion anchors exist (hero + four
    .section-cta blocks);
  * each anchor uses the {{LINE_ID}} URL with target="_blank" rel="noopener"
    and wraps the official 202x60 image with a Thai alt that exposes
    @{{LINE_ID}};
  * the hero anchor's image is eager-loaded; the four section-end
    images are lazy-loaded and the section blocks no longer carry a
    #contact fallback anchor;
  * the contact-section LINE card uses .contact-item, not .line-cta;
  * the self-hosted PNG is the exact unmodified official LINE asset.

All contracts must pass before deployment.
"""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template.html"
LINE_BADGE_PATH = REPO_ROOT / "images" / "line-add-friend-th.png"
OFFICIAL_LINE_BADGE_SHA256 = "4c58bda197c567b3ca6a70878f85626cc266112e574462e995892f2d2b7a2f2f"

_ATTR_RE = re.compile(r'''([\w-]+)\s*=\s*"([^"]*)"''')
_HERO_SECTION_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>(.*?)</section>',
    re.DOTALL,
)
_CONTACT_SECTION_RE = re.compile(
    r'<section\b[^>]*id="contact"[^>]*>(.*?)</section>',
    re.DOTALL,
)
_LINE_CTA_RE = re.compile(
    r'<a\b[^>]*class="line-cta"[^>]*>(.*?)</a>',
    re.DOTALL,
)
_SECTION_CTA_RE = re.compile(
    r'<div\b[^>]*class="[^"]*\bsection-cta\b[^"]*"[^>]*>(.*?)</div>',
    re.DOTALL,
)
_THAI_CHAR_RE = re.compile(r"[\u0E00-\u0E7F]")


def _extract_hero(text: str) -> str:
    """Return the inner HTML of <section class="hero">, or empty string."""
    m = _HERO_SECTION_RE.search(text)
    return m.group(1) if m else ""


class _TemplateMixin:
    """Load template.html once per test class."""

    text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")


# Given: the official LINE Add Friend button appears in exactly five spots —
#        the hero (eager, for LCP) plus four .section-cta blocks (services,
#        testimonials, brands, FAQ) carrying a lazy badge. The contact
#        section's LINE card is a separate utility link and must NOT count as
#        a conversion anchor.
# When:  template.html is scanned for .line-cta anchors and their parent
#        context (.section-cta vs <section id="contact">).
# Then:  the structural contract holds: count, href + safe link attrs,
#        image src/alt/width/height, parent context, loading eagerness,
#        and absence of the #contact fallback.
class TestLineCtaContract(_TemplateMixin, unittest.TestCase):
    def test_self_hosted_badge_matches_official_asset(self) -> None:
        digest = hashlib.sha256(LINE_BADGE_PATH.read_bytes()).hexdigest()
        self.assertEqual(
            digest, OFFICIAL_LINE_BADGE_SHA256,
            msg="The official LINE badge must remain unmodified.",
        )

    def test_exactly_five_line_cta_anchors(self) -> None:
        self.assertEqual(
            len(_LINE_CTA_RE.findall(self.text)), 5,
            msg="Expected exactly 5 .line-cta conversion anchors "
                "(hero + 4 .section-cta blocks).",
        )

    def test_each_anchor_uses_line_id_href_and_safe_link_attrs(self) -> None:
        for idx, m in enumerate(_LINE_CTA_RE.finditer(self.text), start=1):
            anchor = m.group(0)
            self.assertIn(
                'href="https://line.me/R/ti/p/@{{LINE_ID}}"', anchor,
                msg=f"line-cta #{idx} href must use @{{LINE_ID}}.",
            )
            self.assertIn(
                'target="_blank"', anchor,
                msg=f"line-cta #{idx} must open in a new tab.",
            )
            self.assertIn(
                'rel="noopener"', anchor,
                msg=f"line-cta #{idx} must use rel=noopener.",
            )

    def test_each_anchor_wraps_official_image_with_native_dimensions_and_thai_alt(self) -> None:
        for idx, inner in enumerate(_LINE_CTA_RE.findall(self.text), start=1):
            img = re.search(r"<img\b[^>]*>", inner, re.DOTALL)
            self.assertIsNotNone(img,
                                 msg=f"line-cta #{idx} must wrap an <img>.")
            attrs = dict(_ATTR_RE.findall(img.group(0)))
            self.assertEqual(attrs.get("src"), "images/line-add-friend-th.png",
                             msg=f"line-cta #{idx} must use the official "
                                 f"images/line-add-friend-th.png image.")
            self.assertEqual(attrs.get("width"), "202",
                             msg=f"line-cta #{idx} must declare native width=202.")
            self.assertEqual(attrs.get("height"), "60",
                             msg=f"line-cta #{idx} must declare native height=60.")
            alt = attrs.get("alt", "")
            self.assertIn("@{{LINE_ID}}", alt,
                          msg=f"line-cta #{idx} alt must expose @{{LINE_ID}}.")
            self.assertIsNotNone(_THAI_CHAR_RE.search(alt),
                            msg=f"line-cta #{idx} alt must contain Thai text.")

    def test_four_section_cta_blocks_carry_lazy_badges_and_no_contact_fallback(self) -> None:
        blocks = _SECTION_CTA_RE.findall(self.text)
        self.assertEqual(
            len(blocks), 4,
            msg=f"Expected exactly 4 .section-cta blocks, found {len(blocks)}.",
        )
        for idx, block in enumerate(blocks, start=1):
            self.assertIn(
                'class="line-cta"', block,
                msg=f"section-cta #{idx} must contain a .line-cta anchor.",
            )
            self.assertNotIn(
                'href="#contact"', block,
                msg=f"section-cta #{idx} must not carry a #contact fallback "
                    f"anchor; the LINE button replaces it.",
            )
            m = _LINE_CTA_RE.search(block)
            self.assertIsNotNone(
                m, msg=f"section-cta #{idx} .line-cta anchor not matched.",
            )
            img = re.search(r"<img\b[^>]*>", m.group(1), re.DOTALL)
            self.assertIsNotNone(
                img, msg=f"section-cta #{idx} .line-cta must wrap an <img>.",
            )
            attrs = dict(_ATTR_RE.findall(img.group(0)))
            self.assertEqual(
                attrs.get("loading"), "lazy",
                msg=f"section-end .line-cta #{idx} image must be loading='lazy'.",
            )

    def test_hero_badge_is_eager(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No <section class='hero'> found in template.")
        m = _LINE_CTA_RE.search(hero)
        self.assertIsNotNone(m, msg="Hero must contain a .line-cta anchor.")
        img = re.search(r"<img\b[^>]*>", m.group(1), re.DOTALL)
        self.assertIsNotNone(img, msg="Hero .line-cta must wrap an <img>.")
        attrs = dict(_ATTR_RE.findall(img.group(0)))
        self.assertNotEqual(
            attrs.get("loading"), "lazy",
            msg="Hero .line-cta image must be eager-loaded for LCP "
                "(no loading='lazy').",
        )

    def test_contact_section_line_card_excluded_from_conversion_anchors(self) -> None:
        m = _CONTACT_SECTION_RE.search(self.text)
        self.assertIsNotNone(m,
                             msg="No <section id='contact'> found in template.")
        self.assertNotIn(
            'class="line-cta"', m.group(1),
            msg="Contact-section LINE card must use .contact-item, "
                "not .line-cta — it is a utility link, not a conversion anchor.",
        )


if __name__ == "__main__":
    unittest.main()
