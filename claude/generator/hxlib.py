# Hilfen nur für Variante H 06–10 (flib-Formlisten): Visier-Markierung, Labels, 2D-Board mit separatem Visier
import flib
from flib import svg2d,bbox
def S(s):
    s['sight']=True;return s
def apply(m,spec):
    assert len(m.parts)==len(spec),(len(m.parts),len(spec))
    for P,s in zip(m.parts,spec):
        if s.get('label'):P['label']=s['label']
        if s.get('sight'):P['sight']=True
    return m
def _fit(spec,cx0,cy0,w,h,smax=1.25):
    x0,y0,x1,y1=bbox(spec);sc=min(w/(x1-x0),h/(y1-y0),smax)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    return f'translate({cx0-cx*sc:.1f},{cy0-cy*sc:.1f}) scale({sc:.3f})'
def board2d(spec,num,name,vname,col,pill,aria,desc,palette,form,fid):
    gun=[s for s in spec if not s.get('sight')];sig=[s for s in spec if s.get('sight')]
    b=flib.board2d(gun,num,name,vname,col,pill,aria,desc,palette,form,fid)
    b=b.replace('Variante F</title>','Variante H</title>').replace('VARIANTE F · „','VARIANTE H · „')
    old=f'<g transform="{flib.fit(gun)}">'
    assert old in b
    x0,y0,x1,y1=bbox(gun);tall=(y1-y0)>0.8*(x1-x0)
    b=b.replace(old,f'<g transform="{_fit(gun,360,300,600,450) if tall else _fit(gun,380,330,660,360)}">')
    if sig:
        inset=(f'<g><rect x="540" y="18" width="204" height="132" rx="10" fill="#0E1622" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 5"/>'
               f'<text x="552" y="40" font-family="Chakra Petch, sans-serif" font-size="13" font-weight="600" letter-spacing="2" fill="{col}">VISIER · SEPARAT</text>'
               f'<g transform="{_fit(sig,642,96,170,74,1.6)}">{svg2d(sig,fid)}</g></g>')
        b=b.replace('</g>\n</svg>','</g>\n'+inset+'\n</svg>',1)
    return b
