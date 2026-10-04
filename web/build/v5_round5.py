# Round 5 (4. 10. 2026): karusel doporučení (2 řádky, tah, rozbalení se zastaví a vycentruje),
# další případy 2 vedle sebe, služby bez štítků a s infografikou pod cenou, Moje výhoda na O mně,
# měnící se nadpis nad notebookem.

# ---------- karusel doporučení
_plain = [re.sub(r'<details class="ref" style="order:\d+">', '<details class="ref">', it) for it in _items]
LI_CARD = ('<a class="ref ref-li" href="https://www.linkedin.com/in/pavelkroupa/">'
           '<span class="ref-claim">Všechna doporučení jsou veřejně na LinkedInu.</span><span class="ref-li-go">Otevřít LinkedIn</span></a>')
def ref_carousel(label):
    r1 = ''.join(_plain[0:6]); r2 = ''.join(_plain[6:]) + LI_CARD
    return (f'<div class="refs rc" data-rc tabindex="0" aria-label="{label}">'
            f'<div class="rc-row">{r1}</div><div class="rc-row">{r2}</div></div>'
            '<p class="rc-hint">Táhněte do strany. Kliknutím otevřete celý text.</p>')

_ra = WORK.index('<div class="refs">'); _rb = WORK.index('<p class="refs-note">', _ra)
WORK = WORK[:_ra] + ref_carousel('Doporučení, posunujte do strany') + '\n      ' + WORK[_rb:]
WORK = re.sub(r'\s*<p class="refs-note">.*?</p>', '', WORK, count=1, flags=re.S)

SERV = rep(SERV, '  <section>\n    <div class="wrap">\n      <p class="eyebrow sig">Kdo co potvrdí</p>', '  <section class="svc-refs">\n    <div class="wrap">\n      <p class="eyebrow sig">Kdo co potvrdí</p>')
_sa = SERV.index('<div class="confirms svc-confirms">'); _sb = SERV.index('\n      </div>\n    </div>\n  </section>', _sa) + len('\n      </div>')
SERV = SERV[:_sa] + ref_carousel('Doporučení, posunujte do strany') + SERV[_sb:]
SERV = rep(SERV, '<p class="eyebrow sig">Kdo co potvrdí</p>\n      <h2>Co říkají lidé, kteří si mě najali.</h2>',
           '<p class="eyebrow sig">Kdo co potvrdí</p>\n      <h2>Co říkají lidé, se kterými jsem pracoval.</h2>')

# ---------- služby: bez tří štítků, infografika až pod nadpisem a cenou
SERV = re.sub(r'\n\s*<ul class="svc-chips">.*?</ul>', '', SERV, count=1, flags=re.S)
assert 'svc-chips' not in SERV
SERV, _n = re.subn(r'(<div class="svc-ill">.*?</svg></div>)(\s*)(<h3>.*?</h3>\s*<span class="svc-price">.*?</span>\s*<span class="svc-fmt">.*?</span>)',
                   r'\3\2\1', SERV, flags=re.S)
assert _n == 3, _n

# ---------- případy: další dva případy vedle sebe
_cn = [0]
def _next_sec(m):
    i = _cn[0]; _cn[0] += 1
    a, b = CASES[(i + 1) % len(CASES)], CASES[(i + 2) % len(CASES)]
    return ('<section class="canvas case-next">\n    <div class="wrap">\n      <p class="eyebrow sig">Další případy</p>\n'
            '      <div class="cards case-cards next-two">\n' + card(a) + card(b) + '      </div>\n    </div>\n  </section>')
CASEV = re.sub(r'<section class="canvas case-next">.*?</section>', _next_sec, CASEV, flags=re.S)
assert _cn[0] == 4

# ---------- Moje výhoda: z úvodu na O mně
_i = h.index('<p class="eyebrow">Moje výhoda</p>'); _a = h.rfind('<section', 0, _i); _b = h.index('</section>', _i) + len('</section>')
ADV = h[_a:_b]
h = h[:_a].rstrip() + '\n\n  ' + h[_b:].lstrip()
ADV = rep(ADV, 'Dalších jedenáct doporučení je <a class="gold" href="#/portfolio">u ukázek práce</a>.',
          'Dalších deset doporučení je <a class="gold" href="#/reference">v portfoliu</a>.')
