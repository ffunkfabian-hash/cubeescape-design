from flib import *
from flabel import Lb
from fsight import Sg
from eng import rect,circ,roundpoly
U,L,W,K='#2B3FD6','#E8F542','#F2F4F8','#141833'
def spec():
    rib=[D(roundpoly(rect(x,228,8,18),2),K) for x in range(200,460,36)]
    return [
    Lb(P([(100,262),(124,258),(124,346),(100,342)],K,-30,30,r=4),'Schaft'),
    Lb(P([(120,262),(500,262),(562,296),(562,346),(130,346),(116,320)],W,-28,28,r=14,
      dec=[D(roundpoly([(140,300),(540,300),(540,314),(140,314)],4),U),
           D(roundpoly(rect(390,322,120,14),4),K)]),'Gehäuse'),
    Lb(P(rect(166,222,312,40),L,-22,22,r=10,dec=rib,emit=False),'Magazin'),
    # Visierbrücke: zwei Stützen neben dem Magazin bis aufs Gehäuse, Platte darüber, Reflexvisier oben
    P(rect(398,212,20,51),K,23,27,r=2),
    P(rect(398,212,20,51),K,-27,-23,r=2),
    Lb(P(rect(390,204,36,10),K,-27,27,r=3),'Visierschiene'),
    Sg(Lb(P(rect(376,186,64,18),K,-9,9,r=4,dec=[D(roundpoly(rect(418,190,12,8),2),L,True)]),'Visier')),
    # Daumenloch-Schaft: Schaftblock hinten + untere Strebe zum Griff
    Lb(P([(104,346),(196,346),(190,420),(110,420)],U,-20,20,r=8),'Schaft'),
    P(rect(186,402,146,18),U,-16,16,r=6),
    Lb(P([(330,346),(380,346),(372,440),(320,440)],K,-20,20,r=8,dec=[D(roundpoly(rect(332,372+12*i,34,5),2),'#262B55') for i in range(4)]),'Griff'),
    # Abzug + Abzugbügel vor dem Griff
    Lb(P([(386,348),(396,348),(403,388),(394,390)],L,-3.5,3.5,r=1),'Abzug'),
    Lb(P(rect(371,396,76,7),K,-5,5,r=3),'Abzug'),
    Lb(P(rect(440,346,7,57),K,-5,5,r=3),'Abzug'),
    P([(460,346),(520,346),(512,392),(470,392)],K,-16,16,r=8),
    Lb(P(rect(560,280,86,62),U,-22,22,r=12,dec=[D(roundpoly(rect(x,292,10,38),3),K) for x in (578,598,618)]),'Laufmantel'),
    C(644,684,311,15,K,cap=[(311,0,9,'#05060A',False),(311,0,4.5,L,True)]),
    ]
META=dict(num='06',name='Maschinenpistole',vname='Hornisse',col='#E8F542',pill='ULTRAMARIN · ZITRONE · WEISS',
 palette=[U,L,W,K],center=(392,330,0),
 aria='Maschinenpistole Variante F: kompakte weiße Waffe mit zitronengelbem Längsmagazin oben, ultramarinblauem Lauf-Mantel und Daumenloch-Rahmen',
 desc='Kompakt und ergonomisch: das Magazin liegt quer oben auf dem Gehäuse, darunter ein Daumenloch-Rahmen. Weiß mit Ultramarin und Zitronengelb – schnell erkennbar im Gefecht.',
 form='Längsmagazin oben · Visierbrücke als Aufnahme, Reflexvisier separat · Daumenloch-Schaft · Abzug mit Bügel · belüfteter Laufmantel',
 desc3='Die Hornisse als Konzeptblatt: Das gerippte Längsmagazin liegt oben auf dem Gehäuse, die Visierbrücke steht mit zwei Stützen neben dem Magazin auf dem Gehäuse; das Reflexvisier ist ein separates Modul und separat gezeichnet. Hinten bildet der Schaft mit der unteren Strebe das Daumenloch, vor dem Griff liegt der Abzug im Bügel.')
