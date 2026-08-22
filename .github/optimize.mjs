// ============================================================
// optimize.mjs — สคริปต์ย่อไฟล์สำหรับเว็บจริง (รันใน GitHub Actions เท่านั้น)
// Optimize the BUILT site before deploy: shrink images, make WebP
// copies, switch references to WebP, then minify index.html.
//
// CI-ONLY script — the maintainer never runs this. It runs in the
// deploy job AFTER build.py, so it edits the generated index.html
// (never template.html). Local testing: see pages.yml deploy job.
//
// ขั้นตอน / What it does:
//   1. ย่อรูปใน images/ ให้กว้างไม่เกิน 1200px + บีบอัดใหม่
//      Resize every images/*.jpg|png to max 1200px and recompress.
//   2. สร้างไฟล์ .webp คู่กันทุกรูป (เบราว์เซอร์ใหม่เกือบทั้งหมดอ่านได้)
//      Create a .webp sibling next to each image.
//   3. แก้ index.html ให้ใช้ .webp (img → <picture>, url() ใน CSS, preload)
//      Rewrite index.html references to WebP with JPEG/PNG fallback.
//   4. ย่อ index.html (ตัดคอมเมนต์/ช่องว่าง) แล้วตรวจความถูกต้องอีกครั้ง
//      Minify index.html (strip comments/whitespace) and re-verify.
// ============================================================

import { createRequire } from "node:module";
import { readdirSync, readFileSync, writeFileSync, statSync, existsSync } from "node:fs";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";

// sharp + html-minifier-terser are installed OUTSIDE the repo (runner temp
// dir) so node_modules never lands in the Pages artifact — see pages.yml.
// ติดตั้ง dependencies ไว้นอก repo เพื่อไม่ให้ node_modules หลุดไปในเว็บจริง
const require = createRequire(
  (process.env.OPTIMIZER_MODULES || ".") + "/"
);
const sharp = require("sharp");
const { minify } = require("html-minifier-terser");

const ROOT = join(fileURLToPath(import.meta.url), "..", "..");
const IMAGES_DIR = join(ROOT, "images");
const INDEX_HTML = join(ROOT, "index.html");

// ขนาด/คุณภาพ / Tuning knobs
const MAX_DIMENSION = 1200;   // px — พอสำหรับจอมือถือ/เดสก์ท็อปทั่วไป (retina 2x ของการ์ด 600px)
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

// ---- Step 1+2: images / รูปภาพ ------------------------------------------
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

    // rotate() = หมุนตาม EXIF ของรูปถ่ายมือถือก่อน แล้วค่อยย่อ
    // rotate() respects phone-camera EXIF orientation before resizing.
    let pipeline = sharp(path).rotate().resize({
      width: MAX_DIMENSION,
      height: MAX_DIMENSION,
      fit: "inside",
      withoutEnlargement: true, // รูปเล็กอยู่แล้วไม่ขยาย / never upscale
    });

    // 1) เขียนทับไฟล์เดิมด้วยเวอร์ชันที่ย่อแล้ว (เป็น fallback ให้เบราว์เซอร์เก่า)
    //    Overwrite the original with the optimized version (old-browser fallback).
    const optimized = isPng
      ? await pipeline.png({ compressionLevel: 9 }).toBuffer()
      : await pipeline.jpeg({ quality: JPEG_QUALITY, mozjpeg: true }).toBuffer();
    writeFileSync(path, optimized);

    // 2) สร้าง .webp คู่กัน / Create the WebP sibling.
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

// ---- Step 3: rewrite references to WebP / เปลี่ยนการอ้างอิงเป็น WebP ------
// แก้เฉพาะการอ้างอิงแบบ relative "images/..." เท่านั้น — og:image / JSON-LD
// ที่เป็น URL เต็ม ({{SITE_URL}}images/...) จะไม่ถูกแตะ เพราะ crawler ของ
// Facebook/LINE ยังต้องการ JPEG/PNG
// Only relative "images/..." references are rewritten. Absolute URLs
// (og:image, JSON-LD) keep JPEG/PNG for Facebook/LINE crawlers.
function rewriteToWebp(html, webpReady) {
  const forName = (name) => (webpReady.has(name) ? name : null);

  // <img src="images/x.jpg" ...> → <picture> with WebP source + JPEG fallback
  // (single-line img tags — the template's copy-paste blocks keep them so)
  html = html.replace(
    /<img\s+([^>]*?)src="images\/([^"]+?)\.(jpe?g|png)"([^>]*)>/g,
    (match, before, name, ext, after) => {
      if (!forName(name)) return match; // ไม่มี webp ก็ใช้ไฟล์เดิม / no webp → keep
      return (
        `<picture><source srcset="images/${name}.webp" type="image/webp">` +
        `<img ${before}src="images/${name}.${ext}"${after}></picture>`
      );
    }
  );

  // url("images/x.jpg") ใน CSS (รูปพื้นหลัง hero) → webp
  // CSS background url() (hero image) → webp
  html = html.replace(
    /url\("images\/([^")]+?)\.(jpe?g|png)"\)/g,
    (match, name) =>
      forName(name) ? `url("images/${name}.webp")` : match
  );

  // <link rel="preload" as="image" href="images/x.jpg"> → webp
  // (ต้องตรงกับ url() ใน CSS ไม่งั้นเบราว์เซอร์โหลดรูปสองครั้ง)
  // Must match the CSS url() or the browser downloads the image twice.
  html = html.replace(
    /(<link[^>]*rel="preload"[^>]*href=")images\/([^"]+?)\.(jpe?g|png)(")/g,
    (match, pre, name, ext, post) =>
      forName(name) ? `${pre}images/${name}.webp${post}` : match
  );

  return html;
}

// ---- Step 4: minify + verify / ย่อและตรวจสอบ ------------------------------
async function minifyAndVerify(html) {
  const result = await minify(html, {
    collapseWhitespace: true,
    removeComments: true,
    minifyCSS: true,
    removeRedundantAttributes: true,
    sortClassName: false,
    minifyJS: false, // ห้ามแตะ JSON-LD / never touch JSON-LD script bodies
  });

  // ตรวจผลลัพธ์อีกครั้งก่อนเผยแพร่ / Re-verify the output before deploy.
  if (!result.includes("</html>")) {
    fail("index.html ที่ย่อแล้วไม่มีแท็กปิด </html>", "minified index.html lost </html>");
  }
  const ldBlocks = [...result.matchAll(
    /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g
  )];
  if (ldBlocks.length === 0) {
    fail("index.html ที่ย่อแล้วไม่มี JSON-LD", "minified index.html lost JSON-LD");
  }
  for (const block of ldBlocks) {
    try {
      JSON.parse(block[1]); // JSON-LD ต้อง parse ได้เสมอ / must stay valid JSON
    } catch {
      fail("JSON-LD เสียหลังการย่อไฟล์", "JSON-LD broke during minification");
    }
  }
  if (result.includes("{{")) {
    fail("index.html ยังมีตัวแปร {{...}} ที่ไม่ได้แทนค่า", "unreplaced {{TOKEN}} remains");
  }
  return result;
}

const webpReady = await optimizeImages();
const before = statSync(INDEX_HTML).size;
let html = readFileSync(INDEX_HTML, "utf8");
html = rewriteToWebp(html, webpReady);
html = await minifyAndVerify(html);
writeFileSync(INDEX_HTML, html);
console.log(
  `ย่อ index.html: ${kb(before)} → ${kb(statSync(INDEX_HTML).size)} (minified)`
);
console.log("OK: เว็บพร้อมเผยแพร่ (site optimized and ready to deploy)");
