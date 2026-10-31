// PDF ke službám: dvě strany A4 pro toho, kdo schvaluje rozpočet (strana 1) a kdo to prověřuje (strana 2).
// Spouštět z kořene repozitáře: node _tools/onepagers.cjs  → pdf/*.pdf
// S PREVIEW=<složka> uloží i náhledy stran jako PNG. Texty jsou v _tools/onepagers.data.cjs.
// Když se obsah nevejde na stranu, skript skončí chybou a řekne kde.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const { WHY, UI, SERVICES } = require('./onepagers.data.cjs');

const ROOT = process.cwd(), OUT = path.join(ROOT, 'pdf'), PREVIEW = process.env.PREVIEW;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const link = (s) => esc(s).replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2">$1</a>');
const G = '<div class="gap"></div>';
const SQ = '<rect x="3.5" y="3.5" width="17" height="17" rx="3" fill="none" stroke="#111" stroke-width="1.5"/>';
const ICON = {
  part: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12V3.5h5.5a3 3 0 0 1 3 3V12z" fill="#FFCE1B"/><path d="M12 3.5V12h8.5" fill="none" stroke="#111" stroke-width="1.5"/>${SQ}</svg>`,
  full: `<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="3" fill="#FFCE1B"/>${SQ}</svg>`,
  dark: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5H12v17H6.5a3 3 0 0 1-3-3v-11a3 3 0 0 1 3-3z" fill="#FFCE1B"/><path d="M12 3.5h5.5a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H12z" fill="#111"/>${SQ}</svg>`,
};
const cal = (n) => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4.5h12a3 3 0 0 1 3 3v2.5H3V7.5a3 3 0 0 1 3-3z" fill="#FFCE1B"/><rect x="3" y="4.5" width="18" height="16.5" rx="3" fill="none" stroke="#111" stroke-width="1.5"/><path d="M3 10h18" stroke="#111" stroke-width="1.5"/><path d="M8 2.6v3.6M16 2.6v3.6" stroke="#111" stroke-width="1.6" stroke-linecap="round"/><text x="12" y="18.6" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="8.4" font-weight="800" fill="#111">${n}</text></svg>`;
const rich = (s) => esc(s).replace(/&lt;mark&gt;/g, '<mark>').replace(/&lt;\/mark&gt;/g, '</mark>');

