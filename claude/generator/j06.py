from jlib import *
BK,CY,GM,DK='#2B2F35','#38E1FF','#646B75','#121417'
def spec():
    return [
    # Klappschaft: Kappe und zwei Streben
    K([(68,246),(90,246),(90,320),(72,314)],DK,-16,16,b=4,bz=4,label='Schaft'),
    K([(88,256),(210,262),(210,276),(88,272)],BK,-8,8,b=3,bz=3,label='Schaft'),
    K([(88,300),(210,286),(210,298),(88,314)],BK,-8,8,b=3,bz=3),
    # kompaktes Gehäuse, hinten und vorn gebrochen
    K([(206,236),(450,236),(486,252),(486,312),(450,324),(206,324),(196,300),(196,260)],BK,-24,24,b=10,bz=10,label='Gehäuse',
      glow=[((0,1),CY)],dec=[([(230+14*i,280),(238+14*i,280),(232+14*i,300),(224+14*i,300)],DK,False) for i in range(4)]),
    K(rect(250,227.5,180,8.5),DK,-8,8,b=2,bz=2,label='Visierschiene'),
    K([(262,324),(306,324),(296,420),(252,420)],DK,-16,16,b=5,bz=5,label='Griff'),
    K([(318,325),(330,325),(342,358),(331,362)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(304,368,66,9),DK,-6,6,b=2,bz=2),
    K(rect(362,324,9,53),DK,-6,6,b=2,bz=2),
    K([(384,324),(420,324),(432,426),(396,428)],DK,-14,14,b=4,bz=4,label='Magazin',glow=[((1,),CY,2.0)]),
    K([(486,256),(620,260),(636,272),(620,300),(486,306)],BK,-18,18,b=7,bz=7,label='Laufmantel',
      dec=[([(506+20*i,268),(518+20*i,268),(512+20*i,290),(500+20*i,290)],DK,False) for i in range(5)]),
    X(636,690,281,8,GM,n=6,label='Lauf'),
    K([(684,266),(708,266),(724,281),(708,296),(684,296)],DK,-13,13,b=4,bz=4,label='Mündung',glow=[((1,2),CY,1.8)]),
    # --- Reflexvisier separat
    K(rect(320,215.5,58,12.5),DK,-10,10,b=2,bz=2,sight=True,label='Reflexvisier'),
    K([(326,190),(366,190),(382,216),(316,216)],BK,-11,11,b=4,bz=4,sight=True,label='Reflexvisier',
      dec=[([(332,198),(366,198),(372,210),(328,210)],CY,True)]),
    ]
META=dict(sight=('reflex','glass'),num='06',name='Maschinenpistole',nick='HAILSTORM',col=CY,pill='GRAPHIT · EISCYAN · GUNMETAL',palette=[BK,CY,GM,DK],center=(397,320,0),
 desc='Stealth-Maschinenpistole der Black-Ice-Serie: kompaktes Facettengehäuse mit gebrochenen Ecken und eiscyanen Leuchtkanten, Klappschaft aus zwei Streben mit Kappe. Das lange Magazin steckt vor dem offenen Abzugbügel, der geschlitzte Laufmantel führt zum Sechskant-Lauf mit facettierter Mündung. Das Reflexvisier ist separat.',
 form='Klappschaft mit zwei Streben · kompaktes Facettengehäuse mit Leuchtkanten · Visierschiene · Griff + offener Abzugbügel · langes Magazin · geschlitzter Laufmantel · Sechskant-Lauf · facettierte Mündung · Reflexvisier separat')
