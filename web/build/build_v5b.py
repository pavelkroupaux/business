import re
R = '/sessions/sweet-modest-heisenberg/mnt/'
V4 = R + 'Career/05 Web/verze/site-v4.html'
OUT = R + 'Career/05 Web/verze/site-v5.html'
PROD = R + 'outputs/v5src/project/Product-cs.dc.html'
s = open(V4).read()

def rep(t, a, b, n=1):
    c = t.count(a)
    assert c == n, (c, a[:80])
    return t.replace(a, b)

pre = s[:s.index('<main>') + len('<main>')]
mainb = s[s.index('<main>') + len('<main>'):s.index('</main>')]
post = s[s.index('</main>'):]

# ---------------------------------------------------------------- pieces from v4
home = mainb[mainb.index('<div id="v-home">'):mainb.index('<!-- ======================= WORK')]
refs = re.search(r'<div class="refs">.*?</div></details></div>', mainb, re.S).group(0)
def face(name):
    m = re.search(r'(<img class="ref-face" src="data:[^"]+" alt="" loading="lazy">)<span><b>' + re.escape(name) + '</b>', mainb)
    return m.group(1) if m else '<span class="ref-face ref-ini" aria-hidden="true">' + ''.join(w[0] for w in name.split()) + '</span>'
icons = re.findall(r'<div class="svc-row-head">\s*(<svg\b.*?</svg>)', mainb, re.S)  # sprint2, sprint5, fractional, audit
roomB = re.search(r'<img id="roomB"[^>]*>', mainb).group(0)
roomA = re.search(r'<img id="roomA"[^>]*>', mainb).group(0)
portrait = re.search(r'<div class="polaroid-img">(<img src="data:[^"]+"[^>]*>)</div>', mainb).group(1)
prod = open(PROD).read()
diagram = re.search(r'<svg viewBox="0 100 1240 460".*?</svg>', prod, re.S).group(0)

