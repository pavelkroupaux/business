# Round 13 (5. 10. 2026): hlavička služeb vlevo text, vpravo infografika; štítky "Cenu ovlivní" i v tmavém režimu;
# "Proč začít tady" jako karta s tlačítkem; nová stránka Kontakt s formulářem a firemními údaji.

CONTACT2 = '''<div id="v-contact" hidden>
  <section class="canvas dots contact2">
    <div class="wrap">
      <p class="eyebrow sig">Kontakt</p>
      <h1>Kde jste se <span class="fix">zasekli</span>?</h1>
      <p class="lede">Napište mi pár vět. Ozvu se a domluvíme třicetiminutový hovor. V Praze, v Amsterdamu nebo online.</p>
      <div class="ct-grid">
        <form class="ct-form" id="ct-form" novalidate>
          <div class="ct-row2">
            <label class="ct-f"><span>Jméno</span><input name="name" type="text" autocomplete="name" required></label>
            <label class="ct-f"><span>E-mail</span><input name="email" type="email" autocomplete="email" required></label>
          </div>
          <label class="ct-f"><span>Firma <i>nepovinné</i></span><input name="company" type="text" autocomplete="organization"></label>
          <label class="ct-f"><span>Kde jste se zasekli?</span><textarea name="msg" rows="5" required placeholder="Pár vět stačí. Co se nedaří rozhodnout a kdo o tom rozhoduje."></textarea></label>
          <div class="ct-actions"><button type="submit" class="btn btn-fill">Odeslat</button><span class="ct-err" role="alert"></span></div>
          <div class="ct-done" hidden><b>Díky, mám to.</b> Ozvu se na e-mail, který jste vyplnili.<small>Prototyp: formulář zatím nikam neodesílá.</small></div>
        </form>
        <aside class="ct-side">
          <div class="ct-card">
            <p class="op-h">Raději napřímo?</p>
            <div class="copyrow"><span id="mail" class="mail">info@pavelkroupa.com</span><button type="button" id="copy-mail" class="btn btn-line">Zkopírovat</button></div>
            <a class="btn btn-fill ct-cal" href="https://cal.com/pavelkroupa">Vybrat termín hovoru</a>
            <a class="lnk" href="https://www.linkedin.com/in/pavelkroupa/">LinkedIn</a>
          </div>
          <div class="ct-card ct-co">
            <p class="op-h">Firemní údaje</p>
            <dl>
              <dt>Firma</dt><dd>Pavel Kroupa</dd>
              <dt>Sídlo</dt><dd>Mezno 88, 257 86 Mezno</dd>
              <dt>IČO</dt><dd>87977753</dd>
              <dt>DPH</dt><dd>Neplátce DPH</dd>
              <dt>Země</dt><dd>Česká republika</dd>
            </dl>
          </div>
        </aside>
      </div>
    </div>
  </section>
</div>
'''

