# DESIGN.md — Design Token Reference

> Concise reference for future agents and maintainers. Keep changes consistent
> with the tokens and patterns defined here.

---

## 0. Research Log

- **Scope**: basic maintainability-first local business landing page (Bangkok motorcycle shop).
- **Heavyweight reference research deliberately skipped** per orchestrator instruction.
  Lazyweb real-product screen research, imagen concept drafts, and open-design library
  lookups were not run — the brief is a trust-first local-business page, not a showcase.
- **Layer A loaded**: `taste-skill.md` (execution discipline only — trust-first dial preset).
- **Layer B**: none loaded; aesthetic is "polished Suzuki/Yamaha dealer service page" —
  clean, one strong accent, generous whitespace, large tap targets.
- **Dials**: DESIGN_VARIANCE 3-4, MOTION_INTENSITY 2-3, VISUAL_DENSITY 4-5.
  (Trust-first local business → low variance, near-zero motion, moderate density.)
- **Post-initial iteration**: single-source `variables.txt` + `build.py` + npm `html-validate`
  in CI replaced the original all-placeholders-in-HTML + `html5validator` design.
  Changed because repeated shop facts scattered across many HTML locations were
  error-prone for non-technical maintainers — a single KEY=VALUE file is safer.

---

## 0b. Build System

`index.html` is **generated** from `template.html` + `variables.txt` by `build.py`.
Never edit `index.html` directly — it is gitignored and overwritten on every build.

**`{{TOKEN}}` syntax**: `template.html` contains `{{SHOP_NAME}}`, `{{PHONE_TEL}}`, etc.
`build.py` reads `variables.txt` (KEY=VALUE lines), substitutes every `{{TOKEN}}`,
and writes `index.html`. If a token in the template has no matching variable, the
build fails with a bilingual error.

**The 9 variables** (all defined in `variables.txt`):

