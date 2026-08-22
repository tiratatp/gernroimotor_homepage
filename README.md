# ร้านมอเตอร์ไซค์ — เว็บไซต์หน้าร้าน (หน้าเดียว)

เว็บไซต์หน้าร้านมอเตอร์ไซค์ 1 หน้า ภาษาไทย เอาไว้ใช้กับ Google Maps และโฆษณา
โฮสต์ฟรีบน GitHub Pages พร้อมใช้โดเมนเฉพาะของร้านได้

**กฎทอง: แก้ทุกอย่างผ่านเว็บไซต์ GitHub (github.com) ไม่ต้องติดตั้งโปรแกรมอะไรเลย**
Golden rule: edit everything through the GitHub website — no software to install.

---

## สำหรับผู้ดูแลร้าน (คนที่ไม่ได้เขียนโค้ด)

เว็บนี้มีไฟล์สำคัญ 2 ไฟล์ที่คุณต้องแก้:
- **`variables.txt`** — ข้อมูลร้านที่ใช้ซ้ำหลายที่ (ชื่อร้าน เบอร์โทร ที่อยู่ LINE Facebook TikTok โดเมน)
- **`template.html`** — ข้อความทั่วไปและรูปภาพบนหน้าเว็บ

ระบบ GitHub จะสร้างไฟล์ `index.html` (เว็บจริง) จาก 2 ไฟล์นี้ให้อัตโนมัติทุกครั้งที่บันทึก

### แก้ไขที่ 1: เปลี่ยนข้อมูลร้าน (ชื่อร้าน/เบอร์โทร/ที่อยู่/LINE/Facebook/TikTok/โดเมน)

1. เปิดไฟล์ `variables.txt` บน GitHub (คลิกชื่อไฟล์)
2. คลิกปุ่มดินสอ (Edit) มุมขวาบน
3. แก้เฉพาะ **ข้อความทางขวาของเครื่องหมาย `=`** เท่านั้น
4. กด **Commit changes**

> **คำเตือนสำคัญ: แก้เฉพาะทางขวาของเครื่องหมาย `=` เท่านั้น ห้ามแตะชื่อทางซ้าย**
> ถ้าลบหรือเปลี่ยนชื่อทางซ้าย เว็บจะสร้างไม่ได้

**ตัวอย่าง:**
```
ก่อนแก้:  PHONE_DISPLAY = 02-000-0000
หลังแก้:  PHONE_DISPLAY = 089-123-4567
```

**ตารางตัวแปรทั้งหมด (9 ตัว):**

| ชื่อตัวแปร | คำอธิบาย |
|-----------|----------|
| `SHOP_NAME` | ชื่อร้าน (แสดงบนหน้าเว็บ แท็บเบราว์เซอร์ และข้อมูล Google) |
| `PHONE_DISPLAY` | เบอร์โทรแบบมีขีด สำหรับแสดงบนหน้าเว็บ (เช่น 089-123-4567) |
| `PHONE_TEL` | เบอร์โทรแบบตัวเลขล้วน ไม่มีขีด สำหรับปุ่มกดโทร (เช่น 0891234567) |
| `ADDRESS` | ที่อยู่: เลขที่ ถนน แขวง เขต (ไม่ต้องใส่ กรุงเทพมหานคร และรหัสไปรษณีย์ ระบบใส่ให้เอง) |
| `POSTAL_CODE` | รหัสไปรษณีย์ 5 หลัก |
| `LINE_ID` | LINE ID ของร้าน (ไม่ต้องใส่ @ ข้างหน้า) |
| `FACEBOOK_PAGE` | ชื่อเพจ Facebook (ส่วนท้ายของลิงก์ เช่น facebook.com/ชื่อเพจ) |
| `TIKTOK_USER` | ชื่อบัญชี TikTok ไม่ต้องใส่เครื่องหมาย @ |
| `SITE_URL` | โดเมนจริงของเว็บ (ต้องขึ้นต้นด้วย `https://` และลงท้ายด้วย `/`) |

### แก้ไขที่ 2: เปลี่ยนข้อความทั่วไปหรือรูปภาพ

