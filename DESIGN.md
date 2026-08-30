# เกินร้อยมอเตอร์ Design System

## 1. Atmosphere & Identity

หน้าเว็บให้ความรู้สึกตรงไปตรงมา น่าเชื่อถือ และเข้าถึงง่ายแบบร้านมอเตอร์ไซค์ในชุมชน เนื้อหาภาษาไทยอ่านสบายบนมือถือและพาผู้ใช้ไปสู่การโทร แชต LINE หรือเดินทางมาร้านได้เร็ว ลายเซ็นของระบบคือสีแดง racing red เพียงสีเดียวบนพื้นขาว/เทา สลับกับภาพหน้าร้านจริงและพื้นผิวการ์ดที่เรียบแข็งแรง ไม่ตกแต่งเกินหน้าที่

## 2. Color

### Palette

| Role | Token | Value | Usage |
|---|---|---|---|
| Accent/primary | `--color-primary` | `#CF0000` | ปุ่มหลัก ลิงก์ ไอคอน จุดเน้น และ focus ring |
| Accent/hover | `--color-primary-dark` | `#A60000` | hover ของปุ่มหลัก |
| Text/primary | `--color-text` | `#1A1A1A` | ข้อความหลัก หัวข้อ และพื้น footer |
| Text/secondary | `--color-text-muted` | `#5A5A5A` | คำอธิบาย ที่อยู่ และข้อมูลรอง |
| Surface/page | `--color-bg` | `#FFFFFF` | พื้นหน้าและพื้น hero |
| Surface/card | `--color-surface` | `#F6F6F6` | การ์ดและกล่องช่องทางติดต่อ |
| Surface/alternate | `--color-surface-alt` | `#EFEFEF` | พื้น section สลับและข้อความ footer |
| Border/default | `--color-border` | `#E0E0E0` | เส้นคั่น ขอบการ์ด และขอบเมนู |
| Text/on-accent | `--color-white` | `#FFFFFF` | ข้อความบนปุ่มแดงและแถบ header แดง |

### Rules

- `--color-primary` เป็น accent เพียงสีเดียว ห้ามเพิ่ม secondary accent หรือสีแบรนด์ของช่องทาง social.
- **ข้อยกเว้นสำหรับสีแบรนด์ LINE:** ปุ่ม LINE ใช้สีเขียวทางการ `--color-line: #06C755` เป็น token เดียวที่แยกจาก accent หลัก ใช้ได้เฉพาะกับ `.line-cta` เท่านั้น ห้ามนำไปใช้กับองค์ประกอบอื่น เพื่อคงหลักการ single-accent ไว้ ค่าสีนี้มาจากคู่มือแบรนด์ LINE จึงห้ามแก้.
- สีพื้น section สลับด้วย `main > section:nth-of-type(even)` เท่านั้น ห้ามใส่ background class ราย section.
- สีทั้งหมดที่ผู้ดูแลแก้ได้อยู่ใน `:root` ส่วน `CHANGE COLORS HERE`; ต้องเก็บ token เดิมครบทุกตัว.

## 3. Typography

### Font Stack

- Kanit โหลดตัวเอียงน้ำหนัก 600 ไว้ด้วย (`ital,wght@0,600;0,700;1,600`) สำหรับคำถาม FAQ จึงเป็นตัวเอียงจริงของฟอนต์ ไม่ใช่การเอียงจำลองของเบราว์เซอร์.
- Body: `--font-body` = `"Sarabun", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif`.
- Heading: `--font-heading` = `"Kanit", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif`.
- ไม่มี mono หรือ serif font.
- น้ำหนักที่โหลดและใช้: Kanit 600, 700; Sarabun 400, 500, 600, 700.

### Scale

| Level | Mobile | Desktop (≥768px) | Weight / line-height | Usage |
|---|---|---|---|---|
| Hero display | `clamp(2.1rem, 9.5vw, 3rem)` | `3rem` | 700 / 1.3 | ชื่อร้านใน hero (ชื่อร้าน `1.12em` / ชื่อสาขา `0.82em`) |
| Section title | `1.95rem` | `2.4rem` | 700 / body rhythm | หัวข้อ `<h2>` — ค่ามือถือถูกจำกัดที่ `1.95rem` เพราะใหญ่กว่านี้แล้ว `ยี่ห้อและรุ่นรถที่เราจำหน่าย` จะตกบรรทัดที่จอ 375px |
| Subsection | `1.3rem` | `1.3rem` | 600 | หัวข้อย่อย และบรรทัดเวลาเปิดทำการ (`.hours`) |
| Card / label title | `1.05rem`–`1.35rem` | same | 600 | `.service-card h3` = `1.35rem` (ไม่มีไอคอนแล้ว หัวข้อจึงเป็นตัวนำของการ์ด) ส่วน chip และปุ่มยังอยู่ที่ `1.05rem`–`1.15rem` |
| FAQ question | `1.25rem` | same | 600 italic | `<h3>` ในแต่ละ `.faq-item` ครอบด้วยอัญประกาศ “…” และเป็นตัวเอียง ใหญ่กว่าคำตอบชัดเจนเพื่อให้กวาดสายตาหาคำถามได้เร็ว |
| Hero lead | `1.15rem` | `1.3rem` | 400 | tagline |
| Body | `17px` | `18px` | 400 / **1.7** | เนื้อหาภาษาไทยทั้งหมด |
| Supporting | `0.85rem`–`0.95rem` | same | 400–500 | metadata แหล่งรีวิว และข้อมูลรอง |

