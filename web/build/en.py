"""Anglická verze webu: texty a metadata.

Překlady jsou psané podle zásad Nielsen Norman Group: krátké věty, činný rod, nejdůležitější
informace na začátku, čísla jako číslice („2 days a week“), americký pravopis, sériová čárka,
žádné reklamní nadsázky.

Formát: dvojice řádků „cs:“ a „en:“, mezi dvojicemi prázdný řádek. Klíč „cs:“ je vnitřní HTML
prvku tak, jak je v src/index.html (mezery se sjednotí). Když se český text změní, pages.py
vypíše, který anglický překlad chybí, a který se naopak přestal používat.

Ceny jsou v korunách, stejně jako na české verzi.
"""
import re


def _pairs(block):
    out = {}
    for chunk in re.split(r"\n\s*\n", block.strip()):
        lines = [l for l in chunk.strip().split("\n") if l.strip() and not l.lstrip().startswith("#")]
        if not lines:
            continue
        cs = " ".join(l.split("cs:", 1)[1].strip() for l in lines if l.startswith("cs:"))
        en = " ".join(l.split("en:", 1)[1].strip() for l in lines if l.startswith("en:"))
        assert cs and en, f"en.py: neúplná dvojice: {chunk[:80]!r}"
        key = re.sub(r"\s+", " ", cs).strip()
        assert key not in out, f"en.py: dvakrát stejný český text: {key[:80]!r}"
        out[key] = en
    return out


def price(v):
    return f"CZK {v:,}"


PRICE_RANGE = "From CZK 29,000"

