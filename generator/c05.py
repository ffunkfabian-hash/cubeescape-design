from helpers import *
from ctrig import trigger,rail
# Variante C „Monolith“ – konstruktiv überarbeitet nach Masterprompt Abschnitt 4
K,KH,KD,GO,GL,GC,K2='#24262B','#34373E','#16171A','#F5C542','#FFE08A','#FFF2C2','#2A2C31'
def model():
    m=Model()
    # --- Schaft: offenes Skelett aus Schulterstütze, Ober- und Unterholm, Wangenauflage
    m.prism(rect(30,166,22,130),KD,-20,20,r=5);label(m,'Schaft')
    m.prism([(50,174),(204,180),(204,212),(50,212)],K,-14,14,r=4);label(m,'Schaft')
    m.decal('z+',14,rect(60,192,130,3),GO,emit=True)
    m.prism([(50,254),(204,242),(204,262),(50,292)],K,-14,14,r=4);label(m,'Schaft')
    m.prism([(88,162),(186,166),(192,180),(82,178)],KH,-12,12,r=4)
    # --- Gehäuse
    body=[(200,176),(440,168),(470,186),(470,250),(452,262),(200,262)]
    m.prism(body,K,-28,28,r=6);label(m,'Gehäuse')
    m.decal('z+',28,[(202,178),(440,170),(452,178),(202,186)],KH)
    m.decal('z+',28,roundpoly([(200,240),(470,240),(470,250),(452,262),(200,262)],3),KD)
    m.decal('z+',28,roundpoly(rect(236,198,150,22),4),KD)
    m.decal('z+',28.3,rect(246,206,96,4),GO,emit=True)
    for x in (400,416,432):m.decal('z+',28,rect(x,196,6,34),KD)
    # Kammerstängel links (in der Isometrie sichtbar)
    m.prism(rect(228,196,16,12),KD,27,40,r=3);m.decal('z+',40,circ(236,202,4,10),GO,emit=True)
    # --- Griff, Abzug, Bügel
    m.prism([(250,262),(298,262),(284,352),(240,348)],KD,-15,15,r=6);label(m,'Griff')
    for yy in (290,310,330):m.decal('z+',15,strip([(250,yy),(284,yy+2)],3),K2)
    trigger(m,302,262,GO,'#30333A',depth=66,w=34,xr=290,zt=5,zg=6)
    # --- Magazin vor dem Abzugbügel im Magazinschacht
    m.prism(rect(342,258,50,16),KD,-20,20,r=3)
    m.prism([(346,272),(388,272),(394,332),(354,336)],K,-16,16,r=4);label(m,'Magazin')
    m.decal('z+',16,rect(358,300,24,4),GO,emit=True)
    # --- Laufverkleidung (kurz, schmaler als das Gehäuse)
    hg=[(470,190),(628,194),(640,204),(640,226),(628,236),(470,240)]
    m.prism(hg,KH,-18,18,r=5)
    m.decal('z+',18,rect(490,212,120,3),GO,emit=True)
    for x in (500,530,560,590):m.decal('z+',18,rect(x,198,14,8),KD)
    # --- Lauf sichtbar zwischen Verkleidung und Mündungsbremse
    m.cyl(640,734,214,0,9,KD,n=16);label(m,'Lauf')
    # --- Kastenförmige Mündungsbremse
    m.prism(rect(730,198,42,32),K,-14,14,r=4);label(m,'Mündungsbremse')
    for x in (740,754):m.decal('z+',14,rect(x,204,6,20),KD)
    m.decal('x+',772,circ(214,0,6,12),'#050506')
    # --- Schiene, Montageringe, Zielfernrohr
    m.prism(rect(232,158,206,14),KD,-10,10,r=2);label(m,'Visierschiene')
    for x in range(244,432,16):m.decal('y-',158,rect(x,-10,8,20),K2)
    for x in (276,392):
        m.prism(rect(x-11,136,22,24),KD,-9,9,r=3);label(m,'Montageringe');sight(m)
        m.cyl(x-8,x+8,124,0,17,KD,n=8);label(m,'Montageringe');sight(m)
    m.cyl(236,256,124,0,15,K,n=8);sight(m)
    m.cyl(256,428,124,0,13,KH,n=8);label(m,'Zielfernrohr');sight(m)
    m.cyl(428,470,124,0,18,K,n=8);label(m,'Zielfernrohr');sight(m)
    m.decal('x+',470,circ(124,0,13,8),GO,emit=True)
    m.decal('x+',470.4,circ(124,0,7,8),GC,emit=True)
    m.prism(rect(334,102,16,12),KD,-8,8,r=2);label(m,'Verstellturm');sight(m)
    return m