const CSS = `
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#111;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:10.5pt;line-height:1.45}
.page{width:210mm;height:297mm;padding:13mm 15mm 11mm;display:flex;flex-direction:column;overflow:hidden;page-break-after:always;position:relative}
.page:last-child{page-break-after:auto}
.ph{display:flex;justify-content:space-between;font-size:8.5pt;color:#5B5B55;margin-bottom:7.5mm}
.ph b{color:#111}
.eyebrow{margin:0 0 3mm;font-size:8pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#5B5B55}
h1{margin:0 0 4mm;font-size:25pt;line-height:1.08;letter-spacing:-.025em;font-weight:800;max-width:165mm}
mark{background:none;color:inherit;padding:0 .04em;position:relative;z-index:0;white-space:nowrap}
mark::before{content:"";position:absolute;left:0;right:0;bottom:.04em;height:.4em;background:#FFCE1B;z-index:-1}
.lede{margin:0 0 5mm;font-size:11.5pt;line-height:1.5;color:#2b2b28;max-width:165mm}
.k{margin:0 0 2.6mm;font-size:8pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#111}
.sit{display:flex;gap:5mm;align-items:flex-start;background:#F3F2EE;border-radius:4mm;padding:3.4mm 5mm;margin-bottom:4.8mm}
.pill{flex:none;background:#111;color:#FFCE1B;font-size:7.5pt;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:1.4mm 2.6mm;border-radius:1.5mm;margin-top:.3mm}
.sit p{margin:0}.sit ul{margin:0;padding-left:4.2mm}.sit li{margin:0 0 .6mm}
.gets{display:grid;gap:3mm;margin-bottom:4.8mm}.gets.n3{grid-template-columns:repeat(3,1fr)}.gets.n4{grid-template-columns:repeat(4,1fr)}
.card{border:1px solid #E1E0DA;border-radius:3.5mm;padding:3.4mm 3.6mm}
.card b{display:block;font-size:10pt;margin-bottom:1.2mm;line-height:1.25}
.card span{display:block;font-size:9pt;color:#4a4a45;line-height:1.4}
.also{margin:-2.5mm 0 5.5mm;font-size:9.5pt;color:#2b2b28;border-left:2.2mm solid #FFCE1B;padding:.6mm 0 .6mm 3.4mm}
.price{display:grid;grid-template-columns:52mm 1fr;gap:3mm;margin-bottom:4.8mm}
.pbox{background:#FFCE1B;border-radius:3.5mm;padding:4mm}
.pbox .amt{display:block;font-size:17pt;font-weight:800;letter-spacing:-.02em;line-height:1.1}
.pbox .vat{display:block;font-size:8.5pt;font-weight:700;margin:1mm 0 2.4mm}
.pbox .term{display:block;font-size:8.8pt;line-height:1.4}
.pmain{border:1px solid #E1E0DA;border-radius:3.5mm;padding:3.6mm 4mm;display:flex;flex-direction:column;gap:2.6mm}
.tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.tier i{display:block;font-style:normal;font-size:7.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5B5B55}
.tier b{display:block;font-size:9.6pt;margin:.6mm 0 .8mm;line-height:1.25}
.tier span{display:block;font-size:8.6pt;color:#4a4a45;line-height:1.35}
.ptext{margin:0;font-size:9.2pt;line-height:1.45}
.inc{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 4mm;font-size:9pt}
.inc li{padding-left:4.6mm;position:relative}.inc li::before{content:"";position:absolute;left:0;top:1.4mm;width:2.2mm;height:1.2mm;border-left:.5mm solid #111;border-bottom:.5mm solid #111;transform:rotate(-45deg)}
.aff{display:flex;flex-wrap:wrap;gap:1.6mm;align-items:center;font-size:8.4pt}
.aff em{font-style:normal;font-weight:700;margin-right:1mm}
.aff span{border:1px solid #D8D7D0;border-radius:10mm;padding:.5mm 2.4mm}
.pnote{font-size:8.4pt;color:#5B5B55;margin:0}
.why{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm 7mm}
.why div{border-left:1.2mm solid #FFCE1B;padding-left:3mm}
.why b{display:block;font-size:9.8pt;margin-bottom:.6mm}.why span{display:block;font-size:8.9pt;color:#4a4a45;line-height:1.4}
.steps{list-style:none;margin:0 0 2.6mm;padding:0;display:grid;gap:3mm}
.steps.n3{grid-template-columns:repeat(3,1fr)}.steps.n4{grid-template-columns:repeat(4,1fr)}
.steps li{background:#F3F2EE;border-radius:3.5mm;padding:3.4mm 3.6mm}
.steps .no{display:inline-flex;width:6mm;height:6mm;border-radius:50%;background:#FFCE1B;align-items:center;justify-content:center;font-weight:800;font-size:8.5pt;margin-bottom:1.6mm}
.steps b{display:block;font-size:10pt;margin-bottom:.8mm;line-height:1.25}.steps span{display:block;font-size:8.8pt;color:#3a3a36;line-height:1.4}
.snote{margin:0 0 4.8mm;font-size:8.8pt;color:#5B5B55}
.ex{margin-bottom:4.8mm}.ex p{margin:0 0 2mm;font-size:9.2pt}
.ex table{width:100%;border-collapse:collapse;font-size:8.8pt}
.ex th{text-align:left;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:#5B5B55;padding:1.4mm 2mm;border-bottom:1px solid #111}
.ex td{padding:1.8mm 2mm;border-bottom:1px solid #E1E0DA;vertical-align:top}
.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-bottom:4.8mm}
.two.one{grid-template-columns:1fr}
.needs div{border-top:1px solid #111;padding-top:1.6mm;margin-bottom:2.2mm}
.needs b{display:block;font-size:9.6pt}.needs span{display:block;font-size:8.8pt;color:#4a4a45}
.excl{margin:0;padding:0;list-style:none;font-size:8.9pt}
.excl li{padding:1.4mm 0 1.4mm 4.6mm;border-top:1px solid #E1E0DA;position:relative}
.excl li::before{content:"–";position:absolute;left:0;color:#5B5B55}
.it{background:#F3F2EE;border-radius:4mm;padding:4mm 5mm;margin-bottom:4.8mm}
.it .cols{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.it b{display:block;font-size:9.4pt;margin-bottom:.8mm;line-height:1.3}.it span{display:block;font-size:8.7pt;color:#3a3a36;line-height:1.4}
.cases{display:grid;gap:5mm;margin-bottom:4mm}.cases.n1{grid-template-columns:1fr}.cases.n2{grid-template-columns:1fr 1fr}
.case .cm{display:flex;align-items:center;gap:2.4mm;font-size:8.6pt;color:#5B5B55;margin-bottom:.8mm}
.case .cm img{height:4.6mm;width:auto}.case .cm b{color:#111;font-size:10pt}
.case span{display:block;font-size:9pt;color:#3a3a36;line-height:1.4}
.quote{font-size:9.6pt;line-height:1.45;margin:0 0 5mm;padding-left:3.4mm;border-left:1.2mm solid #FFCE1B}
.quote small{display:block;margin-top:1mm;font-size:8.4pt;color:#5B5B55}
.next{margin-top:auto;background:#111;color:#fff;border-radius:4mm;padding:4.6mm 5.4mm;display:flex;justify-content:space-between;align-items:center;gap:6mm}
.next p{margin:0;font-size:10.5pt;line-height:1.45;max-width:120mm}
.next .k{color:#FFCE1B;margin-bottom:1.4mm}
.next .mail{flex:none;text-align:right;font-size:9.4pt;font-weight:700;line-height:1.5}
.next .mail span{display:block;color:#FFCE1B}
.pf{display:flex;justify-content:space-between;align-items:flex-end;margin-top:5mm;padding-top:3mm;border-top:1px solid #E1E0DA;font-size:8.2pt;color:#5B5B55}
.pf b{color:#111}.pf img{height:9mm;width:auto}
.spacer{flex:1}
.tier .cal{display:flex;align-items:center;gap:1.6mm;margin-bottom:.6mm}.tier .cal svg{width:7.4mm;height:7.4mm;flex:none}
.tiers{gap:0}.tier{padding:0 3mm}.tier:first-child{padding-left:0}.tier:last-child{padding-right:0}.tier+.tier{border-left:1px solid #E1E0DA}
.incl{margin:0;font-size:7.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5B5B55}
.it .cols{gap:0}.it .cols>div{padding:0 4.6mm}.it .cols>div:first-child{padding-left:0}.it .cols>div:last-child{padding-right:0}.it .cols>div+div{border-left:1px solid #D2D1CA}
.gap{flex:1 1 0;max-height:8mm}
a{color:inherit;text-decoration:underline;text-decoration-color:#FFCE1B;text-decoration-thickness:.55mm;text-underline-offset:.7mm}
.next a,.pf a{text-decoration:none}
.hero{display:grid;grid-template-columns:1fr 54mm;gap:6mm;align-items:center;margin-bottom:4.8mm}
.hero h1{max-width:none;font-size:23pt}.hero .lede{margin:0}
.hero .art{width:54mm;height:auto;display:block}
.webdiag{border:1px solid #E1E0DA;border-radius:4mm;padding:2.6mm 3mm;margin-bottom:2.6mm}
.webdiag svg{display:block;width:100%;height:auto}
.flow{display:grid;grid-template-columns:31mm 6mm 1fr 6mm 34mm;grid-template-rows:auto auto auto;align-items:center;border:1px solid #E1E0DA;border-radius:4mm;padding:4.4mm 4mm 4mm;margin-bottom:2.6mm}
.flow i{align-self:end;display:block;font-style:normal;font-size:6.8pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#77776F;margin-bottom:1.8mm}
.fin{border:1px solid #CFCEC8;border-radius:2.6mm;padding:2.2mm 2.6mm;margin-bottom:2.2mm}
.fin b,.fout b{display:block;font-size:8.8pt;line-height:1.2}.fin span{display:block;font-size:7.4pt;color:#6b6b66;margin-top:.4mm}
.fout{background:#111;color:#fff;border-radius:2.6mm;padding:2.4mm 2.8mm;margin-bottom:2.2mm}.fout span{display:block;font-size:7.4pt;color:#cfcfca;margin-top:.4mm}
.fin:last-child,.fout:last-child{margin-bottom:0}
.farr{text-align:center;font-size:13pt;line-height:1}
.fl-loop,.fsteps{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:5mm}
.fl-loop{grid-auto-flow:row}
.fl-loop{min-height:2mm;margin-bottom:1.6mm}
.fl-loop .one{border:0;margin:0;text-align:center}
.fl-loop .one em{position:static;transform:none;display:inline-block;border:1.3px dashed #111;border-radius:3mm;padding:.5mm 2.4mm}
.fl-loop .many{height:4.6mm;margin-top:2.6mm}
.fl-loop .many{border:1.3px dashed #111;border-bottom:0;border-radius:2.4mm 2.4mm 0 0;margin:2.6mm 5mm 0;position:relative}
.fl-loop em{position:absolute;left:50%;top:-2.3mm;transform:translateX(-50%);background:#fff;padding:0 1.8mm;font-style:normal;font-size:7.2pt;font-weight:700;white-space:nowrap}
.fstep{border:1px solid #CFCEC8;border-radius:2.6mm;padding:2.6mm;position:relative;align-self:stretch}
.fstep.first{background:#FFCE1B;border:1.4px solid #111}
.fstep .t{display:block;font-size:6.8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5B5B55;margin-bottom:1.2mm}
.fstep.first .t{color:#3a3500}
.fstep .n{display:inline-flex;width:5mm;height:5mm;border-radius:50%;background:#111;color:#fff;font-size:7.5pt;font-weight:800;align-items:center;justify-content:center;margin-bottom:1.2mm}
.fstep b{display:block;font-size:9.6pt;line-height:1.2;margin-bottom:.9mm}
.fstep .c{display:block;font-size:7.8pt;color:#3a3a36;line-height:1.35}
.fstep:not(:last-child)::after{content:"→";position:absolute;right:-4.2mm;top:50%;transform:translateY(-50%);font-size:10.5pt}
`;

