from hlib import *
KB,CU,ST,DK='#2F4FA8','#C87533','#8E969F','#171A22'
INFO=dict(num='02',name='Sturmgewehr',nick='KLEMMSCHIENE',col=CU,pill='KOBALT · KUPFER · STAHL',pal=[KB,CU,ST,DK],center=(460,320,0),
 alt='Sturmgewehr Variante H: modulares Sturmgewehr mit kobaltblauem Oberteil, stahlgrauem Unterteil, zwei Kupfer-Klemmbändern, Rohrschaft mit Wangenauflage, Magazin vor dem Abzugbügel, gelochtem Handschutz mit Kupferklemme, sichtbarem Lauf und Kupfer-Mündung; Holovisier separat gezeichnet',
 desc='Werkstatt-Prototyp aus Modulen: Ein kobaltblaues Oberteil sitzt auf einem stahlgrauen Unterteil, zwei Kupfer-Klemmbänder halten beide zusammen. Der Rohrschaft trägt eine echte Wangenauflage, der gelochte Handschutz ist mit einer Kupferklemme angesetzt. Abzug und Bügel hängen sichtbar unter dem Gehäuse, das Magazin steckt davor im Schacht. Das Holovisier ist ein separates Schienenmodul.',
 form='Rohrschaft mit Wangenauflage · Oberteil + Unterteil mit Kupfer-Klemmbändern · Visierschiene · Magazin im Schacht · gelochter Handschutz · sichtbarer Lauf · Kupfer-Mündung · Holovisier separat')
ITEMS=[
 # Schaft: Schaftkappe, Schaftrohr, Strebe, Wangenauflage
 dict(t='poly',p=[(118,248),(136,248),(136,352),(118,348)],c=DK,z=(-17,17),r=3),
 dict(t='cyl',x=(134,252),y=272,R=10,c=ST,n=16,L='Schaft'),
 dict(t='poly',p=[(134,334),(252,302),(252,316),(134,350)],c=DK,z=(-9,9),r=2),
 dict(t='poly',p=[(160,250),(232,250),(232,263),(160,263)],c=KB,z=(-11,11),r=3),
 # Unterteil
 dict(t='poly',p=[(250,280),(510,280),(510,322),(500,332),(260,332),(250,322)],c=ST,z=(-20,20),r=3,
      d=screws([(262,292),(498,292)],DK)),
 # Oberteil
 dict(t='poly',p=[(240,236),(480,236),(492,248),(492,280.5),(240,280.5)],c=KB,z=(-22,22),r=3,L='Gehäuse',
      d=[([(340,248),(400,248),(400,264),(340,264)],DK,False,2)]+screws([(252,248),(468,248)],DK)),
 # Kupfer-Klemmbaender um Ober- und Unterteil
 dict(t='poly',p=[(300,232),(316,232),(316,336),(300,336)],c=CU,z=(-24,24),r=2,d=screws([(308,244),(308,324)],DK,2.6)),
 dict(t='poly',p=[(420,232),(436,232),(436,336),(420,336)],c=CU,z=(-24,24),r=2,d=screws([(428,244),(428,324)],DK,2.6)),
 # Visierschiene auf dem Oberteil
 dict(t='poly',p=[(250,228),(478,228),(478,236.5),(250,236.5)],c=DK,z=(-9,9),r=1,L='Visierschiene',d=slots(256,474,12,230,6,4,ST)),
 # Griff
 dict(t='poly',p=[(332,330),(382,330),(372,428),(360,438),(328,438),(322,428)],c=DK,z=(-16,16),r=5,L='Griff',
      d=[([(336,346),(372,346),(366,414),(334,414)],'#262A33',False,4)]),
 # Abzugbuegel und Abzug
 dict(t='poly',p=[(384,372),(446,372),(446,382),(384,382)],c=DK,z=(-6,6),r=2),
 dict(t='poly',p=[(436,330),(446,330),(446,382),(436,382)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(398,331),(410,331),(422,362),(411,366)],c=CU,z=(-5,5),r=1,L='Abzug'),
 # Magazin im Schacht + Bodenplatte
 dict(t='poly',p=[(452,330),(494,330),(504,428),(462,432)],c=ST,z=(-15,15),r=3,L='Magazin',
      d=[([(462,346),(488,346),(494,412),(468,414)],'#7A828B',False,3)]),
 dict(t='poly',p=[(460,428),(506,424),(508,438),(462,442)],c=CU,z=(-16,16),r=2),
 # Handschutz mit Kupferklemme
 dict(t='poly',p=[(492,244),(690,244),(700,254),(700,300),(690,310),(492,310)],c=ST,z=(-18,18),r=4,
      d=slots(516,690,22,262,14,10,DK)+slots(516,690,22,284,14,10,DK)),
 dict(t='poly',p=[(490,240),(508,240),(508,314),(490,314)],c=CU,z=(-20,20),r=2,d=screws([(499,252),(499,302)],DK,2.6)),
 # Lauf und Muendung
 dict(t='cyl',x=(700,760),y=277,R=9,c='#4A5058',n=16,L='Lauf'),
 dict(t='poly',p=[(752,262),(790,262),(798,270),(798,284),(790,292),(752,292)],c=CU,z=(-13,13),r=3,L='Mündung',
      d=slots(762,786,10,266,5,8,DK),xd=bore(798,277,6)),
 # --- Holovisier (separat)
 dict(t='poly',p=[(334,214),(406,214),(406,228.5),(334,228.5)],c=DK,z=(-11,11),r=2,S=True,L='Holovisier',d=screws([(344,221),(396,221)],ST,2.3)),
 dict(t='poly',p=[(342,176),(398,176),(406,186),(406,214.5),(334,214.5),(334,186)],c=KB,z=(-13,13),r=4,S=True,L='Holovisier',
      d=[([(344,186),(396,186),(396,206),(344,206)],DK,False,3),([(348,190),(392,190),(392,202),(348,202)],'#8FD3F4',False,2)]),
]
