from eng import *
def mid(c,f=1.45):return lum(c,f)
def d01(P,K,A,L):
    m=Model();KM=mid(K)
    # Griff (nach hinten geneigt)
    m.prism([(130,175),(215,175),(150,345),(62,332)],P,-22,22,r=14);label(m,'Griff')
    m.decal('z+',22,roundpoly([(120,250),(150,252),(122,330),(92,326)],6),A)
    # Abzugbuegel
    GU=lum(K,1.6)
    m.prism([(262,182),(290,182),(272,252),(250,240)],GU,-6,6);label(m,'Abzug')
    m.prism([(205,240),(255,236),(272,252),(214,262)],GU,-6,6)
    m.prism([(224,185),(240,185),(244,234),(230,236)],A,-4,4);label(m,'Abzug')
    # Heckblock (Akzent)
    m.prism([(22,60),(130,40),(140,50),(140,170),(30,172),(18,150)],A,-36,36,r=12);label(m,'Heckkappe')
    m.decal('z+',36,roundpoly(rect(40,120,70,30),6),K)
    m.decal('z+',36,circ(60,80,6),L,emit=True)
    # Mittelteil dunkel
    m.prism([(130,52),(300,48),(300,185),(130,185)],K,-34,34,r=8);label(m,'Verschluss')
    m.decal('z+',34,roundpoly(rect(170,95,90,45),10),KM)
    m.decal('z+',34,circ(200,118,8),A,emit=True);m.decal('z+',34,circ(240,118,8),A,emit=True)
    # Vorderes Paneel
    m.prism([(390,180),(515,180),(505,236),(398,236)],P,-38,38,r=10);m.parts[-1]['bias']=-60
    m.prism([(280,40),(560,28),(575,45),(575,195),(280,190)],P,-40,40,r=12);label(m,'Gehäuse')
    m.decal('z+',40,roundpoly([(300,45),(560,34),(560,48),(300,58)],3),A,emit=True)
    m.decal('z+',40,roundpoly(rect(340,90,130,8),3),K)
    m.decal('z+',40,roundpoly(rect(470,85,40,40),6),K)
    m.decal('z+',40,roundpoly(rect(300,150,60,10),3),KM)
    # Ladeblock unten
    m.prism([(405,225),(505,225),(510,300),(400,300)],P,-30,30,r=10);label(m,'Energiezelle')
    m.decal('z+',30,roundpoly(rect(408,282,98,14),4),A,emit=True)
    # Muendung
    for a,b in ((560,600),(600,640)):m.cyl(a,b,105,0,72,K if a==560 else KM);label(m,'Mündung')
    m.cyl(640,648,105,0,60,K)
    m.decal('x+',648,circ(105,0,48),A,emit=True);m.decal('x+',648.5,circ(105,0,36),'#0B0D10');m.decal('x+',649,circ(105,0,18),L,emit=True)
    return m,(330,190,0)
