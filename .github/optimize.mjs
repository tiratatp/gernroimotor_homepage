// ============================================================
// optimize.mjs — optimize the built site in GitHub Actions only.
// Optimize the BUILT site before deploy: shrink images, make WebP
// copies, switch references to WebP, then minify every built HTML
// page (see HTML_PAGES below) and style.css.
//
// CI-ONLY script — the maintainer never runs this. It runs in the
// deploy job AFTER build.py, so it edits the generated HTML pages
// (never the *-template.html sources) and the deploy copy of
// style.css. Local testing: see pages.yml deploy job.
//
// What it does:
//      Resize every images/*.jpg|png to max 1200px and recompress.
//      Create a .webp sibling next to each image.
//      Rewrite each HTML page's references to WebP with JPEG/PNG fallback.
//      Rewrite style.css url() references to WebP, then minify it.
//      Minify each HTML page (strip comments/whitespace) and re-verify.
// ============================================================

import { createRequire } from "node:module";
import { readdirSync, readFileSync, writeFileSync, statSync, existsSync } from "node:fs";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";

// sharp + html-minifier-terser + clean-css are installed OUTSIDE the repo
// (runner temp dir) so node_modules never lands in the Pages artifact —
// see pages.yml.
const require = createRequire(
  (process.env.OPTIMIZER_MODULES || ".") + "/"
);
const sharp = require("sharp");
const { minify } = require("html-minifier-terser");
const CleanCSS = require("clean-css");

const ROOT = join(fileURLToPath(import.meta.url), "..", "..");
const IMAGES_DIR = join(ROOT, "images");
const STYLE_CSS = join(ROOT, "style.css");
// Every HTML page build.py generates — keep this list in sync with build.py's
// PAGES list so every published page gets the same WebP rewrite + minify pass.
const HTML_PAGES = ["index.html", "ev-models.html"].map((name) => join(ROOT, name));

// Tuning knobs.
const MAX_DIMENSION = 1200;   // px — enough for common mobile and desktop displays
const JPEG_QUALITY = 80;
const WEBP_QUALITY = 78;

function fail(th, en) {
  console.error("ERROR / ข้อผิดพลาด: " + th);
  console.error("(" + en + ")");
  process.exit(1);
}

function kb(bytes) {
  return (bytes / 1024).toFixed(1) + " KB";
}

// ---- Steps 1 and 2: images ----------------------------------------------
// Returns a Set of webp filenames that now exist in images/ (e.g. "shop-front")
async function optimizeImages() {
  if (!existsSync(IMAGES_DIR)) {
    console.log("ไม่มีโฟลเดอร์ images/ — ข้ามขั้นตอนรูปภาพ (no images/ dir, skipping)");
    return new Set();
  }
  const files = readdirSync(IMAGES_DIR).filter((f) =>
    /\.(jpe?g|png)$/i.test(f)
  );
  const webpReady = new Set();

  for (const file of files) {
    const path = join(IMAGES_DIR, file);
    const name = file.replace(/\.(jpe?g|png)$/i, "");
    const before = statSync(path).size;
    const isPng = /\.png$/i.test(file);

    // rotate() respects phone-camera EXIF orientation before resizing.
    let pipeline = sharp(path).rotate().resize({
      width: MAX_DIMENSION,
      height: MAX_DIMENSION,
      fit: "inside",
      withoutEnlargement: true, // Never upscale.
    });

    // Overwrite the original with the optimized version (old-browser fallback).
    const optimized = isPng
      ? await pipeline.png({ compressionLevel: 9 }).toBuffer()
      : await pipeline.jpeg({ quality: JPEG_QUALITY, mozjpeg: true }).toBuffer();
    writeFileSync(path, optimized);

    // Create the WebP sibling.
    const webpPath = join(IMAGES_DIR, name + ".webp");
    await sharp(optimized).webp({ quality: WEBP_QUALITY }).toFile(webpPath);

    webpReady.add(name);
    console.log(
      `ย่อรูป ${file}: ${kb(before)} → ${kb(statSync(path).size)}` +
      ` (+ ${name}.webp ${kb(statSync(webpPath).size)})`
    );
  }
  return webpReady;
}