1. เปิดไฟล์ `template.html` บน GitHub
2. คลิกปุ่มดินสอ (Edit)
3. กด `Ctrl+F` (หรือ `Cmd+F`) แล้วค้นหาคำว่า **`EDIT ME`** หรือ **`แก้ไขตรงนี้`**
4. แก้ข้อความที่ต้องการ
5. กด **Commit changes**

**วิธีเปลี่ยนรูปภาพ:**

1. เตรียมรูปภาพของร้าน (ถ่ายด้วยมือถือก็ได้ แนะนำขนาดไม่เกิน 1 MB)
2. บน GitHub คลิก **Add file → Upload files**
3. สร้างโฟลเดอร์ `images` โดยพิมพ์ `images/` ในช่องชื่อไฟล์ แล้วอัปโหลดรูปเข้าไป
   (เช่น อัปโหลดไฟล์ชื่อ `shop-front.jpg` → จะได้พาธ `images/shop-front.jpg`)
4. เปิด `template.html` แล้วค้นหาคำว่า **`SWAP IMAGE`** หรือ **`เปลี่ยนรูปตรงนี้`**
5. เปลี่ยน URL จาก `https://placehold.co/...` เป็น `images/ชื่อรูปของคุณ.jpg`
6. กด **Commit changes**

> รูปทุกรูปในเว็บตอนนี้เป็นรูปจำลอง (placeholder) ที่ใช้งานได้ทันที
> แต่ควรเปลี่ยนเป็นรูปจริงของร้านก่อนเปิดใช้งาน

### แก้ไขที่ 3: เพิ่มการ์ดบริการ รูปในแกลเลอรี หรือยี่ห้อรถ

1. ใน `template.html` ค้นหาคำว่า **`COPY FROM HERE`** หรือ **`คัดลอกตั้งแต่ตรงนี้`**
2. คัดลอกทุกอย่างตั้งแต่บรรทัด `COPY FROM HERE` จนถึงบรรทัด `TO HERE` / `ถึงตรงนี้`
3. วางต่อจากบล็อกเดิม (ในตำแหน่งเดียวกัน)
4. แก้ข้อความในบล็อกใหม่
5. กด **Commit changes**

> ใช้วิธีนี้เพื่อ: เพิ่มการ์ดบริการใหม่, เพิ่มรูปในแกลเลอรี, เพิ่มวันเปิดทำการ,
> เพิ่มย่อหน้าเกี่ยวกับเรา, เพิ่มช่องทางติดต่อ, เพิ่มยี่ห้อรถ (คัดลอก `<li class="chip">` ในส่วนยี่ห้อ)

---

## ตอนบันทึกแล้วเกิดอะไรขึ้น

ทุกครั้งที่กด **Commit changes** GitHub จะสร้างเว็บและตรวจสอบอัตโนมัติ (ดูได้ที่แท็บ **Actions**):

- **เครื่องหมายเช็คเขียว (✓)** = เว็บอัปเดตภายใน 1-2 นาที
- **เครื่องหมาย X สีแดง** = เว็บเดิมยังออนไลน์อยู่ ไม่มีอะไรพัง — ระบบจะไม่เผยแพร่เว็บที่เสีย

---

## ถ้าเว็บไม่อัปเดต / มีเครื่องหมาย X สีแดง

ถ้าแก้ไฟล์แล้วเว็บไม่อัปเดต หรือเห็นเครื่องหมาย X สีแดงที่แท็บ Actions แปลว่าการแก้ไขทำให้ไฟล์เสีย:

1. เข้า GitHub → คลิกแท็บ **Actions** (ด้านบนของหน้า repo)
2. คลิกการรันที่มีเครื่องหมาย X สีแดง (failed run)
3. ดูว่า step ไหนที่ fail แล้วแก้ตาม:

**ถ้า "Build website from template" fail:**
- ไฟล์ `variables.txt` มีปัญหา — log จะบอกเป็นภาษาไทยว่าผิดตรงไหน
- เช่น: ขาดเครื่องหมาย `=`, ค่าว่างเปล่า, ชื่อตัวแปรซ้ำกัน
- แก้: กลับไปแก้ `variables.txt` ให้ถูกต้อง

