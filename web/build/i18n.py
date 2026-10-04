"""Překlad vyrobených stránek do dalšího jazyka.

Stránka se rozloží na strom prvků tak, aby se dal složit zpátky znak po znaku. Překládá se po
„jednotkách“: nejvyšší prvek, který obsahuje jen text a řádkové značky (b, span, a, br …).
Klíčem je jeho vnitřní HTML se sjednocenými mezerami, takže věta s <span class="fix"> nebo
odkazem se překládá celá a v angličtině může mít jiný slovosled. Zvlášť se překládají
atributy (alt, aria-label, title, placeholder, data-words) a samostatné texty v SVG.

Co zůstane nepřeložené a není v seznamu výjimek, translate() vrátí v seznamu chyb.
"""
import re

TAG_RE = re.compile(r"""<!--.*?-->|<(?:"[^"]*"|'[^']*'|[^'">])*>""", re.S)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
INLINE = {"a", "abbr", "b", "br", "cite", "code", "em", "i", "mark", "q", "s", "small", "span", "strong", "sub", "sup",
          "time", "u", "tspan"}
RAW = {"script", "style"}
ATTRS = ("alt", "aria-label", "title", "placeholder", "data-words")
LETTER = re.compile(r"[A-Za-zÀ-ž]")


class Node:
    __slots__ = ("tag", "start", "children", "end", "text")

    def __init__(self, tag=None, start="", end="", text=None):
        self.tag, self.start, self.end, self.text = tag, start, end, text
        self.children = []


def parse(markup):
    root = Node(tag="#root")
    stack = [root]
    pos = 0
    for m in TAG_RE.finditer(markup):
        if m.start() > pos:
            stack[-1].children.append(Node(text=markup[pos:m.start()]))
        tok = m.group(0)
        pos = m.end()
        if tok.startswith("<!--"):
            stack[-1].children.append(Node(text=tok, tag="#comment"))
            continue
        if tok.startswith("</"):
            name = tok[2:-1].strip().lower()
            # zavírací značka musí sedět s otevřenou, jinak by se strom rozjel
            assert stack[-1].tag == name, f"neuzavřená značka <{stack[-1].tag}> před </{name}>"
            stack[-1].end = tok
            stack.pop()
            continue
        name = re.match(r"<\s*([a-zA-Z0-9:-]+)", tok).group(1).lower()
        node = Node(tag=name, start=tok)
        stack[-1].children.append(node)
        if tok.endswith("/>") or name in VOID or tok.startswith("<!"):
            continue
        stack.append(node)
        if name in RAW:   # obsah skriptu a stylu se nerozkládá
            close = markup.lower().index(f"</{name}", pos)
            node.children.append(Node(text=markup[pos:close]))
            pos = close
    if pos < len(markup):
        stack[-1].children.append(Node(text=markup[pos:]))
    assert len(stack) == 1, f"neuzavřené značky: {[n.tag for n in stack[1:]]}"
    return root


def render(node):
    if node.text is not None:
        return node.text
    inner = "".join(render(c) for c in node.children)
    return inner if node.tag == "#root" else node.start + inner + node.end


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def is_unit(node):
    """Prvek jen s textem a řádkovými značkami, který obsahuje nějaké písmeno."""
    if node.text is not None or node.tag in RAW or node.tag in VOID or node.tag in ("#root", "svg"):
        return False

    def inline_only(n):
        for c in n.children:
            if c.text is not None:
                continue
            if c.tag not in INLINE or not inline_only(c):
                return False
        return True
    return inline_only(node) and bool(LETTER.search(text_of(node)))


def text_of(node):
    if node.text is not None:
        return "" if node.tag == "#comment" else node.text
    return "".join(text_of(c) for c in node.children)


def _attr_swap(start, table, missing, same):
    def one(m):
        name, val = m.group(1), m.group(2)
        if name not in ATTRS or not LETTER.search(val):
            return m.group(0)
        key = norm(val)
        if key in table:
            return f'{name}="{table[key]}"'
        if key not in same:
            missing.append(f'{name}="{val}"')
        return m.group(0)
    return re.sub(r'\b([a-z-]+)="([^"]*)"', one, start)


def translate(markup, units, attrs, same):
    """Vrátí (přeložené HTML, seznam nepřeložených textů)."""
    root = parse(markup)
    assert render(root) == markup, "rozklad stránky nesedí se zdrojem"
    missing = []
    used = set()

    def walk(node, quiet=False):
        if node.text is not None:
            if node.tag == "#comment" or quiet or not LETTER.search(node.text):
                return node.text
            key = norm(node.text)
            if key in units:
                used.add(key)
                lead = node.text[:len(node.text) - len(node.text.lstrip())]
                trail = node.text[len(node.text.rstrip()):]
                return lead + units[key] + trail
            if key not in same:
                missing.append(key)
            return node.text
        start = _attr_swap(node.start, attrs, missing, same) if node.start else ""
        if node.tag == "#root":
            return "".join(walk(c) for c in node.children)
        if node.tag in RAW:
            return start + "".join(c.text for c in node.children) + node.end
        if not quiet and is_unit(node):
            key = norm("".join(render(c) for c in node.children))
            if key in units:
                used.add(key)
                return start + units[key] + node.end
            if not (norm(text_of(node)) in same or key in same):
                missing.append(key)
            # stejné v obou jazycích nebo chybí překlad: text nechat, atributy uvnitř ale přeložit
            return start + "".join(walk(c, True) for c in node.children) + node.end
        return start + "".join(walk(c, quiet) for c in node.children) + node.end

    out = walk(root)
    return out, missing, used


def units_of(markup, same=()):
    """Seznam překladových jednotek ve stránce (pro soupis textů)."""
    found = []

    def walk(node):
        if node.text is not None:
            if node.tag != "#comment" and LETTER.search(node.text):
                found.append(("text", norm(node.text)))
            return
        if node.start:
            for name, val in re.findall(r'\b([a-z-]+)="([^"]*)"', node.start):
                if name in ATTRS and LETTER.search(val):
                    found.append(("attr:" + name, norm(val)))
        if node.tag in RAW:
            return
        if is_unit(node):
            found.append(("html", norm("".join(render(c) for c in node.children))))
            return
        for c in node.children:
            walk(c)
    walk(parse(markup))
    return [(k, v) for k, v in found if v not in same]