// ---- Step 3: rewrite references to WebP ---------------------------------
// Only relative "images/..." references are rewritten. Absolute URLs
// (og:image, JSON-LD) keep JPEG/PNG for Facebook/LINE crawlers.
function rewriteToWebp(html, webpReady) {
  const forName = (name) => (webpReady.has(name) ? name : null);

  // <img src="images/x.jpg" ...> → <picture> with WebP source + JPEG fallback
  // (single-line img tags — the template's copy-paste blocks keep them so)
  html = html.replace(
    /<img\s+([^>]*?)src="images\/([^"]+?)\.(jpe?g|png)"([^>]*)>/g,
    (match, before, name, ext, after) => {
      if (!forName(name)) return match; // Keep the original if WebP is unavailable.
      return (
        `<picture><source srcset="images/${name}.webp" type="image/webp">` +
        `<img ${before}src="images/${name}.${ext}"${after}></picture>`
      );
    }
  );

  // <link rel="preload" as="image" href="images/x.jpg"> → webp
  // Must match the style.css url() rewrite or the browser downloads twice.
  html = html.replace(
    /(<link[^>]*rel="preload"[^>]*href=")images\/([^"]+?)\.(jpe?g|png)(")/g,
    (match, pre, name, ext, post) =>
      forName(name) ? `${pre}images/${name}.webp${post}` : match
  );

  return html;
}

// ---- Step 3b: rewrite and minify style.css ------------------------------
// The hero background url("images/...") lives here. Rewriting to WebP loses
// no fallback because CSS backgrounds never had one (unchanged behavior).
function rewriteAndMinifyCss(webpReady) {
  if (!existsSync(STYLE_CSS)) {
    fail("ไม่พบไฟล์ style.css", "style.css is missing");
  }
  let css = readFileSync(STYLE_CSS, "utf8");
  const before = Buffer.byteLength(css);
  css = css.replace(
    /url\("images\/([^")]+?)\.(jpe?g|png)"\)/g,
    (match, name) =>
      webpReady.has(name) ? `url("images/${name}.webp")` : match
  );
  const result = new CleanCSS({ level: 2 }).minify(css);
  if (result.errors.length > 0) {
    fail("ย่อ style.css ไม่สำเร็จ", "clean-css failed: " + result.errors.join("; "));
  }
  for (const warning of result.warnings) {
    console.log("clean-css warning: " + warning);
  }
  const minified = result.styles;
  if (!minified.includes(":root")) {
    fail("style.css ที่ย่อแล้วไม่มี :root", "minified style.css lost :root");
  }
  if (minified.includes("{{")) {
    fail("style.css ยังมีตัวแปร {{...}} ที่ไม่ได้แทนค่า", "unreplaced {{TOKEN}} remains in style.css");
  }
  writeFileSync(STYLE_CSS, minified);
  console.log(
    `ย่อ style.css: ${kb(before)} → ${kb(statSync(STYLE_CSS).size)} (minified)`
  );
}

// ---- Step 4: minify and verify ------------------------------------------
async function minifyAndVerify(html, pageName) {
  const result = await minify(html, {
    collapseWhitespace: true,
    removeComments: true,
    minifyCSS: true,
    removeRedundantAttributes: true,
    sortClassName: false,
    minifyJS: false, // Never touch JSON-LD script bodies.
  });

  // Re-verify the output before deploy.
  if (!result.includes("</html>")) {
    fail(`${pageName} ที่ย่อแล้วไม่มีแท็กปิด </html>`, `minified ${pageName} lost </html>`);
  }
  const ldBlocks = [...result.matchAll(
    /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g
  )];
  if (ldBlocks.length === 0) {
    fail(`${pageName} ที่ย่อแล้วไม่มี JSON-LD`, `minified ${pageName} lost JSON-LD`);
  }
  for (const block of ldBlocks) {
    try {
      JSON.parse(block[1]); // JSON-LD must stay valid.
    } catch {
      fail(`JSON-LD เสียหลังการย่อไฟล์ (${pageName})`, `JSON-LD broke during minification (${pageName})`);
    }
  }
  if (result.includes("{{")) {
    fail(`${pageName} ยังมีตัวแปร {{...}} ที่ไม่ได้แทนค่า`, `unreplaced {{TOKEN}} remains in ${pageName}`);
  }
  return result;
}

const webpReady = await optimizeImages();
for (const htmlPath of HTML_PAGES) {
  const pageName = htmlPath.slice(ROOT.length + 1);
  const before = statSync(htmlPath).size;
  let html = readFileSync(htmlPath, "utf8");
  html = rewriteToWebp(html, webpReady);
  html = await minifyAndVerify(html, pageName);
  writeFileSync(htmlPath, html);
  console.log(
    `ย่อ ${pageName}: ${kb(before)} → ${kb(statSync(htmlPath).size)} (minified)`
  );
}
rewriteAndMinifyCss(webpReady);
console.log("OK: เว็บพร้อมเผยแพร่ (site optimized and ready to deploy)");