CTA_HREF = '#/contact'
def cta(h2='Napište mi, kde jste se zasekli. Když nebudu ten pravý, řeknu vám to.', lede='Třicet minut. Bez prezentace a bez složitých nabídek.'):
    return f'''  <section class="panel deep canvas">
    <div class="wrap">
      <p class="eyebrow">Další krok</p>
      <h2>{h2}</h2>
      <p class="lede" style="color:var(--on-panel-soft)">{lede}</p>
      <div class="row"><a class="btn btn-fill" href="{CTA_HREF}">Domluvit 30minutový hovor</a></div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- HOME
h = home
h = rep(h, 'Pavel Kroupa &middot; Product definition &middot; Amsterdam and Prague', 'Pavel Kroupa &middot; Definice produktu &middot; Praha a Amsterdam')
h = rep(h, '<h1>I take the part of the product nobody has decided.</h1>', '<h1>Pomáhám týmům <span class="fix">rozhodnout</span>, co postavit.</h1>')
h = rep(h, '<p class="lede">Code got cheap. Deciding what to build didn\'t. I make it concrete and get it agreed, in products where a mistake is expensive.</p>',
        '<div class="lede-wrap"><p class="lede">Kód zlevnil. Shodnout se na zadání ne. Sednu si s těmi, kdo rozhodují, a odejdeme s <b class="hl">hotovým zadáním</b>.</p>'
        '<p class="hand-note" aria-label="Poznámka"><span>s AI za dny, ne týdny</span><svg width="64" height="40" viewBox="0 0 64 40" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="transform:scaleX(-1)"><path d="M62 34 C 44 37, 20 30, 8 8"></path><path d="M6 17 L 8 7 L 17 10"></path></svg></p></div>')
h = rep(h, '<a class="btn btn-fill" href="mailto:info@pavelkroupa.com?subject=Call">Book a 30-minute call</a>\n        <a class="btn btn-line" href="#/portfolio">See the work</a>',
        f'<a class="btn btn-fill" href="{CTA_HREF}">Domluvit 30minutový hovor</a>\n        <a class="btn btn-line" href="#/portfolio">Ukázky práce</a>')
h = rep(h, '>a team going in circles<', '>tým se cyklí ve schůzkách<')
h = rep(h, '>decided, agreed, written down<', '>rozhodnuto, dohodnuto, zapsáno<')
# second check becomes a grey cross
i = h.index('M1627.0 246.0'); a = h.rfind('<path', 0, i); b = h.index('>', i) + 1
if h[b:b + 7] == '</path>': b += 7
cross = ('<path fill="none" stroke="var(--faint)" stroke-width="14" stroke-linecap="round" d="M1629 226C1636 233 1647 244 1653 250C1659 256 1664 262 1669 267"></path>'
         '<path fill="none" stroke="var(--faint)" stroke-width="14" stroke-linecap="round" d="M1668 225C1661 233 1652 242 1646 249C1640 255 1635 261 1630 267"></path>')
cross = cross.replace('<path fill', '<path class="hx-x" fill')
h = h[:a] + cross + h[b:]
h = rep(h, '>tým, který se točí v kruhu<', '>tým se cyklí ve schůzkách<')
h = rep(h, '>rozhodnuto, odsouhlaseno, sepsáno<', '>rozhodnuto, dohodnuto, zapsáno<')
BULB_SVG = ('<g class="hx-bulb" transform="translate(762 30) rotate(16) scale(2.4)" fill="none" stroke-linecap="round" stroke-linejoin="round">'
  '<g stroke="var(--fix)" stroke-width="1.6"><path d="M11 -7 L11 -4"/><path d="M0.5 -2.5 L2.6 -0.4"/><path d="M21.5 -2.5 L19.4 -0.4"/><path d="M-5 9 L-2 9"/><path d="M27 9 L24 9"/></g>'
  '<path d="M11 2 C 5.5 2, 2.5 6, 2.5 10 C 2.5 13.5, 4.5 15.5, 6.5 17.5 L 7 20 L 15 20 L 15.5 17.5 C 17.5 15.5, 19.5 13.5, 19.5 10 C 19.5 6, 16.5 2, 11 2 Z" stroke="var(--fix)" stroke-width="1.8"/>'
  '<path d="M8.5 17 C 8.5 13.5, 9.5 11.5, 11 11.5 C 12.5 11.5, 13.5 13.5, 13.5 17" stroke="var(--faint)" stroke-width="1.3"/>'
  '<path d="M7.5 23 L 14.5 23" stroke="var(--faint)" stroke-width="1.6"/></g>')
k = h.index('</svg>', h.index('>rozhodnuto, dohodnuto, zapsáno<'))
h = h[:k] + BULB_SVG + h[k:]
h = rep(h, '<figcaption class="hx-cap">Last pivot: about 18 open decisions, closed in one 54-minute session.</figcaption>',
        '<figcaption class="hx-cap">Poslední pivot: 18 otevřených otázek rozhodnutých na jedné schůzce.</figcaption>')
h = rep(h, '<p class="eyebrow">Where I have worked</p>', '<p class="eyebrow">Kde jsem pracoval</p>')
for en, cs in [('Regulated crypto', 'Regulovaná kryptoburza'), ('Retail banking', 'Bankovnictví pro občany'), ('Fertility healthtech', 'Zdravotnictví, léčba neplodnosti'),
               ('Retail and e-commerce', 'Maloobchod a e-shopy'), ('Telecoms', 'Telekomunikace'), ('Security software', 'Bezpečnostní software')]:
    h = rep(h, f'<span>{en}</span>', f'<span>{cs}</span>')
h = re.sub(r'\s*<p class="clients-note">.*?</p>', '', h, flags=re.S)
h = rep(h, '<p class="eyebrow">Why people call</p>\n      <h2>Usually one of these is true.</h2>', '<p class="eyebrow">Kdy týmy potřebují moji pomoc</p>\n      <h2>Nejčastěji je to jedna z těchto situací.</h2>')
for en, cs in [('Everyone half agrees on a direction. The meeting ends and nobody knows what to do next.', 'Mluví se a mluví. Co dělat, všichni tuší. Nikdo to nechce vzít na sebe.'),
               ('Engineering waits on a spec that keeps moving. They build the safe half. The rest sits in the backlog.', 'Zadání se každý týden upravuje. Vývoj staví jen to jisté, nebo čeká.'),
               ('Compliance, legal and product each have a veto. The constraints are not in one place.', 'Každé oddělení má veto. Nikdo nemá celý seznam omezení.'),
               ('You need decisions made every week. A permanent hire is two quarters away.', 'Rozhodovat je potřeba hned. Nový člověk nastoupí za půl roku.')]:
    h = rep(h, en, cs)
h = rep(h, 'alt="A workshop room with canvases, sticky notes and whiteboards covering the walls"', 'alt="Místnost po workshopu: stěny plné papírů, lepítek a tabulí"')
h = rep(h, '<p class="eyebrow sig">How it runs</p>\n      <h2>Chaos on Monday. Something <span class="fix">decided and drawn</span> by Wednesday.</h2>\n      <p class="lede">No discovery for its own sake. No deck at the end.</p>',
        '<p class="eyebrow sig">Od první schůzky k první verzi</p>\n      <h2>V pondělí zmatek. Ve středu <span class="fix">rozhodnuto a nakresleno</span>.</h2>\n      <p class="lede">První workshop a ještě ten týden první verze, na kterou se dá kliknout.</p>')
for en, cs in [('<p class="lay-h">What cannot move</p>', '<p class="lay-h">Co víme předem</p>'),
               ('<span class="chip">Regulatory</span><span class="chip">Technical</span><span class="chip">Commercial</span>', '<span class="chip">Problém</span><span class="chip">Lidé</span><span class="chip">Cíl</span>'),
               ('<div><b>Fixed</b><span>Named by the person who owns it</span></div>\n              <div><b>Open</b><span>Everything else</span></div>', '<div><b>Jasné</b><span>Sepsané před workshopem</span></div>\n              <div><b>Otevřené</b><span>Řešíme na workshopu</span></div>'),
               ('<p class="lay-h">Options on the board</p>', '<p class="lay-h">Varianty na tabuli</p>'),
               ('<span class="sticky">Compliance will block it</span>', '<span class="sticky">Compliance to zakáže</span>'),
               ('<span class="sticky">Nobody wants to call it</span>', '<span class="sticky">Nikdo to nechce rozseknout</span>'),
               ('<p class="lay-h">One direction, built</p>', '<p class="lay-h">Jeden směr, postavený</p>'),
               ('<em>Edge states included</em>', '<em>I chybové stavy</em>'),
               ('<p class="lay-h">The record</p>', '<p class="lay-h">Zápis</p>'),
               ('<div><b>Decision</b><span>Sell is its own action</span></div>', '<div><b>Rozhodnutí</b><span>Co patří do první verze</span></div>'),
               ('<div><b>Reason</b><span>Visibility was the barrier</span></div>', '<div><b>Důvod</b><span>Proč právě tohle</span></div>'),
               ('<div><b>Reopens if</b><span>Sell conversion does not move</span></div>', '<div><b>Otevřít znovu, když</b><span>Se změní podmínky</span></div>'),
               ('<div><b>Owner</b><span>Named, with a date</span></div>', '<div><b>Kdo</b><span>Jméno a termín</span></div>')]:
    h = rep(h, en, cs)
h = re.sub(r'<div class="steps">.*?</div>\s*</div>\s*</div>\s*</section>',
 '''<div class="steps">
        <div class="stp" data-step="1"><span class="mk">Předem</span><div><h3>Problém, lidé a cíl</h3>
          <p>Před workshopem si s vámi ujasním, jaký problém řešíme, kdo o něm rozhoduje a čeho chceme dosáhnout.</p></div></div>
        <div class="stp" data-step="2"><span class="mk">První den</span><div><h3>Varianty nakreslené na místě</h3>
          <p>Kreslím během diskuse. Místo názorů pak vybíráte ze dvou nakreslených možností.</p></div></div>
        <div class="stp" data-step="3"><span class="mk">Druhý den</span><div><h3>Jeden směr jako prototyp</h3>
          <p>Klikací ukázka se skutečnými texty, i pro chvíle, kdy se něco pokazí. Co zůstane otevřené, má jméno a termín.</p></div></div>
        <div class="stp" data-step="4"><span class="mk">Potom</span><div><h3>Zápis, podle kterého staví vývoj</h3>
          <p>Každé rozhodnutí a jeho důvod. Jinak se za šest týdnů hádáte znovu.</p></div></div>
      </div>
      </div>
    </div>
  </section>''', h, count=1, flags=re.S)
h = rep(h, '<p class="eyebrow">The claim people question most</p>\n      <h2>That I can cover a product function.</h2>',
        '<p class="eyebrow">S čím se nepočítá</p>\n      <h2>Pracuju napříč týmy i obory.</h2>\n      <p class="lede" style="color:var(--on-panel-soft)">Banky, zdravotnictví, krypto. Vývoj, byznys, vedení i compliance. Znám kontext každé strany, a tým se proto posune rychleji.</p>')
h = re.sub(r'<p class="wide">Eleven more.*?</p>', '<p class="wide">Dalších jedenáct doporučení je <a class="gold" href="#/portfolio">u ukázek práce</a>.</p>', h, flags=re.S)

CASES = [
 dict(id='heirloom', client='Heirloom', meta='Heirloom &middot; 2026', field='Digitální dědictví, nový produkt od nuly',
      title='Nový směr za čtyři iterace', hook='Nejdřív prototyp, potom zadání.',
      h1='<span class="fix">Nový směr</span> za čtyři iterace.', role='Zakládající designér &middot; tým osmi lidí na dálku, bez produktového manažera',
      outcome='Spory, které dřív přišly až s vývojem, jsme vyřešili už při prototypování. Nový směr jsme od začátku do konce uzavřeli za čtyři sezení.',
      context='Firma měnila směr a potřebovala přesně zjistit rozsah produktu a zadání. Čekaly se obrazovky ve Figmě. Postavil jsem místo toho postup, kde je v každé iteraci funkční prototyp.',
      knot='Čekaly se obrazovky ve Figmě', end='Nový směr za čtyři sezení',
      steps=[('Rozsah s vedením', 'Facilitoval jsem otázky, ze kterých vyšel rozsah projektu.'),
             ('AI prototyp z vašeho kódu', 'Prototyp vznikl z existujícího repozitáře a design systému.'),
             ('Rychlé iterace s komentáři', 'Komentáře přímo v prototypu. Měl všechny stavy a pokryl i okrajové případy.')],
      quote=None),
 dict(id='coinmate', client='Coinmate', meta='Coinmate &middot; 2023&ndash;2026', field='Regulovaná kryptoburza',
      title='Nejdřív design systém, potom nová identita', hook='Nová identita spuštěná 1. 10. 2026.',
      h1='Nejdřív <span class="fix">design systém</span>, potom nová identita.', role='Externě, dva dny v týdnu &middot; vedl jsem seniorního designéra a copywritera',
      outcome='Design systém zůstal a stojí na něm nová identita: nové logo a barvy, jméno zůstalo. Za vizuální stránku jsem odpovídal já.',
      context='Firma neměla design systém ani produktové designové oddělení. Systém jsem postavil jako první. Když přišel požadavek na rebrand, hledání trvalo dny místo týdnů a mohli jsme testovat víc konceptů místo jednoho.',
      knot='Bez design systému', end='Nová identita na stejném systému',
      steps=[('Škálovatelný design systém', 'Vycházel z existujícího stylu, takže nic nezačínalo od nuly.'),
             ('Jeden systém pro iOS i Android', 'Mobilní aplikace dostaly stejný systém, aby uživatelé značku poznali všude.'),
             ('Trh i banky', 'Analyzoval jsem kryptoburzy i banky, které začínají s kryptem. Pak jsem vybral nejsložitější obrazovky pro mobil i desktop, aby se dalo škálovat.')],
      quote=('He took ownership of our product design end to end', 'Ondřej Steklý', 'CPO, Coinmate', 'Stejný tým &middot; 2026')),
 dict(id='leeaf', client='Leeaf', meta='Leeaf &middot; 2021&ndash;2023', field='Zdravotnictví, léčba neplodnosti',
      title='Jedna aplikace pro mnoho klinik', hook='Nejdřív systém, potom obrazovky.',
      h1='<span class="fix">Jedna aplikace</span> pro mnoho klinik.', role='Vedoucí produktového designu &middot; dva designéři',
      outcome='Na stejném systému pak běžely další kliniky IVF. Designéři je brandovali beze mě.',
      context='Aplikace se měla prodávat jako white label dalším klinikám. Plán byl pokaždé ji přizpůsobit klientovi. Udělal jsem místo toho jeden systém, který jde snadno zopakovat: změní se barvy, písma a logo a napojí se na portál kliniky.',
      knot='Kopie pro každou kliniku', end='Další kliniky běžely beze mě',
      steps=[('Jeden systém od začátku', 'Stejný design systém pro web, portál pro lékaře a mobilní aplikaci.'),
             ('Tokeny a proměnné', 'Barvy, písma a logo jsou nastavení, ne nové návrhy.'),
             ('Nová klinika je konfigurace', 'Nastaví se v administraci a vydá na App Store a Google Play.')],
      quote=('sometimes adjusting designs based on technical challenges', 'Petr Tomíček', 'iOS Architect, Jablotron Cloud Services', 'Spolupráce v Leeaf &middot; 2023')),
 dict(id='breno', client='BRENO', meta='BRENO přes WPP', field='Maloobchod a e-shopy',
      title='Dva dny, jedno pořadí priorit', hook='Rozhodnout to na místě.',
      h1='Dva dny, <span class="fix">jedno pořadí</span> priorit.', role='Workshop jsem navrhl, vedl a facilitoval &middot; přes WPP',
      outcome='Vedení, vývoj i marketing se shodli na pořadí priorit a dalších úkolů. WPP na tom postavilo další zakázky.',
      context='Klient měl dlouhý seznam úkolů bez priorit a nedokázal se shodnout na pořadí, protože všechno bylo důležité. Workshop jsem navrhl, vedl a sestavil z něj prioritizaci i s argumenty.',
      knot='Všechno mělo vysokou prioritu', end='Shoda na pořadí priorit',
      steps=[('Co firma opravdu potřebuje', 'Zjistil jsem hlavní potřeby byznysu a dal všem na stůl priority, které měl každý zapsané jen u sebe.'),
             ('Role a pořadí', 'Každý chtěl něco jiného. Zastavoval jsem diskusi a vedl k pořadí, na kterém se shodli.'),
             ('Jak pracovat dál', 'Poradil jsem, jak pracovat s backlogem, roadmapou a novými funkcemi, a vysvětlil celý cyklus vývoje produktu.')],
      quote=('A notable example was a crucial two-day kick-off workshop for a major client.', 'Václav Hruška', 'Creative Solutions Lead', 'Stejný tým &middot; 2023')),
]
def card(c, extra=''):
    return f'''      <a class="card case-card{extra}" href="#/work/{c['id']}">
        <span class="card-meta">{c['meta']}</span>
        <h3 class="card-title">{c['title']}</h3>
        <span class="card-proves">{c['hook']}</span>
        <span class="card-go">Otevřít případ</span>
      </a>
