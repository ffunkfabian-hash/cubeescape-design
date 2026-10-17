"""Skins der Konzeptblätter (claude-0.3): Gestaltungsebene über Material und Kanalfarbe.

Katalog CATALOG (9 Skins), je Waffe fünf (pick(); der erste ist der Hauptskin des Blatts). Bausteine (Wunsch des Nutzers,
17.10.2026): Farbflächen über Bauteilgrenzen, Glyphen/Zahlen/Embleme als Aufkleber-Gruppen, Streifen/Verläufe/Ringe,
poliertes Gold/Chrom gegen dunkles Metall mit Kantenabnutzung, Schmuckteile (Rippen/Finnen).
Farben: die sieben MT_-Kanäle (umfärbbar wie die Farbvarianten) plus zwei feste Skin-Akzente SK_Accent1/SK_Accent2.

resolve() löst einen Katalog-Skin für ein Modell in Modellkoordinaten auf (ohne numpy: export_spec.py nutzt dieselben Daten),
apply() setzt Glyphen-Aufkleber und Schmuckteile in eine Modellkopie, xl.skin_texture() malt die Musterflächen im Objektraum.
Muster liegen im Objektraum (Seitenprojektion bzw. Richtung im Modell), nicht in UV – so kann Toolgen sie mit
Objekt-Koordinaten in Blender backen.
"""
import math,copy
from eng import CHANNELS,Model,rect,circ
from xlroles import color_roles,material_of,part_area,METAL_LABELS,DARK_LABELS,GRIP_LABELS,_mix

ACCENTS=('SK_Accent1','SK_Accent2')
SLOTS=CHANNELS+ACCENTS
FINISHES=('paint','polished_gold','polished_chrome','neon')
BLOCKS={'farbflaechen':'Farbflächen','glyphen':'Glyphen/Zahlen','streifen':'Streifen/Verläufe/Ringe',
        'material':'Gold/Chrom + Abnutzung','schmuck':'Schmuckteile'}
LAYER_BLOCK={'side_block':'farbflaechen','bands':'streifen','gradient':'streifen','rings':'streifen','glyphs':'glyphen',
             'finish':'material','edge_wear':'material','trim':'schmuck'}
BARE_METAL='#B9C0C8'      # Farbe der Kantenabnutzung (blankes Metall)
# Rückfall, wenn ein Kanal an der Waffe nicht belegt ist: Farbfeld der Blatt-Palette (hell, mittel, dunkel, Akzent)
SWATCH_FALLBACK={'MT_Primary':0,'MT_Secondary':1,'MT_Metal':1,'MT_Detail':2,'MT_Accent':3,'MT_Energy':3,'MT_Emission':3}

GOLD='#E2B04A';CHROME='#C9D2DC';WHITE='#F2F4F6';INK='#15171A';HAZARD='#F2C230';NEON='#6CF2FF'

