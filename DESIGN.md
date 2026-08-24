# เกินร้อยมอเตอร์ Design System

## 1. Atmosphere & Identity

หน้าเว็บให้ความรู้สึกตรงไปตรงมา น่าเชื่อถือ และเข้าถึงง่ายแบบร้านมอเตอร์ไซค์ในชุมชน เนื้อหาภาษาไทยอ่านสบายบนมือถือและพาผู้ใช้ไปสู่การโทร แชต LINE หรือเดินทางมาร้านได้เร็ว ลายเซ็นของระบบคือสีแดง racing red เพียงสีเดียวบนพื้นขาว/เทา สลับกับภาพหน้าร้านจริงและพื้นผิวการ์ดที่เรียบแข็งแรง ไม่ตกแต่งเกินหน้าที่

## 2. Color

### Palette

| Role | Token | Value | Usage |
|---|---|---|---|
| Accent/primary | `--color-primary` | `#C8102E` | ปุ่มหลัก ลิงก์ ไอคอน จุดเน้น และ focus ring |
| Accent/hover | `--color-primary-dark` | `#A00D24` | hover ของปุ่มหลัก |
| Text/primary | `--color-text` | `#1A1A1A` | ข้อความหลัก หัวข้อ และพื้น footer |
| Text/secondary | `--color-text-muted` | `#5A5A5A` | คำอธิบาย ที่อยู่ และข้อมูลรอง |
| Surface/page | `--color-bg` | `#FFFFFF` | พื้นหน้าและพื้น hero |
| Surface/card | `--color-surface` | `#F6F6F6` | การ์ดและกล่องช่องทางติดต่อ |
| Surface/alternate | `--color-surface-alt` | `#EFEFEF` | พื้น section สลับและข้อความ footer |
| Border/default | `--color-border` | `#E0E0E0` | เส้นคั่น ขอบการ์ด และขอบเมนู |
| Text/on-accent | `--color-white` | `#FFFFFF` | ข้อความบนปุ่มแดงและแถบ header แดง |

### Rules

- `--color-primary` เป็น accent เพียงสีเดียว ห้ามเพิ่ม secondary accent หรือสีแบรนด์ของช่องทาง social.
- **ข้อยกเว้นสำหรับรูปภาพแบรนด์ทางการ:** รูปปุ่ม LINE Add Friend (`images/line-add-friend-th.png`) มีสีเขียวทางการของ LINE อยู่ภายในไฟล์บิตแมปอยู่แล้ว ซึ่งไม่ใช่ CSS token สีเขียวแบรนด์ LINE ถูกจำกัดอยู่เฉพาะภาพแบรนด์ทางการนี้ และคงหลักการ single-accent ใน CSS ไว้.
- สีพื้น section สลับด้วย `main > section:nth-of-type(even)` เท่านั้น ห้ามใส่ background class ราย section.
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
- **Variants**: primary แดง; secondary โปร่งใสขอบขาว.
- **Spacing**: padding เดิม `0.85rem 1.75rem`; กลุ่มปุ่มใช้ `--space-sm`.
- **States**: hover เปลี่ยนพื้น, active `scale(0.98)`, focus-visible outline 3px สี primary.
- **Accessibility**: ใช้ `<a>` เมื่อเป็นการนำทาง/โทร, link text ชัดเจน, external links มี `target="_blank" rel="noopener"` และ touch target ไม่ต่ำกว่า 44px.
- **Motion**: background 0.2s และ transform 0.1s; reduced-motion ลด duration.
- **Layout**: inline cluster; wrap ได้.

### Official LINE CTA (`.line-cta`)
- **Structure**: `<a href="https://line.me/R/ti/p/@{{LINE_ID}}" class="line-cta" target="_blank" rel="noopener"><img src="images/line-add-friend-th.png" alt="เพิ่มเพื่อน LINE @{{LINE_ID}}" width="202" height="60"></a>`.
- **Variants**: ใช้รูปภาพปุ่มทางการขนาดต้นฉบับ 202x60px เหมือนกันทั้งใน hero และท้าย section (บริการ, ยี่ห้อรถ, FAQ).
- **Spacing**: inline-block display; native dimension 202×60px.
- **States**: active `scale(0.98)`, focus-visible outline 3px สี primary พร้อม offset 2px.
- **Accessibility**: ห้ามตัดแต่ง ครอบตัด หรือปรับขนาดรูปภาพบิตแมป; ต้องระบุ `alt` พร้อม LINE ID (`@{{LINE_ID}}`) เสมอ; `width="202"` และ `height="60"` กำหนดขนาดเพื่อป้องกัน layout shift; touch target 202×60px ครอบคลุมเกณฑ์ 44px.
- **Motion**: active press scale 0.1s.
- **Layout**: inline block element.

