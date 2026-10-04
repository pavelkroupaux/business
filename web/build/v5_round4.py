# Round 4 (3. 10. 2026): šipka k notebooku, mezery, linky na mobilu, jednotné odkazy, bez DPH,
# infografiky služeb, O mně (S kým ne, LinkedIn, reference jako karty), Tomíček bez "sometimes".

# ---------- šipka z workshopu do prototypu
BRIDGE = ('<div class="bridge" aria-hidden="true"><svg width="84" height="156" viewBox="0 0 70 130" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M34 4 C 12 34, 56 62, 34 92 C 28 101, 31 112, 35 122"/><path d="M25 111 L35 123 L45 111"/></svg>'
          '<span>z workshopu rovnou do funkčního prototypu</span></div>')
h = rep(h, '<section class="proc">\n    <div class="wrap">\n      <figure class="lap"', '<section class="proc">\n    <div class="wrap">\n      ' + BRIDGE + '\n      <figure class="lap"')

# ---------- Porovnat všechny tři jako tlačítko
h = rep(h, '<p class="svc-all-link"><a class="lnk" href="#/services">Porovnat všechny tři</a></p>',
        '<div class="row" style="margin-top:30px"><a class="btn btn-line" href="#/services">Porovnat všechny tři</a></div>')

# ---------- infografiky služeb (ve stylu notebooku z úvodu)
def rr4(x, y, w, h_, r):
    return (f'M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h_-r} Q{x+w} {y+h_} {x+w-r} {y+h_} '
            f'H{x+r} Q{x} {y+h_} {x} {y+h_-r} V{y+r} Q{x} {y} {x+r} {y} Z')
K = '#1d1d1f'
SV = 'viewBox="0 0 320 200" fill="none" stroke-linecap="round" stroke-linejoin="round" role="img"'
ILL_DP = f'''<svg class="ill" {SV} aria-label="Notebook s prototypem, ze kterého vede tok obrazovek">
  <path d="{rr4(40,16,240,152,12)}" class="lap-frame"/><path d="{rr4(49,25,222,134,5)}" class="lap-scr"/>
  <path d="M22 168 H298 L289 181 Q286 185 279 185 H41 Q34 185 31 181 Z" class="lap-base"/>
  <g stroke="{K}" stroke-width="2">
    <path d="{rr4(60,70,44,32,4)}" fill="#fff"/><path d="M66 79 H90 M66 86 H84" stroke="#a1a1a6"/><path d="{rr4(66,92,18,6,3)}" fill="#FFCE1B" stroke="none"/>
    <path d="M108 86 H122 M117 81 L122 86 L117 91"/>
    <path d="{rr4(126,70,44,32,4)}" fill="#fff"/><circle cx="148" cy="83" r="6" fill="#FFCE1B" stroke="none"/><path d="M137 94 H159" stroke="#a1a1a6"/>
    <path d="M174 86 H186 M181 81 L186 86 L181 91"/>
    <path d="M204 70 L220 86 L204 102 L188 86 Z" fill="#fff"/>
    <path d="M224 86 H236 M231 81 L236 86 L231 91"/>
    <path d="{rr4(240,72,24,28,4)}" fill="#fff"/><path d="M246 86 L250 90 L258 81" stroke-width="2.6"/>
    <path d="M204 106 V122" /><path d="{rr4(186,124,36,20,4)}" fill="#fff"/>
  </g>
  <text x="160" y="52" text-anchor="middle" class="ill-t ill-ts">jeden den, dva, nebo týden</text>
</svg>'''
days = [('Po', 40, False), ('Út', 92, True), ('St', 144, False), ('Čt', 196, True), ('Pá', 248, False)]
day_svg = ''.join(
    f'<path d="{rr4(x,14,40,40,9)}" ' + ('fill="#FFCE1B"' if on else 'class="ill-off"') + '/>'
    f'<text x="{x+20}" y="39" text-anchor="middle" class="ill-d{" on" if on else ""}">{d}</text>'
    for d, x, on in days)
