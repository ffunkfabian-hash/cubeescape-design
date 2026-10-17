BG,SW,OR,WH='#D9CBB0','#1B1C1F','#E8661C','#F4F2EC'
import math
INFO=dict(num='02',name='Sturmgewehr',nick='KANTENLÄUFER',col=OR,pill='BEIGE · SCHWARZ · ORANGE',pal=[BG,SW,OR,WH],center=(420,300,0),
 alt='Sturmgewehr Variante G: kantiges Sturmgewehr in Beige und Schwarz mit Keilschaft, Reflexvisier auf Schiene, nach vorn geneigtem weißem Magazin, sichtbarem Abzugbügel, Handschutz mit Würfel-Lüftung und Mündungsfeuerdämpfer',
 desc='Ein kantiges Sturmgewehr aus abgeschrägten Modulen: Keilschaft, beiges Gehäuse mit Magazinschacht, schwarzer Handschutz mit quadratischen Lüftungsöffnungen. Das Reflexvisier sitzt auf der durchgehenden Schiene, das weiße Magazin steckt leicht nach vorn geneigt im Schacht.',
 form='Keilschaft mit Wangenauflage · abgeschrägtes Gehäuse mit Magazinschacht · Reflexvisier auf Schiene · Pistolengriff mit Abzugbügel · Handschutz mit Würfel-Lüftung · Lauf mit Feuerdämpfer')
ITEMS=[
 # Schaft
 dict(t='poly',p=[(80,236),(100,232),(106,244),(106,324),(100,336),(80,332)],c=SW,z=(-16,16),r=4,L='Schaft'),
 dict(t='poly',p=[(104,236),(232,244),(232,300),(104,328)],c=BG,z=(-13,13),r=5),
 # Wangenauflage als echtes Bauteil auf dem Schaftruecken
 dict(t='poly',p=[(122,226),(204,231),(204,244),(122,239)],c=SW,z=(-10,10),r=3),
 # Griff
 dict(t='poly',p=[(292,298),(338,298),(326,392),(312,404),(274,404),(270,392)],c=SW,z=(-15,15),r=6,L='Griff',
      d=[([(284,318),(324,318),(316,384),(280,384)],'#2A2B30',False,4)]),
 # Abzugbuegel und Abzug
 dict(t='poly',p=[(328,350),(400,350),(400,360),(328,360)],c=SW,z=(-5,5),r=2),
 dict(t='poly',p=[(390,299),(400,299),(400,360),(390,360)],c=SW,z=(-5,5),r=1),
 dict(t='poly',p=[(352,299),(364,299),(372,334),(362,337)],c=OR,z=(-4,4),r=1,L='Abzug'),
 # Magazin (nach vorn geneigt) im Schacht
 dict(t='poly',p=[(412,300),(452,300),(472,388),(432,396)],c=WH,z=(-13,13),r=4,L='Magazin',
      d=[([(424,320),(450,320),(456,346),(430,348)],BG,False,3)]),
 dict(t='poly',p=[(404,294),(460,294),(464,314),(406,314)],c=BG,z=(-17,17),r=2),
 # Gehaeuse
 dict(t='poly',p=[(228,228),(452,228),(472,246),(472,300),(256,300),(228,280)],c=BG,z=(-22,22),r=6,L='Gehäuse',
      d=[([(330,242),(392,242),(392,258),(330,258)],SW,False,2),([(250,262),(262,262),(262,272),(250,272)],OR,False,2)]),
 # Schiene und Reflexvisier
 dict(t='poly',p=[(240,219),(462,219),(462,228.5),(240,228.5)],c=SW,z=(-9,9),r=1,
      d=[([(x,221),(x+6,221),(x+6,225),(x,225)],'#33343A',False,0) for x in range(248,456,14)]),
 dict(t='poly',p=[(330,207),(392,207),(392,219.5),(330,219.5)],c=SW,z=(-10,10),r=2,S=True),
 dict(t='poly',p=[(338,176),(384,176),(392,186),(392,207.5),(338,207.5)],c=SW,z=(-11,11),r=3,L='Reflexvisier',S=True,
      d=[([(346,184),(380,184),(384,190),(384,200),(346,200)],'#3B4A52',False,2)],
      xd=[(392.4,[(190,-7),(203,-7),(203,7),(190,7)],'#3B4A52',False),(392.8,[(195,-1.6),(198,-1.6),(198,1.6),(195,1.6)],OR,True)]),
 # Handschutz mit Wuerfel-Lueftung
 dict(t='poly',p=[(470,236),(628,236),(640,248),(640,292),(628,300),(470,300)],c=SW,z=(-18,18),r=6,L='Handschutz',
      d=[([(x,y),(x+16,y),(x+16,y+16),(x,y+16)],BG,False,2) for x in range(492,620,30) for y in (250,272)]),
 dict(t='poly',p=[(612,232),(632,232),(632,236.5),(612,236.5)],c=SW,z=(-6,6),r=1),
 dict(t='poly',p=[(616,220),(628,220),(628,232.5),(616,232.5)],c=SW,z=(-4,4),r=1,L='Korn',S=True),
 # Lauf und Feuerdaempfer
 dict(t='cyl',x=(638,702),y=268,R=8,c='#3A3C42',n=16,L='Lauf'),
 dict(t='poly',p=[(698,254),(740,254),(748,260),(748,276),(740,282),(698,282)],c=SW,z=(-14,14),r=3,L='Mündung',
      d=[([(708,259),(724,259),(724,263),(708,263)],BG,False,1),([(708,273),(724,273),(724,277),(708,277)],BG,False,1)],
      xd=[(748.4,[(268+6*math.sin(k*0.5236),6*math.cos(k*0.5236)) for k in range(12)],'#0A0A0D',False)]),
]