# ---------------------------------------------------------------- texty na stránkách
UNITS = _pairs(r'''
# ---------- hlavička a patička
cs: Úvod
en: Home

cs: Služby
en: Services

cs: O mně
en: About

cs: Kontakt
en: Contact

cs: <span>Pavel Kroupa &middot; definice produktu a vedení designu</span> <span>info@pavelkroupa.com &middot; Praha a Amsterdam</span>
en: <span>Pavel Kroupa &middot; Product definition and design leadership</span> <span>info@pavelkroupa.com &middot; Prague and Amsterdam</span>

# ---------- úvod
cs: Pomáhám týmům <span class="fix">rozhodnout</span>, co postavit.
en: I help teams <span class="fix">decide</span> what to build.

cs: Kód zlevnil. Shodnout se na zadání ne. Sednu si s těmi, kdo rozhodují, a <b class="hl">s AI máme hotové zadání za dny, ne týdny</b>.
en: Code got cheap. Agreeing on what to build did not. I sit down with your decision-makers, and <b class="hl">with AI, we have a finished spec in days, not weeks</b>.

cs: <a class="btn btn-fill" href="#/contact">Domluvit 30minutový hovor</a> <a class="btn btn-line" href="#/portfolio">Ukázky práce</a>
en: <a class="btn btn-fill" href="#/contact">Book a 30-minute call</a> <a class="btn btn-line" href="#/portfolio">See my work</a>

cs: tým se cyklí ve schůzkách
en: a team going in circles

cs: rozhodnuto, dohodnuto, zapsáno
en: decided, agreed, written down

cs: <span>tým se cyklí<br>ve schůzkách</span><span>rozhodnuto,<br>dohodnuto,<br>zapsáno</span>
en: <span>a team going<br>in circles</span><span>decided,<br>agreed,<br>written down</span>

cs: Kde jsem pracoval
en: Where I've worked

cs: Regulované krypto
en: Regulated crypto

cs: Bankovnictví
en: Banking

cs: Zdravotnictví
en: Healthcare

cs: E-shopy
en: E-commerce

cs: Energetika
en: Energy

cs: Bezpečnostní software
en: Security software

cs: Pracoval jsem pro
en: Clients I've worked for

cs: Kdy týmy potřebují moji pomoc
en: When teams call me

cs: Nejčastěji je to jedna z těchto situací.
en: It's usually one of these situations.

cs: Mluví se a mluví. Co dělat, všichni tuší. Nikdo to nechce vzít na sebe.
en: Lots of talk. Everyone senses what to do. Nobody wants to own the decision.

cs: Zadání se každý týden upravuje. Vývoj staví jen to jisté, nebo čeká.
en: The spec changes every week. Engineering builds only the safe parts, or waits.

cs: Každé oddělení má veto. Nikdo nemá celý seznam omezení.
en: Every department has a veto. Nobody has the full list of constraints.

cs: Rozhodovat je potřeba hned. Nový člověk nastoupí za půl roku.
en: Decisions are needed now. The new hire starts in 6 months.

cs: <span aria-hidden="true">Na workshopu vzniká<br><span class="tw"><span class="fix tw-w" data-words="business logika|user flow|customer journey">business logika</span><span class="tw-c"></span></span></span>
en: <span aria-hidden="true">The workshop produces<br><span class="tw"><span class="fix tw-w" data-words="business logic|user flows|a customer journey">business logic</span><span class="tw-c"></span></span></span>

cs: Rychle a s lidmi, kteří rozhodují.
en: Quickly, and with the people who decide.

cs: Místnost po workshopu. Varianty, lepítka a otevřené otázky na stěnách.
en: The room after a workshop. Options, sticky notes, and open questions on the walls.

cs: Pak z toho vznikne <span class="fix">funkční prototyp</span>.
en: Then it becomes a <span class="fix">working prototype</span>.

cs: Problém
en: Problem

cs: Řešení
en: Solution

cs: Formulář
en: Form

cs: Potvrzení
en: Confirmation

cs: Chyba?
en: Error?

cs: Hotovo
en: Done

cs: Oprava
en: Fix

cs: zpátky do formuláře
en: back to the form

cs: Od problému k business zadání: user flow, customer journey a prototyp, na který se dá kliknout.
en: From problem to business spec: user flows, a customer journey, and a clickable prototype.

cs: Přehrát znovu
en: Play again

cs: Od první schůzky k první verzi
en: From the first meeting to the first version

cs: V pondělí zmatek. Ve středu <span class="fix">rozhodnuto a nakresleno</span>.
en: Chaos on Monday. <span class="fix">Decided and drawn</span> by Wednesday.

cs: První workshop a ještě ten týden první verze, na kterou se dá kliknout.
en: The first workshop, and a clickable first version that same week.

cs: Předem
en: Before we start

cs: Definice problému, týmu a cíle
en: Define the problem, the team, and the goal

cs: Před spoluprací si s vámi ujasním, jaký problém řešíme, kdo o něm rozhoduje a čeho chceme dosáhnout.
en: Before we start, we agree on the problem we're solving, who decides, and what we want to achieve.

cs: Na první schůzce
en: At the first meeting

cs: Varianty kreslené během schůzky
en: Options sketched during the meeting

cs: Varianty řešíme už na první schůzce. Místo názorů pak vybíráte ze dvou nakreslených možností.
en: We work through options in the first meeting. Instead of debating opinions, you choose between 2 sketched alternatives.

cs: Druhý den
en: On day 2

cs: Jeden směr jako prototyp
en: One direction, as a prototype

cs: Funkční ukázka se skutečnými texty, i pro chvíle, kdy se něco pokazí. Co zůstane otevřené, má jméno a termín.
en: A working demo with real copy, including what happens when something goes wrong. Every open question gets an owner and a deadline.

cs: Potom
en: Afterward

cs: Funkční zadání, podle kterého staví vývoj
en: A functional spec that engineering builds from

cs: Každé rozhodnutí a jeho důvod. Jinak se za šest týdnů hádáte znovu.
en: Every decision and the reason behind it. Otherwise, you'll have the same argument again in 6 weeks.

cs: Jak to probíhá podrobně
en: See how it works in detail

cs: Vybrané případy
en: Selected case studies

cs: Rozhodnutí a jejich důvody.
en: Decisions and the reasons behind them.

cs: Vyberte ten, který se podobá vašemu problému.
en: Pick the one that's closest to your problem.

cs: Nový business směr za čtyři iterace
en: A new business direction in 4 iterations

cs: Nejdřív funkční prototyp, potom zadání.
en: Working prototype first, spec second.

cs: Otevřít případ
en: Read the case study

cs: Nejdřív design systém, potom nová identita
en: A design system first, then a new brand identity

cs: Rebranding spuštěn 1. 10. 2026.
en: Rebrand launched October 1, 2026.

cs: Jedna aplikace pro mnoho klinik
en: One app for many clinics

cs: Škálovatelný design systém, white label.
en: A scalable, white-label design system.

cs: Dvoudenní prioritizace business backlogu
en: Business backlog prioritization in 2 days

cs: Rozhodnuto na místě, nastavená strategie.
en: Decided on the spot, with a strategy in place.

cs: <a class="btn btn-line" href="#/portfolio">Všechny případy</a>
en: <a class="btn btn-line" href="#/portfolio">All case studies</a>

cs: Moje služby
en: Services

cs: <span class="fix">Tři způsoby</span>, jak spolupracovat.
en: <span class="fix">3 ways</span> to work together.

cs: od 49 000 Kč
en: From CZK 49,000

cs: Rozhodnutí, na které se dá kliknout. Jeden den, dva, nebo týden.
en: A decision you can click through. 1 day, 2 days, or a week.

cs: Jak to funguje
en: How it works

cs: nahrávka s komentářem
en: narrated recording

cs: co opravit dřív
en: what to fix first

cs: Audit rozhodnutí
en: Decision Audit

cs: od 29 000 Kč
en: From CZK 29,000

cs: Projdu váš produkt a na nahrávce obrazovky ukážu, co ho brzdí.
en: I review your product and show you, in a screen recording, what's holding it back.

cs: Po
en: Mo

cs: Út
en: Tu

cs: St
en: We

cs: Čt
en: Th

cs: Pá
en: Fr

cs: vedení
en: leadership

cs: směr
en: direction

cs: vývoj
en: engineering

cs: Vedení produktu a designu na část úvazku
en: Fractional product and design leadership

cs: od 120 000 Kč měsíčně
en: From CZK 120,000 per month

cs: Dva dny v týdnu ve vašem týmu. Pro firmy, které rozhodují každý týden.
en: 2 days a week on your team. For companies that make product decisions every week.

cs: <a class="btn btn-line" href="#/services">Porovnat všechny tři</a>
en: <a class="btn btn-line" href="#/services">Compare all 3</a>

cs: Další krok
en: Next step

cs: Kde jste se zasekli?
en: Where are you stuck?

cs: Napište mi. Na třicetiminutovém hovoru vám řeknu, jestli vám můžu pomoct. Bez prezentace a bez složitých nabídek.
en: Write to me. In a 30-minute call, I'll tell you whether I can help. No slide deck and no complicated proposals.

cs: <a class="btn btn-fill" href="#/contact">Domluvit 30minutový hovor</a>
en: <a class="btn btn-fill" href="#/contact">Book a 30-minute call</a>

# ---------- portfolio a reference
cs: Čtyři firmy. Čtyři zaseknuté produkty.
en: 4 companies. 4 stuck products.

cs: Reference
en: Recommendations

cs: <b>Ondřej Steklý</b>CPO, Coinmate<i>Stejný tým · 2026</i>
en: <b>Ondřej Steklý</b>CPO, Coinmate<i>Same team · 2026</i>

cs: <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/" target="_blank" rel="noopener">Celé doporučení na LinkedInu</a>
en: <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/" target="_blank" rel="noopener">Full recommendation on LinkedIn</a>

cs: <b>Václav Hruška</b>Creative Solutions Lead<i>Stejný tým · 2023</i>
en: <b>Václav Hruška</b>Creative Solutions Lead<i>Same team · 2023</i>

cs: <b>Michal Červenka</b>Director of Marketing, ESET<i>Klient · 2023</i>
en: <b>Michal Červenka</b>Director of Marketing, ESET<i>Client · 2023</i>

cs: <b>Petr Zátopek</b>CEO, EuroHealth Global Projects<i>Spolupráce v Leeaf · 2023</i>
en: <b>Petr Zátopek</b>CEO, EuroHealth Global Projects<i>Worked together at Leeaf · 2023</i>

cs: <b>Martin Fišera</b>CPO, Product Fruits<i>Klient · 2023</i>
en: <b>Martin Fišera</b>CPO, Product Fruits<i>Client · 2023</i>

cs: <b>Petr Tomíček</b>iOS Architect, Jablotron Cloud Services<i>Spolupráce v Leeaf · 2023</i>
en: <b>Petr Tomíček</b>iOS Architect, Jablotron Cloud Services<i>Worked together at Leeaf · 2023</i>

cs: <b>Lukáš Rykr</b>Freelance Product Designer<i>Můj přímý podřízený · 2023</i>
en: <b>Lukáš Rykr</b>Freelance Product Designer<i>Reported to me · 2023</i>

cs: <b>Lucie Krulich</b>Founder, Motionshift<i>Stejný tým · 2023</i>
en: <b>Lucie Krulich</b>Founder, Motionshift<i>Same team · 2023</i>

cs: <span class="ref-claim">&ldquo;he has consistently met deadlines and effectively managed his workload&rdquo;</span><span class="ref-by"><span class="ref-face ref-ini" aria-hidden="true">PN</span><span><b>Petr Neuhäuser</b>Klient<i>Klient · 2023</i></span></span>
en: <span class="ref-claim">&ldquo;he has consistently met deadlines and effectively managed his workload&rdquo;</span><span class="ref-by"><span class="ref-face ref-ini" aria-hidden="true">PN</span><span><b>Petr Neuhäuser</b>Client<i>Client · 2023</i></span></span>

cs: <b>Jiří Ostizlo</b>COO, Novatop<i>Stejný tým · 2023</i>
en: <b>Jiří Ostizlo</b>COO, Novatop<i>Same team · 2023</i>

cs: <span class="ref-claim">&ldquo;He also has ability to close on design requirements independently.&rdquo;</span><span class="ref-by"><span class="ref-face ref-ini" aria-hidden="true">DV</span><span><b>David Vitecek</b>Starší kolega<i>Spolupráce · 2014</i></span></span>
en: <span class="ref-claim">&ldquo;He also has ability to close on design requirements independently.&rdquo;</span><span class="ref-by"><span class="ref-face ref-ini" aria-hidden="true">DV</span><span><b>David Vitecek</b>Senior colleague<i>Worked together · 2014</i></span></span>

cs: <span class="ref-claim">Všechna doporučení jsou veřejně na LinkedInu.</span><span class="ref-li-go">Otevřít LinkedIn</span>
en: <span class="ref-claim">All recommendations are public on LinkedIn.</span><span class="ref-li-go">Open LinkedIn</span>

# ---------- případy: společné
cs: <a href="#/portfolio"><span>Všechny případy</span></a>
en: <a href="#/portfolio"><span>All case studies</span></a>

cs: <small>Krok</small><span>Rozsah s vedením</span>
en: <small>Step</small><span>Scope with leadership</span>

cs: Výchozí stav
en: Starting point

cs: Co jsem udělal
en: What I did

cs: Jak to dopadlo
en: Outcome

cs: Rozhodnutí, rizika a co to stálo vám ukážu na hovoru. Potom vám pošlu odkaz a heslo k celému případu.
en: I'll walk you through the decisions, risks, and costs on a call. Afterward, I'll send you a link and a password to the full case study.

cs: Další případy
en: More case studies

# ---------- Heirloom
cs: Heirloom &middot; 2026 &middot; Digitální dědictví, nový produkt od nuly
en: Heirloom &middot; 2026 &middot; Digital legacy, a new product from scratch

cs: Nový <span class="fix">business směr</span> za čtyři iterace.
en: A new <span class="fix">business direction</span> in 4 iterations.

cs: <b>Moje role</b> Zakládající designér &middot; tým osmi lidí na dálku, bez produktového manažera
en: <b>My role</b> Founding designer &middot; remote team of 8, with no product manager

cs: <small>Kde se to zaseklo</small><span>Čekaly se obrazovky ve Figmě</span>
en: <small>Where it was stuck</small><span>Everyone expected Figma screens</span>

cs: <small>Krok</small><span>AI prototyp z vašeho kódu</span>
en: <small>Step</small><span>AI prototype from your codebase</span>

cs: <small>Krok</small><span>Rychlé iterace s komentáři</span>
en: <small>Step</small><span>Fast iterations with comments</span>

cs: <small>Výsledek</small><span>Nový směr za čtyři sezení</span>
en: <small>Result</small><span>New direction in 4 sessions</span>

cs: Firma měnila směr a potřebovala přesně zjistit rozsah produktu a zadání. Čekaly se obrazovky ve Figmě. Postavil jsem místo toho postup, kde je v každé iteraci funkční prototyp.
en: The company was changing direction and needed to pin down the product scope and spec. Everyone expected screens in Figma. Instead, I set up a process with a working prototype in every iteration.

cs: <b>Rozsah s vedením.</b> Facilitoval jsem otázky, ze kterých vyšel rozsah projektu. <b>AI prototyp z vašeho kódu.</b> Prototyp vznikl z existujícího repozitáře a design systému. <b>Rychlé iterace s komentáři.</b> Komentáře přímo v prototypu. Měl všechny stavy a pokryl i okrajové případy.
en: <b>Scope with leadership.</b> I facilitated the questions that defined the project scope. <b>AI prototype from your codebase.</b> The prototype was built from the existing repository and design system. <b>Fast iterations with comments.</b> Comments went directly into the prototype. It covered every state, including edge cases.

cs: Spory, které dřív přišly až s vývojem, jsme vyřešili už při prototypování. Nový směr jsme od začátku do konce uzavřeli za čtyři sezení.
en: Disagreements that used to surface during development were settled during prototyping. We closed the new direction, start to finish, in 4 sessions.

# ---------- Coinmate
cs: Coinmate &middot; 2023&ndash;2026 &middot; Regulovaná kryptoburza
en: Coinmate &middot; 2023&ndash;2026 &middot; Regulated crypto exchange

cs: Nejdřív <span class="fix">design systém</span>, potom nová identita.
en: A <span class="fix">design system</span> first, then a new brand identity.

cs: <b>Moje role</b> Externě, dva dny v týdnu &middot; vedl jsem seniorního designéra a copywritera
en: <b>My role</b> External, 2 days a week &middot; led a senior designer and a copywriter

cs: <small>Kde se to zaseklo</small><span>Bez design systému</span>
en: <small>Where it was stuck</small><span>No design system</span>

cs: <small>Krok</small><span>Škálovatelný design systém</span>
en: <small>Step</small><span>A scalable design system</span>

cs: <small>Krok</small><span>Jeden systém pro iOS i Android</span>
en: <small>Step</small><span>One system for iOS and Android</span>

cs: <small>Krok</small><span>Trh i banky</span>
en: <small>Step</small><span>Exchanges and banks</span>

cs: <small>Výsledek</small><span>Nová identita na stejném systému</span>
en: <small>Result</small><span>A new brand on the same system</span>

cs: Firma neměla design systém ani produktové designové oddělení. Systém jsem postavil jako první. Když přišel požadavek na rebrand, hledání trvalo dny místo týdnů a mohli jsme testovat víc konceptů místo jednoho.
en: The company had no design system and no product design team. I built the system first. When the rebrand request came, the exploration took days instead of weeks, and we could test several concepts instead of one.

cs: <b>Škálovatelný design systém.</b> Vycházel z existujícího stylu, takže nic nezačínalo od nuly. <b>Jeden systém pro iOS i Android.</b> Mobilní aplikace dostaly stejný systém, aby uživatelé značku poznali všude. <b>Trh i banky.</b> Analyzoval jsem kryptoburzy i banky, které začínají s kryptem. Pak jsem vybral nejsložitější obrazovky pro mobil i desktop, aby se dalo škálovat.
en: <b>A scalable design system.</b> It built on the existing style, so nothing started from scratch. <b>One system for iOS and Android.</b> The mobile apps got the same system, so users recognize the brand everywhere. <b>Exchanges and banks.</b> I analyzed crypto exchanges and banks that are starting to offer crypto. Then I designed the most complex screens for mobile and desktop first, to make sure the system would scale.

cs: Design systém zůstal a stojí na něm nová identita: nové logo a barvy, jméno zůstalo. Za vizuální stránku jsem odpovídal já.
en: The design system stayed, and the new brand identity is built on it: a new logo and colors, the same name. I was responsible for the visual design.

cs: <b>Ondřej Steklý</b>CPO, Coinmate<i>Stejný tým &middot; 2026</i>
en: <b>Ondřej Steklý</b>CPO, Coinmate<i>Same team &middot; 2026</i>

# ---------- Leeaf
cs: Leeaf &middot; 2020&ndash;2023 &middot; Zdravotnictví, léčba neplodnosti
en: Leeaf &middot; 2020&ndash;2023 &middot; Healthcare, fertility treatment

cs: <span class="fix">Jedna aplikace</span> pro mnoho klinik.
en: <span class="fix">One app</span> for many clinics.

cs: <b>Moje role</b> Vedoucí produktového designu &middot; dva designéři
en: <b>My role</b> Head of product design &middot; team of 2 designers

cs: <small>Kde se to zaseklo</small><span>Kopie pro každou kliniku</span>
en: <small>Where it was stuck</small><span>A separate copy for every clinic</span>

cs: <small>Krok</small><span>Jeden systém od začátku</span>
en: <small>Step</small><span>One system from the start</span>

cs: <small>Krok</small><span>Tokeny a proměnné</span>
en: <small>Step</small><span>Tokens and variables</span>

cs: <small>Krok</small><span>Nová klinika je konfigurace</span>
en: <small>Step</small><span>A new clinic is a configuration</span>

cs: <small>Výsledek</small><span>Další kliniky běžely beze mě</span>
en: <small>Result</small><span>More clinics launched without me</span>

cs: Aplikace se měla prodávat jako white label dalším klinikám. Plán byl pokaždé ji přizpůsobit klientovi. Udělal jsem místo toho jeden systém, který jde snadno zopakovat: změní se barvy, písma a logo a napojí se na portál kliniky.
en: The app was meant to be sold to other clinics as a white-label product. The plan was to customize it for each client. Instead, I built one system that's easy to replicate: change the colors, fonts, and logo, and connect it to the clinic's portal.

cs: <b>Jeden systém od začátku.</b> Stejný design systém pro web, portál pro lékaře a mobilní aplikaci. <b>Tokeny a proměnné.</b> Barvy, písma a logo jsou nastavení, ne nové návrhy. <b>Nová klinika je konfigurace.</b> Nastaví se v administraci a vydá na App Store a Google Play.
en: <b>One system from the start.</b> The same design system for the website, the doctors' portal, and the mobile app. <b>Tokens and variables.</b> Colors, fonts, and the logo are settings, not new designs. <b>A new clinic is a configuration.</b> It's set up in the admin and published to the App Store and Google Play.

cs: Na stejném systému pak běžely další kliniky IVF. Designéři je brandovali beze mě.
en: More IVF clinics then ran on the same system. Designers branded them without me.

cs: <b>Petr Tomíček</b>iOS Architect, Jablotron Cloud Services<i>Spolupráce v Leeaf &middot; 2023</i>
en: <b>Petr Tomíček</b>iOS Architect, Jablotron Cloud Services<i>Worked together at Leeaf &middot; 2023</i>

# ---------- BRENO
cs: BRENO &middot; 2023 &middot; Maloobchod a e-shopy
en: BRENO &middot; 2023 &middot; Retail and e-commerce

cs: Dvoudenní <span class="fix">prioritizace</span> business backlogu.
en: Business backlog <span class="fix">prioritization</span> in 2 days.

cs: <b>Moje role</b> Workshop jsem navrhl, vedl a facilitoval &middot; přes WPP
en: <b>My role</b> Designed, led, and facilitated the workshop &middot; through WPP

cs: <small>Kde se to zaseklo</small><span>Všechno mělo vysokou prioritu</span>
en: <small>Where it was stuck</small><span>Everything was high priority</span>

cs: <small>Krok</small><span>Co firma opravdu potřebuje</span>
en: <small>Step</small><span>What the business really needs</span>

cs: <small>Krok</small><span>Role a pořadí</span>
en: <small>Step</small><span>Roles and order</span>

cs: <small>Krok</small><span>Jak pracovat dál</span>
en: <small>Step</small><span>How to keep working</span>

cs: <small>Výsledek</small><span>Shoda na pořadí priorit</span>
en: <small>Result</small><span>Agreement on priorities</span>

cs: Klient měl dlouhý seznam úkolů bez priorit a nedokázal se shodnout na pořadí, protože všechno bylo důležité. Workshop jsem navrhl, vedl a sestavil z něj prioritizaci i s argumenty.
en: The client had a long, unprioritized task list and couldn't agree on the order, because everything was important. I designed and led the workshop, and turned its output into a prioritized list, with the reasoning for each item.

cs: <b>Co firma opravdu potřebuje.</b> Zjistil jsem hlavní potřeby byznysu a dal všem na stůl priority, které měl každý zapsané jen u sebe. <b>Role a pořadí.</b> Každý chtěl něco jiného. Zastavoval jsem diskusi a vedl k pořadí, na kterém se shodli. <b>Jak pracovat dál.</b> Poradil jsem, jak pracovat s backlogem, roadmapou a novými funkcemi, a vysvětlil celý cyklus vývoje produktu.
en: <b>What the business really needs.</b> I identified the core business needs and put everyone's priorities on the table, including the ones people had only written down for themselves. <b>Roles and order.</b> Everyone wanted something different. I stopped circular discussions and guided the group to an order everyone agreed on. <b>How to keep working.</b> I advised on managing the backlog, the roadmap, and new features, and explained the full product development cycle.

cs: Vedení, vývoj i marketing se shodli na pořadí priorit a dalších úkolů. WPP na tom postavilo další zakázky.
en: Leadership, engineering, and marketing agreed on the order of priorities and next tasks. WPP built further projects on this work.

cs: <b>Václav Hruška</b>Creative Solutions Lead<i>Stejný tým &middot; 2023</i>
en: <b>Václav Hruška</b>Creative Solutions Lead<i>Same team &middot; 2023</i>

# ---------- služby
cs: Jeden den, dva, nebo týden
en: 1 day, 2 days, or a week

cs: Podrobnosti
en: Details

cs: Pět pracovních dní, bez schůzek
en: 5 business days, no meetings

cs: Vedení produktu na část úvazku
en: Fractional product leadership

cs: Dva dny v týdnu, nejméně tři měsíce
en: 2 days a week, for at least 3 months

cs: Třicet minut, bez prezentace. V Praze, v Amsterdamu nebo online.
en: 30 minutes, no slide deck. In Prague, in Amsterdam, or online.

cs: Jeden den, dva dny, nebo týden
en: 1 day, 2 days, or a week

cs: Rozhodnutí, na které se dá kliknout. Přinesete nerozhodnutou věc, odnesete rozhodnutí a funkční prototyp na webu, podle kterého se dá stavět.
en: A decision you can click through. You bring an open question. You leave with a decision and a working prototype on the web that engineering can build from.

cs: Délka
en: Duration

cs: <span><b>Jeden den</b> &middot; od 49 000 Kč &middot; jeden workshop a první verze prototypu</span>
en: <span><b>1 day</b> &middot; from CZK 49,000 &middot; 1 workshop and a first version of the prototype</span>

cs: <span><b>Dva dny</b> &middot; od 125 000 Kč &middot; jedna nerozhodnutá věc, dotažená do konce</span>
en: <span><b>2 days</b> &middot; from CZK 125,000 &middot; 1 open question, resolved end to end</span>

cs: <span><b>Týden</b> &middot; od 220 000 Kč &middot; celá oblast produktu, víc rozhovorů a workshopů</span>
en: <span><b>1 week</b> &middot; from CZK 220,000 &middot; an entire product area, with more interviews and workshops</span>

cs: Co dostanete
en: What you get

cs: <span>Problém, lidé a cíl sepsané předem</span>
en: <span>The problem, the people, and the goal, written up in advance</span>

cs: <span>Workshop s lidmi, kteří rozhodují</span>
en: <span>A workshop with your decision-makers</span>

cs: <span>Funkční prototyp na webu, s heslem a komentáři</span>
en: <span>A working prototype on the web, password-protected, with comments</span>

cs: <span>Zápis: co jsme rozhodli a proč</span>
en: <span>A decision log: what we decided and why</span>

cs: <b>Pro vás, pokud</b> dostanete ty, kdo rozhodují, aspoň na den do jedné místnosti.
en: <b>Right for you if</b> you can get your decision-makers in one room for at least a day.

cs: Pět pracovních dní &middot; bez schůzek
en: 5 business days &middot; no meetings

cs: Projdu váš produkt a na nahrávce obrazovky ukážu, co ho brzdí. Nejlevnější způsob, jak zjistit, jestli spolu pracovat.
en: I review your product and show you, in a screen recording, what's holding it back. The least expensive way to find out whether we should work together.

cs: <span>Nahrávka obrazovky s komentářem</span>
en: <span>A narrated screen recording</span>

cs: <span>Co nefunguje, v pořadí, v jakém bych to opravoval</span>
en: <span>What isn't working, in the order I'd fix it</span>

cs: <span>Doporučení: já, nový člověk, nebo nikdo</span>
en: <span>A recommendation: me, a new hire, or no one</span>

cs: <b>Pro vás, pokud</b> víte, že je něco špatně, a neshodnete se na příčině.
en: <b>Right for you if</b> you know something is wrong but can't agree on the cause.

cs: Dva dny v týdnu &middot; nejméně tři měsíce
en: 2 days a week &middot; at least 3 months

cs: Produktová role ve vašem týmu. Pro firmy, které rozhodují každý týden.
en: A product leadership role on your team. For companies that make decisions every week.

cs: <span>Sedím u porad vedení i produktu</span>
en: <span>I join both leadership and product meetings</span>

cs: <span>Rozsah dohodnutý dřív, než začne vývoj</span>
en: <span>Scope agreed before development starts</span>

cs: <span>Schvalujete prototyp, ne dokument</span>
en: <span>You approve a prototype, not a document</span>

cs: <span>Písemné předání, až přijmete někoho natrvalo</span>
en: <span>A written handover when you hire someone permanently</span>

cs: <b>Pro vás, pokud</b> tu roli potřebujete hned a nábor potrvá měsíce.
en: <b>Right for you if</b> you need the role filled now, and hiring will take months.

cs: Otázky
en: Questions

cs: Než se objednáte.
en: Before you book.

cs: <span>Kolik to stojí?</span>
en: <span>How much does it cost?</span>

cs: Platíte za projekt, ne za hodiny. Audit od 29 000 Kč, Decision Prototype od 49 000 Kč, část úvazku od 120 000 Kč měsíčně.
en: You pay per project, not per hour. Decision Audit from CZK 29,000, Decision Prototype from CZK 49,000, fractional leadership from CZK 120,000 per month.

cs: <span>Nabízíte balíčky?</span>
en: <span>Do you offer packages?</span>

cs: Ano, tři výše. Když se nehodí ani jeden, upravím rozsah. Sazbu ne.
en: Yes, the 3 above. If none of them fits, I'll adjust the scope, but not the rate.

cs: <span>Jak poznám, co se hodí pro mě?</span>
en: <span>How do I know which one is right for me?</span>

cs: Napište mi, kde jste se zasekli. Na třicetiminutovém hovoru vám řeknu, co dává smysl. Klidně i to, že nic z toho.
en: Tell me where you're stuck. In a 30-minute call, I'll tell you what makes sense, even if the answer is none of the above.

cs: <span>Pracujete s malými firmami, nebo jen s velkými?</span>
en: <span>Do you work with small companies, or only large ones?</span>

cs: Obojí. Rozhoduje, jestli je co rozhodnout a jestli u stolu sedí někdo, kdo o tom smí rozhodnout.
en: Both. What matters is whether there's a real decision to make, and whether someone at the table has the authority to make it.

# ---------- Decision Prototype
cs: <a href="#/services"><span>Všechny služby</span></a>
en: <a href="#/services"><span>All services</span></a>

cs: Decision Prototype &middot; Rozhodnutí, na které se dá kliknout
en: Decision Prototype &middot; A decision you can click through

cs: <span class="fix">Funkční prototyp</span> za pár dní.
en: A <span class="fix">working prototype</span> in a few days.

cs: Sednu si s tím, kdo má zadání v hlavě, a doptám se, dokud není jasné, jak má služba fungovat. Pak z toho udělám funkční prototyp na webu. S týmem ho proklikáme, okomentujeme a posuneme se dál.
en: I sit down with the person who has the requirements in their head and ask questions until it's clear how the service should work. Then I turn that into a working prototype on the web. Your team clicks through it, comments, and moves forward.

cs: <a class="btn btn-fill" href="#/contact/decision-prototype">Domluvit 30minutový hovor</a><a class="btn btn-line" href="#/services">Ceny a podmínky</a>
en: <a class="btn btn-fill" href="#/contact/decision-prototype">Book a 30-minute call</a><a class="btn btn-line" href="#/services">Pricing and terms</a>

cs: Dva týdny schůzek. Nic, na co by se dalo kliknout nebo co by šlo vyzkoušet.
en: 2 weeks of meetings. Nothing to click or test.

cs: Na schůzce se všichni shodnou. Vývoj přesto čeká, protože rozhodnutí zůstalo v hlavách a prezentacích.
en: Everyone agrees in the meeting. Engineering still waits, because the decision lives in people's heads and slide decks.

cs: Každé kolo začíná<br><span class="tw"><span class="fix tw-loop" data-words="iterací|workshopem|rozhovorem">iterací</span><span class="tw-c"></span></span>
en: Every round starts<br><span class="tw"><span class="fix tw-loop" data-words="with an iteration|with a workshop|with an interview">with an iteration</span><span class="tw-c"></span></span>

cs: Tým se dohaduje nad funkčním prototypem, ne nad slajdy nebo na další schůzce.
en: The team discusses a working prototype, not slides or another meeting.

cs: ZAČÁTEK
en: START

cs: PRÁCE
en: WORK

cs: CO DOSTANETE
en: WHAT YOU GET

cs: Řízená kola úprav
en: Managed rounds of changes

cs: byznys + vývoj · změny
en: business + engineering · changes

cs: Hotový produkt
en: Existing product

cs: repozitář · návrhy
en: repository · designs

cs: Nový nápad
en: New idea

cs: zatím bez produktu
en: no product yet

cs: Probrat
en: Talk it

cs: to spolu
en: through

cs: řízená diskuse
en: facilitated discussion

cs: Kdo rozhoduje
en: Who decides

cs: Otázky místo slajdů
en: Questions, not slides

cs: Proces služby živě
en: The process, live

cs: Zmapovat
en: Map

cs: službu
en: the service

cs: mapa navigace
en: navigation map

cs: Obrazovky a role
en: Screens and roles

cs: Co je v rozsahu
en: What's in scope

cs: Postavit
en: Build

cs: obrazovky
en: the screens

cs: výstupy
en: outputs

cs: Logika služby
en: Service logic

cs: Průchody
en: User flows

cs: Obrazovky a stavy
en: Screens and states

cs: Dokumentace
en: Documentation

cs: Sdílet
en: Share

cs: jeden odkaz
en: one link

cs: nasazený prototyp
en: deployed prototype

cs: Nasazený prototyp
en: Deployed prototype

cs: Komentáře
en: Comments

cs: Verze
en: Versions

cs: Z vašich skutečných komponent a tokenů.
en: Built from your real components and tokens.

cs: Není to produkční kód. Vývoj podle něj staví, až je rozhodnuto.
en: It's not production code. Engineering builds from it once decisions are made.

cs: Rozhodnutý
en: Decided

cs: rozsah
en: scope

cs: první verze · průchody
en: first version · flows

cs: zápis rozhodnutí
en: decision log

cs: Podklad
en: Handoff

cs: pro vývoj
en: for engineering

cs: stavy · tokeny
en: states · tokens

cs: <span class="fix">Tři věci</span>, které vám zůstanou.
en: <span class="fix">3 things</span> you keep.

cs: Rozhodnutý rozsah
en: A decided scope

cs: Co patří do první verze, které průchody jsou důležité a proč jste se tak rozhodli.
en: What goes into the first version, which flows matter, and why you decided that way.

cs: Jeden odkaz pro všechny
en: One link for everyone

cs: Prototyp na internetu, chráněný heslem. Každý ho otevře v prohlížeči a ke každé obrazovce napíše komentář.
en: A password-protected prototype on the web. Anyone can open it in a browser and comment on any screen.

cs: Podklad, podle kterého staví vývoj
en: A handoff that engineering builds from

cs: Mapa obrazovek, všechny stavy a vaše skutečné barvy a komponenty.
en: A screen map, every state, and your real colors and components.

cs: Délka a cena
en: Duration and price

cs: Jeden den, dva, nebo týden.
en: 1 day, 2 days, or a week.

cs: Jeden den
en: 1 day

cs: <b>Jedna otázka.</b> Workshop a první verze, na kterou se dá kliknout.
en: <b>1 question.</b> A workshop and a clickable first version.

cs: Dva dny
en: 2 days

cs: od 125 000 Kč
en: From CZK 125,000

cs: <b>Jedna nerozhodnutá věc.</b> Workshop, prototyp a zápis. Dotažené do konce.
en: <b>1 open question.</b> A workshop, a prototype, and a decision log. Resolved end to end.

cs: Týden
en: 1 week

cs: od 220 000 Kč
en: From CZK 220,000

cs: <b>Celá oblast produktu.</b> Víc rozhovorů, workshopů a obrazovek. Postup je stejný.
en: <b>An entire product area.</b> More interviews, workshops, and screens. Same process.

cs: V každé délce
en: Included in every option

cs: Problém, lidé a cíl sepsané předem
en: The problem, the people, and the goal, written up in advance

cs: Workshop s lidmi, kteří rozhodují
en: A workshop with your decision-makers

cs: Funkční prototyp na webu, s heslem a komentáři
en: A working prototype on the web, password-protected, with comments

cs: Zápis: co jsme rozhodli a proč
en: A decision log: what we decided and why

cs: Cenu ovlivní
en: What affects the price

cs: Rozsah
en: Scope

cs: Složitost
en: Complexity

cs: Velikost produktu
en: Product size

cs: Platíte za projekt, ne za hodiny. Konečnou nabídku pošlu po první schůzce.
en: You pay per project, not per hour. I'll send a final quote after our first meeting.

cs: <a class="btn btn-fill" href="#/contact/decision-prototype">Domluvit 30minutový hovor</a>
en: <a class="btn btn-fill" href="#/contact/decision-prototype">Book a 30-minute call</a>

cs: V praxi
en: In practice

cs: <span class="fix">Jeden postup</span>, dvě firmy.
en: <span class="fix">One process</span>, 2 companies.

cs: Coinmate &middot; Regulovaná kryptoburza
en: Coinmate &middot; Regulated crypto exchange

cs: Kde to začalo
en: Where it started

cs: Tady jsem poprvé viděl, jak rychle AI prototypuje. Jeden odkaz s heslem a tým mohl hned testovat. Z týdnů na dny.
en: This is where I first saw how fast AI can prototype. One password-protected link, and the team could test right away. From weeks to days.

cs: Heirloom &middot; Digitální dědictví
en: Heirloom &middot; Digital legacy

cs: Kde jsem šel dál
en: Where I took it further

cs: Změnu směru bylo potřeba přesně popsat. Prototypy přímo nad produkčním repozitářem. Uzavřeno zhruba za čtyři sezení.
en: The change in direction had to be defined precisely. Prototypes were built directly on the production repository. Closed in about 4 sessions.

cs: Pro CTO a architekta
en: For CTOs and architects

cs: Otázky, které položíte.
en: Questions you'll ask.

cs: <span>Sahá to na náš produkční kód?</span>
en: <span>Does it touch our production code?</span>

cs: Ne. Používá vaše komponenty, ale produkční kód to není. Vývoj podle něj staví až po rozhodnutí.
en: No. It uses your components, but it isn't production code. Engineering builds from it only after decisions are made.

cs: <span>Kde to běží?</span>
en: <span>Where does it run?</span>

cs: Na GitHubu, za odkazem s heslem.
en: On GitHub, behind a password-protected link.

cs: <span>Komu to potom patří?</span>
en: <span>Who owns it afterward?</span>

cs: Vám. Pokud jsem repozitář založil u sebe, převedu ho na vás.
en: You do. If I created the repository under my account, I'll transfer it to you.

cs: <span>Co od nás potřebujete?</span>
en: <span>What do you need from us?</span>

cs: Hlavně čas toho, kdo rozhoduje. Přístup k repozitáři nebo design systému pomůže, pokud to vaše bezpečnostní pravidla dovolí.
en: Mainly time with your decision-maker. Access to your repository or design system helps, if your security policies allow it.

cs: Další způsoby spolupráce
en: Other ways to work together

cs: Dva dny v týdnu ve vašem týmu.
en: 2 days a week on your team.

cs: Co váš produkt brzdí, na jedné nahrávce.
en: What's holding your product back, in one recording.

# ---------- vedení produktu na část úvazku
cs: Vedení produktu a designu &middot; na část úvazku
en: Product and design leadership &middot; part-time

cs: <span class="fix">Vedení produktu</span>, dokud nenajdete stálého člověka.
en: A <span class="fix">product lead</span> until you hire one.

cs: Dva dny v týdnu sedím ve vašem týmu. Rozhoduju s vámi u porad vedení i produktu a držím směr, aby se vývoj necyklil.
en: 2 days a week, I work as part of your team. I make decisions with you in leadership and product meetings and keep the direction steady, so engineering doesn't go in circles.

cs: <a class="btn btn-fill" href="#/contact/fractional">Domluvit 30minutový hovor</a><a class="btn btn-line" href="#/services">Ceny a podmínky</a>
en: <a class="btn btn-fill" href="#/contact/fractional">Book a 30-minute call</a><a class="btn btn-line" href="#/services">Pricing and terms</a>

cs: Rozhodnutí čekají na člověka, který ještě nenastoupil.
en: Decisions are waiting for someone who hasn't started yet.

cs: Nábor trvá měsíce. Vývoj mezitím staví podle toho, kdo zrovna mluví nejhlasitěji.
en: Hiring takes months. Meanwhile, engineering builds whatever the loudest person in the room asks for.

cs: <span class="fix">Tři věci</span>, které se změní.
en: <span class="fix">3 things</span> that change.

cs: Jasný směr každý týden
en: Clear direction every week

cs: Priority na další týden, dohodnuté s vedením i s vývojem.
en: Next week's priorities, agreed with leadership and engineering.

cs: Rozsah dřív, než se staví
en: Scope before anything gets built

cs: Vývoj dostane zadání, které se v půlce práce nemění.
en: Engineering gets a spec that doesn't change halfway through.

cs: Prototyp místo dokumentu
en: A prototype instead of a document

cs: Schvalujete funkční prototyp na webu, ne další prezentaci.
en: You approve a working prototype on the web, not another slide deck.

cs: Jak to probíhá
en: How it works

cs: Od prvního týdne po předání.
en: From week 1 to handover.

cs: První týden
en: Week 1

cs: Seznámení
en: Onboarding

cs: Projdu produkt, data a lidi. Sepíšu, co je rozhodnuté a co ne.
en: I review the product, the data, and the people. I write down what's decided and what isn't.

cs: Každý týden
en: Every week

cs: Dva dny s týmem
en: 2 days with the team

cs: Porady, workshopy, prototypy. Každé velké rozhodnutí zapíšu i s důvodem.
en: Meetings, workshops, prototypes. I document every major decision, with the reason behind it.

cs: Na konci
en: At the end

cs: Předání
en: Handover

cs: Až přijmete někoho natrvalo, předám mu všechno písemně.
en: When you hire someone permanently, I hand everything over in writing.

cs: <span class="op-label">Cena</span><b class="op-amount">od 120 000 Kč měsíčně</b><span class="op-term">Dva dny v týdnu · nejméně tři měsíce</span><a class="btn btn-fill" href="#/contact/fractional">Domluvit 30minutový hovor</a>
en: <span class="op-label">Price</span><b class="op-amount">From CZK 120,000 per month</b><span class="op-term">2 days a week · at least 3 months</span><a class="btn btn-fill" href="#/contact/fractional">Book a 30-minute call</a>

cs: V ceně
en: Included

cs: Sedím u porad vedení i produktu
en: I join both leadership and product meetings

cs: Rozsah dohodnutý dřív, než začne vývoj
en: Scope agreed before development starts

cs: Schvalujete prototyp, ne dokument
en: You approve a prototype, not a document

cs: Písemné předání, až přijmete někoho natrvalo
en: A written handover when you hire someone permanently

cs: Velikost týmu
en: Team size

cs: Konečnou nabídku pošlu po první schůzce.
en: I'll send a final quote after our first meeting.

cs: <span class="fix">Dva dny v týdnu</span> v Coinmate.
en: <span class="fix">2 days a week</span> at Coinmate.

cs: Externě, dva dny v týdnu. Design systém od nuly, specifikace frontendu, podklady pro licenci MiCA a nová značka.
en: External, 2 days a week. A design system from scratch, front-end specs, documentation for the MiCA license, and a new brand.

cs: <a class="btn btn-fill" href="#/contact/fractional">Domluvit 30minutový hovor</a>
en: <a class="btn btn-fill" href="#/contact/fractional">Book a 30-minute call</a>

# ---------- audit
cs: Zjistěte, co váš produkt <span class="fix">brzdí</span>. Za pět dní.
en: Find out what's <span class="fix">holding back</span> your product. In 5 days.

cs: Projdu váš produkt a na nahrávce obrazovky ukážu, co nefunguje a v jakém pořadí bych to opravoval. Bez schůzek.
en: I review your product and show you, in a screen recording, what isn't working and the order I'd fix it in. No meetings.

cs: <a class="btn btn-fill" href="#/contact/audit">Domluvit 30minutový hovor</a><a class="btn btn-line" href="#/services">Ceny a podmínky</a>
en: <a class="btn btn-fill" href="#/contact/audit">Book a 30-minute call</a><a class="btn btn-line" href="#/services">Pricing and terms</a>

cs: Víte, že je něco špatně. Neshodnete se, co.
en: You know something is wrong. You can't agree on what.

cs: Každé oddělení vidí jinou příčinu. Audit dá všem stejný podklad.
en: Every department sees a different cause. The audit gives everyone the same evidence.

cs: <span class="fix">Tři věci</span> za pět dní.
en: <span class="fix">3 things</span> in 5 days.

cs: Nahrávka obrazovky
en: A screen recording

cs: Projdu produkt jako uživatel a komentuju, co vidím. Pustíte si ji celým týmem.
en: I go through the product as a user and narrate what I see. You can watch it with your whole team.

cs: Seznam podle priority
en: A prioritized list

cs: Co nefunguje, v pořadí, v jakém bych to opravoval.
en: What isn't working, in the order I'd fix it.

cs: Doporučení
en: A recommendation

cs: Jestli to vyřeším já, nový člověk, nebo nikdo.
en: Whether it should be me, a new hire, or no one.

cs: Pět pracovních dní.
en: 5 business days.

cs: Den 1
en: Day 1

cs: Přístupy a otázky
en: Access and questions

cs: Pošlete mi přístup k produktu a pár vět o tom, co vás trápí.
en: Send me access to the product and a few sentences about what's bothering you.

cs: Dny 2 až 4
en: Days 2–4

cs: Průchod produktem
en: Product walkthrough

cs: Procházím, nahrávám a píšu.
en: I go through the product, record, and write.

cs: Den 5
en: Day 5

cs: Dostanete nahrávku a seznam. Když chcete, probereme to na půlhodinovém hovoru.
en: You get the recording and the list. If you want, we can discuss it in a 30-minute call.

cs: <span class="op-label">Cena</span><b class="op-amount">od 29 000 Kč</b><span class="op-term">Pět pracovních dní · bez schůzek</span><a class="btn btn-fill" href="#/contact/audit">Domluvit 30minutový hovor</a>
en: <span class="op-label">Price</span><b class="op-amount">From CZK 29,000</b><span class="op-term">5 business days · no meetings</span><a class="btn btn-fill" href="#/contact/audit">Book a 30-minute call</a>

cs: Nahrávka obrazovky s komentářem
en: A narrated screen recording

cs: Co nefunguje, v pořadí, v jakém bych to opravoval
en: What isn't working, in the order I'd fix it

cs: Doporučení: já, nový člověk, nebo nikdo
en: A recommendation: me, a new hire, or no one

cs: Půlhodinový hovor nad výsledkem, když chcete
en: A 30-minute call about the results, if you want one

cs: Počet průchodů, které projdu
en: Number of flows I review

cs: Konečnou nabídku pošlu, až uvidím produkt.
en: I'll send a final quote once I've seen the product.

cs: Proč začít tady
en: Why start here

cs: Nejlevnější způsob, jak zjistit, jestli spolu pracovat.
en: The least expensive way to find out whether we should work together.

cs: Když se ukáže, že potřebujete víc, víte přesně co. Když ne, máte seznam a můžete začít sami.
en: If it turns out you need more, you'll know exactly what. If not, you have the list and can start on your own.

cs: <a class="btn btn-fill" href="#/contact/audit">Domluvit 30minutový hovor</a>
en: <a class="btn btn-fill" href="#/contact/audit">Book a 30-minute call</a>

# ---------- o mně
cs: <span class="fix">Třináct let</span> dovádím týmy k <span class="fix">rozhodnutí</span>.
en: <span class="fix">13 years</span> of guiding teams to <span class="fix">decisions</span>.

cs: Praha a Amsterdam. Přicházím tam, kde se o produktu ještě nerozhodlo, nebo kde se tým cyklí a potřebuje se pohnout dál.
en: Prague and Amsterdam. I come in where product decisions haven't been made yet, or where a team is going in circles and needs to move forward.

cs: Pavel<small>Definice produktu</small>
en: Pavel<small>Product definition</small>

cs: Jak pracuju
en: How I work

cs: Vedu diskusi a zároveň kreslím.
en: I lead the discussion and sketch at the same time.

cs: Na jednom sezení udržím celek i detail.
en: In a single session, I keep track of both the big picture and the details.

cs: Mezi sezeními píšu. Radši pošlu návrh než pozvánku na schůzku.
en: Between sessions, I write. I'd rather send a draft than a meeting invite.

cs: Vizuál řídím, pixely kreslí designér.
en: I direct the visual design. A designer draws the pixels.

cs: Každé velké rozhodnutí zapíšu i s důvodem. Jinak se k němu vracíme.
en: I write down every major decision with its reason. Otherwise, we keep coming back to it.

cs: S kým mi to jde
en: Who I work best with

cs: S lidmi, kterým jde o výsledek víc než o to mít pravdu.
en: People who care more about the result than about being right.

cs: S týmy, kde chyba něco stojí. Regulátor, licence, zdraví, něčí úspory.
en: Teams where mistakes are costly: regulators, licenses, health, people's savings.

cs: Se zakladateli, kteří přijdou osobně.
en: Founders who show up in person.

cs: Na čem mi záleží
en: What I care about

cs: Řešíme skutečný problém. Když je vyřešený, jdeme dál.
en: We solve the real problem. Once it's solved, we move on.

cs: Výsledek se počítá. Lidi, kteří na něm pracují, taky.
en: The result counts. So do the people who work on it.

cs: Ať to víte hned
en: So you know up front

cs: Co nejsem
en: What I'm not

cs: Nejsem produktový manažer přes metriky. Uzavírám rozhodnutí.
en: I'm not a metrics-driven product manager. I close decisions.

cs: Nejsem agentura.
en: I'm not an agency.

cs: Nejsem ruce do Figmy.
en: I'm not an extra pair of hands in Figma.

cs: Jak vedu týmy, potvrdí Lukáš Rykr, můj přímý podřízený. <a class="gold" href="#/reference">Reference</a>
en: Lukáš Rykr, who reported to me, can tell you how I lead teams. <a class="gold" href="#/reference">Recommendations</a>

cs: <span class="yr">2023&ndash;2026</span><span class="w"><b>Vedoucí produktového designu, Coinmate</b>Regulovaná kryptoburza. Externě, dva dny v týdnu. Design systém od nuly, specifikace frontendu, podklady pro licenci MiCA a nová značka.</span>
en: <span class="yr">2023&ndash;2026</span><span class="w"><b>Head of Product Design, Coinmate</b>Regulated crypto exchange. External, 2 days a week. A design system from scratch, front-end specs, documentation for the MiCA license, and a new brand.</span>

cs: <span class="yr">2023&ndash;dosud</span><span class="w"><b>Zakládající designér a spoluzakladatel, Heirloom</b>Digitální dědictví, nový produkt od nuly. Produktové řízení, které tým neměl, a cesta od prototypu po nasazení.</span>
en: <span class="yr">2023&ndash;present</span><span class="w"><b>Founding Designer and Co-founder, Heirloom</b>Digital legacy, a new product from scratch. The product management the team didn't have, and the path from prototype to launch.</span>

cs: <span class="yr">2020&ndash;2023</span><span class="w"><b>Zakládající designér a vedoucí designu, Leeaf</b>Léčba neplodnosti. iOS, Android a portál pro lékaře. Potom systém, na kterém běžely další kliniky. Dva designéři v týmu.</span>
en: <span class="yr">2020&ndash;2023</span><span class="w"><b>Founding Designer and Head of Design, Leeaf</b>Fertility treatment. iOS, Android, and a doctors' portal. Then the system that other clinics ran on. A team of 2 designers.</span>

cs: <span class="yr">2018&ndash;dosud</span><span class="w"><b>Na volné noze</b>Sprinty a výzkum pro Komerční banku, Českou spořitelnu, CEMEX a ESET. Workshop pro BRENO &middot; 2023. Audity pro ESET, Jablotron a Centropol.</span>
en: <span class="yr">2018&ndash;present</span><span class="w"><b>Freelance</b>Sprints and research for Komerční banka, Česká spořitelna, CEMEX, and ESET. A workshop for BRENO &middot; 2023. Audits for ESET, Jablotron, and Centropol.</span>

cs: <span class="yr">2014&ndash;2018</span><span class="w"><b>Předtím</b>UX designér v Monsteru a Usertechu.</span>
en: <span class="yr">2014&ndash;2018</span><span class="w"><b>Before that</b>UX designer at Monster and Usertech.</span>

cs: <a class="btn btn-line" href="https://www.linkedin.com/in/pavelkroupa/" target="_blank" rel="noopener">Celá kariéra na LinkedInu</a>
en: <a class="btn btn-line" href="https://www.linkedin.com/in/pavelkroupa/" target="_blank" rel="noopener">Full career history on LinkedIn</a>

cs: Moje výhoda
en: My advantage

cs: Myslím v systémech.
en: I think in systems.

cs: Pracuju napříč obory i týmy. Banky, zdravotnictví, krypto. Vývoj, byznys, vedení i compliance. Rychle uvidím, jak spolu věci souvisí, a tým se díky tomu pohne hned.
en: I work across industries and teams: banking, healthcare, and crypto; engineering, business, leadership, and compliance. I quickly see how things connect, so the team can move right away.

cs: Dalších deset doporučení je <a class="gold" href="#/reference">v portfoliu</a>.
en: 10 more recommendations are <a class="gold" href="#/reference">in the portfolio</a>.

cs: Z práce
en: From my work

cs: Workshopy, tabule, prototypy.
en: Workshops, whiteboards, prototypes.

cs: Co říkají lidé, se kterými jsem pracoval.
en: What people I've worked with say.

cs: <a class="btn btn-line" href="#/reference">Všechny reference</a>
en: <a class="btn btn-line" href="#/reference">All recommendations</a>

cs: Něco ve vašem produktu není rozhodnuté? Promluvme si.
en: Is something in your product still undecided? Let's talk.

# ---------- kontakt
cs: Kde jste se <span class="fix">zasekli</span>?
en: Where are you <span class="fix">stuck</span>?

cs: Napište mi pár vět. Ozvu se a domluvíme třicetiminutový hovor. V Praze, v Amsterdamu nebo online.
en: Write me a few sentences. I'll get back to you, and we'll set up a 30-minute call. In Prague, in Amsterdam, or online.

cs: Jméno
en: Name

cs: E-mail
en: Email

cs: Služba
en: Service

cs: Zatím nevím
en: Not sure yet

cs: Firma <i>nepovinné</i>
en: Company <i>optional</i>

cs: Odeslat
en: Send

cs: <b>Díky, mám to.</b> Ozvu se na e-mail, který jste vyplnili.<small>Prototyp: formulář zatím nikam neodesílá.</small>
en: <b>Thanks, got it.</b> I'll reply to the email address you entered.<small>Prototype: this form doesn't send messages yet.</small>

cs: Raději napřímo?
en: Prefer to reach me directly?

cs: Zkopírovat
en: Copy

cs: Vybrat termín hovoru
en: Pick a time for a call

cs: Firemní údaje
en: Company details

cs: Firma
en: Company

cs: Sídlo
en: Registered address

cs: IČO
en: Company ID (IČO)

cs: DPH
en: VAT

cs: Neplátce DPH
en: Not registered for VAT

cs: Země
en: Country

cs: Česká republika
en: Czech Republic
''')

