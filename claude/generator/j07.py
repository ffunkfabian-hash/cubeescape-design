from jlib import *
BK,TQ,GM,DK='#20262F','#7FFFF0','#59626E','#0F1216'
def spec():
    return [
    K([(80,236),(110,232),(200,244),(200,318),(110,330),(84,326)],BK,-18,18,b=7,bz=7,label='Schaft',glow=[((1,),TQ)]),
    K([(196,250),(500,250),(530,266),(530,316),(500,330),(196,330),(186,300)],BK,-26,26,b=10,bz=10,label='Gehäuse',
      dec=[([(214,300),(380,300),(374,312),(220,312)],DK,False)]),
    # Kryokern oben hinten: dunkles Modul mit Leuchtfenster
    K([(210,214),(320,214),(340,232),(340,250.5),(200,250.5)],DK,-20,20,b=6,bz=6,label='Energiemodul',
      dec=[([(226,224),(310,224),(320,240),(222,240)],TQ,True)]),
    K(rect(360,241.5,130,8.5),DK,-10,10,b=2,bz=2,label='Visierschiene'),
    K([(262,330),(306,330),(296,424),(252,424)],DK,-17,17,b=5,bz=5,label='Griff'),
    K([(322,331),(334,331),(346,366),(335,370)],GM,-6,6,b=1.5,bz=1.5,label='Abzug'),
    K(rect(294,378,76,9),DK,-7,7,b=2,bz=2),
    K(rect(362,330,9,57),DK,-7,7,b=2,bz=2),
    K(rect(392,330,74,42),DK,-18,18,b=5,bz=5,label='Energiezelle',dec=[(rect(404,344,50,8),TQ,True)]),
    X(530,700,290,9,GM,n=6,label='Lauf'),
    # Kühlrippen: drei tiefe Facettenplatten mit Leuchtkante oben
    K(rect(552,258,16,64),BK,-28,28,b=4,bz=9,label='Kühlrippen',glow=[((0,),TQ,1.8)]),
    K(rect(588,258,16,64),BK,-28,28,b=4,bz=9,glow=[((0,),TQ,1.8)]),
    K(rect(624,258,16,64),BK,-28,28,b=4,bz=9,glow=[((0,),TQ,1.8)]),
    K([(700,270),(726,270),(744,290),(726,310),(700,310)],DK,-18,18,b=5,bz=5,label='Mündung',glow=[((1,2),TQ,2.0)]),
    # --- Holovisier separat
    K(rect(400,229.5,40,12.5),DK,-11,11,b=2,bz=2,sight=True,label='Holovisier'),
    K([(394,196),(446,196),(456,230),(384,230)],BK,-12,12,b=4,bz=4,sight=True,label='Holovisier',
      dec=[([(402,204),(440,204),(446,222),(396,222)],TQ,True)]),
    ]
META=dict(sight=('holo','glass'),num='07',name='Fusionsgewehr',nick='CRYOCORE',col=TQ,pill='TIEFSCHIEFER · KRYOTÜRKIS · GUNMETAL',palette=[BK,TQ,GM,DK],center=(411,318,0),
 desc='Stealth-Fusionsgewehr der Black-Ice-Serie: Auf dem breiten Facettengehäuse sitzt hinten der dunkle Kryokern mit türkisem Leuchtfenster. Drei tiefe Kühlrippen-Platten mit Leuchtkanten tragen den Sechskant-Lauf, die Energiezelle steckt im Schacht vor dem offenen Abzugbügel. Facettierte Mündung mit Leuchtkanten. Das Holovisier ist separat.',
 form='Keilschaft · breites Facettengehäuse · Kryokern-Energiemodul oben hinten · Visierschiene · Griff + offener Abzugbügel · Energiezelle im Schacht · drei Kühlrippen-Platten · Sechskant-Lauf · facettierte Mündung · Holovisier separat')