| Token | Purpose |
|-------|---------|
| `SHOP_NAME` | Shop name (title, header, hero, footer, JSON-LD, OG tags) |
| `PHONE_DISPLAY` | Phone with dashes for display |
| `PHONE_TEL` | Phone digits-only for `tel:` links and JSON-LD |
| `ADDRESS` | Street address (city/postal added automatically) |
| `POSTAL_CODE` | 5-digit postal code |
| `LINE_ID` | LINE ID without @ |
| `FACEBOOK_PAGE` | Facebook page slug |
| `TIKTOK_USER` | TikTok username without @ |
| `SITE_URL` | Canonical domain (https:// + trailing /) |

**How to add a new variable** (3 steps):
1. Put `{{NEW_TOKEN}}` in `template.html` where the value should appear.
2. Add `NEW_TOKEN = value` in `variables.txt` (uppercase A-Z and _ only, non-empty).
3. `build.py` validates automatically — missing tokens fail the build.

**CI pipeline** (`.github/workflows/pages.yml`): the `validate` job runs
`python3 build.py` then `html-validate` on the generated `index.html` before the
`deploy` job can publish. Broken builds never go live.

---

## 1. Palette Tokens

All colors are CSS custom properties on `:root` in `template.html` (the source; `index.html` is generated — never edit it).
Maintainers change them in one place (marked `CHANGE COLORS HERE / เปลี่ยนสีที่นี่`).

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | `#C8102E` | Accent — buttons, links, icon strokes, brand name |
| `--color-primary-dark` | `#A00D24` | Hover/active state for primary buttons |
| `--color-text` | `#1A1A1A` | Body text, headings, footer background |
| `--color-text-muted` | `#5A5A5A` | Secondary text, descriptions, captions |
| `--color-bg` | `#FFFFFF` | Page background, header background |
| `--color-surface` | `#F6F6F6` | Card backgrounds, contact items |
| `--color-surface-alt` | `#EFEFEF` | Automatic alternating section background (see §4) |
| `--color-border` | `#E0E0E0` | Card borders, table row dividers, header border |
| `--color-white` | `#FFFFFF` | Text on primary/dark backgrounds |

**Contrast**: `#C8102E` on white = ~5.9:1 (passes WCAG AA for body + large text).
White on `#C8102E` = ~5.9:1 (passes AA). `#5A5A5A` on white = ~7.1:1 (passes AAA).

**One accent rule**: `--color-primary` is the ONLY accent. No secondary accent anywhere.

---

## 2. Typography Scale

Font: **Sarabun** (Google Fonts) with system-font fallback stack.
Thai line-height: **1.7** (body) — Thai script needs more vertical space than Latin.

| Element | Size (mobile) | Size (768px+) | Weight |
|---------|---------------|---------------|--------|
| Hero h1 | `clamp(1.75rem, 8vw, 3rem)` (fluid) | `clamp(1.75rem, 8vw, 3rem)` (capped at 3rem) | 700 |
| Section title (h2) | 1.75rem (28px) | 2rem (32px) | 700 |
| Card title (h3) | 1.2rem (19px) | 1.2rem | 600 |
| Body | 17px | 18px | 400 |
| Hero tagline | 1.15rem | 1.3rem | 400 |
| Button | 1.05rem | 1.05rem | 600 |
| Caption / small | 0.85-0.9rem | 0.85-0.9rem | 400 |

> `body` has `overflow-x: hidden` as a horizontal-overflow safety net (prevents
> any wide element from causing horizontal scroll on mobile).

---

## 3. Spacing Rhythm

CSS custom properties on `:root`:

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 0.5rem (8px) | Tight gaps, card title-to-desc |
| `--space-sm` | 1rem (16px) | Container side padding (mobile), heading-to-body |
| `--space-md` | 1.5rem (24px) | Grid gaps, card padding, container side padding (768px+) |
| `--space-lg` | 2.5rem (40px) | Section intro margin, footer padding |
| `--space-xl` | 4rem (64px) | Section vertical padding |

**Radius**: `--radius` 12px (cards, figures), `--radius-sm` 8px (buttons, nav links).
**Max width**: `--max-width` 1100px (content container).
**Header height**: `--header-height` 64px.

---

## 4. Section Anatomy (MANDATORY pattern for new sections)

Every new section MUST clone this structure:

```html
<!-- ================================================================ -->
<!-- N. SECTION NAME / ชื่อส่วนภาษาไทย — คำอธิบายสั้น                    -->
<!-- ================================================================ -->
<section class="section" id="section-id">
  <div class="container">
    <h2 class="section-title">ชื่อส่วน</h2>
    <p class="section-intro">แก้ไขตรงนี้: คำอธิบาย 1-2 ประโยค</p>

    <!-- content here — repeating blocks use COPY FROM HERE / TO HERE fences -->

  </div>
</section>
```

Rules:
- Alternating section backgrounds are AUTOMATIC via `main > section:nth-of-type(even)` in the CSS.
  Never add a background class manually — new `<section class="section">` elements pasted inside
  `<main>` pick up the rhythm on their own, so copy-pasting a section can never break the pattern.
- Every `<section>` gets an `id` for anchor navigation.
- Repeating blocks (cards, images, rows, list items) are wrapped in
  `<!-- COPY FROM HERE / คัดลอกตั้งแต่ตรงนี้ -->` ... `<!-- TO HERE / ถึงตรงนี้ -->`.
- Every editable text region has `<!-- EDIT ME / แก้ไขตรงนี้: ... -->` above it.
- Every image has `<!-- SWAP IMAGE / เปลี่ยนรูปตรงนี้: ... -->` above it.

**NEW SECTIONS MUST CLONE AN EXISTING SECTION'S MARKUP PATTERN.**
Do not invent new wrapper structures, class names, or comment conventions.

---

## 5. Responsive Strategy

- **Mobile-first**: base styles target 375px viewport.
- **Breakpoint**: single breakpoint at `768px` (tablet/desktop). A secondary `600px`
  breakpoint exists only for the contact grid.
- **Grids use `auto-fit` + `minmax`**: services (240px), gallery (220px), contact (200px).
  A pasted 5th item reflows automatically — no CSS change needed.
- **Brand chips** (`.brand-chips` / `.chip`): flex-wrap pill list, `gap: var(--space-xs)`,
  `border-radius: 999px`, centered. Pasting a new `<li class="chip">` reflows automatically.
- **Header nav (mobile)**: checkbox hack (`#nav-toggle` + `<label class="nav-hamburger">`)
  opens a full-width dropdown — no JavaScript. Call button
  is icon-only on mobile (`.call-text` hidden). One shared `<nav class="header-nav">`
  serves both mobile and desktop — add/remove links in that single list only.
- **Header nav (desktop ≥768px)**: hamburger label hidden, `.header-nav` shown as an
  inline row (flex `order` puts nav between brand and call button). Call button shows icon + text.
- **Do NOT use `<details>/<summary>` for the nav**: Chrome hides closed-details children
  with a UA `!important` rule (`content-visibility: hidden`) that author CSS cannot beat —
  the desktop inline nav renders invisible. The checkbox hack is author-controlled and safe.
- **Hero**: `min-height: 70vh` (mobile) / `75vh` (768px+). Background image with dark
  gradient overlay for text contrast.

---

## 6. Accessibility Constraints

- `lang="th"` on `<html>`.
- All images have Thai `alt` text (marked `แก้ไขตรงนี้`).
- SVG icons use `aria-hidden="true"` (decorative).
- `focus-visible` outline: 3px solid `--color-primary`, offset 2px.
- Color contrast: AA minimum (body 4.5:1, large text 3:1). See palette table above.
- `prefers-reduced-motion: reduce` — disables all transitions and smooth scroll.
- Semantic landmarks: `<header>`, `<nav>`, `<main>` (wraps all content sections), `<footer>`.
- Table has `<thead>` with `scope="col"` on `<th>`.

---

## 7. Accepted Debt

- All content sections are wrapped in a single `<main>` landmark (between `<header>` and
  `<footer>`). New sections go INSIDE `<main>`, never between `<main>` and `<footer>`.
- Google Fonts loaded via `<link>` (not self-hosted). Acceptable for a local business
  page where offline use is not a concern; system-font fallback is in the stack.
- No dark mode. The brief is a trust-first local business page with a single light theme.
  Adding dark mode would complicate the maintainer's editing surface.