**ถ้า "Validate HTML structure" fail:**
- แท็กใน `template.html` ขาดหรือเสีย — log จะบอกเลขบรรทัดที่มีปัญหา
- แก้ที่ปลอดภัยที่สุด: ยกเลิกการแก้ไขครั้งล่าสุด (undo / revert)

**ถ้า step ที่ขึ้นต้นด้วย "Check ..." fail:**
- อาจลบคำว่า `EDIT ME` หรือบล็อก `<style>` ไปโดยไม่ได้ตั้งใจ
- แก้: คืนค่าส่วนที่ลบไปกลับมา

**ทางออกสุดท้าย:** ถ้าแก้ไม่ได้ ให้เอา repo ทั้งหมดพร้อม README นี้ ให้นักพัฒนาหรือ AI agent ช่วยแก้

---

## ห้ามแตะ (อันตราย)

- **`index.html`** — ไฟล์นี้ถูกสร้างอัตโนมัติจาก `template.html` + `variables.txt` แก้แล้วจะถูกเขียนทับทุกครั้ง
- **`build.py`** — โปรแกรมสร้างเว็บ ห้ามแก้เด็ดขาด
- **`.github/`** — ระบบตรวจสอบและเผยแพร่อัตโนมัติ ห้ามแก้
- **`.htmlvalidate.json`** — ไฟล์ตั้งค่าการตรวจสอบ HTML ห้ามแก้

---

## FOR AI AGENTS

### File map

| File | Role |
|------|------|
| `template.html` | **Source of truth** — the website template with `{{TOKEN}}` placeholders. Edit text/images/structure here. |
| `variables.txt` | **Single source for repeated facts** — shop name, phone, address, LINE, Facebook, TikTok, domain. The ONE file the caretaker edits for shop info. |
| `build.py` | **Stdlib-only builder** (no pip deps) — substitutes `{{TOKENS}}` from variables.txt into template.html, writes index.html. Bilingual error messages. |
| `index.html` | **Generated output** — listed in `.gitignore`, never edit directly. Always regenerated by `python3 build.py`. |
| `.github/workflows/pages.yml` | **CI/CD** — validate job (build + html-validate + sentinel greps) then deploy job (needs: validate, main only). |
| `.htmlvalidate.json` | **Validator config** — extends html-validate:recommended, cosmetic rules off. |
| `DESIGN.md` | **Design tokens** — palette, type scale, spacing, section anatomy. Read before any visual change. |

### Editing conventions

- **EDIT ME markers**: every editable text region has `<!-- EDIT ME / แก้ไขตรงนี้: ... -->` above it.
- **COPY FROM HERE / TO HERE fences**: every repeating block (service card, gallery figure, hours row, contact card, brand chip) is wrapped in bilingual `<!-- COPY FROM HERE / คัดลอกตั้งแต่ตรงนี้ -->` ... `<!-- TO HERE / ถึงตรงนี้ -->`. These are the maintainer's copy-paste units — never break them.
- **Bilingual comments are the product.** Do not strip comments to make the code "cleaner" — the comments ARE the interface for non-technical maintainers.
- **`{{TOKEN}}` placeholders** in template.html are replaced by build.py from variables.txt. Never hardcode shop facts in template.html — use tokens.

### How to add a new variable

1. Put `{{NEW_TOKEN}}` in `template.html` where the value should appear.
2. Add `NEW_TOKEN = value` in `variables.txt` (uppercase A-Z and _ only, non-empty).
3. `build.py` validates automatically — if the token is missing from variables.txt, the build fails with a clear message.

### After any template edit

Run `python3 build.py` and confirm:
- It prints `OK`
- `grep -c "{{" index.html` returns `0` (no unreplaced tokens)

### Local QA

```bash
python3 build.py
open index.html   # macOS, or just double-click the file
```

### GitHub Pages deployment model

