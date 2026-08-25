#!/usr/bin/env python3
# build.py - generate index.html from template.html and variables.txt.
# Builds index.html by replacing {{TOKENS}} in template.html with variables.txt values.
# Also generates robots.txt and sitemap.xml from SITE_URL.
# GitHub Actions runs this automatically (see .github/workflows/pages.yml).
# Maintainers do NOT need to run this file. Developers: python3 build.py (stdlib only)
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def fail(th, en):
    """Print a bilingual error and stop the build (exit code 1)."""
    print("ERROR / ข้อผิดพลาด: " + th)
    print("(" + en + ")")
    sys.exit(1)


# Allowed formats for fields that have a specific shape. Anchored (full-match)
# so a partial match cannot pass. The check below is the only enforcement.
PHONE_DISPLAY_RE = re.compile(r"0\d{2}-\d{3}-\d{4}")   # 0XX-XXX-XXXX
PHONE_TEL_RE = re.compile(r"0\d{9}")                   # 0 + 9 digits = 10 digits
PHONE_TEL_INTL_RE = re.compile(r"\+66\d{9}")           # +66 + 9 digits
POSTAL_CODE_RE = re.compile(r"\d{5}")                  # exactly 5 digits
# letters/digits/dot/underscore/hyphen — naturally rejects @, whitespace,
# slash, hash, quotes, and markup delimiters while allowing the current
# TikTok dot (e.g. "100motor.bkk").
SOCIAL_RE = re.compile(r"[A-Za-z0-9._-]+")


def validate_value(key, value):
    """Validate known boundary fields. fail() on the first violation."""
    if key == "SITE_URL":
        parts = urlsplit(value)
        if parts.scheme != "https":
            fail(f"SITE_URL '{value}' ต้องใช้ https (ไม่ใช่ http)",
                 f"SITE_URL '{value}' must use https (not http)")
        if not parts.netloc:
            fail(f"SITE_URL '{value}' ไม่มี host",
                 f"SITE_URL '{value}' has no host")
        if parts.query:
            fail(f"SITE_URL '{value}' ต้องไม่มี query string",
                 f"SITE_URL '{value}' must not contain a query string")
        if parts.fragment:
            fail(f"SITE_URL '{value}' ต้องไม่มี fragment",
                 f"SITE_URL '{value}' must not contain a fragment")
        if not value.endswith("/"):
            fail(f"SITE_URL '{value}' ต้องลงท้ายด้วย /",
                 f"SITE_URL '{value}' must end with /")
    elif key in ("PHONE_DISPLAY", "PHONE_BACKUP_DISPLAY"):
        if not PHONE_DISPLAY_RE.fullmatch(value):
            fail(f"{key} '{value}' ต้องอยู่ในรูปแบบ 0XX-XXX-XXXX",
                 f"{key} '{value}' must match format 0XX-XXX-XXXX")
    elif key in ("PHONE_TEL", "PHONE_BACKUP_TEL"):
        if not PHONE_TEL_RE.fullmatch(value):
            fail(f"{key} '{value}' ต้องเป็นตัวเลข 10 หลักขึ้นต้นด้วย 0",
                 f"{key} '{value}' must be 10 digits starting with 0")
    elif key == "PHONE_TEL_INTL":
        if not PHONE_TEL_INTL_RE.fullmatch(value):
            fail(f"PHONE_TEL_INTL '{value}' ต้องขึ้นต้นด้วย +66 แล้วตามด้วยตัวเลข 9 หลัก",
                 f"PHONE_TEL_INTL '{value}' must be +66 followed by 9 digits")
    elif key == "POSTAL_CODE":
        if not POSTAL_CODE_RE.fullmatch(value):
            fail(f"POSTAL_CODE '{value}' ต้องเป็นตัวเลข 5 หลัก",
                 f"POSTAL_CODE '{value}' must be exactly 5 digits")
    elif key in ("LINE_ID", "FACEBOOK_PAGE", "TIKTOK_USER"):
        if not SOCIAL_RE.fullmatch(value):
            fail(f"{key} '{value}' ต้องประกอบด้วยตัวอักษร ตัวเลข . _ - เท่านั้น",
                 f"{key} '{value}' must contain only letters, digits, . _ -")
    elif key == "MAPS_EMBED_URL":
        if not value.startswith("https://www.google.com/maps/embed?pb="):
            fail(f"MAPS_EMBED_URL ต้องเป็น URL ฝังแผนที่จาก Google Maps "
                 f"(เริ่มต้นด้วย https://www.google.com/maps/embed?pb=)",
                 f"MAPS_EMBED_URL must be a Google Maps embed URL "
                 f"(starting with https://www.google.com/maps/embed?pb=)")
    elif key == "BUSINESS_PROFILE_URL":
        parts = urlsplit(value)
        if parts.scheme != "https":
            fail(f"BUSINESS_PROFILE_URL '{value}' ต้องใช้ https (ไม่ใช่ http)",
                 f"BUSINESS_PROFILE_URL '{value}' must use https (not http)")
        if not parts.netloc:
            fail(f"BUSINESS_PROFILE_URL '{value}' ไม่มี host",
                 f"BUSINESS_PROFILE_URL '{value}' has no host")