def d02(P,K,A,L):
    m=Model();PM=mid(P,1.15)
    m.prism([(270,240),(355,240),(330,380),(250,372)],K,-22,22,r=12);label(m,'Griff')
    m.decal('z+',22,roundpoly([(275,270),(320,270),(305,350),(265,346)],6),PM)
    m.prism([(359,246),(375,246),(384,302),(370,306)],A,-6,6);label(m,'Abzug')
    m.prism([(336,322),(406,322),(406,331),(334,331)],lum(K,1.6),-7,7);label(m,'Abzug')
    m.prism(rect(398,244,8,87),lum(K,1.6),-7,7)
    m.prism([(414,244),(476,244),(484,352),(424,356)],P,-20,20,r=8);label(m,'Magazin')
    m.decal('z+',20,roundpoly(rect(432,268,34,8),3),A,emit=True)
    m.prism([(420,350),(486,346),(488,360),(422,364)],K,-21,21,r=4)
    # Schaft
    m.prism([(20,80),(230,62),(232,250),(150,300),(40,312),(18,265)],P,-30,30,r=16);label(m,'Schaft')
    m.decal('z+',30,roundpoly([(50,120),(180,110),(180,220),(120,255),(55,260)],10),K)
    m.decal('z+',30,roundpoly(rect(70,90,110,10),3),A)
    # Gehaeuse
    m.prism([(220,70),(560,55),(575,70),(575,245),(220,245)],P,-38,38,r=12);label(m,'Gehäuse')
    m.decal('z+',38,roundpoly(rect(250,150,300,14),4),A,emit=True)
    m.decal('z+',38,roundpoly(rect(250,90,120,34),8),K)
    m.decal('z+',38,roundpoly(rect(420,95,100,40),8),K)
    m.decal('z+',38,roundpoly(rect(440,105,30,20),4),A,emit=True)
    # Handschutz vorne
    m.prism([(560,105),(800,115),(815,135),(815,270),(560,285)],P,-36,36,r=14);label(m,'Handschutz')
    m.decal('z+',36,roundpoly(rect(590,200,190,14),4),A,emit=True)
    m.decal('z+',36,roundpoly(rect(600,140,160,40),10),K)
    m.decal('z+',36,roundpoly(rect(590,235,200,30),8),K)
    # Muendung
    m.prism([(800,150),(860,155),(866,170),(866,295),(800,300)],K,-30,30,r=10);label(m,'Mündung')
    m.decal('x+',866,roundpoly(rect(-22,-16,44,32),6) and [(y,z) for y,z in roundpoly([(190,-18),(240,-18),(240,18),(190,18)],6)],'#0B0D10')
    m.decal('x+',866.5,circ(215,0,9),A,emit=True)
    # Visierschiene (bleibt an der Waffe)
    m.prism(rect(380,50,170,12),K,-13,13,r=3);label(m,'Visierschiene')
    for xx in range(392,546,22):m.decal('z+',13,rect(xx,52,10,4),PM)
    # Kastenvisier (separat, modular)
    m.prism(rect(410,36,80,16),K,-14,14,r=4);sight(m)
    m.prism([(350,-26),(520,-30),(530,-20),(530,38),(350,40)],K,-24,24,r=10);label(m,'Kastenvisier');sight(m)
    m.decal('z+',24,roundpoly(rect(370,-9,40,30),6),PM);m.decal('z+',24,circ(390,6,8),A,emit=True)
    m.decal('x+',530,circ(6,0,16),A,emit=True)
    return m,(440,180,0)
def d03(P,K,A,L):
    m=Model();PM=mid(P,0.8)
    m.prism([(250,230),(340,230),(315,370),(235,362)],K,-22,22,r=12);label(m,'Griff')
    m.decal('z+',22,roundpoly([(262,260),(310,260),(295,340),(255,336)],6),mid(K,1.6))
    m.prism([(341,246),(357,246),(366,300),(352,304)],A,-6,6);label(m,'Abzug')
    m.prism([(318,322),(366,322),(366,331),(316,331)],lum(K,1.6),-7,7);label(m,'Abzug')
    m.prism(rect(358,244,8,87),lum(K,1.6),-7,7)
    m.prism([(372,242),(430,242),(436,314),(378,318)],K,-22,22,r=8);label(m,'Energiezelle')
    m.decal('z+',22,roundpoly(rect(388,262,30,8),3),A,emit=True)
    # Schaft mit Aussparung (als Rahmen aus Teilen)
    m.prism([(10,70),(210,60),(212,130),(20,135)],P,-28,28,r=12);label(m,'Schaft')
    m.prism([(10,130),(70,130),(70,300),(20,310),(8,280)],P,-28,28,r=12)
    m.prism([(60,250),(212,240),(212,295),(60,305)],P,-28,28,r=10)
    m.decal('z+',28,roundpoly(rect(25,150,30,120),6),PM)
    # Gehaeuse gold
    m.prism([(200,75),(560,62),(575,78),(575,240),(200,245)],P,-38,38,r=12);label(m,'Gehäuse')
    m.decal('z+',38,roundpoly(rect(260,110,180,46),18),K)
    m.decal('z+',38,roundpoly(rect(276,122,148,22),10),A,emit=True)
    m.decal('z+',38,roundpoly(rect(470,90,70,14),4),A,emit=True)
    m.decal('z+',38,roundpoly(rect(210,190,350,18),4),PM)
    # Lauf-Huelle mit Energiekanal
    m.prism([(550,105),(805,112),(815,125),(815,262),(550,268)],K,-34,34,r=12);label(m,'Laufhülle')
    m.prism(rect(560,96,240,14),P,-26,26,r=5)
    m.decal('z+',34,roundpoly(rect(570,155,220,52),20),A,emit=True)
    m.decal('z+',34,roundpoly(rect(600,174,160,10),4),L,emit=True)
    m.prism(rect(560,262,220,40),K,-24,24,r=10)
    m.decal('z+',24,roundpoly(rect(590,275,150,10),3),P)
    # Muendung
    m.prism([(805,128),(895,132),(905,145),(905,280),(805,285)],K,-32,32,r=12);label(m,'Mündung')
    m.decal('x+',905,[(y,z) for y,z in roundpoly([(170,-20),(240,-20),(240,20),(170,20)],8)],'#0B0D10')
    m.decal('x+',905.5,circ(205,0,10),A,emit=True)
    # Visierschiene (bleibt an der Waffe)
    m.prism(rect(290,58,200,12),K,-13,13,r=3);label(m,'Visierschiene')
    for xx in range(302,486,22):m.decal('z+',13,rect(xx,60,10,4),PM)
    # Visier (separat, modular)
    m.prism(rect(330,44,70,14),K,-14,14,r=4);sight(m)
    m.prism([(280,-22),(480,-26),(490,-14),(490,44),(280,48)],P,-24,24,r=12);label(m,'Visier');sight(m)
    m.decal('z+',24,roundpoly(rect(300,-3,80,26),8),A,emit=True)
    m.decal('x+',490,circ(10,0,15),A,emit=True)
    return m,(460,180,0)
