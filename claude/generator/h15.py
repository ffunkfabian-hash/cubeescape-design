"""KH15 „Walzenblock“: schwerer Werkstattwerfer mit freier Sechskammertrommel und geteilter Frontgabel."""
import math
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

PT, OC, DK, HL = '#245E64', '#C59842', '#162E34', '#DAE4CF'
AX, ORBIT = 306, 40


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    b.C(78,246,279,10,DK,n=12,L='Schaft')
    b.C(174,250,279,14,PT,n=12,L='Rohrschaft')
    b.C(166,186,279,18,OC,n=10,L='Schaftklemmring')
    b.P(rect(62,266,22,118),DK,-20,20,r=4,L='Schaftkappe',
        dec=[D(rect(68,280+19*i,10,6),PT) for i in range(5)])
    b.P(rect(100,256,108,14),HL,-15,15,r=3,L='Wangenauflage')
    b.P(rect(108,269,94,11),OC,-13,13,r=2,L='Wangenhalter')
    # Der hohe Heckblock endet vor der Trommel; der Abzugsraum bleibt hinter ihr frei.
    b.P([(238,232),(376,232),(400,250),(400,281),(238,281)],PT,-28,28,r=4,L='Gehäuse',
        dec=[D(roundpoly(rect(270,246,84,9),3),HL)])
    b.P([(238,284),(400,284),(400,344),(382,360),(238,360)],DK,-28,28,r=4,L='Untergehäuse')
    for x in (254,366):
        for z0,z1 in ((28,34),(-34,-28)):
            screws=bolts([(x+10,269),(x+10,306)])
            b.P(rect(x,260,20,54),OC,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    b.P(rect(302,304,56,41),OC,28,36,r=3,L='Ladeklappe',
        dec=[D(roundpoly(rect(312,314,36,20),3),PT)]+bolts([(310,312),(350,337)]))
    b.P(rect(298,304,8,41),HL,29,38,r=2,L='Ladeklappenscharnier')
    # Heller Trommelkörper mit sechs frontalen Kammern und außenliegenden Laufringen.
    b.C(400,536,AX,65,HL,n=12,L='Granattrommel',
        cap=[(AX-ORBIT*math.cos(k*math.pi/3),ORBIT*math.sin(k*math.pi/3),14,DK,False) for k in range(6)])
    for x in (422,506):
        b.C(x,x+10,AX,66,PT,n=12,L='Trommellaufring')
    b.C(382,566,AX,8,DK,n=10,L='Trommelachse')
    b.P(rect(388,218,170,20),PT,-18,18,r=3,L='Oberbrücke',
        dec=bolts([(402,230),(544,230)]))
    rail(b,408,534,218,DK,HL,w=10)
    # Keine volle Frontplatte: beide Gabelwangen tragen Laufaufnahme und Achslager.
    b.P(rect(538,234,20,17),PT,-31,31,r=2,L='Laufträgerquersteg')
    for z0,z1 in ((25,31),(-31,-25)):
        screws=bolts([(548,251),(548,310)])
        b.P(rect(538,240,20,83),OC,z0,z1,r=3,L='Laufträger',
            dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    b.C(536,566,AX,13,PT,n=10,L='Achslager')
    b.P(rect(538,316,20,12),OC,-31,31,r=2,L='Laufträgerquersteg')
    b.C(536,570,AX-ORBIT,28,PT,n=12,L='Laufaufnahme')
    b.C(564,766,AX-ORBIT,23,PT,n=12,L='Lauf')
    b.C(598,618,AX-ORBIT,27,OC,n=10,L='Laufschelle')
    b.P(rect(630,246,107,8),HL,-19,19,r=2,L='Laufleiste',
        dec=[D(rect(642+25*i,248,12,4),DK) for i in range(4)])
    b.C(760,796,AX-ORBIT,31,OC,n=12,L='Mündung',cap=[(AX-ORBIT,0,22,DK,False)])
    b.P(rect(564,286,78,22),OC,-17,17,r=3,L='Vordergriffhalter',
        dec=bolts([(578,298),(628,298)]))
    b.P([(586,305),(624,305),(618,391),(593,391)],DK,-15,15,r=4,L='Vordergriff',
        dec=[D(rect(598,324+12*i,14,5),PT) for i in range(5)])
    grip(b,252,360,DK,PT,h=94,w=49,lean=14)
    b.P(rect(318,357,16,8),DK,-7,7,r=2,L='Abzugslager')
    trigger_group(b,318,360,OC,DK,grip_x0=292,depth=33)
    return b.m


META=dict(num='15',name='Schwerer Granatwerfer',nick='WALZENBLOCK',col=OC,
 pill='DUNKELPETROL · OCKER · HELL',palette=[PT,OC,DK,HL],center=(429,336,0),
 desc='Ein schwerer Werkstatt-Granatwerfer mit großer heller Drehtrommel, hohem Heckblock und langem Rohrschaft. Ockerfarbene Klemmplatten halten die petrolfarbenen Module zusammen; eine geteilte Frontgabel trägt Trommelachse und Laufaufnahme, sodass die sechs Kammern an der Stirnseite erkennbar bleiben.',
 form='Rohrschaft mit Klemmring · Heckgehäuse mit Klemmplatten · Ladeklappe links · Sechskammer-Granattrommel mit Laufringen · Trommelachse · Oberbrücke mit Schiene · paarige Laufträger · Lauf auf oberer Kammerachse · Vordergriff',
 op=dict(reload_de='Ladeklappe links öffnen, die Trommel kammerweise weiterdrehen, sechs Granaten einsetzen und die Klappe schließen.',
         action_de='Das Federwerk in der Trommelachse dreht nach jedem Schuss um eine Kammer; die obere Kammer fluchtet mit dem Lauf.',
         fire_de='Sechs schwere Granaten nacheinander mit Aufprallzünder; der Vordergriff stützt den langen Lauf.',
         reload_en='Open the left loading gate, index the drum chamber by chamber, insert six grenades and close the gate.',
         action_en='A spring mechanism in the drum axle indexes one chamber after each shot; the top chamber aligns with the barrel.',
         fire_en='Fire six heavy impact-fused grenades in succession; the foregrip supports the long barrel.'))
