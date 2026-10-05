"""Stránka Design systém na /ds: styl, loga, barvy, písmo a komponenty webu na jednom místě.

Vyrábí ji pages.py spolu s ostatními stránkami. Bere skutečný styl, skript, hlavičku a patičku
webu a skutečné kusy stránek (karty, lepítka, otázky …), takže se změny na webu propíšou i sem.
Barvy tokenů a rozměry písma čte až prohlížeč přímo ze stylu, ve světlém i tmavém režimu.

Stránka není veřejná: nikde na ni nevede odkaz, není v sitemap.xml ani v llms.txt, má noindex
a robots.txt ji zakazuje. Kdo zná adresu, otevře ji: GitHub Pages neumí stránku zamknout heslem.

Texty, které stránka cituje z webu (claim, ukázky hlasu, zásady z komentářů ve stylu), se při
stavbě kontrolují. Když už na webu nejsou, pages.py vypíše upozornění a stránku je potřeba
upravit tady.
"""
import html
import re
from pathlib import Path

import i18n

# ---------------------------------------------------------------- obsah

ICO = "87977753"

IDENTITY = [
    # (štítek, česky, anglicky, kde se používá)
    ("Claim", 'Pomáhám týmům <span class="fix">rozhodnout</span>, co postavit.',
     'I help teams <span class="fix">decide</span> what to build.',
     "První věta úvodní stránky a obrázku pro sdílení. Fix je na slovese rozhodnout, anglicky decide."),
    ("Tagline", "Definice produktu a funkční prototypy", "Product Definition and Working Prototypes",
     "Za jménem v titulku úvodní stránky."),
    ("Podpůrná věta", "S AI za dny, ne týdny.", "With AI, in days, not weeks.",
     "Na konci popisu úvodní stránky a v obrázku pro sdílení."),
    ("Podpis", "Pavel Kroupa &middot; definice produktu a vedení designu",
     "Pavel Kroupa &middot; Product definition and design leadership",
     "Patička každé stránky. Ve strukturovaných datech jako pracovní pozice."),
]

VOICE = [
    # (pravidlo, vysvětlení, ukázka z webu)
    ("Za sebe, k vám", "Píšu v první osobě, čtenáři vykám.",
     "Napište mi pár vět. Ozvu se a domluvíme třicetiminutový hovor."),
    ("Krátké věty", "Jedna věta, jedna myšlenka.", "Kód zlevnil. Shodnout se na zadání ne."),
    ("Konkrétně", "Dny, ceny a výsledky místo přívlastků.", "Dva dny v týdnu ve vašem týmu."),
    ("Slovy klienta", "Problém popisuju tak, jak ho tým zažívá.",
     "Mluví se a mluví. Co dělat, všichni tuší. Nikdo to nechce vzít na sebe."),
    ("Rozhodnutí na prvním místě", "Hlavní slovo webu je rozhodnout. Služby slibují rozhodnutí, ne činnost.",
     "Rozhodnutí, na které se dá kliknout."),
]

FORMATS = [
    ("Ceny", "od 49 000 Kč, tisíce oddělené mezerou", "From CZK 49,000"),
    ("Roky", "2020&ndash;2023, pomlčka bez mezer", "2020&ndash;2023"),
    ("Data", "1. 10. 2026", "October 1, 2026"),
    ("Oddělovač v titulcích a štítcích", "Heirloom &middot; 2026", "Heirloom &middot; 2026"),
]

# Zásady přímo z komentářů ve stylu webu. Když komentář zmizí, stavba upozorní.
QUOTES = {
    "tabule": "Tabule. Bílá, černá, žlutá jen jako fix.",
    "tecky": "TEČKY: podklad, ne textura.",
    "tecky1": "1. Tečky jen tam, kde na nich něco leží.",
    "tecky2": "2. Co na nich leží, je neprůhledné. Karta, tlačítko, lepítko, papír.",
    "tecky3": "3. Nikdy pod běžícím textem. Nadpis a lede ano, odstavec ne.",
    "fix": "žlutý fix: nejvýš dvakrát na stránku",
    "fixdark": "na tmavém podkladu žlutý fix přebije písmo, tam jen podtržení fixem",
    "papir": "papírové předměty: nikdy plocha, vždycky věc",
    "fotka": "fotka je předmět, který leží na tabuli: papír, páska, stín",
    "linka": "uvnitř listu stejná linka jako kresba: rámečky tažené fixem, ne čárkované UI",
    "ruka": "Ruční věci zůstávají: linka v hlavičce, štítky, lepítka, rukopis.",
    "sklo": "sklo na prvcích, které nejsou rukou",
    "ruka2": "ruka zůstává bez skla: lepítka, linka, polaroid",
    "hero": "linka vteče do tváře a vyjde rovná",
    "nalepeni": "nalepení: přiletí shora, přitiskne se, dosedne",
    "tmavy": "Tmavý režim: z tabule se stane černá tabule. Fix zůstává žlutý.",
    "tokeny": "doplňky pro nový obsah, jen z tokenů",
    "stred": "section heads centre, reading stays left (Apple)",
}

# Hodnoty pohybu, jak jsou ve stylu a skriptu. Když se změní, stavba upozorní.
MOTION_CHECK = ["translateY(16px)", "opacity .7s cubic-bezier(.2,.7,.3,1)", "*55+\"ms\"", "stick .46s",
                "translateY(-30px) rotate(calc(var(--rot) - 7deg)) scale(1.07)", "idx*260", "scale(1.015)",
                ".btn:hover{transform:translateY(-1px)}", "translateX(4px)", "animation-play-state:paused",
                "prefers-reduced-motion:reduce"]

TOKENS = [
    ("Plochy", [("--ground", "Podklad stránky"),
                ("--surface", "Šedá plocha: najetí myší, náhrada skla"),
                ("--raise", "Zvednutá plocha: formulář, karty na O mně")]),
    ("Text", [("--ink", "Nadpisy, text, plné tlačítko, logo pk"),
              ("--muted", "Úvodní odstavce a popisy"),
              ("--faint", "Metadata a drobné popisky")]),
    ("Linky a tečky", [("--line", "Obrysy polí a oddělovače"),
                       ("--grid", "Tečky tabule")]),
    ("Fix", [("--fix", "Žlutý fix, lepítka, logo, plné tlačítko na černé"),
             ("--fix-deep", "Spodní hrana lepítka"),
             ("--on-fix", "Text na žluté")]),
    ("Papír", [("--paper", "Polaroid, citát na černé"),
               ("--paper-ink", "Text na papíře"),
               ("--paper-soft", "Popisky na papíře"),
               ("--paper-hatch", "Šrafování prázdné fotky")]),
    ("Černý panel", [("--panel", "Černá sekce"),
                     ("--on-panel", "Nadpisy na panelu"),
                     ("--on-panel-soft", "Odstavce na panelu")]),
    ("Sklo a světlo", [("--glass", "Skleněná karta a obrysové tlačítko"),
                       ("--glass-strong", "Sklo při najetí myší"),
                       ("--glass-line", "Obrys uzlu v diagramu"),
                       ("--glow-a", "Světlo pod stránkou vpravo nahoře"),
                       ("--glow-b", "Světlo pod stránkou vlevo"),
                       ("--glow-c", "Světlo pod stránkou vpravo dole")]),
    ("Kresba notebooku", [("--lap-frame", "Rám"), ("--lap-base", "Spodek"), ("--lap-notch", "Výřez"),
                          ("--lap-scr", "Obrazovka"), ("--lap-shadow", "Stín")]),
]
OTHER_TOKENS = [("--glass-shadow", "Stín skleněné karty",
                 '<span class="ds-chip" style="background:var(--glass);box-shadow:var(--glass-shadow)"></span>'),
                ("--display", "Nadpisy, tlačítka, popisky", '<span class="ds-chip ds-aa" style="font-family:var(--display)">Aa</span>'),
                ("--text", "Běžný text", '<span class="ds-chip ds-aa" style="font-family:var(--text)">Aa</span>'),
                ("--hand", "Ruční písmo", '<span class="ds-chip ds-aa" style="font-family:var(--hand)">Aa</span>')]
