# AGENTS.md — Instructions for AI Agents

Single-page Thai-language landing page for เกินร้อยมอเตอร์, a Bangkok motorcycle
dealer. No framework, no JS build, no dependencies. Hosted on GitHub Pages. The
human maintainer edits only `variables.txt` and `template.html` through the GitHub
web UI; `README.md` (written in Thai for the shop admin) is their guide — keep it
accurate.

## Build system (the crux)

`index.html` is **generated** — never edit it (it is gitignored and overwritten).

```
template.html  +  variables.txt  --(python3 build.py)-->  index.html
```

- `build.py` is **stdlib-only Python 3** (no pip installs, ever). It substitutes
  `{{TOKEN}}` placeholders in `template.html` with values from `variables.txt`
  and fails with bilingual Thai/English errors on: missing `=`, empty value,
  duplicate key, bad key name (`[A-Z_]+` only), or a template token with no
  matching variable.
- Adding a variable: put `{{NEW_TOKEN}}` in `template.html`, add
  `NEW_TOKEN = value` in `variables.txt`. Nothing else — build.py validates.
- Never hardcode shop facts (name, phone, address, socials, URL) in
  `template.html` — always use a token. `variables.txt` is the single source.

## Verify after any template/variables change

```bash
python3 build.py                 # must print OK
grep -c "{{" index.html          # must be 0 (no unreplaced tokens)
npx --yes html-validate@11 index.html   # same check CI runs; config: .htmlvalidate.json
open index.html                  # visual check
```

CI (`.github/workflows/pages.yml`) additionally runs **sentinel greps** that will
fail if you remove: `EDIT ME` and `คัดลอกตั้งแต่ตรงนี้` markers and `<style>`/`</style>`
from `template.html`; `</html>` and `application/ld+json` from `index.html`.
Deploy runs only on `main` after validate passes, so a red X never breaks the live site.

## Editing conventions (do not break these — they are the product)

- **Bilingual comments (Thai + English) are the maintainer interface.** Never strip
  or "clean up" comments in `template.html`, `variables.txt`, `build.py`, or the
  workflow file.
- Editable text regions carry `<!-- EDIT ME / แก้ไขตรงนี้: ... -->`; images carry
  `<!-- SWAP IMAGE / เปลี่ยนรูปตรงนี้: ... -->`. Keep the markers when editing.
- Repeating blocks (service card, gallery figure, hours row, contact card, brand
  chip) are wrapped in `COPY FROM HERE / คัดลอกตั้งแต่ตรงนี้` … `TO HERE / ถึงตรงนี้`
  fences. These are the maintainer's copy-paste units — preserve them intact.
- Site content is Thai (`<html lang="th">`); keep new user-facing text in Thai.

## Design constraints

- All design tokens are CSS custom properties on `:root` in `template.html`
  (marked `CHANGE COLORS HERE`). **One accent rule**: `--color-primary` (`#C8102E` red)
  is the only accent — no secondary accent anywhere.
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
Settings → Pages → Source must be **GitHub Actions**. Artifact path is `.`
(the repo root), so everything committed at root is published.
