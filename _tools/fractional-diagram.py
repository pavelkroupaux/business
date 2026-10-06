"""Diagram služby Vedení produktu na část úvazku (.ill-fr) na všech stránkách. Spouštět z kořene repozitáře: python3 _tools/fractional-diagram.py"""
import re,sys
def day(x,lbl,on=None):
    d=f"M{x+9} 14 H{x+31} Q{x+40} 14 {x+40} 23 V45 Q{x+40} 54 {x+31} 54 H{x+9} Q{x} 54 {x} 45 V23 Q{x} 14 {x+9} 14 Z"
    s=f'<path d="{d}" class="ill-off"/>'
    if on: s+=f'<path class="dfill" style="--i:{on}" d="{d}" fill="#FFCE1B"/><text x="{x+20}" y="39" text-anchor="middle" class="ill-d don" style="--i:{on}">{lbl}</text>'
    else: s+=f'<text x="{x+20}" y="39" text-anchor="middle" class="ill-d">{lbl}</text>'
    return s
def svg(cls,aria,days,labs):
    xs=[40,92,144,196,248]; ons={1:"0.55s",3:"1.65s"}
    top=''.join(day(x,days[i],ons.get(i)) for i,x in enumerate(xs))
    box="M247 131 H269 Q275 131 275 137 V159 Q275 165 269 165 H247 Q241 165 241 159 V137 Q241 131 247 131 Z"
    return f'''<svg class="{cls}" viewBox="0 0 320 200" fill="none" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{aria}">
  {top}
  <circle class="wk" cx="60" cy="64" r="3.5" fill="#FFCE1B"/>
  <g class="ia" style="--i:2.3s"><circle cx="70" cy="148" r="17" class="ill-node" stroke="currentColor" stroke-width="2"/><text class="ill-q" x="70" y="154" text-anchor="middle">?</text></g>
  <g stroke="currentColor" stroke-width="2"><path class="ln" style="--i:2.75s" pathLength="1" d="M93 148 H133"/><path class="ia" style="--i:3.1s" d="M128 143 L134 148 L128 153"/></g>
  <g class="ia" style="--i:3.2s"><circle cx="164" cy="148" r="24" fill="#fff" stroke="currentColor" stroke-width="2"/></g>
  <circle class="pop" style="--i:4.6s" cx="164" cy="148" r="25" fill="#FFCE1B"/>
  <g class="ia" style="--i:3.2s"><circle cx="164" cy="148" r="16" stroke="#1d1d1f" stroke-width="1.6"/>
    <g class="cmp-n"><path d="M164 135 L168.5 148 H159.5 Z" fill="#1d1d1f"/><path d="M164 161 L168.5 148 H159.5 Z" fill="#fff" stroke="#1d1d1f" stroke-width="1.2"/></g></g>
  <g stroke="currentColor" stroke-width="2"><path class="ln" style="--i:4.95s" pathLength="1" d="M195 148 H235"/><path class="ia" style="--i:5.3s" d="M230 143 L236 148 L230 153"/></g>
  <g class="ia" style="--i:5.4s"><path d="{box}" fill="#fff" stroke="currentColor" stroke-width="2"/></g>
  <path class="pop" style="--i:5.75s" d="{box}" fill="#FFCE1B" stroke="#FFCE1B" stroke-width="2"/>
  <path class="ln" style="--i:5.9s" pathLength="1" d="M249 148 L255 154 L267 141" stroke="#1d1d1f" stroke-width="2.6"/>
  <text class="ia ill-t" style="--i:2.35s" x="70" y="190" text-anchor="middle">{labs[0]}</text><text class="ia ill-t" style="--i:3.25s" x="164" y="190" text-anchor="middle">{labs[1]}</text><text class="ia ill-t" style="--i:5.45s" x="258" y="190" text-anchor="middle">{labs[2]}</text>
</svg>'''
L={'cs':(["Po","Út","St","Čt","Pá"],["vedení","směr","vývoj"]),'en':(["Mo","Tu","We","Th","Fr"],["leadership","direction","engineering"])}
import glob
for f in glob.glob('**/*.html',recursive=True):
    s=open(f).read()
    lang='en' if f.startswith('en/') else 'cs'
    def rep(m):
        cls=m.group(1); aria=m.group(2)
        return svg(cls,aria,*L[lang])
    s2=re.sub(r'<svg class="(ill[^"]*ill-fr)" viewBox="0 0 320 200"[^>]*aria-label="([^"]*)">.*?</svg>',rep,s,flags=re.S)
    if s2!=s: open(f,'w').write(s2); print(f)
