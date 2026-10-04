# Round 9 (4. 10. 2026): šedá loga vpravo nahoře v kartách (+ BRENO), zaoblená šipka z Řešení,
# animované infografiky služeb a jejich miniatury u úvodu služeb.

# ---------- loga v případech: šedá, vpravo nahoře
CARD_GREY = '#8e8e93'
CASE_LOGO['breno'] = 'logo-breno-dark.svg'
def _grey_src(fn):
    global LOGO_GREY
    p = LOGO_DIR + fn
    if not os.path.exists(p): return None
    keep = LOGO_GREY; LOGO_GREY = CARD_GREY
    try: svg = recolor(open(p, encoding='utf-8').read())
    finally: LOGO_GREY = keep
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()
for c in CASES:
    fn = CASE_LOGO.get(c['id'])
    if not fn: continue
    grey = _grey_src(fn)
    if not grey: continue
    col = _logo_src(fn)
    for name in ('h', 'WORK', 'CASEV', 'DP'):
        t = globals()[name]
        if col and col in t:
            t = t.replace(col, grey)
        else:  # BRENO: logo ještě nikde není
            t = t.replace(f'<span class="card-meta">{c["meta"]}</span>', f'<img class="card-logo" src="{grey}" alt="{c["client"]}"><span class="card-meta">{c["meta"]}</span>')
            eb = f'<p class="eyebrow sig">{c["meta"]} &middot; {c["field"]}</p>'
            if name == 'CASEV' and eb in t:
                t = t.replace(eb, f'<img class="case-logo" src="{grey}" alt="{c["client"]}">' + eb)
        globals()[name] = t

# ---------- notebook: zaoblená šipka z Řešení, konec míří dolů
h = rep(h, 'd="M665 200 C 665 236, 285 228, 285 262"', 'd="M665 198 V208 Q665 222 651 222 H299 Q285 222 285 236 V256"')
h = rep(h, 'd="M278 255 L285 265 L292 255"', 'd="M278 249 L285 258 L292 249"')

# ---------- infografiky služeb s animací
def _ia(i): return f' class="ia" style="--i:{i}s"'
ILL_DP2 = f'''<svg class="ill ill-dp" {SV} aria-label="Notebook s prototypem, ze kterého vede tok obrazovek">
  <path d="{rr4(40,16,240,152,12)}" class="lap-frame"/><path d="{rr4(49,25,222,134,5)}" class="lap-scr"/>
  <path d="M22 168 H298 L289 181 Q286 185 279 185 H41 Q34 185 31 181 Z" class="lap-base"/>
  <g stroke="{K}" stroke-width="2">
    <g{_ia(.2)}><path d="{rr4(60,70,44,32,4)}" fill="#fff"/><path d="M66 79 H90 M66 86 H84" stroke="#a1a1a6"/><path d="{rr4(66,92,18,6,3)}" fill="#FFCE1B" stroke="none"/></g>
    <g{_ia(.45)}><path d="M108 86 H122 M117 81 L122 86 L117 91"/></g>
    <g{_ia(.65)}><path d="{rr4(126,70,44,32,4)}" fill="#fff"/><circle cx="148" cy="83" r="6" fill="#FFCE1B" stroke="none"/><path d="M137 94 H159" stroke="#a1a1a6"/></g>
    <g{_ia(.9)}><path d="M174 86 H186 M181 81 L186 86 L181 91"/></g>
    <g{_ia(1.1)}><path d="M204 70 L220 86 L204 102 L188 86 Z" fill="#fff"/></g>
    <g{_ia(1.35)}><path d="M224 86 H236 M231 81 L236 86 L231 91"/></g>
    <g{_ia(1.55)}><path d="{rr4(240,72,24,28,4)}" fill="#fff"/><path d="M246 86 L250 90 L258 81" stroke-width="2.6"/></g>
    <g{_ia(1.8)}><path d="M204 106 V122"/><path d="{rr4(186,124,36,20,4)}" fill="#fff"/></g>
  </g>
</svg>'''
days = [('Po', 40, None), ('Út', 92, .65), ('St', 144, None), ('Čt', 196, 1.95), ('Pá', 248, None)]
day_svg = ''
for d, x, t in days:
    day_svg += f'<path d="{rr4(x,14,40,40,9)}" class="ill-off"/>'
    if t is not None:
        day_svg += f'<path class="dfill" style="--i:{t}s" d="{rr4(x,14,40,40,9)}" fill="#FFCE1B"/>'
    day_svg += f'<text x="{x+20}" y="39" text-anchor="middle" class="ill-d{" don" if t is not None else ""}"{f" style=--i:{t}s" if t is not None else ""}>{d}</text>'
