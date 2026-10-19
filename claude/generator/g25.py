"""KG25 Streuschuss-Handfeuerwaffe „Breitseite“ (claude-0.10.1): Kipprahmen-Revolver mit Schrotladungen (Destiny: Hand Cannon,
Spread Shot Frame, „The Edge of Fate“ 2025). Unterschied zur Handfeuerwaffe (KG12): kurze dicke Trommel mit fünf Schrotkammern statt sechs
Patronen, kurzer Lauf mit breiter, flacher Streumündung, Kipprahmen mit Scharnier vorne unten statt seitlich ausschwenkender Trommel,
verkleideter Hahn."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly,circ
import math
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
AXC=284          # Trommelachse (y)
BX=AXC-17        # Laufachse = obere Kammer der Trommel
def model():
    b=B();D=b.D
    # fester Rahmen mit Griff, Hahnschutz und Scharnier vorne unten
    grip(b,232,306,AN,DK,h=110,w=52,lean=24)
    b.P([(216,270),(252,258),(298,258),(298,316),(394,316),(394,332),(252,334),(222,314)],CR,-17,17,r=5,L='Rahmen')
    b.P([(236,250),(278,244),(290,258),(244,270)],AN,-10,10,r=3,L='Hahnschutz')
    b.P(circ(388,320,9,12),AN,-20,20,L='Scharnier')
    # Kipprahmen: Oberbrücke und Joch vor der Trommel, kippt am Scharnier nach unten; Kippriegel hinten oben
    b.P([(290,236),(400,236),(400,312),(378,312),(378,252),(290,252)],CR,-15,15,r=4,L='Kipprahmen',
        dec=[D(roundpoly(rect(384,262,10,40),2),AN)])
    b.P([(276,240),(292,232),(304,246),(288,254)],OR,-6,6,r=2,L='Kippriegel')
    rail(b,296,394,236,AN,DK,w=9)
    # Trommel: kurz und dick, fünf Schrotkammern (orange Hülsenränder), Achsstift bis ins Joch
    b.C(300,372,AXC,30,AN,n=10,L='Trommel',
        cap=[(AXC-17*math.cos(2*k*math.pi/5),17*math.sin(2*k*math.pi/5),8.5,OR,False) for k in range(5)]
           +[(AXC-17*math.cos(2*k*math.pi/5),17*math.sin(2*k*math.pi/5),4.5,'#050506',False) for k in range(5)])
    b.C(296,384,AXC,5,DK,n=8)
    b.P(rect(306,AXC-4,60,8),DK,-31,31)                                  # Kammerrillen links und rechts
    # kurzer Lauf mit Laufschiene, breite flache Streumündung mit Schlitz
    b.C(400,470,BX,14,DK,n=10,L='Lauf')
    b.P(rect(400,BX-20,70,8),AN,-6,6,r=2,dec=[D(rect(410+14*i,BX-18,6,4),OR) for i in range(4)])
    # Streumündung im Grundriss gefächert (breit nach links und rechts, flach in der Höhe), Querschlitz vorne
    b.Y([(468,-16),(504,-30),(514,-30),(514,30),(504,30),(468,16)],CR,BX-15,BX+15,r=3,L='Streumündung',
        dec=[b.D([(476,-2+zz*0.2),(508,-2+zz*1.6),(508,2+zz*1.6),(476,2+zz*0.2)],AN) for zz in (-14,0,14)])
    M=b.m.parts[-1]['dec']
    M.append(('x+',514,roundpoly(rect(BX-7,-22,14,44),5),'#050506',False))
    for zz in (-13,0,13):M.append(('x+',514.5,circ(BX,zz,2.4,8),OR,True))
    trigger_group(b,302,330,OR,AN,grip_x0=272,depth=34)
    return b.m
META=dict(num='25',name='Streuschuss-Handfeuerwaffe',nick='BREITSEITE',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(358,300,0),
 desc='Kipprahmen-Revolver für Schrotladungen: Eine kurze, dicke Trommel zeigt vorne fünf Schrotkammern mit orangen Hülsenrändern. Der cremefarbene Kipprahmen mit Oberbrücke und Joch kippt am Scharnier vorne unten ab, der kurze Lauf endet in einer breiten, flachen Streumündung mit Querschlitz.',
 form='Rahmen mit verkleidetem Hahn · Kipprahmen mit Oberbrücke und Joch · Kippriegel · kurze dicke Trommel mit fünf Schrotkammern · Scharnier vorne unten · kurzer Lauf mit Laufschiene · breite flache Streumündung · Griff',
 op=dict(reload_de='Kippriegel hinten oben drücken, Kipprahmen mit Lauf und Trommel am Scharnier nach unten kippen, der Sternauswerfer hebt die fünf Hülsen, neue Schrotpatronen einsetzen, zuklappen',
         action_de='Double Action: der verdeckte Hahn spannt bei jedem Abzug und dreht die Trommel um eine der fünf Kammern weiter',
         fire_de='kurzer Streuschuss aus Schrotkugeln, flach gefächert durch die Streumündung; langsame Feuerrate, wirksam auf kurze Distanz',
         reload_en='press the rear top latch, tip the frame with barrel and cylinder down on the front hinge, the star extractor lifts five shells, insert new shot shells, close',
         action_en='double action: the shrouded hammer cocks with every trigger pull and indexes the five-chamber cylinder',
         fire_en='short spread of pellets fanned flat by the spread muzzle; slow rate of fire, effective at close range'))