CSS_R13 = '''
/* ---------- v5 kolo 13 ---------- */
/* hlavička služby: vlevo text, vpravo infografika */
.dhero{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.8fr);gap:56px;align-items:center;text-align:left;margin-top:8px}
.dhero h1,.dhero .lede,.dhero .eyebrow,.dhero .row{margin-left:0;margin-right:0;text-align:left}
.dhero .row{justify-content:flex-start}
.dhero .svc-hero-ill{max-width:380px;width:100%;margin:0 0 0 auto}
.dhero-sec .crumb{text-align:left;margin-left:0;margin-right:0;justify-content:flex-start;max-width:none}
@media(max-width:860px){.dhero{grid-template-columns:1fr;gap:28px}.dhero .svc-hero-ill{max-width:260px;margin:0}}
/* štítky "Cenu ovlivní" čitelné i v tmavém režimu */
.op-dots li{background:transparent;border:1px solid var(--line);color:var(--ink)}
:root[data-theme="dark"] .op-dots li{border-color:rgba(255,255,255,.18)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .op-dots li{border-color:rgba(255,255,255,.18)}}
/* Proč začít tady */
.why-sec{padding-block:clamp(56px,7vw,96px)}
.callout{max-width:820px;margin:0 auto;background:var(--raise);border-radius:28px;box-shadow:var(--glass-shadow);padding:clamp(28px,4vw,48px);text-align:center}
.callout h2{margin-bottom:14px}
.callout .lede{margin-bottom:0}
/* kontakt */
.contact2{text-align:center}
.ct-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.9fr);gap:22px;margin-top:44px;text-align:left;align-items:start}
.ct-form,.ct-card{background:var(--raise);border-radius:24px;box-shadow:var(--glass-shadow);padding:28px}
.ct-form{display:grid;gap:16px}
.ct-row2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.ct-f{display:grid;gap:7px}
.ct-f span{font-family:var(--display);font-size:13.5px;font-weight:600;color:var(--muted)}
.ct-f i{font-style:normal;font-weight:400;color:var(--faint)}
.ct-f input,.ct-f textarea{font:inherit;font-size:16px;color:var(--ink);background:var(--ground);border:1px solid var(--line);border-radius:12px;padding:12px 14px;outline:none;resize:vertical}
.ct-f input:focus,.ct-f textarea:focus{border-color:var(--ink);box-shadow:0 0 0 3px rgba(255,206,27,.45)}
.ct-f .bad{border-color:#d93025}
.ct-actions{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.ct-err{font-size:14px;color:#d93025}
.ct-done{background:var(--surface);border-radius:14px;padding:16px 18px;font-size:15.5px;color:var(--ink)}
.ct-done small{display:block;margin-top:6px;font-size:12.5px;color:var(--faint)}
.ct-side{display:grid;gap:22px}
.ct-card .copyrow{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:2px 0 16px}
.ct-card .mail{font-family:var(--display);font-size:19px;font-weight:600;color:var(--ink);user-select:all}
.ct-cal{margin-bottom:14px}
.ct-card .lnk{display:inline-block}
.ct-co dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0;font-size:15px}
.ct-co dt{color:var(--faint);font-family:var(--display);font-size:13.5px}
.ct-co dd{margin:0;color:var(--ink)}
@media(max-width:860px){.ct-grid{grid-template-columns:1fr}.ct-row2{grid-template-columns:1fr}}
'''

CT_JS = '''<script>
(function(){var f=document.getElementById("ct-form");if(!f)return;
  f.addEventListener("submit",function(e){e.preventDefault();var bad=[];
    [].forEach.call(f.querySelectorAll("[required]"),function(el){var ok=el.value.trim()&&(el.type!=="email"||/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(el.value.trim()));
      el.classList.toggle("bad",!ok);if(!ok)bad.push(el);});
    var err=f.querySelector(".ct-err");
    if(bad.length){err.textContent="Vyplňte prosím jméno, e-mail a pár vět.";bad[0].focus();return;}
    err.textContent="";f.querySelector(".ct-done").hidden=false;f.querySelector(".ct-actions").hidden=true;});
})();
</script>'''

def post_patch13(out):
    # hlavička tří služeb
    for vid in ('v-svc-dp', 'v-svc-fractional', 'v-svc-audit'):
        a, b = _view(out, vid); v = out[a:b]
        m = re.search(r'<section class="canvas">\s*<div class="wrap">\s*(<p class="crumb">.*?</p>)\s*(<div class="svc-hero-ill">.*?</svg></div>)\s*(<p class="eyebrow sig">.*?)(\s*</div>\s*</section>)', v, re.S)
        assert m, vid
        new = (f'<section class="canvas dhero-sec">\n    <div class="wrap">\n      {m.group(1)}\n      <div class="dhero"><div class="dhero-t">{m.group(3)}</div>{m.group(2)}</div>{m.group(4)}')
        v = v[:m.start()] + new + v[m.end():]
        out = out[:a] + v + out[b:]
    # Proč začít tady
    out = re.sub(r'<section class="canvas">\s*<div class="wrap">\s*(<p class="eyebrow sig">Proč začít tady</p>.*?)\s*</div>\s*</section>',
                 lambda m: f'<section class="why-sec">\n    <div class="wrap"><div class="callout">{m.group(1)}<div class="row" style="margin-top:26px"><a class="btn btn-fill" href="#/contact">Domluvit 30minutový hovor</a></div></div></div>\n  </section>',
                 out, count=1, flags=re.S)
    assert 'class="callout"' in out
    # kontakt
    i = out.index('<div id="v-contact"'); j = out.index('</main>', i)
    out = out[:i] + CONTACT2 + out[j:]
    out = re.sub(r'<a ((?:(?!target=)[^>])*?)href="(https://cal\.com/[^"]+|https://www\.linkedin\.com/in/pavelkroupa/)"((?:(?!target=)[^>])*)>', r'<a \1href="\2"\3 target="_blank" rel="noopener">', out)
    k = out.rindex('</style>', 0, out.index('<header'))
    return out[:k] + CSS_R13 + out[k:] + CT_JS