# ---------- Katalog. Lagen in normierten Koordinaten des Waffenkörpers: u 0..1 von hinten nach vorn (Modell x),
# v 0..1 von oben nach unten (Modell y). Bänder/Verläufe: Richtung im Modell, Lage/Breite als Anteil der Körperausdehnung
# entlang dieser Richtung. Ziele: body (Gehäuseflächen), metal (Läufe, Mündungen, Metallteile).
CATALOG=[
 dict(id='rennstreifen',name='Rennstreifen',accents={'SK_Accent1':(CHROME,'polished_chrome'),'SK_Accent2':(WHITE,'paint')},
      layers=[dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='bands',dir=(0,0,1),at=0.28,width=0.13,period=0.31,count=2,slots=['MT_Accent']),
              dict(type='bands',dir=(0,1,0),at=0.36,width=0.12,count=1,slots=['MT_Accent']),
              dict(type='bands',dir=(0,1,0),at=0.52,width=0.035,count=1,slots=['SK_Accent2']),
              dict(type='glyphs',items='num',height=0.30,at=(0.28,0.66),slots=['SK_Accent2']),
              dict(type='edge_wear',target='body',width=0.022,coverage=0.25)]),
 dict(id='goldglyphe',name='Goldglyphe',accents={'SK_Accent1':(GOLD,'polished_gold'),'SK_Accent2':('#8A6420','paint')},
      layers=[dict(type='side_block',poly=[(-0.1,-0.1),(1.1,-0.1),(1.1,1.1),(-0.1,1.1)],slot='MT_Detail'),
              dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='bands',dir=(0,1,0),at=0.18,width=0.03,count=1,slots=['SK_Accent1']),
              dict(type='glyphs',items='runes6',height=0.20,at=(0.55,0.45),slots=['SK_Accent1']),
              dict(type='trim',kind='fins',count=3,slot='SK_Accent1',at=0.85),
              dict(type='edge_wear',target='body',width=0.02,coverage=0.35)]),
 dict(id='warnblock',name='Warnblock',accents={'SK_Accent1':(HAZARD,'paint'),'SK_Accent2':(INK,'paint')},
      layers=[dict(type='bands',dir=(1,-1,0),at=0.0,width=0.045,period=0.09,count=40,slots=['SK_Accent1','SK_Accent2'],
                   window=[(0.74,-0.1),(1.1,-0.1),(1.1,1.1),(0.74,1.1)]),
              dict(type='side_block',poly=[(-0.1,-0.1),(0.22,-0.1),(0.22,1.1),(-0.1,1.1)],slot='MT_Secondary'),
              dict(type='glyphs',items='chevron+num',height=0.26,at=(0.48,0.55),slots=['SK_Accent2']),
              dict(type='edge_wear',target='body',width=0.03,coverage=0.6)]),
 dict(id='zweiton',name='Zweiton-Diagonale',accents={'SK_Accent1':(CHROME,'polished_chrome'),'SK_Accent2':(WHITE,'paint')},
      layers=[dict(type='side_block',poly=[(0.40,-0.1),(1.1,-0.1),(1.1,1.1),(0.62,1.1)],slot='MT_Detail'),
              dict(type='bands',along=((0.40,-0.1),(0.62,1.1)),width=0.025,slots=['MT_Accent']),
              dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='glyphs',items='cube',height=0.36,at=(0.22,0.5),slots=['SK_Accent2','MT_Accent','SK_Accent1']),
              dict(type='edge_wear',target='body',width=0.018,coverage=0.2)]),
 dict(id='stufenblock',name='Stufenblock',accents={'SK_Accent1':(GOLD,'polished_gold'),'SK_Accent2':(INK,'paint')},
      layers=[dict(type='side_block',poly=[(-0.1,0.62),(0.34,0.62),(0.34,0.40),(0.68,0.40),(0.68,0.18),(1.1,0.18),(1.1,1.1),(-0.1,1.1)],slot='MT_Detail'),
              dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='glyphs',items='num',height=0.22,at=(0.80,0.62),slots=['MT_Primary']),
              dict(type='trim',kind='ribs',count=4,slot='SK_Accent1',at=(0.18,0.35)),
              dict(type='edge_wear',target='body',width=0.02,coverage=0.3)]),
 dict(id='zielringe',name='Zielringe',accents={'SK_Accent1':(CHROME,'polished_chrome'),'SK_Accent2':(WHITE,'paint')},
      layers=[dict(type='rings',center=(0.42,0.48),r0=0.10,width=0.11,gap=0.11,count=4,slots=['MT_Accent','SK_Accent2']),
              dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='glyphs',items='runes4',height=0.14,at=(0.80,0.30),slots=['MT_Accent']),
              dict(type='edge_wear',target='body',width=0.018,coverage=0.2)]),
 dict(id='glutverlauf',name='Glutverlauf',accents={'SK_Accent1':('#3A3F47','polished_chrome'),'SK_Accent2':(NEON,'neon')},
      layers=[dict(type='gradient',dir=(1,0,0),start=0.30,end=0.95,steps=5,slots=['MT_Primary','MT_Accent']),
              dict(type='bands',dir=(0,1,0),at=0.66,width=0.03,period=0.07,count=2,slots=['SK_Accent2']),
              dict(type='trim',kind='ribs',count=5,slot='SK_Accent1',at=(0.12,0.40)),
              dict(type='edge_wear',target='body',width=0.018,coverage=0.25)]),
 dict(id='chromrippe',name='Chromrippe',accents={'SK_Accent1':(CHROME,'polished_chrome'),'SK_Accent2':(INK,'paint')},
      layers=[dict(type='side_block',poly=[(-0.1,-0.1),(1.1,-0.1),(1.1,1.1),(-0.1,1.1)],slot='MT_Detail'),
              dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='bands',dir=(0,1,0),at=0.84,width=0.08,count=1,slots=['MT_Accent']),
              dict(type='trim',kind='ribs',count=6,slot='SK_Accent1',at=(0.45,0.40)),
              dict(type='trim',kind='fins',count=2,slot='SK_Accent1',at=0.85),
              dict(type='edge_wear',target='body',width=0.024,coverage=0.4)]),
 dict(id='glyphenband',name='Glyphenband',accents={'SK_Accent1':(CHROME,'polished_chrome'),'SK_Accent2':(NEON,'neon')},
      layers=[dict(type='finish',target='metal',slot='SK_Accent1'),
              dict(type='glyphs',items='runes7',height=0.16,at=(0.55,0.42),slots=['SK_Accent2'],band='MT_Detail'),
              dict(type='edge_wear',target='body',width=0.018,coverage=0.2)]),
]
BY_ID={s['id']:s for s in CATALOG}

