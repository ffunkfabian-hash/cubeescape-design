from flib import *
from flabel import Lb
from gsight import S
from eng import rect,circ,roundpoly
import math
W,K,OR,CY,GR='#F2F2EE','#1C1D21','#FF8A2A','#6FE3EE','#4A4E57'
def strip(pts,w0,w1):
    """Facettierte Bandkette mit Gehrungsfugen: aneinanderstoßende konvexe Vierecke ohne Überlappung."""
    n=len(pts);L=[];R=[]
    for i,p in enumerate(pts):
        w=(w0+(w1-w0)*i/(n-1))/2
        a=pts[max(i-1,0)];b=pts[min(i+1,n-1)]
        if 0<i<n-1:
            d1=(p[0]-a[0],p[1]-a[1]);d2=(b[0]-p[0],b[1]-p[1])
            l1=math.hypot(*d1);l2=math.hypot(*d2)
            n1=(-d1[1]/l1,d1[0]/l1);n2=(-d2[1]/l2,d2[0]/l2)
            nm=(n1[0]+n2[0],n1[1]+n2[1]);lm=math.hypot(*nm);nm=(nm[0]/lm,nm[1]/lm)
            k=w/max(0.3,nm[0]*n1[0]+nm[1]*n1[1])
        else:
            d=(b[0]-a[0],b[1]-a[1]);l=math.hypot(*d);nm=(-d[1]/l,d[0]/l);k=w
        L.append((p[0]+nm[0]*k,p[1]+nm[1]*k));R.append((p[0]-nm[0]*k,p[1]-nm[1]*k))
    return [[L[i],L[i+1],R[i+1],R[i]] for i in range(n-1)]
UP=[(382,194),(374,160),(354,124),(330,96),(312,78),(306,66),(312,54)]
def limb(sign):
    pts=[(x,300+sign*(y-300)) for x,y in UP]
    q=strip(pts,22,8)
    if sign>0:q=[[a,d,c,b] for a,b,c,d in q]  # Umlaufsinn
    return [Lb(P(p,W,-12,12),'Wurfarm') for p in q]
def spec():
    s=[]
    s+=limb(-1)+limb(1)
    s+=[
    # Mittelstück: oben und unten volle Breite, dazwischen Pfeilfenster mit seitlicher Wand
    Lb(P([(364,186),(400,192),(402,242),(366,242)],K,-12,12,r=3),'Mittelstück'),
    Lb(P(rect(366,242,36,62),K,-14,-4,r=2),'Mittelstück'),
    Lb(P([(366,304),(402,304),(400,412),(364,414)],K,-12,12,r=3,
      dec=[D(roundpoly(rect(372,318+14*i,24,8),3),GR) for i in range(5)]),'Griff'),
    # Wurfarmtaschen
    P(rect(362,180,40,12),GR,-14,14,r=3),
    P(rect(362,408,40,12),GR,-14,14,r=3),
    # Sehnenhalter an den Spitzen, Sehne
    P(circ(312,54,7,8),OR,-13,13),
    P(circ(312,546,7,8),OR,-13,13),
    Lb(P(rect(302.5,66,3,468),CY,-1.5,1.5),'Sehne'),
    # Pfeilauflage im Fenster, Pfeil
    Lb(P(rect(366,303,30,5),OR,-4,3.5,r=1),'Pfeilauflage'),
    Lb(C(300,544,300,3,W,n=8),'Pfeil'),
    F(544,570,300,7,1,OR),
    P([(312,300),(336,291),(336,300)],OR,-0.8,0.8),
    P([(312,300),(336,309),(336,300)],OR,-0.8,0.8),
    P(rect(298,296,10,8),K,-3,3,r=2),
    # Visier auf Montagearm, Stabilisator
    P(rect(400,216,8,18),K,-6,6,r=2),  # Visieraufnahme am Mittelstück (bleibt)
    S(P(rect(408,222,22,8),K,-4,4,r=2)),
    S(Lb(P(rect(428,206,16,32),GR,-8,8,r=3,xdec=[('x+',444,roundpoly(rect(218,-3,8,6),2),CY,True)]),'Visier')),
    C(400,486,372,6,K,n=8),
    C(486,506,372,11,GR,n=8),
    ]
    return s
META=dict(num='10',name='Bogen',vname='Kante',col='#FF8A2A',pill='WEISS · SCHWARZ · ORANGE',
 palette=[W,K,OR,CY],center=(400,300,0),
 aria='Bogen Variante G: Recurvebogen mit facettierten weißen Wurfarmen, schwarzem Mittelstück mit Pfeilfenster, oranger Pfeilauflage, cyanfarbener Sehne, Visier und kurzem Stabilisator',
 desc='Ein Recurvebogen aus kantigen Facetten: Die weißen Wurfarme knicken in Segmenten nach hinten und biegen an den Spitzen wieder nach vorn. Das schwarze Mittelstück hat ein Pfeilfenster mit oranger Auflage.',
 form='Facettierte Recurve-Wurfarme · Mittelstück mit Pfeilfenster · Pfeilauflage · Sehne an orangen Haltern · Visier auf Arm · kurzer Stabilisator',
 desc3='Die Kante als Konzeptblatt: Die facettierten Wurfarme stecken oben und unten in den Wurfarmtaschen des Mittelstücks und tragen an den Recurve-Spitzen die orangen Sehnenhalter. Im Pfeilfenster liegt der Pfeil mittig auf der orangen Pfeilauflage, die Nocke sitzt auf der Sehne. Vorne stehen das Visier auf seinem Arm und der kurze Stabilisator.')