# ---------------------------------------------------------------- atributy (alt, aria-label, placeholder …)
ATTRS = _pairs(r'''
cs: Vzhled
en: Color theme

cs: Jedna zamotaná linka se rozplete, projde portrétem Pavla Kroupy, srovná se do rovné čáry a vede k dokumentu se třemi odškrtnutými body.
en: A tangled line untangles, passes through a portrait of Pavel Kroupa, straightens out, and leads to a document with a checklist.

cs: Klienti
en: Clients

cs: Na workshopu vzniká business logika, user flow a customer journey.
en: The workshop produces business logic, user flows, and a customer journey.

cs: Místnost po workshopu: stěny plné papírů, lepítek a tabulí
en: A room after a workshop: walls covered in paper, sticky notes, and whiteboards

cs: Animace: notebook se otevře, nakreslí se problém, řešení a tok obrazovek. Pohled se přiblíží na formulář, ten se nakreslí, kurzor klikne a pohled se vrátí do toku.
en: Animation: a laptop opens, and a problem, a solution, and a flow of screens are drawn. The view zooms in on a form, the form is drawn, a cursor clicks, and the view returns to the flow.

cs: Notebook s prototypem, ze kterého vede tok obrazovek
en: A laptop with a prototype and a flow of screens coming out of it

cs: Nahrávka obrazovky a seznam toho, co opravit dřív
en: A screen recording and a list of what to fix first

cs: Dva dny v týdnu ve vašem týmu: otázky vedení, směr a hotová práce vývoje
en: 2 days a week on your team: leadership questions, direction, and finished engineering work

cs: Doporučení, posunujte do strany
en: Recommendations. Scroll sideways for more.

cs: Co se stalo, po pořadí
en: What happened, step by step

cs: Postup: probrat to spolu, zmapovat službu, postavit obrazovky, sdílet jeden odkaz, pak rozhodnutý rozsah a podklad pro vývoj
en: Process: talk it through, map the service, build the screens, share one link, then a decided scope and a handoff for engineering

cs: Fotky z práce
en: Photos from my work

cs: Místnost po workshopu: stěny plné pláten, lepítek a tabulí
en: A room after a workshop: walls full of canvases, sticky notes, and whiteboards

cs: Místnost po workshopu: tabule, lepítka a papíry na stole
en: A room after a workshop: a whiteboard, sticky notes, and papers on the table

cs: Mapa prototypu pro Heirloom: všechny obrazovky a cesty mezi nimi, rozdělené podle rolí
en: Heirloom prototype map: every screen and the paths between them, grouped by role

cs: Reference
en: Recommendations

cs: Pár vět stačí. Co se nedaří rozhodnout a kdo o tom rozhoduje.
en: A few sentences are enough. What can't you decide, and who makes the decision?
''')

