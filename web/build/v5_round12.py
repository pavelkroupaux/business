# Round 12 (5. 10. 2026): mobilní popisky kresby na řádky, víc místa pod kresbou, DP přepisované slovo na
# vlastním řádku, diagram na mobilu zpět na šířku se scrollem, ikony v kartách "Co dostanete",
# cena jako přehledná nabídka (podle vzoru studií se sprinty, auditů a fractional rolí),
# pořadí služeb: Decision Prototype, Audit, Vedení produktu.

GI = 'viewBox="0 0 64 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
IC_CHECKLIST = (f'<svg {GI}><path d="M8 10 l4 4 l7 -8"/><path d="M28 10 H56"/><path d="M9 22 l9 9 M18 22 l-9 9"/><path d="M28 26 H50"/>'
                '<path d="M8 38 l4 4 l7 -8"/><path d="M28 39 H54"/></svg>')
IC_WWW = (f'<svg {GI}><rect x="6" y="5" width="46" height="31" rx="4"/><path d="M22 44 H36 M29 36 V44"/>'
          '<text x="29" y="25" text-anchor="middle" font-family="var(--display)" font-size="10" font-weight="700" fill="currentColor" stroke="none">www</text>'
          '<path d="M44 26 L44 41 L48 37 L51 43 L54 41.5 L51 35.5 L56 35.5 Z" fill="var(--raise)" stroke-width="2"/></svg>')
IC_CODE = f'<svg {GI}><path d="M20 12 L8 24 L20 36"/><path d="M44 12 L56 24 L44 36"/><path d="M36 8 L28 40"/></svg>'
IC_PLAY = (f'<svg {GI}><rect x="6" y="5" width="52" height="34" rx="4"/><path d="M27 15 L39 22 L27 29 Z" fill="currentColor"/>'
           '<path d="M12 44 H52"/><path d="M12 44 H30" stroke-width="3.4"/></svg>')
IC_LIST = (f'<svg {GI}><g font-family="var(--display)" font-size="11" font-weight="700" fill="currentColor" stroke="none">'
           '<text x="10" y="14" text-anchor="middle">1</text><text x="10" y="28" text-anchor="middle">2</text><text x="10" y="42" text-anchor="middle">3</text></g>'
           '<path d="M22 10 H56"/><path d="M22 24 H48"/><path d="M22 38 H40"/></svg>')
IC_COMPASS = (f'<svg {GI}><circle cx="32" cy="24" r="19"/><path d="M32 10 L36 24 H28 Z" fill="currentColor"/>'
              '<path d="M32 38 L36 24 H28 Z"/></svg>')
GET_ICONS = {'Rozhodnutý rozsah': IC_CHECKLIST, 'Jeden odkaz pro všechny': IC_WWW, 'Podklad, podle kterého staví vývoj': IC_CODE,
             'Nahrávka obrazovky': IC_PLAY, 'Seznam podle priority': IC_LIST, 'Doporučení': IC_CHECKLIST,
             'Jasný směr každý týden': IC_COMPASS, 'Rozsah dřív, než se staví': IC_CHECKLIST, 'Prototyp místo dokumentu': IC_WWW}

def _ok(items): return '<ul class="ilist">' + ''.join(f'<li>{CHECK}<span>{t}</span></li>' for t in items) + '</ul>'
def _dot(items): return '<ul class="op-dots">' + ''.join(f'<li>{t}</li>' for t in items) + '</ul>'
CTA_BTN = '<a class="btn btn-fill" href="#/contact">Domluvit 30minutový hovor</a>'
def offer(price, term, incl, factors, note, incl_h='V ceně'):
    price_col = (f'<div class="op-price"><span class="op-label">Cena</span><b class="op-amount">{price}</b><span class="op-term">{term}</span>{CTA_BTN}</div>') if price else ''
    return (f'<div class="offer{" no-price" if not price else ""}">{price_col}'
            f'<div class="op-col"><p class="op-h">{incl_h}</p>{_ok(incl)}</div>'
            f'<div class="op-col"><p class="op-h">Cenu ovlivní</p>{_dot(factors)}<p class="op-note">{note}</p></div></div>')

