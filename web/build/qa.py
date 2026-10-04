"""QA harness: python3 qa.py out.html route:width:scroll[:scale] ...
Renders the site in srcdoc iframes (own viewport, so media queries apply)."""
import json, sys
R = '/sessions/sweet-modest-heisenberg/mnt/'
site = open(R + 'Career/05 Web/verze/site-v5.html').read()
out = R + 'outputs/' + sys.argv[1]
frames = []
for spec in sys.argv[2:]:
    p = spec.split(':')
    route, w, y = p[0], int(p[1]), int(p[2])
    sc = float(p[3]) if len(p) > 3 else 1.0
    h = int(p[4]) if len(p) > 4 else 1060
    th = p[5] if len(p) > 5 else 'light'
    t = float(p[6]) if len(p) > 6 else 0
    frames.append(dict(route=route, w=w, y=y, sc=sc, h=h, th=th, t=t))
import os
head = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + ('' if os.environ.get('QAANIM') else '<style>*{animation-duration:0s!important;animation-delay:0s!important;transition:none!important}</style>')
page = '''<!doctype html><meta charset="utf-8"><title>QA</title>
<style>body{margin:0;background:#888;display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap;padding:6px}
.f{overflow:hidden;background:#fff;position:relative}.f iframe{border:0;transform-origin:0 0;display:block}
.f b{position:absolute;left:0;top:0;background:#e11;color:#fff;font:11px sans-serif;padding:2px 5px;z-index:2}</style>
<div id="root" style="display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap"></div>
<script>
var SITE=%s, HEAD=%s, FR=%s, EXTRA=%s;
FR.forEach(function(f){
  var d=document.createElement('div'); d.className='f';
  d.style.width=(f.w*f.sc)+'px'; d.style.height=(f.h*f.sc)+'px';
  var i=document.createElement('iframe'); i.width=f.w; i.height=f.h; i.style.transform='scale('+f.sc+')';
  i.srcdoc=HEAD+'<script>try{location.hash="#'+f.route+'"}catch(e){}document.documentElement.setAttribute("data-theme","'+f.th+'");window.QAT='+f.t+'<\\/script>'+SITE+'<script>setTimeout(function(){document.querySelectorAll("[data-rv],.note").forEach(function(e){e.classList.add("in","stuck");e.style.opacity=1});'+EXTRA+';window.scrollTo(0,'+f.y+')},300)<\\/script>';
  var b=document.createElement('b'); b.textContent=f.route+' '+f.w+' @'+f.y+' t'+f.t;
  d.appendChild(i); d.appendChild(b); document.getElementById('root').appendChild(d);
});
</script>''' % (json.dumps(site).replace('</', '<\\/'), json.dumps(head).replace('</', '<\\/'), json.dumps(frames), json.dumps(__import__('os').environ.get('QAJS','0')))
open(out, 'w').write(page)
print(out, len(page))
