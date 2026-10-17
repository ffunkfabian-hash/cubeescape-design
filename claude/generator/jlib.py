"""Modell-Bausteine der Variante J „Black Ice“ (claude-0.4): facettierte Stealth-Körper.

Formliste wie flib (eine Liste von Einträgen, je Eintrag ein Teil von m.parts in gleicher Reihenfolge), dazu:
- K(...)  Facettenprisma: Seitenprofil (x,y) wie bei eng.prism, aber die Kanten zu beiden Seitenflächen sind breit
          abgeschrägt (Fase b in x/y, Tiefe bz in z). Ergebnis: ebene Seitenfläche (eingerückt), schräge Facetten rundum,
          schmales Mittelband. Alle Flächen hart (Kontur zwischen allen Facetten) – keine Rundungen.
- X(...)  Lauf/Rohr als Vieleck entlang x (Sechs- oder Achtkant), alle Flächen hart.
- glow_edges(...)  Leuchtkanten: schmale, leuchtende Aufkleber entlang ausgewählter Kanten der Seitenfläche.
Einträge tragen label/sight/ch wie hxlib bzw. eng.copy_channels.

Flächenreihenfolge eines K-Teils (skins.side_face, export_spec erwarten das): F[0] Seitenfläche z1 (n=(0,0,1)),
F[1] Seitenfläche z0 (n=(0,0,-1)), danach Mittelband und Facetten.
"""
import math
from eng import Model,rect,circ,CHANNELS,copy_channels
from ext import frustum

def _area(p):return sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2
def _onorm(a,b):
    ex,ey=b[0]-a[0],b[1]-a[1];L=math.hypot(ex,ey) or 1
    return ey/L,-ex/L   # nach außen bei positiver Fläche (y nach unten, wie eng.prism)
def inset(prof,b):
    """Profil um b nach innen versetzt (Gehrung je Ecke). Prüft, dass keine Kante kippt (Profil sonst zu spitz für die Fase)."""
    if _area(prof)<0:prof=prof[::-1]
    n=len(prof);out=[]
    for i in range(n):
        p0,p1,p2=prof[i-1],prof[i],prof[(i+1)%n]
        n1=_onorm(p0,p1);n2=_onorm(p1,p2);d=1+n1[0]*n2[0]+n1[1]*n2[1]
        if d<0.25:raise ValueError(f'Ecke {p1} zu spitz für eine Fase')
        out.append((p1[0]-b*(n1[0]+n2[0])/d,p1[1]-b*(n1[1]+n2[1])/d))
    for i in range(n):
        a,c=prof[i],prof[(i+1)%n];a2,c2=out[i],out[(i+1)%n]
        if (c[0]-a[0])*(c2[0]-a2[0])+(c[1]-a[1])*(c2[1]-a2[1])<=0:
            raise ValueError(f'Fase {b} zu breit für Kante {a}–{c}')
    return out

def K(prof,col,z0,z1,b=None,bz=None,emit=False,dec=(),glow=(),xdec=(),label=None,sight=False,ch=None):
    """Facettenprisma. b: Fase in der Profilebene, bz: Fasentiefe je Seite (Standard: 40 % der halben Breite).
    dec: Aufkleber auf beiden Seitenflächen (Punkte x,y, müssen auf der eingerückten Fläche liegen).
    glow: Leuchtkanten als ((Kantenindex, …), Farbe[, Breite]) – Kante i läuft von Profilpunkt i nach i+1.
    xdec: weitere Aufkleber (Ebene, Wert, Punkte, Farbe, leuchtet) wie eng.decal, z. B. ('x+', x, [(y,z) …], …) auf einer
    senkrechten Stirnfläche des Mittelbands."""
    hw=(z1-z0)/2
    bz=0.4*hw if bz is None else bz;b=bz if b is None else b
    return dict(k='facet',prof=list(prof),col=col,z0=z0,z1=z1,b=b,bz=bz,emit=emit,dec=list(dec),glow=list(glow),xdec=list(xdec),
                label=label,sight=sight,ch=ch)
def X(x0,x1,cy,R,col,n=6,cz=0,emit=False,cap=(),label=None,sight=False,ch=None):
    """Vieleck-Lauf entlang x (n Kanten, eine Kante oben flach)."""
    return dict(k='poly_x',x0=x0,x1=x1,cy=cy,cz=cz,R=R,col=col,n=n,emit=emit,cap=list(cap),label=label,sight=sight,ch=ch)
def T(x0,x1,cy,R0,R1,col,cz=0,n=8,emit=False,label=None,sight=False,ch=None):
    """Kegelstumpf entlang x mit n harten Facetten (Linse, Düse)."""
    return dict(k='frus',x0=x0,x1=x1,cy=cy,cz=cz,R0=R0,R1=R1,col=col,n=n,emit=emit,label=label,sight=sight,ch=ch)

