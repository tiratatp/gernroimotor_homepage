"""Structural tests for the official LINE Add Friend image CTA contract.

The contract is per-section, not count-based, so it keeps holding when
sections are added to or removed from the page:

  * every <section> inside <main> carries exactly one .line-cta conversion
    anchor — except <section id="contact">, whose LINE card is a utility
    link (.contact-item) and must NOT be a conversion anchor;
  * each anchor uses the {{LINE_ID}} URL with target="_blank" rel="noopener"
    and wraps the official 202x60 image with a Thai alt that exposes
    @{{LINE_ID}};
  * the hero anchor's image is eager-loaded (LCP); every other section's
    image is lazy-loaded;
  * no section pairs its LINE button with a #contact fallback anchor;
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
_MAIN_RE = re.compile(r"<main\b[^>]*>(.*?)</main>", re.DOTALL)
_SECTION_RE = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.DOTALL)
_LINE_CTA_RE = re.compile(
    r'<a\b[^>]*class="line-cta"[^>]*>(.*?)</a>',
    re.DOTALL,
)
_THAI_CHAR_RE = re.compile(r"[\u0E00-\u0E7F]")


def _extract_main_sections(text: str) -> list[tuple[dict[str, str], str]]:
    """Return (opening-tag attrs, inner HTML) for each <section> in <main>."""
    main = _MAIN_RE.search(text)
    if not main:
        return []
    return [
        (dict(_ATTR_RE.findall(s.group(1))), s.group(2))
        for s in _SECTION_RE.finditer(main.group(1))
    ]


class _TemplateMixin:
    """Load template.html once per test class."""

    text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")


# Given: the page is a sequence of <section> blocks inside <main> and every
#        section is a conversion opportunity. Sections may be added or
#        removed over time, so the contract must not depend on how many
#        exist — only on each section carrying its own button.
# When:  template.html is scanned section by section.
# Then:  every section except #contact carries exactly one validated
#        .line-cta anchor, #contact carries none, the hero badge is eager
#        while all other badges are lazy, and no section keeps a #contact
#        fallback anchor next to its LINE button.
class TestLineCtaContract(_TemplateMixin, unittest.TestCase):
    def test_self_hosted_badge_matches_official_asset(self) -> None:
        digest = hashlib.sha256(LINE_BADGE_PATH.read_bytes()).hexdigest()
        self.assertEqual(
            digest, OFFICIAL_LINE_BADGE_SHA256,
            msg="The official LINE badge must remain unmodified.",
        )

    def test_main_has_multiple_sections(self) -> None:
        self.assertGreaterEqual(
            len(_extract_main_sections(self.text)), 3,
            msg="Sanity check: expected several <section> blocks inside "
                "<main>; the per-section contract would pass vacuously "
                "otherwise.",
        )

    def test_every_section_except_contact_has_exactly_one_line_cta(self) -> None:
        sections = _extract_main_sections(self.text)
        self.assertTrue(sections, msg="No <section> blocks found in <main>.")
        seen_ids = set()
        for attrs, inner in sections:
            section_id = attrs.get("id", "")
            seen_ids.add(section_id)
            label = section_id or attrs.get("class", "<unknown>")
            count = len(_LINE_CTA_RE.findall(inner))
            if section_id == "contact":
                self.assertEqual(
                    count, 0,
                    msg="Contact-section LINE card must use .contact-item, "
                        "not .line-cta — it is a utility link, not a "
                        "conversion anchor.",
                )
            else:
                self.assertEqual(
                    count, 1,
                    msg=f"Section '{label}' must carry exactly one .line-cta "
                        f"conversion anchor, found {count}.",
                )
        self.assertIn(
            "contact", seen_ids,
            msg="Expected a <section id='contact'> inside <main>.",
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

    def test_no_section_pairs_line_cta_with_contact_fallback(self) -> None:
        for attrs, inner in _extract_main_sections(self.text):
            if not _LINE_CTA_RE.search(inner):
                continue
            self.assertNotIn(
                'href="#contact"', inner,
                msg=f"Section '{attrs.get('id', '<unknown>')}' must not "
                    f"carry a #contact fallback anchor; the LINE button "
                    f"replaces it.",
            )

    def test_hero_badge_is_eager_and_all_other_badges_are_lazy(self) -> None:
        hero_badges = 0
        for attrs, inner in _extract_main_sections(self.text):
            m = _LINE_CTA_RE.search(inner)
            if m is None:
                continue
            img = re.search(r"<img\b[^>]*>", m.group(1), re.DOTALL)
            self.assertIsNotNone(img, msg="line-cta must wrap an <img>.")
            loading = dict(_ATTR_RE.findall(img.group(0))).get("loading")
            if "hero" in attrs.get("class", "").split():
                hero_badges += 1
                self.assertNotEqual(
                    loading, "lazy",
                    msg="Hero .line-cta image must be eager-loaded for LCP "
                        "(no loading='lazy').",
                )
            else:
                self.assertEqual(
                    loading, "lazy",
                    msg=f"Section '{attrs.get('id', '<unknown>')}' .line-cta "
                        f"image must be loading='lazy'.",
                )
        self.assertEqual(
            hero_badges, 1,
            msg="Expected exactly one hero section carrying a .line-cta.",
        )


if __name__ == "__main__":
    unittest.main()