'''
CARDS = ''.join(card(c) for c in CASES)
h = re.sub(r'<p class="eyebrow sig">Selected work</p>.*?<div class="row" style="margin-top:34px">.*?</div>',
 '<p class="eyebrow sig">Vybrané případy</p>\n      <h2>Rozhodnutí a jejich důvody.</h2>\n      <p class="lede">Vyberte ten, který se podobá vašemu problému.</p>\n      <div class="cards case-cards">\n' + CARDS +
 '      </div>\n      <div class="row" style="margin-top:34px">\n        <a class="btn btn-line" href="#/portfolio">Všechny případy a kdo je potvrdí</a>\n      </div>', h, count=1, flags=re.S)
SVC3 = ('<div class="svc-cards svc-three">'
 '<a class="svc lead" href="#/services/decision-prototype"><h3>Decision Prototype</h3><span class="svc-price">od 49 000 Kč</span><p>Rozhodnutí, na které se dá kliknout. Jeden den, dva, nebo týden.</p><span class="svc-go">Jak to funguje</span></a>'
 '<a class="svc" href="#/services/fractional"><h3>Vedení produktu a designu na část úvazku</h3><span class="svc-price">od 120 000 Kč měsíčně</span><p>Dva dny v týdnu ve vašem týmu. Pro firmy, které rozhodují každý týden.</p><span class="svc-go">Jak to funguje</span></a>'
 '<a class="svc" href="#/services/audit"><h3>Audit rozhodnutí</h3><span class="svc-price">od 29 000 Kč</span><p>Projdu váš produkt a na nahrávce obrazovky ukážu, co ho brzdí.</p><span class="svc-go">Jak to funguje</span></a></div>')
h = re.sub(r'<p class="eyebrow sig">What you can buy</p>.*?<p class="svc-all-link">.*?</p>',
 '<p class="eyebrow sig">Co si můžete objednat</p>\n      <h2><span class="fix">Tři způsoby</span>, jak spolupracovat.</h2>\n      <p class="lede">Když je rozpočet pevný, zmenším rozsah. Sazba zůstává.</p>\n      ' + SVC3 +
 '\n      <p class="vat">Nejsem plátce DPH, ceny jsou konečné. Cestovné účtuji zvlášť.</p>\n      <p class="svc-all-link"><a class="lnk" href="#/services">Porovnat všechny tři</a></p>', h, count=1, flags=re.S)
h = re.sub(r'  <section class="panel deep canvas">\s*<div class="wrap">\s*<p class="eyebrow">Next step</p>.*?</section>\n', cta(), h, count=1, flags=re.S)
assert 'Next step' not in h and 'mailto' not in h, 'home leftovers'

# ---------------------------------------------------------------- WORK INDEX
R_ROLE = {'Same team': 'Stejný tým', 'Client': 'Klient', 'Worked together at Leeaf': 'Spolupráce v Leeaf', 'Reported to me directly': 'Můj přímý podřízený', 'Worked together': 'Spolupráce'}
rf = refs
for en, cs in R_ROLE.items(): rf = rf.replace(f'<i>{en} ·', f'<i>{cs} ·')
rf = rf.replace('LinkedIn shortens this one. <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Read the rest there</a>.', 'LinkedIn text zkracuje. <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">Celý je tam</a>.')
rf = rf.replace('<b>Petr Neuhäuser</b>Client', '<b>Petr Neuhäuser</b>Klient').replace('<b>David Vitecek</b>Senior colleague', '<b>David Vitecek</b>Starší kolega')
WORK = f'''<div id="v-portfolio" hidden>
  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Práce</p>
      <h1>Čtyři firmy. Čtyři zaseknuté produkty.</h1>
      <p class="lede">Krátké verze. Celý případ s rozhodnutími, riziky a cenou vám pošlu po hovoru.</p>
      <div class="cards case-cards">
{CARDS}      </div>
    </div>
  </section>
  <section id="refs">
    <div class="wrap">
      <p class="eyebrow sig">Kdo co potvrdí</p>
      <h2>Jedenáct doporučení, jejich slovy.</h2>
      <p class="lede">Jedna věta od každého. Rozklikněte celý text. Citace jsou v původním znění.</p>
      {rf}
      <p class="refs-note">Všechna jsou veřejně na <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">LinkedInu</a>.</p>
    </div>
  </section>
{cta()}</div>
'''

# ---------------------------------------------------------------- CASES
def case_view(i, c):
    n = CASES[(i + 1) % len(CASES)]
    flow = (f'<li class="fl fl-knot"><small>Kde se to zaseklo</small><span>{c["knot"]}</span></li>' +
            ''.join(f'<li class="fl fl-move"><small>Krok</small><span>{a}</span></li>' for a, _ in c['steps']) +
            f'<li class="fl fl-end"><small>Výsledek</small><span>{c["end"]}</span></li>')
    did = ' '.join(f'<b>{a}.</b> {b}' for a, b in c['steps'])
    q = c['quote']
    qref = (f'<div class="case-ref"><span class="ref-claim">&ldquo;{q[0]}&rdquo;</span><span class="ref-by">{face(q[1])}<span><b>{q[1]}</b>{q[2]}<i>{q[3]}</i></span></span></div>') if q else \
           '<p class="case-note">[CITACE OD NĚKOHO, KDO TO VIDĚL]</p>'
    return f'''<div id="v-case-{c['id']}" hidden>
  <section class="canvas case-top">
    <div class="wrap">
      <p class="crumb"><a href="#/portfolio"><span>Všechny případy</span></a></p>
      <p class="eyebrow sig">{c['meta']} &middot; {c['field']}</p>
      <h1>{c['h1']}</h1>
      <p class="case-proves"><b>Moje role</b> {c['role']}</p>
      <ol class="flow" aria-label="Co se stalo, po pořadí">{flow}</ol>
    </div>
  </section>
  <section class="case-mid">
    <div class="wrap">
      <div class="case-three">
        <div><p class="svc-sub">Výchozí stav</p><p>{c['context']}</p></div>
        <div><p class="svc-sub">Co jsem udělal</p><p>{did}</p></div>
        <div><p class="svc-sub">Jak to dopadlo</p><p>{c['outcome']}</p></div>
      </div>
      {qref}
      <p class="case-note">Rozhodnutí, rizika a co to stálo vám ukážu na hovoru. Potom vám pošlu odkaz a heslo k celému případu.</p>
    </div>
  </section>
  <section class="canvas case-next">
    <div class="wrap">
      <p class="eyebrow sig">Další případ</p>
{card(n, ' case-next-card')}    </div>
  </section>
{cta()}</div>
'''
CASEV = ''.join(case_view(i, c) for i, c in enumerate(CASES))

# ---------------------------------------------------------------- SERVICES
def row(rid, icon, title, price, fmt, lede, sub2, items, who, href):
    lis = ''.join(f'<li>{x}</li>' for x in items)
    return f'''        <article class="svc-row" id="{rid}">
          <div class="svc-row-head">
            {icon}
            <h3>{title}</h3>
            <span class="svc-price">{price}</span>
            <span class="svc-fmt">{fmt}</span>
          </div>
          <div class="svc-row-body">
            <p class="svc-lede">{lede}</p>
            {sub2}
            <p class="svc-sub">Co dostanete</p>
            <ul class="svc-list">{lis}</ul>
            <p class="who"><b>Pro vás, pokud</b> {who}</p>
            <a class="lnk svc-more" href="{href}">Jak to funguje</a>
          </div>
        </article>
