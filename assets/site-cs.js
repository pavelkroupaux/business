/* staré odkazy s #/ vedou na samostatné stránky */
(function(){var h=location.hash;if(h.indexOf("#/")!==0)return;var r=h.slice(1),p=r==="/reference"?"/portfolio/#refs":r.indexOf("/work/")===0?"/portfolio/"+r.slice(6)+"/":r.indexOf("/contact/")===0?"/contact/?service="+r.slice(9):r.slice(-1)==="/"?r:r+"/";location.replace(p);})();
try{
/* ------------------------------------------------------------------
   CS není překlad. Psáno česky od nuly ze stejného faktu.
   Pravidla: Hlas — pravidla.md
   ------------------------------------------------------------------ */
var CS = {};  /* slovník EN→CS z verze 4 smazán v kole 18 */

(function(){
  /* ---------- routing ---------- */
  var map={"/":"v-home","/portfolio":"v-portfolio","/reference":"v-portfolio","/work/heirloom":"v-case-heirloom","/work/coinmate":"v-case-coinmate","/work/leeaf":"v-case-leeaf","/work/breno":"v-case-breno","/work/wpp":"v-case-wpp","/services":"v-services","/services/decision-prototype":"v-svc-dp","/services/fractional":"v-svc-fractional","/services/audit":"v-svc-audit","/about":"v-about","/contact":"v-contact","/contact/decision-prototype":"v-contact","/contact/audit":"v-contact","/contact/fractional":"v-contact"};
  function route(){
    var h=document.documentElement.getAttribute("data-route")||"/";
    if(h.charAt(0)!=="/")h="/";
    var id=map[h]||"v-home";
    Object.keys(map).forEach(function(k){
      var el=document.getElementById(map[k]);
      if(el)el.hidden=(map[k]!==id);
    });
    document.querySelectorAll(".top a.lnk").forEach(function(a){
      var nav=a.getAttribute("data-nav");
      a.classList.toggle("on",nav===h||(nav==="/portfolio"&&(h.indexOf("/work/")===0||h==="/reference"))||(nav==="/contact"&&h.indexOf("/contact")===0)||(nav==="/services"&&h.indexOf("/services/")===0));
    });
    

  }
  /* ---------- scroll reveal ---------- */
  var io=null, armed=false;
  function tag(){
    var sel=[
      "section > .wrap > .eyebrow","section > .wrap > h1","section > .wrap > h2",
      "section > .wrap > .lede","section > .wrap > .row","section > .wrap > .q",
      "section > .wrap > .wide","section > .wrap > .vat","section > .wrap > .two",
      ".clients",".trig > div",".stp",".off",".entry",".cf",".trow",".ask",".todo"
    ].join(",");
    document.querySelectorAll(sel).forEach(function(el){
      if(!el.hasAttribute("data-rv")) el.setAttribute("data-rv","");
    });
  }
  function arm(){
    if(!io) return;
    document.querySelectorAll("[data-rv]:not(.in)").forEach(function(el){
      if(el.offsetParent!==null||el.getClientRects().length) io.observe(el);
    });
  }
  if("IntersectionObserver" in window){
    document.documentElement.classList.add("js");
    tag();
    io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        var el=e.target, sibs=el.parentElement?el.parentElement.children:[el];
        var i=Array.prototype.indexOf.call(sibs,el);
        el.style.transitionDelay=Math.min(i,6)*55+"ms";
        el.classList.add("in");
        io.unobserve(el);
      });
    },{rootMargin:"0px 0px -8% 0px",threshold:.08});
    armed=true;
  }


  /* ---------- lepítka: nalepí se a text se vypíše ---------- */
  var typedFull=new WeakMap();
  function restoreTyped(){
    document.querySelectorAll(".note .type").forEach(function(el){
      if(typedFull.has(el)){ el.textContent=typedFull.get(el); }
    });
  }
  window.__restoreTyped=restoreTyped;
  function typeInto(el){
    var full=typedFull.has(el)?typedFull.get(el):el.textContent;
    typedFull.set(el,full);
    if(!el.style.minHeight && el.offsetHeight) el.style.minHeight=el.offsetHeight+"px";
    var words=full.split(" "), out="", n=0, STEP=17;
    function esc(c){ return c==="&"?"&amp;":c==="<"?"&lt;":c===">"?"&gt;":c; }
    for(var w=0;w<words.length;w++){
      out+='<span class="w">';
      for(var c=0;c<words[w].length;c++){
        out+='<span class="ch" style="animation-delay:'+(n*STEP)+'ms">'+esc(words[w][c])+'</span>';
        n++;
      }
      out+='</span>';
      if(w<words.length-1){
        out+='<span class="ch sp" style="animation-delay:'+(n*STEP)+'ms"> </span>';
        n++;
      }
    }
    el.innerHTML=out;
  }

  function notes(){
    var wrap=document.querySelector("[data-notes]");
    if(!wrap||!("IntersectionObserver" in window)) return;
    wrap.setAttribute("data-armed","");
    var items=wrap.querySelectorAll(".note");
    var nio=new IntersectionObserver(function(es,obs){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        obs.disconnect();
        for(var i=0;i<items.length;i++){
          (function(n,idx){
            setTimeout(function(){
              n.classList.add("stuck");
              var t=n.querySelector(".type");
              /* text je napsaný předem, lepítko se jen nalepí */
            }, idx*260);
          })(items[i],i);
        }
        /* všechna nalepená (poslední začne po (n-1)×260 ms, nalepení trvá 460 ms): teprve pak štítek „Nalep“ */
        setTimeout(function(){wrap.setAttribute("data-done","");wrap.dispatchEvent(new Event("notesdone"));},(items.length-1)*260+460);
      });
    },{rootMargin:"0px 0px -14% 0px",threshold:.3});
    nio.observe(wrap);
  }

  /* ---------- scrollytelling: tabule stojí, kroky jdou ---------- */
  function scrolly(){
    var sc=document.querySelector("[data-scrolly]");
    if(!sc||!("IntersectionObserver" in window)) return;
    if(window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if(!window.matchMedia("(min-width: 861px)").matches) return;
    sc.classList.add("armed");
    var layers=sc.querySelectorAll(".layer");
    function show(n){
      n=+n;
      for(var i=0;i<layers.length;i++){
        var k=+layers[i].getAttribute("data-layer");
        layers[i].classList.toggle("on",k===n);
        layers[i].classList.toggle("over",k<n);
      }
    }
    show(1);
    var sio=new IntersectionObserver(function(es){
      for(var i=0;i<es.length;i++)
        if(es[i].isIntersecting) show(es[i].target.getAttribute("data-step"));
    },{rootMargin:"-46% 0px -46% 0px",threshold:0});
    sc.querySelectorAll(".stp[data-step]").forEach(function(s){ sio.observe(s); });
  }

  document.addEventListener("click",function(e){
    var a=e.target.closest&&e.target.closest("a[data-jump]"); if(!a) return;
    e.preventDefault(); var t=document.querySelector(a.getAttribute("href"));
    if(t) t.scrollIntoView({behavior:"smooth",block:"start"});
  });
  window.addEventListener("hashchange",function(){route();if(armed) setTimeout(arm,0);});
  route();
  if(armed) arm();
  scrolly();
  notes();

  /* ---------- language ---------- */
  var SEL="p,h1,h2,h3,span,li,cite,a.lnk,a.btn,small,em,b,dd,dt,figcaption";
  var store=new WeakMap();
  function norm(x){return x.replace(/\s+/g," ").trim();}
  var lang=document.documentElement.lang||"cs";

  function apply(l){
    var nodes=document.querySelectorAll(SEL);
    for(var i=0;i<nodes.length;i++){
      var el=nodes[i];
      if(!el.isConnected) continue;
      if(!store.has(el)) store.set(el,el.innerHTML);
      var en=norm(store.get(el));
      if(l==="cs"){ if(CS[en]!==undefined) el.innerHTML=CS[en]; }
      else { if(el.innerHTML!==store.get(el)) el.innerHTML=store.get(el); }
    }
    document.documentElement.lang=(l==="cs"?"cs":"en");
    var b=document.getElementById("lang");
    if(b) b.textContent=(l==="cs"?"EN":"CS");
  }
  function setLang(l){
    lang=l;
    if(window.__restoreTyped) window.__restoreTyped();
    apply(l);
    try{localStorage.setItem("pk-lang",l);}catch(e){}
  }

  

  /* ---------- kopírování e-mailu ---------- */
  var cb=document.getElementById("copy-mail");
  if(cb) cb.addEventListener("click",function(){
    function sel(){ var r=document.createRange(); r.selectNodeContents(document.getElementById("mail")); var x=getSelection(); x.removeAllRanges(); x.addRange(r); cb.textContent="Označeno, zkopírujte"; }
    try{ navigator.clipboard.writeText("contact@pavelkroupa.com").then(function(){ cb.textContent="Zkopírováno"; }, sel); }catch(e){ sel(); }
  });
  /* ---------- theme: dokud se neklikne, řídí se systémem; tlačítko přepíná světlý a tmavý ---------- */
  var root=document.documentElement, tb=document.getElementById("theme"), tg=tb&&tb.querySelector(".tg");
  var dq=window.matchMedia?window.matchMedia("(prefers-color-scheme: dark)"):null;
  function applied(){var a=root.getAttribute("data-theme");return a==="light"||a==="dark"?a:(dq&&dq.matches?"dark":"light");}
  function themeLabel(){if(tb)tb.setAttribute("aria-label",applied()==="dark"?"Přepnout na světlý vzhled":"Přepnout na tmavý vzhled");}
  if(tb){themeLabel();
    if(dq&&dq.addEventListener)dq.addEventListener("change",themeLabel);
    tb.addEventListener("click",function(){
      var m=applied()==="dark"?"light":"dark";
      root.setAttribute("data-theme",m);
      try{localStorage.setItem("pk-theme",m);}catch(e){}
      themeLabel();
      if(tg){tg.classList.remove("tg-go");void tg.getBoundingClientRect();tg.classList.add("tg-go");}
    });}
})();

}catch(e){console.error(e);}
try{
(function(){document.querySelectorAll(".gal-track").forEach(function(t){
  var k=Array.prototype.slice.call(t.children);
  for(var r=0;r<3;r++) k.forEach(function(c){var n=c.cloneNode(true);n.setAttribute("aria-hidden","true");t.appendChild(n);});
});})();

}catch(e){console.error(e);}
try{
(function(){var f=document.querySelector("[data-lap]");if(!f)return;
  function play(){f.classList.remove("play");void f.getBoundingClientRect();f.classList.add("play");}
  /* znovu: víko už je otevřené, přehraje se jen diagram */
  var b=f.querySelector(".lap-re");if(b)b.addEventListener("click",function(){f.classList.add("replay");play();});
  if(!("IntersectionObserver" in window)){f.classList.add("play");return;}
  /* notebook stojí zavřený a otevře se až po nadpisu nad ním (jiskry, psaní, žluté zvýraznění): ten pošle událost lapgo */
  if(document.querySelector("h2.lap-h")){f.addEventListener("lapgo",play,{once:true});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.target.offsetParent!==null){play();io.disconnect();}});},{threshold:.45});
  io.observe(f);
  window.addEventListener("hashchange",function(){if(!f.classList.contains("play")){io.disconnect();io.observe(f);}});
})();

}catch(e){console.error(e);}
try{
(function(){
  document.querySelectorAll(".loop-track").forEach(function(t){
    var k=Array.prototype.slice.call(t.children);
    k.forEach(function(c){var n=c.cloneNode(true);n.setAttribute("aria-hidden","true");n.setAttribute("tabindex","-1");t.appendChild(n);});
  });
  /* tlačítko Reference na úvodu vede na /portfolio/#reference: stránka se ukáže a pak plynule (ease-in-out) sjede na reference */
  function toRefs(){
    if(location.hash!=="#reference"&&location.hash!=="#/reference") return;
    var r=document.getElementById("refs"); if(!r) return;
    var top=document.querySelector(".top"), off=(top?top.offsetHeight:0)+8;
    function goal(){return Math.max(0,r.getBoundingClientRect().top+window.pageYOffset-off);}
    function mark(){if(window.history&&history.replaceState) history.replaceState(null,"",location.pathname+location.search+"#refs");}
    if(matchMedia("(prefers-reduced-motion: reduce)").matches){window.scrollTo(0,goal());mark();return;}
    setTimeout(function(){
      var y0=window.pageYOffset, dy=goal()-y0, T=Math.min(1600,Math.max(800,Math.abs(dy)*.9)), t0=0;
      function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
      function step(now){if(!t0)t0=now;var k=Math.min(1,(now-t0)/T);window.scrollTo(0,y0+dy*ease(k));if(k<1)requestAnimationFrame(step);else mark();}
      requestAnimationFrame(step);
    },450);
  }
  window.addEventListener("hashchange",toRefs); toRefs();
})();

}catch(e){console.error(e);}
try{
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
    var starts=[0,2600,5200];
    function typeTo(word,g,done){var cur=w.textContent;
      (function del(){if(g!==gen)return;if(cur.length){cur=cur.slice(0,-1);w.textContent=cur;timer=setTimeout(del,26);}else(function typ(i){if(g!==gen)return;
        w.textContent=word.slice(0,i);if(i<word.length)timer=setTimeout(function(){typ(i+1);},55);else if(done)done();})(1);})();}
    function run(){gen++;var g=gen;clearTimeout(timer);w.textContent="";var t0=Date.now();
      starts.forEach(function(st,i){setTimeout(function(){if(g!==gen)return;typeTo(words[i],g);},st);});
      setTimeout(function loop(){if(g!==gen)return;var k=0;(function next(){if(g!==gen)return;typeTo(words[k%words.length],g,function(){setTimeout(next,1900);});k++;})();},7800);}
    if("IntersectionObserver" in window){var tio=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.target.offsetParent!==null){run();tio.disconnect();}});},{threshold:.6});tio.observe(w);}else run();
  }
})();

}catch(e){console.error(e);}
try{
(function(){var b=document.querySelector(".proc-toggle"),l=document.querySelector(".proc-steps");if(!b||!l)return;var t0=b.textContent;
  /* po rozbalení i sbalení plynule sjede (ease-in-out) k prvnímu kroku, aby čtenář nezůstal uprostřed */
  var raf=0;function stop(){cancelAnimationFrame(raf);raf=0;["wheel","touchstart","keydown"].forEach(function(e){removeEventListener(e,stop);});}
  function toFirst(){var first=l.querySelector(".pstep");if(!first)return;var top=document.querySelector(".top"),
    y0=scrollY,y1=Math.max(0,first.getBoundingClientRect().top+scrollY-(top?top.offsetHeight:0)-24),d=y1-y0;
    if(Math.abs(d)<8)return;
    if(matchMedia("(prefers-reduced-motion: reduce)").matches){scrollTo(0,y1);return;}
    var ms=Math.min(1100,Math.max(500,Math.abs(d)*.6)),t0=performance.now();stop();
    ["wheel","touchstart","keydown"].forEach(function(e){addEventListener(e,stop,{passive:true});});
    (function step(now){var t=Math.min(1,(now-t0)/ms),e=t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
      scrollTo(0,y0+d*e);if(t<1)raf=requestAnimationFrame(step);else stop();})(t0);}
  b.addEventListener("click",function(){var o=l.classList.toggle("open");b.setAttribute("aria-expanded",o?"true":"false");
    b.textContent=o?"Skrýt podrobnosti":t0;toFirst();});})();

}catch(e){console.error(e);}
try{
(function(){var ills=[].slice.call(document.querySelectorAll(".ill"));if(!ills.length)return;
  function on(s){s.classList.remove("on");void s.getBoundingClientRect();s.classList.add("on");}
  if(!("IntersectionObserver" in window)){ills.forEach(function(s){s.classList.add("on");});return;}
  /* v případech je pod sebou víc diagramů (.case-fig): další se spustí, až dokončí předchozí stejné varianty (počítač, mobil) */
  function prevOf(s){var f=s.closest(".case-fig");if(!f)return null;var p=f.previousElementSibling;while(p&&!p.classList.contains("case-fig"))p=p.previousElementSibling;
    return p?p.querySelector("svg."+(s.classList.contains("dg-m")?"dg-m":"dg-d")):null;}
  function go(s){on(s);var a=s.getAnimations?s.getAnimations({subtree:true}).filter(function(x){var t=x.effect&&x.effect.getComputedTiming();return t&&isFinite(t.endTime);}):[];
    s._done=Promise.all(a.map(function(x){return x.finished.catch(function(){});}));}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){var t=e.target;if(!e.isIntersecting||t.classList.contains("on")||t._wait)return;
    var pv=prevOf(t);if(pv&&pv._done){t._wait=true;pv._done.then(function(){t._wait=false;go(t);});}else go(t);});},{threshold:.5});
  ills.forEach(function(s){io.observe(s);var p=s.parentNode;if(p&&window.matchMedia("(hover: hover)").matches){
    var box=p.closest(".svc,.svc-row,.svc-hero-ill");if(box)box.addEventListener("mouseenter",function(){on(s);});}});
})();

}catch(e){console.error(e);}
try{
(function(){var els=document.querySelectorAll(".tw-loop");if(!els.length)return;
  els.forEach(function(w){var words=w.getAttribute("data-words").split("|"),k=0,started=false;
    function typeTo(word,done){var cur=w.textContent;
      (function del(){if(cur.length){cur=cur.slice(0,-1);w.textContent=cur;setTimeout(del,28);}
        else(function typ(i){w.textContent=word.slice(0,i);if(i<word.length)setTimeout(function(){typ(i+1);},60);else done();})(1);})();}
    function next(){k=(k+1)%words.length;typeTo(words[k],function(){setTimeout(next,2000);});}
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!started&&e.target.offsetParent!==null){started=true;setTimeout(next,1600);io.disconnect();}});},{threshold:.6});
    io.observe(w);});
})();

}catch(e){console.error(e);}
try{
/* Kontakt: notebooky nad kartami se přehrají, když jsou vidět, a znovu po najetí myší nebo klepnutí. */
(function(){var fs=document.querySelectorAll(".cx");if(!fs.length)return;
  if(!("IntersectionObserver" in window)){fs.forEach(function(f){f.classList.add("still");});return;}
  /* Kalendář se poprvé přehraje až po dokončení e-mailu (asi 4,8 s), pak už každý zvlášť. */
  var plays=[].map.call(fs,function(f){var busy=false,card=f.closest(".ct-way")||f;
    function play(){if(busy)return;busy=true;f.classList.remove("play");void f.getBoundingClientRect();f.classList.add("play");setTimeout(function(){busy=false;},5000);}
    card.addEventListener("mouseenter",function(){if(f.classList.contains("play"))play();});
    f.addEventListener("click",play);
    return play;});
  /* Každý se pustí, až je vidět a předchozí dohrál (na mobilu jsou karty pod sebou). */
  var seen=[],ready=[true];
  function go(i){if(seen[i]&&ready[i]&&plays[i]){plays[i]=(plays[i](),null);if(i+1<fs.length)setTimeout(function(){ready[i+1]=true;go(i+1);},4800);}}
  [].forEach.call(fs,function(f,i){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();seen[i]=true;go(i);}});},{threshold:.5});io.observe(f);});
})();

}catch(e){console.error(e);}
try{
/* Kontakt: e-mail s předvyplněným předmětem a začátkem zprávy (bez skriptu zůstává prostý odkaz). */
(function(){var a=document.getElementById("mail-go");if(a)a.href="mailto:contact@pavelkroupa.com?subject="+encodeURIComponent("Dotaz z webu")+"&body="+encodeURIComponent("Zasekli jsme se na: ");})();

}catch(e){console.error(e);}
try{
(function(){var sel=document.getElementById("ct-service");if(!sel)return;
  function pick(){var s=new URLSearchParams(location.search).get("service");[].some.call(sel.options,function(o){if(o.value===s){sel.value=s;return true;}});}
  window.addEventListener("hashchange",pick);pick();})();

}catch(e){console.error(e);}
try{
/* Kreslení fixou na tečkovaném papíře v úvodu. Jen myš na počítači, tahy po chvíli zmizí. */
(function(){
  if(!window.matchMedia||!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var sec=document.querySelector(".hero2"); if(!sec||sec.querySelector(".hx-pen")) return;
  var cv=document.createElement("canvas"); cv.className="hx-pen"; cv.setAttribute("aria-hidden","true"); sec.appendChild(cv);
  var ctx=cv.getContext("2d"), st=[], cur=null, raf=0, dpr=Math.max(1,window.devicePixelRatio||1), HOLD=2600,
      FADE=matchMedia("(prefers-reduced-motion: reduce)").matches?1:1200;
  function size(){var r=sec.getBoundingClientRect();cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);cv.style.width=r.width+"px";cv.style.height=r.height+"px";kick();}
  function pos(ev){var r=sec.getBoundingClientRect();return [ev.clientX-r.left,ev.clientY-r.top];}
  function inkColor(){return (getComputedStyle(document.documentElement).getPropertyValue("--marker")||"#E0241B").trim();}
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

/* Lepítka s otázkami v sekci „Kdy týmy potřebují moji pomoc“. Kurzor je malé lepítko, klik kamkoli nalepí větší s další otázkou. Jen myš na počítači. */
(function(){
  if(!window.matchMedia||!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var sec=document.querySelector(".pdots"); if(!sec||!sec.querySelector("[data-notes]")) return;
  var Q=["Kde jste se zasekli?","Kdo bude na schůzce?","Kdo bude decision maker?"], n=0, MAX=6;
  sec.classList.add("pq-on");
  sec.addEventListener("pointerdown",function(ev){
    if(ev.button!==0||ev.pointerType!=="mouse"||ev.target.closest("a,button,input,label,summary,details")) return;
    ev.preventDefault();
    var r=sec.getBoundingClientRect(), x=Math.min(Math.max(ev.clientX-r.left,96),r.width-96), y=Math.max(ev.clientY-r.top,70);
    var p=document.createElement("div"); p.className="pq"; p.setAttribute("aria-hidden","true");
    p.style.left=x+"px"; p.style.top=y+"px"; p.style.setProperty("--rot",(Math.random()*8-4).toFixed(1)+"deg");
    p.textContent=Q[n%Q.length]; n++; sec.appendChild(p);
    var all=sec.querySelectorAll(".pq:not(.gone)");
    if(all.length>MAX){var o=all[0];o.classList.add("gone");setTimeout(function(){o.remove();},450);}
  });
})();


}catch(e){console.error(e);}
try{
/* Kouzlo před nadpisem „Pak z toho postavím funkční prototyp“. Jedna časová osa, spustí se, když je nadpis zhruba v polovině obrazovky:
   nejdřív se rychle nakreslí šipka, pak se rozsvítí jiskry a prokmitne „magic“, nadpis se napíše písmeno po písmenu (30 ms),
   žluté zvýraznění se protáhne pod slovy a teprve potom se otevře notebook (událost lapgo). */
(function(){var h=document.querySelector("h2.lap-h");if(!h||!("IntersectionObserver" in window))return;var calm=matchMedia("(prefers-reduced-motion: reduce)").matches;
  h.removeAttribute("data-rv");h.classList.remove("in");
  /* psaní: napsaná část je vidět, zbytek je neviditelný, ale zabírá místo, takže se nadpis nepřelamuje a nepřeskakuje */
  var full=h.cloneNode(true),total=full.textContent.length;
  function upto(n){var c=full.cloneNode(true),left=n,tw=document.createTreeWalker(c,NodeFilter.SHOW_TEXT),ts=[],t;
    while((t=tw.nextNode()))ts.push(t);
    ts.forEach(function(t){var k=Math.min(left,t.data.length);left-=k;
      if(k<t.data.length){var r=document.createElement("span");r.className="mg-r";r.textContent=t.data.slice(k);t.data=t.data.slice(0,k);t.parentNode.insertBefore(r,t.nextSibling);}});
    if(n>0){var q=document.createElement("span");q.className="mg-c";q.setAttribute("aria-hidden","true");var r0=c.querySelector(".mg-r");
      if(r0)r0.parentNode.insertBefore(q,r0);else c.appendChild(q);}
    return c.innerHTML;}
  h.setAttribute("aria-label",full.textContent.replace(/\s+/g," ").trim());
  h.classList.add("mg-typing");h.innerHTML=upto(0);
  function type(i){h.innerHTML=upto(i);
    if(i<total)setTimeout(function(){type(i+1);},30);else setTimeout(sweep,250);}
  function sweep(){h.innerHTML=full.innerHTML;h.removeAttribute("aria-label");h.classList.remove("mg-typing");h.classList.add("mg-sweep");
    setTimeout(function(){var f=document.querySelector("[data-lap]");if(f)f.dispatchEvent(new Event("lapgo"));},900);}
  var w=document.createElement("div");w.className="mg";h.parentNode.insertBefore(w,h);w.appendChild(h);
  var b=document.createElement("span");b.className="mg-burst";b.setAttribute("aria-hidden","true");
  var S='<svg viewBox="0 0 24 24"><path d="M12 0C12.5 9 15 11.5 24 12C15 12.5 12.5 15 12 24C11.5 15 9 12.5 0 12C9 11.5 11.5 9 12 0Z"/></svg>';
  [[-190,-36,17,0],[-112,-62,11,.12],[-34,-72,20,.05],[54,-64,12,.2],[134,-46,18,.08],[208,-8,11,.26],
   [156,44,15,.16],[46,58,10,.3],[-72,52,16,.22],[-168,24,11,.34]]
  .forEach(function(p){var s=document.createElement("i");s.className="mg-s";
    s.style.cssText="--x:"+p[0]+"px;--y:"+p[1]+"px;--z:"+p[2]+"px;--t:"+p[3]+"s";s.innerHTML=S;b.appendChild(s);});
  var m=document.createElement("span");m.className="mg-word";m.textContent="magic";b.appendChild(m);
  w.insertBefore(b,h);
  /* šipka nad nadpisem: nenakreslená, při spuštění se rychle nakreslí (třída br-go) */
  var br=document.querySelector(".bridge");
  if(br){[].forEach.call(br.querySelectorAll("path"),function(q){q.setAttribute("pathLength","1");});br.classList.add("br-arm");}
  /* spouštěč: horní okraj nadpisu přejde přes čáru 55 % výšky obrazovky */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.disconnect();
    if(br)br.classList.add("br-go");setTimeout(function(){if(!calm)w.classList.add("mg-go");setTimeout(function(){type(1);},calm?0:450);},br?380:0);});},{threshold:0,rootMargin:"0px 0px -45% 0px"});
  io.observe(w);
})();

}catch(e){console.error(e);}
try{
/* volba jazyka přepínačem EN/CS se pamatuje (pk-lang), úvodní přesměrování podle zařízení ji pak nepřebíjí */
(function(){var a=document.getElementById("lang");if(!a)return;
  a.addEventListener("click",function(){try{localStorage.setItem("pk-lang",a.getAttribute("hreflang")||"");}catch(e){}});})();

}catch(e){console.error(e);}
try{
/* Štítek u kurzoru jako u spolupracovníka ve Figmě: „Nakresli“ u tužky v úvodu, „Nalep“ u lepíku v sekci s otázkami.
   Jde za myší s lehkým zpožděním, schová se nad odkazem a po prvním tahu nebo nalepení zmizí nadobro. Jen myš na počítači. */
(function(){
  if(!window.matchMedia||!matchMedia("(hover: hover) and (pointer: fine)").matches) return;
  var still=matchMedia("(prefers-reduced-motion: reduce)").matches;
  function tag(sec,text,wait){
    if(!sec) return;
    var t=document.createElement("span"); t.className="mp-tag"; t.setAttribute("aria-hidden","true"); t.textContent=text; sec.appendChild(t);
    var x=0,y=0,done=false,shown=false,ok=!wait,seen=false,out=false,lx=0,ly=0;
    function hide(){t.classList.remove("on");shown=false;}
    /* lx, ly = poslední známá poloha myši v okně. Štítek sedí přesně u myši, bez doznívání. Při scrollu se myš nehýbe, ale stránka ano,
       takže se poloha přepočítá i tehdy, a štítek se schová, když myš už není nad sekcí nebo je nad odkazem */
    function place(el){
      var r=sec.getBoundingClientRect(); x=lx-r.left+16; y=ly-r.top+18;
      if(!ok) return;
      if(el&&el.closest&&el.closest("a,button,input,label,summary,details,.pq")){hide();return;}
      t.style.transform="translate("+x.toFixed(1)+"px,"+y.toFixed(1)+"px)";
      if(!shown){shown=true;t.classList.add("on");}}
    function under(){if(!seen||out||done) return null;var el=document.elementFromPoint(lx,ly);return el&&sec.contains(el)?el:null;}
    /* štítek se ukáže až po animaci sekce; když je myš už nad sekcí, objeví se u ní hned */
    if(wait) wait(function(){ok=true;var el=under();if(el)place(el);});
    sec.addEventListener("pointermove",function(ev){
      if(done||ev.pointerType!=="mouse") return;
      lx=ev.clientX; ly=ev.clientY; seen=true; out=false; place(ev.target);
    });
    document.documentElement.addEventListener("mouseleave",function(){out=true;hide();});
    addEventListener("scroll",function(){
      var el=under(); if(el) place(el); else if(shown) hide();
    },{passive:true});
    sec.addEventListener("pointerleave",hide);
    sec.addEventListener("pointerdown",function(ev){if(ev.button!==0||ev.target.closest("a,button,input,label,summary,details")) return;
      done=true;t.classList.add("bye");hide();setTimeout(function(){t.remove();},400);});
  }
  /* úvod: až doběhne animace kresby (čeká na všechny animace v .hx), pak štítek i nápověda pod kresbou */
  var hero=document.querySelector(".hero2");
  tag(hero,"Nakresli",function(go){
    function end(){if(hero) hero.classList.add("hx-done");go();}
    var s=hero&&hero.querySelector(".hx");
    if(!s){end();return;}
    if(!s.getAnimations){setTimeout(end,5000);return;}
    var a=s.getAnimations({subtree:true});
    if(!a.length){end();return;}
    Promise.all(a.map(function(x){return x.finished;})).then(end,end);
  });
  /* lepítka: až se nalepí všechna čtyři */
  var p=document.querySelector(".pdots"), w=p&&p.querySelector("[data-notes]");
  if(w) tag(p,"Nalep",function(go){
    if(!w.hasAttribute("data-armed")||w.hasAttribute("data-done")) go(); else w.addEventListener("notesdone",go,{once:true});
  });
})();

}catch(e){console.error(e);}
try{
/* Karusel na mobilu (data-bc): karty vedle sebe, další vykukuje zprava, pod nimi šipky a tečky.
   Na širší obrazovce zůstává mřížka, ovládání je schované v CSS. */
(function(){
  var still=matchMedia("(prefers-reduced-motion: reduce)").matches;
  [].forEach.call(document.querySelectorAll("[data-bc]"),function(el){
    var items=[].slice.call(el.children); if(items.length<2) return;
    el.classList.add("bc");
    function btn(c,l,h){var b=document.createElement("button");b.type="button";b.className=c;b.setAttribute("aria-label",l);if(h)b.innerHTML=h;return b;}
    var A='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    var nav=document.createElement("div"); nav.className="bc-nav";
    var prev=btn("bc-arr bc-prev","Předchozí karta",A), next=btn("bc-arr bc-next","Další karta",A), dots=document.createElement("div"); dots.className="bc-dots";
    var ds=items.map(function(it,i){var d=btn("bc-dot","Karta %s z %s".replace("%s",i+1).replace("%s",items.length));d.addEventListener("click",function(){go(i);});dots.appendChild(d);return d;});
    nav.appendChild(prev); nav.appendChild(dots); nav.appendChild(next);
    el.parentNode.insertBefore(nav,el.nextSibling);
    function pad(){return parseFloat(getComputedStyle(el).paddingLeft)||0;}
    function go(i){i=Math.max(0,Math.min(items.length-1,i));
      el.scrollTo({left:items[i].offsetLeft-pad(),behavior:still?"auto":"smooth"});}
    var k=-1,raf=0;
    function cur(){var x=el.scrollLeft,p=pad();
      if(x>=el.scrollWidth-el.clientWidth-2) return items.length-1;
      var b=0,bd=1e9;items.forEach(function(it,i){var d=Math.abs(it.offsetLeft-p-x);if(d<bd){bd=d;b=i;}});return b;}
    function upd(){raf=0;var i=cur();if(i===k)return;k=i;
      ds.forEach(function(d,j){if(j===i)d.setAttribute("aria-current","true");else d.removeAttribute("aria-current");});
      prev.disabled=i===0;next.disabled=i===items.length-1;}
    el.addEventListener("scroll",function(){if(!raf)raf=requestAnimationFrame(upd);},{passive:true});
    addEventListener("resize",function(){k=-1;upd();});
    prev.addEventListener("click",function(){go(cur()-1);});
    next.addEventListener("click",function(){go(cur()+1);});
    upd();
  });
})();

}catch(e){console.error(e);}
