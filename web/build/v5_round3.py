# Round 3 (3. 10. 2026): písmo, lístky, tečky, notebook s prototypem a tokem.
def rr(x, y, w, h, r):
    return (f'M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} '
            f'H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z')
INK = '#1d1d1f'; GREY = '#a1a1a6'; YEL = '#FFCE1B'
def P(d, delay=None, w=3, col=INK, extra=''):
    cls = ' class="d"' if delay is not None else ''
    st = f' style="--d:{delay}s"' if delay is not None else ''
    return f'<path{cls}{st} pathLength="1" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

def screen1(anim):
    t = (lambda v: v) if anim else (lambda v: None)
    return ''.join([
        f'<path d="{rr(190,110,620,390,8)}" fill="#fff" stroke="{INK}" stroke-width="6"/>' if not anim else '',
        P(rr(206, 126, 588, 32, 8), t(1.1), 3, GREY),
        P('M250 205 H520', t(1.35), 12),
        P('M250 236 H450', t(1.55), 6, GREY),
        P(rr(250, 268, 300, 46, 10), t(1.75)),
        P('M268 291 H380', t(1.9), 4, GREY),
        P(rr(250, 330, 300, 46, 10), t(2.05)),
        P('M268 353 H350', t(2.2), 4, GREY),
        (f'<path class="btnf" d="{rr(250,398,160,48,24)}" fill="transparent"/>' if anim else f'<path d="{rr(250,398,160,48,24)}" fill="{YEL}"/>'),
        P(rr(250, 398, 160, 48, 24), t(2.4)),
        P('M290 422 H370', t(2.6), 5),
        P(rr(600, 205, 170, 241, 12), t(2.75), 3, GREY),
        P('M612 217 L758 434', t(2.95), 2, GREY),
        P('M758 217 L612 434', t(3.05), 2, GREY),
    ])

def screen2(anim):
    t = (lambda v: v) if anim else (lambda v: None)
    return ''.join([
        f'<path d="{rr(190,110,620,390,8)}" fill="#fff" stroke="{INK}" stroke-width="6"/>',
        P(rr(206, 126, 588, 32, 8), None, 3, GREY),
        f'<circle cx="500" cy="270" r="46" fill="{YEL}"/>',
        P('M478 270 L494 286 L524 254', t(5.6), 7),
        P('M410 350 H590', None, 10), P('M440 380 H560', None, 6, GREY),
        P(rr(430, 412, 140, 44, 22), None, 3),
    ])

S = 0.194
def thumb(x, y):  # transform that maps the screen (190,110,620x390) onto a node box at x,y
    return f'translate({x - 190*S:.1f} {y - 110*S:.1f}) scale({S})'

LAB = lambda x, y, txt, d, size=17: f'<text class="lt f" style="--d:{d}s" x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{txt}</text>'
ARROW = lambda x1, x2, y, d: P(f'M{x1} {y} H{x2}', d, 3) + P(f'M{x2-9} {y-7} L{x2} {y} L{x2-9} {y+7}', d + .25, 3)
DIAGRAM = ''.join([
    f'<g class="f" style="--d:6.7s" transform="{thumb(205, 230)}">{screen1(False)}</g>',
    LAB(265, 330, 'Formulář', 7.0),
    ARROW(330, 388, 268, 7.3),
    LAB(455, 330, 'Potvrzení', 7.5),
    ARROW(520, 568, 268, 7.7),
    P('M610 230 L648 268 L610 306 L572 268 Z', 8.0, 3),
    LAB(610, 274, 'Chyba?', 8.2, 15),
    ARROW(652, 694, 268, 8.4),
    P(rr(700, 232, 96, 72, 10), 8.6, 3),
    P('M732 268 L744 280 L766 256', 8.8, 5),
    LAB(748, 330, 'Hotovo', 8.9),
    P('M610 310 V378', 9.0, 3), P('M603 369 L610 378 L617 369', 9.2, 3),
    P(rr(556, 382, 108, 52, 10), 9.2, 3),
    LAB(610, 414, 'Oprava', 9.4, 15),
    '<path class="f" style="--d:9.5s" d="M552 408 H265 V316" fill="none" stroke="#a1a1a6" stroke-width="2.5" stroke-dasharray="6 8" stroke-linecap="round"/>',
    LAB(400, 400, 'zpátky do formuláře', 9.8, 14),
])

