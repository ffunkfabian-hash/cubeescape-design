WH,GR,CY,OR='#F1EEE8','#3A3E45','#4FC8D8','#F59E3A'
DK='#24272C'
import math
INFO=dict(num='05',name='Scharfschützengewehr',nick='FERNKANTE',col=CY,pill='WEISS · GRAPHIT · CYAN',pal=[WH,GR,CY,OR],center=(450,290,0),
 alt='Scharfschützengewehr Variante G: weißes Präzisionsgewehr mit Lochschaft und Wangenauflage, Pistolengriff mit Abzug und Bügel, Magazin im Schacht davor, schlankem Handschutz mit eingeklapptem Zweibein, sichtbarem Lauf, Mündungsbremse und Zielfernrohr auf zwei Montageringen',
 desc='Präzisionsgewehr nach Abschnitt 4: Lochschaft mit verstellbarer Wangenauflage, Pistolengriff mit Abzug und Bügel, das Magazin sitzt davor im Schacht. Der schlanke Handschutz trägt ein eingeklapptes Zweibein, der Lauf tritt sichtbar aus und endet in einer kantigen Mündungsbremse. Das Zielfernrohr sitzt auf zwei Ringen über der Schiene.',
 form='Lochschaft mit Wangenauflage · Gehäuse mit Montageschiene · Pistolengriff mit Abzugbügel · Magazin vor dem Griff · Handschutz mit Zweibein · sichtbarer Lauf · Mündungsbremse · Zielfernrohr auf zwei Ringen')
ITEMS=[
 # Lochschaft: Schaftkappe, Oberholm, Wangenauflage, Unterholm
 dict(t='poly',p=[(60,226),(80,222),(86,234),(86,320),(80,330),(60,326)],c=GR,z=(-15,15),r=4,L='Schaft'),
 dict(t='poly',p=[(84,226),(252,234),(252,256),(84,250)],c=WH,z=(-12,12),r=4),
 dict(t='poly',p=[(130,216),(206,218),(206,232),(130,229)],c=GR,z=(-9,9),r=3),
 dict(t='poly',p=[(84,306),(252,286),(252,302),(84,322)],c=WH,z=(-12,12),r=4),
 # Griff, Abzugbuegel, Abzug
 dict(t='poly',p=[(290,294),(330,294),(320,384),(306,396),(272,396),(268,384)],c=GR,z=(-14,14),r=6,L='Griff'),
 dict(t='poly',p=[(318,346),(390,346),(390,356),(318,356)],c=GR,z=(-5,5),r=2),
 dict(t='poly',p=[(380,295),(390,295),(390,356),(380,356)],c=GR,z=(-5,5),r=1),
 dict(t='poly',p=[(344,295),(356,295),(364,328),(354,331)],c=OR,z=(-4,4),r=1,L='Abzug'),
 # Magazin im Schacht
 dict(t='poly',p=[(402,300),(450,300),(448,352),(404,352)],c=WH,z=(-13,13),r=4,L='Magazin',
      d=[([(412,322),(440,322),(440,328),(412,328)],OR,False,2)]),
 dict(t='poly',p=[(396,290),(456,290),(456,308),(396,308)],c=GR,z=(-16,16),r=2),
 # Gehaeuse, Kammerstaengel (rechts)
 dict(t='poly',p=[(248,222),(470,222),(486,236),(486,296),(262,296),(248,284)],c=GR,z=(-21,21),r=6,L='Gehäuse',
      d=[([(360,236),(420,236),(420,252),(360,252)],DK,False,2),([(268,268),(282,268),(282,276),(268,276)],CY,True,2)]),
 dict(t='poly',p=[(398,248),(410,248),(410,258),(398,258)],c=GR,z=(20,36)),
 dict(t='sphere',p=(404,253,40),R=7,c=OR),
 # Schiene, Montageringe, Zielfernrohr
 dict(t='poly',p=[(262,213),(470,213),(470,222.5),(262,222.5)],c=DK,z=(-9,9),r=1,
      d=[([(x,215),(x+6,215),(x+6,219),(x,219)],GR,False,0) for x in range(270,466,14)]),
 dict(t='poly',p=[(290,201),(308,201),(308,213.5),(290,213.5)],c=GR,z=(-8,8),r=1,S=True),
 dict(t='poly',p=[(408,201),(426,201),(426,213.5),(408,213.5)],c=GR,z=(-8,8),r=1,S=True),
 dict(t='cyl',x=(288,310),y=190,R=15,c=GR,L='Montageringe',S=True),
 dict(t='cyl',x=(406,428),y=190,R=15,c=GR,S=True),
 dict(t='frustum',x=(222,250),y=190,R=16,R1=12,c=GR,S=True),
 dict(t='cyl',x=(250,430),y=190,R=12,c=WH,L='Zielfernrohr',S=True),
 dict(t='poly',p=[(352,168),(366,168),(366,178.5),(352,178.5)],c=GR,z=(-6,6),r=2,S=True),
 dict(t='frustum',x=(430,470),y=190,R=13,R1=18,c=WH,cap=[(14,CY,True)],S=True),
 # Handschutz mit Zweibein
 dict(t='poly',p=[(484,234),(640,234),(652,244),(652,282),(640,290),(484,290)],c=WH,z=(-16,16),r=6,L='Handschutz',
      d=[([(x,254),(x+22,254),(x+22,262),(x,262)],GR,False,2) for x in range(504,630,32)]),
 dict(t='poly',p=[(598,289),(622,289),(622,300),(598,300)],c=GR,z=(-12,12),r=2),
 dict(t='poly',p=[(610,294),(704,298),(704,305),(610,302)],c=GR,z=(5,11),r=1),
 dict(t='poly',p=[(610,294),(704,298),(704,305),(610,302)],c=GR,z=(-11,-5),r=1),
 # Lauf und Muendungsbremse
 dict(t='cyl',x=(650,800),y=262,R=7,c='#4A4F57',n=16,L='Lauf'),
 dict(t='poly',p=[(798,248),(834,248),(842,254),(842,270),(834,276),(798,276)],c=GR,z=(-13,13),r=3,L='Mündungsbremse',
      d=[([(806,253),(812,253),(812,271),(806,271)],DK,False,1),([(820,253),(826,253),(826,271),(820,271)],DK,False,1)],
      xd=[(842.4,[(262+5*math.sin(k*0.5236),5*math.cos(k*0.5236)) for k in range(12)],'#0A0A0D',False)]),
]
