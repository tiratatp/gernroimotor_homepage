# AGENTS.md — Instructions for AI Agents

Single-page Thai-language landing page for เกินร้อยมอเตอร์, a Bangkok motorcycle
dealer. No framework, no JS build, no dependencies. Hosted on GitHub Pages. The
human maintainer edits only `variables.txt`, `template.html`, and `style.css`
(colors section only) through the GitHub
web UI; `README.md` (written in Thai for the shop admin) is their guide — keep it
accurate.

## Build system (the crux)

`index.html` is **generated** — never edit it (it is gitignored and overwritten).
Same for `robots.txt` and `sitemap.xml` — build.py generates them from `SITE_URL`.

```
template.html  +  variables.txt  --(python3 build.py)-->  index.html  (+ robots.txt, sitemap.xml)
```

- `build.py` is **stdlib-only Python 3** (no pip installs, ever). It substitutes
  `{{TOKEN}}` placeholders in `template.html` with values from `variables.txt`
  and fails with bilingual Thai/English errors on: missing `=`, empty value,
  duplicate key, bad key name (`[A-Z_]+` only), or a template token with no
  matching variable. It also rejects malformed/unmatched placeholders and
  invalid URL, phone, postal-code, or social-identifier formats.
- Adding a variable: put `{{NEW_TOKEN}}` in `template.html`, add
  `NEW_TOKEN = value` in `variables.txt`. Nothing else — build.py validates.
- Never hardcode shop facts (name, phone, address, socials, URL) in
  `template.html` — always use a token. `variables.txt` is the single source.

## Deploy-time optimization (CI only)

The build job runs `.github/optimize.mjs` (Node, sharp + html-minifier-terser +
clean-css, installed into `$RUNNER_TEMP` so `node_modules` never enters the artifact)
after tests and `build.py`. It validates and uploads that same **built** output;
`template.html` and `style.css` stay readable:

- Every `images/*.jpg|png` is resized to ≤1200px (no upscale), EXIF-rotated,
  recompressed, and gets a `.webp` sibling.
- In `index.html`, relative `images/...` references are switched to the WebP:
  `<img>` becomes `<picture>` (JPEG/PNG fallback kept) and `<link rel="preload">`
  is rewritten. **Absolute** URLs (`og:image`, JSON-LD → `og-cover.jpg`) keep JPEG
  for Facebook/LINE crawlers.
- `style.css` gets its hero `url("images/...")` rewritten to the WebP (no CSS
  fallback — background images can't do `<picture>`-style fallbacks, unchanged
  behavior) and is then minified with clean-css level 2 (self-checks: `:root`
  survives, no `{{` tokens).
- `index.html` is then minified (comments/whitespace stripped) and self-checked
  (`</html>`, both JSON-LD blocks must parse, no `{{` tokens).
- The build job rejects non-JPG/PNG files and images > 5 MB.
- `images/*.webp` is gitignored — WebP exists only in the deployed artifact.
- Local preview note: the script is CI-only; running it locally requires
  `OPTIMIZER_MODULES=<dir with sharp + html-minifier-terser + clean-css> node .github/optimize.mjs`
  and it rewrites `images/` in place.

## Verify after any template/variables change

```bash
python3 -m unittest discover -s tests -v
python3 build.py                 # must print OK
grep -c "{{" index.html          # must be 0 (no unreplaced tokens)
npx --yes html-validate@11.9.0 index.html   # same check CI runs; config: .htmlvalidate.json
open index.html                  # visual check
```

CI (`.github/workflows/pages.yml`) additionally runs **sentinel greps** that will
fail if you remove: `EDIT ME` and `คัดลอกตั้งแต่ตรงนี้` markers from
`template.html`, the `style.css` stylesheet link from `template.html`,
`style.css` itself, and `</html>` and `application/ld+json` from `index.html`.
Deploy runs only on `main` after validate passes, so a red X never breaks the live site.

## Editing conventions (do not break these — they are the product)

- Preserve bilingual maintainer comments in `template.html`, `variables.txt`, and
  `style.css`. Comments in `*.py` and `.github/*` are English-only; runtime errors and
  user-facing text remain bilingual or Thai as appropriate.
- Editable text regions carry `<!-- EDIT ME / แก้ไขตรงนี้: ... -->`; images carry
  `<!-- SWAP IMAGE / เปลี่ยนรูปตรงนี้: ... -->` (the hero background's marker is a
  `/* SWAP IMAGE ... */` comment in `style.css`). Keep the markers when editing.
- Repeating blocks (service card, gallery figure, hours row, contact card, brand
  chip) are wrapped in `COPY FROM HERE / คัดลอกตั้งแต่ตรงนี้` … `TO HERE / ถึงตรงนี้`
  fences. These are the maintainer's copy-paste units — preserve them intact.
- Site content is Thai (`<html lang="th">`); keep new user-facing text in Thai.

## Design constraints

- All design tokens are CSS custom properties on `:root` in `style.css`
  (marked `CHANGE COLORS HERE`). **One accent rule**: `--color-primary` (`#C8102E` red)
  is the only accent — no secondary accent anywhere.
- **No inline styles, no `<style>` tag.** All CSS lives in `style.css`; enforce with
  scoped selectors there (both rules are active in `.htmlvalidate.json` and covered
  by tests).
- Font: Sarabun (Google Fonts) with system fallback; Thai body line-height **1.7**.
- **New sections must clone an existing section's markup** — same
  `<section class="section" id="…">` + `.container` + `.section-title` structure,
  inside `<main>` (never between `</main>` and `<footer>`). Alternating section
  backgrounds are automatic via `main > section:nth-of-type(even)` — never add a
  background class manually.
- Mobile-first, single breakpoint at **768px** (plus 600px for the contact grid
  only). Grids use `auto-fit` + `minmax` so pasted items reflow with no CSS change.
- Header mobile nav uses the **checkbox hack** (`#nav-toggle`). Do **not** switch it
  to `<details>`/`<summary>` — Chrome's UA `content-visibility: hidden !important`
  on closed details makes the desktop inline nav invisible.
- Accessibility: WCAG AA contrast minimum, Thai `alt` text on all images,
  `aria-hidden="true"` on decorative SVGs, `focus-visible` outline
  (3px `--color-primary`), `prefers-reduced-motion: reduce` disables transitions.
- Accepted debt: no dark mode, no self-hosted fonts, single `<main>` landmark.

## Deployment

Deployed by the Actions workflow, **not** "Deploy from branch" — repo
Settings → Pages → Source must be **GitHub Actions**. The workflow stages `_site`
with only `index.html`, `style.css`, `robots.txt`, `sitemap.xml`, optimized `images/`, and an
optional `CNAME`; source files, tests, workflows, and README are not published.
