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
    EXPECTED_H1 = "{{SHOP_NAME}} โชคชัย 4 แยก 63"
    EXPECTED_TAGLINE = "ร้านขายมอเตอร์ไซค์ พร้อมให้คำปรึกษาก่อนเข้าร้าน"
    EXPECTED_META_DESC = (
        "{{SHOP_NAME}} ร้านขายมอเตอร์ไซค์โชคชัย 4 แยก 63 "
        "เปิดทุกวัน 8.30-18.30 น. "
        "แอด LINE เช็กสต็อก สี โปร และค่างวดก่อนเข้าร้าน"
    )
    EXPECTED_LEAD_IN = "สนใจรุ่นไหน? แอด LINE เช็กสต็อก สี โปร และค่างวด"

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
        self.assertEqual(
            m.group(1).strip(), self.EXPECTED_H1,
            msg="<h1> must use the approved SEO copy.",
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

    def test_hero_cta_lead_in_exists_before_badge(self) -> None:
        hero = _extract_hero(self.text)
        self.assertTrue(hero, msg="No hero section found.")
        lead_re = re.compile(
            r'<p class="hero-cta-lead">' + re.escape(self.EXPECTED_LEAD_IN) + r"</p>",
        )
        lead_m = lead_re.search(hero)
        self.assertIsNotNone(
            lead_m,
            msg="Hero must contain a <p class='hero-cta-lead'> with the approved "
                "lead-in copy.",
        )
        # The LINE badge anchor must follow the lead-in with only whitespace
        # and HTML comments between them (immediately before the badge).
        after = hero[lead_m.end():]
        badge_m = re.match(
            r'\s*(?:<!--.*?-->\s*)*<a\b[^>]*class="line-cta"',
            after, re.DOTALL,
        )
        self.assertIsNotNone(
            badge_m,
            msg="The hero CTA lead-in must sit immediately before the .line-cta "
                "badge with nothing between them but whitespace.",
        )


if __name__ == "__main__":
    unittest.main()
