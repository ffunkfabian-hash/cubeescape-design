CR,AN,OR,DK='#EDE6D6','#2B2E33','#F07A1A','#15171A'
INFO=dict(num='01',name='Pistole',nick='WÜRFELKERN',col=OR,pill='CREME · ANTHRAZIT · ORANGE',pal=[CR,AN,OR,DK],center=(420,340,0),
 alt='Pistole Variante G: kantige Pistole mit cremefarbenem Schlitten, orange leuchtendem Energiewürfel, anthrazitfarbenem Rahmen, offenem Abzugbügel, würfelförmigem Magazinboden und Kompensator',
 desc='Kompakte Dienstpistole im Cube-Escape-Stil: Der cremefarbene Schlitten trägt einen orange leuchtenden Energiewürfel, der quer durch das Gehäuse steckt. Kimme und Korn sitzen fest auf dem Schlitten; die Kerbe der Kimme und die Spitze des orangen Korns liegen auf einer Linie parallel zum Lauf. Der Lauf ragt vorn aus dem Schlitten in einen kantigen Kompensator. Abzug und Bügel hängen gut sichtbar unter dem Rahmen.',
 form='Abgeschrägter Schlitten mit Energiewürfel · Rahmen mit Zierleiste · Kimme und Korn auf dem Schlitten · Lauf mit Kompensator · geneigter Griff mit Würfel-Magazinboden · offener Abzugbügel')
ITEMS=[
 # Griff (hinten liegend) und Magazinboden
 dict(t='poly',p=[(250,306),(320,306),(308,440),(298,452),(240,452),(232,440)],c=AN,z=(-18,18),r=8,L='Griff',
      d=[([(260,326),(306,326),(298,420),(250,420)],DK,False,5)]+[([(256,y),(302,y),(301,y+4),(255,y+4)],AN,False,0) for y in (350,372,394)]),
 dict(t='poly',p=[(234,450),(306,450),(306,476),(234,476)],c=OR,z=(-21,21),r=4,L='Magazin',
      d=[([(246,460),(294,460),(294,465),(246,465)],DK,False,1)]),
 # Abzugbuegel (unten offen sichtbar) und Abzug
 dict(t='poly',p=[(312,352),(394,352),(394,362),(312,362)],c=DK,z=(-5,5),r=2),
 dict(t='poly',p=[(384,306),(394,306),(394,362),(384,362)],c=DK,z=(-5,5),r=1),
 dict(t='poly',p=[(338,306),(350,306),(360,340),(350,343)],c=OR,z=(-4,4),r=1,L='Abzug'),
 # Rahmen mit Zubehoerschiene
 dict(t='poly',p=[(232,282),(530,282),(530,298),(518,308),(240,308),(232,300)],c=AN,z=(-17,17),r=3,L='Rahmen',
      d=[([(x,300),(x+10,300),(x+10,304),(x,304)],DK,False,0) for x in range(430,516,16)]),
 # Schlitten
 dict(t='poly',p=[(220,232),(520,232),(540,246),(540,282.5),(220,282.5),(208,270),(208,244)],c=CR,z=(-20,20),r=4,L='Schlitten',
      d=[([(x,240),(x+4,240),(x+4,272),(x,272)],AN,False,0) for x in range(222,262,9)]+[([(390,240),(440,240),(440,254),(390,254)],DK,False,2)]),
 # Energiewuerfel quer durch den Schlitten
 dict(t='poly',p=[(292,240),(346,240),(346,278),(292,278)],c=DK,z=(-24,24),r=3),
 dict(t='poly',p=[(296,244),(342,244),(342,274),(296,274)],c=OR,z=(-30,30),r=3,e=True,L='Energiewürfel'),
 # Zierleiste auf dem Schlitten (laeuft mit dem Schlitten); Kimme und Korn stehen am Ende der Liste (IDs der Bestandsteile bleiben)
 dict(t='poly',p=[(222,227.5),(518,227.5),(518,232.5),(222,232.5)],c=DK,z=(-7,7),r=1,R='slide'),
 # Lauf und Kompensator
 dict(t='cyl',x=(538,600),y=258,R=11,c='#3A3D44',n=16,L='Lauf'),
 dict(t='poly',p=[(592,240),(636,240),(646,250),(646,272),(636,280),(592,280)],c=AN,z=(-17,17),r=3,L='Kompensator',
      d=[([(604,246),(610,246),(610,256),(604,256)],DK,False,1),([(618,246),(624,246),(624,256),(618,256)],DK,False,1)],
      xd=[(646.4,[(260+7*__import__('math').sin(k*0.5236),7*__import__('math').cos(k*0.5236)) for k in range(12)],'#0A0A0D',False)]),

 # Kimme (hinten, Sockel mit Kerbe zwischen zwei Pfosten) und Korn (vorn, Keil) fest auf dem Schlitten (claude-0.17.1: statt Reflexvisier VS01).
 # Kerbenoberkante und Kornspitze liegen auf y=214, also parallel zur Muendungsachse (y=258); Kerbe 7 Einheiten breit, Korn 5
 dict(t='poly',p=[(224,222),(250,222),(250,232),(224,232)],c=DK,z=(-12,12),r=1,L='Kimme',S=True,I=True,R='slide'),
 dict(t='poly',p=[(224,214),(250,214),(250,222),(224,222)],c=DK,z=(-12,-3.5),r=1,L='Kimme',S=True,I=True,R='slide'),
 dict(t='poly',p=[(224,214),(250,214),(250,222),(224,222)],c=DK,z=(3.5,12),r=1,L='Kimme',S=True,I=True,R='slide'),
 dict(t='poly',p=[(503,232),(507,214),(512,214),(516,232)],c=OR,z=(-2.5,2.5),r=0,L='Korn',S=True,I=True,R='slide'),
]
