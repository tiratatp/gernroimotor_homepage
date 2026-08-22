#!/usr/bin/env python3
# build.py - สร้าง index.html จาก template.html + variables.txt
# Builds index.html by replacing {{TOKENS}} in template.html with variables.txt values.
# GitHub Actions runs this automatically (see .github/workflows/pages.yml).
# Maintainers do NOT need to run this file. Developers: python3 build.py (stdlib only)
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent


def fail(th, en):
    """Print a bilingual error and stop the build (exit code 1)."""
    print("ERROR / ข้อผิดพลาด: " + th)
    print("(" + en + ")")
    sys.exit(1)


def main():
    vars_file = ROOT / "variables.txt"
    template_file = ROOT / "template.html"
    output_file = ROOT / "index.html"
    if not vars_file.exists():
        fail("ไม่พบไฟล์ variables.txt", "variables.txt not found")
    if not template_file.exists():
        fail("ไม่พบไฟล์ template.html", "template.html not found")

    # 1. Read variables.txt / อ่านไฟล์ตัวแปร
    variables = {}
    for lineno, raw in enumerate(vars_file.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue  # comment or blank line / บรรทัดคอมเมนต์หรือบรรทัดว่าง
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

    # 2. Read template / อ่านแม่แบบ
    html = template_file.read_text(encoding="utf-8")

    # 3. Every {{TOKEN}} in the template must exist in variables.txt
    #    ทุกตัวแปรใน template ต้องมีค่าใน variables.txt
    used = set(re.findall(r"\{\{([A-Z_]+)\}\}", html))
    missing = sorted(used - variables.keys())
    if missing:
        fail("template.html ใช้ตัวแปรที่ไม่มีใน variables.txt: " + ", ".join(missing),
             "template.html uses tokens not defined in variables.txt: " + ", ".join(missing))
    for key in sorted(variables.keys() - used):
        print("NOTE / หมายเหตุ: ตัวแปร " + key + " ไม่ได้ถูกใช้ใน template.html (not used)")

    # 4. Replace and write output / แทนที่แล้วเขียนไฟล์ผลลัพธ์
    for key, value in variables.items():
        html = html.replace("{{" + key + "}}", value)
    output_file.write_text(html, encoding="utf-8")
    print("OK: สร้าง index.html เรียบร้อย (built index.html successfully)")


if __name__ == "__main__":
    main()
