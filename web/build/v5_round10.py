# Round 10 (4. 10. 2026): menší šedé miniatury služeb, CTA jako otázka, nové texty případů,
# "Na workshopu vzniká" nad fotku, nad notebook "vznikne funkční prototyp", nový popisek notebooku.

# ---------- nadpisy: přepisování nad fotku workshopu, nad notebookem funkční prototyp
_tw = re.search(r'<h2 class="tw-h".*?</h2>', h, re.S).group(0)
h = h.replace(_tw, '<h2 class="lap-h">Pak z toho vznikne <span class="fix">funkční prototyp</span>.</h2>', 1)
h = rep(h, '<h2>Rozhoduje se u stěny, ne nad slajdy.</h2>', _tw + '<p class="lede shot-lede">Rychle a s lidmi, kteří rozhodují.</p>')
h = rep(h, 'Od problému k toku obrazovek. Z jedné obrazovky prototyp, na který se dá kliknout, a zpátky do toku, podle kterého staví vývoj.\n    <button type="button" class="lap-re">Přehrát znovu</button>',
        'Od problému k business zadání: user flow, customer journey a prototyp, na který se dá kliknout.\n    <button type="button" class="lap-re">Přehrát znovu</button>')

CARD_TXT = [
    ('<h3 class="card-title">Nový směr za čtyři iterace</h3>', '<h3 class="card-title">Nový business směr za čtyři iterace</h3>'),
    ('<span class="card-proves">Nejdřív prototyp, potom zadání.</span>', '<span class="card-proves">Nejdřív funkční prototyp, potom zadání.</span>'),
    ('<span class="card-proves">Nová identita spuštěná 1. 10. 2026.</span>', '<span class="card-proves">Rebranding spuštěn 1. 10. 2026.</span>'),
    ('<span class="card-proves">Nejdřív systém, potom obrazovky.</span>', '<span class="card-proves">Škálovatelný design systém, white label.</span>'),
    ('<h3 class="card-title">Dva dny, jedno pořadí priorit</h3>', '<h3 class="card-title">Dvoudenní prioritizace business backlogu</h3>'),
    ('<span class="card-proves">Rozhodnout to na místě.</span>', '<span class="card-proves">Rozhodnuto na místě, nastavená strategie.</span>'),
    ('BRENO přes WPP', 'BRENO &middot; 2023'),
    ('<h1><span class="fix">Nový směr</span> za čtyři iterace.</h1>', '<h1>Nový <span class="fix">business směr</span> za čtyři iterace.</h1>'),
    ('<h1>Dva dny, <span class="fix">jedno pořadí</span> priorit.</h1>', '<h1>Dvoudenní <span class="fix">prioritizace</span> business backlogu.</h1>'),
    ('>Všechny případy a kdo je potvrdí<', '>Všechny případy<'),
    ('<h2>Napište mi, kde jste se zasekli. Když nebudu ten pravý, řeknu vám to.</h2>', '<h2>Kde jste se zasekli?</h2>'),
    ('Třicet minut. Bez prezentace a bez složitých nabídek.', 'Napište mi. Na třicetiminutovém hovoru vám řeknu, jestli vám můžu pomoct. Bez prezentace a bez složitých nabídek.'),
    ('V Praze, v Amsterdamu nebo online. Když nebudu ten pravý, řeknu vám to.</p>', 'V Praze, v Amsterdamu nebo online.</p>'),
]

CSS_R10 = '''
/* ---------- v5 kolo 10 ---------- */
.svc-thumb{max-width:118px;margin:0 0 12px}
.svc-thumb .ill{filter:grayscale(1);opacity:.7}
@media(max-width:560px){.svc-thumb{max-width:104px}}
.shot-sec .tw-h{margin-bottom:10px}
.shot-lede{margin:0 auto 40px}
.lap-h{text-align:center;margin:0 auto 30px}
.lap-cap{max-width:46ch}
.lap-re{display:table;margin:14px auto 0}
'''

def post_patch10(out):
    for a, b in CARD_TXT:
        assert a in out, a[:70]
        out = out.replace(a, b)
    # přepisování nadpisu už nečeká na notebook, spustí se, když je nadpis vidět
    out = rep(out, '''var lap=document.querySelector("[data-lap]");
    if(lap){new MutationObserver(function(){if(lap.classList.contains("play"))run();}).observe(lap,{attributes:true,attributeFilter:["class"]});
      if(lap.classList.contains("play"))run();}''',
        '''if("IntersectionObserver" in window){var tio=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.target.offsetParent!==null){run();tio.disconnect();}});},{threshold:.6});tio.observe(w);}else run();''')
    i = out.rindex('</style>', 0, out.index('<header'))
    return out[:i] + CSS_R10 + out[i:]