ABOUT = rep(ABOUT, '  <section class="canvas dots board-sec">', '  ' + ADV + '\n  <section class="canvas dots board-sec">')

# ---------- měnící se nadpis nad notebookem (místo poznámky u šipky)
h = rep(h, '<span>z workshopu rovnou do funkčního prototypu</span></div>', '</div>')
TW = ('<h2 class="tw-h" aria-label="Na workshopu vzniká business logika, prototyp, funkční prototyp, user flow a customer journey.">'
      '<span aria-hidden="true">Na workshopu vzniká<br><span class="tw"><span class="fix tw-w" '
      'data-words="business logika|prototyp|funkční prototyp|user flow|customer journey">business logika</span><span class="tw-c"></span></span></span></h2>')
h = rep(h, '\n      <figure class="lap"', '\n      ' + TW + '\n      <figure class="lap"')

CSS_R5 = '''
/* ---------- v5 kolo 5 ---------- */
/* karusel doporučení */
.refs.rc{display:grid;grid-template-columns:none;gap:22px;align-items:start;margin:44px 0 0;width:100vw;margin-left:calc(50% - 50vw);
  overflow-x:auto;overflow-y:hidden;scrollbar-width:none;padding:14px 0 30px;cursor:grab;outline:none;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 5%,#000 95%,transparent 100%);mask-image:linear-gradient(90deg,transparent 0,#000 5%,#000 95%,transparent 100%)}
.refs.rc::-webkit-scrollbar{display:none}
.refs.rc.drag{cursor:grabbing;user-select:none}
#refs,.svc-refs{overflow-x:clip}
.rc-row{display:flex;gap:22px;width:max-content;align-items:flex-start;padding-inline:11px}
.refs.rc .ref{flex:0 0 360px;width:360px;box-sizing:border-box;transition:flex-basis .4s cubic-bezier(.2,.7,.3,1),width .4s cubic-bezier(.2,.7,.3,1),box-shadow .3s}
.refs.rc .ref[open]{flex-basis:620px;width:620px}
.refs.rc .ref:hover{transform:none}
.ref-li{display:flex;flex-direction:column;justify-content:space-between;gap:18px;padding:28px;text-decoration:none;color:inherit;border:0;background:var(--fix)!important}
.ref-li .ref-claim{color:#1d1d1f!important}
.ref-li-go{font-family:var(--display);font-weight:600;font-size:14.5px;color:#1d1d1f}
.ref-li-go::after{content:" \\2192"}
.rc-hint{font-family:var(--hand);font-size:16px;color:var(--faint);text-align:center;margin:6px auto 0}
@media(max-width:560px){.refs.rc .ref{flex-basis:290px;width:290px}.refs.rc .ref[open]{flex-basis:calc(100vw - 40px);width:calc(100vw - 40px)}}
/* další případy */
.case-next{text-align:center}
.case-next .next-two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px;margin:36px auto 0;text-align:left}
@media(max-width:700px){.case-next .next-two{grid-template-columns:1fr}}
/* služby: infografika pod cenou */
.svc-row-head .svc-ill{margin:20px 0 0}
/* měnící se nadpis */
.tw-h{text-align:center;margin:0 auto 34px}
.tw{display:inline-block;min-height:1.15em}
.tw-c{display:inline-block;width:3px;height:.9em;margin-left:4px;vertical-align:-.08em;background:var(--ink);animation:twblink 1s steps(1) infinite}
@keyframes twblink{50%{opacity:0}}
.bridge{padding-left:0;margin-bottom:10px}
@media (prefers-reduced-motion:reduce){.tw-c{display:none}}
'''