# Texty, které jsou v obou jazycích stejné (jména, firmy, doporučení z LinkedInu v angličtině …).
SAME = set(l.strip() for l in r'''
Pavel Kroupa
Portfolio
Decision Prototype
LinkedIn
info@pavelkroupa.com
Mezno 88, 257 86 Mezno
www
CS
EN
Česká verze
English version
SatoshiLabs
Komerční banka
Česká spořitelna
Modrá pyramida
Centropol
WPP
ESET
Jablotron
Coinmate
Leeaf
BRENO
Heirloom
Heirloom &middot; 2026
Coinmate &middot; 2023&ndash;2026
Leeaf &middot; 2020&ndash;2023
BRENO &middot; 2023
<b>Ondřej Steklý</b>Chief Product Officer, Coinmate
'''.strip().split("\n"))


def _english_quotes():
    """Doporučení z LinkedInu jsou v originále anglicky, zůstávají beze změny."""
    return {
        "&ldquo;at a time when we did not have the product function covered internally, was able to step in and take on a significant part of product management as well&rdquo;",
        "&ldquo;A notable example was a crucial two-day kick-off workshop for a major client.&rdquo;",
        "&ldquo;He is a listener who keeps the end goal in mind.&rdquo;",
        "&ldquo;His design thinking, paired with his adeptness at managing workshops and meetings, truly stood out.&rdquo;",
        "&ldquo;seamlessly transition from big-picture strategic thinking to diving deep into problem-solving&rdquo;",
        "&ldquo;adjusting designs based on technical challenges&rdquo;",
        "&ldquo;efficiently managing tasks in alignment with the roadmap to prevent burnout&rdquo;",
        "&ldquo;his impact on our startup, Motionshift, has been transformative&rdquo;",
        "&ldquo;actively engages with end users to ensure their needs are met through iterative processes&rdquo;",
        "&ldquo;He took ownership of our product design end to end&rdquo;",
    }