ILL_FR2 = f'''<svg class="ill ill-fr" {SV} aria-label="Dva dny v týdnu ve vašem týmu: otázky vedení, směr a hotová práce vývoje">
  {day_svg}
  <circle class="wk" cx="60" cy="64" r="3.5" fill="#FFCE1B"/>
  <g stroke="currentColor" stroke-width="2">
    <g{_ia(2.2)}><path d="M112 58 C 118 84, 140 100, 150 112" stroke-dasharray="4 6" class="ill-soft"/><path d="M216 58 C 210 84, 182 100, 172 112" stroke-dasharray="4 6" class="ill-soft"/></g>
    <g{_ia(2.45)}><path d="M88 150 H135 M187 150 H232"/></g>
    <g{_ia(2.5)}><circle cx="70" cy="150" r="16" class="ill-node"/></g>
    <g{_ia(2.9)}><path d="{rr4(234,134,32,32,7)}" class="ill-node"/><path d="M242 150 L248 156 L259 143" stroke-width="2.6"/></g>
  </g>
  <text class="ia ill-q" style="--i:2.55s" x="70" y="156" text-anchor="middle">?</text>
  <g{_ia(2.7)}><circle cx="161" cy="146" r="24" fill="#FFCE1B"/><circle cx="161" cy="146" r="16" fill="none" stroke="{K}" stroke-width="1.6"/>
    <path d="M161 133 L165.5 146 H156.5 Z" fill="{K}"/><path d="M161 159 L165.5 146 H156.5 Z" fill="#fff" stroke="{K}" stroke-width="1.2" stroke-linejoin="round"/></g>
  <g{_ia(3.0)}><text x="70" y="188" text-anchor="middle" class="ill-t">vedení</text><text x="161" y="188" text-anchor="middle" class="ill-t">směr</text><text x="250" y="188" text-anchor="middle" class="ill-t">vývoj</text></g>
</svg>'''
ILL_AU2 = f'''<svg class="ill ill-au" {SV} aria-label="Nahrávka obrazovky a seznam toho, co opravit dřív">
  <path d="{rr4(16,22,176,116,10)}" class="ill-scr" stroke="currentColor" stroke-width="2.4"/>
  <path d="M16 44 H192" stroke="currentColor" stroke-width="2" class="ill-soft"/>
  <circle cx="30" cy="33" r="4" fill="#FFCE1B"/>
  <g class="pl"><circle cx="104" cy="86" r="22" fill="#FFCE1B"/><path d="M97 75 L115 86 L97 97 Z" fill="{K}"/></g>
  <path d="M30 126 H178" stroke="currentColor" stroke-width="3" class="ill-soft"/>
  <path class="prog" pathLength="1" d="M30 126 H178" stroke="#FFCE1B" stroke-width="4"/>
  <g font-family="var(--display)" font-size="12" font-weight="700" text-anchor="middle">
    <circle class="num" style="--i:1.4s" cx="220" cy="42" r="12"/><text class="numt" style="--i:1.4s" x="220" y="46">1</text>
    <circle class="num" style="--i:2.8s" cx="220" cy="80" r="12"/><text class="numt" style="--i:2.8s" x="220" y="84">2</text>
    <circle class="num" style="--i:4.2s" cx="220" cy="118" r="12"/><text class="numt" style="--i:4.2s" x="220" y="122">3</text>
  </g>
  <g stroke="currentColor" stroke-width="3">
    <path class="ln" style="--i:1.4s" pathLength="1" d="M240 42 H302"/><path class="ln" style="--i:2.8s" pathLength="1" d="M240 80 H290"/><path class="ln" style="--i:4.2s" pathLength="1" d="M240 118 H276"/>
  </g>
  <text x="104" y="172" text-anchor="middle" class="ill-t">nahrávka s komentářem</text>
  <text x="258" y="172" text-anchor="middle" class="ill-t">co opravit dřív</text>
</svg>'''
_ills = re.findall(r'<div class="svc-ill"><svg class="ill".*?</svg></div>', SERV, re.S)
assert len(_ills) == 3, len(_ills)
for old, new in zip(_ills, (ILL_DP2, ILL_FR2, ILL_AU2)):
    SERV = SERV.replace(old, '<div class="svc-ill">' + new + '</div>')

# miniatury u úvodu služeb: karty na úvodu a hlavička každé služby
for href, ill in (('#/services/decision-prototype', ILL_DP2), ('#/services/fractional', ILL_FR2), ('#/services/audit', ILL_AU2)):
    cls = 'svc lead' if 'decision' in href else 'svc'
    h = rep(h, f'<a class="{cls}" href="{href}"><h3>', f'<a class="{cls}" href="{href}"><div class="svc-thumb">{ill}</div><h3>')
