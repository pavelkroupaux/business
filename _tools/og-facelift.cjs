// Obrázky pro sdílení stránky Facelift aplikace: og/og-facelift.png a og/en/og-facelift.png (1200 × 630).
// Spouštět z kořene repozitáře: node _tools/og-facelift.cjs
// Ilustrace je převzatá ze stránky služby (svg.ill-fl). Text v obrázku musí odpovídat og:image:alt na stránce.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const TXT = {
  cs: { src: 'services/facelift/index.html', out: 'og/og-facelift.png', k: 'Facelift aplikace',
        h: 'Lepší aplikace<br>bez <span class="fix">přepisu</span><br>kódu.', s: 'Design systém pro vývoj, s Figmou i bez ní.<br>Od 75 000 Kč.' },
  en: { src: 'en/services/facelift/index.html', out: 'og/en/og-facelift.png', k: 'App Facelift',
        h: 'A better app<br>without <span class="fix">rewriting</span><br>the code.', s: 'A design system for engineering,<br>with or without Figma. From €4,900.' },
};

const page = (lang, t, ill) => `<!doctype html><html lang="${lang}" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="/assets/site.css"><style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#fff}
body{position:relative;font-family:Inter,var(--display);color:var(--ink);
  background-image:radial-gradient(var(--grid) 1.4px,transparent 1.4px);background-size:26px 26px;background-position:13px 13px}
.brand{position:absolute;left:60px;top:44px;display:flex;align-items:center;gap:18px;font-size:24px;font-weight:700;letter-spacing:-.01em}
.brand img{height:58px;width:auto;display:block}
.url{position:absolute;right:62px;top:58px;font-size:22px;font-weight:500;color:var(--faint)}
.txt{position:absolute;left:64px;top:162px;width:640px}
.k{margin:0 0 18px;font-size:25px;font-weight:700;color:var(--faint)}
h1{margin:0;max-width:none;text-align:left;font-family:Inter,var(--display);font-size:74px;font-weight:700;letter-spacing:-.035em;line-height:1.02;color:var(--ink)}
.sub{margin:30px 0 0;font-size:26px;line-height:1.36;color:var(--muted)}
.ill{position:absolute;left:730px;top:210px;width:420px;height:auto}
.ill-t{font-size:15px}
</style></head><body>
<div class="brand"><img src="/logo/pk/pk-svetle.svg" alt="">Pavel Kroupa</div><span class="url">pavelkroupa.com</span>
<div class="txt"><p class="k">${t.k}</p><h1>${t.h}</h1><p class="sub">${t.s}</p></div>
${ill}
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  for (const lang of ['cs', 'en']) {
    const t = TXT[lang];
    const html = fs.readFileSync(path.join(ROOT, t.src), 'utf8');
    const m = html.match(/<svg class="ill ill-fl"[\s\S]*?<\/svg>/);
    if (!m) throw new Error('svg.ill-fl nenalezeno v ' + t.src);
    const ill = m[0].replace('class="ill ill-fl"', 'class="ill on ill-fl" aria-hidden="true"');
    const p = await browser.newPage({ viewport: { width: 1200, height: 630 } });
    await p.route('http://pk.local/**', async (r) => {
      const u = new URL(r.request().url());
      if (u.pathname === '/') return r.fulfill({ body: page(lang, t, ill), contentType: 'text/html; charset=utf-8' });
      const f = path.join(ROOT, decodeURIComponent(u.pathname));
      if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
      const type = { '.css': 'text/css', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' }[path.extname(f)];
      r.fulfill({ body: fs.readFileSync(f), contentType: type || 'application/octet-stream' });
    });
    await p.goto('http://pk.local/');
    await p.evaluate(async () => { await document.fonts.ready; document.getAnimations().forEach((a) => a.finish()); });
    await p.screenshot({ path: path.join(ROOT, t.out) });
    await p.close();
    console.log(t.out);
  }
  await browser.close();
})();
