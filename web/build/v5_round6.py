# Round 6 (4. 10. 2026): úvod podle varianty C, žárovka až po fotce, méně stažených písem.
h = rep(h, '<p class="eyebrow sig">Pavel Kroupa &middot; Definice produktu &middot; Praha a Amsterdam</p>\n', '')
h = re.sub(r'\s*<figcaption class="hx-cap">Poslední pivot:.*?</figcaption>', '', h, count=1, flags=re.S)
assert 'Poslední pivot' not in h
h = re.sub(r'<p class="hand-note".*?</p>', '', h, count=1, flags=re.S)
assert 'hand-note' not in h
h = rep(h, 'a odejdeme s <b class="hl">hotovým zadáním</b>.', 'a <b class="hl">s AI máme hotové zadání za dny, ne týdny</b>.')
# fotka se objeví, když k ní dojede linka; žárovka se rozsvítí hned po ní
h = rep(h, '<g transform="translate(-596.8 -13.4)">', '<g transform="translate(-596.8 -13.4)"><g class="hx-me">')
h = rep(h, 'clip-path="url(#hx-face)"/>', 'clip-path="url(#hx-face)"/></g>')

CSS_R6 = '''
/* ---------- v5 kolo 6 ---------- */
.hx-me{transform-box:fill-box;transform-origin:center;opacity:0;animation:hxme .5s cubic-bezier(.2,.8,.3,1.25) 1.15s forwards}
@keyframes hxme{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
.hx-bulb{animation:hxbulb .9s ease-out 1.75s forwards}
@keyframes hxbulb{0%{opacity:0}25%{opacity:1}40%{opacity:.25}55%{opacity:1}68%{opacity:.5}80%,100%{opacity:1}}
.hero2 .lede-wrap{margin-bottom:6px}
@media (prefers-reduced-motion:reduce){.hx-me,.hx-bulb,.hx-x{opacity:1!important;animation:none!important}}
'''

def post_patch6(out):
    out = rep(out, 'family=Archivo:wght@400..800&', '')
    out = rep(out, '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400', '')
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R6 + out[i:]
