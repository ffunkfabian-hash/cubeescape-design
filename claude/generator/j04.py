from jlib import *
BK,FR,GM,DK='#2E2F36','#BFEFFF','#6A6E78','#131418'
def spec():
    return [
    K([(106,238),(150,232),(270,246),(270,300),(150,320),(112,326),(106,304)],BK,-16,16,b=6,bz=6,label='Schaft',glow=[((1,),FR)]),
    K([(266,226),(470,226),(500,240),(500,300),(266,300)],BK,-20,20,b=8,bz=8,label='Gehäuse',glow=[((0,),FR)],
      dec=[([(330,262),(420,262),(414,282),(336,282)],DK,False)]),
    K(rect(300,217.5,150,8.5),DK,-8,8,b=2,bz=2,label='Visierschiene'),
    K([(296,300),(340,300),(328,400),(284,400)],DK,-15,15,b=5,bz=5,label='Griff'),
    K([(352,301),(364,301),(376,334),(365,338)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(338,344,64,9),DK,-6,6,b=2,bz=2),
    K(rect(394,300,9,53),DK,-6,6,b=2,bz=2),
    # Lauf über dem Röhrenmagazin, Pumpgriff umschließt das Magazin
    X(500,700,252,10,GM,n=6,label='Lauf'),
    X(500,664,284,9,DK,n=6,label='Röhrenmagazin'),
    K([(540,268),(640,268),(652,285),(640,302),(540,302),(528,285)],BK,-17,17,b=6,bz=6,label='Pumpgriff',
      dec=[([(556+16*i,276),(564+16*i,276),(560+16*i,294),(552+16*i,294)],DK,False) for i in range(5)]),
    K(rect(656,238,14,58),DK,-13,13,b=3,bz=3),
    K([(700,234),(724,234),(738,252),(724,270),(700,270)],DK,-14,14,b=4,bz=4,label='Mündung',glow=[((1,2),FR,2.0)]),
    # --- Kimme und Korn separat (offene Visierung auf der Schiene)
    K([(300,200),(310,200),(312,208),(318,208),(320,200),(330,200),(330,218),(300,218)],DK,-7,7,b=1.5,bz=1.5,sight=True,label='Kimme'),
    K([(438,204),(446,196),(452,196),(452,218),(438,218)],BK,-4,4,b=1.2,bz=1.2,sight=True,label='Korn',dec=[(rect(445.5,199,4,4),FR,True)]),
    ]
META=dict(sight=('iron','open'),num='04',name='Schrotflinte',nick='AVALANCHE',col=FR,pill='STURMGRAU · FROSTWEISS · GUNMETAL',palette=[BK,FR,GM,DK],center=(420,290,0),
 desc='Stealth-Schrotflinte der Black-Ice-Serie: kantiges Facettengehäuse mit frostweißer Leuchtkante, Keilschaft und ein facettierter Pumpgriff, der das Sechskant-Röhrenmagazin umschließt. Darüber der Sechskant-Lauf mit Laufklammer und facettierter Mündung. Kimme und Korn sind ein separates Modul für die Visierschiene.',
 form='Keilschaft · Facettengehäuse mit Leuchtkante · Visierschiene · Griff + offener Abzugbügel · Sechskant-Lauf · Röhrenmagazin · facettierter Pumpgriff · Laufklammer · facettierte Mündung · Kimme und Korn separat')
