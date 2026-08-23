# เกินร้อยมอเตอร์ Design System

## 1. Atmosphere & Identity

หน้าเว็บให้ความรู้สึกตรงไปตรงมา น่าเชื่อถือ และเข้าถึงง่ายแบบร้านมอเตอร์ไซค์ในชุมชน เนื้อหาภาษาไทยอ่านสบายบนมือถือและพาผู้ใช้ไปสู่การโทร แชต LINE หรือเดินทางมาร้านได้เร็ว ลายเซ็นของระบบคือสีแดง racing red เพียงสีเดียวบนพื้นขาว/เทา สลับกับภาพหน้าร้านจริงและพื้นผิวการ์ดที่เรียบแข็งแรง ไม่ตกแต่งเกินหน้าที่

## 2. Color

### Palette

| Role | Token | Value | Usage |
|---|---|---|---|
| Accent/primary | `--color-primary` | `#C8102E` | ปุ่มหลัก ลิงก์ ไอคอน จุดเน้น และ focus ring |
| Accent/hover | `--color-primary-dark` | `#A00D24` | hover ของปุ่มและปุ่มโทร |
| Text/primary | `--color-text` | `#1A1A1A` | ข้อความหลัก หัวข้อ และพื้น footer |
| Text/secondary | `--color-text-muted` | `#5A5A5A` | คำอธิบาย ที่อยู่ และข้อมูลรอง |
| Surface/page | `--color-bg` | `#FFFFFF` | พื้นหน้าและ header |
| Surface/card | `--color-surface` | `#F6F6F6` | การ์ดและกล่องช่องทางติดต่อ |
| Surface/alternate | `--color-surface-alt` | `#EFEFEF` | พื้น section สลับและข้อความ footer |
| Border/default | `--color-border` | `#E0E0E0` | เส้นคั่น ขอบการ์ด และขอบเมนู |
| Text/on-accent | `--color-white` | `#FFFFFF` | ข้อความบนปุ่มแดงและบนภาพ hero |

### Rules

- `--color-primary` เป็น accent เพียงสีเดียว ห้ามเพิ่ม secondary accent หรือสีแบรนด์ของช่องทาง social.
- สีพื้น section สลับด้วย `main > section:nth-of-type(even)` เท่านั้น ห้ามใส่ background class ราย section.
- overlay ภาพ hero ใช้สีจาก `--color-text` ในรูปแบบโปร่งใสตามค่าปัจจุบัน; hover แบบโปร่งใสบนปุ่ม hero ใช้สีขาวเดิม ห้ามสร้างสีใหม่เพื่อการตกแต่ง.
- สีทั้งหมดที่ผู้ดูแลแก้ได้อยู่ใน `:root` ส่วน `CHANGE COLORS HERE`; ต้องเก็บ token เดิมครบทุกตัว.

## 3. Typography

### Font Stack

- Primary: `--font-family` = `"Sarabun", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif`.
- ไม่มี mono หรือ serif font.
- น้ำหนักที่โหลดและใช้: 400, 500, 600, 700.

### Scale

| Level | Mobile | Desktop (≥768px) | Weight / line-height | Usage |
|---|---|---|---|---|
| Hero display | `clamp(1.75rem, 8vw, 3rem)` | `3rem` | 700 / 1.3 | ชื่อร้านใน hero |
| Section title | `1.75rem` | `2rem` | 700 / body rhythm | หัวข้อ `<h2>` |
| Subsection | `1.3rem` | `1.3rem` | 600 | หัวข้อย่อยและเวลาเปิดทำการ |
| Card / label title | `1.05rem`–`1.15rem` | same | 600 | ชื่อบริการ FAQ chip และปุ่ม |
| Hero lead | `1.15rem` | `1.3rem` | 400 | tagline |
| Body | `17px` | `18px` | 400 / **1.7** | เนื้อหาภาษาไทยทั้งหมด |
| Supporting | `0.85rem`–`0.95rem` | same | 400–500 | metadata แหล่งรีวิว และข้อมูลรอง |

### Rules

