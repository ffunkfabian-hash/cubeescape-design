from hlib import *
OL,WO,SA,DK='#6B6F5A','#FF6A13','#C9C1A5','#1E2019'
INFO=dict(num='04',name='Schrotflinte',nick='WERKBANK',col=WO,pill='OLIVGRAU · WARNORANGE · SAND',pal=[OL,WO,SA,DK],center=(420,300,0),
 alt='Schrotflinte Variante H: Pump-Schrotflinte mit sandfarbenem Schaft und Wangenauflage, olivgrauem Gehäuse mit Patronenfenster, offenem Abzugbügel, sichtbarem Lauf mit Hitzeschild, Röhrenmagazin darunter, orangem Pumpgriff, Laufklemme und orangem Choke; Lochvisier separat gezeichnet',
 desc='Werkbank-Pumpgun: Der sandfarbene Schaft trägt eine aufgesetzte Wangenauflage, das olivgraue Gehäuse zeigt im Patronenfenster die Ladung. Darunter hängen Abzug und Bügel gut sichtbar. Lauf und Röhrenmagazin werden vorn von einer Laufklemme zusammengehalten, der orange Pumpgriff läuft auf dem Magazin. Das Lochvisier ist ein separates Schienenmodul.',
 form='Schaft mit Wangenauflage · Gehäuse mit Patronenfenster · Visierschiene · offener Abzugbügel · Lauf mit Hitzeschild · Röhrenmagazin · Pumpgriff · Laufklemme · Choke · Lochvisier separat')
ITEMS=[
 dict(t='poly',p=[(106,262),(120,262),(120,342),(106,342)],c=DK,z=(-17,17),r=3),
 dict(t='poly',p=[(120,262),(250,250),(250,316),(150,340),(120,340)],c=SA,z=(-16,16),r=4,L='Schaft'),
 dict(t='poly',p=[(150,246),(232,240),(232,253),(150,261)],c=OL,z=(-10,10),r=3),
 dict(t='poly',p=[(250,240),(420,240),(430,250),(430,320),(250,320)],c=OL,z=(-20,20),r=3,L='Gehäuse',
      d=[([(300,262),(390,262),(390,290),(300,290)],DK,False,3),([(308,268),(352,268),(352,284),(308,284)],WO,False,6)]+screws([(262,252),(418,252),(262,308),(418,308)],DK)),
 dict(t='poly',p=[(268,318),(316,318),(306,412),(294,420),(272,420),(262,410)],c=DK,z=(-15,15),r=5,L='Griff'),
 dict(t='poly',p=[(320,364),(382,364),(382,374),(320,374)],c=DK,z=(-6,6),r=2),
 dict(t='poly',p=[(372,318),(382,318),(382,374),(372,374)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(332,319),(344,319),(356,352),(345,356)],c=WO,z=(-5,5),r=1,L='Abzug'),
 dict(t='poly',p=[(270,232),(412,232),(412,240.5),(270,240.5)],c=DK,z=(-9,9),r=1,d=slots(276,408,12,234,6,4,OL)),
 dict(t='cyl',x=(430,700),y=262,R=11,c='#3A3C34',n=18,L='Lauf'),
 dict(t='poly',p=[(440,244),(640,244),(640,251.5),(440,251.5)],c=SA,z=(-9,9),r=1,d=slots(448,636,14,246,8,3,DK)),
 dict(t='cyl',x=(430,660),y=296,R=10,c='#53574A',n=18,L='Röhrenmagazin'),
 dict(t='poly',p=[(520,282),(600,282),(606,288),(606,312),(600,318),(520,318),(514,312),(514,288)],c=WO,z=(-14,14),r=3,L='Pumpgriff',
      d=slots(526,598,10,286,5,28,'#C9500F')),
 dict(t='poly',p=[(650,246),(666,246),(666,310),(650,310)],c=OL,z=(-13,13),r=2,d=screws([(658,254),(658,302)],DK,2.4)),
 dict(t='cyl',x=(700,732),y=262,R=13,c=WO,n=18,L='Mündung',cap=[(7,'#0A0A0D',False)]),
 # --- Lochvisier (separat)
 dict(t='poly',p=[(298,220),(352,220),(352,232.5),(298,232.5)],c=DK,z=(-10,10),r=2,S=True,L='Lochvisier'),
 dict(t='poly',p=[(316,196),(334,196),(334,220.5),(316,220.5)],c=OL,z=(-4,4),r=2,S=True,L='Lochvisier',d=[(circlep(325,205,3.5),DK,False,0)]),
 dict(t='poly',p=[(310,190),(340,190),(340,220.5),(310,220.5)],c=WO,z=(6,10),r=3,S=True),
 dict(t='poly',p=[(310,190),(340,190),(340,220.5),(310,220.5)],c=WO,z=(-10,-6),r=3,S=True),
]
