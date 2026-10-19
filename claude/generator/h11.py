"""KH11 „Feinraster“: schlankes Werkstatt-Scoutgewehr mit geklemmter Laufbank."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

SG, BR, DK, HL = '#758B76', '#C0A16C', '#252E2B', '#E3E6D6'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Offener Teleskopschaft: dünnes Innenrohr, kräftigere Hülse und geklemmte Wangenauflage.
    b.C(80,258,278,8,DK,n=12,L='Schaft')
    b.C(176,264,278,12,SG,n=12,L='Rohrschaft')
    b.C(172,192,278,16,BR,n=12,L='Schaftklemmring')
    b.P(rect(64,264,22,105),DK,-17,17,r=4,L='Schaftkappe',
        dec=[D(rect(70,278+18*i,10,6),SG) for i in range(5)])
    b.P(rect(104,273,113,13),BR,-12,12,r=3,L='Wangenhalter',
        dec=bolts([(114,279),(206,279)]))
    b.P([(100,252),(198,252),(222,261),(222,275),(100,275)],HL,-17,17,r=4,L='Wangenauflage')
    # Hoher hinterer Verschlussblock und flache vordere Laufbank statt G-Keilgehäuse.
    b.P([(252,246),(456,246),(498,268),(498,293),(252,293)],SG,-23,23,r=4,L='Gehäuse',
        dec=[D(roundpoly(rect(300,256,100,8),3),HL)])
    b.P([(252,296),(498,296),(498,328),(478,338),(252,338)],DK,-23,23,r=3,L='Untergehäuse')
    for x in (272,456):
        for z0,z1 in ((23,28),(-28,-23)):
            screws=bolts([(x+10,279),(x+10,315)])
            b.P(rect(x,271,20,52),BR,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),
                xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    rail(b,302,438,246,DK,HL,w=10)
    b.P(rect(330,271,76,14),HL,23,29,r=2,L='Verschluss',
        dec=[D(rect(338,275,52,5),DK)])
    b.P(rect(378,275,16,9),BR,29,46,r=2,L='Ladehebel')
    # Der schmale Handschutz sitzt tiefer; zwei sichtbare Bügel halten die Laufbank.
    b.P([(496,284),(644,284),(660,296),(660,320),(496,328)],SG,-16,16,r=3,L='Handschutz',
        dec=[D(roundpoly(rect(514+28*i,294,17,16),3),DK) for i in range(5)])
    for x in (506,620):
        b.P(rect(x,276,18,52),BR,-20,20,r=3,L='Laufhalter',
            dec=bolts([(x+9,284),(x+9,319)]))
    b.C(498,778,294,7,DK,n=12,L='Lauf')
    b.C(774,820,294,13,BR,n=8,L='Mündungsbremse',cap=[(294,0,6,DK,False)])
    b.P(rect(784,285,22,5),DK,-13,13,r=1,L='Bremsenschlitz')
    grip(b,270,338,DK,SG,h=94,w=48,lean=12)
    b.P(rect(334,335,16,8),DK,-7,7,r=2,L='Abzugslager')
    trigger_group(b,334,338,BR,DK,grip_x0=310,depth=34)
    b.P(rect(428,327,62,16),BR,-16,16,r=3,L='Magazinhalter',
        dec=bolts([(438,335),(480,335)]))
    b.P([(436,341),(480,341),(478,394),(430,394)],SG,-13,13,r=3,L='Magazin',
        dec=[D(roundpoly(rect(442,351,26,31),2),DK)]+
            [D(rect(447,356+8*i,16,3),HL) for i in range(3)])
    b.P(rect(426,390,57,11),BR,-15,15,r=2,L='Magazinboden')
    return b.m


META=dict(num='11',name='Scout-Gewehr',nick='FEINRASTER',col=BR,
 pill='SALBEI · MESSING · DUNKEL',palette=[SG,BR,DK,HL],center=(442,321,0),
 desc='Ein halbautomatisches Werkstatt-Scoutgewehr mit hohem Verschlussblock, flacher Laufbank und langem freiem Lauf. Messingplatten klemmen die salbeifarbenen Gehäusemodule über der Fuge; der offene Rohrschaft trägt eine helle Wangenauflage, das kurze Patronenmagazin sitzt vor dem Abzug.',
 form='Teleskop-Rohrschaft mit Klemmring · Wangenauflage auf Halter · Ober- und Untergehäuse mit Klemmplatten · Verschluss und Ladehebel links · kurzes Kastenmagazin · Handschutz mit zwei Laufhaltern · langer Lauf mit Mündungsbremse',
 op=dict(reload_de='Kurzes Kastenmagazin vor dem Abzug wechseln und den linken Ladehebel einmal zurückziehen; Kapazität acht Patronen.',
         action_de='Der Verschluss läuft halbautomatisch im hohen Obergehäuse; die Klemmplatten fixieren Ober- und Untermodul.',
         fire_de='Präzises Einzelfeuer auf mittlere und weite Distanz; die Wangenauflage stabilisiert den Anschlag.',
         reload_en='Replace the short box magazine ahead of the trigger and pull the left charging handle once; capacity is eight rounds.',
         action_en='The bolt cycles semi-automatically inside the tall upper receiver; clamp plates secure the upper and lower modules.',
         fire_en='Precise single shots at medium and long range; the cheek rest steadies the shoulder position.'))
