# Round 11 (5. 10. 2026): čitelné popisky v úvodní kresbě, obory na mobilu jako štítky a s jednotnými názvy,
# loga s odkazem, bez "prototyp" u workshopu, miniatury služeb bez animace, reference bez popisů,
# externí odkazy do nového tabu, služby: bez otázek nad kartami, Decision Prototype: přepisované slovo,
# diagram na mobilu, případy v praxi s logem a bez citace, cena v "Jak to probíhá".

SECTOR_NAMES = [('Regulovaná kryptoburza', 'Regulované krypto'), ('Bankovnictví pro občany', 'Bankovnictví'),
                ('Zdravotnictví, léčba neplodnosti', 'Zdravotnictví'), ('Maloobchod a e-shopy', 'E-shopy')]
LOGO_URL = {'Komerční banka': 'https://www.kb.cz', 'Česká spořitelna': 'https://www.csas.cz', 'Modrá pyramida': 'https://www.modrapyramida.cz',
            'Centropol': 'https://www.centropol.cz', 'WPP': 'https://www.wpp.com', 'ESET': 'https://www.eset.com',
            'SatoshiLabs': 'https://satoshilabs.com', 'Jablotron': 'https://www.jablotron.com', 'Coinmate': 'https://coinmate.io',
            'Leeaf': 'https://leeaf.com', 'logo-breno-dark': 'https://www.breno.cz'}

MOBILE_FLOW = '''<div class="flow-m" aria-label="Jak probíhá jedno kolo">
  <div class="fm-start"><span><b>Hotový produkt</b>repozitář · návrhy</span><span><b>Nový nápad</b>zatím bez produktu</span></div>
  <ol class="fm-steps">
    <li class="on"><i>1</i><div><b>Probrat to spolu</b><small>řízená diskuse</small><span>Kdo rozhoduje · Otázky místo slajdů · Proces služby živě</span></div></li>
    <li><i>2</i><div><b>Zmapovat službu</b><small>mapa navigace</small><span>Obrazovky a role · Co je v rozsahu</span></div></li>
    <li><i>3</i><div><b>Postavit obrazovky</b><small>výstupy</small><span>Logika služby · Průchody · Obrazovky a stavy · Dokumentace</span></div></li>
    <li><i>4</i><div><b>Sdílet jeden odkaz</b><small>nasazený prototyp</small><span>Komentáře · Verze</span></div></li>
  </ol>
  <p class="fm-loop">&#8635; Řízená kola úprav: byznys + vývoj, změny</p>
  <p class="fm-note">Z vašich skutečných komponent a tokenů. Není to produkční kód. Vývoj podle něj staví, až je rozhodnuto.</p>
  <div class="fm-end"><span><b>Rozhodnutý rozsah</b>první verze · průchody · zápis rozhodnutí</span><span><b>Podklad pro vývoj</b>mapa navigace · stavy · tokeny</span></div>
</div>'''

def _price_row(title, text):
    return f'<div class="stp-row stp-price-row"><span class="mk">Cena</span><div><h3>{title}</h3><p>{text}</p></div></div>'

