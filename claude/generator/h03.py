from hlib import *
TI,PE,LG,DK='#6E747C','#0F7C80','#D7DCDF','#1A1D21'
INFO=dict(num='03',name='Impulsgewehr',nick='SPULENBANK',col=PE,pill='TITANGRAU · PETROL · HELLGRAU',pal=[TI,PE,LG,DK],center=(450,310,0),
 alt='Impulsgewehr Variante H: Bullpup-Impulsgewehr mit titangrauem Gehäuse, heller Energiezelle hinter dem Griff, offenem Abzugbügel, drei Petrol-Spulenringen auf einem Spulenträger um den sichtbaren Lauf und kantigem Emitter; Ringvisier separat gezeichnet',
 desc='Prüfstand-Prototyp: Hinter dem Griff steckt die helle Energiezelle im Schacht des titangrauen Gehäuses. Nach vorn läuft der sichtbare Lauf durch drei petrolfarbene Spulenringe, die auf einem durchgehenden Spulenträger festgeklemmt sind. Vorn bündelt ein kantiger Emitter den Impuls. Das Ringvisier wird separat auf die Schiene gesetzt.',
 form='Bullpup-Gehäuse · Energiezelle im Schacht hinter dem Griff · offener Abzugbügel · Visierschiene · Lauf mit drei Spulenringen auf Spulenträger · Emitter · Ringvisier separat')
ITEMS=[
 dict(t='poly',p=[(146,242),(162,242),(162,326),(146,322)],c=DK,z=(-20,20),r=3),
 dict(t='poly',p=[(160,236),(420,236),(436,252),(436,318),(420,330),(176,330),(160,316)],c=TI,z=(-22,22),r=4,L='Gehäuse',
      d=[([(186,250),(270,250),(270,280),(186,280)],DK,False,3),([(300,250),(400,250),(400,262),(300,262)],DK,False,2)]+screws([(174,250),(174,316),(424,262),(424,306)],DK)),
 # Energiezelle hinter dem Griff
 dict(t='poly',p=[(200,326),(272,326),(272,380),(200,380)],c=LG,z=(-17,17),r=3,L='Energiezelle',
      d=[([(212,338),(260,338),(260,350),(212,350)],PE,True,2),([(212,360),(260,360),(260,366),(212,366)],TI,False,1)]),
 # Griff, Abzugbuegel, Abzug
 dict(t='poly',p=[(292,328),(340,328),(332,426),(320,436),(296,436),(288,426)],c=DK,z=(-16,16),r=5,L='Griff'),
 dict(t='poly',p=[(342,374),(394,374),(394,384),(342,384)],c=DK,z=(-6,6),r=2),
 dict(t='poly',p=[(384,326),(394,326),(394,384),(384,384)],c=DK,z=(-6,6),r=1),
 dict(t='poly',p=[(350,329),(362,329),(374,362),(363,366)],c=LG,z=(-5,5),r=1,L='Abzug'),
 # Visierschiene
 dict(t='poly',p=[(200,228),(404,228),(404,236.5),(200,236.5)],c=DK,z=(-9,9),r=1,L='Visierschiene',d=slots(206,400,12,230,6,4,TI)),
 # Lauf
 dict(t='cyl',x=(436,704),y=280,R=8,c='#3A3F46',n=16,L='Lauf'),
 # Spulentraeger unter dem Lauf (verbindet Ringe mit Gehaeuse)
 dict(t='poly',p=[(436,300),(664,300),(664,312),(436,312)],c=TI,z=(-6,6),r=2,d=screws([(452,306),(648,306)],DK,2.4)),
 dict(t='torus',x=480,y=280,R=24,rt=5,c=PE,L='Spulenringe'),
 dict(t='torus',x=550,y=280,R=24,rt=5,c=PE,L='Spulenringe'),
 dict(t='torus',x=620,y=280,R=24,rt=5,c=PE,L='Spulenringe'),
 # Emitter
 dict(t='poly',p=[(700,262),(736,262),(748,272),(748,288),(736,298),(700,298)],c=TI,z=(-15,15),r=3,L='Emitter',
      d=slots(710,730,9,268,4,8,DK),xd=bore(748,280,7,PE)),
 # --- Ringvisier (separat)
 dict(t='poly',p=[(256,214),(326,214),(326,228.5),(256,228.5)],c=DK,z=(-10,10),r=2,S=True,L='Ringvisier'),
 dict(t='poly',p=[(260,196),(276,196),(276,214.5),(260,214.5)],c=TI,z=(-6,6),r=2,S=True,L='Ringvisier',d=[(circlep(268,203,3),DK,False,0)]),
 dict(t='poly',p=[(306,198),(318,198),(318,214.5),(306,214.5)],c=TI,z=(-4,4),r=1,S=True),
 dict(t='torus',x=312,y=184,R=14,rt=3,c=PE,S=True),
]
