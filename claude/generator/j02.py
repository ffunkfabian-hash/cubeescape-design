from jlib import *
BK,IC,GM,DK='#2A3038','#4FB8FF','#6B7480','#14171C'
def spec():
    return [
    # Schaft: Keil mit dunkler Aussparung, Leuchtkante oben
    K([(110,236),(150,232),(262,248),(262,300),(150,318),(118,322),(110,300)],BK,-16,16,b=6,bz=6,label='Schaft',
      glow=[((1,),IC)],dec=[([(150,256),(236,262),(236,290),(150,300)],DK,False)]),
    # Gehäuse: lange Facettenplatte, vorn abgeschrägt
    K([(256,226),(520,226),(560,244),(560,300),(520,312),(256,312)],BK,-22,22,b=9,bz=9,label='Gehäuse',glow=[((0,1),IC)],
      dec=[([(300+16*i,286),(310+16*i,286),(304+16*i,300),(294+16*i,300)],DK,False) for i in range(4)]),
    K(rect(300,217.5,200,8.5),DK,-8,8,b=2,bz=2,label='Visierschiene'),
    # Griff, Abzug, offener Bügel
    K([(300,312),(342,312),(330,410),(286,410)],DK,-15,15,b=5,bz=5,label='Griff'),
    K([(354,313),(366,313),(378,346),(367,350)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
    K(rect(340,356,64,9),DK,-6,6,b=2,bz=2),
    K(rect(396,312,9,53),DK,-6,6,b=2,bz=2),
    # Magazin, leicht nach vorn geneigt
    K([(420,312),(462,312),(478,400),(436,404)],DK,-14,14,b=4,bz=4,label='Magazin',glow=[((1,),IC,2.0)]),
    # Handschutz mit schrägen Schlitzen
    K([(560,244),(700,250),(716,264),(700,296),(560,300)],BK,-17,17,b=7,bz=7,label='Handschutz',
      dec=[([(590+22*i,262),(602+22*i,262),(596+22*i,284),(584+22*i,284)],DK,False) for i in range(5)]),
    X(716,780,272,8,GM,n=6,label='Lauf'),
    K([(772,256),(800,256),(816,272),(800,288),(772,288)],DK,-12,12,b=4,bz=4,label='Mündung',glow=[((1,2),IC,1.8)]),
    # --- Holovisier separat: Klemmfuß + facettierter Rahmen mit Glasfenster
    K(rect(380,205.5,56,12.5),DK,-10,10,b=2,bz=2,sight=True,label='Holovisier'),
    K([(384,170),(436,170),(446,206),(374,206)],BK,-11,11,b=4,bz=4,sight=True,label='Holovisier',
      dec=[([(392,178),(430,178),(436,198),(386,198)],IC,True)]),
    ]
META=dict(sight=('holo','glass'),num='02',name='Sturmgewehr',nick='FROSTBITE',col=IC,pill='SCHIEFERNACHT · GLETSCHERBLAU · GUNMETAL',palette=[BK,IC,GM,DK],center=(460,320,0),
 desc='Stealth-Sturmgewehr der Black-Ice-Serie: Gehäuse und Handschutz sind lange Facettenplatten mit scharf abgeschrägter Front, der Schaft ist ein Keil mit dunkler Aussparung. Gletscherblaue Leuchtkanten laufen über Gehäuseoberkante und Schaftrücken. Magazin vor dem offenen Abzugbügel, Sechskant-Lauf mit facettierter Mündung. Das Holovisier ist separat.',
 form='Keilschaft mit Aussparung · Facettengehäuse mit Leuchtkanten · Visierschiene · Griff + offener Abzugbügel · Magazin im Schacht · geschlitzter Handschutz · Sechskant-Lauf · facettierte Mündung · Holovisier separat')
