// Obrázky pro LinkedIn do složky linkedin/. Spouštět z kořene repozitáře: node _tools/linkedin-assets.cjs
// Zamotaná čára je z úvodu webu, lepítko z logo/logo.svg, texty jsou schválené věty z /ds/ (Identita).
// Profil a titulní obrázek se ukládají ve dvojnásobném rozlišení, aby byly ostré i po zmenšení na LinkedInu.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd(), OUT = path.join(ROOT, 'linkedin');
const TXT = {
  cs: { h: 'Pomáhám týmům <span class="fix">rozhodnout</span>, co postavit.', s: 'Funkční prototyp a hotové zadání. S AI za dny, ne týdny.' },
  en: { h: 'I help teams <span class="fix">decide</span> what to build.', s: 'A working prototype and a finished spec. With AI, in days, not weeks.' },
};
// Zamotaná čára z úvodu (začátek path.hx-one v en/index.html), bez dlouhého konce k portrétu.
function tangle() {
  const html = fs.readFileSync(path.join(ROOT, 'en/index.html'), 'utf8');
  const d = (html.match(/<path class="hx-one" d="([^"]*)"/) || [])[1];
  const cut = d && d.indexOf('C221.379');
  if (!d || cut < 0) throw new Error('path.hx-one nenalezena');
  return d.slice(0, cut); // končí v bodě 216.348 64.2667
}
// Lepítko s fajfkou z logo/logo.svg, vložené do kresby na x, y o velikosti w.
const STICKER = fs.readFileSync(path.join(ROOT, 'logo/logo.svg'), 'utf8');
const sticker = (x, y, w) => STICKER.replace(/<svg [^>]*viewBox="([^"]*)">/, `<svg x="${x}" y="${y}" width="${w}" height="${w}" viewBox="$1">`);
// Ručně tažená čára: body proložené křivkou, s malým chvěním (stejné při každém spuštění).
function hand(pts, seed) {
  let r = seed; const rnd = () => ((r = (r * 16807) % 2147483647) / 2147483647 - 0.5) * 3;
  const q = pts.map(([x, y], i) => (i && i < pts.length - 1 ? [x + rnd(), y + rnd()] : [x, y]));
  let d = `M${q[0][0]} ${q[0][1]}`;
  for (let i = 0; i < q.length - 1; i++) {
    const a = q[i - 1] || q[i], b = q[i], c = q[i + 1], e = q[i + 2] || c;
    d += `C${(b[0] + (c[0] - a[0]) / 6).toFixed(1)} ${(b[1] + (c[1] - a[1]) / 6).toFixed(1)} ${(c[0] - (e[0] - b[0]) / 6).toFixed(1)} ${(c[1] - (e[1] - b[1]) / 6).toFixed(1)} ${c[0].toFixed(1)} ${c[1].toFixed(1)}`;
  }
  return d;
}
const STROKE = 'fill="none" stroke="#111111" stroke-linecap="round" stroke-linejoin="round"';

const base = (lang, w, h, body, css) => `<!doctype html><html lang="${lang}" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="/assets/site.css"><style>
html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden;background:#fff}
body{position:relative;font-family:Inter,var(--display);color:var(--ink);
  background-image:radial-gradient(var(--grid) 1.4px,transparent 1.4px);background-size:26px 26px;background-position:13px 13px}
.art{position:absolute;inset:0}
h1{margin:0;max-width:none;text-align:left;font-family:Inter,var(--display);font-weight:700;letter-spacing:-.035em;line-height:1.04;color:var(--ink)}
p{margin:0;font-family:Inter,var(--display);color:var(--muted)}
.txt{position:absolute}.url{display:block;font-size:22px;font-weight:500;color:var(--faint)}
${css}</style></head><body>${body}</body></html>`;

const T = tangle(), pages = [];
// Profil: 1584 × 396. Fotka zakrývá levý dolní roh (asi x 40–390, y od 200).
// Zamotaná čára je nad fotkou, čára vede mezi fotkou a textem pod text a končí u lepítka.
const S = 1.15, TX = 48, TY = 22, END = [TX + 216.348 * S, TY + 64.2667 * S];
const LINE = hand([END, [335, 118], [378, 176], [412, 248], [452, 312], [520, 346], [640, 352], [800, 346], [960, 352], [1120, 347], [1250, 350], [1328, 334], [1366, 284]], 7);
const profileArt = `<svg class="art" viewBox="0 0 1584 396" aria-hidden="true">
  <path d="${T}" ${STROKE} stroke-width="${(6.2 / S).toFixed(2)}" transform="translate(${TX} ${TY}) scale(${S})"/>
  <path d="${LINE}" ${STROKE} stroke-width="6.2"/>${sticker(1340, 96, 196)}</svg>`;
// Firma, titulní obrázek: 1128 × 191. Logo firmy zakrývá levý dolní roh a na mobilu se okraje ořízne,
// proto je všechno uprostřed: nadpis nahoře, pod ním čára z úvodu (zamotaná čára, šipka) a lepítko místo dokumentu.
function homeLine() {
  const html = fs.readFileSync(path.join(ROOT, 'en/index.html'), 'utf8');
  const one = (html.match(/<path class="hx-one" d="([^"]*)"/) || [])[1];
  const arrow = (html.match(/<path class="hx-r" d="(M1476 190[^"]*)"/) || [])[1];
  if (!one || !arrow) throw new Error('čára z úvodu nenalezena');
  return `<path d="${one}" ${STROKE} stroke-width="4.55" transform="translate(4 30) scale(2.86)"/><path d="${arrow}" ${STROKE} stroke-width="13"/>${sticker(1560, 92, 238)}`;
}
const coverArt = `<svg class="line" viewBox="0 20 1810 350" aria-hidden="true">${homeLine()}</svg>`;
for (const lang of ['cs', 'en']) {
  const t = TXT[lang];
  pages.push({ file: `linkedin-profil-${lang}.png`, w: 1584, h: 396, html: base(lang, 1584, 396,
    `${profileArt}<div class="txt"><h1>${t.h}</h1><p class="sub">${t.s}</p><span class="url">pavelkroupa.com</span></div>`,
    `.txt{left:486px;top:58px;width:820px}h1{font-size:64px}.sub{margin-top:20px;font-size:23px;line-height:1.35}.url{margin-top:16px;font-size:20px}`) });
  pages.push({ file: `linkedin-firma-cover-${lang}.png`, w: 1128, h: 191, html: base(lang, 1128, 191,
    `<div class="txt"><h1>${t.h}</h1></div>${coverArt}`,
    `.txt{left:0;right:0;top:26px;text-align:center}h1{display:inline-block;font-size:${lang === 'cs' ? 28 : 30}px;white-space:nowrap}
     .line{position:absolute;left:50%;top:76px;width:540px;transform:translateX(-50%)}`) });
}
// Firma, logo: 400 × 400. Logo pk ve čtverci na bílém (logo/pk/pk-svetle-ctverec.svg).
const PK = fs.readFileSync(path.join(ROOT, 'logo/pk/pk-svetle-ctverec.svg'), 'utf8');
pages.push({ file: 'linkedin-firma-logo-400.png', w: 400, h: 400, html: `<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;width:400px;height:400px;background:#fff}svg{display:block;width:400px;height:400px}</style></head><body>${PK}</body></html>` });

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const p of pages) {
    const page = await browser.newPage({ viewport: { width: p.w, height: p.h }, deviceScaleFactor: p.w > 400 ? 2 : 1 });
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
