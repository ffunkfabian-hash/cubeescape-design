from eng import *
import math
def rr(x,y,w,h,r):return roundpoly(rect(x,y,w,h),r)
def arcband(x0,x1,y0,depth,th):
    o=[(x0+(x1-x0)*t, y0+4*t*(1-t)*depth) for t in [i/10 for i in range(11)]]
    i=[(x0+th+(x1-x0-2*th)*t, y0+4*t*(1-t)*(depth-th)) for t in [k/10 for k in range(11)]][::-1]
    return o+i
BL='#0A0A0D'
def nh(m):
    m.parts[-1]['nohull']=True;m.parts[-1]['hull']=False
def d06():
    P,DK,A,AL='#D8DCE0','#2A2F38','#F5B014','#FFE7A3';K='#1C2027'
    m=Model()
    m.prism([(70,140),(98,140),(98,305),(72,305)],K,-24,24,r=8);label(m,'Schaft')
    m.prism([(95,188),(158,188),(128,300),(95,300)],P,-18,18,r=8);label(m,'Schaft')
    m.prism(rect(95,145,110,50),P,-20,20,r=12)
    m.decal('z+',20,rr(140,155,50,10,4),DK)
    m.cyl(200,265,172,0,14,K);label(m,'Schaft')
    # Griff + Abzugbuegel
    m.prism([(330,245),(392,245),(420,372),(360,378)],K,-20,20,r=12);label(m,'Griff')
    m.decal('z+',20,roundpoly([(366,290),(382,290),(402,352),(386,352)],5),A,emit=True)
    m.prism(arcband(408,500,250,60,11),'#8A93A3',-7,7);nh(m);label(m,'Abzug')
    m.prism([(438,250),(452,250),(460,300),(446,303)],A,-6,6);label(m,'Abzug')
    # Magazin vorne
    m.prism([(562,242),(612,242),(606,365),(566,365)],K,-18,18,r=8);label(m,'Magazin')
    m.decal('z+',18,rr(578,262,12,74,5),A,emit=True)
    # Gehaeuse
    m.prism([(260,128),(560,128),(580,148),(580,252),(260,252)],DK,-30,30,r=12);label(m,'Gehäuse')
    m.decal('z+',30,roundpoly([(290,138),(470,138),(480,185),(290,190)],8),P)
    m.decal('z+',30,rr(320,152,130,14,6),A,emit=True)
    m.decal('z+',30,rr(300,205,140,12,5),'#3E4450')
    m.decal('z+',30,rr(470,170,70,26,8),A,emit=True)
    # Vorderer Block
    m.prism([(540,122),(662,122),(684,144),(684,242),(562,242),(540,218)],P,-36,36,r=14)
    m.decal('z+',36,[(580,150),(610,180),(600,190),(570,160)],DK)
    m.decal('z+',36,[(610,180),(640,150),(650,160),(620,190)],DK)
    # Muendung
    m.prism(rect(684,132,40,108),K,-30,30,r=10);label(m,'Mündung')
    m.decal('x+',724,circ(160,0,15),BL);m.decal('x+',724.5,circ(160,0,6),A,emit=True)
    m.decal('x+',724,circ(208,0,13),BL)
    # Tragegriff / Visier
    m.prism(rect(310,100,18,32),K,-7,7,r=5);m.parts[-1]['bias']=40;m.prism(rect(470,100,18,32),K,-7,7,r=5);m.parts[-1]['bias']=40
    m.prism(rect(296,88,212,16),K,-8,8,r=8);label(m,'Tragegriff')
    # Kimme (hinten) und Korn (vorne) – separat, modular auf dem Tragegriff
    m.prism([(300,88),(328,88),(328,62),(320,62),(314,74),(308,62),(300,62)],K,-9,9);label(m,'Kimme · Korn');sight(m)
    m.prism([(486,88),(510,88),(504,58),(492,58)],K,-6,6);label(m,'Kimme · Korn');sight(m)
    m.decal('z+',6,rect(495,62,6,6),A,emit=True)
    return m,(400,250,0)
