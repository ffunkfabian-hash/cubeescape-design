WH,AN,CY,BE='#F2F2EE','#33363C','#38D6E8','#CFC3A8'
INFO=dict(num='03',name='Impulsgewehr',nick='PULSWÜRFEL',col=CY,pill='WEISS · ANTHRAZIT · CYAN',pal=[WH,AN,CY,BE],center=(410,300,0),
 alt='Impulsgewehr Variante G: weißes Impulsgewehr mit offenem Käfig, in dem ein leuchtender Cyan-Würfel zwischen zwei Achsen gehalten wird, gestuftem Emitter aus Blöcken, Visier, Energiezelle und sichtbarem Abzugbügel',
 desc='Das Herz der Waffe ist ein leuchtender Pulswürfel, der offen in einem Käfig zwischen zwei Achsen sitzt. Davor verjüngt sich der Emitter in drei gestuften Blöcken bis zur quadratischen Mündung. Unter dem Käfig steckt die Energiezelle, dahinter Griff und Abzug.',
 form='Weißes Hinterteil mit Schaft · offener Käfig mit Pulswürfel auf Achsen · gestufter Block-Emitter · quadratische Mündung · Energiezelle unter dem Käfig · Visier auf Schiene')
ITEMS=[
 # Schaft
 dict(t='poly',p=[(120,240),(146,236),(146,316),(120,312)],c=AN,z=(-15,15),r=4,L='Schaft'),
 dict(t='poly',p=[(144,240),(250,246),(250,290),(144,312)],c=WH,z=(-14,14),r=5,
      d=[([(162,256),(232,258),(232,264),(162,262)],BE,False,2)]),
 # Griff, Abzugbuegel, Abzug
 dict(t='poly',p=[(278,302),(318,302),(308,392),(296,404),(262,404),(258,392)],c=AN,z=(-15,15),r=6,L='Griff'),
 dict(t='poly',p=[(306,352),(378,352),(378,362),(306,362)],c=AN,z=(-5,5),r=2),
 dict(t='poly',p=[(368,303),(378,303),(378,362),(368,362)],c=AN,z=(-5,5),r=1),
 dict(t='poly',p=[(326,303),(344,303),(356,342),(340,347)],c=CY,z=(-5,5),r=2,L='Abzug'),
 # Hinteres Gehaeuse
 dict(t='poly',p=[(248,226),(372,226),(372,304),(268,304),(248,288)],c=WH,z=(-24,24),r=8,L='Gehäuse',
      d=[([(262,250),(356,250),(356,256),(262,256)],AN,False,2),([(340,272),(356,272),(356,282),(340,282)],CY,True,2)]),
 # Schiene und Visier
 dict(t='poly',p=[(270,217),(350,217),(350,226.5),(270,226.5)],c=AN,z=(-8,8),r=1),
 dict(t='poly',p=[(290,198),(336,198),(342,206),(342,217.5),(290,217.5)],c=AN,z=(-10,10),r=3,L='Visier',S=True,
      xd=[(342.4,[(208,-5),(215,-5),(215,5),(208,5)],CY,True)]),
 # Kaefig
 # schlanke Kaefigstreben (je 2 oben/unten) mit Querstegen fuer die Wuerfelachsen
 dict(t='cyl',x=(370,486),y=231,R=4.5,zc=18,c=AN,n=12,L='Käfig'),
 dict(t='cyl',x=(370,486),y=231,R=4.5,zc=-18,c=AN,n=12),
 dict(t='cyl',x=(370,486),y=299,R=4.5,zc=18,c=AN,n=12),
 dict(t='cyl',x=(370,486),y=299,R=4.5,zc=-18,c=AN,n=12),
 dict(t='poly',p=[(422,227),(434,227),(434,238),(422,238)],c=AN,z=(-21,21),r=1),
 dict(t='poly',p=[(422,292),(434,292),(434,303),(422,303)],c=AN,z=(-21,21),r=1),
 dict(t='poly',p=[(484,226),(500,226),(500,304),(484,304)],c=AN,z=(-24,24),r=3),
 # Achsen und Pulswuerfel
 dict(t='poly',p=[(424,237),(432,237),(432,246),(424,246)],c=BE,z=(-4,4)),
 dict(t='poly',p=[(424,284),(432,284),(432,293),(424,293)],c=BE,z=(-4,4)),
 dict(t='poly',p=[(408,245),(448,245),(448,285),(408,285)],c=CY,z=(-20,20),r=2,e=True,L='Pulswürfel'),
 # Energiezelle unter dem Kaefig
 dict(t='poly',p=[(392,303),(452,303),(448,348),(396,348)],c=BE,z=(-14,14),r=4,L='Energiezelle',
      d=[([(404,318),(440,318),(438,326),(406,326)],CY,True,2)]),
 # Gestufter Emitter
 dict(t='poly',p=[(498,236),(560,236),(560,296),(498,296)],c=WH,z=(-20,20),r=4,
      d=[([(508,262),(550,262),(550,270),(508,270)],AN,False,2)]),
 dict(t='poly',p=[(558,242),(612,242),(612,290),(558,290)],c=AN,z=(-16,16),r=3),
 dict(t='poly',p=[(610,248),(660,248),(660,284),(610,284)],c=WH,z=(-12,12),r=3),
 dict(t='poly',p=[(658,252),(690,252),(690,280),(658,280)],c=AN,z=(-10,10),r=2,L='Mündung',
      xd=[(690.4,[(259,-6),(273,-6),(273,6),(259,6)],CY,True)]),
]
