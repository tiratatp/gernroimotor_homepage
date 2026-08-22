"""Black-box CLI tests for build.py admin-input policy.

CLI boundary only (sys.executable invocation, no import). build.py is copied
into a per-test temp dir so ROOT = Path(__file__).parent resolves locally;
fixtures are minimal and deterministic. All cases must pass before deployment.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_PY_SRC = REPO_ROOT / "build.py"

REQUIRED_TOKENS: tuple[str, ...] = (
    "SHOP_NAME", "PHONE_DISPLAY", "PHONE_TEL", "PHONE_TEL_INTL",
    "PHONE_BACKUP_DISPLAY", "PHONE_BACKUP_TEL",
    "ADDRESS", "POSTAL_CODE", "LINE_ID", "FACEBOOK_PAGE",
    "TIKTOK_USER", "SITE_URL",
)

BILINGUAL_ERROR_MARKER = "ERROR / ข้อผิดพลาด:"


def _valid_variables_block() -> str:
    return textwrap.dedent("""\
        SHOP_NAME = เกินร้อยมอเตอร์
        PHONE_DISPLAY = 096-142-6542
        PHONE_TEL = 0961426542
        PHONE_TEL_INTL = +66961426542
        PHONE_BACKUP_DISPLAY = 094-595-9624
        PHONE_BACKUP_TEL = 0945959624
        ADDRESS = 545 ซอยโชคชัย 4
        POSTAL_CODE = 10230
        LINE_ID = 485txeto
        FACEBOOK_PAGE = gernroimotor
        TIKTOK_USER = 100motor.bkk
        SITE_URL = https://example.com/
        """)


def _minimal_template(extra: tuple[str, ...] = ()) -> str:
    body = "".join(f"{{{{{n}}}}}" for n in REQUIRED_TOKENS + extra)
    return f"<html><body>{body}</body></html>\n"


class _BuildHarness(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name)
        self.build_py = self.workspace / "build.py"
        shutil.copyfile(BUILD_PY_SRC, self.build_py)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_build(
        self, variables_text: str, template_text: str,
    ) -> subprocess.CompletedProcess[str]:
        (self.workspace / "variables.txt").write_text(variables_text, encoding="utf-8")
        (self.workspace / "template.html").write_text(template_text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(self.build_py)],
            cwd=self.workspace, capture_output=True, text=True, timeout=15,
        )

    def with_var(self, var: str, value: str) -> str:
        lines = _valid_variables_block().splitlines()
        prefix = f"{var} = "
        for i, line in enumerate(lines):
            if line.startswith(prefix):
                lines[i] = f"{prefix}{value}"
                break
        return "\n".join(lines) + "\n"

    def assertRejected(
        self,
        result: subprocess.CompletedProcess[str],
        *,
        marker: str,
        label: str,
    ) -> None:
        combined = result.stdout + result.stderr
        with self.subTest(case=label):
            self.assertNotEqual(
                result.returncode, 0,
                msg=f"build.py accepted invalid input (exit 0)\nstdout={result.stdout!r}\nstderr={result.stderr!r}",
            )
            self.assertIn(
                marker, combined,
                msg=f"build.py failed but did not mention {marker!r}\nstdout={result.stdout!r}\nstderr={result.stderr!r}",
            )


# Given: 12 policy-valid variables + template referencing all of them.
# When: build.py runs. Then: exits 0 and prints OK — harness is wired right.
class TestValidBuildHarness(_BuildHarness):
    def test_valid_fixtures_build_successfully(self) -> None:
        result = self.run_build(_valid_variables_block(), _minimal_template())
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)


# Given/When/Then: a malformed placeholder must be rejected with the bilingual error.
class TestMalformedPlaceholder(_BuildHarness):
    def test_lowercase_placeholder_is_rejected(self) -> None:
        result = self.run_build(
            _valid_variables_block(), _minimal_template(("lowercase",)),
        )
        self.assertRejected(result, marker=BILINGUAL_ERROR_MARKER, label="lowercase_token")


# Given/When/Then: each malformed SITE_URL must be rejected; error names SITE_URL.
class TestSiteUrlPolicy(_BuildHarness):
    def test_invalid_site_urls_are_rejected(self) -> None:
        for label, bad in (
            ("http_not_https", "http://example.com/"),
            ("missing_host", "https:///"),
            ("missing_trailing_slash", "https://example.com"),
            ("contains_query_string", "https://example.com/?utm=fallback"),
            ("contains_fragment", "https://example.com/#contact"),
        ):
            with self.subTest(case=label):
                result = self.run_build(
                    self.with_var("SITE_URL", bad), _minimal_template(),
                )
                self.assertRejected(result, marker="SITE_URL", label=label)


# Given/When/Then: each malformed phone must be rejected; error names the variable.
class TestPhoneFormatPolicy(_BuildHarness):
    def test_invalid_phone_formats_are_rejected(self) -> None:
        for label, var, bad in (
            ("display_missing_dashes", "PHONE_DISPLAY", "0961426542"),
            ("tel_contains_dashes", "PHONE_TEL", "096-142-6542"),
            ("intl_missing_country_code", "PHONE_TEL_INTL", "0961426542"),
            ("intl_wrong_country_code", "PHONE_TEL_INTL", "+1234567890"),
            ("backup_display_missing_dashes", "PHONE_BACKUP_DISPLAY", "0945959624"),
            ("backup_tel_contains_dashes", "PHONE_BACKUP_TEL", "094-595-9624"),
        ):
            with self.subTest(case=label):
                result = self.run_build(
                    self.with_var(var, bad), _minimal_template(),
                )
                self.assertRejected(result, marker=var, label=label)


# Given/When/Then: POSTAL_CODE must be 5 digits; everything else is rejected.
class TestPostalCodePolicy(_BuildHarness):
    def test_invalid_postal_codes_are_rejected(self) -> None:
        for label, bad in (
            ("four_digits", "1023"),
            ("contains_letter", "1023a"),
        ):
            with self.subTest(case=label):
                result = self.run_build(
                    self.with_var("POSTAL_CODE", bad), _minimal_template(),
                )
                self.assertRejected(result, marker="POSTAL_CODE", label=label)


# Given/When/Then: social IDs must avoid leading '@', whitespace, slashes, '#'.
class TestSocialIdentifierPolicy(_BuildHarness):
    def test_invalid_social_identifiers_are_rejected(self) -> None:
        for label, var, bad in (
            ("line_id_leading_at", "LINE_ID", "@485txeto"),
            ("line_id_contains_whitespace", "LINE_ID", "485 txeto"),
            ("facebook_page_contains_slash", "FACEBOOK_PAGE", "gern/roimotor"),
            ("tiktok_user_contains_hash", "TIKTOK_USER", "100motor#bkk"),
            ("tiktok_user_leading_at", "TIKTOK_USER", "@100motor.bkk"),
        ):
            with self.subTest(case=label):
                result = self.run_build(
                    self.with_var(var, bad), _minimal_template(),
                )
                self.assertRejected(result, marker=var, label=label)


if __name__ == "__main__":
    unittest.main()