- เนื้อหาผู้ใช้เป็นภาษาไทย และ body line-height ต้องคงที่ `1.7`.
- หัวข้อใช้ลำดับ semantic ตามโครง section; ห้ามเลือก heading level จากขนาดตัวอักษร.
- ข้อความยาวจำกัดที่ 60–65ch เพื่อความอ่านง่าย; ห้ามลด body ต่ำกว่าค่าปัจจุบัน.

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
- Breakpoint `600px` ใช้เฉพาะ contact-list ตามข้อยกเว้นเดิม.
- `.container` กว้างไม่เกิน `--max-width`, กึ่งกลาง และใช้ gutter จาก spacing token.
- Grid รายการใช้ `auto-fit` + `minmax()` เพื่อให้บล็อกที่ผู้ดูแลคัดลอก reflow อัตโนมัติ.
- Section ใหม่หรือ section ที่ปรับต้องคงโครง `<section class="section" id="…"><div class="container">…` ภายใน `<main>`.
- Header สูงขั้นต่ำ 64px และ `html` ใช้ `scroll-padding-top: 6rem` เพื่อไม่ให้ anchor ถูก sticky header บัง.

## 5. Components

### Section Shell
- **Structure**: `.section` → `.container` → `.section-title` + optional `.section-intro` + main content.
- **Variants**: alternating background เกิดจากลำดับ section อัตโนมัติเท่านั้น.
- **Spacing**: `--space-xl`, `--space-sm`, `--space-md`, `--space-lg`.
- **States**: static.
- **Accessibility**: unique section `id`, heading order ถูกต้อง, anchor landing ไม่ถูก header บัง.
- **Motion**: none.
- **Layout**: document stack.

### Button
- **Structure**: `<a class="btn btn-primary|btn-secondary">` พร้อม optional SVG `aria-hidden="true"`.
- **Variants**: primary แดง; secondary โปร่งใสขอบขาวบน hero.
- **Spacing**: padding เดิม `0.85rem 1.75rem`; กลุ่มปุ่มใช้ `--space-sm`.
- **States**: hover เปลี่ยนพื้น, active `scale(0.98)`, focus-visible outline 3px สี primary.
- **Accessibility**: ใช้ `<a>` เมื่อเป็นการนำทาง/โทร, link text ชัดเจน, external links มี `target="_blank" rel="noopener"` และ touch target ไม่ต่ำกว่า 44px.
- **Motion**: background 0.2s และ transform 0.1s; reduced-motion ลด duration.
- **Layout**: inline cluster; wrap ได้.

### Content Card
- **Structure**: semantic `article`/`figure` หรือ contact `<a>` บน surface พร้อม border.
- **Variants**: service, testimonial, gallery, contact channel.
- **Spacing**: `--space-md`; internal gaps `--space-xs` / `--space-sm`.
- **States**: contact card hover เปลี่ยน border เป็น primary; static cards ไม่มี decorative hover.
- **Accessibility**: decorative SVG `aria-hidden="true"`; meaningful image มี Thai alt; clickable card เป็น anchor ทั้งใบ.
- **Motion**: none beyond inherited link/button interaction.
- **Layout**: responsive auto-fit grid.

### Section Contact CTA
- **Structure**: compact `.section-cta` cluster หลัง main content ของ section มีข้อความสั้นและ `<a href="#contact" class="btn btn-primary">`.
- **Variants**: ข้อความตาม context ของ about, brands, FAQ; visual treatment เดียวกัน.
- **Spacing**: แยกจาก content ด้วย `--space-lg`; internal gap `--space-sm`.
- **States**: inherited Button states.
- **Accessibility**: link text ต้องบอกการกระทำ ไม่ใช้ “คลิกที่นี่”; touch target ใช้ Button primitive.
- **Motion**: inherited Button motion.
- **Layout**: wrapping cluster, centered on narrow screens only when content naturally wraps.

### Consolidated Contact Section
- **Structure**: Section Shell → `.location-grid`; left column contains map, address, directions Button; right column contains prominent hours and `.contact-list` for phone primary, backup, LINE.
- **Variants**: one column below 768px; map-left/contact-right from 768px. Contact list changes layout only at existing 600px convention.
- **Spacing**: column gap `--space-lg`; card gap `--space-md`; address/action stack uses `--space-sm`.
- **States**: map static; directions and channel links use existing Button/Content Card states.
- **Accessibility**: iframe keeps descriptive Thai `title`, `loading="lazy"`, `referrerpolicy`; channel labels and values remain visible; external links use `rel="noopener"`.
- **Motion**: none beyond primitives.
- **Layout**: responsive sidebar grid; map/address/directions left, hours/actions right.

