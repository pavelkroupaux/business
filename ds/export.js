/* Export design systému: PDF (tisk), JSON (tokeny a texty), Markdown a samostatné HTML. Vše se skládá ze stránky /ds v prohlížeči, takže export odpovídá tomu, co je vidět. */
(function () {
  var box = document.querySelector("[data-export]");
  if (!box) return;
  var btn = box.querySelector("[data-export-open]"), menu = box.querySelector("[data-export-menu]");
  var ORIGIN = location.origin, day = new Date().toISOString().slice(0, 10), base = "pavelkroupa-design-system-" + day;

  function toggle(open) {
    menu.hidden = !open;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { toggle(menu.hidden); });
  document.addEventListener("click", function (e) { if (!box.contains(e.target)) toggle(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { toggle(false); btn.focus(); } });

  function clean(s) { return (s || "").replace(/\s+/g, " ").trim(); }
  function abs(u) { try { return new URL(u, location.href).href; } catch (e) { return u; } }
  function save(name, type, data) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([data], { type: type }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  /* tokeny z řádků s data-t; hodnoty jsou už načtené z CSS (světlý a tmavý režim) */
  function tokens() {
    var out = [];
    [].forEach.call(document.querySelectorAll(".ds-tg"), function (g) {
      var h = g.querySelector("h3"), items = [];
      [].forEach.call(g.querySelectorAll("li[data-t]"), function (li) {
        var l = li.querySelector(".ds-val.l"), d = li.querySelector(".ds-val.d"), n = li.querySelector(".ds-name span");
        var light = l ? l.getAttribute("data-copy") || "" : "";
        items.push({ name: li.getAttribute("data-t"), description: n ? clean(n.textContent) : "", light: light, dark: d ? d.getAttribute("data-copy") || "" : light });
      });
      if (items.length) out.push({ group: h ? clean(h.firstChild ? h.firstChild.textContent : h.textContent) : "", items: items });
    });
    return out;
  }
  function typography() {
    return [].map.call(document.querySelectorAll("[data-spec]"), function (b) {
      var k = b.querySelector(".ds-k"), m = b.querySelector(".ds-m"), s = b.querySelector("[data-spec-el]");
      return { label: k ? clean(k.textContent) : "", sample: s ? clean(s.textContent) : "", spec: m ? clean(m.textContent) : "" };
    });
  }
  function dimensions() {
    return [].map.call(document.querySelectorAll("[data-dim]"), function (td) {
      var tr = td.parentNode.firstElementChild;
      return { name: clean(tr.textContent), value: clean(td.textContent) };
    });
  }
  function files() {
    return [].map.call(document.querySelectorAll(".ds-files"), function (ul) {
      var k = ul.parentNode.querySelector(".ds-k");
      return {
        group: k ? clean(k.textContent) : "",
        files: [].map.call(ul.querySelectorAll("a"), function (a) { return { name: clean(a.textContent), url: abs(a.getAttribute("href")) }; })
      };
    });
  }

  /* text stránky jako seznam bloků; stejný průchod pro JSON i Markdown */
  var SKIP = "script,style,svg,button,nav,[hidden],.ds-stage,.ds-board,.ds-src,.ds-toc,.ds-side,.ds-export,.ds-probe,.ds-replay,.ds-seg,.ds-sw,.ds-files,.eyebrow,.pk-gate,.pk-load";
  function inline(el) {
    var s = "";
    [].forEach.call(el.childNodes, function (n) {
      if (n.nodeType === 3) { s += n.nodeValue; return; }
      if (n.nodeType !== 1 || n.matches("svg,script,style,[hidden]")) return;
      var t = inline(n);
      if (n.tagName === "A" && n.getAttribute("href")) s += "[" + clean(t) + "](" + abs(n.getAttribute("href")) + ")";
      else if (n.tagName === "CODE") s += "`" + clean(t) + "`";
      else if (n.tagName === "BR") s += " ";
      else s += t;
    });
    return clean(s);
  }
  function blocks(root, out) {
    [].forEach.call(root.children, function (el) {
      if (el.matches(SKIP)) return;
      var t = el.tagName, c = el.classList, x;
      if (/^H[1-4]$/.test(t)) { x = inline(el); if (x) out.push({ type: "h" + t[1], text: x }); }
      else if (t === "P" || c.contains("ds-k")) {
        x = inline(el); if (!x) return;
        if (c.contains("ds-k")) out.push({ type: "label", text: x });
        else if (c.contains("ds-en")) out.push({ type: "p", text: "EN: " + x });
        else if (c.contains("ds-ex")) out.push({ type: "p", text: "„" + x + "“" });
        else out.push({ type: "p", text: x });
      }
      else if (t === "UL" || t === "OL") {
        var items = [].map.call(el.children, inline).filter(Boolean);
        if (items.length) out.push({ type: "list", items: items });
      }
      else if (t === "DL") {
        var rows = [], k = "";
        [].forEach.call(el.children, function (n) { if (n.tagName === "DT") k = inline(n); else if (n.tagName === "DD") rows.push([k, inline(n)]); });
        if (rows.length) out.push({ type: "dl", rows: rows });
      }
      else if (t === "TABLE") {
        var tr = [].map.call(el.querySelectorAll("tr"), function (r) { return [].map.call(r.children, inline); });
        if (tr.length) out.push({ type: "table", rows: tr });
      }
      else if (t === "IMG") out.push({ type: "img", text: el.getAttribute("alt") || "", url: abs(el.getAttribute("src")) });
      else if (t === "FIGURE" || t === "SPAN" && c.contains("ds-tab")) { x = inline(el); if (x) out.push({ type: "p", text: x }); }
      else blocks(el, out);
    });
    return out;
  }
  function sections() {
    return [].map.call(document.querySelectorAll("main.ds section.ds-hero, main.ds section[id]"), function (s) {
      var b = blocks(s, []), h = b.filter(function (x) { return x.type === "h1" || x.type === "h2"; })[0];
      return { id: s.id || "uvod", title: h ? h.text : "", blocks: b };
    });
  }

  function exportJson() {
    var data = {
      name: "Design systém, pavelkroupa.com",
      exported: new Date().toISOString(),
      source: ORIGIN + "/ds/",
      note: "Tokeny mají hodnotu pro světlý a tmavý režim. Texty sekcí jsou v poli sections.",
      tokens: tokens(),
      typography: typography(),
      dimensions: dimensions(),
      files: files(),
      sections: sections().map(function (s) {
        return { id: s.id, title: s.title, text: s.blocks.map(function (b) {
          if (b.items) return b.items; if (b.rows) return b.rows; return b.text;
        }) };
      })
    };
    save(base + ".json", "application/json", JSON.stringify(data, null, 2));
  }

  function row(cells) { return "| " + cells.map(function (c) { return String(c).replace(/\|/g, "\\|"); }).join(" | ") + " |"; }
  function exportMd() {
    var L = ["# Design systém, pavelkroupa.com", "", "Exportováno " + day + " z " + ORIGIN + "/ds/", ""];
    sections().forEach(function (s) {
      L.push("");
      s.blocks.forEach(function (b) {
        switch (b.type) {
          case "h1": L.push("## " + b.text, ""); break;
          case "h2": L.push("## " + b.text, ""); break;
          case "h3": L.push("### " + b.text, ""); break;
          case "h4": L.push("#### " + b.text, ""); break;
          case "label": L.push("**" + b.text + "**", ""); break;
          case "p": L.push(b.text, ""); break;
          case "img": L.push("![" + b.text + "](" + b.url + ")", ""); break;
          case "list": b.items.forEach(function (i) { L.push("- " + i); }); L.push(""); break;
          case "dl": b.rows.forEach(function (r) { L.push("- **" + r[0] + "**: " + r[1]); }); L.push(""); break;
          case "table":
            b.rows.forEach(function (r, i) { L.push(row(r)); if (i === 0) L.push(row(r.map(function () { return "---"; }))); });
            L.push(""); break;
        }
      });
      if (s.id === "barvy") {
        tokens().forEach(function (g) {
          L.push("### " + g.group, "", row(["Token", "Světlý", "Tmavý", "Použití"]), row(["---", "---", "---", "---"]));
          g.items.forEach(function (t) { L.push(row(["`" + t.name + "`", "`" + t.light + "`", "`" + t.dark + "`", t.description])); });
          L.push("");
        });
      }
      if (s.id === "stazeni") {
        files().forEach(function (g) {
          L.push("**" + g.group + "**", "");
          g.files.forEach(function (f) { L.push("- [" + f.name + "](" + f.url + ")"); });
          L.push("");
        });
      }
    });
    save(base + ".md", "text/markdown", L.join("\n").replace(/\n{3,}/g, "\n\n").trim() + "\n");
  }

  /* HTML: kopie stránky bez skriptů a navigace, styl a písmo vložené dovnitř. Obrázky zůstávají odkazy na pavelkroupa.com. */
  function blobToData(b) {
    return new Promise(function (ok) { var r = new FileReader(); r.onload = function () { ok(r.result); }; r.readAsDataURL(b); });
  }
  function exportHtml() {
    var old = btn.textContent;
    btn.textContent = "Připravuji…";
    fetch("/assets/site.css").then(function (r) { return r.text(); }).then(function (css) {
      var urls = css.match(/url\(\/assets\/fonts\/[^)]+\)/g) || [];
      return Promise.all(urls.map(function (u) {
        var p = u.slice(4, -1);
        return fetch(p).then(function (r) { return r.blob(); }).then(blobToData).then(function (d) { css = css.split(u).join("url(" + d + ")"); });
      })).then(function () { return css.replace(/url\(\/(?!\/)/g, "url(" + ORIGIN + "/"); });
    }).then(function (css) {
      var doc = document.documentElement.cloneNode(true);
      [].forEach.call(doc.querySelectorAll("script,link[rel=preload],link[rel=stylesheet],header.top,.ds-side,.ds-export,.ds-probe,.ds-replay,.ds-seg,.pk-gate,.pk-load,noscript"), function (n) { n.remove(); });
      doc.classList.remove("pk-lock");
      [].forEach.call(doc.querySelectorAll("[href^='/'],[src^='/']"), function (n) {
        ["href", "src"].forEach(function (a) { var v = n.getAttribute(a); if (v && v[0] === "/" && v[1] !== "/") n.setAttribute(a, ORIGIN + v); });
      });
      [].forEach.call(doc.querySelectorAll("a[href^='#']"), function (a) { a.removeAttribute("download"); });
      var st = document.createElement("style");
      st.textContent = css + "[data-rv],.note{opacity:1!important;transform:none!important}*,*::before,*::after{animation:none!important}.ds{padding-left:0!important}";
      doc.querySelector("head").appendChild(st);
      var h = doc.querySelector("meta[name=robots]"); if (h) h.remove();
      save(base + ".html", "text/html", "<!doctype html>\n" + doc.outerHTML);
    }).catch(function () { alert("Export HTML se nepovedl."); }).then(function () { btn.textContent = old; });
  }

  /* PDF: tisk ve světlém režimu, rozložení řeší @media print ve stránce */
  function exportPdf() {
    var r = document.documentElement, prev = r.getAttribute("data-theme");
    function back() { if (prev === null) r.removeAttribute("data-theme"); else r.setAttribute("data-theme", prev); window.removeEventListener("afterprint", back); }
    r.setAttribute("data-theme", "light");
    window.addEventListener("afterprint", back);
    setTimeout(function () { window.print(); }, 150);
  }

  menu.addEventListener("click", function (e) {
    var b = e.target.closest("[data-export-as]");
    if (!b) return;
    toggle(false);
    ({ pdf: exportPdf, json: exportJson, md: exportMd, html: exportHtml })[b.getAttribute("data-export-as")]();
  });
})();