def d04(P,K,A,L):
    m=Model();KM=mid(K)
    m.prism([(250,195),(345,200),(305,362),(222,352)],K,-24,24,r=14);label(m,'Griff')
    m.decal('z+',24,roundpoly([(262,230),(318,232),(292,330),(252,326)],6),KM)
    m.prism([(347,258),(363,258),(372,316),(358,320)],A,-6,6);label(m,'Abzug')
    m.prism([(318,334),(402,330),(402,339),(316,343)],lum(K,1.6),-7,7);label(m,'Abzug')
    m.prism(rect(394,256,8,83),lum(K,1.6),-7,7)
    # Schaft
    m.prism([(18,90),(195,70),(205,265),(130,322),(58,322),(28,272)],K,-30,30,r=16);label(m,'Schaft')
    m.decal('z+',30,roundpoly([(40,100),(180,85),(185,175),(50,185)],10),P)
    m.decal('z+',30,roundpoly(rect(70,215,80,10),3),KM)
    # Gehaeuse
    m.prism([(170,40),(585,30),(590,255),(170,262)],K,-40,40,r=14)
    m.prism([(205,4),(520,0),(535,20),(535,95),(205,98)],P,-34,34,r=14)
    m.decal('z+',34,roundpoly(rect(420,10,70,12),4),A,emit=True)
    m.decal('z+',40,roundpoly(rect(230,150,70,22),6),KM)
    m.decal('z+',40,circ(430,140,12),A,emit=True)
    m.decal('z+',40,roundpoly(rect(470,120,80,26),6),KM)
    # Trommelkasten
    m.prism([(440,184),(715,184),(715,330),(460,340),(440,320)],K,-52,52,r=18);label(m,'Trommelmagazin')
    m.decal('z+',52,roundpoly(rect(480,205,160,90),12),KM)
    m.decal('z+',52,roundpoly(rect(500,250,40,12),3),A,emit=True)
    # Oberer Lauf
    m.prism([(570,42),(950,48),(970,62),(970,175),(570,180)],K,-36,36,r=16);label(m,'Oberlauf')
    m.decal('z+',36,roundpoly([(600,58),(940,62),(940,110),(600,112)],10),A,emit=True)
    m.decal('z+',36,roundpoly(rect(650,120,260,14),5),L,emit=True)
    m.decal('x+',970,[(y,z) for y,z in roundpoly([(70,-26),(150,-26),(150,26),(70,26)],14)],A,emit=True)
    m.decal('x+',970.5,[(y,z) for y,z in roundpoly([(88,-12),(132,-12),(132,12),(88,12)],8)],L,emit=True)
    # Unterer Lauf
    m.cyl(715,760,245,0,56,K)
    m.cyl(760,900,245,0,56,A,emit=False);label(m,'Unterlauf')
    m.cyl(900,975,245,0,58,K)
    m.decal('x+',975,circ(245,0,36),'#0B0D10');m.decal('x+',975.5,circ(245,0,20),A,emit=True)
    return m,(500,180,0)