RC_JS = r'''<script>
(function(){
  var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canHover=window.matchMedia("(hover: hover)").matches;
  document.querySelectorAll("[data-rc]").forEach(function(sc){
    var rows=[].slice.call(sc.querySelectorAll(".rc-row"));
    rows.forEach(function(r){[].slice.call(r.children).forEach(function(c){
      var n=c.cloneNode(true);n.setAttribute("aria-hidden","true");n.removeAttribute("open");
      [].forEach.call(n.querySelectorAll("summary,a"),function(x){x.tabIndex=-1;});
      if(n.tagName==="A")n.tabIndex=-1; r.appendChild(n);});});
    var pos=0,last=0,hold=0,hover=false,openEl=null,ours=0;
    function half(){var r=rows[0],k=r.children.length/2;return r.children[k].offsetLeft-r.children[0].offsetLeft;}
    function setPos(p){var H=half();if(H>0){while(p>=H)p-=H;while(p<0)p+=H;}pos=p;ours=Math.round(p);sc.scrollLeft=p;}
    function pause(ms){hold=Date.now()+ms;}
    function tick(t){var dt=last?Math.min(t-last,50):16;last=t;
      if(!reduce&&!hover&&!openEl&&Date.now()>hold&&sc.offsetParent!==null){setPos(pos+0.028*dt);}
      requestAnimationFrame(tick);}
    sc.addEventListener("scroll",function(){if(Math.abs(sc.scrollLeft-ours)>2){pos=sc.scrollLeft;ours=sc.scrollLeft;
      var H=half();if(H>0&&(pos>=H||pos<=0)&&!openEl)setPos(pos);pause(2500);}});
    ["wheel","touchstart"].forEach(function(e){sc.addEventListener(e,function(){pause(2500);},{passive:true});});
    if(canHover){sc.addEventListener("mouseenter",function(){hover=true;});sc.addEventListener("mouseleave",function(){hover=false;});}
    var down=false,sx=0,sl=0,moved=false;
    sc.addEventListener("pointerdown",function(e){if(e.pointerType!=="mouse")return;down=true;moved=false;sx=e.clientX;sl=sc.scrollLeft;});
    window.addEventListener("pointermove",function(e){if(!down)return;var dx=e.clientX-sx;if(Math.abs(dx)>4){moved=true;sc.classList.add("drag");}
      if(moved){setPos(sl-dx);pause(2500);}});
    window.addEventListener("pointerup",function(){if(!down)return;down=false;setTimeout(function(){sc.classList.remove("drag");},0);});
    sc.addEventListener("click",function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false;}},true);
    sc.addEventListener("toggle",function(e){var d=e.target;if(!d||d.tagName!=="DETAILS")return;
      if(d.open){[].forEach.call(sc.querySelectorAll("details[open]"),function(o){if(o!==d)o.open=false;});openEl=d;
        setTimeout(function(){var r=d.getBoundingClientRect(),s=sc.getBoundingClientRect();
          sc.scrollTo({left:sc.scrollLeft+(r.left+r.width/2)-(s.left+s.width/2),behavior:"smooth"});
          var dy=r.height>innerHeight*.85?(r.top-90):((r.top+r.height/2)-innerHeight/2);
          window.scrollBy({top:dy,behavior:"smooth"});},430);}
      else if(openEl===d){openEl=null;pos=sc.scrollLeft;pause(1500);}},true);
    requestAnimationFrame(tick);
  });

  /* měnící se nadpis nad notebookem */
  var w=document.querySelector(".tw-w");
  if(w){var words=w.getAttribute("data-words").split("|"),timer=null,gen=0;
    if(reduce){w.textContent="funkční prototyp";return;}
    var starts=[0,1600,3600,6400,8800];
    function typeTo(word,g,done){var cur=w.textContent;
      (function del(){if(g!==gen)return;if(cur.length){cur=cur.slice(0,-1);w.textContent=cur;timer=setTimeout(del,26);}else(function typ(i){if(g!==gen)return;
        w.textContent=word.slice(0,i);if(i<word.length)timer=setTimeout(function(){typ(i+1);},55);else if(done)done();})(1);})();}
    function run(){gen++;var g=gen;clearTimeout(timer);w.textContent="";var t0=Date.now();
      starts.forEach(function(st,i){setTimeout(function(){if(g!==gen)return;typeTo(words[i],g);},st);});
      setTimeout(function loop(){if(g!==gen)return;var k=0;(function next(){if(g!==gen)return;typeTo(words[k%words.length],g,function(){setTimeout(next,1900);});k++;})();},11800);}
    var lap=document.querySelector("[data-lap]");
    if(lap){new MutationObserver(function(){if(lap.classList.contains("play"))run();}).observe(lap,{attributes:true,attributeFilter:["class"]});
      if(lap.classList.contains("play"))run();}
  }
})();
</script>'''

def post_patch5(out):
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R5 + out[i:]
    return out + RC_JS

# DP infografika: bez duplicitního textu (délka je teď nad ní)
SERV = rep(SERV, '<text x="160" y="52" text-anchor="middle" class="ill-t ill-ts">jeden den, dva, nebo týden</text>', '')