def d07():
    P,DK,A,AL='#CFE0F0','#1E2A38','#22D3EE','#CFFAFE';K='#151C26'
    m=Model()
    m.prism([(40,224),(128,224),(62,272),(40,262)],DK,-20,20,r=8)
    m.prism([(40,150),(180,140),(205,160),(205,232),(40,232)],DK,-22,22,r=12);label(m,'Schaft')
    m.decal('z+',22,rr(70,156,96,24,8),P)
    m.prism([(300,278),(352,278),(382,392),(332,398)],K,-20,20,r=12);label(m,'Griff')
    m.prism(arcband(354,438,280,50,11),'#8A93A3',-7,7);nh(m);label(m,'Abzug')
    m.prism([(380,280),(394,280),(402,324),(388,326)],A,-6,6);label(m,'Abzug')
    m.prism(rect(236,278,52,72),K,-22,22,r=10);label(m,'Energiezelle')
    m.prism([(200,120),(400,110),(432,132),(432,282),(222,282),(200,260)],P,-38,38,r=16);label(m,'Ladekammer')
    m.decal('z+',38,rr(236,160,160,62,20),K)
    m.decal('z+',38,rr(250,176,132,30,14),A,emit=True)
    m.decal('z+',38,rr(262,186,104,10,5),AL,emit=True)
    m.prism(rect(256,100,112,14),K,-14,14,r=3);label(m,'Visierschiene')
    for xx in range(264,364,18):m.decal('z+',14,rect(xx,102,8,4),'#3E4E64')
    m.prism(rect(250,64,124,36),P,-24,24,r=12);label(m,'Visier');sight(m)
    m.decal('z+',24,rr(270,74,84,8,4),'#1E2A38')
    m.decal('x+',374,circ(82,0,10),A,emit=True)
    m.prism(rect(440,250,300,42),DK,-28,28,r=10)
    for k in range(5):m.decal('z+',28,rr(480+44*k,262,28,12,5),'#0B1118')
    m.prism([(430,126),(742,126),(762,146),(762,252),(430,252)],DK,-34,34,r=12);label(m,'Laufkasten')
    m.decal('z+',34,rr(468,150,240,64,24),'#0B1118')
    m.decal('z+',34,rr(478,168,220,26,13),A,emit=True)
    m.decal('z+',34,rr(490,176,196,10,5),AL,emit=True)
    m.prism(rect(760,138,24,104),K,-30,30,r=8);label(m,'Mündung')
    m.decal('x+',784,rr(160,-18,60,36,14),BL);m.decal('x+',784.5,circ(190,0,9),A,emit=True)
    return m,(410,250,0)
