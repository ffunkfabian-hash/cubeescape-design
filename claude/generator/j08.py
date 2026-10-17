from jlib import *
BK,IB,GM,DK='#30343C','#8CD8FF','#6E7581','#15171B'
def spec():
    return [
    # Skelettschaft: Kappe, Oberholm, Unterholm
    K([(62,232),(84,232),(84,324),(66,320)],DK,-16,16,b=4,bz=4,label='Schaftkappe'),
    K([(82,234),(220,248),(220,262),(82,250)],BK,-11,11,b=4,bz=4,label='Schaft',glow=[((0,),IB,1.8)]),
    K([(82,304),(220,290),(220,304),(82,320)],BK,-11,11,b=4,bz=4),
    K([(216,236),(460,236),(490,250),(490,310),(460,322),(216,322),(206,300),(206,256)],BK,-22,22,b=9,bz=9,label='Gehäuse',
      glow=[((0,),IB)],dec=[([(236,292),(330,292),(324,306),(242,306)],DK,False)]),
    K(rect(240,227.5,210,8.5),DK,-9,9,b=2,bz=2,label='Visierschiene'),
    K([(272,322),(316,322),(306,418),(262,418)],DK,-16,16,b=5,bz=5,label='Griff'),
    K([(330,323),(342,323),(354,356),(343,360)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(316,366,66,9),DK,-6,6,b=2,bz=2),
    K(rect(374,322,9,53),DK,-6,6,b=2,bz=2),
    K([(398,322),(440,322),(452,394),(412,396)],DK,-14,14,b=4,bz=4,label='Magazin',glow=[((1,),IB,2.0)]),
    K([(490,252),(660,258),(676,272),(660,298),(490,304)],BK,-16,16,b=6,bz=6,label='Laufmantel',
      dec=[([(512+24*i,266),(526+24*i,266),(520+24*i,290),(506+24*i,290)],DK,False) for i in range(5)]),
    X(676,730,278,7,GM,n=6,label='Lauf'),
    K([(724,264),(740,264),(754,278),(740,292),(724,292)],DK,-11,11,b=3.5,bz=3.5,label='Mündung',glow=[((1,2),IB,1.6)]),
    # --- Zielfernrohr mit Montageringen separat
    K(rect(298,203.5,16,24.5),DK,-11,11,b=3,bz=3,sight=True,label='Montageringe'),
    K(rect(398,203.5,16,24.5),DK,-11,11,b=3,bz=3,sight=True,label='Montageringe'),
    T(246,272,192,14,11,BK,n=8,sight=True),
    X(270,450,192,11,BK,n=8,sight=True,label='Zielfernrohr'),
    T(446,486,192,11,15,BK,n=8,sight=True),
    X(484,487,192,13,IB,n=8,emit=True,sight=True),
    ]
META=dict(sight=('scope','lens'),num='08',name='Spurgewehr',nick='PERMAFROST',col=IB,pill='GLETSCHERGRAU · FIRNBLAU · GUNMETAL',palette=[BK,IB,GM,DK],center=(408,306,0),
 desc='Stealth-Spurgewehr der Black-Ice-Serie: Skelettschaft aus zwei Facettenholmen mit Kappe, langes Facettengehäuse mit firnblauen Leuchtkanten. Magazin vor dem offenen Abzugbügel, geschlitzter Laufmantel, Sechskant-Lauf und facettierte Mündung. Zielfernrohr (Achtkant) mit Montageringen ist separat.',
 form='Skelettschaft mit Kappe · Facettengehäuse mit Leuchtkante · Visierschiene · Griff + offener Abzugbügel · Magazin im Schacht · geschlitzter Laufmantel · Sechskant-Lauf · facettierte Mündung · Zielfernrohr separat')
