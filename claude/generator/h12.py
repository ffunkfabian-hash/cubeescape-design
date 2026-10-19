"""KH12 „Drehklaue“: geklemmter Werkstatt-Revolver mit tiefem Trommelrahmen."""
import math
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

TC, YE, DK, HL = '#A65B44', '#E0B838', '#302723', '#F0DECD'
AX, ORBIT = 299, 19


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Rückwärtiges Gehäuse: klarer Fugenspalt, beidseitige aufgeschraubte Laschen.
    b.P([(266,251),(318,251),(336,266),(336,301),(266,301)],TC,-23,23,r=4,L='Gehäuse')
    b.P([(266,304),(336,304),(336,347),(278,347),(266,336)],DK,-23,23,r=4,L='Untergehäuse')
    for z0,z1 in ((23,28),(-28,-23)):
        screws=bolts([(281,289),(281,321)])
        b.P(rect(271,280,20,49),YE,z0,z1,r=3,L='Gehäuseklemmplatte',
            dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    # Hohe Oberbrücke und tiefe Unterbrücke bilden einen offenen, klauenartigen Rahmen.
    b.P(rect(328,242,132,17),TC,-18,18,r=3,L='Oberbrücke',
        dec=bolts([(340,250),(448,250)]))
    b.P(rect(324,251,12,96),TC,-18,18,r=2,L='Rahmen')
    b.P(rect(332,334,107,13),TC,-16,16,r=3,L='Unterbrücke')
    b.P([(430,254),(454,254),(454,337),(430,337)],YE,-19,19,r=3,L='Rahmenpfosten',
        dec=bolts([(442,264),(442,326)]))
    rail(b,344,432,242,DK,HL,w=9)
    # Sechs echte Stirnkammern; die obere Kammer (280, 0) fluchtet mit dem Lauf.
    b.C(336,426,AX,32,HL,n=12,L='Trommel',
        cap=[(AX-ORBIT*math.cos(k*math.pi/3),ORBIT*math.sin(k*math.pi/3),7,DK,False) for k in range(6)])
    b.P(rect(345,291,70,8),TC,31,34,r=2,L='Trommel')
    b.P(rect(345,291,70,8),TC,-34,-31,r=2,L='Trommel')   # Rippen drehen mit der Trommel
    b.C(326,436,AX,5,DK,n=10,L='Trommelachse')
    b.P(rect(312,292,15,12),YE,23,31,r=2,L='Trommelriegel',
        dec=[D(circ(319,298,3,10),DK)])
    b.P([(282,252),(280,236),(294,224),(305,228),(300,250)],YE,-7,7,r=2,L='Hahn')
    # Kurzer, hoher Mantel; der lange freiliegende Ausstoßer liegt darunter.
    b.P([(452,258),(558,258),(578,274),(578,302),(452,302)],TC,-19,19,r=3,L='Laufmantel',
        dec=[D(roundpoly(rect(470+28*i,268,16,14),2),DK) for i in range(3)]+bolts([(464,290),(562,290)]))
    b.C(450,603,AX-ORBIT,10,DK,n=12,L='Lauf',cap=[(AX-ORBIT,0,6,DK,False)])
    b.C(576,600,AX-ORBIT,17,YE,n=8,L='Mündung',cap=[(AX-ORBIT,0,8,DK,False)])
    b.C(426,552,318,4,DK,n=10,L='Ausstoßerstange')
    b.P(rect(538,302,17,21),YE,-9,9,r=2,L='Ausstoßerhalter',
        dec=bolts([(546,312)]))
    grip(b,250,343,DK,TC,h=109,w=50,lean=19)
    b.P(rect(310,344,16,8),DK,-7,7,r=2,L='Abzugslager')
    trigger_group(b,310,347,YE,DK,grip_x0=289,depth=34)
    return b.m


META=dict(num='12',name='Handfeuerwaffe',nick='DREHKLAUE',col=YE,
 pill='TERRAKOTTA · SIGNALGELB · DUNKEL',palette=[TC,YE,DK,HL],center=(424,337,0),
 desc='Ein kompakter Werkstatt-Revolver mit hoher Oberbrücke und tiefem, klauenförmigem Trommelrahmen. Die helle Sechskammertrommel liegt zwischen den terrakottafarbenen Modulen; gelbe Klemmplatten und ein sichtbarer Ausstoßerhalter geben den Anbauteilen klare Befestigungen.',
 form='Geklemmtes Gehäuse · hoher Rahmen mit tiefer Unterbrücke · Sechskammertrommel mit Achse · Trommelriegel links · Hahn · kurzer Laufmantel · Ausstoßerstange mit Halter · Griff',
 op=dict(reload_de='Linken Trommelriegel drücken, Trommel ausschwenken, Hülsen mit der Ausstoßerstange auswerfen, sechs Patronen laden und einschwenken.',
         action_de='Double Action: Der Abzug spannt den Hahn und dreht die Trommel um eine Kammer; die obere Kammer fluchtet mit dem Lauf.',
         fire_de='Großkalibrige Einzelschüsse mit deutlichem Hochschlag; die langen Griffschalen bieten Platz für die zweite Hand.',
         reload_en='Press the left cylinder latch, swing out the cylinder, eject cases with the ejector rod, load six rounds and swing shut.',
         action_en='Double action: the trigger cocks the hammer and indexes the cylinder; the top chamber aligns with the barrel.',
         fire_en='Heavy single shots with strong muzzle rise; the long grip panels leave room for the support hand.'))
