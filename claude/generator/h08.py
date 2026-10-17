from flib import *
from flabel import Lb
from hxlib import S
from eng import rect,circ,roundpoly
TG,KU,DK,HG='#1F4A3A','#C06A3A','#15201B','#DCE6DE'
def bolts(pts,c=DK,r=3.0):return [D(circ(x,y,r,10),c) for x,y in pts]
def spec():
    return [
    # Bullpup-Körper (Tiefgrün) mit Kupfer-Messskala
    Lb(P([(80,240),(420,240),(440,256),(440,320),(420,334),(110,334),(80,316)],TG,-25,25,r=8,
      dec=[D(rect(130+12*i,246,3,8 if i%5 else 14),KU) for i in range(22)]
          +[D(roundpoly(rect(118,278,132,26),5),DK),D(roundpoly(rect(128,286,54,8),2),KU,True)]
          +bolts([(96,262),(96,300),(428,272),(428,304)])),'Gehäuse'),
    # Schaftkappe (Gummi)
    Lb(P(rect(64,234,20,108),DK,-23,23,r=5,dec=[D(roundpoly(rect(68,246+16*i,12,8),2),'#2A3A32') for i in range(5)]),'Schaft'),
    # Magazin hinter dem Griff (Bullpup) im Schacht
    Lb(P([(170,334),(214,334),(220,398),(176,400)],KU,-16,16,r=4,dec=[D(roundpoly(rect(182,352,26,5),2),DK),D(roundpoly(rect(184,382,28,6),2),DK)]),'Magazin'),
    # Griff, Abzug, offener Bügel vor dem Griff
    Lb(P([(300,334),(340,334),(332,426),(290,426)],DK,-16,16,r=6,dec=[D(roundpoly(rect(302,352+14*i,26,5),2),'#2A3A32') for i in range(5)]),'Griff'),
    Lb(P([(352,335),(363,335),(376,370),(365,373)],KU,-6,6,r=2),'Abzug'),
    P(rect(332,380,72,9),DK,-7,7,r=3),
    P(rect(396,334,9,55),DK,-7,7,r=3),
    # Montageschiene (bleibt)
    Lb(P(rect(150,230,230,11),DK,-9,9,r=2,dec=[D(rect(x,232,8,4),'#2A3A32') for x in range(158,374,16)]),'Visierschiene'),
    # Zielfernrohr separat: zwei Ringe mit Klemmfuß, Rohr, Okular, Objektiv
    S(P(rect(186,214,18,17),DK,-12,12,r=3)),
    S(P(rect(318,214,18,17),DK,-12,12,r=3)),
    S(P(rect(182,186,26,30),KU,-16,16,r=4,dec=bolts([(195,208)],DK,2.4))),
    S(P(rect(314,186,26,30),KU,-16,16,r=4,dec=bolts([(327,208)],DK,2.4))),
    S(Lb(C(150,362,200,13,DK,n=12),'Zielfernrohr')),
    S(F(124,150,200,17,13,TG)),
    S(F(362,392,200,13,18,TG)),
    S(C(392,396,200,18,DK,n=12,cap=[(200,0,13,KU,True)])),
    # Laufmantel mit Leiterfenstern + Kupfer-Klemmbänder
    Lb(P([(440,258),(640,258),(652,270),(652,308),(440,308)],TG,-15,15,r=5,
      dec=[D(roundpoly(rect(456+26*i,272,16,22),3),DK) for i in range(7)]),'Laufmantel'),
    P(rect(500,252,10,62),KU,-18,18,r=3),
    P(rect(604,252,10,62),KU,-18,18,r=3),
    # sichtbarer Lauf, Gabel-Emitter
    C(652,698,283,6,'#3A4A42',n=16),
    Lb(P(rect(696,262,14,42),DK,-11,11,r=3),'Mündung'),
    P(rect(708,264,44,8),KU,-7,7,r=3),
    P(rect(708,294,44,8),KU,-7,7,r=3),
    ]
META=dict(num='08',name='Spurgewehr',vname='Messlatte',col='#C06A3A',pill='TIEFGRÜN · KUPFER · DUNKEL',
 palette=[TG,KU,DK,HG],center=(408,306,0),
 aria='Spurgewehr Variante H: tiefgrünes Bullpup-Spurgewehr mit kupferner Messskala, Magazin hinter dem Griff, offenem Abzugbügel, Laufmantel mit Leiterfenstern und Kupfer-Klemmbändern, sichtbarem Lauf und Gabel-Emitter; Zielfernrohr separat',
 desc='Präzisions-Spurgewehr der Werkstatt-Serie im Bullpup-Aufbau: Das Magazin sitzt hinter dem Griff, oben läuft eine kupferne Messskala über das tiefgrüne Gehäuse. Der Laufmantel mit Leiterfenstern ist mit zwei Kupferbändern geklemmt, vorne gabelt sich der Emitter. Das Zielfernrohr ist ein separates Modul.',
 form='Bullpup-Gehäuse mit Messskala · Magazin hinter dem Griff · offener Abzugbügel · Laufmantel mit Leiterfenstern und Klemmbändern · Gabel-Emitter · Zielfernrohr separat',
 desc3='Die Messlatte als Konzeptblatt: Im Bullpup-Aufbau steckt das Kupfer-Magazin hinter dem Griff im Schacht, der Abzug liegt offen im Bügel davor. Über das tiefgrüne Gehäuse läuft die Kupfer-Messskala bis zur Schiene. Vorne folgen der Laufmantel mit Leiterfenstern und zwei Kupfer-Klemmbändern, der sichtbare Lauf und der Gabel-Emitter. Das Zielfernrohr mit zwei Ringen wird separat auf die Schiene gesetzt.')