def main():
    vars_file = ROOT / "variables.txt"
    template_file = ROOT / "template.html"
    output_file = ROOT / "index.html"
    if not vars_file.exists():
        fail("ไม่พบไฟล์ variables.txt", "variables.txt not found")
    if not template_file.exists():
        fail("ไม่พบไฟล์ template.html", "template.html not found")

    # 1. Read variables.txt.
    variables = {}
    for lineno, raw in enumerate(vars_file.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue  # Comment or blank line.
        if "=" not in line:
            fail(f"variables.txt บรรทัดที่ {lineno}: ไม่มีเครื่องหมาย =",
                 f"variables.txt line {lineno}: missing '=' sign")
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not re.fullmatch(r"[A-Z_]+", key):
            fail(f"ชื่อตัวแปร '{key}' ผิดรูปแบบ (ต้องเป็น A-Z และ _ เท่านั้น)",
                 f"bad variable name '{key}' (UPPERCASE A-Z and _ only)")
        if not value:
            fail(f"ตัวแปร {key} ไม่มีค่า (ว่างเปล่า)", f"variable {key} is empty")
        if key in variables:
            fail(f"ตัวแปร {key} ถูกเขียนซ้ำสองครั้ง", f"variable {key} defined twice")
        variables[key] = value

    # 2. Read the template.
    html = template_file.read_text(encoding="utf-8")

    # 2a. Validate template placeholders.
    #     A complete {{...}} block whose body is not [A-Z_]+ is malformed.
    #     Any leftover {{ or }} (no matching pair) is also malformed and would
    #     ship to the live site if we silently let it pass.
    for match in re.finditer(r"\{\{([^{}]*)\}\}", html):
        body = match.group(1)
        if not re.fullmatch(r"[A-Z_]+", body):
            fail(f"template.html มี placeholder '{{{{{body}}}}}' ผิดรูปแบบ (ต้องเป็น A-Z และ _ เท่านั้น)",
                 f"template.html has malformed placeholder '{{{{{body}}}}}' (UPPERCASE A-Z and _ only)")
    leftover = re.sub(r"\{\{[A-Z_]+\}\}", "", html)
    if "{{" in leftover or "}}" in leftover:
        fail("template.html มี {{ หรือ }} ที่ไม่ตรงกัน",
             "template.html has unmatched {{ or }}")

    # 2b. Validate known boundary values.
    for key, value in variables.items():
        validate_value(key, value)

    # 3. Every {{TOKEN}} in the template must exist in variables.txt.
    used = set(re.findall(r"\{\{([A-Z_]+)\}\}", html))
    missing = sorted(used - variables.keys())
    if missing:
        fail("template.html ใช้ตัวแปรที่ไม่มีใน variables.txt: " + ", ".join(missing),
             "template.html uses tokens not defined in variables.txt: " + ", ".join(missing))
    for key in sorted(variables.keys() - used):
        print("NOTE / หมายเหตุ: ตัวแปร " + key + " ไม่ได้ถูกใช้ใน template.html (not used)")

    # 4. Replace tokens and write the output.
    for key, value in variables.items():
        html = html.replace("{{" + key + "}}", value)
    output_file.write_text(html, encoding="utf-8")

    # 5. Generate robots.txt and sitemap.xml from SITE_URL.
    site_url = variables["SITE_URL"]  # guaranteed present: template.html uses it
    (ROOT / "robots.txt").write_text(
        "# This file is auto-generated by build.py — do not edit directly.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: " + site_url + "sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- auto-generated by build.py — do not edit directly -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url><loc>" + site_url + "</loc></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print("OK: สร้าง index.html + robots.txt + sitemap.xml เรียบร้อย (built successfully)")


if __name__ == "__main__":
    main()
