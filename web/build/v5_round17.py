# Round 17 (5. 10. 2026): logo pk v hlavičce, post-it jako favicon, logo v JSON-LD.
import base64 as _b64, urllib.parse as _uq
from lockup import mark as _pk_mark

# pk jako vložené SVG. Barvy písma a linky řídí CSS, takže funguje světlý i tmavý režim.
_vb = re.search(r'viewBox="([^"]+)"', open(B + '../logo/pk/pk-svetle.svg').read()).group(1)
_body = _pk_mark('#000001', '#000002').replace('fill="#000001"', 'class="pk-t"').replace('fill="#000002"', 'class="pk-l"')
PK_SVG = f'<svg class="pk" viewBox="{_vb}" aria-hidden="true" focusable="false">{_body}</svg>'
# hlavička je mimo pohledy, mění se až v hotovém HTML (post_patch17)

CSS_R17 = '''
/* ---------- v5 kolo 17: logo pk v hlavičce ---------- */
.mark .pk{height:30px;width:auto;display:block;flex:none;margin:-6px 0 -4px}
.pk-t,.pk-l{fill:var(--ink)}
:root[data-theme="dark"] .pk-l{fill:#5C5C60}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .pk-l{fill:#5C5C60}}
@media(max-width:480px){.mark .pk{height:26px}}
@media(max-width:380px){.top .mark .pk{display:none}}
'''

_FAV = B + '../logo/favicon/'
_fsvg = open(_FAV + 'favicon.svg').read()
_fapple = _b64.b64encode(open(_FAV + 'apple-touch-icon.png', 'rb').read()).decode()
FAV_TAGS17 = ('<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,' + _uq.quote(_fsvg.replace('"', "'"), safe=" =:/'") + '">\n'
              '<link rel="apple-touch-icon" href="data:image/png;base64,' + _fapple + '">\n'
              '<meta name="theme-color" content="#FFCE1B">\n')

def post_patch17(out):
    out = rep(out, '<a class="mark" href="#/"><i></i>Pavel Kroupa</a>', '<a class="mark" href="#/">' + PK_SVG + 'Pavel Kroupa</a>')
    out = rep(out, FAV_TAGS, FAV_TAGS17)
    out = rep(out, '"@id": "https://www.pavelkroupa.com/#sluzby", "name": "Pavel Kroupa", "url": "https://www.pavelkroupa.com/", ',
              '"@id": "https://www.pavelkroupa.com/#sluzby", "name": "Pavel Kroupa", "url": "https://www.pavelkroupa.com/", '
              '"logo": "https://www.pavelkroupa.com/logo/pk/pk-svetle-ctverec-400.png", ')
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R17 + out[i:]
