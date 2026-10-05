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
  if("IntersectionObserver" in window &&
     !window.matchMedia("(prefers-reduced-motion: reduce)").matches){
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
    if(window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
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
    try{ navigator.clipboard.writeText("info@pavelkroupa.com").then(function(){ cb.textContent="Zkopírováno"; }, sel); }catch(e){ sel(); }
  });
  /* ---------- theme ---------- */
  var modes=["system","light","dark"];
  var glyphs={system:"◑",light:"☀",dark:"☾"};
  var mode="system";
  function setTheme(m){
    mode=m;
    if(m==="system") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme",m);
    document.getElementById("themeGlyph").textContent=glyphs[m];
    try{localStorage.setItem("pk-theme",m);}catch(e){}
  }
  try{ var st=localStorage.getItem("pk-theme"); if(modes.indexOf(st)>-1) setTheme(st); }catch(e){}
  document.getElementById("theme").addEventListener("click",function(){
    setTheme(modes[(modes.indexOf(mode)+1)%modes.length]);
  });
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
  var b=f.querySelector(".lap-re");if(b)b.addEventListener("click",play);
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window)){f.classList.add("play");return;}
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
(function(){var b=document.querySelector(".proc-toggle"),l=document.querySelector(".proc-steps");if(!b||!l)return;
  b.addEventListener("click",function(){var o=l.classList.toggle("open");b.setAttribute("aria-expanded",o?"true":"false");
    b.textContent=o?"Skrýt podrobnosti":"Jak to probíhá podrobně";});})();

}catch(e){console.error(e);}
try{
(function(){var ills=[].slice.call(document.querySelectorAll(".ill"));if(!ills.length)return;
  function on(s){s.classList.remove("on");void s.getBoundingClientRect();s.classList.add("on");}
  if(!("IntersectionObserver" in window)||window.matchMedia("(prefers-reduced-motion: reduce)").matches){ills.forEach(function(s){s.classList.add("on");});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!e.target.classList.contains("on"))on(e.target);});},{threshold:.5});
  ills.forEach(function(s){io.observe(s);var p=s.parentNode;if(p&&window.matchMedia("(hover: hover)").matches){
    var box=p.closest(".svc,.svc-row,.svc-hero-ill")||p;box.addEventListener("mouseenter",function(){on(s);});}});
})();

}catch(e){console.error(e);}
try{
(function(){var els=document.querySelectorAll(".tw-loop");if(!els.length)return;
  var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  els.forEach(function(w){var words=w.getAttribute("data-words").split("|"),k=0,started=false;
    if(reduce){w.textContent=words[0];return;}
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
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window)){fs.forEach(function(f){f.classList.add("still");});return;}
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
(function(){var a=document.getElementById("mail-go");if(a)a.href="mailto:info@pavelkroupa.com?subject="+encodeURIComponent("Dotaz z webu")+"&body="+encodeURIComponent("Zasekli jsme se na: ");})();

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