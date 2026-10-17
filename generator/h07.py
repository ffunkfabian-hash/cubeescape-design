from flib import *
from flabel import Lb
from hxlib import S
from eng import rect,circ,roundpoly
SG,TQ,DK,SL='#B8B09C','#1FB5A8','#2A2C2E','#E4DECF'
def bolts(pts,c=DK,r=3.0):return [D(circ(x,y,r,10),c) for x,y in pts]
def spec():
    return [
    # Skelettschaft: Schaftkappe, Oberholm, Strebe
    Lb(P([(80,232),(104,232),(104,330),(84,326)],DK,-20,20,r=5),'Schaft'),
    P(rect(102,238,92,14),SG,-12,12,r=3),
    P([(102,306),(194,288),(194,302),(102,320)],SG,-12,12,r=2),
    # Energiemodul hinten oben, mit zwei Klemmbändern
    Lb(P(rect(200,212,124,42),DK,-22,22,r=6,dec=[D(roundpoly(rect(214,222,94,18),5),TQ,True)]),'Energiemodul'),
    P(rect(226,206,12,54),SL,-25,25,r=3,dec=bolts([(232,214)],DK,2.4)),
    P(rect(288,206,12,54),SL,-25,25,r=3,dec=bolts([(294,214)],DK,2.4)),
    # Gehäuse (Sandgrau)
    Lb(P([(192,252),(500,252),(520,268),(520,316),(498,330),(212,330),(192,312)],SG,-26,26,r=8,
      dec=[D(roundpoly(rect(214,300,170,10),3),DK)]+[D(roundpoly(rect(400+16*i,272,8,26),2),DK) for i in range(5)]+bolts([(204,266),(204,300),(508,280),(508,306)])),'Gehäuse'),
    # Schiene vorne oben (bleibt an der Waffe)
    P(rect(340,242,150,11),DK,-10,10,r=2,dec=[D(rect(x,244,7,4),'#45484C') for x in range(348,484,15)]),
    # Visier separat: Klemmfuß + Holo-Rahmen
    S(P(rect(392,228,42,15),DK,-11,11,r=3,dec=bolts([(402,235),(424,235)],SL,2.2))),
    S(Lb(P([(386,196),(440,196),(446,228),(380,228)],SG,-12,12,r=5,
      xdec=[('x+',446,roundpoly(rect(202,-7,20,14),4),TQ,True)]),'Visier')),
    # Griff, Abzug, offener Bügel
    Lb(P([(262,330),(304,330),(296,424),(252,424)],DK,-17,17,r=6,dec=[D(roundpoly(rect(264,348+14*i,28,5),2),'#45484C') for i in range(5)]),'Griff'),
    Lb(P([(322,331),(333,331),(346,368),(335,371)],SL,-6,6,r=2),'Abzug'),
    P(rect(294,378,76,9),DK,-7,7,r=3),
    P(rect(362,330,9,57),DK,-7,7,r=3),
    # Energiezelle im Schacht unter dem Vorderteil
    Lb(P(rect(392,330,74,42),DK,-18,18,r=5,dec=[D(roundpoly(rect(402,342,54,8),3),TQ,True)]),'Energiezelle'),
    # Lauf, drei Kühlrippen-Platten, Mündung
    C(520,700,290,9,'#3E4144',n=16),
    Lb(P(rect(540,256,14,68),SL,-30,30,r=3),'Kühlrippen'),
    P(rect(576,256,14,68),SL,-30,30,r=3),
    P(rect(612,256,14,68),SL,-30,30,r=3),
    P(rect(662,272,12,36),DK,-16,16,r=3),
    Lb(C(700,742,290,15,DK,n=12,cap=[(290,0,10,'#050506',False),(290,0,5,TQ,True)]),'Mündung'),
    ]
META=dict(num='07',name='Fusionsgewehr',vname='Kolbenwerk',col='#1FB5A8',pill='SANDGRAU · TÜRKIS · ANTHRAZIT',
 palette=[SG,TQ,DK,SL],center=(411,318,0),
 aria='Fusionsgewehr Variante H: sandgraues Werkstatt-Fusionsgewehr mit aufgeklemmtem Energiemodul oben hinten, Skelettschaft, Energiezelle unter dem Vorderteil, offenem Abzugbügel, drei Kühlrippen-Platten am sichtbaren Lauf und türkisem Mündungskern; Holo-Visier separat',
 desc='Werkstatt-Fusionsgewehr: Das Energiemodul ist mit zwei Klemmbändern oben auf das sandgraue Gehäuse gesetzt und lässt sich tauschen. Drei Kühlrippen-Platten sitzen direkt auf dem sichtbaren Lauf, die Energiezelle steckt unten im Schacht. Das Holo-Visier ist ein separates Modul.',
 form='Aufgeklemmtes Energiemodul · Skelettschaft · Energiezelle im Schacht · offener Abzugbügel · Kühlrippen auf dem Lauf · Mündung mit Kern · Visier separat',
 desc3='Das Kolbenwerk als Konzeptblatt: Oben hinten sitzt das tauschbare Energiemodul mit türkisem Fenster, gehalten von zwei verschraubten Klemmbändern. Unter dem Vorderteil steckt die Energiezelle im Schacht, davor liegt der Abzug offen im Bügel. Am sichtbaren Lauf folgen drei Kühlrippen-Platten, eine Laufstütze und die Mündung mit türkisem Kern. Das Holo-Visier wird separat auf die Schiene geklemmt.')
