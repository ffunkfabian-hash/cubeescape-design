from flib import *
from flabel import Lb
from hxlib import S
from eng import rect,circ,roundpoly
SC,LI,DK,HG='#4A5563','#B5E02E','#1C2027','#C9CFD6'
def bolts(pts,c=DK,r=3.2):return [D(circ(x,y,r,10),c) for x,y in pts]
def spec():
    return [
    # Abschussrohr als kantiges Kastenrohr
    Lb(P(rect(160,190,480,80),SC,-40,40,r=12,
      dec=[D(roundpoly(rect(300,206,150,14),4),DK),D(roundpoly(rect(470,244,120,10),3),DK)]+bolts([(176,206),(176,254),(624,206),(624,254)])),'Abschussrohr'),
    # Limetten-Spannbänder (umlaufend)
    P(rect(258,184,16,92),LI,-44,44,r=4,dec=bolts([(266,196),(266,264)],DK,2.6)),
    P(rect(508,184,16,92),LI,-44,44,r=4,dec=bolts([(516,196),(516,264)],DK,2.6)),
    # Mündungsrahmen mit Öffnung und Raketenspitze
    Lb(P(rect(640,184,18,92),LI,-44,44,r=6,
      xdec=[('x+',658,roundpoly(rect(198,-30,64,60),10),'#050506',False),('x+',658.5,circ(230,0,12,14),'#E8F7B0',True)]),'Mündung'),
    # offene Abgasdüse hinten mit Innenrohr
    Lb(F(112,160,230,46,36,DK),'Abgasdüse'),
    C(108,113,230,42,'#050506',n=16),
    C(100,108,230,46,SC,n=16),
    # Tragrahmen unter dem Rohr
    P(rect(220,270,330,14),DK,-14,14,r=3,dec=bolts([(232,277),(538,277)],HG,2.4)),
    # Schulterstütze
    Lb(P([(178,270),(244,270),(244,316),(196,316)],HG,-18,18,r=5,dec=[D(roundpoly(rect(188,284,48,6),2),DK)]),'Schulterstütze'),
    # Griff, Abzug, offener Bügel
    Lb(P([(300,284),(340,284),(330,380),(290,380)],DK,-16,16,r=6,dec=[D(roundpoly(rect(302,302+14*i,26,5),2),'#30353D') for i in range(5)]),'Griff'),
    Lb(P([(352,285),(363,285),(374,322),(364,325)],LI,-6,6,r=2),'Abzug'),
    P(rect(330,332,66,9),DK,-7,7,r=3),
    P(rect(388,284,9,57),DK,-7,7,r=3),
    # Vordergriff
    Lb(P([(470,284),(502,284),(498,362),(474,362)],DK,-14,14,r=6),'Vordergriff'),
    # Visier-Aufnahme seitlich LINKS am Rohr (Sichtlinie neben dem Rohr): Montageklammer + Schiene auf Höhe der Oberkante
    P(rect(318,190,132,26),DK,40,47,r=4,dec=bolts([(330,203),(438,203)],HG,2.6)),
    Lb(P(rect(322,188,124,16),DK,47,56,r=2,dec=[D(rect(x,192,8,8),'#30353D') for x in range(330,440,15)]),'Visierschiene'),
    # Klappvisier separat (sitzt seitlich links auf der Schiene, Optik über Rohroberkante)
    S(P(rect(366,178,32,24),DK,56,66,r=3)),
    S(Lb(P([(362,138),(400,138),(404,180),(358,180)],HG,58,82,r=5,
      dec=[D(roundpoly(rect(370,146,22,22),4),DK)],xdec=[('x+',404,roundpoly(rect(146,62,22,14),3),LI,True)]),'Visier')),
    ]
META=dict(snote='seitlich links montiert',num='09',name='Raketenwerfer',vname='Lastenträger',col='#B5E02E',pill='SCHIEFER · LIMETTE · DUNKEL',
 palette=[SC,LI,DK,HG],center=(380,253,0),
 aria='Raketenwerfer Variante H: schiefergraues Kastenrohr auf einem dunklen Tragrahmen, gehalten von zwei limettengrünen Spannbändern, mit offener Abgasdüse hinten, Mündungsrahmen mit Raketenspitze, Schulterstütze, Griff mit offenem Abzugbügel und Vordergriff; Klappvisier separat, seitlich links montiert',
 desc='Werkstatt-Raketenwerfer: Das kantige Kastenrohr liegt auf einem dunklen Tragrahmen und ist mit zwei verschraubten Limetten-Spannbändern gesichert. Hinten öffnet sich die Abgasdüse, vorne zeigt der Mündungsrahmen die Raketenspitze. Das Klappvisier ist ein separates Modul und wird seitlich links montiert, damit das Rohr die Sichtlinie nicht verdeckt.',
 form='Kastenrohr auf Tragrahmen · zwei Spannbänder · offene Abgasdüse · Mündungsrahmen · Schulterstütze · offener Abzugbügel · Vordergriff · Visierschiene seitlich links · Visier separat',
 desc3='Der Lastenträger als Konzeptblatt: Das schiefergraue Kastenrohr ist mit zwei limettengrünen Spannbändern auf den dunklen Tragrahmen geschraubt. Darunter sitzen Schulterstütze, Griff mit offenem Abzug im Bügel und der Vordergriff. Hinten öffnet sich die Abgasdüse mit dunklem Innenrohr, vorne trägt der Mündungsrahmen die leuchtende Raketenspitze. Das Klappvisier wird separat auf die Visierschiene gesetzt, die seitlich links an der Rohroberkante verschraubt ist – so bleibt die Sichtlinie neben dem Rohr frei.')