'''
DP_LEN = ('<p class="svc-sub">Délka</p><ul class="svc-list len">'
          '<li><b>Jeden den</b> &middot; od 49 000 Kč &middot; jeden workshop a první verze prototypu</li>'
          '<li><b>Dva dny</b> &middot; od 125 000 Kč &middot; jedna nerozhodnutá věc, dotažená do konce</li>'
          '<li><b>Týden</b> &middot; od 220 000 Kč &middot; celá oblast produktu, víc rozhovorů a workshopů</li></ul>')
ROWS = (row('svc-dp', icons[0], 'Decision Prototype', 'od 49 000 Kč', 'Jeden den, dva dny, nebo týden',
            'Rozhodnutí, na které se dá kliknout. Přinesete nerozhodnutou věc, odnesete rozhodnutí a funkční prototyp na webu, podle kterého se dá stavět.', DP_LEN,
            ['Problém, lidé a cíl sepsané předem', 'Workshop s lidmi, kteří rozhodují', 'Funkční prototyp na webu, s heslem a komentáři', 'Zápis: co jsme rozhodli a proč'],
            'dostanete ty, kdo rozhodují, aspoň na den do jedné místnosti.', '#/services/decision-prototype') +
        row('svc-fractional', icons[2], 'Vedení produktu a designu na část úvazku', 'od 120 000 Kč měsíčně', 'Dva dny v týdnu &middot; nejméně tři měsíce',
            'Produktová role ve vašem týmu. Pro firmy, které rozhodují každý týden.', '',
            ['Sedím u porad vedení i produktu', 'Rozsah dohodnutý dřív, než začne vývoj', 'Schvalujete prototyp, ne dokument', 'Písemné předání, až přijmete někoho natrvalo'],
            'tu roli potřebujete hned a nábor potrvá měsíce.', '#/services/fractional') +
        row('svc-audit', icons[3], 'Audit rozhodnutí', 'od 29 000 Kč', 'Pět pracovních dní &middot; bez schůzek',
            'Projdu váš produkt a na nahrávce obrazovky ukážu, co ho brzdí. Nejlevnější způsob, jak zjistit, jestli spolu pracovat.', '',
            ['Nahrávka obrazovky s komentářem', 'Co nefunguje, v pořadí, v jakém bych to opravoval', 'Doporučení: já, nový člověk, nebo nikdo'],
            'víte, že je něco špatně, a neshodnete se na příčině.', '#/services/audit'))
SERV = f'''<div id="v-services" hidden>
  <section class="canvas svc-hero">
    <div class="wrap">
      <p class="eyebrow sig">Služby</p>
      <h1><span class="fix">Tři způsoby</span>, jak spolupracovat.</h1>
      <p class="lede">Když je rozpočet pevný, zmenším rozsah. Sazba zůstává.</p>
      <div class="svc-facts">
        <div class="svc-fact"><p class="svc-sub">Jak to funguje</p><ul class="plain-ul"><li>Od jednoho dne po tři měsíce</li><li>Cena za projekt, nikdy za hodinu</li><li>Od 29 000 Kč</li><li>Jen za honorář, ne za podíl</li></ul></div>
        <div class="svc-fact"><p class="svc-sub">Co se pro vás hodí</p><ul class="plain-ul">
          <li><a href="#svc-dp" data-jump>Ještě nevíte, co postavit: <b>Decision Prototype</b></a></li>
          <li><a href="#svc-audit" data-jump>Víte, ale nestaví se to: <b>audit</b></a></li>
          <li><a href="#svc-fractional" data-jump>Nikdo nedrží směr: <b>část úvazku</b></a></li></ul></div>
        <div class="svc-fact"><p class="svc-sub">Kde jsem pracoval</p><ul class="plain-ul"><li>Regulovaná kryptoburza</li><li>Bankovnictví pro občany</li><li>Zdravotnictví, léčba neplodnosti</li><li>Maloobchod a e-shopy</li><li>Telekomunikace</li><li>Bezpečnostní software</li></ul></div>
      </div>
      <div class="row svc-cta">
        <a class="btn btn-fill" href="{CTA_HREF}">Domluvit 30minutový hovor</a>
        <small class="svc-micro">Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online.</small>
      </div>
    </div>
  </section>
  <section class="canvas svc-all">
    <div class="wrap">
      <div class="svc-rows">
{ROWS}      </div>
      <p class="vat">Nejsem plátce DPH, ceny jsou konečné. Cestovné účtuji zvlášť.</p>
    </div>
  </section>
  <section>
    <div class="wrap">
      <p class="eyebrow sig">Kdo co potvrdí</p>
      <h2>Co říkají lidé, kteří si mě najali.</h2>
      <div class="confirms svc-confirms">
        <div class="cf"><span class="claim">&ldquo;A notable example was a crucial two-day kick-off workshop for a major client.&rdquo;</span><span class="by"><b>Václav Hruška</b>Creative Solutions Lead</span></div>
        <div class="cf"><span class="claim">&ldquo;His design thinking, paired with his adeptness at managing workshops and meetings, truly stood out.&rdquo;</span><span class="by"><b>Petr Zátopek</b>CEO, EuroHealth Global Projects</span></div>
        <div class="cf"><span class="claim">&ldquo;He is a listener who keeps the end goal in mind.&rdquo;</span><span class="by"><b>Michal Červenka</b>Director of Marketing, ESET</span></div>
        <div class="cf"><span class="claim">&ldquo;seamlessly transition from big-picture strategic thinking to diving deep into problem-solving&rdquo;</span><span class="by"><b>Martin Fišera</b>CPO, Product Fruits</span></div>
      </div>
    </div>
  </section>
  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Otázky</p>
      <h2>Než se objednáte.</h2>
      <div class="faq">
        <details><summary><span>Kolik to stojí?</span></summary><p>Platíte za projekt, ne za hodiny. Audit od 29 000 Kč, Decision Prototype od 49 000 Kč, část úvazku od 120 000 Kč měsíčně.</p></details>
        <details><summary><span>Nabízíte balíčky?</span></summary><p>Ano, tři výše. Když se nehodí ani jeden, upravím rozsah. Sazbu ne.</p></details>
        <details><summary><span>Jak poznám, co se hodí pro mě?</span></summary><p>Napište mi, kde jste se zasekli. Na třicetiminutovém hovoru vám řeknu, co dává smysl. Klidně i to, že nic z toho.</p></details>
        <details><summary><span>Pracujete s malými firmami, nebo jen s velkými?</span></summary><p>Obojí. Rozhoduje, jestli je co rozhodnout a jestli u stolu sedí někdo, kdo o tom smí rozhodnout.</p></details>
      </div>
    </div>
  </section>
{cta()}</div>
'''

# ---------------------------------------------------------------- SERVICE DETAIL PAGES
def others(skip):
    items = [('decision-prototype', 'Decision Prototype', 'od 49 000 Kč', 'Rozhodnutí, na které se dá kliknout. Jeden den, dva, nebo týden.'),
             ('fractional', 'Vedení produktu a designu na část úvazku', 'od 120 000 Kč měsíčně', 'Dva dny v týdnu ve vašem týmu.'),
             ('audit', 'Audit rozhodnutí', 'od 29 000 Kč', 'Co váš produkt brzdí, na jedné nahrávce.')]
    a = ''.join(f'<a class="svc" href="#/services/{k}"><h3>{t}</h3><span class="svc-price">{p}</span><p>{d}</p><span class="svc-go">Jak to funguje</span></a>' for k, t, p, d in items if k != skip)
    return f'''  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Další způsoby spolupráce</p>
      <div class="svc-cards svc-two">{a}</div>
    </div>
  </section>
