from eng import *
from ctrig import trigger,rail
R,RD,RH,BK,BK2,G,GD,GL='#8E1F2F','#5E1420','#B23246','#1C181C','#2C262C','#FFD166','#C9952E','#FFF1C9'
def model():
    m=Model()
    m.prism([(250,270),(330,270),(316,420),(230,420)],BK,-24,24,r=10);label(m,'Griff')
    m.decal('z+',24,roundpoly([(262,290),(318,290),(306,400),(248,400)],6),R)
    for yy in (316,346,376):m.decal('z+',24,rect(254,yy,54,4),RD)
    # Abzug + Buegel, deutlich unter dem Gehaeuse
    trigger(m,338,280,G,BK2,depth=76,w=46,xr=318,zt=5,zg=6)
    m.prism([(110,170),(130,170),(130,260),(110,256)],BK,-28,28,r=6)
    body=[(150,150),(430,140),(452,160),(452,280),(150,280),(130,260),(130,170)]
    m.prism(body,R,-36,36,r=10);label(m,'Gehäuse')
    m.decal('z+',36,roundpoly([(150,152),(430,142),(444,155),(142,163)],3),RH)
    m.decal('z+',36,roundpoly([(132,248),(450,248),(450,278),(152,278),(132,260)],4),RD)
    m.decal('z+',36,roundpoly(rect(150,176,120,74),18),BK)
    m.decal('z+',36,roundpoly(rect(290,176,140,10),3),BK)
    m.decal('z+',36,roundpoly(rect(290,196,100,6),2),G,emit=True)
    # Energiezelle: steckt quer im Gehaeuse, ragt beidseitig leicht aus dem Rahmen
    m.prism(rect(162,188,96,50),G,-38,38,r=12,emit=True);label(m,'Energiezelle')
    for xx in (184,208,232):m.decal('z+',38,rect(xx,188,4,50),GD,emit=True)
    m.decal('z+',38,roundpoly(rect(166,194,20,10),3),GL,emit=True)
    m.prism(rect(170,136,92,14),G,-12,12,r=4,emit=True);label(m,'Ladeleiste')
    # Visierschiene auf dem Gehaeuse (bleibt), Visier (Kimme + Korn) separat
    rail(m,276,436,133,BK2,BK,z=9,h=12,slope=-6/160)
    # Kimme: Fuss + zwei Wangen mit Kerbe (Kerbe quer zur Schussrichtung)
    m.prism([(284,124),(316,124),(316,134),(284,135)],BK,-11,11,r=2);label(m,'Kimme');sight(m)
    for z0,z1 in ((-11,-3),(3,11)):
        m.prism([(288,106),(312,106),(312,125),(288,125)],BK,z0,z1,r=2);sight(m)
        m.decal('x-',288,[(108,z0+2),(108,z1-2),(114,z1-2),(114,z0+2)],G)
    m.prism([(402,120),(430,120),(430,130),(402,131)],BK,-9,9,r=2);label(m,'Korn');sight(m)
    m.prism([(410,100),(422,100),(422,121),(410,121)],BK,-3,3,r=2);sight(m)
    m.decal('z+',3,circ(416,106,3,10),G,emit=True)
    for (x1,yc) in ((642,239),(662,181)):
        for a,b in ((452,520),(546,600),(614,x1)):m.cyl(a,b,yc,0,25,BK);label(m,'Doppellauf')
        m.decal('x+',x1,circ(yc,0,15),'#050506')
        m.decal('x+',x1+0.5,circ(yc,0,8),GL,emit=True)
    m.prism(rect(520,150,26,120),R,-31,31,r=8)
    m.prism(rect(600,150,14,120),G,-31,31,r=5,emit=False);label(m,'Mündungsring')
    return m