def pick(sheet,full=None,num=None):
    """fünf Skins je Blatt; der erste ist der Hauptskin (Isometrie, Orthos, Farbvarianten). Reihenfolge: Drehung des Katalogs
    je Blatt (Schritt 2 über 9 Skins), dann – wenn das Modell gegeben ist – Skins, deren Lagen alle Platz finden, zuerst."""
    fam='CDFGH'.index(sheet[1]);n=int(sheet[2:])
    st=(n+fam*5)%len(CATALOG)   # gleichmäßig über die 50 Blätter, Probeblätter verschieden
    order=[CATALOG[(st+2*j)%len(CATALOG)]['id'] for j in range(len(CATALOG))]
    if full is not None:
        miss={sid:sum(1 for t in resolve(full,sid,sheet,num)['notes'] if not t.startswith('finish')) for sid in order}
        order=sorted(order,key=lambda sid:miss[sid])
    return order[:5]

# ---------- Glyphen: eigene Segmentziffern (schräg), eigene Runen, Embleme. Zeichenbox 1×2 (Ziffern/Runen), 2×2 (Embleme).
T=0.27
def _seg(p,q,t=T):
    """Segment mit spitzen Enden (Sechseck) von p nach q"""
    (x0,y0),(x1,y1)=p,q;L=math.hypot(x1-x0,y1-y0);ux,uy=(x1-x0)/L,(y1-y0)/L;nx,ny=-uy,ux;h=t/2
    return [(x0,y0),(x0+ux*h+nx*h,y0+uy*h+ny*h),(x1-ux*h+nx*h,y1-uy*h+ny*h),(x1,y1),(x1-ux*h-nx*h,y1-uy*h-ny*h),(x0+ux*h-nx*h,y0+uy*h-ny*h)]
def _bar(p,q,t=T):
    (x0,y0),(x1,y1)=p,q;L=math.hypot(x1-x0,y1-y0);nx,ny=-(y1-y0)/L*t/2,(x1-x0)/L*t/2
    return [(x0+nx,y0+ny),(x1+nx,y1+ny),(x1-nx,y1-ny),(x0-nx,y0-ny)]
_g=0.06;_a,_b=T/2,1-T/2
SEGS={'a':((_a+_g,_a),(_b-_g,_a)),'g':((_a+_g,1),(_b-_g,1)),'d':((_a+_g,2-_a),(_b-_g,2-_a)),
      'f':((_a,_a+_g),(_a,1-_g)),'b':((_b,_a+_g),(_b,1-_g)),'e':((_a,1+_g),(_a,2-_a-_g)),'c':((_b,1+_g),(_b,2-_a-_g))}
DIGITS={'0':'abcdef','1':'bc','2':'abged','3':'abgcd','4':'fgbc','5':'afgcd','6':'afgedc','7':'abc','8':'abcdefg','9':'abcdfg'}
RUNES=[  # eigene Zeichen, keine Schrift eines bestehenden Spiels
 [((0.15,0),(0.15,2)),((0.15,0.55),(0.9,0.05))],
 [((0.5,0),(0.5,2)),((0.08,0.7),(0.92,0.7)),((0.08,1.4),(0.92,1.4))],
 [((0.1,0.05),(0.9,1)),((0.9,1),(0.1,1.95))],
 [((0.08,0.12),(0.92,0.12)),((0.5,0.12),(0.5,1.25)),((0.08,1.95),(0.92,1.25))],
 [((0.5,0.05),(0.08,1.0)),((0.5,0.05),(0.92,1.0)),((0.5,1.25),(0.5,2))],
 [((0.08,0.3),(0.92,0.3)),((0.08,1.0),(0.92,1.0)),((0.08,1.7),(0.92,1.7)),((0.5,0.3),(0.5,1.0))],
 [((0.1,0.05),(0.5,1.95)),((0.5,1.95),(0.9,0.05)),((0.2,0.75),(0.8,0.75))],
 [((0.12,0),(0.12,1.3)),((0.12,1.3),(0.9,1.95)),((0.9,0),(0.9,1.0))],
]
SLANT=0.16
def _slant(poly,h=2.0):return [(x+(h-y)*SLANT,y) for x,y in poly]
def _shrink(poly,f=0.9):
    cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly)
    return [(cx+(x-cx)*f,cy+(y-cy)*f) for x,y in poly]
