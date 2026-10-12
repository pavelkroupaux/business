// Obrázky pro LinkedIn do složky linkedin/. Spouštět z kořene repozitáře: node _tools/linkedin-assets.cjs
// Kresba je z úvodu webu (svg.hx v index.html a en/index.html), texty jsou schválené věty z /ds/ (Identita).
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd(), OUT = path.join(ROOT, 'linkedin');
const TXT = {
  cs: { h: 'Pomáhám týmům <span class="fix">rozhodnout</span>, co postavit.', s: 'Funkční prototyp a hotové zadání. S AI za dny, ne týdny.' },
  en: { h: 'I help teams <span class="fix">decide</span> what to build.', s: 'A working prototype and a finished spec. With AI, in days, not weeks.' },
};
// Kresba z úvodu: celé svg, jen jiný výřez (viewBox).
function hx(lang) {
  const html = fs.readFileSync(path.join(ROOT, lang === 'cs' ? 'index.html' : 'en/index.html'), 'utf8');
  const m = html.match(/<svg class="hx"[\s\S]*?<\/svg>/);
  if (!m) throw new Error('svg.hx nenalezeno');
  return m[0].replace(/ role="img" aria-label="[^"]*"/, ' aria-hidden="true"');
}
const crop = (svg, vb, cls) => svg.replace(/class="hx" viewBox="[^"]*"/, `class="hx ${cls}" viewBox="${vb}"`);
const TANGLE = '0 30 510 380', DOC = '1590 30 410 420';

const base = (lang, w, h, body, css) => `<!doctype html><html lang="${lang}" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="/assets/site.css"><style>
html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden;background:#fff}
body{position:relative;font-family:Inter,var(--display);color:var(--ink);
  background-image:radial-gradient(var(--grid) 1.4px,transparent 1.4px);background-size:26px 26px;background-position:13px 13px}
.hx{position:absolute;width:auto;height:auto}.hx-me,.hx-bulb,.hx-lab{display:none}
h1{margin:0;max-width:none;text-align:left;font-family:Inter,var(--display);font-weight:700;letter-spacing:-.035em;line-height:1.04;color:var(--ink)}
p{margin:0;font-family:Inter,var(--display);color:var(--muted)}
.url{position:absolute;font-size:22px;font-weight:500;color:var(--faint)}
${css}</style></head><body>${body}</body></html>`;

const pages = [];
for (const lang of ['cs', 'en']) {
  const t = TXT[lang], svg = hx(lang);
  // Profil: 1584 × 396. Fotka zakrývá levý dolní roh, text je vpravo od ní.
  pages.push({ file: `linkedin-profil-${lang}.png`, w: 1584, h: 396, html: base(lang, 1584, 396,
    `${crop(svg, TANGLE, 'tg')}${crop(svg, DOC, 'dc')}
     <div class="txt"><h1>${t.h}</h1><p class="sub">${t.s}</p></div><span class="url">pavelkroupa.com</span>`,
    `.tg{left:56px;top:34px;width:300px;-webkit-mask-image:linear-gradient(to right,#000 75%,transparent);mask-image:linear-gradient(to right,#000 75%,transparent)}.dc{right:56px;top:58px;width:250px}
     .txt{position:absolute;left:440px;top:72px;width:820px}
     h1{font-size:68px}.sub{margin-top:22px;font-size:24px;line-height:1.35}
     .url{left:440px;top:300px}`) });
  // Firma, titulní obrázek: 1128 × 191. Logo firmy zakrývá levý dolní roh.
  pages.push({ file: `linkedin-firma-cover-${lang}.png`, w: 1128, h: 191, html: base(lang, 1128, 191,
    `${crop(svg, DOC, 'dc')}<div class="txt"><h1>${t.h}</h1><span class="url">pavelkroupa.com</span></div>`,
    `.dc{right:44px;top:20px;width:140px}
     .txt{position:absolute;left:210px;top:52px;width:720px}
     h1{font-size:${lang === 'cs' ? 34 : 38}px;white-space:nowrap}.url{position:static;display:block;margin-top:14px;font-size:19px}`) });
}
// Firma, logo: 400 × 400. Lepítko s fajfkou na bílém.
const sticker = fs.readFileSync(path.join(ROOT, 'logo/logo.svg'), 'utf8');
pages.push({ file: 'linkedin-firma-logo-400.png', w: 400, h: 400, html: `<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;width:400px;height:400px;background:#fff;display:grid;place-items:center}svg{width:300px;height:300px}</style></head><body>${sticker}</body></html>` });

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const p of pages) {
    const page = await browser.newPage({ viewport: { width: p.w, height: p.h } });
    await page.route('http://pk.local/**', async (r) => {
      const u = new URL(r.request().url());
      if (u.pathname === '/') return r.fulfill({ body: p.html, contentType: 'text/html; charset=utf-8' });
      const f = path.join(ROOT, decodeURIComponent(u.pathname));
      if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
      const ext = path.extname(f), type = { '.css': 'text/css', '.webp': 'image/webp', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' }[ext];
      r.fulfill({ body: fs.readFileSync(f), contentType: type || 'application/octet-stream' });
    });
    await page.goto('http://pk.local/');
    await page.evaluate(async () => { await document.fonts.ready; document.getAnimations().forEach((a) => a.finish()); });
    await page.screenshot({ path: path.join(OUT, p.file) });
    await page.close();
    console.log('linkedin/' + p.file);
  }
  await browser.close();
})();
