from flib import *
from flabel import Lb
from hxlib import S
from eng import rect,circ,roundpoly
import math
EL,KO,DK,KH='#EFE7D6','#2447B8','#1A1C24','#7FA0FF'
def bolts(pts,c=DK,r=2.6):return [D(circ(x,y,r,10),c) for x,y in pts]
def strip(pts,w0,w1):
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
UP=[(382,192),(376,164),(360,132),(338,106),(316,86),(304,76)]
CX,CT,CB,CR=300,72,528,16   # Rollenmittelpunkte, Radius
def limb(sign):
    pts=[(x,300+sign*(y-300)) for x,y in UP]
    q=strip(pts,24,10)
    if sign>0:q=[[a,d,c,b] for a,b,c,d in q]
    return [Lb(P(p,KO,-11,11),'Wurfarm') for p in q]
def cam(cy):
    return [Lb(P(circ(CX,cy,CR,16),KO,-6,6,dec=[D(circ(CX,cy,9,12),'#3557D0'),D(circ(CX+5,cy-4,3,8),DK)]),'Umlenkrolle'),
            P(circ(CX,cy,5,10),DK,-13,13),            # Achse durch beide Gabelwangen
            P([(CX-4,cy),(CX+8,cy),(CX+14,cy+(20 if cy<300 else -20)),(CX+2,cy+(20 if cy<300 else -20))],'#1A2E78',-13,-8,r=2),  # Gabelwange
            P([(CX-4,cy),(CX+8,cy),(CX+14,cy+(20 if cy<300 else -20)),(CX+2,cy+(20 if cy<300 else -20))],'#1A2E78',8,13,r=2)]
def spec():
    s=[]
    s+=limb(-1)+limb(1)
    s+=cam(CT)+cam(CB)
    s+=[
    # Mittelstück (Elfenbein) mit Pfeilfenster: oben voll, Mitte nur Seitenwand, unten Griff
    Lb(P([(362,184),(402,190),(404,280),(364,280)],EL,-12,12,r=3,dec=bolts([(372,202),(394,202),(372,266),(394,266)])),'Mittelstück'),
    P(rect(364,280,40,40),EL,-14,-4,r=2),
    Lb(P([(364,320),(404,320),(402,414),(362,416)],DK,-12,12,r=3,dec=[D(roundpoly(rect(370,334+14*i,26,7),3),'#2C2F3A') for i in range(5)]),'Griff'),
    # Kobalt-Klemmplatten an den Wurfarmtaschen (verschraubt)
    P(rect(360,178,46,14),KO,-14,14,r=3,dec=bolts([(370,185),(396,185)],EL,2.2)),
    P(rect(360,408,46,14),KO,-14,14,r=3,dec=bolts([(370,415),(396,415)],EL,2.2)),
    # Sehne tangential an der Vorderseite beider Rollen
    Lb(P(rect(CX-CR-1.5,CT,3,CB-CT),KH,-1.5,1.5),'Sehne'),
    # Pfeilauflage und Pfeil (Nocke auf der Sehne)
    Lb(P(rect(366,303,30,5),KO,-4,3.5,r=1),'Pfeilauflage'),
    Lb(C(CX-CR+2,560,300,3,EL,n=8),'Pfeil'),
    F(560,586,300,7,1,KO),
    P(rect(CX-CR-4,296,10,8),DK,-3,3,r=2),
    P([(CX-CR+12,300),(CX-CR+36,291),(CX-CR+36,300)],KO,-0.8,0.8),
    P([(CX-CR+12,300),(CX-CR+36,309),(CX-CR+36,300)],KO,-0.8,0.8),
    # Visierhalter (bleibt) + Pin-Visier separat
    P(rect(404,226,30,8),DK,-4,4,r=2),
    S(Lb(P(rect(432,208,18,34),KO,-8,8,r=3,xdec=[('x+',450,roundpoly(rect(220,-3,8,6),2),KH,True)]),'Visier')),
    # Stabilisator
    Lb(C(404,488,372,6,DK,n=8),'Stabilisator'),
    C(488,510,372,11,KO,n=8),
    ]
    return s
META=dict(num='10',name='Bogen',vname='Spannwerk',col='#2447B8',pill='ELFENBEIN · KOBALT · DUNKEL',
 palette=[EL,KO,DK,KH],center=(400,300,0),
 aria='Bogen Variante H: Compoundbogen mit elfenbeinfarbenem, verschraubtem Mittelstück, kobaltblauen Wurfarmen, Umlenkrollen in Gabelwangen mit Achsen, tangential geführter Sehne, Pfeil auf der Pfeilauflage und Stabilisator; Pin-Visier separat',
 desc='Compoundbogen aus der Werkstatt-Serie: Das elfenbeinfarbene Mittelstück ist mit kobaltblauen Klemmplatten an den Wurfarmtaschen verschraubt. An den Spitzen laufen die Umlenkrollen auf Achsen in Gabelwangen, die Sehne läuft tangential an ihrer Vorderseite. Das Pin-Visier ist ein separates Modul für den Visierhalter.',
 form='Verschraubtes Mittelstück mit Pfeilfenster · Wurfarme mit Klemmplatten · Umlenkrollen auf Achsen · tangentiale Sehne · Pfeil auf Auflage · Stabilisator · Visier separat',
 desc3='Das Spannwerk als Konzeptblatt: Die kobaltblauen Wurfarme stecken in den Wurfarmtaschen und sind mit verschraubten Klemmplatten am elfenbeinfarbenen Mittelstück gesichert. An den Spitzen laufen die Umlenkrollen auf Achsen in Gabelwangen, die Sehne verläuft tangential an ihrer Vorderseite. Im Pfeilfenster liegt der Pfeil auf der Auflage, die Nocke sitzt auf der Sehne. Vorne der Visierhalter und der Stabilisator; das Pin-Visier wird separat montiert.')