def emblem(kind):
    """(Polygon, Farbindex) in Box 2×2"""
    if kind=='cube':   # Würfel (Cube-Escape-Motiv) aus drei Rauten
        s=0.866;c=(1,1);top=[(1,0),(1+s,0.5),c,(1-s,0.5)];lf=[(1-s,0.5),c,(1,2),(1-s,1.5)];rt=[c,(1+s,0.5),(1+s,1.5),(1,2)]
        return [(_shrink(top,0.86),0),(_shrink(lf,0.86),1),(_shrink(rt,0.86),2)]
    if kind=='chevron':  # drei Winkel nach vorn (Mündung)
        out=[]
        for k in range(3):
            o=k*0.55;out.append(([(o,0),(o+0.34,0),(o+0.9,1),(o+0.34,2),(o,2),(o+0.56,1)],0))
        return out
    if kind=='ring':
        oc=circ(1,1,1,28);ic=circ(1,1,0.68,28)
        return [(oc+[oc[0]]+[ic[0]]+ic[::-1]+[ic[0]],0),(circ(1,1,0.3,16),0)]
    raise KeyError(kind)
def glyph_items(spec,sheet,num):
    """Inhalt einer Glyphen-Lage: Liste ('digit'|'rune'|'emblem', Wert)"""
    seed=sum(ord(c)*(i+3) for i,c in enumerate(sheet))
    if spec=='num':return [('digit',ch) for ch in num]
    if spec.startswith('runes'):
        n=int(spec[5:]);return [('rune',(seed*7+i*5+(i*i)%3)%len(RUNES)) for i in range(n)]
    if spec=='chevron+num':return [('emblem','chevron')]+[('digit',ch) for ch in num]
    return [('emblem',spec)]
def layout(items,h):
    """Polygone (x,y) einer Glyphenzeile der Höhe h, Ursprung oben links; Rückgabe (Liste (Polygon, Farbindex), Breite)"""
    k=h/2.0;x=0.0;out=[]
    for kind,val in items:
        if kind=='digit':
            for sname in DIGITS[val]:out.append(([(x+px*k,py*k) for px,py in _slant(_seg(*SEGS[sname]))],0))
            x+=(1+SLANT*2+0.42)*k
        elif kind=='rune':
            for p,q in RUNES[val]:out.append(([(x+px*k,py*k) for px,py in _slant(_bar(p,q,0.24))],0))
            x+=(1+SLANT*2+0.45)*k
        else:
            for poly,ci in emblem(val):out.append(([(x+px*k,py*k) for px,py in poly],ci))
            x+=(2.0+(1.1 if val=='chevron' else 0)+0.5)*k
    w=x-0.42*k
    return out,w

# ---------- Geometrie-Hilfen (Modellkoordinaten: x vorn, y unten, z links)
def _verts(P):return [q for f in P['F'] for q in f['v']]
def bbox(P):
    vs=_verts(P);return [min(q[0] for q in vs),min(q[1] for q in vs),min(q[2] for q in vs)],[max(q[0] for q in vs),max(q[1] for q in vs),max(q[2] for q in vs)]
def side_face(P):
    """Prisma: Profil (x,y) der Seitenfläche, z0, z1; sonst None"""
    f=P['F'][0]
    if tuple(f['n'])!=(0,0,1):return None
    return [(x,y) for x,y,_ in f['v']],P['F'][1]['v'][0][2],f['v'][0][2]
def inside(poly,x,y):
    c=False;n=len(poly)
    for i in range(n):
        (x0,y0),(x1,y1)=poly[i],poly[i-1]
        if (y0>y)!=(y1>y) and x<(x1-x0)*(y-y0)/(y1-y0)+x0:c=not c
    return c
def _rect_hit(a,b,pad=0):return not(a[2]+pad<=b[0] or b[2]+pad<=a[0] or a[3]+pad<=b[1] or b[3]+pad<=a[1])
def top_at(P,x):
    """Oberkante (kleinstes y) des Teils an der Stelle x, oder None"""
    sf=side_face(P)
    if sf:
        poly=sf[0];ys=[]
        for i in range(len(poly)):
            (x0,y0),(x1,y1)=poly[i],poly[i-1]
            if (x0<=x<=x1 or x1<=x<=x0) and x0!=x1:ys.append(y0+(y1-y0)*(x-x0)/(x1-x0))
        return min(ys) if ys else None
    lo,hi=bbox(P)
    if tuple(P['F'][0]['n'])==(1,0,0) and lo[0]<=x<=hi[0]:return lo[1]
    return None