# Ve stylu zůstaly ze starších verzí a na webu se už neprojeví (přebíjí je pozdější pravidla).
LEGACY = ["--accent", "--on-accent", "--serif", "--panel-deep", "--panel-line", "--panel-grid", "--glass-edge"]

TOC = [("identita", "Identita"), ("hlas", "Hlas"), ("logo", "Logo"), ("ikony", "Ikony"), ("barvy", "Barvy"),
       ("pismo", "Písmo"), ("jazyk", "Vizuální jazyk"), ("pohyb", "Pohyb"), ("komponenty", "Komponenty"),
       ("rezimy", "Režimy"), ("sdileni", "Sdílení"), ("stazeni", "Ke stažení"), ("kod", "V kódu")]


# ---------------------------------------------------------------- pomocníci

def esc(s):
    return html.escape(s, quote=True)


def grab(markup, start_re, nth=0, has=None):
    """Prvek ze stránky webu (i s obsahem), jehož otevírací značka odpovídá start_re
    a který obsahuje text has."""
    hits = []

    def walk(node):
        for c in node.children:
            if c.text is None:
                if re.search(start_re, c.start) and (has is None or has in i18n.render(c)):
                    hits.append(c)
                walk(c)
    walk(i18n.parse(markup))
    assert len(hits) > nth, f"ds.py: na webu chybí prvek {start_re!r} {has or ''}, upravte ukázku komponenty"
    return i18n.render(hits[nth])


def code_view(snippet):
    """Zdroj ukázky k nahlédnutí: SVG zkrácené, odsazení srovnané."""
    s = re.sub(r"(<svg\b[^>]*>).*?(</svg>)", r"\1…\2", snippet, flags=re.S)
    lines = [l.rstrip() for l in s.strip("\n").split("\n") if l.strip()]
    ind = [len(l) - len(l.lstrip()) for l in lines[1:]]
    cut = min(ind) if ind else 0
    lines = [lines[0].lstrip()] + [l[cut:] for l in lines[1:]]
    return esc("\n".join(lines))


def visible(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup)))


def size(path):
    n = path.stat().st_size
    return f"{n / 1024:.0f} kB" if n >= 1024 else f"{n} B"


def demo(title, note, inner, src=None, cls=""):
    """Komponenta: nadpis, kdy ji použít, živá ukázka a její HTML."""
    code = (f'<details class="ds-src"><summary>HTML</summary><pre><code>{code_view(src or inner)}</code></pre></details>'
            if src is not False else "")
    return (f'<article class="ds-comp {cls}"><div class="ds-comp-h"><h3>{title}</h3><p>{note}</p></div>'
            f'<div class="ds-stage">{inner}</div>{code}</article>')


# ---------------------------------------------------------------- styl a skript jen pro tuto stránku