SAME |= _english_quotes()
SAME_PREFIXES = ("Pavel joined us", "He was also an early adopter", "I've worked closely with Pavel", "Working with Pavel",
                 "I am confident in Pavel", "I had the chance to work with Pavel", "Pavle quickly processes",
                 "I've been working remotely with Pavel", "Pavel's strength lies", "I've had an opportunity to work",
                 "Pavel greatly improved", "We have been working closely", "Pavel's expertise in UX",
                 "I've had the pleasure", "Throughout our long collaboration", "Pavel consistently demonstrates",
                 "Pavel is not only hardworking", "I met Pavel during")


class _Same(set):
    """Celé texty doporučení se poznají podle začátku, aby se nemusely opisovat."""
    def __contains__(self, item):
        return set.__contains__(self, item) or item.startswith(SAME_PREFIXES)


SAME = _Same(SAME)

# ---------------------------------------------------------------- texty ve skriptu
JS = [
    ('"Označeno, zkopírujte"', '"Selected. Copy it now."'),
    ('"Zkopírováno"', '"Copied"'),
    ('"funkční prototyp"', '"a working prototype"'),
    ('"Skrýt podrobnosti"', '"Hide details"'),
    ('"Jak to probíhá podrobně"', '"See how it works in detail"'),
    ('"Vyplňte prosím jméno, e-mail a pár vět."', '"Please enter your name, your email address, and a few sentences."'),
]

