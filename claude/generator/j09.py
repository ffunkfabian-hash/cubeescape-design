from jlib import *
BK,IC,GM,DK='#262C34','#59D0FF','#66707C','#111317'
def spec():
    return [
    # Abschussrohr als großer Facettenkasten, Leuchtkante oben
    K([(160,190),(600,190),(636,204),(636,266),(600,280),(160,280),(150,262),(150,208)],BK,-40,40,b=14,bz=14,label='Abschussrohr',
      glow=[((0,),IC,2.6)],dec=[([(220,240),(560,240),(552,254),(228,254)],DK,False)]),
    # Mündungsrahmen mit Öffnung und Raketenspitze auf der Stirnfläche
    K(rect(632,194,26,82),DK,-36,36,b=6,bz=8,label='Mündung',
      xdec=[('x+',658,[(212,-22),(212,22),(258,22),(258,-22)],'#050506',False),('x+',658.5,circ(235,0,11,8),IC,True)]),
    # Abgasdüse hinten
    T(108,152,235,44,34,DK,n=8,label='Abgasdüse'),
    X(104,109,235,40,'#050506',n=8),
    X(98,106,235,46,BK,n=8),
    K(rect(220,280,330,14),DK,-14,14,b=3,bz=3),
    K([(178,280),(244,280),(244,326),(196,326)],BK,-18,18,b=5,bz=5,label='Schulterstütze'),
    K([(300,294),(340,294),(330,390),(290,390)],DK,-16,16,b=5,bz=5,label='Griff'),
    K([(352,295),(363,295),(374,332),(364,335)],GM,-6,6,b=1.5,bz=1.5,label='Abzug'),
    K(rect(330,342,66,9),DK,-7,7,b=2,bz=2),
    K(rect(388,294,9,57),DK,-7,7,b=2,bz=2),
    K([(470,294),(502,294),(498,372),(474,372)],DK,-14,14,b=4,bz=4,label='Vordergriff'),
    # Visieraufnahme seitlich LINKS am Rohr (Sichtlinie neben dem Rohr)
    K(rect(318,208,132,26),DK,40,47,b=2,bz=2),
    K(rect(322,204,124,14),DK,47,56,b=2,bz=2,label='Visierschiene'),
    # --- Reflexvisier separat, sitzt seitlich links, Optik über der Rohroberkante
    K(rect(364,196,34,22),DK,56,64,b=2,bz=2,sight=True),
    K([(360,150),(404,150),(410,196.5),(354,196.5)],BK,56,80,b=5,bz=5,sight=True,label='Reflexvisier',
      dec=[([(368,160),(398,160),(402,186),(364,186)],IC,True)]),
    ]
META=dict(sight=('reflex','glass'),snote='seitlich links montiert',num='09',name='Raketenwerfer',nick='ICEBREAKER',col=IC,pill='KALTGRAPHIT · SIGNALEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(380,253,0),
 desc='Stealth-Raketenwerfer der Black-Ice-Serie: Das Abschussrohr ist ein großer Facettenkasten mit breiten Fasen und Leuchtkante oben, vorn sitzt der Mündungsrahmen mit dunkler Öffnung und leuchtender Raketenspitze, hinten die achtkantige Abgasdüse. Darunter Tragrahmen, Schulterstütze, Griff mit offenem Abzugbügel und Vordergriff. Das Reflexvisier ist separat und wird seitlich links montiert, damit das Rohr die Sichtlinie nicht verdeckt.',
 form='Facettenkasten-Rohr mit Leuchtkante · Mündungsrahmen mit Raketenspitze · achtkantige Abgasdüse · Tragrahmen · Schulterstütze · Griff + offener Abzugbügel · Vordergriff · Visierschiene seitlich links · Reflexvisier separat')