### Rules

- หัวข้อ semantic h1–h6 ใช้ Kanit; ข้อความอื่นทั้งหมดใช้ Sarabun.
- เนื้อหาผู้ใช้เป็นภาษาไทย และ body line-height ต้องคงที่ `1.7`.
- หัวข้อใช้ลำดับ semantic ตามโครง section; ห้ามเลือก heading level จากขนาดตัวอักษร.
- ข้อความยาวจำกัดที่ 60–65ch เพื่อความอ่านง่าย; ห้ามลด body ต่ำกว่าค่าปัจจุบัน. ข้อยกเว้น: `.chip-group-intro` เป็นประโยคเดียวสั้น ๆ ไม่ใช่ย่อหน้ายาว จึงไม่จำกัดความกว้าง ปล่อยให้ container (สูงสุด `--max-width`) และขนาดจอเป็นตัวกำหนดการตัดบรรทัด.
- วลีภาษาไทยที่ห้ามหักกลางบรรทัดให้ครอบด้วย `<span class="nowrap">` (`.nowrap` = `white-space: nowrap`) แล้วเว้นวรรคระหว่าง span เป็นจุดขึ้นบรรทัดใหม่จุดเดียวที่อนุญาต.
- hero `<h1>` สองส่วนใช้ `display: block` จึงอยู่คนละบรรทัดเสมอ ทุกขนาดจอรวมถึงเดสก์ท็อป ขนาดต่างกัน: `.hero-title-name` = `1.12em` และ `.hero-title-branch` = `0.82em` อิงกับ `clamp(2.1rem, 9.5vw, 3rem)` ของ `.hero h1` จึงเลื่อนตามทุกขนาดจอโดยไม่ต้องเขียน breakpoint เพิ่ม.
- hero `<h1>` ใช้สี `--color-primary` (#CF0000) เหมือนแถบ header — คอนทราสต์บนพื้นขาว 5.75:1 ผ่าน WCAG AA.
- hero `<h1>` ใช้กติกานี้เสมอ: สองกลุ่มคือ `{{SHOP_NAME}}` และ `โชคชัย 4 แยก 63` ดังนั้นเมื่อจอแคบพอจะขึ้นสองบรรทัด จะแบ่งตรงชื่อร้าน/ชื่อสาขาเท่านั้น ไม่หักกลางวลี (หนึ่งบรรทัดตั้งแต่ ~768px ขึ้นไป, สองบรรทัดที่แคบกว่านั้น) — บังคับด้วยเทสต์ `test_h1_splits_only_between_shop_name_and_branch`.

## 4. Spacing & Layout

### Spacing Tokens

| Token | Value | Usage |
|---|---|---|
| `--space-xs` | `0.5rem` | ระยะชิด ไอคอน/label และ chip gap |
| `--space-sm` | `1rem` | gutter มือถือ ระยะในรายการ และกลุ่มปุ่ม |
| `--space-md` | `1.5rem` | padding การ์ดและ grid gap หลัก |
| `--space-lg` | `2.5rem` | ช่องว่างระหว่างกลุ่มเนื้อหา |
| `--space-xl` | `4rem` | section padding และ hero padding |

ค่ากลไกขนาดเล็กที่มีอยู่ (`0.25rem`, `0.4rem`, `0.6rem`, `0.85rem`) ใช้เฉพาะภายใน primitive เดิม เช่น nav, button และ chip; ห้ามนำไปสร้าง rhythm ใหม่.

### Geometry Tokens

| Token | Value | Usage |
|---|---|---|
| `--radius` | `12px` | การ์ด แผนที่ และรูป gallery |
| `--radius-sm` | `8px` | ปุ่ม เมนู และ touch controls |
| `--max-width` | `1100px` | container และ header content |

### Grid & Responsive Rules

- Mobile-first; breakpoint หลักมีเพียง `768px`. ที่ `768px` body และ section title โตขึ้น, container gutter เพิ่ม, nav เปลี่ยนเป็นแถว และ layout สองคอลัมน์เริ่มทำงาน.
- ไม่มี breakpoint อื่นนอกจาก `768px` แล้ว — `.contact-list` เป็นคอลัมน์เดียวทุกขนาดจอ จึงไม่ต้องใช้ breakpoint `600px` อีกต่อไป.
- `.container` กว้างไม่เกิน `--max-width`, กึ่งกลาง และใช้ gutter จาก spacing token.
- Grid รายการใช้ `auto-fit` + `minmax()` เพื่อให้บล็อกที่ผู้ดูแลคัดลอก reflow อัตโนมัติ ยกเว้น `.contact-list` และ `.services-grid` ที่ตั้งใจให้เป็น `1fr` คอลัมน์เดียวเสมอ การ์ดที่คัดลอกเพิ่มจะต่อลงล่างเป็นแถวใหม่.
- Section ใหม่หรือ section ที่ปรับต้องคงโครง `<section class="section" id="…"><div class="container">…` ภายใน `<main>`.
- Header สูงขั้นต่ำ 64px และ `html` ใช้ `scroll-padding-top: 6rem` เพื่อไม่ให้ anchor ถูก sticky header บัง.

## 5. Components

### Section Shell
- **Page order**: hero → ยี่ห้อและรุ่นรถ (`#brands`) → บริการของเรา (`#services`) → รีวิวจากครอบครัวเกินร้อย (`#testimonials`) → คำถามที่พบบ่อย (`#faq`) → ติดต่อเรา (`#contact`). รุ่นรถขึ้นก่อนเพราะเป็นสิ่งที่ลูกค้ามองหาเป็นอย่างแรก. พื้นสลับคำนวณจาก `nth-of-type` จึงเปลี่ยนตามลำดับอัตโนมัติ.
- **Structure**: `.section` → `.container` → `.section-title` + optional `.section-intro` + main content. `.section-title` ใช้สี `--color-primary` (#CF0000) เหมือนหัวข้อ hero — คอนทราสต์บนพื้นขาว 5.75:1 และบนพื้น `--color-surface-alt` 5.00:1 ผ่าน WCAG AA ทั้งคู่ ส่วนหัวข้อย่อย `.subsection-title` ยังเป็น `--color-text` เพื่อคงลำดับชั้นระหว่างหัวข้อหลักกับหัวข้อย่อย.
- **FAQ dividers**: `.faq-item` มีเส้นคั่นด้านบน แต่ `.faq-item:first-child` ถอดเส้นบนและ padding บนออก และไม่มีเส้นใต้รายการสุดท้าย เส้นคั่นจึงอยู่ระหว่างคำถามเท่านั้น ไม่กลายเป็นกรอบครอบทั้งกลุ่ม.
- **Logo chips**: ยี่ห้อใช้โลโก้แทนข้อความ (`.chip-logo` + `<img>` จาก `images/<brand>-logo.svg`) และไม่มีกรอบชิป — กรอบมนรอบโลโก้ที่รูปทรงต่างกันดูไม่เข้ากัน ส่วนชิปรุ่นรถที่เป็นข้อความยังคงกรอบไว้. โลโก้สูง 30px เท่ากันทุกยี่ห้อ ความกว้างไหลตามสัดส่วนของแต่ละโลโก้ ทุกไฟล์ต้องมี `viewBox` ไม่งั้นย่อขนาดด้วย CSS ไม่ได้ และต้องใส่ `alt` เป็นชื่อยี่ห้อ เพราะไม่มีข้อความให้ Google และ screen reader อ่านแล้ว.
- **Section marker**: `.section-title::after` วาดขีดแดง 56x4px (`--color-primary`, radius 2px) ใต้หัวข้อทุกส่วน ทำหน้าที่เป็นจุดสังเกตว่าขึ้นส่วนใหม่ ซึ่งมองเห็นได้แม้เลื่อนเร็วบนมือถือ — การเว้นช่องว่างอย่างเดียวไม่พอ เพราะบนจอเล็กผู้ใช้เห็นหน้าเว็บทีละส่วนเท่านั้น ระยะใต้หัวข้อคือ `--space-md`.
- **Variants**: alternating background เกิดจากลำดับ section อัตโนมัติเท่านั้น.
- **Spacing**: `--space-xl`, `--space-sm`, `--space-md`, `--space-lg`.
- **States**: static.
- **Accessibility**: unique section `id`, heading order ถูกต้อง, anchor landing ไม่ถูก header บัง.
- **Motion**: none.
- **Layout**: document stack.

### Button
- **Structure**: `<a class="btn btn-primary|btn-secondary">` พร้อม optional SVG `aria-hidden="true"`.
- **Variants**: primary แดง; secondary โปร่งใสขอบขาว.
- **Spacing**: padding เดิม `0.85rem 1.75rem`; กลุ่มปุ่มใช้ `--space-sm`.
- **States**: hover เปลี่ยนพื้น, active `scale(0.98)`, focus-visible outline 3px สี primary.
- **Accessibility**: ใช้ `<a>` เมื่อเป็นการนำทาง/โทร, link text ชัดเจน, external links มี `target="_blank" rel="noopener"` และ touch target ไม่ต่ำกว่า 44px.
- **Spacing**: padding `0.85rem 1.4rem` และ `gap: 0.4rem` ระหว่างไอคอนกับข้อความ.
- **Icon alignment**: `.btn` ใช้ `inline-flex` + `align-items: center` + `gap: 0.4rem` เพื่อให้ไอคอนกับข้อความอยู่กึ่งกลางแนวตั้งตรงกันจริง ห้ามกลับไปใช้ `vertical-align: middle` ซึ่งอิงเส้นฐาน + ครึ่ง x-height ทำให้ไอคอนเยื้องต่ำกว่าข้อความไทยราว 2-3px.
- **Motion**: background 0.2s และ transform 0.1s; reduced-motion ลด duration.
- **Layout**: inline cluster; wrap ได้.

### Official LINE CTA (`.line-cta`)
- **Structure**: `<a href="https://line.me/R/ti/p/@{{LINE_ID}}" class="line-cta" target="_blank" rel="noopener"><img class="line-cta-logo" src="images/line-logo.svg" alt="" width="320" height="320"><span class="line-cta-text">ข้อความของส่วนนี้</span></a>` — ปุ่มประกอบจากโลโก้ LINE + ข้อความ ไม่ใช่รูปปุ่มสำเร็จรูป จึงตั้งข้อความต่างกันได้ในแต่ละส่วน.
- **Sizing**: ปุ่มสูง 58px โลโก้ 58x58px ข้อความ 1.2rem padding ซ้าย 0.6rem padding ขวา 1.2rem เว้นระยะโลโก้-ข้อความ 0.15rem — ขนาดปุ่ม/ข้อความ/padding คือค่าเดิม (48px / 1rem / `--space-xs` / `--space-sm`) บวก 20% ถ้าจะปรับขนาดอีก ให้ปรับทุกค่าพร้อมกันเพื่อคงสัดส่วน ส่วน gap ตั้งไว้ต่ำเป็นพิเศษเพราะไฟล์โลโก้มีช่องว่างรอบเครื่องหมายอยู่ในตัวแล้ว.
- **Alignment**: `.section-cta` มือถือใช้ `justify-content: center` ปุ่มจึงอยู่กลางเมื่อขึ้นบรรทัดใหม่ ตั้งแต่ 768px ขึ้นไปกลับเป็น `space-between` (ข้อความซ้าย ปุ่มขวา) ส่วนปุ่มใน hero อยู่กลางทุกขนาดจออยู่แล้ว.
- **Logo blend**: `line-logo.svg` มีพื้นสี่เหลี่ยมมนสี #06C755 ในตัวไฟล์ ซึ่งตรงกับพื้นปุ่มพอดี พื้นจึงกลืนหายไป เหลือเห็นเฉพาะเครื่องหมาย LINE สีขาว (หลักการเดียวกับโลโก้ร้านที่กลืนกับแถบ header สีแดง) — ด้วยเหตุนี้ overlay สถานะ hover/press จึงต้องคลุมทั้งปุ่มผ่าน `::after` ไม่ใช่เปลี่ยนแค่ `background` มิฉะนั้นโลโก้จะไม่กลืนอีกต่อไป.
- **Variants**: โครงปุ่ม โลโก้ และสีเหมือนกันทุกที่ ต่างกันเฉพาะข้อความใน `.line-cta-text` ซึ่งเขียนให้เข้ากับบริบทของแต่ละส่วน และต้องไม่ซ้ำกัน (บังคับด้วยเทสต์ `test_each_section_label_is_distinct`).
- **Spacing**: `inline-flex` จัดกึ่งกลางแนวตั้ง โลโก้ 58×58px ประกบข้อความโดยตรง.
- **States**: active `scale(0.98)`, focus-visible outline 3px สี primary พร้อม offset 2px.
- **Accessibility**: โลโก้เป็นภาพประดับ ใช้ `alt=""` เพราะข้อความในปุ่มคือชื่อที่ screen reader อ่าน; `width="320"` และ `height="320"` (ขนาดจริงของไฟล์) กำหนดไว้กัน layout shift ส่วนขนาดแสดงผลคุมด้วย CSS; ปุ่มสูง 58px เกินเกณฑ์ touch target 44px.
- **Motion**: active press scale 0.1s.
- **Layout**: inline-flex element.

### Hero
- **Structure**: `<section class="hero" id="top">` → `.hero-media` (semantic `<img>`) + `.hero-content` (`<h1>` + `.hero-tagline` + `.hero-location` + `.hero-actions`). รูปอยู่เหนือข้อความบนมือถือ (image-first stack). `.hero-location` เป็นบรรทัดที่ตั้งร้านและย่านใกล้เคียง ใช้ `0.95rem` สี `--color-text-muted` จางกว่าแท็กไลน์. `.hero-actions` วางปุ่ม LINE ไว้บน และปุ่มนำทางไปร้านไว้ล่างเสมอ (`flex-direction: column`) ทุกขนาดจอ ไม่ใช่เฉพาะตอนจอแคบ. ใน `<h1>` มีเฉพาะชื่อร้านที่เป็น `.nowrap` — บรรทัดสาขายาวเกินกว่าจะอยู่บรรทัดเดียวที่ 375px จึงปล่อยให้ตัดบรรทัดได้.
- **Variants**: none — หน้าเดียวเท่านั้น.
- **Spacing**: image full-bleed บนมือถือ; `.hero-content` ใช้ `--space-lg` / `--space-sm` / `--space-xl`.
- **States**: `.line-cta` active press & focus-visible outline; ไม่มี hover บนรูป hero.
- **Accessibility**: hero `<img>` มี Thai alt, `width`/`height`, `loading="eager"`, `fetchpriority="high"`; `.line-cta` link `target="_blank" rel="noopener"` และระบุ `@{{LINE_ID}}` ใน `alt` ของรูปภาพ.
- **Motion**: none.
- **Layout**: mobile-first stacked; ที่ ≥768px รูปและข้อความจำกัด max-width และกึ่งกลาง — คงโครงเดียวกับมือถือ.

### รีวิวจากครอบครัวเกินร้อย (`#testimonials`)
- **Structure**: `.section-title` (รีวิวจากครอบครัวเกินร้อย) → `.carousel-track` (ภาพรวมความประทับใจ) → `.carousel-track.review-carousel` (ภาพรีวิวจาก Google) → `.section-cta` เดียว. หัวข้อบอกเนื้อหาครบอยู่แล้วจึงไม่มีคำโปรยและไม่มีหัวข้อย่อยคั่น เนื้อหาทั้งหมดเป็นภาพ ไม่มีการ์ดรีวิวแบบข้อความแล้ว รีวิวลูกค้ากับรูปวันรับรถรวมอยู่ในส่วนเดียวกัน เพราะเล่าเรื่องเดียวกันคือลูกค้าจริงของร้าน (เดิมแยกเป็น `#delivery` ต่างหาก).
- **Variants**: ทั้งสองกลุ่มเป็นสไลด์เลื่อนด้านข้าง มีรั้ว COPY FROM HERE ของตัวเอง. `.review-carousel` ทับค่าของสไลด์ปกติสองอย่าง: รูปรีวิวเป็นแนวนอน 2:1 จึงใช้ `aspect-ratio: 2 / 1` กับ `object-fit: contain` (ถ้าใช้ 1:1 + cover ตามค่าเดิม ข้อความรีวิวจะโดนครอป) และสไลด์กว้างกว่า `clamp(260px, 80vw, 560px)` เพื่อให้อ่านตัวหนังสือในรูปได้ ใช้ `80vw` เท่ากับสไลด์ด้านบน รูปถัดไปจึงโผล่มาแวบ ๆ เท่ากัน (27px ที่จอ 375px) เป็นสัญญาณว่าเลื่อนต่อได้.
- **Spacing**: `.carousel-track` มี `margin-bottom: --space-md` เพื่อไม่ให้ชนบล็อกถัดไป.
- **Slide sizing**: `.carousel-slide` ใช้ `flex: 0 0 clamp(260px, 80vw, 360px)` ไม่ใช้ breakpoint ความกว้างจึงไหลต่อเนื่องและหยุดโตที่ 360px (เดิมเป็น `85%` แล้วกระโดดเป็น `31%` ที่ 768px ทำให้สไลด์หดฮวบทันที) รูปเป็นจัตุรัส ความสูงจึงเท่าความกว้างและสูงสุด 360px เช่นกัน.
- **States**: carousel track มี focus-visible outline สำหรับการเลื่อนด้วยคีย์บอร์ด.
- **Accessibility**: `.carousel-track` คง `role="region"`, `aria-label` ภาษาไทย และ `tabindex="0"`; รูปทุกใบมี alt ภาษาไทยพร้อม `{{SHOP_NAME}}`.
- **Motion**: การเลื่อนเป็นการ scroll ปกติ ไม่มี autoplay.
- **Layout**: แถบรูปความประทับใจ แล้วแถบภาพรีวิว ปิดท้ายด้วยปุ่ม LINE เดียว (หนึ่ง `.line-cta` ต่อหนึ่ง section ตามสัญญาในเทสต์).

### Content Card
- **Structure**: semantic `article`/`figure` หรือ contact `<a>` บน surface พร้อม border.
- **Variants**: service, testimonial, gallery, contact channel.
- **Spacing**: `--space-md`; internal gaps `--space-xs` / `--space-sm`.
- **States**: contact card hover เปลี่ยน border เป็น primary; static cards ไม่มี decorative hover.
- **Accessibility**: decorative SVG `aria-hidden="true"`; meaningful image มี Thai alt; clickable card เป็น anchor ทั้งใบ.
- **Motion**: none beyond inherited link/button interaction.
- **Layout**: responsive auto-fit grid.

### Section Contact CTA
- **Structure**: compact `.section-cta` cluster หลัง main content ของ section (บริการ, รีวิวลูกค้า, ยี่ห้อรถ, FAQ) มีเพียงปุ่ม LINE ไม่มีข้อความนำหน้าแล้ว: `<a href="https://line.me/R/ti/p/@{{LINE_ID}}" class="line-cta" target="_blank" rel="noopener"><img class="line-cta-logo" src="images/line-logo.svg" alt="" width="320" height="320" loading="lazy"><span class="line-cta-text">ข้อความของส่วนนี้</span></a>`.
- **Variants**: ต่างกันเฉพาะข้อความบนปุ่ม ทุกส่วนไม่มีข้อความนำหน้าแล้ว ปุ่มอยู่กึ่งกลางทุกขนาดจอด้วย `justify-content: center` ที่ base ไม่มี override ที่ 768px.
- **Spacing**: แยกจาก content ด้วย `--space-lg`; internal gap `--space-sm`.
- **States**: inherited Official LINE CTA (`.line-cta`) states.
- **Accessibility**: โลโก้ในปุ่มเป็นภาพประดับ (`alt=""`) ชื่อที่ screen reader อ่านคือข้อความในปุ่ม; ปุ่มสูง 58px เกินเกณฑ์ touch target 44px.
- **Motion**: inherited `.line-cta` motion.
- **Layout**: ปุ่มเดียวอยู่กึ่งกลางทุกความกว้าง.

### Consolidated Contact Section
- **Structure**: Section Shell → `.contact-hours` → `.location-grid` (ส่วนนี้ไม่มี `.section-intro`). `.contact-hours` เป็นข้อความล้วนเต็มความกว้าง อยู่ใต้ `.section-title` ทันที ไม่มีหัวข้อย่อยกำกับ ไม่มีพื้นหลังและเส้นขอบ (เป็นข้อมูล ไม่ใช่ปุ่ม) เหลือเฉพาะ padding ล่าง `--space-md` จึงชิดขอบซ้ายเดียวกับหัวข้อ วันและเวลาอยู่บรรทัดเดียวกัน (`<strong>เปิดทุกวัน</strong> 08:30 - 18:30 น.` ไม่มี `<br>`) และมี `.address-line` (ที่อยู่จาก `{{ADDRESS}}` + `{{POSTAL_CODE}}`) ต่อท้ายในบล็อกเดียวกัน เวลาเปิดกับที่อยู่จึงอ่านต่อเนื่องกันก่อนถึงแผนที่. `.location-grid` คอลัมน์ซ้ายเป็นแผนที่ (src จาก `{{MAPS_EMBED_URL}}` ใน variables.txt) และปุ่มนำทาง; คอลัมน์ขวาเป็น `.contact-list` (โทรเลย, แอด LINE, ติดตาม Facebook, ติดตาม TikTok) การ์ดใช้พื้นขาว `--color-bg` บนพื้นส่วนสีเทา พร้อมเงาบาง ๆ (`0 1px 3px rgba(0,0,0,0.10)`) เพื่อให้ดูยกขึ้นและกดได้ กดแล้วเงาหายและขยับลง 1px เหมือนปุ่มจริง ป้ายกำกับใช้คำชวนกดเพราะทุกการ์ดเป็นลิงก์ และค่าของแต่ละช่องทาง (`<small>`) ใช้สี `--color-primary` น้ำหนัก 500 ให้อ่านเหมือนลิงก์ (คอนทราสต์บนพื้นการ์ดสีขาว 5.75:1 ผ่าน AA) ไม่มีไอคอนลูกศรแล้ว — เงายกการ์ดกับค่าสีลิงก์บอกว่ากดได้เพียงพอ และลูกศรจะสื่อผิดกับการ์ดโทรศัพท์ซึ่งเปิดแป้นโทร ไม่ได้เปิดเว็บภายนอก. ส่วนการ์ดเบอร์สำรองถูกคอมเมนต์ไว้ใน `template.html` (มาร์กอัปยังอยู่ครบ เปิดกลับได้ตามคำอธิบายในคอมเมนต์). `{{BUSINESS_PROFILE_URL}}` ไม่มีลิงก์ที่แสดงบนหน้า — ใช้เฉพาะใน JSON-LD `sameAs` เท่านั้น.
- **Variants**: one column below 768px; map-left/contact-right from 768px. `.contact-list` stays a single column at every width, so the channel cards always read as one vertical stack.
- **Spacing**: column gap `--space-lg`; `.contact-list` gap `--space-xs` เพื่อให้การ์ดช่องทางติดต่ออยู่ชิดกันเป็นกลุ่มเดียว; `.contact-item` padding `--space-sm var(--space-md)` (แนวตั้งบางกว่าการ์ดทั่วไป) ข้อความ `1.1rem` / `<small>` `0.95rem`; address/action stack uses `--space-sm`.
- **States**: map static; directions and channel links use existing Button/Content Card states.
- **Accessibility**: iframe มี `title` ภาษาไทย, `loading="lazy"`, `allowfullscreen`, `referrerpolicy="strict-origin-when-cross-origin"` และไม่มี `width`/`height`/`style` (CSS กำหนดขนาด); channel labels and values remain visible; external links use `rel="noopener"`.
- **Motion**: none beyond primitives.
- **Layout**: hours sit full-width under the intro; below that a responsive sidebar grid — map/address/directions left, contact channels right.

### Header Navigation
- **Structure**: `.header-brand` is a linked logo image — `<a href="#top" class="header-brand"><img src="images/logo.jpg" alt="{{SHOP_NAME}}" width="800" height="800"></a>` (intrinsic 800x800) — not visible text; the shop name survives only as the image `alt`. `.header-brand` is a fixed 128x48 landscape crop viewport (`overflow: hidden`) and `.header-brand img` uses `object-fit: cover; object-position: center` to trim the logo's top/bottom whitespace, so the 800x800 square reads as a landscape logo inside the 64px header. The logo's baked background is #CF0000, which directly matches the header `--color-primary` (#CF0000); since the bitmap and the header bar are the same red, `.header-brand img` needs no `filter` or `mix-blend-mode` treatment — the red rectangle already disappears into the header bar while the white Thai mark stays crisp. `.header-brand picture` mirrors the img sizing (`width`/`height: 100%`) so the deploy-time optimizer's `<img>`→`<picture>` rewrite behaves identically. Dimensions are the same on mobile and desktop. A single shared `<nav>` is controlled on mobile by the `#nav-toggle` checkbox + label and becomes inline at 768px. มี JavaScript ขนาดเล็กก่อน `</body>` ที่ uncheck `#nav-toggle` หลังคลิกลิงก์ใน `.header-nav a` เพื่อปิดเมนูมือถือหลังเลือก anchor — คง checkbox hack ไว้สำหรับการเปิด/ปิดด้วยปุ่ม hamburger. `.header-call` เป็นปุ่มโทรไอคอนอย่างเดียว (`tel:{{PHONE_TEL}}`) วางไว้ก่อนเมนูทางขวา ใช้ `margin-left: auto` ดันตัวเองและเมนูไปชิดขวา กล่อง 44x44 ไม่มีเส้นขอบ (ต่างจาก hamburger ที่มีเส้นขอบ) hover เป็นพื้นหลัง `rgba(255,255,255,0.15)` แสดงทั้งมือถือและเดสก์ท็อป ช่องทางติดต่ออื่นทั้งหมดยังอยู่ใน `#contact`.
- **Variants**: mobile dropdown (white) / desktop row (on red bar).
- **States**: open/closed icons, hover accent, focus-visible on checkbox label and links.
- **Accessibility**: checkbox hack must remain (no `<details>`); the brand link's accessible name comes from `alt="{{SHOP_NAME}}"` (no visible text) and its 128x48 box meets the 44px touch target; the logo's baked #CF0000 background directly matches `--color-primary` (see Structure) so it blends seamlessly with the header bar with no color treatment; hamburger and desktop nav links use `--color-white` on `--color-primary` bar (WCAG AA) with a white focus ring; mobile dropdown stays white with `--color-text` and a primary focus ring for readability; controls meet 44px target.
- **Motion**: none.
- **Layout**: sticky header cluster; the header carries a single icon-only call shortcut (`.header-call`) and `#contact` remains the full location/contact section.

### Footer
- **Structure**: `<footer class="site-footer">` → `.container` → copyright `<small>` only; the shop name appears once, in the copyright line. Facebook and TikTok moved into `#contact` as `.contact-item` cards, so every channel now lives in one place.
- **Variants**: none.
- **Spacing**: `--space-lg` vertical padding.
- **States**: static text; global focus-visible outline applies to any link added later.
- **Accessibility**: no interactive controls; the copyright is plain text.
- **Motion**: none.
- **Layout**: single centered line.

## 6. Motion & Interaction

| Type | Current value | Usage |
|---|---|---|
| Standard hover | `0.2s ease` | button background |
| Press feedback | `0.1s ease` | button transform |
| Smooth navigation | browser smooth scroll | in-page anchors |

- Motion communicates interaction only; static cards and content do not animate.
- Animate only composited `transform` for press feedback; color transition is limited to interactive background state.
- `prefers-reduced-motion: reduce` disables smooth scroll and reduces transition/animation duration to `0.01ms`.
- Every interactive item keeps hover, active where applicable, and visible keyboard focus.

## 7. Depth & Surface

Strategy: **mixed border + restrained shadow**.

- Cards use `--color-surface`, 1px `--color-border`, and `--radius`; they do not cast shadows.
- Header uses a restrained shadow (`0 2px 6px rgba(0,0,0,0.15)`) to separate the primary-red bar while sticky.
- Mobile nav dropdown uses the existing stronger shadow (`0 8px 16px rgba(0,0,0,0.08)`) to indicate overlay depth.
- Hero depth comes from the real shop image above a white text surface, not gradients or decorative shapes.
- Footer is a single dark plane using `--color-text`; social links remain typographic and do not become colored badges.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- Target WCAG 2.2 AA: body contrast at least 4.5:1, large text/UI boundaries at least 3:1.
- All links and controls are keyboard reachable and show a 3px focus-visible outline with 2px offset: primary on light surfaces and white on the primary-red header.
- Touch controls target at least 44×44px; responsive layouts must not create horizontal scrolling at 375px.
- Thai alt text is required for meaningful images; decorative SVGs require `aria-hidden="true"`.
- Iframes require descriptive title, lazy loading, and referrer policy. New-tab links require `rel="noopener"`.
- Body line-height remains 1.7 (Sarabun body, Kanit headings); content and action labels must use direct Thai wording for low cognitive load.
- Reduced-motion behavior in Section 6 is mandatory.

### Primary Personas / Tasks

- ลูกค้ามือถือที่ต้องการโทรหรือ LINE ทันที: ต้องพบ primary phone, backup phone และ LINE ใน contact section เดียว.
- ลูกค้าที่กำลังเดินทาง: ต้องเห็นแผนที่ ที่อยู่ และปุ่มนำทางในคอลัมน์เดียวกัน.
- ลูกค้าที่วางแผนเข้าร้าน: ต้องเห็นเวลาเปิดทำการเด่นก่อนช่องทางติดต่อ — จึงวางไว้บรรทัดแรกใต้หัวข้อ `ติดต่อเรา`.
- ผู้ดูแลร้านที่แก้ผ่าน GitHub: ต้องยังค้นหา EDIT ME / SWAP IMAGE / COPY FROM HERE / TO HERE และคัดลอกบล็อกซ้ำได้โดย layout ไม่พัง.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|---|---|---|---|
| ไม่มี dark mode | ทั้งเว็บ | เป็นข้อจำกัดผลิตภัณฑ์ที่ยอมรับไว้และลดภาระผู้ดูแล | ทบทวนเมื่อผู้ดูแลร้องขอ |
| Google Fonts เป็น third-party | `template.html` | ต้องการ Kanit (หัวข้อ) และ Sarabun (ข้อความ) และยอมรับ system fallback; ยังไม่ self-host | ทบทวนเมื่อมี asset pipeline สำหรับ font |
| ปุ่ม LINE ใช้สีเขียวแบรนด์ | `.line-cta` (hero และ section-end CTAs) | ปุ่มสร้างเองจากโลโก้ `images/line-logo.svg` + ข้อความ เพื่อให้แต่ละส่วนใช้ข้อความต่างกันได้; สีตามคู่มือแบรนด์ LINE — พื้น `--color-line` #06C755, hover ทับ `rgba(0,0,0,0.1)`, กดทับ `rgba(0,0,0,0.3)` ผ่าน `.line-cta::after` ซึ่งคลุมทั้งปุ่มรวมโลโก้ | คงไว้ตามข้อกำหนดแบรนด์ของ LINE |