# ---------------------------------------------------------------- metadata
NAV = {"/": "Home", "/portfolio": "Portfolio", "/services": "Services", "/about": "About", "/contact": "Contact"}
CRUMBS = {"home": "Home", "portfolio": "Portfolio", "services": "Services", "about": "About", "contact": "Contact"}

META = {
    "/": dict(title="Pavel Kroupa · Product Definition and Working Prototypes",
              desc="I help teams decide what to build. A workshop with your decision-makers, a working prototype, "
                   "and a finished spec. With AI, in days, not weeks.",
              og="og-home"),
    "/portfolio": dict(title="Portfolio · Pavel Kroupa",
                       desc="4 companies, 4 stuck products: Coinmate, Leeaf, Heirloom, and BRENO. What was decided "
                            "and how it turned out.",
                       og="og-portfolio"),
    "/work/heirloom": dict(title="Heirloom: A New Business Direction in 4 Iterations",
                           desc="Digital legacy. Working prototype first, spec second. We closed the new direction "
                                "in 4 sessions.",
                           og="og-portfolio"),
    "/work/coinmate": dict(title="Coinmate: Design System and New Brand Identity",
                           desc="Regulated crypto exchange. A design system first, then a new brand identity. "
                                "Rebrand launched October 1, 2026.",
                           og="og-portfolio"),
    "/work/leeaf": dict(title="Leeaf: One App for Many Clinics",
                        desc="Fertility treatment. A scalable, white-label design system. More clinics launched on "
                             "the same system.",
                        og="og-portfolio"),
    "/work/breno": dict(title="BRENO: Backlog Prioritization in 2 Days",
                        desc="Retail and e-commerce. A 2-day workshop through WPP. Leadership, engineering, and "
                             "marketing agreed on priorities.",
                        og="og-portfolio"),
    "/services": dict(title="Services · Decision Prototype, Audit, Product Leadership",
                      desc="3 ways to work together: Decision Prototype from CZK 49,000, Decision Audit from "
                           "CZK 29,000, and product leadership from CZK 120,000 per month.",
                      og="og-decision-prototype"),
    "/services/decision-prototype": dict(title="Decision Prototype: A Working Prototype in Days",
                                         desc="A workshop with your decision-makers and a working prototype on the "
                                              "web. 1 day, 2 days, or a week. From CZK 49,000.",
                                         og="og-decision-prototype"),
    "/services/audit": dict(title="Product Audit in 5 Days · Pavel Kroupa",
                            desc="A narrated screen recording and a list of what to fix first. No meetings. "
                                 "From CZK 29,000.",
                            og="og-audit"),
    "/services/fractional": dict(title="Fractional Product and Design Leadership",
                                 desc="2 days a week on your team, for at least 3 months, until you hire someone "
                                      "permanent. From CZK 120,000 per month.",
                                 og="og-fractional"),
    "/about": dict(title="About · Pavel Kroupa",
                   desc="13 years of guiding teams to decisions. Banking, healthcare, crypto. Prague and Amsterdam.",
                   og="og-home"),
    "/contact": dict(title="Contact · Pavel Kroupa",
                     desc="Tell me where you're stuck. A 30-minute call in Prague, in Amsterdam, or online.",
                     og="og-home"),
}

