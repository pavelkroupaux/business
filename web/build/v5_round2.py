# Round 2 of v5 feedback (3. 10. 2026). Exec'd from build_v5b.py before MAIN is assembled.
ICO = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
CHECK = f'<svg class="ic" {ICO}><path d="M20 6 9 17l-5-5"/></svg>'
XMARK = f'<svg class="ic" {ICO}><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>'
I_TARGET = f'<svg {ICO}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/></svg>'
I_PEN = f'<svg {ICO}><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>'
I_CLICK = f'<svg {ICO}><path d="m9 9 5 12 1.8-5.2L21 14Z"/><path d="M7.2 2.2 8 5.1"/><path d="M5.1 8 2.2 7.2"/><path d="M14 4.1 12 6"/><path d="m6 12-1.9 2"/></svg>'
I_DOC = f'<svg {ICO}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/></svg>'

# ---------- 1. Kde jsem pracoval: Energetika místo Telekomunikací, jména klientů pod obory
BOLT = ('<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3.9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M27.5 5.5 L11.5 27 L23.5 27 L20.5 42.5 L36.5 20.5 L24.5 20.5 Z"/></svg>')
i = h.index('<span>Telekomunikace</span>'); a = h.rfind('<li>', 0, i)
h = h[:a] + '<li>' + BOLT + '<span>Energetika</span></li>' + h[i + len('<span>Telekomunikace</span></li>'):]
CLIENTS = ['Komerční banka', 'Česká spořitelna', 'Modrá pyramida', 'Centropol', 'WPP', 'ESET', 'SatoshiLabs', 'Jablotron', 'Coinmate', 'Leeaf']
k = h.index('</ul>', h.index('<ul class="sectors">')) + len('</ul>')
h = h[:k] + '\n      <ul class="client-names" aria-label="Klienti">' + ''.join(f'<li>{c}</li>' for c in CLIENTS) + '</ul>' + h[k:]

# ---------- 3. Fotka workshopu: nadpis a popisek
SHOT_OPEN = '<section class="canvas" style="padding-block:clamp(56px,7vw,92px)"><div class="wrap">'
h = rep(h, SHOT_OPEN, '<section class="canvas shot-sec"><div class="wrap">'
        '<p class="eyebrow sig">Workshop v akci</p><h2>Jak vypadá workshop se mnou.</h2>')
k = h.index('</figure>', h.index('shot-sec"')) + len('</figure>')
h = h[:k] + '<p class="shot-cap">Místnost po workshopu. Varianty, lepítka a otevřené otázky na stěnách.</p>' + h[k:]

# ---------- 4. Proces: statické kroky místo scrollytellingu
PROC = [('Předem', I_TARGET, 'Definice problému, týmu a cíle', 'Před spoluprací si s vámi ujasním, jaký problém řešíme, kdo o něm rozhoduje a čeho chceme dosáhnout.'),
        ('Na první schůzce', I_PEN, 'Varianty kreslené během schůzky', 'Varianty řešíme už na první schůzce. Místo názorů pak vybíráte ze dvou nakreslených možností.'),
        ('Druhý den', I_CLICK, 'Jeden směr jako prototyp', 'Funkční ukázka se skutečnými texty, i pro chvíle, kdy se něco pokazí. Co zůstane otevřené, má jméno a termín.'),
        ('Potom', I_DOC, 'Funkční zadání, podle kterého staví vývoj', 'Každé rozhodnutí a jeho důvod. Jinak se za šest týdnů hádáte znovu.')]
steps = ''.join(f'<li class="pstep"><div class="pstep-top"><span class="pstep-ic">{ic}</span><span class="pstep-when">{w}</span></div><h3>{t}</h3><p>{p}</p></li>' for w, ic, t, p in PROC)
a = h.index('<section class="ruled">', h.index('Od první schůzky k první verzi') - 200)
b = h.index('</section>', h.index('data-scrolly')) + len('</section>')
assert 'Od první schůzky' in h[a:b]
h = h[:a] + f'''<section class="canvas proc">
    <div class="wrap">
      <p class="eyebrow sig">Od první schůzky k první verzi</p>
      <h2>V pondělí zmatek. Ve středu <span class="fix">rozhodnuto a nakresleno</span>.</h2>
      <p class="lede">První workshop a ještě ten týden první verze, na kterou se dá kliknout.</p>
      <ol class="proc-steps">{steps}</ol>
    </div>
  </section>''' + h[b:]