class Frame:
    """Körperrahmen einer Waffe: Ziele body/metal, normierte Koordinaten u/v"""
    def __init__(s,full):
        s.full=full
        gun=[(i,P) for i,P in enumerate(full.parts) if not P.get('sight')]
        from eng import Model as _M
        gm=_M();gm.parts=[P for _,P in gun]
        role=color_roles(gm)
        s.gun=gun
        body=[];metal=[]
        for i,P in gun:
            if P['emit']:continue
            lb=P.get('label') or ''
            r=role(P['col'],False)
            if lb in METAL_LABELS or (material_of(P)=='brushed' and r not in ('light','lightx')):metal.append(i)
            elif r in ('light','lightx') and lb not in DARK_LABELS and lb not in GRIP_LABELS:body.append(i)
        tot=sum(part_area(P) for _,P in gun)
        if sum(part_area(full.parts[i]) for i in body)<0.15*tot:   # Körper zu klein (dunkle Waffe): größte Nicht-Metallteile dazu
            rest=sorted([i for i,P in gun if not P['emit'] and i not in body and i not in metal and (P.get('label') or '') not in DARK_LABELS],
                        key=lambda i:-part_area(full.parts[i]))
            for i in rest:
                body.append(i)
                if sum(part_area(full.parts[j]) for j in body)>=0.25*tot:break
        s.body=sorted(body);s.metal=sorted(metal)
        bbs=[bbox(full.parts[i]) for i in s.body] or [bbox(P) for _,P in gun]
        s.lo=[min(b[0][k] for b in bbs) for k in range(3)];s.hi=[max(b[1][k] for b in bbs) for k in range(3)]
        gb=[bbox(P) for _,P in gun]
        s.glo=[min(b[0][k] for b in gb) for k in range(3)];s.ghi=[max(b[1][k] for b in gb) for k in range(3)]
        s.L=s.hi[0]-s.lo[0];s.H=s.hi[1]-s.lo[1];s.W=s.hi[2]-s.lo[2]
        s.base=min(s.H,0.32*s.L)   # Bezugshöhe für Glyphen/Rippen (Bogen: Spannweite zählt nicht)
    def xy(s,u,v):return (s.lo[0]+u*s.L,s.lo[1]+v*s.H)
    def extent(s,d):
        cs=[(x,y,z) for x in (s.lo[0],s.hi[0]) for y in (s.lo[1],s.hi[1]) for z in (s.lo[2],s.hi[2])]
        ts=[x*d[0]+y*d[1]+z*d[2] for x,y,z in cs];return min(ts),max(ts)
    def target(s,t):return s.metal if t=='metal' else s.body

def _unit(d):L=math.sqrt(sum(a*a for a in d));return tuple(a/L for a in d)

def _blockers(F,i,side,extra):
    """Rechtecke (x0,y0,x1,y1), die die Seitenfläche von Teil i auf der Seite +1/-1 verdecken oder schon belegt sind"""
    P=F.full.parts[i];poly,z0,z1=side_face(P);zf=z1 if side>0 else z0
    out=list(extra)
    for j,Q in F.gun:
        if j==i:continue
        lo,hi=bbox(Q)
        if (side>0 and hi[2]>zf+0.5) or (side<0 and lo[2]<zf-0.5):out.append((lo[0],lo[1],hi[0],hi[1]))
    pl='z+' if side>0 else 'z-'
    for plane,val,pts,_,_ in P['dec']:
        if plane==pl and abs(val-zf)<1.0:
            out.append((min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)))
    return out

def place_rect(F,w,h,at,avoid=(),scales=(1,0.85,0.72,0.6,0.5),pad=None):
    """Freies Rechteck w×h auf der Seitenfläche eines Prismas (beide Seiten frei, ganz in der Fläche, nicht verdeckt),
    nahe der Wunschlage at=(u,v). Erst Körperteile, dann übrige flache Teile der Waffe (Rohr-Körper: Kästen, Griffstücke).
    Rückgabe (Teil, (x0,y0,x1,y1), Maßstab) oder None."""
    def flat(ids):return sorted([i for i in ids if side_face(F.full.parts[i])],key=lambda i:-area_poly(side_face(F.full.parts[i])[0]))[:6]
    groups=[flat(F.body),flat([i for i,P in F.gun if i not in F.body and not P['emit'] and (P.get('label') or '') not in ('Abzug','Abzugbügel')])]
    tx,ty=F.xy(*at)
    info={}
    for i in groups[0]+groups[1]:
        poly=side_face(F.full.parts[i])[0]
        info[i]=(poly,_blockers(F,i,1,avoid)+_blockers(F,i,-1,avoid),min(p[0] for p in poly),max(p[0] for p in poly),min(p[1] for p in poly),max(p[1] for p in poly))
    for cands in groups:
        for sc in scales:
            ww,hh=w*sc,h*sc;pd=pad if pad is not None else 0.12*hh
            best=None
            for i in cands:
                poly,bl,x0_,x1_,y0_,y1_=info[i]
                if x1_-x0_<ww or y1_-y0_<hh:continue
                st=max(1.0,hh*0.3);x=x0_
                while x+ww<=x1_:
                    y=y0_
                    while y+hh<=y1_:
                        r=(x,y,x+ww,y+hh)
                        if not any(_rect_hit(r,q,pd) for q in bl) and \
                           all(inside(poly,x+ww*a,y+hh*b) for a in (-0.04,0.25,0.5,0.75,1.04) for b in (-0.08,0.5,1.08)):
                            sc_=(x+ww/2-tx)**2+(y+hh/2-ty)**2
                            if best is None or sc_<best[0]:best=(sc_,i,r)
                        y+=st
                    x+=st
            if best:return best[1],best[2],sc
    return None
