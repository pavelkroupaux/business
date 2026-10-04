# Round 18 (5. 10. 2026, Claude Code): opravy, které vznikly v repozitáři, aby je další build nepřepsal.
# - Leeaf 2020–2023 (bylo 2021–2023)
# - Heirloom: zástupná citace pryč, doplní se později
# - O mně: galerie bez zástupných rámečků „[FOTKA: …]“, místo nich mapa prototypu (src/img/mapa-prototypu.jpg)
# - popisky fotek v galerii česky, odkaz na logo BRENO bez názvu souboru
# - hlavička: na mobilu jen logo pk (se jménem přetékala do strany), jméno zůstává pro čtečky obrazovky
# - kontaktní formulář se vejde i na 320 px
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