LAPTOP = f'''<figure class="lap" data-lap aria-label="Animace: notebook se otevře, na obrazovce se nakreslí wireframe, kliknutí přepne na další obrazovku a obrazovky se složí do diagramu toku.">
  <svg viewBox="0 0 1000 600" role="img" aria-hidden="true">
    <defs><clipPath id="lap-screen"><path d="{rr(190,110,620,390,8)}"/></clipPath></defs>
    <ellipse cx="500" cy="566" rx="420" ry="14" class="lap-shadow"/>
    <g class="lid">
      <path d="{rr(170,90,660,430,22)}" class="lap-frame"/>
      <circle cx="500" cy="100" r="3.5" fill="#55555a"/>
      <path d="{rr(190,110,620,390,8)}" class="lap-scr"/>
      <g clip-path="url(#lap-screen)">
        <g class="s1">{screen1(True)}
          <circle class="rip" cx="330" cy="422" r="16" fill="none" stroke="{YEL}" stroke-width="5"/>
        </g>
        <g class="s2">{screen2(True)}</g>
        {DIAGRAM}
        <g class="cur"><path d="M0 0 L0 28 L7.5 21 L12.5 32 L18 29.5 L13 19 L23 19 Z" fill="{INK}" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>
      </g>
    </g>
    <path d="M110 520 H890 L868 550 Q862 558 850 558 H150 Q138 558 132 550 Z" class="lap-base"/>
    <path d="M440 520 H560 Q556 530 546 530 H454 Q444 530 440 520 Z" class="lap-notch"/>
  </svg>
  <figcaption class="lap-cap">Z workshopu rovnou prototyp, na který se dá kliknout. Z prototypu tok, podle kterého staví vývoj.
    <button type="button" class="lap-re">Přehrát znovu</button></figcaption>
</figure>
'''

# proces bez teček, notebook na začátku sekce
h = rep(h, '<section class="canvas proc">\n    <div class="wrap">\n',
        '<section class="proc">\n    <div class="wrap">\n      ' + LAPTOP)
# tečky pod fotkou workshopu, O mně a referencemi (v4 je jinde vypíná, proto vlastní třída)
h = rep(h, '<section class="canvas shot-sec">', '<section class="canvas dots shot-sec">')
WORK = rep(WORK, '<section id="refs" class="canvas">', '<section id="refs" class="canvas dots">')
ABOUT = rep(ABOUT, '<section class="canvas about-top">', '<section class="canvas dots about-top">')
ABOUT = rep(ABOUT, '<section class="canvas board-sec">', '<section class="canvas dots board-sec">')

