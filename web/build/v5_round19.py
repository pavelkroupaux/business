# Round 19 (5. 10. 2026, Claude Code): kreslení v úvodu a odesílání kontaktního formuláře.
# - úvod: na počítači jde po úvodní sekci kreslit myší, fixou v barvě písma. Tahy chvíli zůstanou
#   a pak zmizí. Podle prototypu z Claude Chat (pfDraw). Na dotykových zařízeních se nic nemění.
# - kontakt: formulář pošle zprávu e-mailem na FORM_TO_19 přes službu FormSubmit (formsubmit.co),
#   bez účtu a bez klíče. Poprvé přijde na tu adresu e-mail s odkazem „Activate Form“, po kliknutí
#   chodí zprávy rovnou. Odpovědět jde přímo z pošty, odpověď jde na e-mail z formuláře.
# - kontakt: pryč poznámka „Prototyp: formulář zatím nikam neodesílá“, přibyla past na roboty.
FORM_TO_19 = 'design@pavelkroupa.com'

CSS_R19 = '''
/* ---------- v5 kolo 19: kreslení v úvodu ---------- */
.hero2{position:relative}
.hx-pen{position:absolute;left:0;top:0;pointer-events:none;z-index:3}
.hx-pen-hint{display:none}
@media (hover:hover) and (pointer:fine){
  .hero2{cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Cg transform='rotate(45 16 16)'%3E%3Crect x='12.5' y='2' width='7' height='19' rx='2' fill='%23111' stroke='%23fff' stroke-width='1.2'/%3E%3Crect x='12.5' y='4' width='7' height='4' fill='%23FFCE1B'/%3E%3Cpath d='M12.5 21 L19.5 21 L17.6 26.5 L14.4 26.5 Z' fill='%23111' stroke='%23fff' stroke-width='1.2'/%3E%3C/g%3E%3C/svg%3E") 8 24,crosshair}
  .hero2 a,.hero2 button{cursor:pointer}
  .hx-pen-hint{display:block;margin:6px 0 0;max-width:none;text-align:right;font-family:var(--hand);font-size:15px;
    color:var(--faint);transition:opacity .4s}
  .hero2.drew .hx-pen-hint{opacity:0}
}
.hero2.drawing,.hero2.drawing *{-webkit-user-select:none;user-select:none}
/* kontakt: past na roboty (lidé ji nevidí ani na ni nenarazí klávesnicí) a tlačítko při odesílání */
.ct-hp{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);border:0;opacity:0}
.ct-actions .btn[disabled]{opacity:.6;cursor:progress}
'''

JS_R19 = '''<script>
/* Kreslení fixou na tečkovaném papíře v úvodu. Jen myš na počítači, tahy po chvíli zmizí. */
(function(){
  if(!window.matchMedia||!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var sec=document.querySelector(".hero2"); if(!sec||sec.querySelector(".hx-pen")) return;
  var cv=document.createElement("canvas"); cv.className="hx-pen"; cv.setAttribute("aria-hidden","true"); sec.appendChild(cv);
  var ctx=cv.getContext("2d"), st=[], cur=null, raf=0, dpr=Math.max(1,window.devicePixelRatio||1), HOLD=2600,
      FADE=matchMedia("(prefers-reduced-motion: reduce)").matches?1:1200;
  function size(){var r=sec.getBoundingClientRect();cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);cv.style.width=r.width+"px";cv.style.height=r.height+"px";kick();}
  function pos(ev){var r=sec.getBoundingClientRect();return [ev.clientX-r.left,ev.clientY-r.top];}
  function inkColor(){return (getComputedStyle(document.documentElement).getPropertyValue("--ink")||"#111").trim();}
  function paint(){
    raf=0; var now=performance.now(), col=inkColor();
    ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,cv.width,cv.height); ctx.setTransform(dpr,0,0,dpr,0,0);
    ctx.lineCap="round"; ctx.lineJoin="round"; ctx.lineWidth=5; ctx.strokeStyle=col;
    st=st.filter(function(s){return s===cur||now-s.end<HOLD+FADE;});
    st.forEach(function(s){
      var a=(s===cur)?1:Math.min(1,1-(now-s.end-HOLD)/FADE); if(a<=0) return; ctx.globalAlpha=a;
      var p=s.p; ctx.beginPath(); ctx.moveTo(p[0][0],p[0][1]);
      if(p.length<3){ctx.lineTo(p[p.length-1][0]+.01,p[p.length-1][1]);}
      else{for(var i=1;i<p.length-1;i++){var mx=(p[i][0]+p[i+1][0])/2,my=(p[i][1]+p[i+1][1])/2;ctx.quadraticCurveTo(p[i][0],p[i][1],mx,my);}ctx.lineTo(p[p.length-1][0],p[p.length-1][1]);}
      ctx.stroke();
    });
    ctx.globalAlpha=1; if(st.length) kick();
  }
  function kick(){if(!raf) raf=requestAnimationFrame(paint);}
  sec.addEventListener("pointerdown",function(ev){
    if(ev.button!==0||ev.pointerType!=="mouse"||ev.target.closest("a,button,input,label,summary,details")) return;
    ev.preventDefault(); cur={p:[pos(ev)],end:0}; st.push(cur); sec.classList.add("drawing","drew"); kick();
  });
  window.addEventListener("pointermove",function(ev){if(!cur) return; var q=pos(ev),l=cur.p[cur.p.length-1]; if(Math.abs(q[0]-l[0])+Math.abs(q[1]-l[1])>1.5){cur.p.push(q);kick();}});
  window.addEventListener("pointerup",function(){if(!cur) return; cur.end=performance.now(); cur=null; sec.classList.remove("drawing"); kick();});
  if(window.ResizeObserver) new ResizeObserver(size).observe(sec); size();
})();
</script>'''