def area_poly(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))/2

# ---------- Auflösen
_CACHE={}
def resolve(full,sid,sheet,num):
    key=(id(full),len(full.parts),sid,sheet,num)
    if key not in _CACHE:_CACHE[key]=_resolve(full,sid,sheet,num)
    return _CACHE[key]
def _resolve(full,sid,sheet,num):
    """Katalog-Skin sid für das Modell full (Visier eingeschlossen; Skins gelten nur für die Waffe ohne Visier).
    Rückgabe: dict(id,name,accents,layers[...],notes[...]) in Modelleinheiten."""
    S=BY_ID[sid];F=Frame(full)
    out=dict(id=sid,name=S['name'],accents=S['accents'],layers=[],notes=[],frame=dict(lo=F.lo,hi=F.hi))
    taken=[]
    def uvpoly(poly):return [F.xy(u,v) for u,v in poly]
    for Lr in S['layers']:
        t=Lr['type']
        if t=='finish':
            ps=F.target(Lr['target'])
            if not ps:out['notes'].append(f"finish {Lr['target']}: keine Teile");continue
            out['layers'].append(dict(type=t,parts=ps,slot=Lr['slot'],target=Lr['target']))
        elif t=='side_block':
            out['layers'].append(dict(type=t,parts=F.body,poly=uvpoly(Lr['poly']),slot=Lr['slot']))
        elif t=='bands':
            if 'along' in Lr:   # Linie entlang einer Kante (Farbteilung): Richtung senkrecht zur Linie in der Seitenebene
                (a,b)=[F.xy(*p) for p in Lr['along']];dx,dy=b[0]-a[0],b[1]-a[1];d=_unit((dy,-dx,0))
                t0=a[0]*d[0]+a[1]*d[1];w=Lr['width']*F.L
                out['layers'].append(dict(type=t,parts=F.body,dir=d,t0=t0-w/2,width=w,period=w,count=1,slots=Lr['slots'],window=None))
                continue
            d=_unit(Lr['dir']);e0,e1=F.extent(d);E=e1-e0
            w=Lr['width']*E;per=Lr.get('period',Lr['width'])*E
            out['layers'].append(dict(type=t,parts=F.body,dir=d,t0=e0+Lr['at']*E,width=w,period=per,count=Lr['count'],
                                      slots=Lr['slots'],window=uvpoly(Lr['window']) if Lr.get('window') else None))
        elif t=='gradient':
            d=_unit(Lr['dir']);e0,e1=F.extent(d);E=e1-e0
            out['layers'].append(dict(type=t,parts=F.body,dir=d,t0=e0+Lr['start']*E,t1=e0+Lr['end']*E,steps=Lr['steps'],slots=Lr['slots']))
        elif t=='rings':
            c=F.xy(*Lr['center']);u=F.base
            out['layers'].append(dict(type=t,parts=F.body,center=c,r0=Lr['r0']*u,width=Lr['width']*u,gap=Lr['gap']*u,
                                      count=Lr['count'],slots=Lr['slots']))
        elif t=='edge_wear':
            out['layers'].append(dict(type=t,parts=F.target(Lr['target']),width=Lr['width']*F.base,coverage=Lr['coverage'],color=BARE_METAL))
        elif t=='glyphs':
            items=glyph_items(Lr['items'],sheet,num);h=Lr['height']*F.base
            polys,w=layout(items,h)
            pl=place_rect(F,w,h,Lr['at'],taken,scales=(1,0.85,0.72,0.6,0.5,0.42,0.35))
            if not pl:out['notes'].append(f"glyphs {Lr['items']}: kein freier Platz auf einer Seitenfläche");continue
            i,(x0,y0,x1,y1),sc=pl;taken.append((x0,y0,x1,y1))
            P=full.parts[i];_,z0,z1=side_face(P)
            decs=[]
            for poly,ci in polys:
                pts=[(x0+px*sc,y0+py*sc) for px,py in poly]
                slot=Lr['slots'][min(ci,len(Lr['slots'])-1)]
                decs.append(('z+',z1,pts,slot))
                decs.append(('z-',z0,[(x0+x1-px,py) for px,py in pts],slot))   # rechte Seite gespiegelt: liest sich richtig
            content=' '.join(str(v) for _,v in items)
            out['layers'].append(dict(type=t,part=i,items=Lr['items'],content=content,rect=(x0,y0,x1,y1),height=h*sc,decals=decs))
            if Lr.get('band'):   # dunkles Band hinter der Glyphenzeile (über alle Körperteile)
                pad=(y1-y0)*0.32;d=(0.0,1.0,0.0)
                out['layers'].insert(len(out['layers'])-1,dict(type='bands',parts=F.body,dir=d,t0=y0-pad,width=(y1-y0)+2*pad,
                                     period=(y1-y0)+2*pad,count=1,slots=[Lr['band']],window=None))
        elif t=='trim':
            r=_trim(F,Lr,taken)
            if not r:out['notes'].append(f"trim {Lr['kind']}: kein freier Platz");continue
            out['layers'].append(r)
    return out

