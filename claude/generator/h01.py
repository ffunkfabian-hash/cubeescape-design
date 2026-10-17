import math
from hlib import *
GR,YE,ST,DK='#3B3F45','#E8B10C','#9AA1A9','#1C1E22'
INFO=dict(num='01',name='Pistole',nick='SCHRAUBSTOCK',col=YE,pill='GRAPHIT · SIGNALGELB · STAHL',pal=[GR,YE,ST,DK],center=(430,330,0),
 alt='Pistole Variante H: modulare Werkstatt-Pistole mit stahlgrauem Schlittenmodul, zwei signalgelben Klemmbändern, graphitfarbenem Rahmen, Visierschiene, verschraubtem Mündungsmodul, offenem Abzugbügel und Magazin mit gelber Bodenplatte; Reflexvisier separat gezeichnet',
 desc='Prototyp aus der Werkstatt-Serie: Das stahlgraue Schlittenmodul ist mit zwei signalgelben Klemmbändern auf den Graphit-Rahmen geschraubt. Vorn sitzt ein austauschbares, verschraubtes Mündungsmodul auf dem sichtbaren Lauf. Abzug und Bügel hängen offen unter dem Rahmen. Das Mini-Reflexvisier ist ein separates Modul für die Schiene.',
 form='Verschraubtes Schlittenmodul mit zwei Klemmbändern · Visierschiene · Rahmen mit Zubehörschiene · Lauf mit Mündungsmodul · kantiger Griff mit Magazin · offener Abzugbügel · Reflexvisier separat')
ITEMS=[
 dict(t='poly',p=[(246,300),(322,300),(312,430),(300,442),(242,442),(234,430)],c=GR,z=(-18,18),r=6,L='Griff',
      d=[([(256,318),(308,318),(300,410),(252,410)],DK,False,4)]+screws([(262,330),(296,330),(256,398),(290,398)],GR,3)),
 dict(t='poly',p=[(238,440),(306,440),(306,466),(238,466)],c=YE,z=(-20,20),r=3,L='Magazin',
      d=[([(250,450),(294,450),(294,455),(250,455)],DK,False,1)]),
 dict(t='poly',p=[(316,352),(404,352),(404,363),(316,363)],c=DK,z=(-6,6),r=2,L='Abzug'),
 dict(t='poly',p=[(394,296),(404,296),(404,363),(394,363)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(338,297),(354,297),(370,340),(357,345)],c=YE,z=(-5,5),r=1,L='Abzug'),
 dict(t='poly',p=[(226,272),(540,272),(540,290),(528,300),(236,300),(226,290)],c=GR,z=(-17,17),r=3,
      d=slots(424,526,16,291,10,5,DK)+screws([(244,282),(520,282)],DK)),
 dict(t='poly',p=[(214,226),(512,226),(530,240),(530,272.5),(214,272.5),(204,262),(204,236)],c=ST,z=(-19,19),r=4,L='Schlitten',
      d=[([(x,236),(x+5,236),(x+5,264),(x,264)],GR,False,0) for x in range(218,262,10)]+[([(330,238),(390,238),(390,250),(330,250)],DK,False,2)]+screws([(302,244),(302,262),(420,244),(420,262)],DK)),
 dict(t='poly',p=[(270,222),(292,222),(292,276),(270,276)],c=YE,z=(-21,21),r=2,L='Klemmband',d=screws([(281,234),(281,264)],DK,2.6)),
 dict(t='poly',p=[(448,222),(470,222),(470,276),(448,276)],c=YE,z=(-21,21),r=2,L='Klemmband',d=screws([(459,234),(459,264)],DK,2.6)),
 # Visierschiene zwischen den Klemmbaendern
 dict(t='poly',p=[(300,218),(440,218),(440,226.5),(300,226.5)],c=DK,z=(-8,8),r=1,L='Visierschiene',d=slots(306,436,12,220,6,4,GR)),
 dict(t='cyl',x=(528,588),y=252,R=11,c='#5A6068',n=16,L='Lauf'),
 dict(t='poly',p=[(580,232),(632,232),(642,242),(642,264),(632,274),(580,274)],c=GR,z=(-18,18),r=3,L='Mündung',
      d=[([(592,240),(600,240),(600,250),(592,250)],DK,False,1),([(610,240),(618,240),(618,250),(610,250)],DK,False,1)]+screws([(588,264),(626,264)],YE,2.8),
      xd=bore(642,252,7)),
 # --- Visier (separat): Mini-Reflexvisier auf der Schiene
 dict(t='poly',p=[(334,206),(392,206),(392,218.5),(334,218.5)],c=DK,z=(-10,10),r=2,S=True,L='Reflexvisier',d=screws([(342,212),(384,212)],GR,2.2)),
 dict(t='poly',p=[(344,180),(384,180),(392,190),(392,206.5),(334,206.5),(334,190)],c=GR,z=(-11,11),r=3,S=True,L='Reflexvisier',
      d=[([(342,188),(386,188),(386,202),(342,202)],DK,False,2),([(346,191),(382,191),(382,199),(346,199)],'#7FC8E8',False,2)]),
]
