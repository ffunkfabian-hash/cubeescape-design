"""KH14 „Schwenkbock“: einschüssiger Werkstatt-Kipplaufwerfer mit offenem Rohrschaft."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

AU, BR, DK, HL = '#624558', '#BA9860', '#291F2A', '#EBE1CF'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Luftiger Rohrschaft; die Reserve liegt in einem echten seitlichen Halter darunter.
    b.C(86,264,289,9,DK,n=12,L='Schaft')
    b.C(194,270,289,13,AU,n=12,L='Rohrschaft')
    b.C(188,208,289,17,BR,n=10,L='Schaftklemmring')
    b.P(rect(70,274,22,112),DK,-18,18,r=4,L='Schaftkappe',
        dec=[D(rect(76,288+18*i,10,6),AU) for i in range(5)])
    b.P(rect(110,270,111,12),HL,-13,13,r=3,L='Wangenauflage')
    b.P(rect(116,280,99,10),BR,-11,11,r=2,L='Wangenhalter')
    b.P([(120,282),(136,282),(136,316),(218,316),(218,333),(120,333)],BR,8,27,r=3,L='Granathalter',
        dec=bolts([(128,298),(205,324)]))
    b.C(137,196,319,11,HL,n=10,cz=35,L='Ersatzgranate')
    b.F(196,218,319,11,5,BR,n=10,cz=35,L='Ersatzgranate')
    # Kompakter Verschlussbock mit Ober-/Untermodul und zwei paarigen Klemmplatten.
    b.P([(258,248),(386,248),(414,268),(414,296),(258,296)],AU,-24,24,r=4,L='Gehäuse',
        dec=[D(roundpoly(rect(300,262,67,10),3),HL)])
    b.P([(258,299),(414,299),(414,336),(394,348),(258,348)],DK,-24,24,r=4,L='Untergehäuse')
    for x in (274,380):
        for z0,z1 in ((24,30),(-30,-24)):
            screws=bolts([(x+10,283),(x+10,325)])
            b.P(rect(x,275,20,58),BR,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    rail(b,302,374,248,DK,HL,w=10)
    b.P([(382,249),(388,232),(412,232),(422,243),(406,251)],BR,-7,7,r=2,L='Verriegelungshebel')
    # Die massive Schwenklasche unter dem Lauf führt zum Scharnier am Bock.
    b.P([(408,307),(452,307),(452,322),(430,342),(408,342)],AU,-18,18,r=3,L='Schwenklasche',
        dec=bolts([(439,316)]))
    b.P(circ(420,329,13,12),BR,-28,28,L='Scharnier',
        dec=[D(circ(420,329,5,10),DK)])
    b.C(412,692,288,31,AU,n=12,L='Kipplauf')
    # Zwei angeklemmte Bänder gliedern den langen Lauf; sichtbare Stirnöffnung an der Mündung.
    for x in (438,636):
        b.C(x,x+19,288,35,BR,n=10,L='Laufschelle')
    b.P(rect(478,266,130,8),HL,-27,27,r=2,L='Laufleiste',
        dec=[D(rect(492+28*i,268,12,4),DK) for i in range(4)])
    b.C(688,718,288,36,DK,n=12,L='Mündung',cap=[(288,0,26,BR,False),(288,0,22,DK,False)])
    b.P(rect(514,314,46,20),BR,-17,17,r=3,L='Vordergriffhalter',
        dec=bolts([(525,323),(550,323)]))
    b.P([(518,332),(555,332),(550,404),(525,404)],DK,-14,14,r=4,L='Vordergriff',
        dec=[D(rect(530,348+12*i,14,5),AU) for i in range(4)])
    grip(b,284,348,DK,AU,h=94,w=48,lean=13)
    b.P(rect(348,345,16,8),DK,-7,7,r=2,L='Abzugslager')
    trigger_group(b,348,348,BR,DK,grip_x0=323,depth=35)
    return b.m


META=dict(num='14',name='Spezial-Granatwerfer',nick='SCHWENKBOCK',col=BR,
 pill='AUBERGINE · MESSING · DUNKEL',palette=[AU,BR,DK,HL],center=(395,329,0),
 desc='Ein einschüssiger Werkstatt-Granatwerfer mit langem, auberginefarbenem Kipplauf und kurzem Verschlussbock. Messingplatten überbrücken die Gehäusefuge, eine kräftige Lasche verbindet den Lauf mit dem tiefen Scharnier; links unter dem offenen Rohrschaft hält ein verschraubter Träger die Ersatzgranate.',
 form='Rohrschaft mit Klemmring · geklemmter Verschlussbock · Verriegelungshebel oben · langer Kipplauf mit zwei Schellen · Schwenklasche und Scharnier · große Mündung · Ersatzgranate im linken Halter · Vordergriff',
 op=dict(reload_de='Verriegelungshebel öffnen, Kipplauf am tiefen Scharnier abkippen, Hülse auswerfen, eine Granate einsetzen und den Lauf verriegeln.',
         action_de='Ein Schuss pro Ladung; die Ersatzgranate sitzt links unter dem Rohrschaft und lässt sich aus ihrem offenen Halter ziehen.',
         fire_de='Eine Granate fliegt im Bogen; Aufprallzünder oder Fernzündung durch einen zweiten Druck auf den Abzug.',
         reload_en='Open the locking lever, tip the barrel down on its low hinge, eject the case, insert one grenade and lock the barrel shut.',
         action_en='One shot per load; the spare grenade sits in an open holder on the left beneath the tube stock.',
         fire_en='Lob one grenade; use its impact fuse or detonate remotely with a second trigger pull.'))
