from jlib import *
BK,AU,GM,DK='#232B2E','#5CFFC8','#5E6A6E','#101415'
def spec():
    return [
    K([(150,240),(250,236),(250,316),(170,322),(150,300)],BK,-18,18,b=7,bz=7,label='Schaft',glow=[((0,),AU)]),
    # Gehäuse mit zwei Leuchtkanten
    K([(246,222),(500,222),(540,240),(540,306),(500,318),(246,318)],BK,-26,26,b=10,bz=10,label='Gehäuse',glow=[((0,1),AU)],
      dec=[([(270,286),(380,286),(372,300),(278,300)],DK,False)]),
    K(rect(290,213.5,190,8.5),DK,-8,8,b=2,bz=2,label='Visierschiene'),
    K([(300,318),(344,318),(332,412),(288,412)],DK,-16,16,b=5,bz=5,label='Griff'),
    K([(356,319),(368,319),(380,352),(369,356)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(344,362,62,9),DK,-6,6,b=2,bz=2),
    K(rect(398,318,9,53),DK,-6,6,b=2,bz=2),
    # Energiezelle im Schacht vor dem Bügel, leuchtendes Fenster
    K(rect(414,318,60,54),DK,-18,18,b=5,bz=5,label='Energiezelle',dec=[(rect(424,332,40,10),AU,True)]),
    X(540,700,272,9,GM,n=6,label='Lauf'),
    # drei facettierte Beschleunigerringe auf dem Lauf
    K(rect(570,246,16,52),BK,-24,24,b=4,bz=8,label='Beschleunigerring',dec=[(rect(574,256,8,32),AU,True)]),
    K(rect(606,246,16,52),BK,-24,24,b=4,bz=8,dec=[(rect(610,256,8,32),AU,True)]),
    K(rect(642,246,16,52),BK,-24,24,b=4,bz=8,dec=[(rect(646,256,8,32),AU,True)]),
    K([(700,252),(726,252),(748,272),(726,292),(700,292)],DK,-16,16,b=5,bz=5,label='Emitter',glow=[((1,2),AU,2.0)]),
    # --- Reflexvisier separat
    K(rect(352,201.5,56,12.5),DK,-10,10,b=2,bz=2,sight=True,label='Reflexvisier'),
    K([(356,176),(396,176),(412,202),(346,202)],BK,-11,11,b=4,bz=4,sight=True,label='Reflexvisier',
      dec=[([(362,184),(396,184),(402,196),(358,196)],AU,True)]),
    ]
META=dict(sight=('reflex','glass'),num='03',name='Impulsgewehr',nick='AURORA',col=AU,pill='POLARNACHT · AURORAGRÜN · GUNMETAL',palette=[BK,AU,GM,DK],center=(450,310,0),
 desc='Stealth-Impulsgewehr der Black-Ice-Serie: ein breites Facettengehäuse mit auroragrünen Leuchtkanten, davor drei kantige Beschleunigerringe mit leuchtenden Schlitzen auf dem Sechskant-Lauf. Die Energiezelle steckt mit Leuchtfenster im Schacht vor dem offenen Abzugbügel, vorn sitzt ein facettierter Emitter. Das Reflexvisier ist separat.',
 form='Keilschaft · breites Facettengehäuse mit Leuchtkanten · Visierschiene · Griff + offener Abzugbügel · Energiezelle im Schacht · drei Beschleunigerringe · Sechskant-Lauf · facettierter Emitter · Reflexvisier separat')