def _trim(F,Lr,taken):
    if Lr['kind']=='ribs':
        n=Lr['count'];rw=0.022*F.L;gap=rw*1.3;h=0.42*F.base;w=n*rw+(n-1)*gap
        pl=place_rect(F,w,h,Lr['at'],taken,scales=(1,0.85,0.7,0.55,0.45,0.36))
        if not pl:return None
        i,(x0,y0,x1,y1),sc=pl;taken.append((x0,y0,x1,y1))
        P=F.full.parts[i];_,z0,z1=side_face(P);e=max(2.0,0.035*F.W)
        parts=[]
        for k in range(n):
            xx=x0+k*(rw+gap)*sc
            prof=[(xx,y0),(xx+rw*sc,y0),(xx+rw*sc,y1),(xx,y1)]
            parts.append(dict(prof=prof,z0=z1-0.6,z1=z1+e,attach=i))
            parts.append(dict(prof=prof,z0=z0-e,z1=z0+0.6,attach=i))
        return dict(type='trim',kind='ribs',slot=Lr['slot'],parts=parts,attach=i,count=n)
    # Finnen oben, schräg nach hinten; nicht über Visierschiene/Visier und nicht in andere Teile
    n=Lr['count'];fw=0.03*F.L;fh=0.2*F.base;lean=0.55*fh;stp=fw*2.1;th=max(2.0,0.04*F.L)
    keep=[]
    for j,Q in enumerate(F.full.parts):
        if Q.get('sight') or (Q.get('label') or '') in ('Visierschiene','Montage','Montageringe'):
            lo,hi=bbox(Q);keep.append((lo[0]-fw,hi[0]+fw))
    cands=[i for i in F.body+F.metal]
    tx=F.xy(Lr['at'],0)[0];best=None
    for i in cands:
        P=F.full.parts[i];lo,hi=bbox(P);zc=(lo[2]+hi[2])/2
        x=lo[0]+lean+fw
        while x+(n-1)*stp+fw<=hi[0]-fw:
            fins=[];ok=True
            for k in range(n):
                xa=x+k*stp;ta,tb=top_at(P,xa),top_at(P,xa+fw)
                if ta is None or tb is None or abs(ta-tb)>0.25*fh:ok=False;break
                yb=max(ta,tb)+1.5
                box=(xa-lean,yb-fh-max(ta,tb)+min(ta,tb),xa+fw,min(ta,tb)-0.5)
                if any(a<=xa+fw and xa-lean<=b for a,b in keep):ok=False;break
                for j,Q in F.gun:
                    if j==i:continue
                    ql,qh=bbox(Q)
                    if ql[0]<box[2] and box[0]<qh[0] and ql[1]<box[3] and box[1]<qh[1] and ql[2]<zc+th and zc-th<qh[2]:ok=False;break
                if not ok:break
                fins.append(dict(prof=[(xa,yb),(xa+fw,yb),(xa+fw-lean,min(ta,tb)-fh),(xa-lean,min(ta,tb)-fh)],z0=zc-th/2,z1=zc+th/2,attach=i))
            if ok:
                sc_=abs(x-tx)
                if best is None or sc_<best[0]:best=(sc_,i,fins)
            x+=fw*0.5
    if not best:   # kein Platz oben: Rippen an der Seite
        return _trim(F,dict(Lr,kind='ribs',at=(Lr['at'],0.4)),taken)
    return dict(type='trim',kind='fins',slot=Lr['slot'],parts=best[2],attach=best[1],count=n)

# ---------- Farben und Anwenden
def slot_colors(rs,chans,swatches):
    """Farbe und Oberfläche je Slot für eine Variante: MT_-Kanal aus der Palette (unbelegt: Farbfeld der Blatt-Palette),
    Akzente fest aus dem Skin. Rückgabe {slot: (hex, finish, quelle)}"""
    out={}
    for ch in CHANNELS:
        c=chans.get(ch)
        out[ch]=(c,'paint','channel') if c else (swatches[SWATCH_FALLBACK[ch]].upper(),'paint','swatch')
    for a,(c,fin) in rs['accents'].items():out[a]=(c,fin,'accent')
    if 'MT_Energy' in out:out['MT_Energy']=(out['MT_Energy'][0],'neon',out['MT_Energy'][2])
    return out