CSS_R11 = '''
/* ---------- v5 kolo 11 ---------- */
/* úvodní kresba: popisky čitelné, na mobilu pod kresbou */
.hx-labs-m{display:none}
@media(max-width:700px){.hx-lab{display:none}
  .hx-labs-m{display:flex;justify-content:space-between;gap:16px;margin-top:8px;font-family:var(--hand);font-size:14px;line-height:1.3;color:var(--muted)}
  .hx-labs-m span{flex:1 1 0;min-width:0}
  .hx-labs-m span:last-child{text-align:right}}
/* obory na mobilu jako štítky */
@media(max-width:700px){
  .sectors{display:flex!important;flex-wrap:wrap;justify-content:center;gap:8px;grid-template-columns:none}
  .sectors li{flex-direction:row;gap:7px;padding:8px 13px;border-radius:980px;background:var(--surface);font-size:13px}
  .sectors svg{width:17px;height:17px}}
/* loga s odkazem */
.lg a{display:flex;align-items:center;gap:8px;border:0;text-decoration:none;color:inherit;transition:opacity .2s}
.lg a:hover{opacity:.7}
/* miniatury služeb bez animace */
.svc-thumb .ill *{animation:none!important}
.svc-thumb .ia{opacity:1;transform:none}
.svc-thumb .dfill{transform:none}
.svc-thumb .wk{display:none}
.svc-thumb .prog,.svc-thumb .ln{stroke-dashoffset:0}
.svc-thumb .num{fill:#FFCE1B;stroke:#FFCE1B}
.svc-thumb .numt,.svc-thumb .don{fill:#1d1d1f}
a.svc{position:relative}
@media(max-width:700px){a.svc .svc-thumb{position:absolute;top:22px;right:20px;width:92px;max-width:92px;margin:0}
  a.svc h3,a.svc .svc-price{padding-right:104px}}
/* Decision Prototype: diagram na mobilu svisle */
.flow-m{display:none}
@media(max-width:700px){.diagram svg{display:none}.diagram{padding:20px 18px;overflow:visible}.flow-m{display:block;text-align:left}}
.fm-start,.fm-end{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.fm-start span,.fm-end span{border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;font-size:12.5px;color:#6e6e73;line-height:1.35}
.fm-start b,.fm-end b,.fm-steps b{display:block;font-family:var(--display);font-size:14.5px;color:#1d1d1f}
.fm-steps{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:12px;position:relative}
.fm-steps::before{content:"";position:absolute;left:15px;top:14px;bottom:14px;border-left:2px dashed #c7c7cc}
.fm-steps li{position:relative;display:grid;grid-template-columns:32px 1fr;gap:12px;align-items:start}
.fm-steps i{width:32px;height:32px;border-radius:50%;background:#fff;border:2px solid #1d1d1f;display:grid;place-items:center;font-style:normal;font-family:var(--display);font-weight:700;font-size:14px;color:#1d1d1f}
.fm-steps li.on i{background:#FFCE1B;border-color:#FFCE1B}
.fm-steps li>div{border:1.5px solid #e5e5ea;border-radius:12px;padding:10px 12px;background:#fff}
.fm-steps li.on>div{background:#FFCE1B;border-color:#FFCE1B}
.fm-steps small{display:block;font-size:12px;color:#6e6e73;margin:1px 0 4px}
.fm-steps span{font-size:12.5px;color:#3a3a3c;line-height:1.4}
.fm-loop{font-family:var(--hand);font-size:15px;color:#6e6e73;margin:14px 0 0;text-align:center;max-width:none}
.fm-note{font-size:12.5px;color:#6e6e73;margin:6px 0 14px;text-align:center;max-width:none}
/* cena v "Jak to probíhá" */
.stp-price{display:inline-block;margin-top:8px;font-family:var(--display);font-size:15px;font-weight:700;color:var(--ink);
  background:linear-gradient(to top,var(--fix) 38%,transparent 38%)}
.stp-price-row h3{font-size:clamp(22px,2.4vw,28px)}
.stp-price-row p{color:var(--muted)}
.case-cards.one{grid-template-columns:minmax(0,560px);justify-content:center}
'''

GEN_TW_JS = r'''<script>
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
</script>'''

