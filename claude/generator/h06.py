from flib import *
from flabel import Lb
from hxlib import S
from eng import rect,circ,roundpoly
BO,MS,DK,EL='#7A1F2B','#C9A24A','#231C1E','#E9DFCF'
def bolts(pts,c=DK,r=3.2):return [D(circ(x,y,r,10),c) for x,y in pts]
def spec():
    return [
    # Teleskopschaft: Rohr, Messing-Klemmring, Schaftkappe
    C(96,188,250,9,DK,n=12),
    P(rect(146,238,16,24),MS,-12,12,r=3,dec=bolts([(154,250)],DK,2.6)),
    Lb(P([(68,232),(98,232),(98,318),(74,312)],BO,-20,20,r=5,dec=[D(roundpoly(rect(76,250,14,48),3),DK)]),'Schaft'),
    # oberes Gehäusemodul (Bordeaux)
    Lb(P([(200,230),(470,230),(490,246),(490,290),(200,290),(186,276),(186,244)],BO,-24,24,r=6,
      dec=[D(roundpoly(rect(236,246,96,22),4),DK),D(roundpoly(rect(246,252,60,8),2),MS,True)]+bolts([(206,252),(206,274),(476,256),(476,278)])),'Gehäuse'),
    # unteres Gehäusemodul (dunkel) mit Magazinschacht
    P([(214,290),(444,290),(444,316),(424,326),(214,326)],DK,-20,20,r=4),
    # Messing-Klemmplatten über der Modulfuge
    P(rect(240,282,26,20),MS,-27,27,r=3,dec=bolts([(247,288),(259,296)],DK,2.4)),
    P(rect(404,282,26,20),MS,-27,27,r=3,dec=bolts([(411,288),(423,296)],DK,2.4)),
    # Montageschiene (bleibt an der Waffe)
    Lb(P(rect(222,220,230,11),DK,-10,10,r=2,dec=[D(rect(x,222,8,4),'#3A3034') for x in range(230,446,16)]),'Visierschiene'),
    # Visier separat: Klemmfuß + Reflexvisier
    S(P(rect(330,206,48,15),DK,-11,11,r=3,dec=bolts([(340,213),(368,213)],MS,2.4))),
    S(Lb(P([(326,176),(382,176),(390,206),(320,206)],BO,-13,13,r=5,
      xdec=[('x+',390,roundpoly(rect(182,-8,18,16),4),MS,True)]),'Visier')),
    # Laufmantel mit Fenstern + Messing-Klemmring
    Lb(P([(490,240),(620,240),(632,252),(632,290),(490,290)],BO,-18,18,r=5,
      dec=[D(roundpoly(rect(x,252,20,24),3),DK) for x in (506,536,566)]),'Laufmantel'),
    P(rect(596,234,14,62),MS,-21,21,r=3),
    # Lauf + Kompensator
    C(632,690,266,7,'#3A3034',n=16),
    Lb(P(rect(690,252,34,28),DK,-11,11,r=4,dec=[D(roundpoly(rect(698,256,6,8),2),'#0A0A0D'),D(roundpoly(rect(710,256,6,8),2),'#0A0A0D')],
      xdec=[('x+',724,circ(266,0,6,12),'#050506',False)]),'Mündung'),
    # Griff (dunkel) mit Griffrillen
    Lb(P([(262,326),(306,326),(296,420),(250,420)],DK,-17,17,r=6,dec=[D(roundpoly(rect(264,344+14*i,30,5),2),'#3A3034') for i in range(5)]),'Griff'),
    # Abzug + offener Bügel vor dem Griff, deutlich unter dem Gehäuse
    Lb(P([(330,327),(342,327),(354,362),(343,366)],MS,-6,6,r=2),'Abzug'),
    P(rect(298,374,78,9),DK,-7,7,r=3),
    P(rect(368,326,9,57),DK,-7,7,r=3),
    # Magazin (Messing) im Schacht vor dem Bügel
    Lb(P([(384,326),(418,326),(424,422),(392,426)],MS,-14,14,r=4,dec=[D(roundpoly(rect(394,346,18,4),1),DK),D(roundpoly(rect(396,404,20,6),2),DK)]),'Magazin'),
    ]
META=dict(num='06',name='Maschinenpistole',vname='Klemmbacke',col='#C9A24A',pill='BORDEAUX · MESSING · ANTHRAZIT',
 palette=[BO,MS,DK,EL],center=(397,300,0),
 aria='Maschinenpistole Variante H: modulare Werkstatt-MP mit bordeauxrotem Ober- und dunklem Untergehäuse, verbunden durch zwei verschraubte Messing-Klemmplatten, Teleskopschaft, Messing-Magazin, offenem Abzugbügel und Laufmantel mit Fenstern; Reflexvisier separat',
 desc='Werkstatt-MP aus zwei verschraubten Modulen: Ober- und Untergehäuse halten über zwei Messing-Klemmplatten zusammen. Teleskopschaft mit Klemmring, Messing-Magazin im Schacht, Laufmantel mit Fenstern und Kompensator. Das Reflexvisier ist ein separates Modul für die Schiene.',
 form='Zweiteiliges Gehäuse mit Messing-Klemmplatten · Teleskopschaft · Magazin vor dem Abzug · offener Abzugbügel · Laufmantel mit Klemmring · Kompensator · Visier separat',
 desc3='Die Klemmbacke als Konzeptblatt: Bordeaux-Obergehäuse und dunkles Untergehäuse sind über zwei verschraubte Messing-Klemmplatten verbunden. Der Abzug liegt offen im Bügel vor dem Griff, davor steckt das Messing-Magazin im Schacht. Hinten der Teleskopschaft mit Klemmring, vorne Laufmantel mit Fenstern, sichtbarer Lauf und Kompensator. Das Reflexvisier wird separat auf die Schiene geklemmt.')