def d08():
    P,DK,A,AL='#3A3D44','#18191C','#EF2B2B','#FFB4B4'
    m=Model()
    m.prism([(46,196),(114,196),(84,272),(46,272)],P,-22,22,r=8)
    m.prism([(40,132),(172,126),(194,146),(194,204),(40,204)],P,-24,24,r=14)
    m.prism(rect(28,128,20,148),DK,-26,26,r=6);label(m,'Schaft')
    m.decal('z+',24,rr(70,150,80,10,5),DK)
    m.prism([(252,248),(302,248),(322,372),(272,378)],DK,-20,20,r=12);label(m,'Griff')
    m.prism(arcband(304,388,250,68,11),'#8A93A3',-7,7);nh(m);label(m,'Abzug')
    m.prism([(326,250),(342,250),(352,306),(336,309)],A,-6,6);label(m,'Abzug')
    m.prism([(400,292),(442,292),(452,372),(412,374)],DK,-18,18,r=10)
    m.prism([(190,120),(332,114),(352,134),(352,250),(190,250)],DK,-32,32,r=12)
    m.prism(rect(400,256,222,40),DK,-28,28,r=10)
    m.decal('z+',28,rr(470,270,90,10,5),'#2C2E33')
    m.prism([(350,130),(732,124),(762,150),(762,258),(350,258)],P,-36,36,r=16);label(m,'Laufmantel')
    m.decal('z+',36,rr(372,170,360,32,16),'#0B0B0E')
    m.decal('z+',36,rr(380,176,344,22,11),A,emit=True)
    m.decal('z+',36,rr(392,183,318,8,4),AL,emit=True)
    m.decal('z+',36,rr(380,222,140,22,8),DK)
    m.prism(rect(380,110,300,20),P,-24,24,r=10)
    m.prism(circ(300,186,58,28),DK,-44,44,smooth=True);label(m,'Energie-Auge')
    m.decal('z+',44,circ(300,186,42,28),P)
    m.decal('z+',44.5,circ(300,186,24,24),A,emit=True)
    m.decal('z+',45,circ(300,186,9,16),AL,emit=True)
    m.prism([(200,108),(336,103),(336,115),(200,120)],DK,-13,13,r=3);label(m,'Visierschiene')
    m.prism(rect(212,88,22,18),DK,-9,9,r=4);sight(m);label(m,'Montage');m.prism(rect(296,84,22,18),DK,-9,9,r=4);sight(m);label(m,'Montage')
    m.cyl(190,336,74,0,18,DK);label(m,'Zielfernrohr');sight(m)
    m.decal('x+',336,circ(74,0,12),A,emit=True)
    m.prism(rect(762,140,26,112),DK,-30,30,r=10);label(m,'Mündung')
    m.decal('x+',788,rr(166,-22,56,44,16),BL);m.decal('x+',788.5,circ(194,0,10),A,emit=True)
    return m,(410,245,0)
def d09():
    P,DK,A,AL='#D8DCE0','#2A2F38','#EC4FA6','#FBCFE8';K='#1C2027'
    m=Model()
    m.prism([(112,282),(204,282),(192,332),(124,332)],K,-22,22,r=8)
    m.prism([(300,300),(352,300),(372,412),(322,416)],K,-22,22,r=12);label(m,'Griff')
    m.prism(arcband(352,436,300,74,11),'#8A93A3',-7,7);nh(m);label(m,'Abzug')
    m.prism([(370,300),(386,300),(396,358),(380,361)],A,-6,6);label(m,'Abzug')
    m.prism([(520,296),(562,296),(566,362),(526,362)],K,-18,18,r=8);label(m,'Vordergriff')
    m.prism(rect(284,276,144,26),P,-30,30,r=8)
    m.prism(rect(40,126,42,168),A,-46,46,r=12);label(m,'Heckdüse')
    m.decal('z+',46,rr(52,150,16,110,6),DK)
    m.decal('x-',40,rr(140,-34,120,68,22),BL)
    m.prism(rect(80,120,202,166),P,-50,50,r=20)
    m.decal('z+',50,rr(126,166,70,26,8),K);m.decal('z+',50.5,rr(136,174,48,10,5),A,emit=True)
    m.prism(rect(280,116,152,162),K,-46,46,r=18)
    m.decal('z+',46,circ(350,190,18,18),'#3E4450');m.decal('z+',46.5,circ(350,190,10,18),'#2A2F38')  # Ladeklappe statt Deko-Punkt
    m.decal('z+',46,rr(300,230,110,10,5),'#3E4450')
    m.prism(rect(430,104,232,194),P,-54,54,r=22);label(m,'Rohr')
    m.decal('z+',54,rr(486,164,96,28,10),K);m.decal('z+',54.5,rr(498,173,72,10,5),A,emit=True)
    m.prism([(656,92),(722,92),(748,118),(748,282),(722,308),(656,308)],K,-60,60,r=12);label(m,'Mündung')
    m.decal('x+',748,rr(138,-42,124,84,24),BL)
    m.decal('x+',748.5,rr(152,-28,96,56,18),A,emit=True)
    m.decal('x+',749,rr(170,-12,60,24,10),AL,emit=True)
    # Visierschiene seitlich LINKS am Rohr (Rohr würde oben die Sichtlinie verdecken) – auf Höhe der oberen Rohrkante
    m.prism(rect(296,120,132,18),P,44,60,r=4);label(m,'Visierschiene')
    for xx in range(306,424,18):m.decal('z+',60,rect(xx,125,8,8),'#4A5262',both=False)
    # Visier (separat, modular auf der seitlichen Schiene)
    m.prism(rect(334,104,16,26),K,58,74,r=3);sight(m);m.prism(rect(392,104,16,26),K,58,74,r=3);sight(m)
    m.cyl(318,420,108,86,16,K);label(m,'Visier');sight(m)
    m.decal('x+',420,circ(108,86,11),A,emit=True)
    return m,(400,250,0)
