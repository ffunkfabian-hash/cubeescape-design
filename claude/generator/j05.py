from jlib import *
BK,VI,GM,DK='#1E2230','#A9A2FF','#5B6074','#0E1018'
def spec():
    return [
    # Keilschaft mit Aussparung, Wangenauflage oben
    K([(100,240),(130,236),(262,252),(262,306),(130,330),(104,340),(100,320)],BK,-14,14,b=6,bz=5,label='Schaft',
      dec=[([(140,262),(236,270),(236,294),(140,310)],DK,False)]),
    K([(146,225),(236,233),(236,249),(146,238)],DK,-10,10,b=3,bz=3,label='Wangenauflage'),
    K([(258,236),(480,236),(500,250),(500,310),(480,318),(258,318)],BK,-20,20,b=8,bz=8,label='Gehäuse',glow=[((0,),VI)]),
    # Kammerstängel links (z+)
    K(rect(300,256,10,26),DK,20,30,b=2,bz=2),
    K([(298,282),(312,282),(316,290),(312,298),(298,298),(294,290)],GM,20,34,b=2,bz=2),
    K(rect(270,227.5,210,8.5),DK,-9,9,b=2,bz=2,label='Visierschiene'),
    K([(300,318),(346,318),(336,416),(292,416)],DK,-15,15,b=5,bz=5,label='Griff'),
    K([(360,319),(372,319),(384,352),(373,356)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(350,364,58,9),DK,-6,6,b=2,bz=2),
    K(rect(400,318,9,55),DK,-6,6,b=2,bz=2),
    K([(414,318),(456,318),(460,386),(418,386)],DK,-14,14,b=4,bz=4,label='Magazin',glow=[((1,),VI,2.0)]),
    K([(500,250),(670,256),(684,270),(670,300),(500,306)],BK,-16,16,b=6,bz=6,label='Handschutz',
      dec=[([(526+24*i,266),(540+24*i,266),(534+24*i,290),(520+24*i,290)],DK,False) for i in range(5)]),
    X(684,800,278,7,GM,n=6,label='Lauf'),
    K([(792,262),(822,262),(838,278),(822,294),(792,294)],DK,-12,12,b=4,bz=4,label='Mündungsbremse',glow=[((1,2),VI,1.8)],
      dec=[(rect(798+8*i,268,4,20),'#05060A',False) for i in range(3)]),
    # --- Zielfernrohr mit Montageringen separat (Achtkant)
    K(rect(318,203.5,18,24.5),DK,-12,12,b=3,bz=3,sight=True,label='Montageringe'),
    K(rect(420,203.5,18,24.5),DK,-12,12,b=3,bz=3,sight=True,label='Montageringe'),
    T(254,282,191,15,12,BK,n=8,sight=True),
    X(280,480,191,12,BK,n=8,sight=True,label='Zielfernrohr'),
    K(rect(372,172,18,8),VI,-5,5,b=1.5,bz=1.5,sight=True),
    T(476,520,191,12,17,BK,n=8,sight=True),
    X(518,521,191,15,VI,n=8,emit=True,sight=True),
    ]
META=dict(sight=('scope','lens'),num='05',name='Scharfschützengewehr',nick='LONG NIGHT',col=VI,pill='MITTERNACHT · POLARVIOLETT · GUNMETAL',palette=[BK,VI,GM,DK],center=(470,300,0),
 desc='Stealth-Präzisionsgewehr der Black-Ice-Serie: Keilschaft mit Aussparung und Wangenauflage, langes Facettengehäuse mit polarvioletter Leuchtkante und Kammerstängel links. Der Handschutz trägt schräge Schlitze, der Sechskant-Lauf endet in einer facettierten Mündungsbremse. Magazin vor dem offenen Abzugbügel. Zielfernrohr (Achtkant) und Montageringe sind separat.',
 form='Keilschaft mit Wangenauflage · Facettengehäuse mit Leuchtkante · Kammerstängel links · Visierschiene · Griff + offener Abzugbügel · Magazin im Schacht · geschlitzter Handschutz · Sechskant-Lauf · facettierte Mündungsbremse · Zielfernrohr separat')