const head = (lang, n) => `<header class="ph"><span><b>Pavel Kroupa</b> · ${esc(UI[lang].sub)}</span><span>${n} / 2</span></header>`;
const site = (lang) => (lang === 'en' ? 'https://pavelkroupa.com/en/' : 'https://pavelkroupa.com/');
const foot = (lang) => `<footer class="pf"><span><b>Pavel Kroupa</b> · <a href="mailto:contact@pavelkroupa.com">contact@pavelkroupa.com</a> · <a href="${site(lang)}">pavelkroupa.com</a><br>${esc(UI[lang].place)}</span><img src="/logo/pk/pk-svetle.svg" alt=""></footer>`;

function page1(lang, t, art) {
  const u = UI[lang], p = t.price;
  const sit = t.situation.list ? `<ul>${t.situation.list.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : `<p>${esc(t.situation.text)}</p>`;
  let main = '';
  if (p.tiers) main += `<div class="tiers">${p.tiers.map(([a, b, c], i) => `<div class="tier">${p.tierDays ? `<div class="cal">${cal(p.tierDays[i])}<i>${esc(a)}</i></div>` : p.tierIcons ? `<div class="cal">${ICON[p.tierIcons[i]]}<i>${esc(a)}</i></div>` : `<i>${esc(a)}</i>`}<b>${esc(b)}</b><span>${esc(c)}</span></div>`).join('')}</div>`;
  if (p.text) main += `<p class="ptext">${esc(p.text)}</p>`;
  if (p.included) main += `${p.includedLabel ? `<p class="incl">${esc(p.includedLabel)}</p>` : ''}<ul class="inc">${p.included.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>`;
  main += `<div class="aff"><em>${esc(u.affects)}</em>${p.affects.map((x) => `<span>${esc(x)}</span>`).join('')}</div>`;
  if (p.note) main += `<p class="pnote">${esc(p.note)}</p>`;
  return `<section class="page">${head(lang, 1)}
<p class="eyebrow">${esc(t.eyebrow)}</p><div class="hero"><div><h1>${rich(t.h1)}</h1><p class="lede">${esc(t.lede)}</p></div><img class="art" src="${art.ill}" alt=""></div>
${G}<div class="sit"><span class="pill">${esc(t.situation.label)}</span>${sit}</div>
${G}<p class="k">${esc(u.gets)}</p><div class="gets n${t.gets.length}">${t.gets.map(([a, b]) => `<div class="card"><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div>
${t.also ? `<p class="also">${esc(t.also)}</p>` : ''}
${G}<p class="k">${esc(u.price)}</p><div class="price"><div class="pbox"><span class="amt">${esc(p.amount)}</span><span class="vat">${esc(p.vat)}</span><span class="term">${esc(p.term)}</span></div><div class="pmain">${main}</div></div>
${G}<p class="k">${esc((t.why || WHY[lang]).h)}</p><div class="why">${(t.why || WHY[lang]).items.map((it, i) => (i === 2 && t.why3 ? t.why3 : it)).map(([a, b]) => `<div><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div>
<div class="spacer"></div>${foot(lang)}</section>`;
}

function flow(lang, f) {
  const u = UI[lang], n = f.steps.length;
  const loop = f.loop ? `<div class="fl-loop" style="grid-template-columns:repeat(${n},1fr)">${Array.from({ length: n }, (_, i) => i + 1).map((i) => i === f.loop[0] ? `<div class="${f.loop[0] === f.loop[1] ? 'one' : 'many'}" style="grid-column:${f.loop[0]} / ${f.loop[1] + 1}"><em>${esc(f.loop[2])}</em></div>` : (i > f.loop[0] && i <= f.loop[1]) ? '' : '<span></span>').join('')}</div>` : '<div class="fl-loop"></div>';
  return `<div class="flow"><i>${esc(u.begin)}</i><span></span><i>${esc(u.work)}</i><span></span><i>${esc(u.gets)}</i>
<span></span><span></span>${loop}<span></span><span></span>
<div>${f.in.map(([a, b]) => `<div class="fin"><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div><div class="farr">→</div>
<div class="fsteps">${f.steps.map(([tm, a, c], i) => `<div class="fstep${i ? '' : ' first'}"><span class="t">${esc(tm)}</span><span class="n">${i + 1}</span><b>${esc(a)}</b><span class="c">${esc(c)}</span></div>`).join('')}</div>
<div class="farr">→</div><div>${f.out.map(([a, b]) => `<div class="fout"><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div></div>`;
}

function page2(lang, t, art) {
  const u = UI[lang];
  let h = `<section class="page">${head(lang, 2)}<p class="k">${esc(u.how)}</p>`;
  if (t.diagram) h += `<div class="webdiag">${art.diagram}</div>`;
  else if (t.flow) h += flow(lang, t.flow);
  else h += `<ol class="steps n${t.steps.length}">${t.steps.map(([a, b], i) => `<li><span class="no">${i + 1}</span><b>${esc(a)}</b><span>${esc(b)}</span></li>`).join('')}</ol>`;
  h += t.stepsNote ? `<p class="snote">${esc(t.stepsNote)}</p>` : '<div style="height:3mm"></div>';
  if (t.example) h += `${G}<div class="ex"><p class="k">${esc(u.example)}</p><p>${esc(t.example.text)}</p><table><tr>${t.example.head.map((x) => `<th>${esc(x)}</th>`).join('')}</tr>${t.example.rows.map((r) => `<tr>${r.map((x) => `<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</table></div>`;
  const cols = [];
  if (t.needs) cols.push(`<div class="needs"><p class="k">${esc(u.needs)}</p>${t.needs.map(([a, b]) => `<div><b>${esc(a)}</b><span>${esc(b)}</span></div>`).join('')}</div>`);
  if (t.excl) cols.push(`<div><p class="k">${esc(u.excl)}</p><ul class="excl">${t.excl.map((x) => `<li>${link(x)}</li>`).join('')}</ul></div>`);
  if (cols.length) h += `${G}<div class="two${cols.length === 1 ? ' one' : ''}">${cols.join('')}</div>`;
  if (t.it) h += `${G}<div class="it"><p class="k">${esc(t.itLabel || u.it)}</p><div class="cols">${t.it.map(([q, a]) => `<div><b>${esc(q)}</b><span>${link(a)}</span></div>`).join('')}</div></div>`;
  h += `${G}<p class="k">${esc(u.practice)}</p><div class="cases n${t.practice.length}">${t.practice.map(([, name, meta, text]) =>
    `<div class="case"><div class="cm"><b>${esc(name)}</b>${meta ? `· ${esc(meta)}` : ''}</div><span>${esc(text)}</span></div>`).join('')}</div>`;
  if (t.quote) h += `<p class="quote">“${esc(t.quote[0])}”<small>${esc(t.quote[1])}, ${esc(t.quote[2])}</small></p>`;
  h += `${G}<div class="next"><div><p class="k">${esc(u.next)}</p><p>${esc(t.next)}</p></div><div class="mail"><a href="mailto:contact@pavelkroupa.com">contact@pavelkroupa.com</a><span><a href="${site(lang)}">pavelkroupa.com</a></span></div></div>${foot(lang)}</section>`;
  return h;
}

const doc = (lang, t, art) => `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><title>Pavel Kroupa · ${esc(t.eyebrow)}</title><style>${CSS}</style></head><body>${page1(lang, t, art)}${page2(lang, t, art)}</body></html>`;

// Obrázky ze stránky služby: ilustrace (.svc-hero-ill) vykreslená se styly webu jako PNG ve trojnásobném rozlišení,
// a diagram postupu (figure.diagram) vložený jako vektor s písmem Inter.
function serve(p, html) {
  return p.route('**/*', async (r) => {
    const u = new URL(r.request().url());
    if (u.host !== 'pk.local') return r.abort();
    if (u.pathname === '/') return r.fulfill({ body: html, contentType: 'text/html; charset=utf-8' });
    const f = path.join(ROOT, decodeURIComponent(u.pathname));
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
    const type = { '.css': 'text/css', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' }[path.extname(f)];
    r.fulfill({ body: fs.readFileSync(f), contentType: type || 'application/octet-stream' });
  });
}
async function loadArt(browser, key, lang) {
  const src = fs.readFileSync(path.join(ROOT, (lang === 'en' ? 'en/' : '') + `services/${key}/index.html`), 'utf8');
  const m = src.match(/<div class="svc-hero-ill">(<svg class="ill [\s\S]*?<\/svg>)/);
  if (!m) throw new Error(`ilustrace nenalezena: ${lang} ${key}`);
  const svg = m[1].replace(/^<svg class="ill /, '<svg class="ill on ');
  const p = await browser.newPage({ viewport: { width: 700, height: 500 }, deviceScaleFactor: 3 });
  await serve(p, `<!doctype html><html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/assets/site.css">
<style>html,body{margin:0;background:#fff}.box{width:640px;padding:10px}</style></head><body><div class="box">${svg}</div></body></html>`);
  await p.goto('http://pk.local/', { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; document.getAnimations().forEach((a) => { try { a.finish(); } catch (e) {} }); });
  await p.waitForTimeout(100);
  const ill = 'data:image/png;base64,' + (await (await p.$('svg.ill')).screenshot()).toString('base64');
  await p.close();
  const d = src.match(/<figure class="diagram">(<svg[\s\S]*?<\/svg>)/);
  const diagram = d ? d[1].replace(/ width="\d+" height="\d+"/, '').replace(/font-family="[^"]*"/g, 'font-family="Inter, Helvetica, Arial, sans-serif"') : '';
  return { ill, diagram };
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  if (PREVIEW) fs.mkdirSync(PREVIEW, { recursive: true });
  const browser = await chromium.launch(); let bad = 0;
  for (const s of SERVICES) for (const lang of ['cs', 'en']) {
    const art = await loadArt(browser, s.key, lang);
    if (s[lang].diagram && !art.diagram) throw new Error(`diagram nenalezen: ${lang} ${s.key}`);
    const html = doc(lang, s[lang], art);
    const p = await browser.newPage({ viewport: { width: 794, height: 1123 } });
    await p.route('http://pk.local/**', async (r) => {
      const u = new URL(r.request().url());
      if (u.pathname === '/') return r.fulfill({ body: html, contentType: 'text/html; charset=utf-8' });
      const f = path.join(ROOT, decodeURIComponent(u.pathname));
      if (!f.startsWith(ROOT) || !fs.existsSync(f)) return r.fulfill({ status: 404, body: '' });
      r.fulfill({ body: fs.readFileSync(f), contentType: f.endsWith('.svg') ? 'image/svg+xml' : 'application/octet-stream' });
    });
    await p.goto('http://pk.local/', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
      const spacer = pg.querySelector('.spacer'), foot = pg.querySelector('.pf');
      const free = spacer ? spacer.getBoundingClientRect().height : (pg.querySelector('.next').getBoundingClientRect().top - [...pg.children].filter((c) => !c.matches('.next,.pf')).pop().getBoundingClientRect().bottom);
      return { page: i + 1, overflow: pg.scrollHeight > pg.clientHeight + 1 || foot.getBoundingClientRect().bottom > pg.getBoundingClientRect().bottom + 1, free: Math.round(free) };
    }));
    const file = s.file[lang];
    over.forEach((o) => { if (o.overflow) { bad++; console.log(`PŘETÉKÁ ${file} strana ${o.page}`); } });
    await p.pdf({ path: path.join(OUT, file), format: 'A4', printBackground: true, preferCSSPageSize: true });
    if (PREVIEW) {
      const pages = await p.$$('.page');
      for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(PREVIEW, file.replace('.pdf', `-${i + 1}.png`)) });
    }
    console.log(`pdf/${file}  volné místo (px): ${over.map((o) => o.free).join(', ')}`);
    await p.close();
  }
  await browser.close();
  if (bad) process.exit(1);
})();
