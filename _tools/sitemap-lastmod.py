"""Datum poslední změny (<lastmod>) v sitemap.xml podle gitu.
Spouštět z kořene repozitáře po změně stránek: python3 _tools/sitemap-lastmod.py
Stránka s neuloženou změnou dostane dnešní datum, ostatní datum posledního commitu, který ji měnil."""
import re, subprocess, datetime, os

SITE = 'https://pavelkroupa.com'
today = datetime.date.today().isoformat()

def file_for(loc):
    p = loc[len(SITE):].lstrip('/')
    return os.path.join(p, 'index.html') if (p == '' or p.endswith('/')) else p

def lastmod(path):
    dirty = subprocess.run(['git', 'status', '--porcelain', '--', path], capture_output=True, text=True).stdout.strip()
    if dirty:
        return today
    d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path], capture_output=True, text=True).stdout.strip()
    return d or today

s = open('sitemap.xml', encoding='utf8').read()
changed = 0
def fix(m):
    global changed
    loc, old = m.group(2), m.group(4)
    path = file_for(loc)
    if not os.path.exists(path):
        print('chybí soubor pro', loc); return m.group(0)
    new = lastmod(path)
    if new != old:
        changed += 1
    return m.group(1) + new + m.group(5)
s2 = re.sub(r'(<loc>([^<]+)</loc>(\s*)<lastmod>)([^<]*)(</lastmod>)', fix, s)
open('sitemap.xml', 'w', encoding='utf8').write(s2)
print(f'sitemap.xml: změněno {changed} dat')