CSS = """
/* Design systém (/ds): jen pro tuto stránku. Barvy, písmo a rádiusy z tokenů webu. */
.ds section{padding-block:clamp(72px,9vw,128px)}
.ds section+section{padding-top:clamp(24px,3vw,40px)}
.ds-hero{padding-bottom:clamp(56px,7vw,96px)!important}
.ds section[id]{scroll-margin-top:64px}
.ds .wrap{min-width:0}
.ds-toc{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:34px auto 0;max-width:820px}
.ds-toc a{font-family:var(--display);font-size:14px;font-weight:500;letter-spacing:-.01em;color:var(--ink);
  text-decoration:none;padding:8px 15px;border-radius:980px;background:var(--glass);box-shadow:var(--glass-shadow);
  -webkit-backdrop-filter:blur(20px) saturate(180%);backdrop-filter:blur(20px) saturate(180%);transition:background .25s ease}
.ds-toc a:hover{background:var(--glass-strong)}
.ds-note{font-family:var(--display);font-size:13px;color:var(--faint);text-align:center;max-width:62ch;margin:26px auto 0}
.ds h3{text-align:left}
.ds-grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));margin-top:40px}
.ds-grid.two{grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr))}
.ds-card{background:var(--glass);box-shadow:var(--glass-shadow);border-radius:28px;padding:24px 26px;min-width:0;
  -webkit-backdrop-filter:blur(24px) saturate(180%);backdrop-filter:blur(24px) saturate(180%)}
.ds-card>:last-child{margin-bottom:0}
.ds-card p,.ds-card li{font-size:15px;line-height:1.5;color:var(--muted);max-width:none}
.ds-k{display:block;font-family:var(--display);font-size:13px;font-weight:600;letter-spacing:0;color:var(--faint);margin:0 0 8px}
.ds-big{font-family:var(--display);font-size:clamp(22px,2.6vw,30px);font-weight:600;letter-spacing:-.03em;line-height:1.15;
  color:var(--ink)!important;margin:0 0 10px!important}
.ds-en{font-family:var(--display);font-size:15px;color:var(--ink)!important;margin:0 0 12px!important}
.ds-en::before{content:"EN ";font-size:11px;font-weight:600;letter-spacing:.06em;color:var(--faint)}
.ds-use{font-size:13.5px!important;color:var(--faint)!important}
.ds code,.ds pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:0}
.ds code{font-size:.84em;background:var(--surface);border-radius:6px;padding:.12em .4em;color:var(--ink);word-break:break-word}
.ds-dl{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:8px 18px;margin:0;font-size:15px}
.ds-dl dt{font-family:var(--display);font-size:14px;color:var(--faint)}
.ds-dl dd{margin:0;color:var(--ink);min-width:0;overflow-wrap:anywhere}
.ds-dl a{color:var(--ink)}
.ds-table{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}
.ds-table th{font-family:var(--display);font-size:13px;font-weight:600;color:var(--faint);text-align:left;padding:0 12px 8px 0}
.ds-table td{padding:10px 12px 10px 0;border-top:1px solid var(--line);color:var(--ink);vertical-align:top}
.ds-scroll{overflow-x:auto;max-width:100%}
.ds-q{font-family:var(--display);font-size:15px;font-style:normal;color:var(--ink);margin:0 0 12px;padding-left:14px;
  border-left:3px solid var(--fix);max-width:none}
.ds-ex{font-family:var(--hand);font-size:19px;line-height:1.35;color:var(--ink)!important;margin-top:12px!important}
.ds-ex::before{content:"\\201E"}.ds-ex::after{content:"\\201C"}

/* loga a ikony */
.ds-tiles{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));margin-top:40px}
.ds-tile{margin:0;min-width:0}
.ds-tile>div{aspect-ratio:4/3;border-radius:22px;display:grid;place-items:center;padding:22px;box-shadow:var(--glass-shadow)}
.ds-tile img{max-width:100%;max-height:100%;width:auto;height:auto;display:block}
.ds-tile figcaption{font-family:var(--display);font-size:13.5px;color:var(--muted);margin-top:10px;line-height:1.4}
.ds-tile figcaption b{display:block;color:var(--ink);font-weight:600}
.ds-on-light{background:#FFFFFF}.ds-on-dark{background:#111111}
.ds-on-check{background:repeating-conic-gradient(var(--surface) 0 25%,var(--ground) 0 50%) 0 0/18px 18px}
.ds-mark .pk{height:clamp(72px,12vw,120px);width:auto;display:block}
.ds-icons{display:flex;flex-wrap:wrap;align-items:flex-end;gap:22px 26px;margin-top:8px}
.ds-icons figure{margin:0;text-align:center}
.ds-icons img{display:block;margin:0 auto 8px}
.ds-icons figcaption{font-family:var(--display);font-size:12.5px;color:var(--faint);line-height:1.35}
.ds-tab{display:inline-flex;align-items:center;gap:8px;max-width:100%;padding:9px 16px 9px 12px;border-radius:12px 12px 0 0;
  background:var(--surface);font-family:var(--display);font-size:13px;color:var(--ink);box-shadow:0 -1px 0 var(--line) inset}
.ds-tab span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ds-bar{height:6px;border-radius:0 6px 6px 6px;background:#FFCE1B;max-width:340px}

/* barvy */
.ds-tg{margin-top:34px}
.ds-tg h3{font-size:17px;margin:0 0 10px}
.ds-sw{list-style:none;margin:0;padding:0;display:grid;gap:0}
.ds-sw li{display:grid;grid-template-columns:64px minmax(0,1fr) auto;gap:4px 16px;align-items:center;padding:10px 0;
  border-top:1px solid var(--line)}
.ds-chip{display:flex;width:64px;height:40px;border-radius:12px;overflow:hidden;box-shadow:0 0 0 1px var(--line) inset}
.ds-chip i{flex:1;box-shadow:0 0 0 1px rgba(128,128,128,.18) inset}
.ds-name b{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;font-weight:600;color:var(--ink);
  letter-spacing:0;display:block}
.ds-name span{font-size:14px;color:var(--muted);line-height:1.35;display:block}
.ds-vals{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.ds-val{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;letter-spacing:0;color:var(--ink);
  background:var(--surface);border:0;border-radius:8px;padding:5px 8px;cursor:pointer;max-width:260px;text-align:left;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ds-val::before{font-family:var(--display);font-size:10.5px;font-weight:600;color:var(--faint);margin-right:6px}
.ds-val.l::before{content:"☀"}.ds-val.d::before{content:"☾"}.ds-val.l.both::before{content:"☀ ☾"}
.ds-aa{display:grid!important;place-items:center;font-size:20px;color:var(--ink);background:var(--surface)}
.ds-val:hover{background:var(--glass-strong);box-shadow:var(--glass-shadow)}
.ds-val.ok{background:var(--fix);color:#111111}
@media(max-width:640px){
  .ds-sw li{grid-template-columns:52px minmax(0,1fr)}
  .ds-chip{width:52px;height:36px}
  .ds-vals{grid-column:2;justify-content:flex-start}
  .ds-val{max-width:100%}
}

/* písmo */
.ds-spec{display:grid;grid-template-columns:150px minmax(0,1fr);gap:6px 24px;align-items:baseline;padding:22px 0;
  border-top:1px solid var(--line)}
.ds-spec>.ds-k{margin:0}
.ds-spec .ds-m{grid-column:2;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;
  color:var(--faint);letter-spacing:0}
.ds-spec h1,.ds-spec h2,.ds-spec h3,.ds-spec .lede,.ds-spec .eyebrow,.ds-spec p{margin:0;text-align:left;max-width:none}
@media(max-width:640px){.ds-spec{grid-template-columns:1fr}.ds-spec .ds-m{grid-column:1}}
.ds-glyphs{font-size:clamp(40px,7vw,72px);line-height:1.05;letter-spacing:-.02em;color:var(--ink);margin:6px 0 14px!important;
  overflow-wrap:anywhere}
.ds-weights{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:22px;color:var(--ink);margin:0 0 12px!important}
.ds-hand{font-family:var(--hand)}
.ds-sys{font-family:var(--display)}

/* vizuální jazyk */
.ds-board{position:relative;border-radius:22px;min-height:190px;display:grid;place-items:center;padding:28px;
  box-shadow:0 0 0 1px var(--line) inset;margin-top:14px;overflow:hidden}
.ds-board.dots{background-color:var(--ground)}
.ds-chips{display:flex;gap:10px;margin-top:14px}
.ds-chips i{width:56px;height:56px;border-radius:14px;box-shadow:0 0 0 1px var(--line) inset}
.ds-panel{background:var(--panel);color:var(--on-panel);border-radius:22px;padding:22px 24px;margin-top:12px}
.ds-panel p{color:var(--on-panel)!important;font-family:var(--display);font-size:22px!important;font-weight:600;
  letter-spacing:-.02em;margin:0!important}
.ds-light p{font-family:var(--display);font-size:22px!important;font-weight:600;letter-spacing:-.02em;color:var(--ink)!important;
  margin:14px 0 0!important}
.ds-pair{display:flex;flex-wrap:wrap;gap:28px;align-items:center;justify-content:center;margin-top:14px}
.ds-pair .note{width:190px;min-height:150px}
.ds-pair .note p{font-size:18px}
.ds-glasscard{background:var(--glass);box-shadow:var(--glass-shadow);border-radius:28px;padding:20px 22px;width:210px;
  -webkit-backdrop-filter:blur(24px) saturate(180%);backdrop-filter:blur(24px) saturate(180%);font-family:var(--display);
  font-size:15px;color:var(--ink)}
.ds-glasscard small{display:block;font-size:13px;color:var(--faint);margin-top:4px}
.ds-hx .hx-fig{margin:24px auto 0}
.ds-print{display:flex;justify-content:center;padding:18px 0 4px}
.ds-dims td:first-child{color:var(--muted);font-family:var(--display);font-size:14px}
.ds-dims td:last-child{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13px}

/* komponenty */
.ds-comps{display:grid;gap:22px;margin-top:40px}
.ds-comp{background:var(--glass);box-shadow:var(--glass-shadow);border-radius:28px;padding:26px;min-width:0;
  -webkit-backdrop-filter:blur(24px) saturate(180%);backdrop-filter:blur(24px) saturate(180%)}
.ds-comp-h h3{margin:0 0 6px}
.ds-comp-h p{font-size:15px;color:var(--muted);margin:0;max-width:70ch}
.ds-stage{margin-top:20px;padding:28px;border-radius:20px;background:var(--ground);box-shadow:0 0 0 1px var(--line) inset;
  min-width:0;overflow:hidden}
.ds-stage.dots{background-color:var(--ground)}
.ds-stage>.panel{margin:-28px;padding:36px 28px;border-radius:20px}
.ds-stage>.ds-foot{margin:22px -28px -28px;padding:28px;border-radius:0 0 20px 20px}
.ds-stage .cards,.ds-stage .svc-cards,.ds-stage .notes,.ds-stage .faq,.ds-stage .acards{margin-top:0}
.ds-stage .notes{max-width:none}
.ds-stage .clients2{margin:0}
.ds-stage .ct-form{max-width:560px}
.ds-stage .q{margin:0}
.ds-src{margin-top:14px}
.ds-src summary{font-family:var(--display);font-size:13px;font-weight:600;color:var(--faint);cursor:pointer;
  list-style:none;display:inline-flex;gap:6px;align-items:center}
.ds-src summary::-webkit-details-marker{display:none}
.ds-src summary::before{content:"+";font-weight:600}
.ds-src[open] summary::before{content:"−"}
.ds-src pre{margin:10px 0 0;padding:16px;border-radius:14px;background:var(--surface);overflow:auto;max-height:340px;
  font-size:12.5px;line-height:1.55;color:var(--ink);white-space:pre}
@media(max-width:480px){
  .ds-card,.ds-comp{padding:20px 18px}
  .ds-stage{padding:18px}
  .ds-stage>.panel{margin:-18px;padding:28px 18px}
  .ds-stage>.ds-foot{margin:18px -18px -18px;padding:22px 18px}
}
.ds-replay{margin-top:16px}
.ds-replay .btn{font-size:15px;padding:9px 18px}
.ds-rv-demo{display:grid;place-items:center;min-height:120px}
.ds-rv-demo>div{font-family:var(--display);font-size:22px;font-weight:600;letter-spacing:-.02em;color:var(--ink)}

/* režimy */
.ds-seg{display:inline-flex;gap:4px;padding:4px;border-radius:980px;background:var(--surface);margin:26px auto 0}
.ds-seg button{font-family:var(--display);font-size:15px;font-weight:500;color:var(--muted);background:transparent;border:0;
  border-radius:980px;padding:9px 16px;cursor:pointer}
.ds-seg button[aria-pressed="true"]{background:var(--ground);color:var(--ink);box-shadow:var(--glass-shadow)}
.ds-center{text-align:center}
.ds-list{margin:0;padding-left:20px}
.ds-list li{margin:0 0 8px}

/* sdílení a soubory */
.ds-og{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));margin-top:20px}
.ds-og figure{margin:0}
.ds-og img{width:100%;height:auto;display:block;border-radius:14px;box-shadow:0 0 0 1px var(--line)}
.ds-og figcaption{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;color:var(--faint);
  margin-top:8px;letter-spacing:0}
.ds-files{list-style:none;margin:0;padding:0}
.ds-files li{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-top:1px solid var(--line);font-size:14.5px}
.ds-files a{color:var(--ink);overflow-wrap:anywhere;min-width:0}
.ds-files span{color:var(--faint);font-family:var(--display);font-size:13px;white-space:nowrap}
"""