### Hero
- **Structure**: `<section class="hero" id="top">` → `.hero-media` (semantic `<img>`) + `.hero-content` (`<h1>` + `.hero-tagline` + `.line-cta`). รูปอยู่เหนือข้อความบนมือถือ (image-first stack).
- **Variants**: none — หน้าเดียวเท่านั้น.
- **Spacing**: image full-bleed บนมือถือ; `.hero-content` ใช้ `--space-lg` / `--space-sm` / `--space-xl`.
- **States**: `.line-cta` active press & focus-visible outline; ไม่มี hover บนรูป hero.
- **Accessibility**: hero `<img>` มี Thai alt, `width`/`height`, `loading="eager"`, `fetchpriority="high"`; `.line-cta` link `target="_blank" rel="noopener"` และระบุ `@{{LINE_ID}}` ใน `alt` ของรูปภาพ.
- **Motion**: none.
- **Layout**: mobile-first stacked; ที่ ≥768px รูปและข้อความจำกัด max-width และกึ่งกลาง — คงโครงเดียวกับมือถือ.

### Content Card
- **Structure**: semantic `article`/`figure` หรือ contact `<a>` บน surface พร้อม border.
- **Variants**: service, testimonial, gallery, contact channel.
- **Spacing**: `--space-md`; internal gaps `--space-xs` / `--space-sm`.
- **States**: contact card hover เปลี่ยน border เป็น primary; static cards ไม่มี decorative hover.
- **Accessibility**: decorative SVG `aria-hidden="true"`; meaningful image มี Thai alt; clickable card เป็น anchor ทั้งใบ.
- **Motion**: none beyond inherited link/button interaction.
- **Layout**: responsive auto-fit grid.

### Section Contact CTA
- **Structure**: compact `.section-cta` cluster หลัง main content ของ section (บริการ, ยี่ห้อรถ, FAQ) ประกอบด้วยข้อความสั้นและ `<a href="https://line.me/R/ti/p/@{{LINE_ID}}" class="line-cta" target="_blank" rel="noopener"><img src="images/line-add-friend-th.png" alt="เพิ่มเพื่อน LINE @{{LINE_ID}}" width="202" height="60" loading="lazy"></a>`.
- **Variants**: ข้อความตาม context ของบริการ, ยี่ห้อรถ, FAQ; ใช้รูปภาพปุ่มทางการ LINE Add Friend เดียวกัน.
- **Spacing**: แยกจาก content ด้วย `--space-lg`; internal gap `--space-sm`.
- **States**: inherited Official LINE CTA (`.line-cta`) states.
- **Accessibility**: รูปภาพปุ่มมี `alt` ระบุ LINE ID พร้อม `loading="lazy"`; touch target 202×60px.
- **Motion**: inherited `.line-cta` motion.
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
- **Structure**: single shared `<nav>` controlled on mobile by `#nav-toggle` checkbox + label; inline at 768px. ไม่มีปุ่มโทรใน header — ช่องทางติดต่อทั้งหมดอยู่ใน `#contact`.
- **Variants**: mobile dropdown (white) / desktop row (on red bar).
- **States**: open/closed icons, hover accent, focus-visible on checkbox label and links.
- **Accessibility**: checkbox hack must remain (no `<details>`); brand, hamburger, and desktop nav links use `--color-white` on `--color-primary` bar (WCAG AA) with a white focus ring; mobile dropdown stays white with `--color-text` and a primary focus ring for readability; controls meet 44px target.
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
| รูปภาพแบรนด์ทางการ LINE Add Friend มีสีเขียวแบรนด์ | `.line-cta` (hero และ section-end CTAs) | ใช้รูปภาพปุ่มทางการบิตแมป 202x60px จาก LINE เพื่อการจดจำแบรนด์; สีเขียวฝังในไฟล์รูปภาพบิตแมป จึงอนุโลมเป็นข้อยกเว้นภาพแบรนด์ทางการโดยไม่สร้าง CSS accent token เพิ่ม | คงไว้ตามข้อกำหนดแบรนด์ของ LINE |