The site is deployed via the GitHub Actions workflow (`.github/workflows/pages.yml`), NOT via "Deploy from branch". The workflow:
1. **validate** job: `python3 build.py` → `html-validate` on index.html → sentinel greps on template.html/index.html.
2. **deploy** job (only on `main`, only if validate passed): `configure-pages` → `upload-pages-artifact` (path=.) → `deploy-pages`.

GitHub repo Settings → Pages → Source must be set to **GitHub Actions** (not "Deploy from branch").

---

## Deployment (step-by-step)

### First-time setup (3 bullets)

1. Push all files to the `main` branch of a GitHub repository.
2. Go to **Settings → Pages → Source** and select **GitHub Actions** (NOT "Deploy from branch").
3. The workflow runs automatically on every push to `main`; after the first green check, the site is live at `https://<username>.github.io/<repo>/`.

### Custom domain (โดเมนของตัวเอง)

1. **ตั้งค่า SITE_URL** ใน `variables.txt` เป็นโดเมนจริงของร้าน (เช่น `https://www.yourshop.com/`)
2. **สร้างไฟล์ CNAME** ใน repo ชื่อไฟล์ `CNAME` (ไม่มีนามสกุล) บรรจุโดเมนเดียวบรรทัดเดียว:
   ```
   www.yourshop.com
   ```
   > ห้ามใส่โดเมนจำลอง — ต้องเป็นโดเมนจริง ไม่งั้นลิงกก์ github.io เริ่มต้นจะพัง
3. **ตั้งค่า DNS** ที่ผู้ให้บริการโดเมน:

   **สำหรับโดเมนหลัก** (เช่น `yourshop.com`) ให้เพิ่ม A records ชี้ไปที่ IP ของ GitHub Pages:

   | Type | Host | Value |
   |------|------|-------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |

   **สำหรับ www** (เช่น `www.yourshop.com`) ให้เพิ่ม CNAME record:

   | Type | Host | Value |
   |------|------|-------|
   | CNAME | `www` | `<username>.github.io` |

   > แทนที่ `<username>` ด้วยชื่อผู้ใช้/องค์กร GitHub ของคุณ

4. **เปิด Enforce HTTPS**: ไปที่ **Settings → Pages** → ใส่โดเมนในช่อง Custom domain → กด **Save** → รอ DNS แพร่กระจาย (ไม่กี่นาทีถึงหลายชั่วโมง) → ติ๊ก **Enforce HTTPS**

> การเปลี่ยนแปลง DNS อาจใช้เวลาตั้งแต่ไม่กี่นาทีถึงหลายชั่วโมง

---

## Pre-publish checklist (ตรวจสอบก่อนเปิดใช้งาน)

ก่อนเปิดเว็บจริง ให้ทำตามนี้:

- [ ] แก้ค่าทั้ง 9 ตัวใน `variables.txt` ให้เป็นข้อมูลจริงของร้าน
- [ ] แก้ข้อความและรูปภาพใน `template.html` (ค้นหา `EDIT ME` และ `SWAP IMAGE`)
- [ ] แก้รายชื่อยี่ห้อใน `template.html` ให้ตรงกับของจริงในร้าน
- [ ] กด Commit changes แล้วรอเครื่องหมายเช็คเขียว (✓) ที่แท็บ Actions
- [ ] เปิดเว็บบน **โทรศัพท์มือถือ** (ผู้ใช้ 80%+ มาจากมือถือผ่าน Google Maps)
- [ ] ทดสอบปุ่ม **นำทางไปร้าน** — ต้องเปิด Google Maps
- [ ] ทดสอบปุ่ม **โทรเลย** — ต้องเปิดหน้าโทรศัพท์
- [ ] ทดสอบปุ่ม **เพิ่มเพื่อน LINE** — ต้องเปิด LINE
- [ ] ทดสอบลิงก์ **Facebook** และ **TikTok** — ต้องเปิดถูกเพจ/บัญชี
- [ ] ส่ง URL เว็บไปที่ **Google Search Console** (search.google.com/search-console)
- [ ] อัปเดต **Google Business Profile** ให้ใส่ URL เว็บ (business.google.com)
