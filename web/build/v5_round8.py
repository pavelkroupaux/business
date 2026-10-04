# Round 8 (4. 10. 2026): loga výš k hraně černé sekce, tečky pod "Kdy týmy...", workshop bez eyebrow,
# notebook: byznys logika -> tok -> zoom na formulář -> kreslení a klik -> zoom ven do toku,
# proces s postupným odkrytím, loga v případech.

# ---------- černá sekce: loga nahoře, tečky až od "Kdy týmy potřebují moji pomoc"
h = rep(h, '<section class="panel">\n    <div class="wrap">\n      <p class="logos-h">', '<section class="panel has-logos">\n    <div class="wrap">\n      <p class="logos-h">')
_i = h.index('</ul></div>', h.index('class="marquee logos"')) + len('</ul></div>')
h = h[:_i] + '\n    </div>\n    <div class="pdots">\n    <div class="wrap">' + h[_i:]
_j = h.index('</section>', _i)
h = h[:_j] + '  </div>\n  ' + h[_j:]

# ---------- workshop: bez eyebrow, lepší nadpis
h = rep(h, '<p class="eyebrow sig">Workshop v akci</p><h2>Jak vypadá workshop se mnou.</h2>', '<h2>Rozhoduje se u stěny, ne nad slajdy.</h2>')

# ---------- notebook: nová choreografie
S1 = 0.177
def wire(t0):
    o = [0, .15, .3, .45, .55, .65, .75, .9, 1.0, 1.1, 1.2, 1.3, 1.38]
    t = lambda k: round(t0 + o[k], 2)
    return ''.join([
        f'<path d="{rr(190,110,620,390,8)}" fill="#fff" stroke="{INK}" stroke-width="6"/>',
        P(rr(206, 126, 588, 32, 8), t(0), 3, GREY),
        P('M250 205 H520', t(1), 12), P('M250 236 H450', t(2), 6, GREY),
        P(rr(250, 268, 300, 46, 10), t(3)), P('M268 291 H380', t(4), 4, GREY),
        P(rr(250, 330, 300, 46, 10), t(5)), P('M268 353 H350', t(6), 4, GREY),
        f'<path class="btnf2" d="{rr(250,398,160,48,24)}" fill="transparent"/>',
        P(rr(250, 398, 160, 48, 24), t(7)), P('M290 422 H370', t(8), 5),
        P(rr(600, 205, 170, 241, 12), t(9), 3, GREY), P('M612 217 L758 434', t(10), 2, GREY), P('M758 217 L612 434', t(11), 2, GREY),
        f'<circle class="rip2" cx="330" cy="422" r="16" fill="none" stroke="{YEL}" stroke-width="5"/>',
    ])
LAB2 = lambda x, y, txt, d, size=17: f'<text class="lt f" style="--d:{d}s" x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{txt}</text>'
DIAG = ''.join([
    P(rr(250, 140, 170, 56, 12), 1.1, 3), LAB2(335, 175, 'Problém', 1.3, 20),
    ARROW(426, 572, 168, 1.5),
    f'<path class="f" style="--d:1.9s" d="{rr(580,140,170,56,12)}" fill="{YEL}"/>', P(rr(580, 140, 170, 56, 12), 1.8, 3), LAB2(665, 175, 'Řešení', 2.0, 20),
    P('M665 200 C 665 236, 285 228, 285 262', 2.3, 2.5), P('M278 255 L285 265 L292 255', 2.55, 2.5),
    P(rr(230, 270, 110, 74, 8), 2.6, 3), P('M246 292 H300', 2.75, 3, GREY), P(rr(246, 316, 44, 12, 6), 2.8, 2), LAB2(285, 368, 'Formulář', 2.8),
    ARROW(344, 394, 307, 2.9),
    P(rr(400, 270, 110, 74, 8), 3.1, 3), f'<circle class="f" style="--d:3.25s" cx="455" cy="298" r="10" fill="{YEL}"/>', P('M428 324 H482', 3.3, 3, GREY), LAB2(455, 368, 'Potvrzení', 3.3),
    ARROW(514, 558, 307, 3.4),
    P('M600 269 L638 307 L600 345 L562 307 Z', 3.6, 3), LAB2(600, 313, 'Chyba?', 3.8, 15),
    ARROW(642, 684, 307, 3.9),
    P(rr(690, 272, 96, 70, 8), 4.1, 3), P('M722 307 L734 319 L756 295', 4.25, 5), LAB2(738, 368, 'Hotovo', 4.3),
    P('M600 349 V386', 4.3, 3), P('M593 378 L600 388 L607 378', 4.45, 3),
    P(rr(546, 392, 108, 50, 10), 4.45, 3), LAB2(600, 423, 'Oprava', 4.6, 15),
    '<path class="f" style="--d:4.6s" d="M542 417 H285 V350" fill="none" stroke="#a1a1a6" stroke-width="2.5" stroke-dasharray="6 8" stroke-linecap="round"/>',
    LAB2(415, 405, 'zpátky do formuláře', 4.8, 14),
])
BADGE = (f'<g class="f" style="--d:10.2s"><circle cx="338" cy="272" r="13" fill="{YEL}" stroke="{INK}" stroke-width="2.5"/>'
         f'<path d="M332 272 L337 277 L345 267" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>')