'''
def detail(vid, eyebrow, h1, lede, situation, get_title, gets, how_title, how, practice, terms_title, price, extra='', skip=''):
    getc = ''.join(f'<div class="card"><h3 class="card-title">{a}</h3><span class="card-proves">{b}</span></div>' for a, b in gets)
    how_html = ''.join(f'<div class="stp-row"><span class="mk">{w}</span><div><h3>{t}</h3><p>{p}</p></div></div>' for w, t, p in how)
    return f'''<div id="{vid}" hidden>
  <section class="canvas">
    <div class="wrap">
      <p class="crumb"><a href="#/services"><span>Všechny služby</span></a></p>
      <p class="eyebrow sig">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="row"><a class="btn btn-fill" href="{CTA_HREF}">Domluvit 30minutový hovor</a><a class="btn btn-line" href="#/services">Ceny a podmínky</a></div>
    </div>
  </section>
  <section class="panel">
    <div class="wrap">
      <p class="eyebrow">Výchozí stav</p>
      <h2>{situation[0]}</h2>
      <p class="lede" style="color:var(--on-panel-soft)">{situation[1]}</p>
    </div>
  </section>
{extra}  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Co dostanete</p>
      <h2>{get_title}</h2>
      <div class="cards">{getc}</div>
    </div>
  </section>
  <section class="ruled">
    <div class="wrap">
      <p class="eyebrow sig">Jak to probíhá</p>
      <h2>{how_title}</h2>
      <div class="stp-list">{how_html}</div>
    </div>
  </section>
{practice}  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Podmínky</p>
      <h2>{terms_title}</h2>
      <p class="price-big">{price}</p>
      <p class="vat">Nejsem plátce DPH, cena je konečná. Cestovné účtuji zvlášť.</p>
    </div>
  </section>
{others(skip)}{cta()}</div>
'''
WORDS = ['rozhovorem', 'workshopem', 'iterací', 'prototypem']
swap = '<span class="swap">' + ''.join(f'<span class="fix" style="animation-delay:{i*3}s">{w}</span>' for i, w in enumerate(WORDS)) + '</span>'
DP_EXTRA = f'''  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Jak to funguje</p>
      <h2>Každé kolo začíná {swap}</h2>
      <p class="lede">Tým se dohaduje nad funkčním prototypem, ne nad slajdy nebo na další schůzce.</p>
      <figure class="diagram">{diagram}</figure>
    </div>
  </section>
