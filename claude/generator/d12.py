"""KD12 „Funkenschlag“: kompakter Sechskammerrevolver mit massigem D-Rahmen."""
import math
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#FF914A', '#FFE0BA'
AX, RING = 290, 20


def model():
    b = B(); D = b.D
    b.P([(236,320),(290,320),(316,430),(254,440),(230,414)],K,-24,24,r=12,L='Griff',
        dec=[D(roundpoly([(252,342),(276,342),(294,410),(266,416)],9),P),
             D(roundpoly([(262,352),(269,352),(282,400),(275,402)],4),A,True)])
    b.P([(224,266),(248,248),(300,248),(300,326),(240,332),(224,310)],
        DK,-25,25,r=12,L='Rahmen',
        dec=[D(roundpoly(rect(240,268,42,30),9),P)])
    # Ober- und Unterbrücke lassen zwischen den Pfosten ein echtes Trommelfenster.
    b.P(rect(280,240,124,20),DK,-23,23,r=8,L='Oberbrücke',
        dec=[D(roundpoly(rect(302,244,82,10),5),P)])
    b.P(rect(290,320,104,14),DK,-20,20,r=6,L='Rahmen')
    b.P(rect(374,252,28,80),DK,-25,25,r=10,L='Rahmen',
        dec=[D(roundpoly(rect(384,280,10,30),5),A,True)])
    # k=0 ist exakt die obere Kammer bei (y=270,z=0), wie die Laufachse.
    b.C(300,374,AX,32,DK,n=16,L='Trommel',
        cap=[(AX,0,29,P,False)]+
            [(AX-RING*math.cos(k*math.pi/3),RING*math.sin(k*math.pi/3),6,'#050506',False)
             for k in range(6)]+[(AX,0,7,K,False)])
    for x in (308,356):
        b.C(x,x+7,AX,33,K,n=16,L='Trommel')
    b.P(rect(264,302,20,10),A,24,34,r=4,L='Trommelriegel')
    b.P([(244,250),(254,226),(268,228),(280,252),(266,260)],A,-8,8,r=5,L='Hahn')
    rail(b,294,396,240,K,DK,w=12)
    b.P([(398,242),(496,242),(518,258),(518,296),(398,302)],DK,-26,26,r=12,L='Laufmantel',
        dec=[D(roundpoly(rect(412,252,84,24),9),P),
             D(roundpoly(rect(414,283,76,7),3),A,True),
             D(roundpoly(rect(426,260,48,6),3),K)])
    b.C(516,540,AX-RING,14,K,n=12,L='Lauf',
        cap=[(AX-RING,0,10,P,False),(AX-RING,0,7,'#050506',False)])
    b.C(374,474,314,5,K,n=12,L='Ausstoßerstange')
    b.P(rect(466,296,16,22),DK,-8,8,r=6,L='Ausstoßerstange')
    b.P(arcband(300,396,332,66,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(322,333),(336,333),(348,375),(334,379)],A,-6,6,r=4,L='Abzug')
    return b.m


META=dict(num='12',name='Handfeuerwaffe',nick='FUNKENSCHLAG',col=A,
 pill='SOLAR-VERSION',palette=[P,DK,A,AL],center=(382,332,0),
 desc='Ein kompakter, tief gerundeter Rahmen umschließt die schwere Trommel mit sechs Kammern. Der kurze breite Laufmantel liegt auf der oberen Kammerachse; helle Deckplatten und ein orange leuchtender Streifen gliedern die dunkle Masse.',
 form='Kompakter Rahmen mit Oberbrücke · Trommel mit sechs Kammern · Trommelriegel links · freier Hahn · kurzer breiter Laufmantel · obere Kammerachse · Ausstoßerstange · tiefer Griff mit hellen Griffschalen · gebogener Bügel',
 op=dict(reload_de='Trommelriegel links drücken, Trommel nach links ausschwenken, sechs Patronen laden und Trommel wieder einschwenken.',
         action_de='Double Action: Jeder Abzug spannt den Hahn und dreht die Trommel um eine Kammer weiter.',
         fire_de='Ein großkalibriger Schuss je Abzug mit kräftigem Hochschlag; die obere Trommelkammer fluchtet mit dem Lauf.',
         reload_en='Press the left cylinder latch, swing the cylinder out to the left, load six rounds and swing it closed.',
         action_en='Double action: each trigger pull cocks the hammer and indexes the cylinder by one chamber.',
         fire_en='One heavy shot per trigger pull with strong muzzle rise; the upper cylinder chamber lines up with the barrel.'))
