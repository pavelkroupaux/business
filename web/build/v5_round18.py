# Round 18 (5. 10. 2026, Claude Code): opravy, které vznikly v repozitáři, aby je další build nepřepsal.
# - Leeaf 2020–2023 (bylo 2021–2023)
# - Heirloom: zástupná citace pryč, doplní se později
# - O mně: galerie bez zástupných rámečků „[FOTKA: …]“, místo nich mapa prototypu (src/img/mapa-prototypu.jpg)
# - popisky fotek v galerii česky, odkaz na logo BRENO bez názvu souboru
# - hlavička: na mobilu jen logo pk (se jménem přetékala do strany), jméno zůstává pro čtečky obrazovky
# - kontaktní formulář se vejde i na 320 px
# - nejmenší telefony (do 360 px): o něco menší nadpisy, dlouhá slova sahala až do okraje
# - omezený pohyb: notebook a infografiky služeb se ukážou v konečném stavu (dřív zůstaly prázdné)
# - slovník EN→CS z verze 4 pryč: přepínač jazyka je skrytý, slovník se nikdy nepoužil a jeho staré ceny
#   v eurech mohli roboti číst jako platné. Anglická verze se dělá zvlášť (web/build/en.py v repozitáři).
import base64 as _b64_18, re as _re_18

_MAP18 = _b64_18.b64encode(open(B + 'src/img/mapa-prototypu.jpg', 'rb').read()).decode()


CSS_R18 = '''
/* ---------- v5 kolo 18: na mobilu jen logo pk, jméno zůstává pro čtečky obrazovky ---------- */
@media(max-width:480px){
  .top .mark .mark-t{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
  .top .mark .pk{display:block}
}
/* kontakt: na 320 px se formulář nevešel, pole se teď smí zúžit */
.ct-form,.ct-card,.ct-f{min-width:0}
.ct-f input,.ct-f textarea,.ct-f select{min-width:0;width:100%;box-sizing:border-box}
/* nejmenší telefony: dlouhá slova v nadpisech (spolupracovat, Recommendations) by sahala až do okraje */
@media(max-width:360px){h1{font-size:40px}h2{font-size:31px}}
/* omezený pohyb: notebook a infografiky služeb rovnou v konečném stavu. Pravidlo *{animation:none!important}
   jinak vypne i jejich zkrácené animace (.lap *, .ill * na 1 ms) a zůstane prázdný notebook a nevyplněné infografiky. */
@media(prefers-reduced-motion:reduce){
  .lap.play .lid{animation-name:lapopen!important}
  .lap.play .d{animation-name:lapdraw!important}
  .lap.play .f{animation-name:lapfade!important}
  .lap.play .cur,.lap2.play .cur2{animation-name:lapcur!important}
  .lap.play .rip,.lap2.play .rip2{animation-name:laprip!important}
  .lap.play .btnf,.lap2.play .btnf2{animation-name:lapbtn!important}
  .lap.play .s1{animation-name:lapout!important}
  .lap.play .s2{animation-name:lapin,lapshrink!important}
  .lap2.play .z-diag{animation-name:zin,zout!important}
  .lap2.play .z-s1{animation-name:s1in,s1out!important}
  .ill.on .ln{animation-name:lapdraw!important}
  .ill.on .ia{animation-name:illin!important}
  .ill.on .dfill{animation-name:dfill!important}
  .ill.on .don,.ill.on .numt{animation-name:don!important}
  .ill.on .wk{animation-name:wk!important}
  .ill.on .prog{animation-name:prog!important}
  .ill.on .num{animation-name:numon!important}
  .lap.play *,.ill.on *{animation-fill-mode:forwards!important}
}
'''


def post_patch18(out):
    out = rep(out, 'Leeaf &middot; 2021&ndash;2023', 'Leeaf &middot; 2020&ndash;2023', 5)
    out = rep(out, '      <p class="case-note">[CITACE OD NĚKOHO, KDO TO VIDĚL]</p>\n', '')
    out = rep(out, '<figure class="print ph"><span>[FOTKA: prototyp na obrazovce]</span></figure>'
                   '<figure class="print ph"><span>[FOTKA: workshop s týmem]</span></figure>',
              '<figure class="print"><img loading="lazy" src="data:image/jpeg;base64,' + _MAP18 + '" '
              'alt="Mapa prototypu pro Heirloom: všechny obrazovky a cesty mezi nimi, rozdělené podle rolí" width="720" height="480"></figure>')
    out = rep(out, 'alt="A workshop room with canvases, sticky notes and whiteboards covering the walls"',
              'alt="Místnost po workshopu: stěny plné pláten, lepítek a tabulí"')
    out = rep(out, 'alt="A workshop room after a session: a whiteboard, sticky notes and paper on the table"',
              'alt="Místnost po workshopu: tabule, lepítka a papíry na stole"')
    out = rep(out, 'aria-label="logo-breno-dark"', 'aria-label="BRENO"')
    # hlavička na mobilu: logo pk se jménem přetékalo do strany (390 px), jméno zůstává pro čtečky obrazovky
    out = rep(out, '</svg>Pavel Kroupa</a>', '</svg><span class="mark-t">Pavel Kroupa</span></a>')
    i = out.rindex('</style>', 0, out.index('<header'))
    out = out[:i] + CSS_R18 + out[i:]
    m = _re_18.search(r'\nvar CS = \{\n.*?\n\};\n', out, _re_18.S)
    assert m, 'kolo 18: slovník CS nenalezen'
    out = out[:m.start()] + '\nvar CS = {};  /* slovník EN→CS z verze 4 smazán v kole 18 */\n' + out[m.end():]
    return out