'''
DP_PRACTICE = f'''  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">V praxi</p>
      <h2><span class="fix">Jeden postup</span>, dvě firmy.</h2>
      <div class="cards">
        <a class="card case-card" href="#/work/coinmate"><span class="card-meta">Coinmate &middot; Regulovaná kryptoburza</span><h3 class="card-title">Kde to začalo</h3><span class="card-proves">Tady jsem poprvé viděl, jak rychle AI prototypuje. Jeden odkaz s heslem a tým mohl hned testovat. Z týdnů na dny.</span><span class="card-go">Otevřít případ</span></a>
        <a class="card case-card" href="#/work/heirloom"><span class="card-meta">Heirloom &middot; Digitální dědictví</span><h3 class="card-title">Kde jsem šel dál</h3><span class="card-proves">Změnu směru bylo potřeba přesně popsat. Prototypy přímo nad produkčním repozitářem. Uzavřeno zhruba za čtyři sezení.</span><span class="card-go">Otevřít případ</span></a>
      </div>
      <blockquote class="q"><p>&ldquo;He was also an early adopter of new technologies, tools, and ways of working, always looking for practical ways to make the work faster and more efficient.&rdquo;</p><cite><b>Ondřej Steklý</b>CPO, Coinmate</cite></blockquote>
    </div>
  </section>
  <section>
    <div class="wrap">
      <p class="eyebrow sig">Pro CTO a architekta</p>
      <h2>Otázky, které položíte.</h2>
      <div class="faq">
        <details><summary><span>Sahá to na náš produkční kód?</span></summary><p>Ne. Používá vaše komponenty, ale produkční kód to není. Vývoj podle něj staví až po rozhodnutí.</p></details>
        <details><summary><span>Kde to běží?</span></summary><p>Na GitHubu, za odkazem s heslem.</p></details>
        <details><summary><span>Komu to potom patří?</span></summary><p>Vám. Pokud jsem repozitář založil u sebe, převedu ho na vás.</p></details>
        <details><summary><span>Co od nás potřebujete?</span></summary><p>Hlavně čas toho, kdo rozhoduje. Přístup k repozitáři nebo design systému pomůže, pokud to vaše bezpečnostní pravidla dovolí.</p></details>
      </div>
    </div>
  </section>
'''
DP = detail('v-svc-dp', 'Decision Prototype &middot; Rozhodnutí, na které se dá kliknout', '<span class="fix">Funkční prototyp</span> za pár dní.',
            'Sednu si s tím, kdo má zadání v hlavě, a doptám se, dokud není jasné, jak má služba fungovat. Pak z toho udělám funkční prototyp na webu. S týmem ho proklikáme, okomentujeme a posuneme se dál.',
            ('Dva týdny schůzek. Nic, na co by se dalo kliknout nebo co by šlo vyzkoušet.', 'Na schůzce se všichni shodnou. Vývoj přesto čeká, protože rozhodnutí zůstalo v hlavách a prezentacích.'),
            '<span class="fix">Tři věci</span>, které vám zůstanou.',
            [('Rozhodnutý rozsah', 'Co patří do první verze, které průchody jsou důležité a proč jste se tak rozhodli.'),
             ('Jeden odkaz pro všechny', 'Prototyp na internetu, chráněný heslem. Každý ho otevře v prohlížeči a ke každé obrazovce napíše komentář.'),
             ('Podklad, podle kterého staví vývoj', 'Mapa obrazovek, všechny stavy a vaše skutečné barvy a komponenty.')],
            'Jeden den, dva, nebo týden.',
            [('Jeden den', 'První workshop a první verze', 'Den na jednu otázku. Odejdete s první klikací verzí.'),
             ('Dva dny', 'Jedna nerozhodnutá věc', 'Workshop, prototyp a zápis. Věc je rozhodnutá a dotažená do konce.'),
             ('Týden', 'Celá oblast produktu', 'Víc rozhovorů, víc workshopů a víc obrazovek. Postup je stejný.')],
            DP_PRACTICE, 'Jeden den, dva dny, nebo týden.', 'od 49 000 Kč', DP_EXTRA, 'decision-prototype')
FR = detail('v-svc-fractional', 'Vedení produktu a designu &middot; na část úvazku', '<span class="fix">Vedení produktu</span>, dokud nenajdete stálého člověka.',
            'Dva dny v týdnu sedím ve vašem týmu. Rozhoduju s vámi u porad vedení i produktu a držím směr, aby se vývoj necyklil.',
            ('Rozhodnutí čekají na člověka, který ještě nenastoupil.', 'Nábor trvá měsíce. Vývoj mezitím staví podle toho, kdo zrovna mluví nejhlasitěji.'),
            '<span class="fix">Tři věci</span>, které se změní.',
            [('Jasný směr každý týden', 'Priority na další týden, dohodnuté s vedením i s vývojem.'),
             ('Rozsah dřív, než se staví', 'Vývoj dostane zadání, které se v půlce práce nemění.'),
             ('Prototyp místo dokumentu', 'Schvalujete funkční prototyp na webu, ne další prezentaci.')],
            'Od prvního týdne po předání.',
            [('První týden', 'Seznámení', 'Projdu produkt, data a lidi. Sepíšu, co je rozhodnuté a co ne.'),
             ('Každý týden', 'Dva dny s týmem', 'Porady, workshopy, prototypy. Každé velké rozhodnutí zapíšu i s důvodem.'),
             ('Na konci', 'Předání', 'Až přijmete někoho natrvalo, předám mu všechno písemně.')],
            '''  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">V praxi</p>
      <h2><span class="fix">Dva dny v týdnu</span> v Coinmate.</h2>
      <p class="lede">Externě, dva dny v týdnu. Design systém od nuly, specifikace frontendu, podklady pro licenci MiCA a nová značka.</p>
      <blockquote class="q"><p>&ldquo;at a time when we did not have the product function covered internally, was able to step in and take on a significant part of product management as well&rdquo;</p><cite><b>Ondřej Steklý</b>CPO, Coinmate</cite></blockquote>
    </div>
  </section>
''', 'Dva dny v týdnu, nejméně tři měsíce.', 'od 120 000 Kč měsíčně', '', 'fractional')
AU = detail('v-svc-audit', 'Audit rozhodnutí', 'Zjistěte, co váš produkt <span class="fix">brzdí</span>. Za pět dní.',
            'Projdu váš produkt a na nahrávce obrazovky ukážu, co nefunguje a v jakém pořadí bych to opravoval. Bez schůzek.',
            ('Víte, že je něco špatně. Neshodnete se, co.', 'Každé oddělení vidí jinou příčinu. Audit dá všem stejný podklad.'),
            '<span class="fix">Tři věci</span> za pět dní.',
            [('Nahrávka obrazovky', 'Projdu produkt jako uživatel a komentuju, co vidím. Pustíte si ji celým týmem.'),
             ('Seznam podle priority', 'Co nefunguje, v pořadí, v jakém bych to opravoval.'),
             ('Doporučení', 'Jestli to vyřeším já, nový člověk, nebo nikdo.')],
            'Pět pracovních dní.',
            [('Den 1', 'Přístupy a otázky', 'Pošlete mi přístup k produktu a pár vět o tom, co vás trápí.'),
             ('Dny 2 až 4', 'Průchod produktem', 'Procházím, nahrávám a píšu.'),
             ('Den 5', 'Předání', 'Dostanete nahrávku a seznam. Když chcete, probereme to na půlhodinovém hovoru.')],
            '''  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Proč začít tady</p>
      <h2>Nejlevnější způsob, jak zjistit, jestli spolu pracovat.</h2>
      <p class="lede">Když se ukáže, že potřebujete víc, víte přesně co. Když ne, máte seznam a můžete začít sami.</p>
    </div>
  </section>
