import math
from hlib import *
SL,OC,LG,DK='#4D5560','#D29A2E','#C8CDD2','#16191D'
INFO=dict(num='05',name='Scharfschützengewehr',nick='MESSLATTE',col=OC,pill='SCHIEFER · OCKER · HELLGRAU',pal=[SL,OC,LG,DK],center=(460,300,0),
 alt='Scharfschützengewehr Variante H: modulares Präzisionsgewehr mit hellgrauem Skelettschaft und ockerfarbener Wangenauflage, Schiefer-Gehäuse mit Kammerstängel links, Pistolengriff mit offenem Abzugbügel, Magazin im Schacht, gelochtem Handschutz mit Ocker-Klemmring, sichtbarem Lauf und Ocker-Mündungsbremse; Zielfernrohr mit Montageringen separat gezeichnet',
 desc='Präzisionsgewehr nach Abschnitt 4: Ein hellgrauer Skelettschaft mit verstellbarer Wangenauflage führt in das abgeschrägte Schiefer-Gehäuse. Darunter sitzen Pistolengriff, gut sichtbarer Abzug mit Bügel und davor das Magazin im Schacht. Der gelochte Handschutz ist mit einem Ocker-Klemmring angesetzt, der Lauf tritt sichtbar aus und endet in einer Mündungsbremse. Zielfernrohr und Montageringe sind ein separates Modul für die Schiene.',
 form='Skelettschaft mit Wangenauflage · abgeschrägtes Gehäuse mit Kammerstängel links · Pistolengriff + offener Abzugbügel · Magazin im Schacht · Visierschiene · gelochter Handschutz · sichtbarer Lauf · Mündungsbremse · Zielfernrohr separat')
ITEMS=[
 dict(t='poly',p=[(100,250),(116,250),(116,350),(100,346)],c=DK,z=(-16,16),r=3),
 dict(t='poly',p=[(116,252),(262,256),(262,272),(116,270)],c=LG,z=(-12,12),r=3,L='Schaft'),
 dict(t='poly',p=[(116,330),(262,300),(262,314),(116,346)],c=LG,z=(-12,12),r=3,L='Schaft'),
 dict(t='poly',p=[(180,268),(194,268),(194,322),(180,326)],c=LG,z=(-10,10),r=2),
 dict(t='poly',p=[(140,240),(232,242),(232,257),(140,255)],c=OC,z=(-10,10),r=3),
 dict(t='poly',p=[(140,255),(150,255),(150,270),(140,270)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(222,256),(232,256),(232,272),(222,272)],c=DK,z=(-6,6),r=1),
 # Gehaeuse
 dict(t='poly',p=[(260,240),(470,240),(486,252),(486,310),(470,318),(260,318)],c=SL,z=(-20,20),r=3,L='Gehäuse',
      d=[([(320,254),(400,254),(400,268),(320,268)],DK,False,2)]+screws([(272,252),(458,252),(272,306),(458,306)],DK)),
 # Kammerstaengel links (z+)
 dict(t='poly',p=[(302,256),(312,256),(312,282),(302,282)],c=DK,z=(20,32),r=1),
 dict(t='sphere',p=(307,286,32),R=6,c=OC),
 # Visierschiene
 dict(t='poly',p=[(270,232),(480,232),(480,240.5),(270,240.5)],c=DK,z=(-9,9),r=1,d=slots(276,476,12,234,6,4,SL)),
 # Griff, Abzugbuegel, Abzug
 dict(t='poly',p=[(300,316),(346,316),(338,416),(326,426),(298,426),(292,416)],c=DK,z=(-15,15),r=5,L='Griff'),
 dict(t='poly',p=[(350,364),(408,364),(408,374),(350,374)],c=DK,z=(-6,6),r=2),
 dict(t='poly',p=[(398,316),(408,316),(408,374),(398,374)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(360,317),(372,317),(384,350),(373,354)],c=OC,z=(-5,5),r=1,L='Abzug'),
 # Magazin + Bodenplatte
 dict(t='poly',p=[(414,316),(454,316),(458,388),(418,388)],c='#2E333A',z=(-14,14),r=3,L='Magazin'),
 dict(t='poly',p=[(416,386),(460,386),(460,396),(416,396)],c=OC,z=(-15,15),r=2),
 # Handschutz + Klemmring
 dict(t='poly',p=[(486,252),(660,256),(666,262),(666,300),(660,306),(486,310)],c=SL,z=(-16,16),r=4,L='Handschutz',
      d=slots(508,650,20,268,12,9,DK)+slots(508,650,20,286,12,9,DK)),
 dict(t='poly',p=[(484,246),(500,246),(500,316),(484,316)],c=OC,z=(-18,18),r=2,d=screws([(492,256),(492,306)],DK,2.4)),
 # Lauf und Muendungsbremse
 dict(t='cyl',x=(666,790),y=280,R=7,c='#2A2E33',n=16,L='Lauf'),
 dict(t='poly',p=[(782,264),(824,264),(832,272),(832,288),(824,296),(782,296)],c=OC,z=(-12,12),r=3,L='Mündungsbremse',
      d=slots(792,820,10,268,5,8,DK),xd=bore(832,280,5)),
 # --- Zielfernrohr mit Montageringen (separat)
 dict(t='poly',p=[(318,204),(338,204),(338,232.5),(318,232.5)],c=DK,z=(-13,13),r=2,S=True,L='Montageringe'),
 dict(t='poly',p=[(420,204),(440,204),(440,232.5),(420,232.5)],c=DK,z=(-13,13),r=2,S=True,L='Montageringe'),
 dict(t='frustum',x=(262,292),y=196,R=15,R1=11,c=SL,S=True,cap=[]),
 dict(t='cyl',x=(290,470),y=196,R=11,c=SL,n=20,S=True,L='Zielfernrohr'),
 dict(t='poly',p=[(370,176),(388,176),(388,186),(370,186)],c=OC,z=(-6,6),r=2,S=True),
 dict(t='frustum',x=(468,512),y=196,R=11,R1=17,c=SL,S=True,cap=[(13,'#5FB8D0',False)]),
]