# ---------- 5. Tmavá sekce: systémové myšlení
h = rep(h, '<p class="eyebrow">S čím se nepočítá</p>\n      <h2>Pracuju napříč týmy i obory.</h2>\n      <p class="lede" style="color:var(--on-panel-soft)">Banky, zdravotnictví, krypto. Vývoj, byznys, vedení i compliance. Znám kontext každé strany, a tým se proto posune rychleji.</p>',
        '<p class="eyebrow">Moje výhoda</p>\n      <h2>Myslím v systémech.</h2>\n      <p class="lede" style="color:var(--on-panel-soft)">Pracuju napříč obory i týmy. Banky, zdravotnictví, krypto. Vývoj, byznys, vedení i compliance. Rychle uvidím, jak spolu věci souvisí, a tým se díky tomu pohne hned.</p>')

# ---------- 6. Služby na úvodu: bez věty o rozpočtu
h = rep(h, '<p class="eyebrow sig">Co si můžete objednat</p>', '<p class="eyebrow sig">Moje služby</p>')
h = rep(h, '\n      <p class="lede">Když je rozpočet pevný, zmenším rozsah. Sazba zůstává.</p>\n      <div class="svc-cards svc-three">', '\n      <div class="svc-cards svc-three">')

# ---------- Portfolio
WORK = rep(WORK, '<p class="eyebrow sig">Práce</p>', '<p class="eyebrow sig">Portfolio</p>')
WORK = rep(WORK, '<section id="refs">', '<section id="refs" class="canvas">')
_ra = WORK.index('<div class="refs">'); _rb = WORK.index('</details></div>', _ra) + len('</details></div>')
_items = re.findall(r'<details class="ref">.*?</details>', WORK[_ra:_rb], re.S)
assert len(_items) == 11
_items = [it.replace('<details class="ref">', f'<details class="ref" style="order:{n}">', 1) for n, it in enumerate(_items)]
WORK = WORK[:_ra] + '<div class="refs"><div class="refs-col">' + ''.join(_items[0::2]) + '</div><div class="refs-col">' + ''.join(_items[1::2]) + '</div></div>' + WORK[_rb:]

# ---------- Služby: odrážky jako jeden blok, Energetika
SERV = rep(SERV, '<li>Telekomunikace</li>', '<li>Energetika</li>')
def _wrap_li(m):
    return re.sub(r'<li>(.*?)</li>', r'<li><span>\1</span></li>', m.group(0))
SERV = re.sub(r'<ul class="svc-list[^"]*">.*?</ul>', _wrap_li, SERV, flags=re.S)

# ---------- Služby: přehlednější hlavička
SERV = rep(SERV, '<h1><span class="fix">Tři způsoby</span>, jak spolupracovat.</h1>\n      <p class="lede">Když je rozpočet pevný, zmenším rozsah. Sazba zůstává.</p>',
           '<h1><span class="fix">Tři způsoby</span>, jak spolupracovat.</h1>\n      <p class="lede">Vyberte podle toho, kde jste se zasekli.</p>')
PICKS = [('svc-dp', 'Ještě nevíte, co postavit', 'Decision Prototype', 'od 49 000 Kč', 'Jeden den, dva, nebo týden'),
         ('svc-audit', 'Víte co, ale nestaví se to', 'Audit rozhodnutí', 'od 29 000 Kč', 'Pět pracovních dní, bez schůzek'),
         ('svc-fractional', 'Nikdo nedrží směr', 'Vedení produktu na část úvazku', 'od 120 000 Kč měsíčně', 'Dva dny v týdnu, nejméně tři měsíce')]
pick_html = '<div class="picks">' + ''.join(
    f'<a class="pick" href="#{i}" data-jump><span class="pick-q">{q}</span><b class="pick-t">{t}</b><span class="pick-p">{p_}</span><span class="pick-f">{f}</span><span class="pick-go">Podrobnosti</span></a>'
    for i, q, t, p_, f in PICKS) + '</div>'