ZX, ZY, ZS = 500 - 285 * 5.6, 305 - 307 * 5.6, 5.6
LAPTOP2 = f'''<figure class="lap lap2" data-lap aria-label="Animace: notebook se otevře, nakreslí se problém, řešení a tok obrazovek. Pohled se přiblíží na formulář, ten se nakreslí, kurzor klikne a pohled se vrátí do toku.">
  <svg viewBox="0 0 1000 600" role="img" aria-hidden="true">
    <defs><clipPath id="lap2-screen"><path d="{rr(190,110,620,390,8)}"/></clipPath></defs>
    <ellipse cx="500" cy="566" rx="420" ry="14" class="lap-shadow"/>
    <g class="lid">
      <path d="{rr(170,90,660,430,22)}" class="lap-frame"/>
      <circle cx="500" cy="100" r="3.5" fill="#55555a"/>
      <path d="{rr(190,110,620,390,8)}" class="lap-scr"/>
      <g clip-path="url(#lap2-screen)">
        <g class="z-diag">{DIAG}</g>
        <g class="z-s1">{wire(5.7)}</g>
        {BADGE}
        <g class="cur2"><path d="M0 0 L0 28 L7.5 21 L12.5 32 L18 29.5 L13 19 L23 19 Z" fill="{INK}" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>
      </g>
    </g>
    <path d="M110 520 H890 L868 550 Q862 558 850 558 H150 Q138 558 132 550 Z" class="lap-base"/>
    <path d="M440 520 H560 Q556 530 546 530 H454 Q444 530 440 520 Z" class="lap-notch"/>
  </svg>
  <figcaption class="lap-cap">Od problému k toku obrazovek. Z jedné obrazovky prototyp, na který se dá kliknout, a zpátky do toku, podle kterého staví vývoj.
    <button type="button" class="lap-re">Přehrát znovu</button></figcaption>
</figure>
'''
_a = h.index('<figure class="lap"'); _b = h.index('</figure>', _a) + len('</figure>')
h = h[:_a] + LAPTOP2.strip() + h[_b:]
h = rep(h, 'data-words="business logika|prototyp|funkční prototyp|user flow|customer journey"', 'data-words="business logika|user flow|prototyp|funkční prototyp|customer journey"')
h = rep(h, 'aria-label="Na workshopu vzniká business logika, prototyp, funkční prototyp, user flow a customer journey."',
        'aria-label="Na workshopu vzniká business logika, user flow, prototyp, funkční prototyp a customer journey."')

# ---------- proces: postupné odkrytí
h, _n = re.subn(r'(<li class="pstep">.*?</h3>)(<p>.*?</p>)(</li>)', r'\1<div class="pstep-more">\2</div>\3', h, flags=re.S)
assert _n == 4, _n
h = rep(h, '</ol>\n    </div>\n  </section>', '</ol>\n      <div class="row" style="margin-top:28px"><button type="button" class="btn btn-line proc-toggle" aria-expanded="false">Jak to probíhá podrobně</button></div>\n    </div>\n  </section>')

# ---------- loga v případech (karty a detail)
CASE_LOGO = {'heirloom': 'Logo.svg', 'coinmate': 'color_logo.svg', 'leeaf': 'logo Leeaf - cropped.svg'}
def _logo_src(fn):
    p = LOGO_DIR + fn
    return 'data:image/svg+xml;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else None
