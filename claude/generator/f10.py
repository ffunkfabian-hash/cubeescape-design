from flib import *
from flabel import Lb
from fsight import Sg
from eng import rect,circ,roundpoly
import math
I,E,PK,K='#3730A3','#F5EBDC','#FF5D8F','#1B1A2E'
def arcpts(cx,cy,r,a0,a1,n=10):return [(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)),cy+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
def limb(sign):
    # Sichelfoermiger Wurfarm (quadratische Kurve, verjuengt)
    p0=(372,300+sign*100);p1=(380,300+sign*176);p2=(276,300+sign*150)
    pts=[];n=12
    for i in range(n+1):
        t=i/n;pts.append(((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]))
    L=[];R=[]
    for i,p in enumerate(pts):
        a=pts[max(i-1,0)];b=pts[min(i+1,n)];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);w=(18-10*i/n)/2
        L.append((p[0]-dy/l*w,p[1]+dx/l*w));R.append((p[0]+dy/l*w,p[1]-dx/l*w))
    return L+R[::-1]
def wrap(cx,cy,a0,a1,r0=12.6,r1=14.4):
    # kurzes Bogenstueck der Sehne in der Rollennut (konvexes Viereck)
    A0,A1=math.radians(a0),math.radians(a1)
    return [(cx+r0*math.cos(A0),cy+r0*math.sin(A0)),(cx+r1*math.cos(A0),cy+r1*math.sin(A0)),(cx+r1*math.cos(A1),cy+r1*math.sin(A1)),(cx+r0*math.cos(A1),cy+r0*math.sin(A1))]
def spec():
    up=limb(-1);dn=limb(1)
    tipU=(266-0,154);tipD=(266,446)
    s=[
    Lb(P(limb(-1),E,-7,7,smooth=True),'Wurfarm'),
    Lb(P(limb(1),E,-7,7,smooth=True),'Wurfarm'),
    # Mittelstück: oben/unten volle Breite, in der Mitte seitlich ausgespartes Pfeilfenster mit Griff
    Lb(P([(352,196),(386,190),(396.3,284),(363.8,284)],I,-11,11,r=5),'Mittelstück'),
    Lb(P([(363.8,284),(396.3,284),(398,300),(396.3,316),(363.8,316),(366,300)],I,-17,-4.5,r=3,
      dec=[D(roundpoly(rect(370,288,22,26),5),E)]),'Griff'),
    P([(363.8,316),(396.3,316),(386,410),(352,404)],I,-11,11,r=5),
    Lb(P(circ(266,150,13,20),PK,-9,9,smooth=True,dec=[D(circ(266,150,4),K)]),'Umlenkrolle'),
    Lb(P(circ(266,450,13,20),PK,-9,9,smooth=True,dec=[D(circ(266,450,4),K)]),'Umlenkrolle'),
    # Sehne laeuft tangential an der Rueckseite der Rollen (x=253) und umschlingt die Rollen in der Nut
    Lb(P([(251.5,150),(254.5,150),(254.5,450),(251.5,450)],PK,-1.5,1.5,emit=True),'Sehne'),
    ]+[P(wrap(266,cy,a,a+15),PK,-1.5,1.5,emit=True) for cy in (150,450) for a in range(90,270,15)]+[
    Lb(P(rect(394,248,12,12),K,-6,6,r=2),'Visierschiene'),
    Sg(P(rect(404,250,30,8),K,-5,5,r=3)),
    # Pin-Ring quer zur Laufachse: Durchsicht nach vorn (−Y), bis 0.6 seitlich (Querfenster, claude-0.7 behoben)
    Sg(Lb(C(434,442,254,10,PK,n=18,emit=True,cap=[(254,0,4,K,False)]),'Visier')),
    C(255,520,300,3.5,E,n=12,cz=0),
    Lb(P(rect(366,303.5,26,5),K,-4.6,4,r=1.5),'Pfeilauflage'),
    F(520,548,300,8,1,PK,cz=0),
    P([(264,300),(292,289),(292,300)],PK,-0.8,0.8),
    P([(264,300),(292,311),(292,300)],PK,-0.8,0.8),
    P([(248,296),(264,296),(264,304),(248,304)],PK,-2.5,2.5,r=2),
    Lb(C(392,470,362,6,K,n=16),'Stabilisator'),
    C(470,494,362,12,I,n=16),
    ]
    return s
META=dict(num='10',name='Bogen',vname='Sichel',col='#FF5D8F',pill='INDIGO · ELFENBEIN · PINK',
 palette=[I,E,PK,K],center=(380,300,0),
 aria='Bogen Variante F: Compound-Bogen mit sichelförmigen elfenbeinfarbenen Wurfarmen, indigoblauem Mittelstück, pinken Umlenkrollen, leuchtender Sehne, Visier und Stabilisator',
 desc='Ein Compound-Bogen: sichelförmige Wurfarme mit pinken Umlenkrollen an den Spitzen, ein Visier und ein Stabilisator nach vorne. Indigo, Elfenbein und Pink.',
 form='Sichelförmige Wurfarme · Umlenkrollen an den Spitzen, Sehne läuft in der Rollennut · Mittelstück mit Pfeilfenster, Griff und Pfeilauflage · Visieraufnahme (Visier separat) · Stabilisator',
 desc3='Die Sichel als Konzeptblatt: Die beiden Wurfarme stecken oben und unten im Mittelstück und tragen an den Spitzen die Umlenkrollen, um deren Rückseite die Sehne in der Nut läuft. Der Pfeil liegt in der Sehnenebene im ausgesparten Pfeilfenster auf der Pfeilauflage, der Stabilisator zeigt nach vorne; das Visier ist ein separates Modul und separat gezeichnet.')