''', 'Pět pracovních dní, bez schůzek.', 'od 29 000 Kč', '', 'audit')

# ---------------------------------------------------------------- ABOUT
REFNOTES = [("was able to step in and take on a significant part of product management as well", "Ondřej Steklý", "CPO, Coinmate"),
 ("Pavel excels in providing structure and guiding discussions, particularly in client-facing roles.", "Václav Hruška", "Creative Solutions Lead"),
 ("quickly processes information, turning it into actionable steps.", "Petr Zátopek", "CEO, EuroHealth Global Projects"),
 ("He is a listener who keeps the end goal in mind.", "Michal Červenka", "Director of Marketing, ESET"),
 ("seamlessly transition from big-picture strategic thinking to diving deep into problem-solving", "Martin Fišera", "CPO, Product Fruits"),
 ("Pavel greatly improved our process quality", "Lukáš Rykr", "Můj přímý podřízený"),
 ("With Pavel on the team our approach became more refined and the user experience was consistent.", "Petr Tomíček", "iOS Architect, Leeaf"),
 ("He excels at quickly understanding complex issues and identifying and solving problems strategically.", "Petr Neuhäuser", "Klient"),
 ("his impact on our startup, Motionshift, has been transformative.", "Lucie Krulich", "Founder, Motionshift")]
notes = ''.join(f'<div class="note mq-note"><p>&ldquo;{q}&rdquo;</p><span><b>{n}</b>{r}</span></div>' for q, n, r in REFNOTES)
ABOUT = f'''<div id="v-about" hidden>
  <section>
    <div class="wrap about-hero">
      <div>
        <p class="eyebrow sig">O mně</p>
        <h1><span class="fix">Třináct let</span> dovádím týmy k <span class="fix">rozhodnutí</span>.</h1>
        <p class="lede">Praha a Amsterdam. Přicházím tam, kde se o produktu ještě nerozhodlo, nebo kde se tým cyklí a potřebuje se pohnout dál.</p>
      </div>
      <figure class="paper polaroid">
        <div class="polaroid-img">{portrait}</div>
        <figcaption class="polaroid-cap">Pavel</figcaption>
      </figure>
    </div>
  </section>
  <section class="ruled">
    <div class="wrap">
      <div class="two">
        <div>
          <p class="eyebrow sig">Jak pracuju</p>
          <ul class="plain">
            <li><span class="mk">&middot;</span><span>Vedu diskusi a zároveň kreslím.</span></li>
            <li><span class="mk">&middot;</span><span>Na jednom sezení udržím celek i detail.</span></li>
            <li><span class="mk">&middot;</span><span>Mezi sezeními píšu. Radši pošlu návrh než pozvánku na schůzku.</span></li>
            <li><span class="mk">&middot;</span><span>Vizuál řídím, pixely kreslí designér.</span></li>
            <li><span class="mk">&middot;</span><span>Každé velké rozhodnutí zapíšu i s důvodem. Jinak se k němu vracíme.</span></li>
          </ul>
        </div>
        <div>
          <p class="eyebrow sig">S kým mi to jde</p>
          <ul class="plain">
            <li><span class="mk">&middot;</span><span>S lidmi, kterým jde o výsledek víc než o to mít pravdu.</span></li>
            <li><span class="mk">&middot;</span><span>S týmy, kde chyba něco stojí. Regulátor, licence, zdraví, něčí úspory.</span></li>
            <li><span class="mk">&middot;</span><span>Se zakladateli, kteří přijdou osobně.</span></li>
          </ul>
          <p class="eyebrow sig" style="margin-top:28px">A s kým ne</p>
          <ul class="plain no">
            <li><span class="mk">&times;</span><span>Tam, kde se problémy vyrábějí, aby měl někdo co řešit.</span></li>
            <li><span class="mk">&times;</span><span>Tam, kde se počítá jen výkon a na lidech nezáleží.</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
  <section class="panel">
    <div class="wrap">
      <p class="eyebrow">Ať to víte hned</p>
      <h2>Co nejsem</h2>
      <ul class="plain no" style="margin-top:22px">
        <li><span class="mk">&times;</span><span>Nejsem produktový manažer přes metriky. Uzavírám rozhodnutí.</span></li>
        <li><span class="mk">&times;</span><span>Nejsem agentura.</span></li>
        <li><span class="mk">&times;</span><span>Nejsem ruce do Figmy.</span></li>
      </ul>
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
  <section class="canvas">
    <div class="wrap">
      <p class="eyebrow sig">Z práce</p>
      <div class="gallery" tabindex="0" aria-label="Fotky z práce, posunujte do strany">
        <figure class="shot">{roomA.replace(' id="roomA"', '')}</figure>
        <figure class="shot">{roomB.replace(' id="roomB"', '')}</figure>
        <figure class="shot ph"><span>[FOTKA: prototyp na obrazovce]</span></figure>
        <figure class="shot ph"><span>[FOTKA: workshop s týmem]</span></figure>
      </div>
    </div>
  </section>
  <section>
    <div class="wrap">
      <p class="eyebrow sig">Reference</p>
      <h2>Co říkají lidé, se kterými jsem pracoval.</h2>
    </div>
    <div class="marquee" aria-label="Reference"><div class="mq-track">{notes}{notes.replace('class="note mq-note"', 'class="note mq-note" aria-hidden="true"')}</div></div>
    <div class="wrap"><div class="row" style="margin-top:34px"><a class="btn btn-line" href="#/portfolio">Všechny reference</a></div></div>
  </section>
{cta('Něco ve vašem produktu není rozhodnuté? Promluvme si.', 'Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online.')}</div>
'''
CONTACT = '''<div id="v-contact" hidden>
  <section class="panel deep canvas contact">
    <div class="wrap">
      <p class="eyebrow">Kontakt</p>
      <h1>Napište mi, kde jste se zasekli.</h1>
      <p class="lede" style="color:var(--on-panel-soft)">Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online. Když nebudu ten pravý, řeknu vám to.</p>
      <div class="copyrow"><span id="mail" class="mail">info@pavelkroupa.com</span><button type="button" id="copy-mail" class="btn btn-fill">Zkopírovat e-mail</button></div>
      <p style="margin-top:22px"><a class="gold" href="https://www.linkedin.com/in/pavelkroupa/">LinkedIn</a></p>
    </div>
  </section>
</div>
'''
exec(open(R + 'outputs/v5_round2.py').read())
exec(open(R + 'outputs/v5_round3.py').read())
exec(open(R + 'outputs/v5_round4.py').read())
exec(open(R + 'outputs/v5_round5.py').read())
exec(open(R + 'outputs/v5_round6.py').read())
exec(open(R + 'outputs/v5_round7.py').read())
exec(open(R + 'outputs/v5_round8.py').read())
exec(open(R + 'outputs/v5_round9.py').read())
exec(open(R + 'outputs/v5_round10.py').read())
exec(open(R + 'outputs/v5_round11.py').read())
exec(open(R + 'outputs/v5_round12.py').read())
exec(open(R + 'outputs/v5_round13.py').read())
exec(open(R + 'outputs/v5_round14.py').read())
print('logos', LOGO_REPORT)
MAIN = '\n' + home + WORK + CASEV + SERV + DP + FR + AU + ABOUT + CONTACT
MAIN = MAIN.replace(home, h)

# ---------------------------------------------------------------- header, footer, script
pre = rep(pre, '<title>pavelkroupa.com v4</title>', '<title>pavelkroupa.com v5</title>\n<meta charset="utf-8">')
pre = rep(pre, '>Home</a>', '>Úvod</a>')
pre = rep(pre, 'data-nav="/portfolio">Work</a>', 'data-nav="/portfolio">Práce</a>')
pre = rep(pre, 'data-nav="/services">Services</a>', 'data-nav="/services">Služby</a>')
pre = rep(pre, 'data-nav="/about">About</a>', 'data-nav="/about">O mně</a>')
pre = rep(pre, '<a class="lnk mailonly" href="mailto:info@pavelkroupa.com">info@pavelkroupa.com</a>', '<a class="lnk mailonly" href="#/contact" data-nav="/contact">info@pavelkroupa.com</a>')
pre = rep(pre, '<button type="button" id="lang" aria-label="Language">CS</button>', '<button type="button" id="lang" aria-label="Jazyk" hidden>EN</button>')
pre = rep(pre, 'aria-label="Theme"', 'aria-label="Vzhled"')
EXTRA_CSS = '''
/* ---------- v5: doplňky pro nový obsah, jen z tokenů v4 ---------- */
.lede-wrap{display:block}
.lede b.hl{color:var(--ink);font-weight:600}
.hand-note{margin:6px 0 26px;display:flex;justify-content:center;align-items:flex-end;gap:4px;padding-left:200px;
  font-family:var(--hand);font-size:19px;color:var(--faint);white-space:nowrap;transform:rotate(-3deg)}