### Header Navigation
- **Structure**: single shared `<nav>` controlled on mobile by `#nav-toggle` checkbox + label; inline at 768px.
- **Variants**: mobile dropdown / desktop row.
- **States**: open/closed icons, hover accent, focus-visible on checkbox label and links.
- **Accessibility**: persistent header-call `aria-label`; checkbox hack must remain (no `<details>`); controls meet 44px target.
- **Motion**: none.
- **Layout**: sticky header cluster; only `#contact` represents location/contact.

### Footer Social Navigation
- **Structure**: `<nav aria-label="โซเชียลมีเดีย"><ul class="footer-socials"><li><a><svg>…</svg><span>…` for Facebook and TikTok, followed by copyright; the shop name appears once in the copyright line only.
- **Variants**: monochrome icon-plus-text links; no channel brand colors.
- **Spacing**: cluster gap `--space-sm`, separation `--space-xs` / `--space-sm`.
- **States**: default light text, hover underline, global focus-visible outline.
- **Accessibility**: semantic nav/list, recognizable decorative SVG icons use `aria-hidden="true"` and `currentColor`, accessible visible link text includes platform name and handle, external links use `target="_blank" rel="noopener"`, touch targets at least 44px.
- **Motion**: none.
- **Layout**: centered wrapping cluster.

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
- Header uses a subtle existing shadow (`0 1px 3px rgba(0,0,0,0.06)`) plus border to separate it while sticky.
- Mobile nav dropdown uses the existing stronger shadow (`0 8px 16px rgba(0,0,0,0.08)`) to indicate overlay depth.
- Hero depth comes from the real shop image plus dark overlay, not gradients or decorative shapes.
- Footer is a single dark plane using `--color-text`; social links remain typographic and do not become colored badges.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- Target WCAG 2.2 AA: body contrast at least 4.5:1, large text/UI boundaries at least 3:1.
- All links and controls are keyboard reachable and show the 3px `--color-primary` focus-visible outline with 2px offset.
- Touch controls target at least 44×44px; responsive layouts must not create horizontal scrolling at 375px.
- Thai alt text is required for meaningful images; decorative SVGs require `aria-hidden="true"`.
- Iframes require descriptive title, lazy loading, and referrer policy. New-tab links require `rel="noopener"`.
- Sarabun body line-height remains 1.7; content and action labels must use direct Thai wording for low cognitive load.
- Reduced-motion behavior in Section 6 is mandatory.

### Primary Personas / Tasks

- ลูกค้ามือถือที่ต้องการโทรหรือ LINE ทันที: ต้องพบ primary phone, backup phone และ LINE ใน contact section เดียว.
- ลูกค้าที่กำลังเดินทาง: ต้องเห็นแผนที่ ที่อยู่ และปุ่มนำทางในคอลัมน์เดียวกัน.
- ลูกค้าที่วางแผนเข้าร้าน: ต้องเห็นเวลาเปิดทำการเด่นก่อนช่องทางติดต่อ.
- ผู้ดูแลร้านที่แก้ผ่าน GitHub: ต้องยังค้นหา EDIT ME / SWAP IMAGE / COPY FROM HERE / TO HERE และคัดลอกบล็อกซ้ำได้โดย layout ไม่พัง.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|---|---|---|---|
| ไม่มี dark mode | ทั้งเว็บ | เป็นข้อจำกัดผลิตภัณฑ์ที่ยอมรับไว้และลดภาระผู้ดูแล | ทบทวนเมื่อผู้ดูแลร้องขอ |
| Google Fonts เป็น third-party | `template.html` | ต้องการ Sarabun และยอมรับ system fallback; ยังไม่ self-host | ทบทวนเมื่อมี asset pipeline สำหรับ font |
| ไม่มี JavaScript ปิดเมนูหลังเลือก anchor | header mobile nav | โครงการกำหนด no-JS และ checkbox hack รักษา desktop nav ได้เสถียร | ทบทวนเมื่อข้อกำหนด no-JS เปลี่ยน |
| มี breakpoint 600px เฉพาะ contact grid | `style.css` | เป็นข้อยกเว้นเดิมเพื่อรักษาขนาดการ์ดและ touch readability | คงไว้จน layout contact เปลี่ยนระบบ |