TIERS = '''<div class="tiers">
  <div class="tier"><span class="tier-d">Jeden den</span><b class="tier-p">od 49 000 Kč</b><p><b>Jedna otázka.</b> Workshop a první verze, na kterou se dá kliknout.</p></div>
  <div class="tier"><span class="tier-d">Dva dny</span><b class="tier-p">od 125 000 Kč</b><p><b>Jedna nerozhodnutá věc.</b> Workshop, prototyp a zápis. Dotažené do konce.</p></div>
  <div class="tier"><span class="tier-d">Týden</span><b class="tier-p">od 220 000 Kč</b><p><b>Celá oblast produktu.</b> Víc rozhovorů, workshopů a obrazovek. Postup je stejný.</p></div>
</div>'''
DP_PRICE = ('<section class="ruled price-sec">\n    <div class="wrap">\n      <p class="eyebrow sig">Délka a cena</p>\n      <h2>Jeden den, dva, nebo týden.</h2>\n      '
            + TIERS + offer(None, None,
                ['Problém, lidé a cíl sepsané předem', 'Workshop s lidmi, kteří rozhodují', 'Funkční prototyp na webu, s heslem a komentáři', 'Zápis: co jsme rozhodli a proč'],
                ['Rozsah', 'Složitost', 'Velikost produktu'],
                'Platíte za projekt, ne za hodiny. Konečnou nabídku pošlu po první schůzce.', 'V každé délce') +
            f'\n      <div class="row" style="margin-top:34px">{CTA_BTN}</div>\n    </div>\n  </section>')
AU_OFFER = offer('od 29 000 Kč', 'Pět pracovních dní · bez schůzek',
                 ['Nahrávka obrazovky s komentářem', 'Co nefunguje, v pořadí, v jakém bych to opravoval', 'Doporučení: já, nový člověk, nebo nikdo', 'Půlhodinový hovor nad výsledkem, když chcete'],
                 ['Velikost produktu', 'Počet průchodů, které projdu'], 'Konečnou nabídku pošlu, až uvidím produkt.')
FR_OFFER = offer('od 120 000 Kč měsíčně', 'Dva dny v týdnu · nejméně tři měsíce',
                 ['Sedím u porad vedení i produktu', 'Rozsah dohodnutý dřív, než začne vývoj', 'Schvalujete prototyp, ne dokument', 'Písemné předání, až přijmete někoho natrvalo'],
                 ['Rozsah', 'Velikost týmu'], 'Konečnou nabídku pošlu po první schůzce.')

CSS_R12 = '''
/* ---------- v5 kolo 12 ---------- */
.hero2 .hx-fig{margin-bottom:clamp(40px,6vw,96px)}
@media(max-width:700px){.hero2 .hx-fig{margin-bottom:24px}}
/* diagram na mobilu: na šířku, posouvá se */
@media(max-width:700px){.diagram svg{display:block!important;min-width:680px}.flow-m{display:none!important}
  .diagram{overflow-x:auto;padding:20px;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}}
/* karty "Co dostanete" s ikonou, na užší šířce pod sebou */
.get-ic{width:58px;height:44px;color:var(--muted);margin-bottom:6px}
.get-ic svg{width:100%;height:100%;display:block}
@media(max-width:900px){.cards.get-cards{grid-template-columns:1fr}}
/* ceny */
.stp-price{color:#1d1d1f}
.tiers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:44px;text-align:left}
.tier{background:var(--raise);border-radius:24px;padding:26px 26px 28px;box-shadow:var(--glass-shadow);display:flex;flex-direction:column;gap:8px}
.tier-d{font-family:var(--display);font-size:15px;font-weight:600;color:var(--muted)}
.tier-p{font-family:var(--display);font-size:clamp(26px,2.6vw,32px);font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.tier p{margin:6px 0 0;font-size:15.5px;line-height:1.5;color:var(--muted);max-width:none}
.tier p b{color:var(--ink);font-weight:600}
.offer{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1.2fr) minmax(0,.9fr);gap:0;margin-top:22px;text-align:left;
  background:var(--raise);border-radius:24px;box-shadow:var(--glass-shadow);overflow:hidden}
.offer.no-price{grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)}
.op-price,.op-col{padding:28px 28px 30px}
.op-col+.op-col,.op-price+.op-col{border-left:1px solid var(--line)}
.op-price{display:flex;flex-direction:column;gap:6px;align-items:flex-start;background:var(--surface)}
.op-label,.op-h{font-family:var(--display);font-size:13px;font-weight:600;color:var(--faint);margin:0 0 6px}
.op-h{margin-bottom:14px}
.op-amount{font-family:var(--display);font-size:clamp(28px,2.8vw,36px);font-weight:700;letter-spacing:-.03em;color:var(--ink);line-height:1.1}
.op-term{font-size:15px;color:var(--muted);margin-bottom:18px}
.op-dots{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.op-dots li{font-family:var(--display);font-size:13.5px;font-weight:550;color:var(--muted);background:var(--surface);border-radius:980px;padding:7px 13px}
.op-note{font-size:14.5px;line-height:1.5;color:var(--muted);margin:16px 0 0;max-width:none}
.offer .ilist li{font-size:15px}
@media(max-width:900px){.tiers{grid-template-columns:1fr}.offer,.offer.no-price{grid-template-columns:1fr}
  .op-col+.op-col,.op-price+.op-col{border-left:0;border-top:1px solid var(--line)}}
/* kroky auditu a části úvazku vedle sebe */
#v-svc-audit .stp-list,#v-svc-fractional .stp-list{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:40px}
#v-svc-audit .stp-row,#v-svc-fractional .stp-row{display:flex;flex-direction:column;gap:6px;border:0;padding:24px 24px 26px;background:var(--raise);border-radius:24px;box-shadow:var(--glass-shadow);text-align:left}
@media(max-width:900px){#v-svc-audit .stp-list,#v-svc-fractional .stp-list{grid-template-columns:1fr}}
'''

