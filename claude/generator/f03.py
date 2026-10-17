AN,SI,LI,SW='#26292E','#B8BEC6','#C6F432','#121417'
INFO=dict(num='03',name='Impulsgewehr',nick='DREIZACK',col=LI,pill='ANTHRAZIT · SILBER · LIMETTE',pal=[AN,SI,LI,SW],center=(380,320,0),
 alt='Impulsgewehr Variante F: rundes Silbergehäuse mit leuchtender Limetten-Energiekugel oben und drei Zinken vorne, von zwei Ringen gebündelt',
 desc='Der Impuls wird in einer offen sichtbaren Limetten-Energiekugel geladen. Vorne stehen drei Zinken nebeneinander wie bei einem Dreizack; zwei Ringe fassen die äußeren Zinken, der Mittelzinken feuert den Impuls. Das Reflexvisier sitzt modular auf der Schiene und ist separat gezeichnet.',
 form='Energiekugel in zwei Halterungen oben · drei Zinken nebeneinander (Dreizack) · zwei Bündelringe fassen die äußeren Zinken · Visierschiene, Visier separat · Griff mit Abzugbügel')
ITEMS=[
 dict(t='poly',p=[(90,250),(180,240),(190,250),(190,330),(110,340),(90,320)],c=AN,z=(-18,18),r=12,L='Schaft',d=[([(96,300),(186,292),(186,300),(98,308)],SW,False,2)]),
 dict(t='poly',p=[(180,228),(420,228),(440,248),(440,320),(400,340),(200,340),(180,320)],c=SI,z=(-30,30),r=18,L='Gehäuse',
      d=[([(210,256),(380,256),(380,302),(210,302)],SW,False,10),([(224,274),(366,274),(366,284),(224,284)],LI,True,4),([(396,262),(420,262),(420,272),(396,272)],SW,False,2),([(396,284),(420,284),(420,294),(396,294)],SW,False,2)]),
 dict(t='poly',p=[(262,200),(272,200),(276,232),(258,232)],c=AN,z=(-8,8),r=3),
 dict(t='poly',p=[(328,200),(338,200),(342,232),(324,232)],c=AN,z=(-8,8),r=3),
 dict(t='sphere',p=(300,208,0),R=28,c=LI,e=True,L='Energiekugel'),
 dict(t='poly',p=[(250,340),(300,340),(290,430),(244,430)],c=SW,z=(-18,18),r=10,L='Griff'),
 dict(t='poly',p=[(292,404),(360,402),(360,410),(291,412)],c=SW,z=(-4,4)),
 dict(t='poly',p=[(352,338),(360,338),(360,410),(352,410)],c=SW,z=(-4,4)),
 dict(t='poly',p=[(312,338),(324,338),(330,368),(320,370)],c=SI,z=(-6,6),L='Abzug'),
 dict(t='cyl',x=(440,640),y=284,R=12,c=SW,L='Zinken'),
 dict(t='frustum',x=(640,676),y=284,R=12,R1=3,c=LI,e=True),
 # aeussere Zinken links und rechts neben dem Mittelzinken (Dreizack in der Waagerechten)
 dict(t='poly',p=[(440,277),(604,277),(630,284),(604,291),(440,291)],c=SI,z=(22,38),r=3,L='Zinken'),
 dict(t='poly',p=[(440,277),(604,277),(630,284),(604,291),(440,291)],c=SI,z=(-38,-22),r=3,L='Zinken'),
 dict(t='torus',x=500,y=284,R=42,rt=4.5,c=AN,L='Bündelring'),
 dict(t='torus',x=572,y=284,R=42,rt=4.5,c=LI,e=True,L='Bündelring'),
 # Visierschiene vorne auf dem Gehaeuse
 dict(t='poly',p=[(352,221),(418,221),(418,228.5),(352,228.5)],c=SW,z=(-9,9),r=1,L='Visierschiene',
      d=[([(x,222.5),(x+6,222.5),(x+6,226),(x,226)],AN,False,0) for x in range(358,414,12)]),
 # Reflexvisier (separat gezeichnet)
 dict(t='poly',p=[(366,213),(406,213),(406,221.5),(366,221.5)],c=AN,z=(-7,7),r=1,S=True),
 dict(t='poly',p=[(358,195),(404,195),(414,203),(414,214),(358,214)],c=AN,z=(-9,9),r=3,L='Visier',S=True,
      xd=[(414.3,[(205+4.5*__import__('math').sin(k*0.5236),4.5*__import__('math').cos(k*0.5236)) for k in range(12)],LI,True)]),
]
