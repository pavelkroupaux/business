#!/usr/bin/env python3
"""Kontrola anglických textů webu podle pravidel v _brand/.

  python3 _tools/copy-lint.py                 # zakázané vzorce ve všech en/ stránkách
  python3 _tools/copy-lint.py --against HEAD  # navíc texty, které jsou delší než v HEAD

Citace doporučení (.rcard, .ref, blockquote) a texty v ukázkách obrazovek klientů
(třídy lf-…, nebo cokoli s atributem data-nolint) se nekontrolují.
Konec s kódem 1, když něco najde.
"""
import glob, html, re, subprocess, sys
from html.parser import HTMLParser

SKIP_CLASSES = {"rcard", "ref", "ref-claim", "ref-full", "q"}
SKIP_PREFIXES = ("lf-",)  # obrazovky aplikace Leeaf v případové studii
SKIP_TAGS = {"script", "style", "svg", "blockquote"}
BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "li", "figcaption", "dt", "dd", "td", "th",
              "summary", "a", "button", "title", "div", "section", "span"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr"}

WORDS = (r"seamless(ly)?|leverag\w*|unlock\w*|empower\w*|transformative|robust|elevat\w*|"
         r"game[- ]chang\w*|cutting[- ]edge|delv\w*|landscape|realm|tapestry|embark\w*|"
         r"navigat(e|es|ed|ing)|foster\w*|pivotal|crucial|holistic|synerg\w*|supercharg\w*|fast-paced")
CHECKS = [
    ("slovo typické pro AI", re.compile(r"\b(" + WORDS + r")\b", re.I)),
    ("journey (jen „customer journey“)", re.compile(r"(?<!customer )\bjourneys?\b", re.I)),
    ("dlouhá pomlčka", re.compile(r"—| – ")),
    ("věta začíná „Otherwise,“", re.compile(r"(^|[.!?]\s+)Otherwise,")),
    ("„X first, Y second“", re.compile(r"\bfirst, [\w ]+ second\b", re.I)),
    ("„not just … but“", re.compile(r"\bnot just\b.*\bbut\b", re.I)),
    ("sloganový konec „No X and no Y“", re.compile(r"\bNo [\w -]+ and no [\w -]+\.")),
    ("kalk: close a decision", re.compile(r"\bclos(e|ed|ing) (the |a )?(decision|direction)", re.I)),
    ("kalk: under the lid", re.compile(r"under the lid", re.I)),
    ("kalk: in the frame of", re.compile(r"in the frame of", re.I)),
    ("kalk: eventually / actual", re.compile(r"\b(eventually|actual)\b", re.I)),
]


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip, self.buf, self.out = [], 0, [], []

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if t:
            self.out.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "description":
            self.out.append(a.get("content", ""))
        if tag in VOID:
            if tag == "br":
                self.buf.append(" ")
            return
        cls = (a.get("class") or "").split()
        skip = (tag in SKIP_TAGS or "data-nolint" in a or bool(SKIP_CLASSES & set(cls))
                or any(c.startswith(SKIP_PREFIXES) for c in cls))
        self.stack.append(skip)
        if skip:
            self.skip += 1
        if tag in BLOCK_TAGS and tag != "span":
            self.flush()

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        if self.stack.pop():
            self.skip -= 1
        if tag in BLOCK_TAGS and tag != "span":
            self.flush()

    def handle_data(self, d):
        if not self.skip:
            self.buf.append(d)


def blocks(src):
    p = Blocks()
    p.feed(src)
    p.flush()
    return p.out


def visible(line):
    line = re.sub(r"(?s)<(script|style|svg)[^>]*>.*?</\1>", "", line)
    return html.unescape(re.sub(r"<[^>]+>", "", line)).strip()


def length_check(ref):
    diff = subprocess.run(["git", "diff", "-U0", ref, "--", "en/"],
                          capture_output=True, text=True).stdout
    found, fname, minus, plus = [], None, [], []

    def pair():
        if len(minus) != len(plus):
            return
        for o, n in zip(minus, plus):
            if "image:alt" in o:
                continue
            a, b = visible(o), visible(n)
            if a and b and len(b) > len(a):
                found.append(f"{fname}: delší text ({len(a)} → {len(b)} znaků): {b[:90]}")

    for l in diff.splitlines() + ["@@"]:
        if l.startswith("+++ "):
            fname = l[6:]
        elif l.startswith("@@"):
            pair()
            minus, plus = [], []
        elif l.startswith("-") and not l.startswith("---"):
            minus.append(l[1:])
        elif l.startswith("+"):
            plus.append(l[1:])
    return found


def main():
    found = []
    for f in sorted(glob.glob("en/**/*.html", recursive=True)):
        for t in blocks(open(f, encoding="utf-8").read()):
            for name, rx in CHECKS:
                if rx.search(t):
                    found.append(f"{f}: {name}: {t[:110]}")
    if "--against" in sys.argv:
        found += length_check(sys.argv[sys.argv.index("--against") + 1])
    for x in found:
        print(x)
    print(f"{len(found)} nálezů" if found else "OK, nic nenalezeno")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