def d10():
    P,DK,A,AL='#3A3D44','#17181B','#F2C230','#FFF1B8'
    m=Model()
    # Mittellinie des Bogens (Pfeilrichtung +x)
    def c(t):  # t in [-1,1]
        return (430-110*t*t, 250+215*t)
    def band(t0,t1,wf,off=0,N=14):
        L=[];R=[]
        for i in range(N+1):
            t=t0+(t1-t0)*i/N;p=c(t);q=c(t+0.001)
            dx,dy=q[0]-p[0],q[1]-p[1];l=math.hypot(dx,dy);nx,ny=-dy/l,dx/l
            w=wf(t)
            L.append((p[0]+nx*(off+w/2),p[1]+ny*(off+w/2)));R.append((p[0]+nx*(off-w/2),p[1]+ny*(off-w/2)))
        return L+R[::-1]
    W=lambda t:14+20*(1-abs(t))**2
    for t0,t1 in ((-1,-0.2),(0.2,1)):
        m.prism(band(t0,t1,W),P,-11,11,smooth=True);m.parts[-1]['nohull']=True;label(m,'Wurfarm')
        m.parts[-1]['F'][0]['hard']=True
        m.decal('z+',11,band(t0+0.06*(1 if t0<0 else 0),t1-0.06*(1 if t1>0 else 0),lambda t:4),A,emit=True)
    # Mittelstück (Riser) mit Pfeilfenster: oben/unten getrennt, Steg auf der rechten Seite
    for t0,t1 in ((-0.3,-0.09),(0.09,0.3)):
        m.prism(band(t0,t1,W),DK,-13,13,smooth=True);m.parts[-1]['nohull']=True;m.parts[-1]['F'][0]['hard']=True
    # Griffstück: oberer und unterer Teil, dazwischen das Fenster
    m.prism([(412,206),(452,201),(455,233),(414,233)],DK,-16,16,r=8)
    m.prism([(416,268),(456,268),(462,312),(420,314)],DK,-16,16,r=10);label(m,'Griff')
    m.decal('z+',16,rr(430,276,12,30,5),A,emit=True)
    # Steg (rechte Seite) verbindet oben und unten am Fenster
    m.prism(rect(414,226,42,48),DK,-16,-7,r=6)
    # Pfeilauflage im Fenster
    m.prism(rect(420,253,30,7),A,-7.5,6,r=2);label(m,'Pfeilauflage')
    # Rollen an den Spitzen
    for y in (40,460):
        m.prism(circ(322,y,16,18),DK,-9,9,smooth=True);label(m,'Umlenkrolle');m.decal('z+',9,circ(322,y,7,14),A,emit=True)
        # Achse mit Lagerdeckeln auf beiden Seiten des Wurfarms
        m.prism(circ(322,y,5,12),'#55595F',-16,16,smooth=True);label(m,'Rollenachse')
        m.decal('z+',16,circ(322,y,3,10),'#0B0B0E')
    # Sehne tangential an der Rückseite der Rollen
    m.prism(rect(303,40,5,420),A,-2,2,r=2,emit=True);label(m,'Sehne')
    # Pfeil: Nocke an der Sehne, Schaft durchs Pfeilfenster
    m.prism(rect(308,247,272,6),AL,-3,3,r=3);label(m,'Pfeil')
    m.prism([(580,240),(612,250),(580,260)],A,-3,3)
    m.prism([(312,243),(336,247),(336,253),(312,257)],A,-1,1)
    m.prism(rect(301,245,9,10),A,-3.5,3.5,r=2)                                # Nocke auf der Sehne
    return m,(440,250,0)
