from jlib import *
BK,IC,GM,DK='#252A33','#6FDCFF','#5A6370','#121418'
def spec():
    return [
    # Griff: schräg nach hinten, zwei große Facetten
    K([(248,300),(318,300),(306,432),(240,432),(232,410)],BK,-18,18,label='Griff',
      dec=[([(258,330),(300,330),(292,404),(250,404)],DK,False)]),
    K([(236,430),(310,430),(312,458),(232,458)],DK,-19,19,b=4,bz=5,label='Magazin',glow=[((0,),IC,2.0)]),
    # Abzug, Bügel
    K([(338,302),(352,302),(366,342),(354,346)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K([(318,352),(404,352),(404,362),(318,362)],DK,-6,6,b=2,bz=2),
    K([(394,300),(404,300),(404,362),(394,362)],DK,-6,6,b=2,bz=2),
    # Rahmen mit Zubehörschiene
    K([(226,272),(548,272),(548,288),(536,302),(236,302),(226,290)],BK,-16,16,b=4,bz=5,
      dec=[([(440+18*i,284),(450+18*i,284),(446+18*i,292),(436+18*i,292)],DK,False) for i in range(5)]),
    # Schlitten: Keil, vorn und hinten scharf abgeschrägt (Tarnkappen-Facetten)
    K([(214,224),(488,224),(552,250),(552,272.5),(214,272.5),(196,250)],BK,-20,20,b=9,bz=9,label='Schlitten',
      glow=[((0,1),IC,2.4)],dec=[([(232+12*i,238),(238+12*i,238),(244+12*i,262),(238+12*i,262)],DK,False) for i in range(4)]),
    # Visierschiene auf dem Schlitten
    K([(300,216),(440,216),(440,224.5),(300,224.5)],DK,-8,8,b=2,bz=2,label='Visierschiene'),
    # Lauf (Sechskant) und Mündung
    X(540,590,252,10,GM,n=6,label='Lauf'),
    K([(580,236),(622,236),(640,252),(622,268),(580,268)],DK,-15,15,b=5,bz=5,label='Mündung',glow=[((1,2),IC,2.0)]),
    # --- Visier separat: Reflexvisier mit Facettenhaube
    K([(334,204),(392,204),(392,216.5),(334,216.5)],DK,-10,10,b=2,bz=2,sight=True,label='Reflexvisier'),
    K([(338,180),(380,180),(394,204.5),(330,204.5)],BK,-11,11,b=4,bz=4,sight=True,label='Reflexvisier',
      dec=[([(344,188),(380,188),(386,200),(340,200)],IC,True)]),
    ]
META=dict(sight=('reflex','glass'),num='01',name='Pistole',nick='SPLINTER',col=IC,pill='STEALTH-GRAPHIT · EISBLAU · GUNMETAL',palette=[BK,IC,GM,DK],center=(420,330,0),
 desc='Stealth-Pistole der Black-Ice-Serie: Der Schlitten ist ein flacher Keil mit breiten Facetten statt Rundungen, vorn und hinten scharf abgeschrägt. Eisblaue Leuchtkanten laufen entlang der oberen Schlittenkanten. Rahmen mit Zubehörschiene, Sechskant-Lauf und facettierte Mündung. Abzug offen im Bügel, Magazin mit Leuchtkante. Das Reflexvisier mit Facettenhaube ist separat.',
 form='Facettierter Keilschlitten mit Leuchtkanten · Visierschiene · Rahmen mit Zubehörschiene · Sechskant-Lauf · facettierte Mündung · schräger Griff mit Magazin · offener Abzugbügel · Reflexvisier separat')