def _view(out, vid):
    a = out.index(f'<div id="{vid}"'); b = out.index('<div id="', a + 10)
    return a, b

def post_patch12(out):
    # mobilní popisky kresby na řádky
    out = rep(out, '<div class="hx-labs-m" aria-hidden="true"><span>tým se cyklí ve schůzkách</span><span>rozhodnuto, dohodnuto, zapsáno</span></div>',
              '<div class="hx-labs-m" aria-hidden="true"><span>tým se cyklí<br>ve schůzkách</span><span>rozhodnuto,<br>dohodnuto,<br>zapsáno</span></div>')
    # DP: přepisované slovo na novém řádku, mobilní svislý diagram pryč
    out = rep(out, '<h2>Každé kolo začíná <span class="tw">', '<h2>Každé kolo začíná<br><span class="tw">')
    out = re.sub(r'<div class="flow-m".*?</div>\s*</div>(?=</figure>)', '', out, count=1, flags=re.S)
    assert 'class="flow-m"' not in out
    # ikony v kartách "Co dostanete"
    for t, ic in GET_ICONS.items():
        out = out.replace(f'<div class="card"><h3 class="card-title">{t}</h3>', f'<div class="card get-card"><div class="get-ic">{ic}</div><h3 class="card-title">{t}</h3>')
    out = out.replace('<div class="cards"><div class="card get-card">', '<div class="cards get-cards"><div class="card get-card">')
    # DP: cena jako nabídka
    a, b = _view(out, 'v-svc-dp'); v = out[a:b]
    v = re.sub(r'<section class="ruled">\s*<div class="wrap">\s*<p class="eyebrow sig">Jak to probíhá</p>.*?</section>', lambda m: DP_PRICE, v, count=1, flags=re.S)
    assert 'Délka a cena' in v
    out = out[:a] + v + out[b:]
    # Audit a část úvazku: kroky vedle sebe a pod nimi nabídka
    for vid, off in (('v-svc-audit', AU_OFFER), ('v-svc-fractional', FR_OFFER)):
        a, b = _view(out, vid); v = out[a:b]
        v = re.sub(r'<div class="stp-row stp-price-row">.*?</div></div>', '', v, count=1, flags=re.S)
        i = v.index('</div>\n    </div>\n  </section>', v.index('<div class="stp-list">')) + len('</div>')
        v = v[:i] + off + v[i:]
        out = out[:a] + v + out[b:]
    # pořadí služeb: Decision Prototype, Audit, Vedení produktu
    a, b = _view(out, 'v-services'); v = out[a:b]
    rows = {m.group(1): m.group(0) for m in re.finditer(r'<article class="svc-row" id="(svc-[a-z]+)">.*?</article>', v, re.S)}
    assert set(rows) == {'svc-dp', 'svc-fractional', 'svc-audit'}
    s0 = v.index(rows['svc-dp']); s1 = v.index(rows['svc-audit']) + len(rows['svc-audit'])
    v = v[:s0] + rows['svc-dp'] + '\n' + rows['svc-audit'] + '\n' + rows['svc-fractional'] + v[s1:]
    out = out[:a] + v + out[b:]
    a, b = _view(out, 'v-home'); v = out[a:b]
    cards = {m.group(1): m.group(0) for m in re.finditer(r'<a class="svc[^"]*" href="#/services/([a-z-]+)">.*?</a>', v, re.S)}
    if set(cards) >= {'decision-prototype', 'fractional', 'audit'}:
        s0 = v.index(cards['decision-prototype']); s1 = v.index(cards['audit']) + len(cards['audit'])
        v = v[:s0] + cards['decision-prototype'] + cards['audit'] + cards['fractional'] + v[s1:]
        out = out[:a] + v + out[b:]
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R12 + out[i:]
