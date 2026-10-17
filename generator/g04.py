OR,AN,CR,DK='#EE7B22','#26282C','#EFE6D2','#141518'
import math
INFO=dict(num='04',name='Schrotflinte',nick='BLOCKBRECHER',col=OR,pill='ORANGE · ANTHRAZIT · CREME',pal=[OR,AN,CR,DK],center=(415,300,0),
 alt='Schrotflinte Variante G: orange Halbautomatik-Schrotflinte mit Keilschaft, Gehäuse mit Patronen-Sichtfenster, Kastenmagazin, Abzugbügel, anthrazitfarbenem Laufmantel und breiter Schlitz-Mündung',
 desc='Eine wuchtige Halbautomatik-Schrotflinte: Das orange Gehäuse zeigt im Sichtfenster die geladenen Patronen, das Kastenmagazin steckt vor dem Abzugbügel. Der kurze Lauf führt aus dem flachen Laufmantel in eine breite Schlitz-Mündung, die die Schrotgarbe waagerecht auffächert.',
 form='Keilschaft · Gehäuse mit Patronen-Sichtfenster · Pistolengriff mit Abzugbügel · Kastenmagazin im Schacht · flacher Laufmantel mit Lüftungsschlitzen · breite Schlitz-Mündung · Lochvisier')
ITEMS=[
 # Schaft
 dict(t='poly',p=[(90,232),(112,228),(118,240),(118,326),(112,338),(90,334)],c=AN,z=(-17,17),r=4,L='Schaft'),
 dict(t='poly',p=[(116,236),(236,244),(236,298),(116,330)],c=OR,z=(-14,14),r=5),
 # Wangenauflage als echtes Bauteil
 dict(t='poly',p=[(132,227),(214,232),(214,246),(132,241)],c=CR,z=(-10,10),r=3),
 # Griff, Abzugbuegel, Abzug
 dict(t='poly',p=[(296,306),(340,306),(328,396),(314,408),(276,408),(272,396)],c=AN,z=(-16,16),r=6,L='Griff',
      d=[([(286,326),(326,326),(318,388),(282,388)],DK,False,4)]),
 dict(t='poly',p=[(330,356),(402,356),(402,366),(330,366)],c=AN,z=(-5,5),r=2),
 dict(t='poly',p=[(392,307),(402,307),(402,366),(392,366)],c=AN,z=(-5,5),r=1),
 dict(t='poly',p=[(350,307),(368,307),(380,346),(364,351)],c=CR,z=(-5,5),r=2,L='Abzug'),
 # Kastenmagazin im Schacht
 dict(t='poly',p=[(412,306),(470,306),(466,392),(416,392)],c=AN,z=(-15,15),r=5,L='Magazin',
      d=[([(426,326),(456,326),(455,334),(427,334)],CR,False,2),([(426,342),(456,342),(455,350),(427,350)],CR,False,2)]),
 dict(t='poly',p=[(406,300),(476,300),(476,318),(406,318)],c=OR,z=(-18,18),r=2),
 # Gehaeuse mit Patronen-Sichtfenster
 dict(t='poly',p=[(234,226),(470,226),(486,240),(486,308),(250,308),(234,292)],c=OR,z=(-26,26),r=8,L='Gehäuse',
      d=[([(300,250),(424,250),(424,278),(300,278)],DK,False,3)]+[([(306+k*24,254),(324+k*24,254),(324+k*24,274),(306+k*24,274)],CR,False,2) for k in range(5)]),
 # Schiene und Lochvisier
 dict(t='poly',p=[(250,217),(468,217),(468,226.5),(250,226.5)],c=AN,z=(-9,9),r=1),
 dict(t='poly',p=[(256,198),(282,198),(282,217.5),(256,217.5)],c=AN,z=(-10,10),r=4,L='Visier',S=True,
      d=[([(264,203),(274,203),(274,211),(264,211)],DK,False,3)]),
 # Laufmantel, Lauf, Schlitz-Muendung
 dict(t='poly',p=[(484,238),(662,238),(676,250),(676,282),(662,294),(484,294)],c=AN,z=(-20,20),r=6,L='Laufmantel',
      d=[([(506+k*36,250),(528+k*36,250),(528+k*36,260),(506+k*36,260)],OR,False,2) for k in range(4)]),
 dict(t='cyl',x=(674,722),y=266,R=13,c='#3A3C42',n=18,L='Lauf'),
 dict(t='poly',p=[(718,244),(752,248),(760,256),(760,276),(752,284),(718,288)],c=OR,z=(-22,22),r=4,L='Mündung',
      xd=[(760.4,[(261,-16),(271,-16),(271,16),(261,16)],DK,False)]),
 dict(t='poly',p=[(728,244),(748,244),(748,249),(728,249)],c=AN,z=(-6,6),r=1),
 dict(t='poly',p=[(732,232),(744,232),(744,244.5),(732,244.5)],c=AN,z=(-4,4),r=1,L='Korn',S=True),
]
