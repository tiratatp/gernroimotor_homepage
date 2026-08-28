"""Exact SEO/hero copy contract tests for template.html.

Guards:
  * <title> uses the approved copy with the {{SHOP_NAME}} token;
  * hero <h1> uses the approved copy with the {{SHOP_NAME}} token;
  * hero tagline visible text matches the approved copy exactly;
  * meta description uses the approved copy with the {{SHOP_NAME}} token;
  * og:description matches the meta description copy exactly;
  * hero CTA lead-in sits immediately before the official LINE badge.

All contracts must pass before deployment.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template.html"
STYLE_PATH = REPO_ROOT / "style.css"

_HERO_SECTION_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>(.*?)</section>',
    re.DOTALL,
)


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


# Given: the approved SEO copy changes to <title>, <h1>, hero tagline, meta
#        description, og:description (matching meta description), and a new
#        hero CTA lead-in before the LINE badge.
# When:  template.html is parsed for each element.
# Then:  the exact approved copy is present and the lead-in sits immediately
#        before the badge.
class TestSeoCopyContract(_TemplateMixin, unittest.TestCase):
    EXPECTED_TITLE = "{{SHOP_NAME}} | ร้านขายมอเตอร์ไซค์ โชคชัย 4 แยก 63"
    EXPECTED_H1 = "{{SHOP_NAME}} ร้านมอเตอร์ไซค์ ลาดพร้าว โชคชัย 4"
    EXPECTED_TAGLINE = (
        "มีรถให้เลือกทั้ง Honda, Yamaha และมอเตอร์ไซค์ไฟฟ้า "
        "พร้อมเช็กโปรโมชั่น เงินดาวน์ ค่างวด และสต็อกได้ก่อนเข้าร้าน"
    )
    EXPECTED_META_DESC = (
        "{{SHOP_NAME}} ร้านขายมอเตอร์ไซค์ใกล้โชคชัย 4 แยก 63 ลาดพร้าว "
        "เปิดทุกวัน 8.30-18.30 น. "
        "แอด LINE เช็กสต็อก สี โปร และค่างวดก่อนเข้าร้าน"
    )
    EXPECTED_LOCATION = (
        "ร้านอยู่ โชคชัย 4 แยก 63 ลาดพร้าว "
        "เดินทางสะดวกจากโซนนาคนิวาส ลาดพร้าววังหิน รัชดา และห้วยขวาง"
    )

    def test_title_tag_uses_approved_copy(self) -> None:
        m = re.search(r"<title>(.*?)</title>", self.text, re.DOTALL)
        self.assertIsNotNone(m, msg="No <title> tag found in template.")
        self.assertEqual(
            m.group(1).strip(), self.EXPECTED_TITLE,
            msg="<title> must use the approved SEO copy.",
        )

    def test_h1_uses_approved_copy(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No <section class='hero'> found in template.")
        m = re.search(r"<h1>(.*?)</h1>", hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No <h1> found in hero.")
        # Visible text is the contract; nowrap spans inside the h1 are markup.
        visible = re.sub(r"<[^>]+>", " ", m.group(1)).strip()
        visible = re.sub(r"\s+", " ", visible)
        self.assertEqual(
            visible, self.EXPECTED_H1,
            msg="<h1> must use the approved SEO copy.",
        )

    def test_h1_shop_name_never_breaks(self) -> None:
        """The shop name must stay on one line; the branch line may wrap.

        Both parts are display:block so they always sit on separate lines. The
        branch line is now long enough that forcing nowrap on it overflowed a
        375px screen, so only the shop name carries the nowrap guarantee.
        """
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No hero section found.")
        m = re.search(r"<h1>(.*?)</h1>", hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No <h1> found in hero.")
        inner = m.group(1).strip()
        name = re.search(
            r'<span class="[^"]*\bnowrap\b[^"]*\bhero-title-name\b[^"]*">([^<]+)</span>',
            inner,
        )
        self.assertIsNotNone(
            name,
            msg="The shop name span must carry both nowrap and hero-title-name.",
        )
        self.assertEqual(
            name.group(1).strip(), "{{SHOP_NAME}}",
            msg="The nowrap-protected part of the h1 must be the shop name token.",
        )
        self.assertNotIn(
            "nowrap", re.search(r'<span class="[^"]*hero-title-branch[^"]*"', inner).group(0),
            msg="The branch line must not be nowrap; it is too long to fit one line.",
        )

    def test_h1_parts_carry_their_own_size_hooks(self) -> None:
        """Shop name and branch are sized separately, so each needs its own class."""
        hero = _extract_hero(self.text)
        m = re.search(r"<h1>(.*?)</h1>", hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No <h1> found in hero.")
        inner = m.group(1)
        for cls, part in (("hero-title-name", "{{SHOP_NAME}}"),
                          ("hero-title-branch", "ร้านมอเตอร์ไซค์ ลาดพร้าว โชคชัย 4")):
            m2 = re.search(
                r'<span class="[^"]*\b' + cls + r'\b[^"]*">([^<]+)</span>', inner,
            )
            self.assertIsNotNone(
                m2, msg=f"h1 must carry a .{cls} span for its own font-size.",
            )
            self.assertEqual(
                m2.group(1).strip(), part,
                msg=f".{cls} must wrap {part!r}.",
            )
        style = STYLE_PATH.read_text(encoding="utf-8")
        for cls in ("hero-title-name", "hero-title-branch"):
            self.assertIn(
                "." + cls, style,
                msg=f"style.css must define a .{cls} rule.",
            )

    def test_hero_tagline_uses_approved_copy(self) -> None:
        hero = _extract_hero(self.text)
        m = re.search(r'<p class="hero-tagline">(.*?)</p>', hero, re.DOTALL)
        self.assertIsNotNone(m, msg="No .hero-tagline paragraph found in hero.")
        visible = re.sub(r"<[^>]+>", " ", m.group(1)).strip()
        visible = re.sub(r"\s+", " ", visible)
        self.assertEqual(
            visible, self.EXPECTED_TAGLINE,
            msg="Hero tagline visible text must match the approved copy exactly.",
        )

    def test_meta_description_uses_approved_copy(self) -> None:
        m = re.search(
            r'<meta\s+name="description"\s+content="([^"]*)"',
            self.text,
        )
        self.assertIsNotNone(m, msg="No meta description found in template.")
        self.assertEqual(
            m.group(1), self.EXPECTED_META_DESC,
            msg="Meta description must use the approved copy exactly.",
        )

    def test_og_description_matches_meta_description(self) -> None:
        m = re.search(
            r'<meta\s+property="og:description"\s+content="([^"]*)"',
            self.text,
        )
        self.assertIsNotNone(m, msg="No og:description found in template.")
        self.assertEqual(
            m.group(1), self.EXPECTED_META_DESC,
            msg="og:description must match the approved meta description copy "
                "exactly.",
        )

    def test_hero_location_line_precedes_the_line_button(self) -> None:
        """The location line is the last text before the hero's LINE button."""
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No hero section found.")
        loc_re = re.compile(
            r'<p class="hero-location">' + re.escape(self.EXPECTED_LOCATION) + r"</p>",
        )
        loc_m = loc_re.search(hero)
        self.assertIsNotNone(
            loc_m,
            msg="Hero must contain a <p class='hero-location'> with the approved copy.",
        )
        after = hero[loc_m.end():]
        self.assertIsNotNone(
            re.match(r'\s*(?:<!--.*?-->\s*)*<div class="hero-actions">\s*'
                     r'(?:<!--.*?-->\s*)*<a\b[^>]*class="line-cta"', after, re.DOTALL),
            msg="The LINE button must follow the location line, with only "
                "whitespace and comments between them.",
        )
