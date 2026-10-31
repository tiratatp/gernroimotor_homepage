"""Structural tests for ev-models-template.html (the EV-models landing page).

Guards:
  * ev-models-template.html exists and keeps the maintainer markers
    (EDIT ME / COPY FROM HERE...TO HERE) that README.md teaches.
  * it links style.css and carries no inline style="..." attributes.
  * every images/... path it references exists on disk.
  * canonical / og:url point at the page's own URL ({{SITE_URL}}ev-models.html).
  * build.py actually builds ev-models.html, with no leftover {{TOKEN}},
    a closing </html>, and valid JSON-LD.

All contracts must pass before deployment.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "ev-models-template.html"
OUTPUT_PATH = REPO_ROOT / "ev-models.html"

_INLINE_STYLE_RE = re.compile(r"\sstyle\s*=\s*[\"']")
_IMAGE_REF_RE = re.compile(r"images/[A-Za-z0-9._-]+")


class TestEvModelsTemplateExists(unittest.TestCase):
    def test_template_file_exists(self) -> None:
        self.assertTrue(
            TEMPLATE_PATH.exists(),
            msg="ev-models-template.html is missing from the repo root.",
        )


class _TemplateMixin:
    text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = TEMPLATE_PATH.read_text(encoding="utf-8")


class TestMaintainerMarkers(_TemplateMixin, unittest.TestCase):
    def test_edit_me_markers_present(self) -> None:
        self.assertIn("EDIT ME", self.text)

    def test_copy_paste_fences_present(self) -> None:
        self.assertIn("COPY FROM HERE", self.text)
        self.assertIn("คัดลอกตั้งแต่ตรงนี้", self.text)
        self.assertIn("TO HERE", self.text)
        self.assertIn("ถึงตรงนี้", self.text)


class TestStylesheet(_TemplateMixin, unittest.TestCase):
    def test_links_shared_stylesheet(self) -> None:
        self.assertIn('rel="stylesheet" href="style.css"', self.text)


class TestNoInlineStyles(_TemplateMixin, unittest.TestCase):
    def test_no_inline_style_attributes(self) -> None:
        match = _INLINE_STYLE_RE.search(self.text)
        self.assertIsNone(
            match,
            msg="ev-models-template.html has an inline style=... attribute; "
                "all styling must live in style.css.",
        )


class TestReferencedImagesExist(_TemplateMixin, unittest.TestCase):
    def test_images_referenced_exist_on_disk(self) -> None:
        missing = []
        for ref in sorted(set(_IMAGE_REF_RE.findall(self.text))):
            if not (REPO_ROOT / ref).exists():
                missing.append(ref)
        self.assertEqual(
            missing, [],
            msg=f"ev-models-template.html references images missing from images/: {missing}",
        )


class TestCanonicalUrl(_TemplateMixin, unittest.TestCase):
    def test_canonical_and_og_url_point_at_this_page(self) -> None:
        self.assertIn('<link rel="canonical" href="{{SITE_URL}}ev-models.html">', self.text)
        self.assertIn('<meta property="og:url" content="{{SITE_URL}}ev-models.html">', self.text)


class TestBuildOutput(unittest.TestCase):
    """Run the real build.py and inspect the generated ev-models.html."""

    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "build.py")],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "build.py failed:\n" + result.stdout + result.stderr
            )
        cls.html = OUTPUT_PATH.read_text(encoding="utf-8")

    def test_output_file_was_generated(self) -> None:
        self.assertTrue(OUTPUT_PATH.exists())

    def test_no_unreplaced_tokens(self) -> None:
        self.assertNotIn("{{", self.html)
        self.assertNotIn("}}", self.html)

    def test_closing_html_tag_present(self) -> None:
        self.assertIn("</html>", self.html)

    def test_json_ld_is_valid(self) -> None:
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            self.html, re.DOTALL,
        )
        self.assertGreater(len(blocks), 0, msg="No JSON-LD block found in ev-models.html.")
        for block in blocks:
            json.loads(block)  # Raises on invalid JSON.


if __name__ == "__main__":
    unittest.main()
