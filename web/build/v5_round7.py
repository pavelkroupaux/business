# Round 7 (4. 10. 2026): klienti jako plovoucí pás šedých log v jedné řadě, v černé sekci
# "Kdy týmy potřebují moji pomoc". Loga z Career/img/logos/*.svg se přebarví na jednu šedou,
# bílé části se vyříznou (průhledné). Kde logo chybí, jede v pásu jméno.
import os, base64, unicodedata
LOGO_DIR = R + 'Career/07 Assets/loga klientů/'
LOGO_GREY = '#a1a1a6'
def _key(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', t)
ALIASES = {'Komerční banka': ['komercnibanka', 'kb'], 'Česká spořitelna': ['ceskasporitelna', 'csas', 'sporitelna'],
           'Modrá pyramida': ['modrapyramida', 'mpss'], 'Centropol': ['centropol'], 'WPP': ['wpp'], 'ESET': ['esetcsppprimary', 'eset'],
           'SatoshiLabs': ['satoshilabs', 'trezor'], 'Jablotron': ['jablotron'], 'Coinmate': ['coinmate', 'colorlogo'], 'Leeaf': ['leeaf']}
SKIP = {'logo'}  # Heirloom (Logo.svg) patří do případů, ne mezi klienty
_KEEP_BLACK = True
_WHITE = re.compile(r'^(#fff|#ffffff|white|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))$', re.I)
def _lum(v):
    m = re.match(r'^#([0-9a-f]{3}|[0-9a-f]{6})$', v, re.I)
    if not m: return None
    hx = m.group(1); hx = ''.join(c*2 for c in hx) if len(hx) == 3 else hx
    lin = lambda c: c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4
    r, g, b = (lin(int(hx[i:i+2], 16)/255) for i in (0, 2, 4))
    return .2126*r + .7152*g + .0722*b
CUT = {'#fab20b'}  # Jablotron: žlutý podklad pryč, ať je vidět nápis
def _col(v):
    v = v.strip()
    if v.lower() in ('none', 'transparent', 'inherit') or v.startswith('url('):
        return v
    if _WHITE.match(v) or v.lower() in CUT: return 'none'
    if v.lower() in ('#000',): return '#000'
    L = _lum(v)
    return 'none' if (L is not None and L > .7) else LOGO_GREY
def recolor(svg):
    svg = re.sub(r'<script.*?</script>', '', svg, flags=re.S | re.I)
    svg = re.sub(r'<metadata.*?</metadata>', '', svg, flags=re.S | re.I)
    svg = re.sub(r'\b(fill|stroke|stop-color)="([^"]+)"', lambda m: f'{m.group(1)}="{_col(m.group(2))}"', svg)
    svg = re.sub(r'\b(fill|stroke|stop-color)\s*:\s*([^;"}]+)', lambda m: f'{m.group(1)}:{_col(m.group(2))}', svg)
    # výchozí výplň (prvky bez fill jsou jinak černé)
    svg = re.sub(r'<svg\b(?![^>]*\sfill=)', f'<svg fill="{LOGO_GREY}"', svg, count=1)
    return svg
files = {}
if os.path.isdir(LOGO_DIR):
    for f in sorted(os.listdir(LOGO_DIR)):
        if f.lower().endswith('.svg'):
            files[_key(os.path.splitext(f)[0])] = LOGO_DIR + f
def _img(path, alt):
    svg = open(path, encoding='utf-8').read()
    if 'ESET CS PP - primary' in path:  # bílá písmena v oválu: místo vyříznutí černá, a bez sloganu
        svg = svg.replace('fill: #fff;', 'fill: #000;').replace('viewBox="0 0 580 115"', 'viewBox="0 0 250 115"')
    b64 = base64.b64encode(recolor(svg).encode()).decode()
    return f'<li class="lg"><img src="data:image/svg+xml;base64,{b64}" alt="{alt}" loading="lazy"></li>'
used = set(); items = []
for name in CLIENTS:
    path = next((files[k] for a in ALIASES[name] for k in files if (k.startswith(a) or (len(a) > 4 and a in k))), None)
    if path:
        used.add(path); it = _img(path, name)
        if name == 'SatoshiLabs':
            it = it.replace('</li>', '<span class="lg-t">SatoshiLabs</span></li>').replace('class="lg"', 'class="lg lg-mark"')
        items.append(it)
    else:
        items.append(f'<li class="lg lg-t">{name}</li>')
for k, path in files.items():
    if path not in used and not k.startswith('eset') and k not in SKIP:  # druhá varianta ESET loga se nepoužije
        items.append(_img(path, os.path.splitext(os.path.basename(path))[0]))
LOGO_REPORT = (len(files), sum(1 for i in items if 'lg-t' not in i), [n for n, i in zip(CLIENTS, items) if 'lg-t' in i])
LOGOS = ('<p class="logos-h">Pracoval jsem pro</p>'
         '<div class="marquee logos" aria-label="Klienti"><ul class="mq-track gal-track logo-track">' + ''.join(items) + '</ul></div>')
# pryč ze světlé části pod obory, dovnitř černé sekce nad "Kdy týmy potřebují moji pomoc"
h = re.sub(r'\s*<ul class="client-names" aria-label="Klienti">.*?</ul>', '', h, count=1, flags=re.S)
h = rep(h, '<section class="panel">\n    <div class="wrap">\n      <p class="eyebrow">Kdy týmy potřebují moji pomoc</p>',
        '<section class="panel">\n    <div class="wrap">\n      ' + LOGOS + '\n      <p class="eyebrow">Kdy týmy potřebují moji pomoc</p>')

CSS_R7 = '''
/* ---------- v5 kolo 7: pás log v černé sekci ---------- */
.logos-h{font-family:var(--display);font-size:13px;font-weight:600;color:var(--on-panel-soft);text-align:center;margin:0 auto 6px;max-width:none}
.marquee.logos{padding:10px 0;margin:0 auto clamp(64px,8vw,104px);max-width:1040px}
.mq-track.logo-track{list-style:none;margin:0;padding:0 0 0 56px;gap:56px;align-items:center;animation-duration:70s}
.lg{flex:0 0 auto;height:30px;display:flex;align-items:center}
.lg img{height:24px;width:auto;max-width:140px;display:block}
.lg img[alt="Modrá pyramida"]{height:40px;max-width:none}
.lg img[alt="Česká spořitelna"]{height:32px;max-width:none}
.lg img[alt="WPP"]{height:30px}
.lg img[alt="ESET"]{height:26px}
.lg-mark{gap:8px}
.lg-mark img{height:24px}
.lg-t{font-family:var(--display);font-size:16px;font-weight:700;letter-spacing:-.02em;color:''' + LOGO_GREY + ''';white-space:nowrap}
@media(max-width:560px){.lg img{height:19px}.lg-t{font-size:14px}.mq-track.logo-track{gap:40px}}
'''

def post_patch7(out):
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R7 + out[i:]
