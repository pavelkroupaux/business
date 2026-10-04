# Round 14 (5. 10. 2026): "Kontakt" vpravo v hlavičce, výběr služby ve formuláři (předvyplněný ze stránky služby),
# malé šedé infografiky i v kartách výběru nahoře na stránce Služby.

SVC_SLUG = {'v-svc-dp': 'decision-prototype', 'v-svc-audit': 'audit', 'v-svc-fractional': 'fractional'}
SELECT = ('<label class="ct-f"><span>Služba</span><select name="service" id="ct-service">'
          '<option value="">Zatím nevím</option>'
          '<option value="decision-prototype">Decision Prototype</option>'
          '<option value="audit">Audit rozhodnutí</option>'
          '<option value="fractional">Vedení produktu na část úvazku</option></select></label>')

CSS_R14 = '''
/* ---------- v5 kolo 14 ---------- */
.ct-f select{font:inherit;font-size:16px;color:var(--ink);background:var(--ground);border:1px solid var(--line);border-radius:12px;padding:12px 40px 12px 14px;outline:none;
  -webkit-appearance:none;appearance:none;background-image:linear-gradient(45deg,transparent 50%,currentColor 50%),linear-gradient(135deg,currentColor 50%,transparent 50%);
  background-position:calc(100% - 20px) 52%,calc(100% - 15px) 52%;background-size:5px 5px;background-repeat:no-repeat}
.ct-f select:focus{border-color:var(--ink);box-shadow:0 0 0 3px rgba(255,206,27,.45)}
/* karty výběru na stránce Služby s malou šedou infografikou */
a.pick{position:relative}
a.pick .svc-thumb{margin:0 0 10px}
@media(max-width:700px){a.pick .svc-thumb{position:absolute;top:20px;right:20px;width:92px;max-width:92px;margin:0}a.pick .pick-t,a.pick .pick-p{padding-right:104px}}
/* výsledek v případu: vždy černý, čitelný i v tmavém režimu */
.fl-end{background:#111!important}
.fl-end span{color:#fff!important}
.fl-end small{color:#FFCE1B!important}
:root[data-theme="dark"] .fl-end{box-shadow:0 0 0 1px rgba(255,206,27,.55)!important}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .fl-end{box-shadow:0 0 0 1px rgba(255,206,27,.55)!important}}
/* hlavička: Kontakt i na mobilu */
@media(max-width:480px){.top-in{gap:10px}.top a.lnk{font-size:12.5px}.top .mark{font-size:14px}.top .ctl{margin-left:0}}
@media(max-width:380px){.top-in{gap:8px}.top a.lnk{font-size:12px}.top .mark{font-size:13px}.top .mark i{display:none}}
'''

SVC_JS = '''<script>
(function(){var sel=document.getElementById("ct-service");if(!sel)return;
  function pick(){var m=(location.hash||"").match(/^#\\/contact\\/([a-z-]+)$/);if(m){sel.value=m[1];}}
  window.addEventListener("hashchange",pick);pick();})();
</script>'''

def post_patch14(out):
    # hlavička
    out = rep(out, '<a class="lnk mailonly" href="#/contact" data-nav="/contact">info@pavelkroupa.com</a>', '<a class="lnk" href="#/contact" data-nav="/contact">Kontakt</a>')
    out = rep(out, '(nav==="/portfolio"&&(h.indexOf("/work/")===0||h==="/reference"))', '(nav==="/portfolio"&&(h.indexOf("/work/")===0||h==="/reference"))||(nav==="/contact"&&h.indexOf("/contact")===0)')
    # trasy kontaktu se službou
    out = rep(out, '"/contact":"v-contact"', '"/contact":"v-contact","/contact/decision-prototype":"v-contact","/contact/audit":"v-contact","/contact/fractional":"v-contact"')
    for vid, slug in SVC_SLUG.items():
        a, b = _view(out, vid)
        out = out[:a] + out[a:b].replace('href="#/contact"', f'href="#/contact/{slug}"') + out[b:]
    # výběr služby ve formuláři
    out = rep(out, '<label class="ct-f"><span>Firma <i>nepovinné</i></span>', SELECT + '\n          <label class="ct-f"><span>Firma <i>nepovinné</i></span>')
    # malé šedé infografiky v kartách výběru
    for href, ill in (('#svc-dp', ILL_DP2), ('#svc-audit', ILL_AU2), ('#svc-fractional', ILL_FR2)):
        thumb = '<div class="svc-thumb">' + ill.replace('<svg class="ill ', '<svg class="ill on static ', 1) + '</div>'
        out = rep(out, f'<a class="pick" href="{href}" data-jump><b class="pick-t">', f'<a class="pick" href="{href}" data-jump>{thumb}<b class="pick-t">')
    k = out.rindex('</style>', 0, out.index('<header'))
    return out[:k] + CSS_R14 + out[k:] + SVC_JS