for c in CASES:
    src = _logo_src(CASE_LOGO.get(c['id'], '_none_'))
    if not src: continue
    tag = f'<img class="card-logo" src="{src}" alt="{c["client"]}">'
    meta = f'<span class="card-meta">{c["meta"]}</span>'
    for name in ('h', 'WORK', 'CASEV', 'DP'):
        globals()[name] = globals()[name].replace(meta, tag + meta)
    eb = f'<p class="eyebrow sig">{c["meta"]} &middot; {c["field"]}</p>'
    CASEV = rep(CASEV, eb, f'<img class="case-logo" src="{src}" alt="{c["client"]}">' + eb)

CSS_R8 = '''
/* ---------- v5 kolo 8 ---------- */
/* černá sekce: loga u horní hrany, tečky až pod nimi */
.panel.has-logos{padding-top:clamp(28px,3.4vw,44px);padding-bottom:0}
.panel.has-logos .marquee.logos{margin-bottom:0}
.pdots{position:relative;padding:clamp(64px,8vw,104px) 0 clamp(96px,12vw,150px)}
.pdots::before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(rgba(255,255,255,.16) 1.4px,transparent 1.4px);background-size:26px 26px;
  -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 140px);mask-image:linear-gradient(to bottom,transparent 0,#000 140px)}
.pdots>.wrap{position:relative}
/* notebook 2 */
.lap2 .z-diag,.lap2 .z-s1{transform-box:view-box;transform-origin:0 0}
.lap2 .z-s1{opacity:0}
.lap2 .cur2{transform-box:view-box;transform:translate(780px,470px);opacity:0}
.lap2 .rip2{transform-box:fill-box;transform-origin:center;opacity:0}
.lap2.play .z-diag{animation:zin .8s cubic-bezier(.6,0,.3,1) 4.95s forwards,zout .8s cubic-bezier(.6,0,.3,1) 9.3s forwards}
.lap2.play .z-s1{animation:s1in .3s ease 5.5s forwards,s1out .8s cubic-bezier(.6,0,.3,1) 9.3s forwards}
.lap2.play .cur2{animation:lapcur 1.6s cubic-bezier(.4,0,.2,1) 7.5s forwards}
.lap2.play .rip2{animation:laprip .6s ease-out 8.45s forwards}
.lap2.play .btnf2{animation:lapbtn .3s ease 8.5s forwards}
@keyframes zin{0%{transform:none;opacity:1}70%{opacity:1}100%{transform:translate(''' + f'{ZX:.1f}px,{ZY:.1f}px) scale({ZS})' + ''';opacity:0}}
@keyframes zout{0%{transform:translate(''' + f'{ZX:.1f}px,{ZY:.1f}px) scale({ZS})' + ''';opacity:0}25%{opacity:1}100%{transform:none;opacity:1}}
@keyframes s1in{to{opacity:1}}
@keyframes s1out{from{transform:none;opacity:1}to{transform:translate(''' + f'{230-190*S1:.1f}px,{272.5-110*S1:.1f}px) scale({S1})' + ''';opacity:1}}
/* proces: popisy až na kliknutí */
.pstep-more{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s cubic-bezier(.2,.7,.3,1)}
.pstep-more>p{overflow:hidden;min-height:0}
.proc-steps.open .pstep-more{grid-template-rows:1fr}
.proc-steps.open .pstep-more>p{padding-top:4px}
/* loga v případech */
.card-logo{display:block;height:26px;width:auto;max-width:150px;margin-bottom:6px}
.card-logo[alt="Coinmate"]{height:44px;margin:-9px 0 -3px -7px}
.card-logo[alt="Heirloom"]{height:22px}
.card-logo[alt="Leeaf"]{height:24px}
.case-logo{display:block;height:40px;width:auto;max-width:200px;margin:0 auto 22px}
:root[data-theme="dark"] .card-logo,:root[data-theme="dark"] .case-logo{filter:brightness(0) invert(.92)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .card-logo,:root:not([data-theme="light"]) .case-logo{filter:brightness(0) invert(.92)}}
'''

PROC_JS = '''<script>
(function(){var b=document.querySelector(".proc-toggle"),l=document.querySelector(".proc-steps");if(!b||!l)return;
  b.addEventListener("click",function(){var o=l.classList.toggle("open");b.setAttribute("aria-expanded",o?"true":"false");
    b.textContent=o?"Skrýt podrobnosti":"Jak to probíhá podrobně";});})();
</script>'''

def post_patch8(out):
    out = rep(out, 'var starts=[0,1600,3600,6400,8800];', 'var starts=[0,2600,5600,7600,9600];')
    out = rep(out, '},11800);}', '},12600);}')
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R8 + out[i:] + PROC_JS