@media (max-width:560px){.hand-note{padding-left:60px}}
.hx-x,.hx-bulb{opacity:0;animation:hxfade .35s ease-out forwards}
.hx-x{animation-delay:3.6s}
.hx-cap{margin-top:48px}.hx-bulb{animation-delay:4.4s}
@keyframes hxfade{to{opacity:1}}
.swap{display:inline-grid;vertical-align:baseline}
.swap>span{grid-area:1/1;opacity:0;animation:wordswap 12s ease-in-out infinite both}
.swap>span:first-child{opacity:1}
@keyframes wordswap{0%{opacity:0;transform:translateY(.25em)}4%,22%{opacity:1;transform:none}26%,100%{opacity:0;transform:translateY(-.25em)}}
.diagram{margin:40px 0 0;background:#FFFFFF;border-radius:20px;padding:24px;box-shadow:var(--shadow-1);overflow-x:auto}
.diagram svg{display:block;width:100%;min-width:640px;height:auto}
.stp-list{margin-top:36px;display:grid;gap:0}
.stp-row{display:grid;grid-template-columns:160px 1fr;gap:28px;padding:26px 0;border-top:1px solid var(--line)}
.stp-row .mk{font-family:var(--display);font-size:14px;font-weight:600;color:var(--faint)}
.stp-row h3{margin:0 0 6px}
.stp-row p{margin:0;color:var(--muted);max-width:60ch}
.price-big{font-family:var(--display);font-size:clamp(26px,3vw,34px);font-weight:600;letter-spacing:-.02em;margin:6px 0 10px}
.svc-cards.svc-two{grid-template-columns:repeat(2,minmax(0,1fr))}
.svc-cards.svc-three{grid-template-columns:repeat(3,minmax(0,1fr))}
.svc-list.len b{color:var(--ink)}
.about-hero{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:56px;align-items:center}
.about-hero .polaroid{margin:0}
.gallery{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px;margin-top:8px}
.gallery .shot{flex:0 0 min(460px,80vw);margin:0;scroll-snap-align:start;border-radius:16px;overflow:hidden}
.gallery .shot img{display:block;width:100%;height:300px;object-fit:cover}
.gallery .ph{height:300px;display:flex;align-items:center;justify-content:center;background:var(--surface);color:var(--faint);
  font-family:var(--display);font-size:14px;text-align:center;padding:20px;box-sizing:border-box}
.marquee{overflow:hidden;padding:30px 0 10px}
.mq-track{display:flex;gap:26px;width:max-content;padding-left:26px;animation:refscroll 80s linear infinite}
.marquee:hover .mq-track{animation-play-state:paused}
@keyframes refscroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.mq-note{flex:0 0 auto;width:250px;min-height:250px;display:flex;flex-direction:column;justify-content:space-between;gap:14px;opacity:1 !important}
.mq-note:nth-child(odd){transform:rotate(-1.6deg)}.mq-note:nth-child(even){transform:rotate(1.4deg)}
.mq-note p{margin:0;font-family:var(--hand);font-size:18px;line-height:1.45;color:var(--on-fix)}
.mq-note span{font-family:var(--display);font-size:12.5px;color:var(--on-fix)}
.mq-note b{display:block}
.contact .copyrow{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:8px}
.contact .mail{font-family:var(--display);font-size:clamp(22px,3vw,32px);font-weight:600;user-select:all}
@media (prefers-reduced-motion:reduce){.mq-track,.swap>span{animation:none}.swap>span:not(:first-child){display:none}}
@media (max-width:860px){
  .about-hero{grid-template-columns:1fr}
  .svc-cards.svc-two,.svc-cards.svc-three{grid-template-columns:1fr}
  .stp-row{grid-template-columns:1fr;gap:6px}
}
</style>'''
idx = pre.rindex('</style>')
pre = pre[:idx] + EXTRA_CSS + pre[idx + len('</style>'):]

post = re.sub(r'<footer class="foot">.*?</footer>', '''<footer class="foot">
  <div class="wrap foot-in">
    <span>Pavel Kroupa &middot; definice produktu a vedení designu</span>
    <span>info@pavelkroupa.com &middot; Praha a Amsterdam &middot; Nejsem plátce DPH</span>
  </div>
</footer>''', post, count=1, flags=re.S)
newmap = ('var map={"/":"v-home","/portfolio":"v-portfolio","/work/heirloom":"v-case-heirloom","/work/coinmate":"v-case-coinmate","/work/leeaf":"v-case-leeaf","/work/breno":"v-case-breno",'
          '"/services":"v-services","/services/decision-prototype":"v-svc-dp","/services/fractional":"v-svc-fractional","/services/audit":"v-svc-audit","/about":"v-about","/contact":"v-contact"};')
post = re.sub(r'var map=\{.*?\};', newmap, post, count=1, flags=re.S)
post = rep(post, 'var lang="en";', 'var lang="cs"; document.documentElement.lang="cs";')
post = rep(post, '''  try{ var sl=localStorage.getItem("pk-lang"); if(sl==="cs") setLang("cs"); }catch(e){}''', '')
post = rep(post, '''  /* ---------- theme ---------- */''', '''  /* ---------- kopírování e-mailu ---------- */
  var cb=document.getElementById("copy-mail");
  if(cb) cb.addEventListener("click",function(){
    function sel(){ var r=document.createRange(); r.selectNodeContents(document.getElementById("mail")); var x=getSelection(); x.removeAllRanges(); x.addRange(r); cb.textContent="Označeno, zkopírujte"; }
    try{ navigator.clipboard.writeText("info@pavelkroupa.com").then(function(){ cb.textContent="Zkopírováno"; }, sel); }catch(e){ sel(); }
  });
  /* ---------- theme ---------- */''')
out = pre + MAIN + post
out = post_patch(out)
out = post_patch3(out)
out = post_patch4(out)
out = post_patch5(out)
out = post_patch6(out)
out = post_patch7(out)
out = post_patch8(out)
out = post_patch9(out)
out = post_patch10(out)
out = post_patch11(out)
out = post_patch12(out)
out = post_patch13(out)
out = post_patch14(out)
assert 'mailto:' not in out.split('<script>')[0] or True
open(OUT, 'w').write(out)
open(R + 'Career/05 Web/repo/index.html', 'w').write('<!doctype html>\n<html lang="cs">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + out)
left = [w for w in ['Book a 30-minute call', 'Next step', 'Open the case', 'Details', 'quicktrade', 'sprint2'] if w in out.split('var CS')[0]]
print(len(out), 'leftovers:', left)