chips = '<ul class="svc-chips"><li>Cena za projekt, nikdy za hodinu</li><li>Od jednoho dne po tři měsíce</li><li>Jen za honorář, ne za podíl</li><li>Nejsem plátce DPH</li></ul>'
_a = SERV.index('<div class="svc-facts">'); _b = SERV.index('</div>', SERV.index('<div class="row svc-cta">')) + len('</div>')
SERV = (SERV[:_a] + pick_html + '\n      ' + chips +
        '\n      <div class="row svc-cta"><a class="btn btn-fill" href="#/contact">Domluvit 30minutový hovor</a></div>'
        '\n      <p class="svc-micro">Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online.</p>' + SERV[_b:])

# ---------- O mně
def lst(items, icon):
    return '<ul class="ilist">' + ''.join(f'<li>{icon}<span>{t}</span></li>' for t in items) + '</ul>'
HOW = ['Vedu diskusi a zároveň kreslím.', 'Na jednom sezení udržím celek i detail.', 'Mezi sezeními píšu. Radši pošlu návrh než pozvánku na schůzku.',
       'Vizuál řídím, pixely kreslí designér.', 'Každé velké rozhodnutí zapíšu i s důvodem. Jinak se k němu vracíme.']
WITH = ['S lidmi, kterým jde o výsledek víc než o to mít pravdu.', 'S týmy, kde chyba něco stojí. Regulátor, licence, zdraví, něčí úspory.', 'Se zakladateli, kteří přijdou osobně.']
NOT = ['Tam, kde se problémy vyrábějí, aby měl někdo co řešit.', 'Tam, kde se počítá jen výkon a na lidech nezáleží.']
NOTME = ['Nejsem produktový manažer přes metriky. Uzavírám rozhodnutí.', 'Nejsem agentura.', 'Nejsem ruce do Figmy.']
ph = lambda t: f'<figure class="print ph"><span>{t}</span></figure>'
_rA = roomA.replace(' id="roomA"', ''); _rB = roomB.replace(' id="roomB"', '')
PRINTS = (f'<figure class="print">{_rA}</figure>'
          f'<figure class="print">{_rB}</figure>'
          + ph('[FOTKA: prototyp na obrazovce]') + ph('[FOTKA: workshop s týmem]'))
PRINTS2 = PRINTS + PRINTS
hid = lambda x: x.replace('<figure class="print', '<figure aria-hidden="true" class="print')
NOTES_HID = notes.replace('class="note mq-note"', 'class="note mq-note" aria-hidden="true"')
ABOUT = f'''<div id="v-about" hidden>
  <section class="canvas about-top">
    <div class="wrap about-hero">
      <div>
        <p class="eyebrow sig">O mně</p>
        <h1><span class="fix">Třináct let</span> dovádím týmy k <span class="fix">rozhodnutí</span>.</h1>
        <p class="lede">Praha a Amsterdam. Přicházím tam, kde se o produktu ještě nerozhodlo, nebo kde se tým cyklí a potřebuje se pohnout dál.</p>
      </div>
      <figure class="paper polaroid">
        <div class="polaroid-img">{portrait}</div>
        <figcaption class="polaroid-cap">Pavel<small>Definice produktu</small></figcaption>
      </figure>
    </div>
    <div class="wrap">
      <div class="acards">
        <div class="acard"><p class="acard-h">Jak pracuju</p>{lst(HOW, CHECK)}</div>
        <div class="acard"><p class="acard-h">S kým mi to jde</p>{lst(WITH, CHECK)}</div>
        <div class="acard no"><p class="acard-h">A s kým ne</p>{lst(NOT, XMARK)}</div>
      </div>
    </div>
  </section>
  <section class="panel">
    <div class="wrap">
      <p class="eyebrow">Ať to víte hned</p>
      <h2>Co nejsem</h2>
      <div class="notme">{lst(NOTME, XMARK)}</div>
      <p class="wide" style="margin-top:30px">Jak vedu týmy, potvrdí Lukáš Rykr, můj přímý podřízený. <a class="gold" href="#/portfolio">Reference</a></p>
    </div>
  </section>
  <section class="ruled">
    <div class="wrap">
      <p class="eyebrow sig">Kde jsem pracoval</p>
      <div class="track">
        <div class="trow"><span class="yr">2023&ndash;2026</span><span class="w"><b>Vedoucí produktového designu, Coinmate</b>Regulovaná kryptoburza. Externě, dva dny v týdnu. Design systém od nuly, specifikace frontendu, podklady pro licenci MiCA a nová značka.</span></div>
        <div class="trow"><span class="yr">2023&ndash;dosud</span><span class="w"><b>Zakládající designér a spoluzakladatel, Heirloom</b>Digitální dědictví, nový produkt od nuly. Produktové řízení, které tým neměl, a cesta od prototypu po nasazení.</span></div>
        <div class="trow"><span class="yr">2020&ndash;2023</span><span class="w"><b>Zakládající designér a vedoucí designu, Leeaf</b>Léčba neplodnosti. iOS, Android a portál pro lékaře. Potom systém, na kterém běžely další kliniky. Dva designéři v týmu.</span></div>
        <div class="trow"><span class="yr">2018&ndash;dosud</span><span class="w"><b>Na volné noze</b>Sprinty a výzkum pro Komerční banku, Českou spořitelnu, CEMEX a ESET. Workshop pro BRENO přes WPP. Audity pro ESET, Jablotron a Centropol.</span></div>
        <div class="trow"><span class="yr">2014&ndash;2018</span><span class="w"><b>Předtím</b>UX designér v Monsteru a Usertechu.</span></div>
      </div>
      <p style="margin-top:22px"><a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Celá kariéra na LinkedInu</a></p>
    </div>
  </section>
  <section class="canvas board-sec">
    <div class="wrap">
      <p class="eyebrow sig">Z práce</p>
      <h2>Workshopy, tabule, prototypy.</h2>
    </div>
    <div class="marquee gal" aria-label="Fotky z práce"><div class="mq-track gal-track">{PRINTS}</div></div>
    <div class="wrap" style="margin-top:72px">
      <p class="eyebrow sig">Reference</p>
      <h2>Co říkají lidé, se kterými jsem pracoval.</h2>
    </div>
    <div class="marquee refq" aria-label="Reference"><div class="mq-track">{notes}{NOTES_HID}</div></div>
    <div class="wrap"><div class="row" style="margin-top:28px"><a class="btn btn-line" href="#/portfolio">Všechny reference</a></div></div>
  </section>
{cta('Něco ve vašem produktu není rozhodnuté? Promluvme si.', 'Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online.')}</div>
'''