CSS_R3 = '''
/* ---------- v5 kolo 3 ---------- */
.dots,.canvas.dots{background-image:radial-gradient(var(--grid) 1.4px,transparent 1.4px)!important;background-size:26px 26px}
.note p{font-size:21.5px;line-height:1.72}
/* notebook */
:root{--lap-frame:#2c2c2e;--lap-base:#d4d4d9;--lap-notch:#b4b4ba;--lap-scr:#ffffff;--lap-shadow:rgba(17,17,17,.10)}
:root[data-theme="dark"]{--lap-frame:#3a3a3c;--lap-base:#56565b;--lap-notch:#3f3f44;--lap-scr:#f5f5f7;--lap-shadow:rgba(0,0,0,.5)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--lap-frame:#3a3a3c;--lap-base:#56565b;--lap-notch:#3f3f44;--lap-scr:#f5f5f7;--lap-shadow:rgba(0,0,0,.5)}}
.lap{margin:0 auto clamp(56px,7vw,96px);max-width:900px}
.lap svg{display:block;width:100%;height:auto;overflow:visible}
.lap-frame{fill:var(--lap-frame)}.lap-base{fill:var(--lap-base)}.lap-notch{fill:var(--lap-notch)}.lap-scr{fill:var(--lap-scr)}.lap-shadow{fill:var(--lap-shadow)}
.lap .lt{font-family:var(--hand);font-weight:500;fill:#6e6e73}
.lap .lid{transform-box:view-box;transform-origin:500px 520px;transform:scaleY(.035)}
.lap .d{stroke-dasharray:1;stroke-dashoffset:1}
.lap .f{opacity:0}
.lap .cur{transform-box:view-box;transform:translate(780px,470px);opacity:0}
.lap .rip{transform-box:fill-box;transform-origin:center;opacity:0}
.lap .s1,.lap .s2{transform-box:view-box;transform-origin:0 0}
.lap .s2{transform:translateX(640px)}
.lap.play .lid{animation:lapopen 1s cubic-bezier(.2,.8,.2,1) forwards}
.lap.play .d{animation:lapdraw .55s ease forwards;animation-delay:var(--d)}
.lap.play .f{animation:lapfade .45s ease forwards;animation-delay:var(--d)}
.lap.play .cur{animation:lapcur 1.6s cubic-bezier(.4,0,.2,1) 3.3s forwards}
.lap.play .rip{animation:laprip .6s ease-out 4.25s forwards}
.lap.play .btnf{animation:lapbtn .3s ease 4.3s forwards}
.lap.play .s1{animation:lapout .7s cubic-bezier(.6,0,.3,1) 4.9s forwards}
.lap.play .s2{animation:lapin .7s cubic-bezier(.6,0,.3,1) 4.9s forwards,lapshrink .9s cubic-bezier(.6,0,.3,1) 6.4s forwards}
@keyframes lapopen{to{transform:scaleY(1)}}
@keyframes lapdraw{to{stroke-dashoffset:0}}
@keyframes lapfade{to{opacity:1}}
@keyframes lapcur{0%{opacity:0;transform:translate(780px,470px)}15%{opacity:1}55%{transform:translate(330px,422px)}62%{transform:translate(330px,422px) scale(.85)}70%{transform:translate(330px,422px) scale(1)}90%{opacity:1;transform:translate(330px,422px)}100%{opacity:0;transform:translate(338px,430px)}}
@keyframes laprip{0%{opacity:1;transform:scale(.4)}100%{opacity:0;transform:scale(2.6)}}
@keyframes lapbtn{to{fill:#FFCE1B}}
@keyframes lapout{to{transform:translateX(-640px)}}
@keyframes lapin{to{transform:translateX(0)}}
@keyframes lapshrink{from{transform:translateX(0)}to{transform:''' + f'translate({395-190*S:.1f}px,{230-110*S:.1f}px) scale({S})' + '''}}
.lap-cap{font-family:var(--hand);font-size:18px;color:var(--muted);text-align:center;margin:22px auto 0;max-width:52ch;line-height:1.5}
.lap-re{display:inline-block;margin-left:8px;font-family:var(--display);font-size:13px;font-weight:600;color:var(--ink);background:var(--surface);
  border:0;border-radius:980px;padding:6px 12px;cursor:pointer;vertical-align:1px}
@media (prefers-reduced-motion:reduce){.lap *{animation-duration:1ms!important;animation-delay:0s!important}}
'''
LAP_JS = '''<script>
(function(){var f=document.querySelector("[data-lap]");if(!f)return;
  function play(){f.classList.remove("play");void f.getBoundingClientRect();f.classList.add("play");}
  var b=f.querySelector(".lap-re");if(b)b.addEventListener("click",play);
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window)){f.classList.add("play");return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.target.offsetParent!==null){play();io.disconnect();}});},{threshold:.45});
  io.observe(f);
  window.addEventListener("hashchange",function(){if(!f.classList.contains("play")){io.disconnect();io.observe(f);}});
})();
</script>'''

def post_patch3(out):
    out = rep(out, '&family=Caveat:wght@400..700', '')
    out = rep(out, '--hand:"Shantell Sans","Caveat",ui-rounded,cursive;', '--hand:"Shantell Sans",ui-rounded,"Arial Rounded MT Bold",system-ui,sans-serif;')
    out = rep(out, 'font-family="Shantell Sans, Caveat, cursive"', 'font-family="Shantell Sans, ui-rounded, system-ui, sans-serif"')
    assert 'Caveat' not in out
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R3 + out[i:]
    return out + LAP_JS