def post_patch11(out):
    body_start = out.index('<main>')
    head_part, body = out[:body_start], out[body_start:]
    # popisky kresby
    body = rep(body, 'font-size="30" font-weight="500" fill="var(--muted)"', 'font-size="40" font-weight="500" fill="var(--muted)"')
    _i = body.index('</svg>', body.index('class="hx-lab"')) + len('</svg>')
    body = body[:_i] + '<div class="hx-labs-m" aria-hidden="true"><span>tým se cyklí ve schůzkách</span><span>rozhodnuto, dohodnuto, zapsáno</span></div>' + body[_i:]
    # obory
    for a, b in SECTOR_NAMES:
        body = rep(body, f'<span>{a}</span>', f'<span>{b}</span>')
    # loga s odkazem do nového tabu
    def _wrap(m):
        inner = m.group(2)
        alt = re.search(r'alt="([^"]+)"', inner)
        name = alt.group(1) if alt else re.sub(r'<[^>]+>', '', inner).strip()
        url = LOGO_URL.get(name) or LOGO_URL.get(name.replace('SatoshiLabs', 'SatoshiLabs'))
        if not url: return m.group(0)
        return f'{m.group(1)}<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">{inner}</a></li>'
    _a = body.index('<ul class="mq-track gal-track logo-track">'); _b = body.index('</ul>', _a)
    strip = re.sub(r'(<li class="lg[^"]*">)(.*?)</li>', _wrap, body[_a:_b], flags=re.S)
    body = body[:_a] + strip + body[_b:]
    # workshop: bez prototypu
    body = rep(body, 'data-words="business logika|user flow|prototyp|funkční prototyp|customer journey"', 'data-words="business logika|user flow|customer journey"')
    body = rep(body, 'aria-label="Na workshopu vzniká business logika, user flow, prototyp, funkční prototyp a customer journey."', 'aria-label="Na workshopu vzniká business logika, user flow a customer journey."')
    body = rep(body, 'var starts=[0,2600,5600,7600,9600];', 'var starts=[0,2600,5200];')
    body = rep(body, '},12600);}', '},7800);}')
    # portfolio a služby: reference bez popisů
    body = rep(body, '\n      <p class="lede">Krátké verze. Celý případ s rozhodnutími, riziky a cenou vám pošlu po hovoru.</p>', '')
    body = rep(body, '<p class="eyebrow sig">Kdo co potvrdí</p>\n      <h2>Jedenáct doporučení, jejich slovy.</h2>\n      <p class="lede">Jedna věta od každého. Rozklikněte celý text. Citace jsou v původním znění.</p>', '<h2>Reference</h2>')
    body = rep(body, '<p class="eyebrow sig">Kdo co potvrdí</p>\n      <h2>Co říkají lidé, se kterými jsem pracoval.</h2>', '<h2>Reference</h2>')
    body = body.replace('<p class="rc-hint">Táhněte do strany. Kliknutím otevřete celý text.</p>', '')
    body = body.replace('LinkedIn text zkracuje. <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Celý je tam</a>.',
                        '<a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Celé doporučení na LinkedInu</a>')
    # služby: jen názvy v kartách výběru
    body = re.sub(r'<span class="pick-q">[^<]*</span>', '', body)
    body = rep(body, '\n      <p class="lede">Vyberte podle toho, kde jste se zasekli.</p>', '')
    # miniatury na úvodu: hned hotové (bez animace)
    body = body.replace('<div class="svc-thumb"><svg class="ill ', '<div class="svc-thumb"><svg class="ill on static ')
    # Decision Prototype: přepisované slovo, diagram na mobilu, případy s logem, cena
    body = re.sub(r'<span class="swap">.*?</span></span>',
                  '<span class="tw"><span class="fix tw-loop" data-words="iterací|workshopem|rozhovorem">iterací</span><span class="tw-c"></span></span>', body, count=1, flags=re.S)
    _d = body.index('<figure class="diagram">'); _e = body.index('</figure>', _d)
    body = body[:_e] + MOBILE_FLOW + body[_e:]
    # případy v praxi: logo, bez citace
    g_cm, g_hl = _grey_src('color_logo.svg'), _grey_src('Logo.svg')
    body = rep(body, '<a class="card case-card" href="#/work/coinmate"><span class="card-meta">Coinmate &middot; Regulovaná kryptoburza</span>',
               f'<a class="card case-card" href="#/work/coinmate"><img class="card-logo" src="{g_cm}" alt="Coinmate"><span class="card-meta">Coinmate &middot; Regulovaná kryptoburza</span>')
    body = rep(body, '<a class="card case-card" href="#/work/heirloom"><span class="card-meta">Heirloom &middot; Digitální dědictví</span>',
               f'<a class="card case-card" href="#/work/heirloom"><img class="card-logo" src="{g_hl}" alt="Heirloom"><span class="card-meta">Heirloom &middot; Digitální dědictví</span>')
    body = re.sub(r'\s*<blockquote class="q"><p>&ldquo;He was also an early adopter.*?</blockquote>', '', body, count=1, flags=re.S)
    cm_card = (f'<div class="cards case-cards one"><a class="card case-card" href="#/work/coinmate"><img class="card-logo" src="{g_cm}" alt="Coinmate">'
               '<span class="card-meta">Coinmate &middot; 2023&ndash;2026</span><h3 class="card-title">Nejdřív design systém, potom nová identita</h3>'
               '<span class="card-proves">Rebranding spuštěn 1. 10. 2026.</span><span class="card-go">Otevřít případ</span></a></div>')
    _f = body.index('<h2><span class="fix">Dva dny v týdnu</span> v Coinmate.</h2>')
    _g = body.index('<blockquote class="q">', _f); _h = body.index('</blockquote>', _g) + len('</blockquote>')
    body = body[:_g] + cm_card + body[_h:]
    # cena přímo v "Jak to probíhá", samostatné Podmínky pryč
    for mk, price in (('Jeden den', 'od 49 000 Kč'), ('Dva dny', 'od 125 000 Kč'), ('Týden', 'od 220 000 Kč')):
        body = re.sub(rf'(<div class="stp-row"><span class="mk">{mk}</span><div><h3>[^<]*</h3><p>[^<]*</p>)', rf'\1<span class="stp-price">{price}</span>', body, count=1)
    ROWS_END = {'Celá oblast produktu': _price_row('Dohodneme se na první schůzce', 'Ceny výše jsou výchozí. Konečnou nabídku pošlu po první schůzce podle rozsahu, složitosti a velikosti produktu.'),
                'Předání': None, 'Den 5': None}
    _s = body.index('<div class="stp-list">', body.index('id="v-svc-dp"')); _t = body.index('</div></div></div>', _s) + len('</div></div>')
    body = body[:_t] + ROWS_END['Celá oblast produktu'] + body[_t:]
    _s = body.index('<div class="stp-list">', body.index('id="v-svc-fractional"')); _t = body.index('</div></div></div>', _s) + len('</div></div>')
    body = body[:_t] + _price_row('od 120 000 Kč měsíčně', 'Dva dny v týdnu, nejméně tři měsíce. Konečnou nabídku pošlu po první schůzce podle rozsahu a velikosti týmu.') + body[_t:]
    _s = body.index('<div class="stp-list">', body.index('id="v-svc-audit"')); _t = body.index('</div></div></div>', _s) + len('</div></div>')
    body = body[:_t] + _price_row('od 29 000 Kč', 'Pět pracovních dní, bez schůzek. Konečnou nabídku pošlu podle velikosti produktu.') + body[_t:]
    body, _n = re.subn(r'\s*<section class="canvas">\s*<div class="wrap">\s*<p class="eyebrow sig">Podmínky</p>.*?</section>', '', body, flags=re.S)
    assert _n == 3, _n
    # externí odkazy do nového tabu
    body = re.sub(r'<a ((?:(?!target=)[^>])*?)href="(https?://[^"]+)"((?:(?!target=)[^>])*)>', r'<a \1href="\2"\3 target="_blank" rel="noopener">', body)
    out = head_part + body
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R11 + out[i:] + GEN_TW_JS
