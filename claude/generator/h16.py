"""KH16 „Gurtwerk“: Werkstatt-MG mit Rohrschaft, geklemmten Modulen und linker Gurtzuführung."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

PL, CU, DK, HL = '#51475F', '#D99468', '#20212A', '#E3E0D6'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Rohrschaft mit Klemmring und separater Wangenauflage, alle Teile verbunden.
    b.C(74,254,294,10,DK,n=12,L='Rohrschaft')
    b.P(rect(62,260,20,116),DK,-20,20,r=4,L='Schaftkappe',
        dec=[D(rect(67,274+18*i,10,6),PL) for i in range(5)])
    b.P(rect(98,274,106,14),CU,-14,14,r=3,L='Wangenhalter',dec=bolts([(108,281),(194,281)]))
    b.P([(96,252),(186,252),(214,262),(214,276),(96,276)],HL,-18,18,r=4,L='Wangenauflage')
    b.C(222,246,294,17,CU,n=12,L='Schaftklemmring')
    # Ober- und Untergehäuse mit Fuge und Klemmplatten. „Gehäuse“ hält den Visierbezug unabhängig vom linken Kasten.
    b.P([(244,248),(506,248),(534,264),(534,292),(244,292)],PL,-27,27,r=4,L='Gehäuse',
        dec=[D(roundpoly(rect(316,256,104,8),3),HL)])
    b.P([(244,295),(534,295),(534,330),(508,340),(244,340)],DK,-27,27,r=4,L='Untergehäuse')
    for x in (264,494):
        for z0,z1 in ((27,32),(-32,-27)):
            screws=bolts([(x+11,280),(x+11,311)])
            b.P(rect(x,272,22,47),CU,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),
                xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    # Hinteres Deckelscharnier; die Schiene sitzt ohne Luftspalt im Zuführdeckel.
    b.P(circ(302,244,7,12),CU,-31,31,L='Deckelscharnier')
    b.P([(300,232),(468,232),(490,244),(490,252),(300,252)],PL,-28,28,r=3,L='Zuführdeckel',
        dec=bolts([(316,242),(468,242)]))
    rail(b,326,454,234,DK,HL,w=12)
    # Linker Schieber und Ladehebel; die übrigen Gehäusemodule bleiben symmetrisch.
    b.P(rect(342,272,66,16),HL,27,33,r=3,L='Verschluss')
    b.P(rect(366,276,18,10),CU,33,50,r=2,L='Ladehebel')
    # Der Kasten bleibt vollständig vor Griff und Abzug; Gurt reicht bis unter den Deckel.
    b.P(rect(408,304,102,18),CU,27,44,r=3,L='Kastenhalter',
        dec=bolts([(418,313),(500,313)]))
    b.P([(422,312),(510,312),(520,326),(520,408),(422,408)],PL,34,92,r=5,L='Munitionskasten',
        dec=[D(roundpoly(rect(424,334,80,52),4),DK),D(rect(432,344,64,8),CU),
             D(rect(432,368,42,6),HL)]+bolts([(432,322),(506,397)]))
    b.P([(430,246),(480,246),(494,270),(494,316),(432,316),(432,276)],CU,27,46,r=2,L='Patronengurt',
        dec=[D(rect(438+9*i,254,4,20),DK) for i in range(5)]+
            [D(rect(440+9*i,280,4,28),DK) for i in range(5)])
    # Angesetzter gelochter Laufmantel, kräftige Schellen und Laufwechselgriff.
    b.P([(532,258),(738,258),(756,274),(756,318),(740,334),(532,334)],PL,-21,21,r=4,L='Laufmantel',
        dec=[D(roundpoly(rect(554+29*i,277,17,26),3),DK) for i in range(6)])
    for x in (532,690):
        b.C(x,x+20,296,39,CU,n=8,L='Laufmantelschelle')
    for x in (556,630):
        b.P(rect(x,230,12,32),CU,-8,8,r=2,L='Tragegriffhalter',
            dec=bolts([(x+6,252)]))
    b.P(rect(548,216,102,18),DK,-11,11,r=5,L='Tragegriff',
        dec=[D(roundpoly(rect(560,221,78,7),3),HL)])
    b.C(750,836,296,10,DK,n=12,L='Lauf')
    b.C(828,872,296,17,CU,n=8,L='Feuerdämpfer',cap=[(296,0,10,DK,False)])
    # Eingeklapptes Zweibein mit gemeinsamem Halter und je einem beschrifteten Bein.
    b.P(rect(694,330,18,32),DK,-27,27,r=3,L='Zweibeinhalter')
    for z in (-20,20):
        b.C(704,796,354,4,HL,n=8,cz=z,L='Zweibein')
        b.P(rect(784,350,18,18),DK,z-7,z+7,r=2,L='Zweibeinfuß')
    grip(b,278,338,DK,PL,h=98,w=50,lean=14)
    trigger_group(b,342,338,CU,DK,grip_x0=320,depth=36)
    b.P([(574,332),(610,332),(604,402),(580,402)],DK,-15,15,r=5,L='Vordergriff',
        dec=[D(rect(585,350+12*i,14,5),PL) for i in range(4)])
    return b.m


META=dict(num='16',name='Maschinengewehr',nick='GURTWERK',col=CU,
 pill='PFLAUMENGRAU · KUPFER · DUNKEL',palette=[PL,CU,DK,HL],center=(467,326,0),
 desc='Ein verschraubtes Werkstatt-Maschinengewehr mit offenem Rohrschaft und kupferfarbenen Klemmplatten über der Gehäusefuge. Links führt der Patronengurt vom angesetzten Kasten unter den Zuführdeckel; der lange Laufmantel trägt zwei Schellen, einen Laufwechselgriff und das eingeklappte Zweibein.',
 form='Rohrschaft mit Klemmring · Ober- und Untergehäuse mit verschraubten Klemmplatten · Zuführdeckel mit Schiene · Munitionskasten und Patronengurt links · Laufmantel mit Schellen · Tragegriff · Ladehebel · zwei Zweibeinbeine · Vordergriff',
 op=dict(reload_de='Zuführdeckel aufklappen, Kasten links wechseln, Gurt einlegen, Deckel schließen und Ladehebel zurückziehen.',
         action_de='Der Verschluss läuft im Obergehäuse; die Gurtzuführung zieht mit jedem Schuss eine Patrone aus dem linken Kasten nach.',
         fire_de='Dauerfeuer mit steigender Feuerrate beim Halten; der Tragegriff dient dem Laufwechsel.',
         reload_en='Open the feed cover, replace the left ammo box, lay in the belt, close the cover and pull the charging handle.',
         action_en='The bolt travels inside the upper receiver; each shot advances one cartridge from the left ammo box.',
         fire_en='Sustained automatic fire with a rising rate while held; the carry handle serves barrel changes.'))
