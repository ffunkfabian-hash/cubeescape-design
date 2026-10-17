from flib import *
from flabel import Lb
from fsight import Sg
from eng import rect,circ,roundpoly
G,R,W,K='#8D99AE','#D90429','#EDF2F4','#2B2D42'
def spec():
    bores=[]
    for y in (226,276):
        for z in (-34,0,34):bores+=[(y,z,15,'#06070B',False),(y,z,7.5,R,True)]
    xd=[('x+',626,circ(y,z,r),c,e) for (y,z,r,c,e) in bores]
    return [
    Lb(F(196,242,252,50,38,K),'Abgasdüse'),
    P(rect(238,204,64,96),W,-46,46,r=16,dec=[D(roundpoly(rect(252,232,36,10),3),R)]),
    Lb(P(rect(298,190,312,124),G,-56,56,r=24,
      dec=[D(roundpoly(rect(330,210,130,54),10),W),D(roundpoly(rect(342,222,64,8),3),K),D(roundpoly(rect(342,238,96,8),3),K),
           D(roundpoly([(486,286),(590,286),(590,298),(486,298)],3),R)]),'Raketenkasten'),
    Lb(P(rect(604,184,22,136),W,-62,62,r=8,xdec=xd),'Raketenrohre'),
    # Visierschiene seitlich LINKS am Raketenkasten (Sichtlinie am Kasten vorbei, wie RPG-7/Carl Gustaf)
    Lb(P(rect(424,192,52,22),K,56,64,r=3,dec=[D(rect(x,196,5,14),'#3E4256') for x in range(430,472,10)]),'Visierschiene'),
    Sg(P(rect(430,196,40,14),K,64,68,r=2)),
    Sg(Lb(P(rect(410,186,76,24),W,68,86,r=5,xdec=[('x+',486,circ(198,77,5),R,True)]),'Visier')),
    P(rect(380,312,180,10),K,-22,22,r=3),
    Lb(P([(402,322),(446,322),(438,410),(394,410)],K,-16,16,r=8,dec=[D(roundpoly(rect(404,350,28,6),2),R)]),'Griff'),
    # Abzug im Bügel vor dem hinteren Griff
    Lb(P([(452,324),(462,324),(469,366),(460,368)],R,-3.5,3.5,r=1),'Abzug'),
    Lb(P(rect(437,374,62,7),K,-5,5,r=3),'Abzug'),
    P(rect(492,322,7,59),K,-5,5,r=3),
    Lb(P([(520,322),(552,322),(548,384),(516,384)],K,-14,14,r=8),'Vordergriff'),
    ]
META=dict(num='09',name='Raketenwerfer',vname='Bienenstock',col='#D90429',pill='TAUBENGRAU · KIRSCHROT · WEISS',
 palette=[G,R,W,K],center=(412,300,0),
 aria='Raketenwerfer Variante F: breiter taubengrauer Kasten mit weißem Frontrahmen und sechs Raketenrohren, rotem Visier, Abgasdüse hinten und zwei Griffen',
 desc='Statt eines Rohrs ein ganzer Kasten: sechs kleine Raketen in zwei Reihen, die als Salve starten. Taubengrau mit weißem Rahmen und kirschroten Warnakzenten. Die Visierschiene ist seitlich links montiert, das Visier separat gezeichnet.',
 form='Raketenkasten mit sechs Rohren · weißer Frontrahmen · Visierschiene seitlich links montiert, Visier separat · Abgasdüse hinten · Griff mit Abzug und Vordergriff',
 desc3='Der Bienenstock als Konzeptblatt: Vorne sitzen die sechs Raketenrohre im weißen Rahmen, hinten die Abgasdüse. Seitlich links am Kasten sitzt auf Höhe der Oberkante die Visierschiene für das separat gezeichnete Visier – so verdeckt der Kasten die Sichtlinie nicht; unten trägt eine Schiene den Griff mit Abzug im Bügel und den Vordergriff.')
