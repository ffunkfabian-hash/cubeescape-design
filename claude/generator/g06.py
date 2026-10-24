from flib import *
from flabel import Lb
from gsight import S
from eng import rect,circ,roundpoly
CR,AN,OR,CY,DK='#EFE6D2','#2C2F36','#FF7A1A','#5FD4E0','#1A1C21'
def spec():
    vents=[D(roundpoly(rect(x,282,12,30),3),DK) for x in (516,536,556,576)]
    return [
    # Klappschaft: Schaftkappe, zwei Streben, Scharnierblock am Gehäuse
    Lb(P([(98,252),(120,252),(120,350),(98,346)],CR,-22,22,r=5),'Schaft'),
    P(rect(118,262,58,13),AN,-9,9,r=3),
    P(rect(118,318,58,12),AN,-9,9,r=3),
    P(rect(170,256,14,78),AN,-17,17,r=3),
    # Gehäuse mit abgeschrägten Kanten
    Lb(P([(182,252),(468,252),(500,270),(500,328),(470,340),(202,340),(182,322)],CR,-26,26,r=8,
      dec=[D(roundpoly([(186,316),(496,316),(496,326),(468,338),(204,338),(186,322)],3),AN),
           D(roundpoly(rect(232,272,92,26),5),AN),
           D(roundpoly(rect(244,280,68,10),3),DK),
           D(roundpoly(rect(424,276,34,7),2),OR,True)]),'Gehäuse'),
    # Montageschiene + Reflexvisier
    P(rect(232,242,212,11),AN,-10,10,r=2,dec=[D(rect(x,244,7,4),DK) for x in range(240,436,16)]),
    S(P(rect(334,228,40,15),AN,-9,9,r=3)),
    S(Lb(P([(318,198),(380,198),(388,229),(312,229)],AN,-13,13,r=5,
      xdec=[('x+',388,roundpoly(rect(205,-8,18,16),4),CY,True)]),'Visier')),
    # belüfteter Laufmantel, Lauf, Mündung
    Lb(P([(500,262),(598,262),(616,278),(616,318),(598,332),(500,332)],AN,-20,20,r=6,dec=vents),'Laufmantel'),
    C(616,652,297,8,DK,n=16),
    C(652,676,297,13,AN,n=8,cap=[(297,0,7,'#050506',False),(297,0,3,OR,True)]),
    # Vordergriff
    Lb(P([(522,332),(560,332),(553,392),(528,392)],CR,-13,13,r=6),'Vordergriff'),
    # Griff mit Magazin im Griffschacht, orange Bodenplatte
    Lb(P([(300,340),(352,340),(342,442),(286,442)],AN,-18,18,r=6,
      dec=[D(roundpoly(rect(300,360+12*i,36,5),2),DK) for i in range(5)]),'Griff'),
    Lb(P([(288,440),(342,440),(340,460),(286,460)],OR,-16,16,r=4),'Magazin'),
    # Abzug + Abzugbügel vor dem Griff, deutlich unter dem Gehäuse
    Lb(P([(364,341),(376,341),(388,384),(376,388)],OR,-6,6,r=2),'Abzug'),
    P(rect(348,406,70,9),AN,-7,7,r=3),
    P(rect(410,340,9,75),AN,-7,7,r=3),
    ]
META=dict(num='06',name='Maschinenpistole',vname='Funke',col='#FF7A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(387,330,0),
 aria='Maschinenpistole Variante G: kompakte cremefarbene PDW mit abgeschrägtem Gehäuse, Klappschaft, Reflexvisier auf Schiene, belüftetem Laufmantel und Magazin im Griff mit oranger Bodenplatte',
 desc='Kompakte PDW in der Cube-Escape-Designsprache: cremefarbenes, abgeschrägtes Gehäuse, Magazin im Griff, Klappschaft und ein Reflexvisier auf der Schiene. Orange nur an Abzug, Magazin und Ladeanzeige.',
 form='Abgeschrägtes Gehäuse · Magazin im Griff · Klappschaft mit zwei Streben · Reflexvisier auf Schiene · belüfteter Laufmantel · Vordergriff',
 desc3='Der Funke als Konzeptblatt: Das Magazin steckt im Pistolengriff und schließt unten mit der orangen Bodenplatte ab. Vor dem Griff liegt der orange Abzug im Bügel, hinten klappt der Schaft am Scharnierblock. Das Reflexvisier steht auf einer Montage auf der Schiene, vorne folgen belüfteter Laufmantel, Lauf und Mündung.')