def d05(P,K,A,L):
    """Scharfschuetzengewehr D „Wueste“ – Konstruktion nach Masterprompt Abschnitt 4."""
    m=Model();PM=mid(P,0.86);KM=mid(K,1.5)
    # --- Schaft: Schulterstütze + Wangenauflage + Unterstrebe (Daumenloch-Rahmen) ---
    m.prism([(-82,102),(-70,102),(-74,292),(-86,292)],K,-22,22,r=4)            # Gummi-Schaftkappe
    m.prism([(-70,100),(-40,100),(-38,292),(-74,292)],P,-24,24,r=6);label(m,'Schaft')
    m.prism([(-40,106),(92,106),(92,150),(-40,150)],P,-20,20,r=8);label(m,'Schaft')
    m.prism(rect(-26,93,86,13),K,-15,15,r=5)                                  # Wangenauflage
    m.prism([(-40,256),(92,196),(92,230),(-40,290)],P,-18,18,r=6);label(m,'Schaft')
    # --- Gehäuse ---
    rec=[(90,110),(345,110),(360,125),(360,215),(345,235),(90,235)]
    m.prism(rec,P,-32,32,r=10);label(m,'Gehäuse')
    m.decal('z+',32,roundpoly(rect(150,134,120,34),8),K)                     # Auswurffenster
    m.decal('z+',32,roundpoly(rect(160,145,60,12),4),KM)
    m.decal('z+',32,circ(300,151,7),A,emit=True)                             # Ladeanzeige
    m.decal('z+',32,roundpoly(rect(110,196,230,8),3),PM)
    # --- Montageschiene + Zielfernrohr auf zwei Ringen ---
    m.prism(rect(118,98,236,12),K,-13,13,r=3);label(m,'Visierschiene')
    for xx in range(126,350,18):m.decal('z+',13,rect(xx,100,8,4),KM)        # Rillen der Schiene
    # --- Zielfernrohr (separat, modular auf der Schiene) ---
    for xx in (165,290):
        m.prism(rect(xx,78,22,20),K,-10,10,r=3);sight(m)
        if xx==165:label(m,'Montage')
        m.cyl(xx,xx+22,58,0,25,K);sight(m)
        if xx==165:label(m,'Montage')
    m.cyl(98,150,58,0,24,K);sight(m)                                         # Okular
    m.decal('x-',98,circ(58,0,17),'#0B0D10');m.decal('x-',97.6,circ(58,0,9),KM)
    m.cyl(150,165,58,0,21,P);sight(m);m.cyl(187,290,58,0,21,P);label(m,'Zielfernrohr');sight(m)
    m.cyl(312,330,58,0,21,P);sight(m)
    m.cyl(330,398,58,0,28,P);label(m,'Zielfernrohr');sight(m)                # Objektiv
    m.cyl(398,410,58,0,30,K);sight(m)
    m.decal('x+',410,circ(58,0,23),'#0B0D10');m.decal('x+',410.5,circ(58,0,12),A,emit=True)
    m.prism(rect(226,22,26,16),K,-10,10,r=3);sight(m)                         # Höhenturm
    m.prism(rect(229,48,20,20),K,17,29,r=3);sight(m)                          # Seitenturm (Parallaxe)
    # --- Griff, Abzug, Abzugbügel ---
    m.prism([(212,235),(262,235),(246,346),(194,341)],K,-18,18,r=10);label(m,'Griff')
    for yy in (270,292,314):m.decal('z+',18,roundpoly([(214,yy),(248,yy),(246,yy+8),(211,yy+8)],2),KM)
    m.prism([(279,235),(295,235),(304,290),(290,294)],A,-6,6);label(m,'Abzug')
    m.prism([(258,302),(314,302),(314,311),(254,311)],lum(K,1.6),-7,7);label(m,'Abzug')
    m.prism(rect(306,235,8,76),lum(K,1.6),-7,7)
    # --- Magazin vor dem Abzug ---
    m.prism([(320,235),(356,235),(362,312),(326,315)],P,-16,16,r=5);label(m,'Magazin')
    m.decal('z+',16,roundpoly(rect(332,252,18,8),2),A,emit=True)
    m.prism([(323,312),(364,309),(366,322),(325,325)],K,-17,17,r=3)
    # --- Laufverkleidung (schlank) ---
    hg=[(352,122),(705,126),(720,140),(720,196),(352,206)]
    m.prism(hg,PM,-24,24,r=10)
    m.decal('z+',24,roundpoly(rect(420,148,170,9),4),A,emit=True)
    for xx in (612,640,668):m.decal('z+',24,roundpoly(rect(xx,140,16,44),4),K)  # Kühlschlitze
    # --- Lauf + Mündungsbremse ---
    m.cyl(700,866,165,0,11,K);label(m,'Lauf')
    mb=[(862,141),(930,141),(944,153),(944,189),(862,189)]
    m.prism(mb,P,-18,18,r=6);label(m,'Mündungsbremse')
    for xx in (876,898,920):m.decal('z+',18,roundpoly(rect(xx,150,12,30),3),K)
    m.decal('x+',944,circ(165,0,10),'#0B0D10');m.decal('x+',944.5,circ(165,0,5),A,emit=True)
    return m,(430,185,0)