CSS_R2 = '''
/* ---------- v5 kolo 2 ---------- */
:root{interpolate-size:allow-keywords}
/* klienti */
.client-names{list-style:none;padding:0;margin:40px auto 0;max-width:900px;display:flex;flex-wrap:wrap;justify-content:center;gap:12px 30px}
.client-names li{font-family:var(--display);font-size:16px;font-weight:650;letter-spacing:-.015em;color:var(--faint)}
/* lístky */
.note{justify-content:center;align-items:center;text-align:center}
.note p{line-height:1.55;font-size:20px}
/* fotka workshopu */
.shot-sec{text-align:center;padding-block:clamp(64px,8vw,104px)}
.shot-sec h2{margin-bottom:44px}
.shot-cap{font-family:var(--hand);font-size:18px;color:var(--muted);margin:26px auto 0;max-width:46ch;text-align:center}
/* proces */
.proc{text-align:center}
.proc-steps{list-style:none;padding:0;margin:56px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;position:relative;text-align:left}
.proc-steps::before{content:"";position:absolute;left:10%;right:10%;top:51px;border-top:2px dashed var(--faint);opacity:.45}
.pstep{position:relative;background:var(--raise);border-radius:24px;padding:26px 24px 28px;box-shadow:var(--glass-shadow);display:flex;flex-direction:column;gap:10px}
.pstep-top{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.pstep-ic{width:50px;height:50px;border-radius:50%;background:var(--fix);color:#1d1d1f;display:grid;place-items:center;flex:none}
.pstep-ic svg{width:24px;height:24px}
.pstep-when{font-family:var(--hand);font-size:19px;font-weight:600;color:var(--muted)}
.pstep h3{margin:0;font-size:19px;line-height:1.25;letter-spacing:-.02em}
.pstep p{margin:0;font-size:15.5px;line-height:1.55;color:var(--muted)}
@media(max-width:980px){.proc-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.proc-steps::before{display:none}}
@media(max-width:560px){.proc-steps{grid-template-columns:1fr}}
/* reference v portfoliu: karty, které se rozbalí celé */
.refs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;align-items:start;max-width:none;margin-top:48px}
.refs-col{display:grid;gap:22px;align-content:start}
.refs .ref{background:var(--raise);border-radius:24px;box-shadow:var(--glass-shadow);overflow:hidden;
  transition:box-shadow .3s ease,transform .3s cubic-bezier(.2,.7,.3,1)}
.refs .ref:hover{transform:translateY(-2px)}
.refs .ref summary{background:transparent!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important;
  display:flex;flex-direction:column;gap:20px;padding:28px 72px 26px 28px;border-radius:0}
.refs .ref summary:hover{background:transparent!important}
.refs .ref summary .ref-claim::after{content:none}
.refs .ref summary::after{content:"+";position:absolute;top:24px;right:24px;width:34px;height:34px;border-radius:50%;
  display:grid;place-items:center;background:var(--surface);color:var(--ink);font-family:var(--display);font-size:20px;font-weight:500;line-height:1;
  transition:transform .35s cubic-bezier(.2,.7,.3,1),background .2s}
.refs .ref[open] summary::after{transform:rotate(45deg);background:var(--fix);color:#1d1d1f}
.refs .ref-claim{font-size:20px}
.refs .ref-full{background:transparent!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important;
  margin:0;padding:0 28px 28px;border-radius:0}
.refs .ref-full p{font-size:16px;line-height:1.6;color:var(--muted)}
.refs .ref-full::before{content:"";display:block;border-top:1px solid var(--line);margin-bottom:20px}
.refs .ref::details-content{block-size:0;overflow:hidden;transition:block-size .4s cubic-bezier(.2,.7,.3,1),content-visibility .4s allow-discrete}
.refs .ref[open]::details-content{block-size:auto}
@media(max-width:760px){.refs{grid-template-columns:1fr;gap:16px}.refs-col{display:contents}.refs .ref summary{padding:24px 64px 22px 22px}.refs .ref-full{padding:0 22px 24px}}
/* případy 2x2, odkaz na srovnání na střed */
.case-cards{grid-template-columns:repeat(2,minmax(0,1fr))}
@media(max-width:700px){.case-cards{grid-template-columns:1fr}}
#offers .svc-all-link{text-align:center}
/* hlavička na mobilu v jednom řádku */
@media(max-width:480px){.top-in{flex-wrap:nowrap;gap:14px}.top .mark{margin-right:auto;white-space:nowrap}.top a.lnk[data-nav="/"]{display:none}.top a.lnk{white-space:nowrap}}
/* služby: hlavička s výběrem */
.svc-hero{text-align:center}
.picks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:48px;text-align:left}
.pick{display:flex;flex-direction:column;gap:8px;background:var(--raise);border-radius:24px;padding:26px 26px 24px;box-shadow:var(--glass-shadow);
  text-decoration:none;color:inherit;transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.pick:hover{transform:translateY(-3px)}
.pick-q{font-family:var(--hand);font-size:18px;color:var(--muted)}
.pick-t{font-family:var(--display);font-size:21px;font-weight:700;letter-spacing:-.02em;line-height:1.2;color:var(--ink)}
.pick-p{font-family:var(--display);font-size:16px;font-weight:650;color:var(--ink)}
.pick-f{font-size:14.5px;color:var(--muted)}
.pick-go{margin-top:auto;padding-top:14px;font-family:var(--display);font-size:14px;font-weight:600;color:var(--ink)}
.pick-go::after{content:" \\2193"}
.svc-chips{list-style:none;padding:0;margin:28px auto 0;display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.svc-chips li{font-family:var(--display);font-size:13.5px;font-weight:550;color:var(--muted);background:var(--surface);border-radius:980px;padding:8px 14px}
.svc-hero .svc-cta{justify-content:center;margin-top:36px}
.svc-micro{font-family:var(--display);font-size:13.5px;color:var(--faint);margin:12px auto 0;text-align:center}
.svc-confirms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:44px}
.svc-confirms .cf{background:var(--raise);box-shadow:var(--glass-shadow);border-radius:24px;padding:26px 28px;display:flex;flex-direction:column;gap:16px;text-align:left}
.svc-confirms .cf .claim{font-family:var(--display);font-size:18px;line-height:1.4;letter-spacing:-.015em;color:var(--ink)}
.faq{margin-left:auto;margin-right:auto;text-align:left}
@media(max-width:900px){.picks{grid-template-columns:1fr}.svc-confirms{grid-template-columns:1fr}}
/* služby */
.svc-row .svc-more,a.lnk.svc-more{color:var(--ink);font-family:var(--display);font-weight:600;font-size:15px}
.svc-more::after{content:" \\2192"}
.svc-hero{padding-bottom:clamp(36px,4vw,56px)}
.svc-all{padding-top:clamp(28px,3vw,44px)}
.svc-list li>span{min-width:0}
/* o mně */
.about-top{padding-bottom:clamp(72px,9vw,120px)}
.polaroid-cap small{display:block;font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.02em;color:var(--paper-soft);margin-top:4px}
.acards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:clamp(56px,7vw,88px)}
.acard{background:var(--raise);border-radius:24px;padding:28px 26px 30px;box-shadow:var(--glass-shadow)}
.acard-h{font-family:var(--display);font-size:19px;font-weight:700;letter-spacing:-.02em;color:var(--ink);margin:0 0 18px}
.ilist{list-style:none;padding:0;margin:0;display:grid;gap:14px}
.ilist li{display:grid;grid-template-columns:26px 1fr;gap:12px;align-items:start;font-size:16px;line-height:1.5;color:var(--ink)}
.ilist .ic{width:26px;height:26px;padding:5px;box-sizing:border-box;border-radius:50%;background:var(--fix);color:#1d1d1f;stroke-width:3}
.acard.no .ilist .ic,.notme .ilist .ic{background:var(--surface);color:var(--muted)}
.notme{margin:24px auto 0;width:fit-content;max-width:100%;text-align:left}
.notme .ilist li{color:var(--on-panel);font-size:18px}
.panel .notme .ilist .ic{background:rgba(255,255,255,.12);color:var(--on-panel)}
@media(max-width:900px){.acards{grid-template-columns:1fr}}
@media(max-width:860px){.about-hero .polaroid{justify-self:center;margin:8px auto 0}}
/* nástěnka: fotky a reference */
.marquee{overflow:hidden;padding:44px 0 64px;margin-top:8px;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 6%,#000 94%,transparent 100%);mask-image:linear-gradient(90deg,transparent 0,#000 6%,#000 94%,transparent 100%)}
.mq-track{gap:34px;padding-left:34px}
.gal-track{animation-duration:120s}
.print{flex:0 0 auto;width:360px;margin:0;padding:10px 10px 12px;background:var(--paper);border-radius:3px;position:relative;line-height:0;
  box-shadow:0 1px 2px rgba(17,17,17,.10),0 20px 30px -16px rgba(17,17,17,.40)}
.print:nth-child(odd){transform:rotate(-1.4deg)}
.print:nth-child(even){transform:rotate(1.2deg) translateY(10px)}
.print::before{content:"";position:absolute;top:-13px;left:50%;margin-left:-38px;width:76px;height:24px;
  background:rgba(255,206,27,.55);border-left:1px solid rgba(17,17,17,.10);border-right:1px solid rgba(17,17,17,.10);transform:rotate(-2.6deg)}
.print img{display:block;width:100%;height:240px;object-fit:cover;border-radius:1px}
.print.ph{height:262px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;line-height:1.4}
.print.ph span{display:flex;align-items:center;justify-content:center;width:100%;height:100%;padding:20px;box-sizing:border-box;text-align:center;
  font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.06em;color:var(--paper-soft);
  background:repeating-linear-gradient(135deg,var(--paper-hatch) 0 9px,var(--paper) 9px 18px)}
.board-sec{text-align:center}
@media(max-width:560px){.print{width:270px}.print img{height:180px}.print.ph{height:202px}.marquee{padding:36px 0 52px}}
@media (prefers-reduced-motion:reduce){.marquee{overflow-x:auto}}
'''

def post_patch(out):
    out = rep(out, 'data-nav="/portfolio">Práce</a>', 'data-nav="/portfolio">Portfolio</a>')
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R2 + out[i:]
    LOOP = """<script>
(function(){document.querySelectorAll(".gal-track").forEach(function(t){
  var k=Array.prototype.slice.call(t.children);
  for(var r=0;r<3;r++) k.forEach(function(c){var n=c.cloneNode(true);n.setAttribute("aria-hidden","true");t.appendChild(n);});
});})();
</script>"""
    return out + LOOP