JS = r"""
(function(){
  /* tokeny: hodnoty ve světlém a tmavém režimu přímo ze stylu webu */
  var rows=[].slice.call(document.querySelectorAll("[data-t]"));
  if(rows.length){
    var root=document.documentElement,prev=root.getAttribute("data-theme");
    var still=document.createElement("style");
    still.textContent="*,*::before,*::after{transition:none!important}";
    document.head.appendChild(still);
    function read(mode){root.setAttribute("data-theme",mode);var cs=getComputedStyle(root),o={};
      rows.forEach(function(r){var n=r.getAttribute("data-t");o[n]=cs.getPropertyValue(n).trim();});return o;}
    var L=read("light"),D=read("dark");
    if(prev===null)root.removeAttribute("data-theme");else root.setAttribute("data-theme",prev);
    getComputedStyle(root).color;still.parentNode.removeChild(still);
    rows.forEach(function(r){var n=r.getAttribute("data-t"),l=L[n]||"",d=D[n]||"";
      var c=r.querySelector(".ds-chip");
      if(c&&c.children.length===2){c.children[0].style.background=l;c.children[1].style.background=d;}
      var vl=r.querySelector(".ds-val.l"),vd=r.querySelector(".ds-val.d");
      if(vl){vl.textContent=l;vl.title=l;vl.setAttribute("data-copy",l);}
      if(vd){if(d===l){vd.parentNode.removeChild(vd);if(vl)vl.classList.add("both");}
             else{vd.textContent=d;vd.title=d;vd.setAttribute("data-copy",d);}}
    });
  }
  /* kopírování hodnoty kliknutím */
  document.addEventListener("click",function(e){
    var b=e.target.closest&&e.target.closest("[data-copy]");if(!b)return;
    var v=b.getAttribute("data-copy"),t=b.textContent;
    function done(){b.classList.add("ok");b.textContent="Zkopírováno";setTimeout(function(){b.classList.remove("ok");b.textContent=t;},1100);}
    try{navigator.clipboard.writeText(v).then(done,function(){});}catch(x){}
  });
  /* písmo: rozměry tak, jak je prohlížeč právě vykresluje */
  function metrics(){
    var w=document.querySelector("[data-vw]");if(w)w.textContent=Math.round(window.innerWidth)+" px";
    document.querySelectorAll("[data-spec]").forEach(function(box){
      var el=box.querySelector("[data-spec-el]"),out=box.querySelector(".ds-m");if(!el||!out)return;
      var s=getComputedStyle(el),fs=parseFloat(s.fontSize),lh=parseFloat(s.lineHeight),ls=parseFloat(s.letterSpacing)||0;
      function n(x){return String(Math.round(x*10)/10).replace(".",",");}
      out.textContent=n(fs)+" px · řádek "+(isNaN(lh)?"normal":n(lh)+" px")+" · váha "+s.fontWeight+
        (ls?" · prostrkání "+n(ls)+" px":"")+" · "+(/Shantell/.test(s.fontFamily)?"Shantell Sans":"systémové písmo");
    });
    document.querySelectorAll("[data-dim]").forEach(function(td){
      var p=td.getAttribute("data-dim").split("|"),el=document.querySelector(p[0]);if(!el){td.textContent="(na stránce není)";return;}
      var s=getComputedStyle(el);td.textContent=p.slice(1).map(function(k){return s[k];}).join(" / ");
    });
  }
  var rt=null;metrics();window.addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(metrics,150);});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(metrics);
  /* přepínač režimu: ovládá stejné tlačítko jako hlavička, volba se pamatuje stejně */
  var seg=document.querySelector("[data-ds-theme]"),tb=document.getElementById("theme");
  if(seg&&tb){
    function cur(){return document.documentElement.getAttribute("data-theme")||"system";}
    function sync(){[].forEach.call(seg.querySelectorAll("button"),function(b){b.setAttribute("aria-pressed",b.value===cur()?"true":"false");});}
    seg.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;
      for(var i=0;i<3&&cur()!==b.value;i++)tb.click();sync();});
    tb.addEventListener("click",function(){setTimeout(sync,0);});
    sync();
  }
  /* přehrát znovu */
  document.addEventListener("click",function(e){
    var b=e.target.closest&&e.target.closest("[data-replay]");if(!b)return;
    var k=b.getAttribute("data-replay");
    if(k==="notes"){var w=document.querySelector("[data-notes]");if(!w)return;
      if(!w.hasAttribute("data-armed"))w.setAttribute("data-armed","");
      var ns=w.querySelectorAll(".note");[].forEach.call(ns,function(x){x.classList.remove("stuck");});void w.offsetWidth;
      [].forEach.call(ns,function(x,i){setTimeout(function(){x.classList.add("stuck");},i*260);});}
    if(k==="hx"){var f=document.querySelector(".ds-hx .hx-fig");if(f){var c=f.cloneNode(true);f.parentNode.replaceChild(c,f);}}
    if(k==="rv"){var r=document.querySelector(".ds-rv-demo [data-rv]");if(!r)return;
      r.classList.remove("in");void r.offsetWidth;setTimeout(function(){r.classList.add("in");},60);}
  });
})();
"""


# ---------------------------------------------------------------- stránka

