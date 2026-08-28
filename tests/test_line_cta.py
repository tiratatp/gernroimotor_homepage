"""Structural tests for the LINE CTA contract.

Each button is built from the LINE logo mark plus its own Thai label, so
the label can differ per section while the link and brand styling stay
identical everywhere.

The contract is per-section, not count-based, so it keeps holding when
sections are added to or removed from the page:

  * every <section> inside <main> carries exactly one .line-cta conversion
    anchor — except <section id="contact">, whose LINE card is a utility
    link (.contact-item) and must NOT be a conversion anchor;
  * each anchor uses the {{LINE_ID}} URL with target="_blank" rel="noopener";
  * each anchor pairs the shared images/line-logo.svg mark (decorative,
    empty alt) with a non-empty Thai label in .line-cta-text;
  * every section's label is distinct — the point of the split is that each
    button can say something different;
  * each label is preceded by an EDIT ME marker so the maintainer can find it;
  * the hero anchor's logo is eager-loaded (LCP); every other section's is
    lazy-loaded;
  * no section pairs its LINE button with a #contact fallback anchor;
  * style.css paints the button with LINE's brand states: base #06C755,
    hover +10% black, press +30% black.

All contracts must pass before deployment.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template.html"
LINE_LOGO_PATH = REPO_ROOT / "images" / "line-logo.svg"
STYLE_PATH = REPO_ROOT / "style.css"
LINE_BASE_COLOR = "#06C755"

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
    def test_line_logo_asset_exists(self) -> None:
        self.assertTrue(
            LINE_LOGO_PATH.is_file(),
            msg="images/line-logo.svg must exist — every LINE button uses it.",
        )
        svg = LINE_LOGO_PATH.read_text(encoding="utf-8")
        self.assertIn("<svg", svg, msg="line-logo.svg must be an SVG.")
        self.assertIn(
            LINE_BASE_COLOR.lower(), svg.lower(),
            msg="The logo mark must keep LINE's #06C755 plate so it blends "
                "into the button background.",
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

    def test_each_anchor_pairs_shared_logo_with_thai_label(self) -> None:
        for idx, inner in enumerate(_LINE_CTA_RE.findall(self.text), start=1):
            img = re.search(r"<img\b[^>]*>", inner, re.DOTALL)
            self.assertIsNotNone(img,
                                 msg=f"line-cta #{idx} must include the logo <img>.")
            attrs = dict(_ATTR_RE.findall(img.group(0)))
            self.assertEqual(attrs.get("src"), "images/line-logo.svg",
                             msg=f"line-cta #{idx} must use the shared "
                                 f"images/line-logo.svg mark.")
            self.assertEqual(
                attrs.get("alt"), "",
                msg=f"line-cta #{idx} logo is decorative (the label carries "
                    f"the meaning) and must use alt=\"\".",
            )
            label = re.search(
                r'<span class="line-cta-text">([^<]+)</span>', inner,
            )
            self.assertIsNotNone(
                label,
                msg=f"line-cta #{idx} must carry a .line-cta-text label.",
            )
            text = label.group(1).strip()
            self.assertTrue(text,
                            msg=f"line-cta #{idx} label must not be empty.")
            self.assertIsNotNone(
                _THAI_CHAR_RE.search(text),
                msg=f"line-cta #{idx} label must contain Thai text.",
            )

    def test_each_section_label_is_distinct(self) -> None:
        labels = re.findall(
            r'<span class="line-cta-text">([^<]+)</span>', self.text,
        )
        self.assertGreaterEqual(
            len(labels), 2,
            msg="Sanity check: expected several LINE button labels.",
        )
        self.assertEqual(
            len(set(l.strip() for l in labels)), len(labels),
            msg="Each section's LINE button must carry its own label; "
                f"found duplicates in {labels}.",
        )

    def test_each_label_is_marked_editable(self) -> None:
        """Every button sits under an EDIT ME marker the maintainer can grep."""
        for idx, m in enumerate(_LINE_CTA_RE.finditer(self.text), start=1):
            preceding_lines = self.text[:m.start()].splitlines()[-3:]
            self.assertTrue(
                any("EDIT ME" in line for line in preceding_lines),
                msg=f"line-cta #{idx} must be directly preceded by an EDIT ME "
                    f"comment so the maintainer knows the label is editable; "
                    f"saw {preceding_lines}.",
            )

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

    def test_button_uses_line_brand_state_colors(self) -> None:
        """Base #06C755, hover +10% black, press +30% black (LINE's spec)."""
        style = STYLE_PATH.read_text(encoding="utf-8")
        self.assertIn(
            LINE_BASE_COLOR, style,
            msg="style.css must define LINE's base color #06C755.",
        )
        self.assertIn(
            ".line-cta:hover::after", style,
            msg="Hover state must be a translucent overlay covering the whole "
                "button (logo included), not a background-only change.",
        )
        self.assertIn(
            "rgba(0,0,0,0.1)", style.replace(" ", ""),
            msg="Hover overlay must be black at 10% opacity.",
        )
        self.assertIn(
            ".line-cta:active::after", style,
            msg="Press state must use the same overlay mechanism as hover.",
        )
        self.assertIn(
            "rgba(0,0,0,0.3)", style.replace(" ", ""),
            msg="Press overlay must be black at 30% opacity.",
        )

    def test_hero_badge_is_eager_and_all_other_badges_are_lazy(self) -> None:
        hero_ctas = 0
        for attrs, inner in _extract_main_sections(self.text):
            m = _LINE_CTA_RE.search(inner)
            if m is None:
                continue
            img = re.search(r"<img\b[^>]*>", m.group(1), re.DOTALL)
            self.assertIsNotNone(img, msg="line-cta must include the logo <img>.")
            loading = dict(_ATTR_RE.findall(img.group(0))).get("loading")
            if "hero" in attrs.get("class", "").split():
                hero_ctas += 1
                self.assertNotEqual(
                    loading, "lazy",
                    msg="Hero .line-cta logo must be eager-loaded for LCP "
                        "(no loading='lazy').",
                )
            else:
                self.assertEqual(
                    loading, "lazy",
                    msg=f"Section '{attrs.get('id', '<unknown>')}' .line-cta "
                        f"logo must be loading='lazy'.",
                )
        self.assertEqual(
            hero_ctas, 1,
            msg="Expected exactly one hero section carrying a .line-cta.",
        )


if __name__ == "__main__":
    unittest.main()