FORM_HEAD_OLD_19 = '''(function(){var f=document.getElementById("ct-form");if(!f)return;
  f.addEventListener("submit",function(e){e.preventDefault();var bad=[];'''
FORM_HEAD_NEW_19 = '''(function(){var f=document.getElementById("ct-form");if(!f)return;
  /* Odeslání e-mailem přes FormSubmit, viz kolo 19. */
  var TO="https://formsubmit.co/ajax/''' + FORM_TO_19 + '''",busy=false;
  f.addEventListener("submit",function(e){e.preventDefault();if(busy)return;var bad=[];'''
FORM_TAIL_OLD_19 = '''    err.textContent="";f.querySelector(".ct-done").hidden=false;f.querySelector(".ct-actions").hidden=true;});'''
FORM_TAIL_NEW_19 = '''    err.textContent="";
    function v(n){var el=f.elements[n];return el?el.value.trim():"";}
    function done(){f.querySelector(".ct-done").hidden=false;f.querySelector(".ct-actions").hidden=true;}
    if(v("_honey")){done();return;}
    var sel=f.elements.service,btn=f.querySelector("button[type=submit]"),label=btn.textContent;
    var data={name:v("name"),email:v("email"),service:sel&&sel.value?sel.options[sel.selectedIndex].text:"",
      company:v("company"),message:v("msg"),page:location.href,_template:"basic",_captcha:"false",
      _subject:"Zpráva z webu pavelkroupa.com"+(document.documentElement.lang==="en"?" (EN)":"")+": "+v("name")};
    busy=true;btn.disabled=true;btn.textContent="Odesílám…";
    fetch(TO,{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return {};}).then(function(j){if(!r.ok||String(j.success)!=="true")throw new Error(j.message||r.status);});})
      .then(done,function(){err.textContent="Zprávu se nepodařilo odeslat. Zkuste to prosím znovu, nebo mi napište na info@pavelkroupa.com.";})
      .then(function(){busy=false;btn.disabled=false;btn.textContent=label;});
  });'''


def post_patch19(out):
    # úvod: nápověda pod kresbou (jen na počítači s myší, schová se po prvním tahu)
    out = rep(out, '<span>rozhodnuto,<br>dohodnuto,<br>zapsáno</span></div>\n      </figure>\n',
              '<span>rozhodnuto,<br>dohodnuto,<br>zapsáno</span></div>\n      </figure>\n'
              '      <p class="hx-pen-hint" aria-hidden="true">tady můžete kreslit</p>\n')
    # kontakt: odeslání, past na roboty, pryč poznámka o prototypu
    out = rep(out, '<div class="ct-done" hidden><b>Díky, mám to.</b> Ozvu se na e-mail, který jste vyplnili.'
                   '<small>Prototyp: formulář zatím nikam neodesílá.</small></div>',
              '<div class="ct-done" hidden><b>Díky, mám to.</b> Ozvu se na e-mail, který jste vyplnili.</div>')
    out = rep(out, '<div class="ct-actions"><button type="submit" class="btn btn-fill">Odeslat</button>',
              '<input class="ct-hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
              '<div class="ct-actions"><button type="submit" class="btn btn-fill">Odeslat</button>')
    out = rep(out, FORM_HEAD_OLD_19, FORM_HEAD_NEW_19)
    out = rep(out, FORM_TAIL_OLD_19, FORM_TAIL_NEW_19)
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R19 + out[i:]
    return out.rstrip('\n') + '\n' + JS_R19