def build(ctx):
    """Vrátí (HTML stránky, seznam upozornění). ctx připraví pages.py."""
    views, css_src, js_src = ctx["views"], ctx["css"], ctx["js"]
    P = ctx["path"]   # adresa české stránky podle trasy webu, např. P("/contact") -> /contact/
    cs, en, out = ctx["cs"], ctx["en"], ctx["out"]
    fix_links = ctx["map_links"]
    warnings = []

    site_text = visible(" ".join(views.values()) + ctx["footer"])
    for label, cz, eng, _ in IDENTITY:
        if label != "Claim" and visible(cz).strip() not in site_text + ctx["meta_text"]:
            warnings.append(f"{label} „{visible(cz).strip()}“ už na webu není")
    if visible(IDENTITY[0][1]).strip() not in site_text:
        warnings.append("claim už není na úvodní stránce")
    for rule, _, ex in VOICE:
        if ex not in site_text:
            warnings.append(f"ukázka hlasu „{ex}“ už na webu není")
    for k, q in QUOTES.items():
        if q not in css_src and q not in js_src:
            warnings.append(f"zásada „{q}“ už ve stylu není")
    for m in MOTION_CHECK:
        if m not in css_src and m not in js_src:
            warnings.append(f"pohyb se změnil (ve stylu ani skriptu není {m!r}), upravte sekci Pohyb")
    assert ICO in views["v-contact"], "ds.py: IČO na stránce Kontakt nesedí"

    def q(key):
        return f'<p class="ds-q">{esc(QUOTES[key])}</p>'

    home, about, dp, contact = views["v-home"], views["v-about"], views["v-svc-dp"], views["v-contact"]
    # kusy stránek webu, odkazy převedené na skutečné adresy
    case_cards = fix_links('<div class="cards case-cards">\n' + grab(home, r'class="card case-card"', 0) + "\n"
                           + grab(home, r'class="card case-card"', 1) + "\n</div>")
    svc_cards = fix_links(grab(home, r'class="svc-cards svc-three"'))
    notes = fix_links(grab(home, r'class="notes" data-notes'))
    faq = fix_links(grab(dp, r'class="faq"'))
    polaroid = fix_links(grab(about, r'class="paper polaroid"'))
    quote = fix_links(grab(about, r'<blockquote class="q"'))
    prt = fix_links(grab(about, r'<figure class="print"'))
    acard = fix_links(grab(about, r'class="acard"'))
    sectors = fix_links(grab(home, r'class="clients2"'))
    crumb = fix_links(grab(views["v-case-coinmate"], r'class="crumb"'))
    hx = fix_links(grab(home, r'class="hx-fig"'))
    lap = fix_links(grab(home, r'data-lap'))
    fields = fix_links('<div class="ct-form">\n' + grab(contact, r'class="ct-row2"') + "\n"
                       + grab(contact, r'<label class="ct-f"', has="<span>Služba") + "\n"
                       + grab(contact, r'<label class="ct-f"', has="<textarea") + "\n</div>")
    cta = fix_links(grab(home, r'class="panel deep canvas"'))
    note_one = grab(home, r'class="note"')

    # ------------------------------------------------ identita
    ident_cards = "".join(
        f'<div class="ds-card"><span class="ds-k">{label}</span><p class="ds-big">{cz}</p>'
        f'<p class="ds-en">{eng}</p><p class="ds-use">{use}</p></div>'
        for label, cz, eng, use in IDENTITY)
    svc_rows = "".join(
        f'<tr><td>{esc(cs["services"][k]["name"])}</td><td>{esc(en["services"][k]["name"])}</td>'
        f'<td>od {cs["price"](min(o[2] for o in cs["services"][k]["offers"]))}'
        f'{" " + cs["unit_text"] if any(o[3] for o in cs["services"][k]["offers"]) else ""}</td></tr>'
        for k in ("dp", "audit", "fractional"))
    addr = cs["business"]["address"]
    identita = f'''
  <section id="identita">
    <div class="wrap">
      <p class="eyebrow sig">Identita</p>
      <h2>Kdo, co a jak se to jmenuje.</h2>
      <p class="lede">Hlavní věta, podtitul a firemní údaje. Stejné texty jsou v titulcích, v obrázcích pro sdílení a ve strukturovaných datech.</p>
      <div class="ds-grid two">{ident_cards}</div>
      <div class="ds-card" style="margin-top:16px">
          <span class="ds-k">Služby</span>
          <div class="ds-scroll"><table class="ds-table"><thead><tr><th>Česky</th><th>Anglicky</th><th>Cena</th></tr></thead><tbody>{svc_rows}</tbody></table></div>
          <p class="ds-use" style="margin-top:12px">Decision Prototype se nepřekládá. Platí se za projekt, ne za hodiny. Ceny jsou v korunách i v anglické verzi.</p>
      </div>
      <div class="ds-grid two" style="margin-top:16px">
        <div class="ds-card">
          <span class="ds-k">Firemní údaje</span>
          <dl class="ds-dl"><dt>Firma</dt><dd>Pavel Kroupa</dd><dt>Sídlo</dt><dd>{esc(addr["streetAddress"])}, {esc(addr["postalCode"])} {esc(addr["addressLocality"])}</dd>
          <dt>IČO</dt><dd>{ICO}</dd><dt>DPH</dt><dd>Neplátce DPH</dd><dt>Země</dt><dd>Česká republika</dd></dl>
        </div>
        <div class="ds-card">
          <span class="ds-k">Kontakt</span>
          <dl class="ds-dl"><dt>E-mail</dt><dd>info@pavelkroupa.com</dd><dt>Hovor</dt><dd><a href="https://cal.com/pavelkroupa" rel="noopener">cal.com/pavelkroupa</a></dd>
          <dt>LinkedIn</dt><dd><a href="https://www.linkedin.com/in/pavelkroupa/" rel="noopener">linkedin.com/in/pavelkroupa</a></dd>
          <dt>Působí</dt><dd>Praha a Amsterdam, online</dd><dt>Web</dt><dd>pavelkroupa.com (www přesměruje sem), anglicky /en/</dd></dl>
        </div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ hlas
    voice_cards = "".join(
        f'<div class="ds-card"><h3>{esc(rule)}</h3><p>{esc(why)}</p><p class="ds-ex">{esc(sample)}</p></div>'
        for rule, why, sample in VOICE)
    fmt_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in FORMATS)
    hlas = f'''
  <section id="hlas">
    <div class="wrap">
      <p class="eyebrow sig">Hlas</p>
      <h2>Krátce, konkrétně, za sebe.</h2>
      <p class="lede">Pravidla vyčtená z textů webu. Úplná pravidla jsou ve vaultu v souboru Hlas — pravidla.md.</p>
      <div class="ds-grid">{voice_cards}
        <div class="ds-card"><h3>Čeština není překlad</h3><p class="ds-q">CS není překlad. Psáno česky od nuly ze stejného faktu.</p>
          <p>Angličtina podle Nielsen Norman Group: krátké věty, činný rod, to hlavní na začátku, čísla číslicemi, americký pravopis.</p></div>
      </div>
      <div class="ds-card" style="margin-top:16px">
        <span class="ds-k">Zápis</span>
        <div class="ds-scroll"><table class="ds-table"><thead><tr><th>Co</th><th>Česky</th><th>Anglicky</th></tr></thead><tbody>{fmt_rows}</tbody></table></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ logo
    mark = re.search(r'<svg class="pk".*?</svg>', ctx["header"], re.S).group(0)
    logo = f'''
  <section id="logo">
    <div class="wrap">
      <p class="eyebrow sig">Logo</p>
      <h2>Značka pk a lepítko s fajfkou.</h2>
      <p class="lede">Dvě podoby jedné značky. Písmena pk s linkou do hlavičky a dokumentů, samotné lepítko do ikon.</p>
      <div class="ds-tiles">
        <figure class="ds-tile"><div class="ds-on-light"><img src="/logo/pk/pk-svetle.svg" alt="Logo pk, světlá verze" width="288" height="322" loading="lazy"></div><figcaption><b>pk, světlá</b>Na bílém a světlém podkladu.</figcaption></figure>
        <figure class="ds-tile"><div class="ds-on-dark"><img src="/logo/pk/pk-tmave.svg" alt="Logo pk, tmavá verze" width="288" height="322" loading="lazy"></div><figcaption><b>pk, tmavá</b>Bílá písmena, šedá linka #5C5C60.</figcaption></figure>
        <figure class="ds-tile"><div class="ds-on-check"><img src="/logo/pk/pk-svetle-ctverec.svg" alt="Logo pk ve čtverci, světlé" width="500" height="500" loading="lazy" style="border-radius:10px"></div><figcaption><b>Čtverec, světlý</b>S bílým podkladem. Logo firmy ve vyhledávání (pk-svetle-ctverec-400.png).</figcaption></figure>
        <figure class="ds-tile"><div class="ds-on-check"><img src="/logo/pk/pk-tmave-ctverec.svg" alt="Logo pk ve čtverci, tmavé" width="500" height="500" loading="lazy" style="border-radius:10px"></div><figcaption><b>Čtverec, tmavý</b>S černým podkladem #111111.</figcaption></figure>
      </div>
      <div class="ds-grid two">
        <div class="ds-card"><span class="ds-k">V hlavičce webu</span>
          <div class="ds-mark" style="margin:6px 0 16px">{mark}</div>
          <p>Vložené přímo do stránky, barvy bere z tokenů: písmena a linka <code>--ink</code>, v tmavém režimu linka #5C5C60. Výška 30 px, do 480 px šířky okna 26 px. Na mobilu zůstává jen pk, jméno čte čtečka obrazovky.</p></div>
        <div class="ds-card"><span class="ds-k">Pravidla</span>
          <ul class="ds-list"><li>Barvy loga: žlutá #FFCE1B, černá #111111, bílá a šedá linka #5C5C60 na tmavém podkladu.</li>
          <li>Lepítko je natočené o 6° proti směru hodinových ručiček. Fajfka je tažená rukou, ne geometrická.</li>
          <li>Na tmavém podkladu tmavá verze. Lepítko zůstává žluté.</li>
          <li>Loga se nepřebarvují a nedeformují. Vždy ze souborů v <code>/logo/</code>.</li></ul></div>
      </div>
      <div class="ds-tiles">
        <figure class="ds-tile"><div class="ds-on-check"><img src="/logo/logo.svg" alt="Lepítko s fajfkou" width="452" height="452" loading="lazy"></div><figcaption><b>Lepítko</b>logo.svg. Základ favikony a ikon aplikace.</figcaption></figure>
        <figure class="ds-tile"><div class="ds-on-check"><img src="/logo/logo-pk.svg" alt="Lepítko s fajfkou a podpisem pk" width="452" height="452" loading="lazy"></div><figcaption><b>Lepítko s podpisem</b>logo-pk.svg. Pk vpravo dole.</figcaption></figure>
        <figure class="ds-tile"><div class="ds-on-check"><img src="/logo/logo-na-cerne-1024.png" alt="Lepítko na černém čtverci" width="1024" height="1024" loading="lazy"></div><figcaption><b>Na černé</b>PNG 1024 px, také na bílé a se stínem.</figcaption></figure>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ ikony
    ikony = '''
  <section id="ikony">
    <div class="wrap">
      <p class="eyebrow sig">Ikony</p>
      <h2>Favikona a ikony aplikace.</h2>
      <p class="lede">Lepítko s fajfkou. Prohlížeč si vezme SVG, starší prohlížeče ICO, telefony PNG.</p>
      <div class="ds-grid two">
        <div class="ds-card"><span class="ds-k">V prohlížeči</span>
          <div class="ds-tab"><img src="/favicon.svg" alt="" width="16" height="16"><span>Pavel Kroupa · Definice produktu a funkční prototypy</span></div>
          <div class="ds-bar" title="theme-color #FFCE1B"></div>
          <p style="margin-top:14px">Barva lišty prohlížeče na telefonu (theme-color) je žlutá #FFCE1B.</p></div>
        <div class="ds-card"><span class="ds-k">Soubory</span>
          <div class="ds-icons">
            <figure><img src="/favicon.svg" alt="Favikona SVG 16 px" width="16" height="16"><figcaption>16</figcaption></figure>
            <figure><img src="/favicon.svg" alt="Favikona SVG 32 px" width="32" height="32"><figcaption>32<br>favicon.svg</figcaption></figure>
            <figure><img src="/favicon.ico" alt="Favikona ICO" width="32" height="32"><figcaption>32<br>favicon.ico</figcaption></figure>
            <figure><img src="/apple-touch-icon.png" alt="Ikona pro iPhone" width="60" height="60" loading="lazy" style="border-radius:13px"><figcaption>180<br>apple-touch-icon</figcaption></figure>
            <figure><img src="/icon-192.png" alt="Ikona aplikace 192 px" width="64" height="64" loading="lazy"><figcaption>192<br>icon-192</figcaption></figure>
            <figure><img src="/icon-512.png" alt="Ikona aplikace 512 px" width="80" height="80" loading="lazy"><figcaption>512<br>icon-512</figcaption></figure>
          </div>
          <p style="margin-top:14px">Ikona pro iPhone má bílý podklad, Android bere ikony 192 a 512 px ze souboru site.webmanifest.</p></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ barvy
    def sw(name, role, chip=None):
        c = chip or '<span class="ds-chip"><i></i><i></i></span>'
        return (f'<li data-t="{name}">{c}<span class="ds-name"><b>{name}</b><span>{esc(role)}</span></span>'
                f'<span class="ds-vals"><button type="button" class="ds-val l">…</button>'
                f'<button type="button" class="ds-val d">…</button></span></li>')
    groups = "".join(f'<div class="ds-tg"><h3>{g}</h3><ul class="ds-sw">{"".join(sw(n, r) for n, r in items)}</ul></div>'
                     for g, items in TOKENS)
    others = "".join(sw(n, r, chip) for n, r, chip in OTHER_TOKENS)
    barvy = f'''
  <section id="barvy">
    <div class="wrap">
      <p class="eyebrow sig">Barvy</p>
      <h2>Bílá, černá a žlutý fix.</h2>
      <p class="lede">Hodnoty se načítají přímo ze stylu webu. ☀ světlý režim, ☾ tmavý. Kliknutím hodnotu zkopírujete.</p>
      {q("tabule")}
      {groups}
      <div class="ds-tg"><h3>Stín a písmo</h3><ul class="ds-sw">{others}</ul></div>
      <div class="ds-grid two">
        <div class="ds-card"><span class="ds-k">Mimo tokeny</span>
          <ul class="ds-list"><li>#D93025: chybně vyplněné pole ve formuláři.</li>
          <li>Žlutá na 45 % (rgba(255,206,27,.45)): rámeček pole, do kterého se píše.</li>
          <li>Žlutá na 55 %: páska na fotkách.</li>
          <li>#5C5C60: linka v logu pk v tmavém režimu.</li></ul></div>
        <div class="ds-card"><span class="ds-k">Ze starších verzí</span>
          <p>Ve stylu zůstaly proměnné, které už se na webu neprojeví, protože je přebíjí pozdější pravidla: {", ".join(f"<code>{n}</code>" for n in LEGACY)}. Při úklidu ve vaultu je lze smazat.</p></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ písmo
    specs = [
        ("h1, nadpis stránky", '<h1 data-spec-el>Pomáhám týmům rozhodnout, co postavit.</h1>'),
        ("h2, nadpis sekce", '<h2 data-spec-el>Rozhodnutí a jejich důvody.</h2>'),
        ("h3, nadpis karty", '<h3 data-spec-el>Jedna aplikace pro mnoho klinik</h3>'),
        ("lede, úvodní odstavec", '<p class="lede" data-spec-el>Vyberte ten, který se podobá vašemu problému.</p>'),
        ("eyebrow, štítek nad nadpisem", '<p class="eyebrow sig" data-spec-el>Vybrané případy</p>'),
        ("p, běžný text", '<p data-spec-el>Před spoluprací si s vámi ujasním, jaký problém řešíme, kdo o něm rozhoduje a čeho chceme dosáhnout.</p>'),
        ("lepítko, ruční písmo", '<p class="ds-hand" data-spec-el style="font-size:21px;font-weight:500;line-height:1.32">Mluví se a mluví. Co dělat, všichni tuší.</p>'),
    ]
    spec_html = "".join(f'<div class="ds-spec" data-spec><span class="ds-k">{label}</span>{el}<span class="ds-m"></span></div>'
                        for label, el in specs)
    weights = lambda fam: "".join(f'<span class="{fam}" style="font-weight:{w}">{w}</span>' for w in (400, 500, 600, 700, 800))
    pismo = f'''
  <section id="pismo">
    <div class="wrap">
      <p class="eyebrow sig">Písmo</p>
      <h2>Systémové písmo a ruka.</h2>
      <p class="lede">Na všechno systémové bezpatkové písmo. Shantell Sans jen na věci, které píše ruka.</p>
      <div class="ds-grid two">
        <div class="ds-card"><span class="ds-k">Systémové písmo, <code>--display</code> a <code>--text</code></span>
          <p class="ds-glyphs ds-sys" style="font-weight:600">Aa Čč Řř Žž 1234</p>
          <p class="ds-weights">{weights("ds-sys")}</p>
          <p>Na Applu SF Pro, jinde Helvetica Neue, Helvetica nebo Arial. Nic se nestahuje, stránka je hned čitelná.</p></div>
        <div class="ds-card"><span class="ds-k">Shantell Sans, <code>--hand</code></span>
          <p class="ds-glyphs ds-hand" style="font-weight:600">Aa Čč Řř Žž 1234</p>
          <p class="ds-weights">{weights("ds-hand")}</p>
          <p>Lepítka, popisky kreseb, polaroid. Z vlastního serveru (licence SIL OFL 1.1), tloušťka 400 až 800. Čeština si stáhne jen malý výřez s háčky a čárkami.</p></div>
      </div>
      <div class="ds-card" style="margin-top:16px">
        <span class="ds-k">Velikosti při současné šířce okna: <span data-vw></span>. Nadpisy a úvodní odstavec rostou se šířkou okna.</span>
        {spec_html}
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ vizuální jazyk
    dims = [("Šířka obsahu", ".wrap|maxWidth"), ("Okraj po stranách", ".wrap|paddingLeft"),
            ("Odsazení sekce", "section.ds-probe|paddingTop"), ("Rádius karty", ".ds-stage .card|borderTopLeftRadius"),
            ("Rádius formuláře", ".ds-stage .ct-form|borderTopLeftRadius"), ("Rádius pole", ".ds-stage .ct-f input|borderTopLeftRadius"),
            ("Rádius tlačítka", ".ds-stage .btn|borderTopLeftRadius"), ("Rádius lepítka", ".ds-stage .note|borderTopLeftRadius"),
            ("Rádius papíru", ".ds-stage .paper|borderTopLeftRadius"), ("Rozteč teček", ".dots|backgroundSize")]
    dim_rows = "".join(f'<tr><td>{a}</td><td data-dim="{b}"></td></tr>' for a, b in dims)
    jazyk = f'''
  <section id="jazyk" class="canvas dots">
    <div class="wrap">
      <p class="eyebrow sig">Vizuální jazyk</p>
      <h2>Tabule, fix, papír a sklo.</h2>
      <p class="lede">Web vypadá jako tabule po workshopu. Čisté plochy jsou z Applu, ruční věci zůstávají ruční.</p>
      <div class="ds-grid two">
        <div class="ds-card"><h3>Tabule</h3>{q("tabule")}
          <div class="ds-chips"><i style="background:#FFFFFF"></i><i style="background:#1D1D1F"></i><i style="background:#FFCE1B"></i></div></div>
        <div class="ds-card"><h3>Tečky</h3>{q("tecky")}{q("tecky1")}{q("tecky2")}{q("tecky3")}
          <div class="ds-board dots"><a class="btn btn-line" href="#tecky">Na tečkách leží věc</a></div></div>
        <div class="ds-card"><h3>Žlutý fix</h3>{q("fix")}{q("fixdark")}
          <div class="ds-light"><p>Pomáhám týmům <span class="fix">rozhodnout</span>.</p></div>
          <div class="panel ds-panel"><p>Na černé jen <span class="fix">podtržení</span>.</p></div></div>
        <div class="ds-card"><h3>Papír</h3>{q("papir")}{q("fotka")}
          <div class="ds-print">{prt}</div></div>
        <div class="ds-card"><h3>Sklo a ruka</h3>{q("sklo")}{q("ruka2")}{q("ruka")}
          <div class="ds-pair"><div class="ds-glasscard">Karta je ze skla<small>--glass, --glass-shadow</small></div>{note_one}</div></div>
        <div class="ds-card"><h3>Kresba a ilustrace</h3>{q("linka")}
          <p>Ručně kreslené jsou linka v úvodu, šipka pod fotkou z workshopu a obrazovka notebooku: čáry tažené fixem a popisky ručním písmem.</p>
          <p>Ilustrace služeb a ikony oborů jsou čisté a šedé, bez rukopisu. Ukázky jsou u komponent Karta služby a Obory.</p></div>
      </div>
      <div class="ds-card ds-hx" style="margin-top:16px"><h3>Ruční linka v úvodu</h3>{q("hero")}
        {hx}
        <div class="ds-replay"><button type="button" class="btn btn-line" data-replay="hx">Přehrát znovu</button></div></div>
      <div class="ds-grid two">
        <div class="ds-card"><h3>Rozvržení</h3>{q("stred")}
          <p>Nadpis sekce, štítek nad ním a úvodní odstavec jsou na středu. Text, karty a seznamy se čtou zleva.</p></div>
        <div class="ds-card"><h3>Rozměry</h3><div class="ds-scroll"><table class="ds-table ds-dims"><tbody>{dim_rows}</tbody></table></div></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ pohyb
    pohyb = f'''
  <section id="pohyb">
    <div class="wrap">
      <p class="eyebrow sig">Pohyb</p>
      <h2>Věci se nalepí, dopíšou a dokreslí.</h2>
      <p class="lede">Pohyb ukazuje, co se děje. Kdo má v systému zapnutý omezený pohyb, vidí rovnou konečný stav.</p>
      <div class="ds-grid two">
        <div class="ds-card"><h3>Odhalení při posunu</h3><p>Nadpisy, odstavce a karty vyjedou o 16 px a zprůhlední se za 0,7 s, křivka cubic-bezier(.2,.7,.3,1). Sousední prvky se zpozdí po 55 ms.</p>
          <div class="ds-stage ds-rv-demo"><div data-rv>Vyjede a zprůhlední se</div></div>
          <div class="ds-replay"><button type="button" class="btn btn-line" data-replay="rv">Přehrát znovu</button></div></div>
        <div class="ds-card"><h3>Měnící se slovo</h3><p>Slovo s fixem se smaže a napíše znovu, písmeno po písmenu. Mezi slovy asi 2 s. Na webu v úvodu a u Decision Prototype.</p>
          <div class="ds-stage"><h2 style="margin:0;font-size:clamp(28px,3.4vw,40px)">Každé kolo začíná<br><span class="tw"><span class="fix tw-loop" data-words="iterací|workshopem|rozhovorem">iterací</span><span class="tw-c"></span></span></h2></div></div>
        <div class="ds-card"><h3>Najetí myší</h3><p>Karta se zvětší o 1,5 % (0,5 s), tlačítko povyskočí o 1 px, šipka odkazu popojede o 4 px. Pás log a fotek jede dokola a pod myší se zastaví.</p>
          <div class="ds-stage"><div class="row"><a class="btn btn-fill" href="#pohyb">Tlačítko</a><a class="lnk" href="#pohyb">Odkaz se šipkou</a></div></div></div>
        <div class="ds-card"><h3>Lepítka</h3>{q("nalepeni")}<p>Přiletí o 30 px shora, natočená o 7° víc, a dosednou za 0,46 s. Každé další o 260 ms později. Ukázka je u komponenty Lepítka.</p></div>
      </div>
      <div class="ds-card" style="margin-top:16px"><h3>Kresba notebooku</h3><p>Notebook se otevře, nakreslí se problém, řešení a tok obrazovek, kurzor klikne. Spustí se, když je kresba z poloviny vidět.</p>
        {lap}</div>
    </div>
  </section>'''

    # ------------------------------------------------ komponenty
    comps = "".join([
        demo("Tlačítka", "Plné pro hlavní akci, nejvýš jedno v sekci. Obrysové ze skla pro vedlejší. Na černém panelu je plné tlačítko žluté.",
             f'<div class="row"><a class="btn btn-fill" href="{P("/contact")}">Domluvit 30minutový hovor</a>'
             f'<a class="btn btn-line" href="{P("/portfolio")}">Ukázky práce</a></div>'
             '<div class="panel ds-foot"><div class="row">'
             f'<a class="btn btn-fill" href="{P("/contact")}">Domluvit 30minutový hovor</a></div></div>'),
        demo("Odkazy", "Odkaz v textu a pod kartou: žluté podtržení a šipka. Drobečková navigace nad nadpisem detailu.",
             f'<p style="margin:0 0 16px"><a class="lnk" href="{P("/portfolio")}">Všechny případy</a></p>' + crumb),
        demo("Nadpis sekce", "Štítek, nadpis a úvodní odstavec. Fix nejvýš dvakrát na stránku.",
             '<p class="eyebrow sig">Vybrané případy</p><h2>Rozhodnutí a jejich <span class="fix">důvody</span>.</h2>'
             '<p class="lede">Vyberte ten, který se podobá vašemu problému.</p>'),
        demo("Lepítka", "Situace, ve kterých klient je. Jen na černém panelu, ručním písmem, každé jinak natočené.",
             f'<div class="panel">{notes}<div class="ds-replay" style="text-align:center"><button type="button" class="btn btn-line" data-replay="notes">Nalepit znovu</button></div></div>',
             src=notes),
        demo("Karta případu", "Logo klienta šedě vpravo nahoře, rok, výsledek jednou větou, odkaz.", case_cards),
        demo("Karta služby", "Ilustrace, název, cena od, jedna věta. Ilustrace se dokreslí, když je karta vidět.", svc_cards),
        demo("Otázky a odpovědi", "Rozbalovací řádky. Text otázek a odpovědí jde i do strukturovaných dat.", faq),
        demo("Seznam s ikonami", "Karta s krátkými body. Žluté kolečko pro ano, šedé pro ne.", f'<div class="acards" style="grid-template-columns:minmax(0,420px)">{acard}</div>', src=acard),
        demo("Obory", "Kde mám zkušenost. Malé šedé ikony, nekřičí. Na mobilu se z nich stanou štítky.", sectors),
        demo("Citát na černé", "Doporučení jako papír položený na tabuli. Původní znění z LinkedInu.", f'<div class="panel">{quote}</div>', src=quote),
        demo("Polaroid", "Portrét jako předmět: papír, natočení, podpis ručním písmem.", f'<div style="padding:10px 0 4px">{polaroid}</div>', src=polaroid),
        demo("Formulář", "Pole s popiskem nad sebou. Při psaní žlutý rámeček, chyba červeně #D93025.", fields),
        demo("Výzva na konci stránky", "Černý panel s jedním žlutým tlačítkem. Na konci každé stránky.", cta, cls="ds-wide"),
    ])
    komponenty = f'''
  <section id="komponenty">
    <div class="wrap">
      <p class="eyebrow sig">Komponenty</p>
      <h2>Skutečné kusy webu.</h2>
      <p class="lede">Ukázky se berou přímo ze stránek webu. Když se změní web, změní se i tady.</p>
      <div class="ds-comps">{comps}</div>
    </div>
  </section>'''

    # ------------------------------------------------ režimy
    rezimy = f'''
  <section id="rezimy" class="ds-center">
    <div class="wrap">
      <p class="eyebrow sig">Režimy</p>
      <h2>Světlý a tmavý režim.</h2>
      <p class="lede">Web se řídí nastavením systému. V hlavičce jde přepnout: ◑ podle systému, ☀ světlý, ☾ tmavý. Volba se pamatuje v prohlížeči.</p>
      <div class="ds-seg" data-ds-theme role="group" aria-label="Vzhled"><button type="button" value="system">◑ Podle systému</button><button type="button" value="light">☀ Světlý</button><button type="button" value="dark">☾ Tmavý</button></div>
      <div class="ds-grid two" style="text-align:left">
        <div class="ds-card"><span class="ds-k">Zásada</span>{q("tmavy")}</div>
        <div class="ds-card"><span class="ds-k">Co se v tmavém režimu mění</span>
          <ul class="ds-list"><li>Plochy a text se otočí, hodnoty jsou u barev.</li><li>Žlutý fix je jen podtržení.</li>
          <li>Karty nemají stín, sklo je tmavé.</li><li>Loga klientů jsou světlá.</li><li>Linka v logu pk je šedá.</li>
          <li>Lepítka, fix a tlačítko na černé zůstávají žluté.</li></ul></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ sdílení
    def og_list(d, prefix):
        return "".join(f'<figure><img src="{prefix}{p.name}" alt="Obrázek pro sdílení {p.stem}" width="1200" height="630" loading="lazy">'
                       f'<figcaption>{prefix}{p.name}</figcaption></figure>' for p in sorted(d.glob("*.png")))
    sdileni = f'''
  <section id="sdileni">
    <div class="wrap">
      <p class="eyebrow sig">Sdílení</p>
      <h2>Obrázky pro sdílení.</h2>
      <p class="lede">1200 × 630 px, jeden pro každou hlavní stránku. Ukáže se v náhledu odkazu na LinkedInu, ve WhatsAppu nebo ve Slacku.</p>
      <h3 style="margin-top:36px">Česky</h3>
      <div class="ds-og">{og_list(out / "og", "/og/")}</div>
      <h3 style="margin-top:36px">Anglicky</h3>
      <div class="ds-og">{og_list(out / "og" / "en", "/og/en/")}</div>
    </div>
  </section>'''

    # ------------------------------------------------ ke stažení
    def files(paths):
        return "".join(f'<li><a href="/{p.relative_to(out).as_posix()}" download>{p.name}</a><span>{size(p)}</span></li>'
                       for p in paths)
    logo_dir = out / "logo"
    font_links = "".join(f'<li><a href="{u}" download>{n}</a><span>{size(out / u.lstrip("/"))}</span></li>'
                         for n, u in ctx["font_urls"].items())
    stazeni = f'''
  <section id="stazeni">
    <div class="wrap">
      <p class="eyebrow sig">Ke stažení</p>
      <h2>Soubory.</h2>
      <div class="ds-grid">
        <div class="ds-card"><span class="ds-k">Logo pk</span><ul class="ds-files">{files(sorted((logo_dir / "pk").glob("*")))}</ul></div>
        <div class="ds-card"><span class="ds-k">Lepítko</span><ul class="ds-files">{files(sorted(p for p in logo_dir.glob("*") if p.is_file()))}</ul></div>
        <div class="ds-card"><span class="ds-k">Ikony</span><ul class="ds-files">{files([out / n for n in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "site.webmanifest")])}</ul></div>
        <div class="ds-card"><span class="ds-k">Písmo Shantell Sans</span><ul class="ds-files">{font_links}</ul>
          <p style="margin-top:12px">Celá rodina na <a href="https://fonts.google.com/specimen/Shantell+Sans" rel="noopener">Google Fonts</a>, licence SIL OFL 1.1.</p></div>
      </div>
    </div>
  </section>'''

    # ------------------------------------------------ v kódu
    kod = '''
  <section id="kod">
    <div class="wrap">
      <p class="eyebrow sig">V kódu</p>
      <h2>Kde co je.</h2>
      <div class="ds-grid two">
        <div class="ds-card"><span class="ds-k">Soubory</span>
          <dl class="ds-dl"><dt>Styl a tokeny</dt><dd><code>web/src/index.html</code>, proměnné na <code>:root</code>. Vzniká ve vaultu (<code>build_v5b.py</code> a kola).</dd>
          <dt>Stránky</dt><dd><code>web/build/pages.py</code>, výstup v kořeni repozitáře</dd>
          <dt>Tato stránka</dt><dd><code>web/build/ds.py</code></dd>
          <dt>Písmo</dt><dd><code>web/build/fonts/web/</code></dd>
          <dt>Loga</dt><dd><code>logo/</code>, ve vaultu <code>export_pk.py</code> a <code>export_logo.py</code></dd>
          <dt>Sdílení</dt><dd><code>og/</code>, česky z <code>og.py</code> ve vaultu, anglicky z <code>web/build/og_en.py</code></dd>
          <dt>Hosting</dt><dd>GitHub Pages z větve <code>main</code>, doména v souboru <code>CNAME</code>. Cloudflare jen DNS.</dd></dl></div>
        <div class="ds-card"><span class="ds-k">Nová komponenta</span>''' + q("tokeny") + '''
          <ul class="ds-list"><li>Barvy jen z tokenů, žádné nové hodnoty.</li><li>Vyzkoušet ve světlém i tmavém režimu.</li>
          <li>Na tečkách jen neprůhledné věci.</li><li>Pohyb vypnout při omezeném pohybu (prefers-reduced-motion).</li>
          <li>Na 320 px široké obrazovce nic nepřetéká do strany.</li></ul></div>
      </div>
    </div>
  </section>'''

    toc = "".join(f'<a href="#{a}">{t}</a>' for a, t in TOC)
    hero = f'''
  <section class="canvas dots ds-hero">
    <div class="wrap">
      <p class="eyebrow sig">Interní stránka</p>
      <h1>Design <span class="fix">systém</span></h1>
      <p class="lede">Jak web pavelkroupa.com vypadá, mluví a hýbe se. Barvy, písmo a komponenty se berou přímo ze stylu a stránek webu.</p>
      <nav class="ds-toc" aria-label="Obsah">{toc}</nav>
      <p class="ds-note">Jen pro vnitřní potřebu. Nikde na ni nevede odkaz a vyhledávače ji nemají indexovat.</p>
    </div>
  </section>'''

    body = hero + identita + hlas + logo + ikony + barvy + pismo + jazyk + pohyb + komponenty + rezimy + sdileni + stazeni + kod
    page = f'''<!doctype html>
<html lang="cs" data-route="/ds">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Design systém · Pavel Kroupa</title>
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#FFCE1B">
{ctx["early_theme"]}
{ctx["preload"]}
<link rel="stylesheet" href="{ctx["css_url"]}">
<style>{ctx["minify_css"](CSS)}</style>

{ctx["header"]}

<main class="ds">
<div id="v-ds">
{body}
</div>
</main>

<section class="ds-probe" hidden></section>

{ctx["footer"]}

<script src="{ctx["js_url"]}"></script>
<script>{ctx["minify_js"](JS)}</script>
</html>
'''
    assert "data:image" not in page and 'href="#/' not in page
    return page, warnings