ILL_FR = f'''<svg class="ill" {SV} aria-label="Dva dny v týdnu ve vašem týmu, propojuji vedení, produkt a vývoj">
  {day_svg}
  <g stroke="currentColor" stroke-width="2">
    <path d="M112 58 C 118 84, 140 100, 152 112" stroke-dasharray="4 6" class="ill-soft"/>
    <path d="M216 58 C 210 84, 186 100, 170 112" stroke-dasharray="4 6" class="ill-soft"/>
    <path d="M86 150 H136 M186 150 H234"/>
    <circle cx="70" cy="150" r="16" class="ill-node"/><circle cx="250" cy="150" r="16" class="ill-node"/>
  </g>
  <circle cx="161" cy="140" r="24" fill="#FFCE1B"/>
  <path d="M153 148 L161 128 L169 148 L161 143 Z" fill="{K}"/>
  <text x="70" y="186" text-anchor="middle" class="ill-t">vedení</text>
  <text x="161" y="186" text-anchor="middle" class="ill-t">směr</text>
  <text x="250" y="186" text-anchor="middle" class="ill-t">vývoj</text>
</svg>'''
ILL_AU = f'''<svg class="ill" {SV} aria-label="Nahrávka obrazovky a seznam toho, co opravit dřív">
  <path d="{rr4(16,22,176,116,10)}" class="ill-scr" stroke="currentColor" stroke-width="2.4"/>
  <path d="M16 44 H192" stroke="currentColor" stroke-width="2" class="ill-soft"/>
  <circle cx="30" cy="33" r="4" fill="#FFCE1B"/>
  <circle cx="104" cy="88" r="22" fill="#FFCE1B"/><path d="M97 77 L115 88 L97 99 Z" fill="{K}"/>
  <path d="M30 126 H178" stroke="currentColor" stroke-width="3" class="ill-soft"/><path d="M30 126 H92" stroke="#FFCE1B" stroke-width="4"/>
  <g font-family="var(--display)" font-size="12" font-weight="700" text-anchor="middle">
    <circle cx="220" cy="42" r="12" fill="#FFCE1B"/><text x="220" y="46" fill="{K}">1</text>
    <circle cx="220" cy="80" r="12" class="ill-num"/><text x="220" y="84" class="ill-numt">2</text>
    <circle cx="220" cy="118" r="12" class="ill-num"/><text x="220" y="122" class="ill-numt">3</text>
  </g>
  <g stroke="currentColor" stroke-width="3"><path d="M240 42 H302"/><path d="M240 80 H290" class="ill-soft"/><path d="M240 118 H276" class="ill-soft"/></g>
  <text x="104" y="172" text-anchor="middle" class="ill-t">nahrávka s komentářem</text>
  <text x="258" y="172" text-anchor="middle" class="ill-t">co opravit dřív</text>
</svg>'''
for icon, ill in [(icons[0], ILL_DP), (icons[2], ILL_FR), (icons[3], ILL_AU)]:
    SERV = rep(SERV, icon, '<div class="svc-ill">' + ill + '</div>')

# ---------- O mně
OK2 = ['Řešíme skutečný problém. Když je vyřešený, jdeme dál.', 'Výsledek se počítá. Lidi, kteří na něm pracují, taky.']
ABOUT = rep(ABOUT, f'<div class="acard no"><p class="acard-h">A s kým ne</p>{lst(NOT, XMARK)}</div>',
            f'<div class="acard"><p class="acard-h">Na čem mi záleží</p>{lst(OK2, CHECK)}</div>')
ABOUT = rep(ABOUT, '<p style="margin-top:22px"><a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Celá kariéra na LinkedInu</a></p>',
            '<div class="row" style="margin-top:30px"><a class="btn btn-line" href="https://www.linkedin.com/in/pavelkroupa/">Celá kariéra na LinkedInu</a></div>')
ABOUT = rep(ABOUT, '<a class="gold" href="#/portfolio">Reference</a>', '<a class="gold" href="#/reference">Reference</a>')
_cards = ''.join('<a class="rcard" href="#/reference">' + re.search(r'<summary>(.*?)</summary>', it, re.S).group(1) + '</a>' for it in _items)
ABOUT = rep(ABOUT, '<div class="marquee refq" aria-label="Reference"><div class="mq-track">' + notes + NOTES_HID + '</div></div>',
            '<div class="marquee refc" aria-label="Reference"><div class="mq-track loop-track">' + _cards + '</div></div>')
ABOUT = rep(ABOUT, '<a class="btn btn-line" href="#/portfolio">Všechny reference</a>', '<a class="btn btn-line" href="#/reference">Všechny reference</a>')