def facet(m,prof,col,z0,z1,b,bz,emit=False):
    if _area(prof)<0:prof=prof[::-1]
    ins=inset(prof,b) if b>0 else list(prof)
    zm0,zm1=z0+bz,z1-bz
    if zm1<zm0:zm0=zm1=(z0+z1)/2
    n=len(prof)
    F=[dict(v=[(x,y,z1) for x,y in ins],n=(0,0,1),hard=True),dict(v=[(x,y,z0) for x,y in ins[::-1]],n=(0,0,-1),hard=True)]
    for i in range(n):
        a,c=prof[i],prof[(i+1)%n];a2,c2=ins[i],ins[(i+1)%n];nx,ny=_onorm(a,c)
        if zm1>zm0:F.append(dict(v=[(a[0],a[1],zm1),(c[0],c[1],zm1),(c[0],c[1],zm0),(a[0],a[1],zm0)],n=(nx,ny,0),hard=True))
        if bz>0:
            L=math.sqrt((nx*bz)**2+(ny*bz)**2+b*b) or 1
            F.append(dict(v=[(a[0],a[1],zm1),(a2[0],a2[1],z1),(c2[0],c2[1],z1),(c[0],c[1],zm1)],n=(nx*bz/L,ny*bz/L,b/L),hard=True))
            F.append(dict(v=[(c[0],c[1],zm0),(c2[0],c2[1],z0),(a2[0],a2[1],z0),(a[0],a[1],zm0)],n=(nx*bz/L,ny*bz/L,-b/L),hard=True))
    m.parts.append(dict(F=F,col=col,emit=emit,dec=[],hull=True))
    return ins

def poly_x(m,x0,x1,cy,cz,R,col,n=6,emit=False):
    a0=math.pi/n   # eine Kante oben waagrecht
    ring=[(cy-R*math.cos(a0+2*math.pi*k/n),cz+R*math.sin(a0+2*math.pi*k/n)) for k in range(n)]
    F=[dict(v=[(x1,y,z) for y,z in ring],n=(1,0,0),hard=True),dict(v=[(x0,y,z) for y,z in ring[::-1]],n=(-1,0,0),hard=True)]
    for i in range(n):
        (ay,az),(by,bz)=ring[i],ring[(i+1)%n];my,mz=(ay+by)/2-cy,(az+bz)/2-cz;L=math.hypot(my,mz)
        F.append(dict(v=[(x0,ay,az),(x0,by,bz),(x1,by,bz),(x1,ay,az)],n=(0,my/L,mz/L),hard=True))
    m.parts.append(dict(F=F,col=col,emit=emit,dec=[]))

def strip(p,q,w,inward):
    """schmaler Streifen der Breite w entlang p→q, nach innen (Richtung inward) versetzt, Enden um w eingezogen"""
    ex,ey=q[0]-p[0],q[1]-p[1];L=math.hypot(ex,ey);ux,uy=ex/L,ey/L;ix,iy=inward
    a=(p[0]+ux*w,p[1]+uy*w);c=(q[0]-ux*w,q[1]-uy*w)
    return [a,c,(c[0]+ix*w,c[1]+iy*w),(a[0]+ix*w,a[1]+iy*w)]
def glow_edges(ins,edges,w,col):
    """Leuchtkanten auf der Seitenfläche: Kanten i (von Ecke i nach i+1 des eingerückten Profils), Abstand 0.6 w zur Kante"""
    if _area(ins)<0:ins=ins[::-1]
    out=[];n=len(ins)
    for i in edges:
        p,q=ins[i%n],ins[(i+1)%n];nx,ny=_onorm(p,q);g=0.6*w
        out.append((strip((p[0]-nx*g,p[1]-ny*g),(q[0]-nx*g,q[1]-ny*g),w,(-nx,-ny)),col,True))
    return out

def model(spec):
    m=Model()
    for s in spec:
        k=s['k']
        if k=='facet':
            ins=facet(m,s['prof'],s['col'],s['z0'],s['z1'],s['b'],s['bz'],emit=s['emit'])
            P=m.parts[-1]
            decs=list(s['dec'])
            for edges,c,*wd in s['glow']:decs+=glow_edges(ins,edges,wd[0] if wd else 2.2,c)
            for pts,c,e in decs:
                P['dec'].append(('z+',s['z1'],pts,c,e))
                P['dec'].append(('z-',s['z0'],pts,c,e))
            P['dec']+=[tuple(x) for x in s['xdec']]
        elif k=='poly_x':
            poly_x(m,s['x0'],s['x1'],s['cy'],s['cz'],s['R'],s['col'],n=s['n'],emit=s['emit'])
            for cy,cz,r,c,e in s['cap']:m.parts[-1]['dec'].append(('x+',s['x1'],circ(cy,cz,r,max(6,s['n'])),c,e))
        elif k=='frus':
            frustum(m,s['x0'],s['x1'],s['cy'],s['cz'],s['R0'],s['R1'],s['col'],n=s['n'],emit=s['emit'])
            for f in m.parts[-1]['F']:f['hard']=True
        else:raise KeyError(k)
    assert len(m.parts)==len(spec)
    for P,s in zip(m.parts,spec):
        if s.get('label'):P['label']=s['label']
        if s.get('sight'):P['sight']=True
    return copy_channels(m,spec)

def bbox(spec):
    xs=[];ys=[]
    for s in spec:
        if s['k']=='facet':xs+=[p[0] for p in s['prof']];ys+=[p[1] for p in s['prof']]
        else:R=s.get('R') or max(s['R0'],s['R1']);xs+=[s['x0'],s['x1']];ys+=[s['cy']-R,s['cy']+R]
    return min(xs),min(ys),max(xs),max(ys)