KEYWORDS = ("working prototype, clickable prototype, product requirements, product spec, product discovery workshop, "
            "design sprint, UX audit, product audit, fractional product leadership, fractional CPO, "
            "fractional product lead, product design, design system, UX consultant Prague, UX consultant Amsterdam, "
            "fintech, crypto exchange, banking, healthcare, decision prototype, product definition")

OG_ALT = {
    "og-home": "Pavel Kroupa: I help teams decide what to build.",
    "og-portfolio": "Portfolio: 4 companies. 4 stuck products.",
    "og-decision-prototype": "Decision Prototype: A working prototype in a few days.",
    "og-audit": "Decision Audit: Find out what's holding back your product. In 5 days.",
    "og-fractional": "A product lead until you hire one.",
}

PERSON = dict(
    jobTitle="Product definition and design leadership",
    description="For 13 years, I've guided teams to decisions. I come in where product decisions haven't been made "
                "yet, or where a team is going in circles and needs to move forward.",
    knowsAbout=["working prototypes", "product discovery", "UX audits", "design systems", "product leadership",
                "fintech", "healthcare"],
    workLocation=["Prague", "Amsterdam"],
)

BUSINESS = dict(
    description=None,  # = popis úvodní stránky
    areaServed=["Czech Republic", "Netherlands", "online"],
    catalog="Services",
    address=dict(streetAddress="Mezno 88", postalCode="257 86", addressLocality="Mezno", addressCountry="CZ"),
)