CSS_R4 = '''
/* ---------- v5 kolo 4 ---------- */
/* šipka z workshopu do prototypu */
.shot-sec{padding-bottom:clamp(40px,5vw,64px)}
.proc{padding-top:0}
.bridge{display:flex;align-items:center;justify-content:center;gap:10px;color:var(--faint);margin:0 auto 18px;padding-left:220px}
.bridge span{font-family:var(--hand);font-size:19px;color:var(--faint);white-space:nowrap;transform:rotate(-3deg)}
@media(max-width:560px){.bridge{padding-left:0;flex-direction:column;gap:2px}.bridge span{white-space:normal;text-align:center}}
.lap{margin-bottom:clamp(96px,12vw,160px)}
/* spojovací linka kroků i na mobilu */
@media(max-width:980px){
  .proc-steps{grid-template-columns:1fr;max-width:560px;margin-inline:auto;gap:30px}
  .proc-steps::before{display:block;left:48px;right:auto;top:51px;bottom:51px;border-top:0;border-left:2px dashed var(--faint)}
}
/* jednotné odkazy: žluté podtržení a šipka */
.card-go,.svc-go,.pick-go,a.svc-more,main a.lnk{color:var(--ink)!important;font-family:var(--display);font-weight:600;font-size:14.5px;
  border:0!important;padding-top:10px;align-self:flex-start;display:block;
  text-decoration:underline;text-decoration-color:var(--fix);text-decoration-thickness:3px;text-underline-offset:5px;text-decoration-skip-ink:none}
.card-go::after,.svc-go::after,a.svc-more::after,main a.lnk::after{content:"\\2192";display:inline-block;margin-left:6px;text-decoration:none;transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.pick-go::after{display:inline-block;margin-left:6px}
a.card:hover .card-go::after,a.svc:hover .svc-go::after,a.svc-more:hover::after,main a.lnk:hover::after{transform:translateX(4px)}
:root[data-theme="dark"] .card-go{color:var(--ink)!important}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .card-go{color:var(--ink)!important}}
/* infografiky služeb */
.svc-row-head .svc-ill{width:100%;max-width:300px;margin:0 0 8px;color:var(--ink)}
.ill{display:block;width:100%;height:auto}
.ill-t{font-family:var(--hand);font-size:14px;fill:var(--muted)}
.ill-d{font-family:var(--display);font-size:13px;font-weight:700;fill:var(--muted)}
.ill-d.on{fill:#1d1d1f}
.ill-t.ill-ts{fill:#6e6e73}
.ill-off{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.ill-soft{opacity:.35}
.ill-node{fill:var(--raise)}
.ill-scr{fill:var(--raise)}
.ill-num{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.ill-numt{fill:var(--muted)}
@media(max-width:860px){.svc-row-head .svc-ill{max-width:260px}}
/* reference na O mně: jedoucí karty */
.refc .mq-track{animation-duration:110s;align-items:stretch}
.rcard{flex:0 0 auto;width:340px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;gap:20px;
  background:var(--raise);border-radius:24px;padding:26px 26px 24px;box-shadow:var(--glass-shadow);text-decoration:none;color:inherit;border:0;text-align:left;
  transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.rcard:hover{transform:translateY(-3px)}
.rcard .ref-claim{font-family:var(--display);font-size:18px;line-height:1.4;letter-spacing:-.015em;color:var(--ink)}
.rcard .ref-claim::after{content:none!important}
@media(max-width:560px){.rcard{width:280px}}
'''

REFS_JS = '''<script>
(function(){
  document.querySelectorAll(".loop-track").forEach(function(t){
    var k=Array.prototype.slice.call(t.children);
    k.forEach(function(c){var n=c.cloneNode(true);n.setAttribute("aria-hidden","true");n.setAttribute("tabindex","-1");t.appendChild(n);});
  });
  function toRefs(){ if(location.hash==="#/reference"){ setTimeout(function(){var r=document.getElementById("refs");if(r)r.scrollIntoView({behavior:"smooth",block:"start"});},80);} }
  window.addEventListener("hashchange",toRefs); toRefs();
})();
</script>'''

def post_patch4(out):
    out = rep(out, '"/portfolio":"v-portfolio",', '"/portfolio":"v-portfolio","/reference":"v-portfolio",')
    out = rep(out, '(nav==="/portfolio"&&h.indexOf("/work/")===0)', '(nav==="/portfolio"&&(h.indexOf("/work/")===0||h==="/reference"))')
    out = re.sub(r'\s*<p class="vat">[^<]*</p>', '', out)
    out = out.replace('<li>Nejsem plátce DPH</li>', '')
    out = rep(out, ' &middot; Nejsem plátce DPH</span>', '</span>')
    assert out.count('&ldquo;sometimes adjusting designs') >= 3
    out = out.replace('&ldquo;sometimes adjusting designs based on technical challenges&rdquo;', '&ldquo;adjusting designs based on technical challenges&rdquo;')
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R4 + out[i:]
    return out + REFS_JS