def slots_used(rs):
    u=[]
    for L in rs['layers']:
        for s in ([L['slot']] if 'slot' in L else [])+list(L.get('slots',[]))+[d[3] for d in L.get('decals',[])]:
            if s not in u:u.append(s)
    return [s for s in SLOTS if s in u]

def apply(m,rs,colors):
    """Kopie von m mit Skin-Markierungen: '_sk' (Index im Modell), Glyphen als Aufkleber, Schmuckteile als neue Teile.
    Musterflächen malt xl.skin_texture() beim Rastern."""
    m2=copy.copy(m);m2.parts=[]
    idx={id(P):i for i,P in enumerate(m.parts)}
    add={}
    for L in rs['layers']:
        if L['type']=='glyphs':
            for plane,val,pts,slot in L['decals']:add.setdefault(L['part'],[]).append((plane,val,pts,colors[slot][0],colors[slot][1]=='neon'))
    for i,P in enumerate(m.parts):
        Q=dict(P);Q['_sk']=i
        if i in add:Q['dec']=list(P['dec'])+add[i]
        m2.parts.append(Q)
    for L in rs['layers']:
        if L['type']!='trim':continue
        c,fin,_=colors[L['slot']]
        for tp in L['parts']:
            tm=Model();tm.prism(tp['prof'],c,tp['z0'],tp['z1'],r=0)
            Q=tm.parts[-1];Q['_sk']=-1;Q['_skslot']=L['slot'];Q['bias']=0.5
            m2.parts.append(Q)
    return m2

def summary(rs):
    """Bausteine eines aufgelösten Skins (für Blatt und Spec)"""
    b=[]
    for L in rs['layers']:
        k=LAYER_BLOCK[L['type']]
        if k not in b:b.append(k)
    return [k for k in BLOCKS if k in b]

# Kurzbeschreibung je Skin für die Prompts des Blatts (deutsch, englisch)
DESC={
 'rennstreifen':('zwei Rennstreifen in Akzentfarbe über die Oberseite, Seitenband mit weißer Zierlinie, große schräge Segmentnummer, Läufe poliertes Chrom, leichte Kantenabnutzung',
                 'two accent racing stripes over the top, side band with white pinstripe, large slanted segment number, polished chrome barrels, light edge wear'),
 'goldglyphe':('dunkles Gehäuse, poliertes Gold an Läufen und Mündung, goldene Runenzeile und Zierlinie, goldene Finnen, Kantenabnutzung',
               'dark body, polished gold barrels and muzzle, row of gold glyphs and gold pinstripe, gold fins, edge wear'),
 'warnblock':('gelb-schwarze Warnstreifen vorn, Heckblock in Zweitfarbe, Winkel-Emblem mit Nummer, starke Kantenabnutzung',
              'yellow-black hazard stripes at the front, rear block in secondary color, chevron emblem with number, heavy edge wear'),
 'zweiton':('diagonale Zweifarb-Teilung mit Akzentlinie, Würfel-Emblem, Chrom an Läufen',
            'diagonal two-tone split with accent line, cube emblem, chrome barrels'),
 'stufenblock':('gestufte Farbblöcke dunkel unter hell, Gold an Metallteilen, goldene Rippen, Segmentnummer',
                'stepped color blocks dark below light, gold metal parts, gold ribs, segment number'),
 'zielringe':('konzentrische Ringe in Akzentfarbe und Weiß auf der Seite, kleine Runen, Chrom an Läufen',
              'concentric accent and white rings on the side, small glyphs, chrome barrels'),
 'glutverlauf':('gestufter Farbverlauf von der Grundfarbe zur Akzentfarbe nach vorn, zwei leuchtende Neonlinien, dunkle Chromrippen',
                'stepped color gradient from base to accent toward the muzzle, two glowing neon lines, dark chrome ribs'),
 'chromrippe':('dunkles Gehäuse, Chromrippen an der Seite, Chromfinnen, Akzentband unten, Kantenabnutzung',
               'dark body, chrome side ribs, chrome fins, accent band along the bottom, edge wear'),
 'glyphenband':('dunkles Band mit leuchtender Neon-Runenzeile über die Seite, Chrom an Läufen',
                'dark side band with a glowing neon glyph row, chrome barrels'),
}
SLOT_DE={'MT_Primary':'Primär','MT_Secondary':'Sekundär','MT_Accent':'Akzent','MT_Metal':'Metall','MT_Energy':'Energie',
         'MT_Emission':'Leuchte','MT_Detail':'Detail','SK_Accent1':'Skin-Akzent 1','SK_Accent2':'Skin-Akzent 2'}
FINISH_DE={'paint':'Lack','polished_gold':'Gold poliert','polished_chrome':'Chrom poliert','neon':'Neon'}