SERVICES = {
    "dp": dict(name="Decision Prototype",
               desc="A decision you can click through. You bring an open question. You leave with a decision and a "
                    "working prototype on the web that engineering can build from.",
               offers=[("1 day", "1 workshop and a first version of the prototype.", 49000, None),
                       ("2 days", "1 open question, resolved end to end.", 125000, None),
                       ("1 week", "An entire product area, with more interviews and workshops.", 220000, None)]),
    "audit": dict(name="Decision Audit",
                  desc="I review your product and show you, in a screen recording, what isn't working and the order "
                       "I'd fix it in. No meetings.",
                  offers=[(None, "5 business days, no meetings.", 29000, None)]),
    "fractional": dict(name="Fractional product and design leadership",
                       desc="2 days a week, I work as part of your team. I make decisions with you in leadership and "
                            "product meetings and keep the direction steady, so engineering doesn't go in circles.",
                       offers=[(None, "2 days a week, for at least 3 months.", 120000, "MON")]),
}

NOTFOUND = dict(
    title="Page Not Found · Pavel Kroupa",
    eyebrow="Error 404",
    h1='This page <span class="fix">doesn\'t exist</span>.',
    lede="The site has a new structure, and some old addresses no longer work. Start on the home page, "
         "or tell me where you're stuck.",
    home="Go to the home page",
    contact="Contact me",
)