CRUMB = '<p class="crumb"><a href="#/services"><span>Všechny služby</span></a></p>'
DP = rep(DP, CRUMB, CRUMB + f'\n      <div class="svc-hero-ill">{ILL_DP2}</div>')
FR = rep(FR, CRUMB, CRUMB + f'\n      <div class="svc-hero-ill">{ILL_FR2}</div>')
AU = rep(AU, CRUMB, CRUMB + f'\n      <div class="svc-hero-ill">{ILL_AU2}</div>')

CSS_R9 = '''
/* ---------- v5 kolo 9 ---------- */
/* loga v kartách případů: šedá, vpravo nahoře */
.case-card{position:relative}
.case-card .card-logo{position:absolute;top:28px;right:30px;margin:0;height:22px;max-width:120px;filter:none!important}
.case-card .card-logo[alt="Coinmate"]{height:40px;top:18px;right:22px;margin:0}
.case-card .card-logo[alt="Heirloom"]{height:20px}
.case-card .card-logo[alt="BRENO"]{height:16px;top:31px}
.case-card .card-meta{padding-right:130px}
.case-logo{filter:none!important}
/* animované infografiky */
.ill .ia{opacity:0;transform:translateY(5px);transform-box:fill-box}
.ill.on .ia{animation:illin .45s cubic-bezier(.2,.7,.3,1) var(--i) forwards}
@keyframes illin{to{opacity:1;transform:none}}
.ill .dfill{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0)}
.ill.on .dfill{animation:dfill .55s cubic-bezier(.2,.7,.3,1) var(--i) forwards}
@keyframes dfill{to{transform:scaleY(1)}}
.ill.on .don{animation:don .2s ease var(--i) forwards}
@keyframes don{to{fill:#1d1d1f}}
.ill .wk{transform-box:view-box;opacity:0}
.ill.on .wk{animation:wk 2.6s linear forwards}
@keyframes wk{0%{opacity:1;transform:translateX(0)}92%{opacity:1}100%{opacity:0;transform:translateX(208px)}}
.ill-q{font-family:var(--display);font-size:18px;font-weight:800;fill:currentColor}
.ill .pl{transform-box:fill-box;transform-origin:center}
.ill.on .pl{animation:pl .45s ease .25s}
@keyframes pl{50%{transform:scale(.82)}}
.ill .prog{stroke-dasharray:1;stroke-dashoffset:1}
.ill.on .prog{animation:prog 4s ease-in-out .6s forwards}
@keyframes prog{0%{stroke-dashoffset:1}20%,35%{stroke-dashoffset:.66}55%,70%{stroke-dashoffset:.33}90%,100%{stroke-dashoffset:0}}
.ill .num{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.ill.on .num{animation:numon .3s ease var(--i) forwards}
@keyframes numon{to{fill:#FFCE1B;stroke:#FFCE1B}}
.ill .numt{fill:var(--muted)}
.ill.on .numt{animation:don .3s ease var(--i) forwards}
.ill .ln{stroke-dasharray:1;stroke-dashoffset:1}
.ill.on .ln{animation:lapdraw .5s ease var(--i) forwards}
@media (prefers-reduced-motion:reduce){.ill *{animation-duration:1ms!important;animation-delay:0s!important}}
/* miniatury */
.svc-thumb{max-width:210px;margin:-4px 0 14px;color:var(--ink)}
.svc-hero-ill{max-width:280px;margin:8px auto 22px;color:var(--ink)}
@media(max-width:560px){.svc-thumb{max-width:180px}.svc-hero-ill{max-width:230px}}
'''

ILL_JS = '''<script>
(function(){var ills=[].slice.call(document.querySelectorAll(".ill"));if(!ills.length)return;
  function on(s){s.classList.remove("on");void s.getBoundingClientRect();s.classList.add("on");}
  if(!("IntersectionObserver" in window)||window.matchMedia("(prefers-reduced-motion: reduce)").matches){ills.forEach(function(s){s.classList.add("on");});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!e.target.classList.contains("on"))on(e.target);});},{threshold:.5});
  ills.forEach(function(s){io.observe(s);var p=s.parentNode;if(p&&window.matchMedia("(hover: hover)").matches){
    var box=p.closest(".svc,.svc-row,.svc-hero-ill")||p;box.addEventListener("mouseenter",function(){on(s);});}});
})();
</script>'''

def post_patch9(out):
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R9 + out[i:] + ILL_JS
