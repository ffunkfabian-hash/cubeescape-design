NV,IN,CH,CY='#12142A','#2E2F73','#E9D8B4','#00E5FF'
INFO=dict(num='05',name='Scharfschützengewehr',nick='MITTERNACHTSSCHIENE',col=CY,pill='INDIGO · CHAMPAGNER · CYAN',pal=[NV,IN,CH,CY],center=(380,280,0),
 alt='Scharfschützengewehr Variante F: Railgun in Indigo und Champagner mit Skelettschaft, Pistolengriff mit Abzugbügel, Energiemagazin, Lauf zwischen zwei Schienen, Mündungsbremse und Zielfernrohr auf zwei Montageringen',
 desc='Aus dem Gewehr wird eine Railgun: Der Lauf liegt zwischen zwei Champagner-Schienen, die von zwei Klammern gehalten werden und in einer Mündungsbremse enden. Das Zielfernrohr ist ein separates Modul: Es wird mit zwei Ringen auf die Montageschiene gesetzt und separat gezeichnet; das Energiemagazin steckt vor dem Abzugbügel im Gehäuse.',
 form='Skelettschaft mit Strebe und Schaftkappe · Pistolengriff mit Abzugbügel · Energiemagazin vor dem Griff · Lauf zwischen zwei Schienen · Mündungsbremse · Montageschiene, Zielfernrohr separat')
ITEMS=[
 # Schaft: Kappe, obere und untere Strebe, Verbindungsstrebe, Wangenauflage
 dict(t='poly',p=[(52,226),(74,226),(78,236),(78,328),(74,338),(52,338)],c=NV,z=(-15,15),r=6,L='Schaft'),
 dict(t='poly',p=[(76,234),(204,230),(204,246),(76,250)],c=IN,z=(-9,9),r=3),
 dict(t='poly',p=[(76,312),(204,288),(204,302),(76,328)],c=IN,z=(-9,9),r=3),
 dict(t='poly',p=[(128,246),(142,246),(142,304),(128,307)],c=IN,z=(-7,7),r=2),
 dict(t='poly',p=[(110,222),(184,220),(184,232),(110,235)],c=CH,z=(-8,8),r=4),
 # Gehaeuse mit abgeschraegter Front
 dict(t='poly',p=[(200,222),(404,222),(424,240),(424,300),(200,300)],c=IN,z=(-24,24),r=10,L='Gehäuse',
      d=[([(214,236),(330,236),(330,256),(214,256)],CH,False,5),([(344,236),(396,236),(396,248),(344,248)],NV,False,2),([(214,284),(250,284),(250,289),(214,289)],CY,True,2)]),
 # Montageschiene oben
 dict(t='poly',p=[(236,213),(404,213),(404,222.5),(236,222.5)],c=NV,z=(-9,9),r=1,L='Visierschiene',
      d=[([(x,215),(x+6,215),(x+6,219),(x,219)],IN,False,0) for x in range(244,400,14)]),
 # Pistolengriff
 dict(t='poly',p=[(262,299),(302,299),(292,390),(248,390)],c=NV,z=(-15,15),r=7,L='Griff',
      d=[([(266,322),(290,322),(287,346),(262,346)],IN,False,3)]),
 # Abzugbuegel (unten + vorne) und Abzug
 dict(t='poly',p=[(291,370),(340,370),(340,378),(290,378)],c=NV,z=(-5,5)),
 dict(t='poly',p=[(332,299),(340,299),(340,378),(332,378)],c=NV,z=(-5,5)),
 dict(t='poly',p=[(306,299),(314,299),(319,332),(312,334)],c=CH,z=(-3,3),L='Abzug'),
 # Energiemagazin im Schacht vor dem Abzugbuegel
 dict(t='poly',p=[(350,299),(394,299),(390,356),(354,356)],c=NV,z=(-13,13),r=5,L='Magazin',
      d=[([(360,312),(384,312),(383,318),(361,318)],CY,True,2)]),
 # Lauf zwischen zwei Schienen
 dict(t='cyl',x=(424,686),y=270,R=7,c='#3A3C55',n=16,L='Lauf'),
 dict(t='poly',p=[(424,244),(668,244),(676,251),(668,258),(424,258)],c=CH,z=(-12,12),r=3,
      d=[([(432,255),(660,255),(660,257.5),(432,257.5)],CY,True,1)]),
 dict(t='poly',p=[(424,282),(668,282),(676,289),(668,296),(424,296)],c=CH,z=(-12,12),r=3,
      d=[([(432,282.5),(660,282.5),(660,285),(432,285)],CY,True,1)]),
 dict(t='poly',p=[(492,240),(506,240),(506,300),(492,300)],c=NV,z=(-15,15),r=3),
 dict(t='poly',p=[(590,240),(604,240),(604,300),(590,300)],c=NV,z=(-15,15),r=3),
 # Muendungsbremse
 dict(t='poly',p=[(668,242),(702,246),(712,254),(712,286),(702,294),(668,298)],c=NV,z=(-15,15),r=4,L='Mündungsbremse',
      d=[([(676,256),(684,256),(684,284),(676,284)],IN,False,2),([(690,257),(698,257),(698,283),(690,283)],IN,False,2)],
      xd=[(712.4,[(270+6*__import__('math').sin(k*0.5236),6*__import__('math').cos(k*0.5236)) for k in range(12)],CY,True)]),
 # Zielfernrohr auf zwei Ringen
 dict(t='poly',p=[(256,203),(272,203),(272,213.5),(256,213.5)],c=NV,z=(-7,7),r=1,S=True),
 dict(t='poly',p=[(354,203),(370,203),(370,213.5),(354,213.5)],c=NV,z=(-7,7),r=1,S=True),
 dict(t='cyl',x=(254,274),y=191,R=14,c=CH,S=True),
 dict(t='cyl',x=(352,372),y=191,R=14,c=CH,S=True),
 dict(t='frustum',x=(206,228),y=191,R=15,R1=11.5,c=NV,S=True),
 dict(t='cyl',x=(228,392),y=191,R=11.5,c=IN,L='Zielfernrohr',S=True),
 dict(t='poly',p=[(304,172),(318,172),(318,181),(304,181)],c=NV,z=(-6,6),r=2,S=True),
 dict(t='frustum',x=(392,420),y=191,R=11.5,R1=18,c=NV,cap=[(14,CY,True)],S=True),
]
