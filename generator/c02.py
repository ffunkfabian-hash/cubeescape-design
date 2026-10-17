from helpers import *
from ctrig import trigger,rail
G,O,D,OR,OL2,HI,OLD,ORL='#2F4F3A','#6B7F4E','#1C2A20','#FF8C1A','#86996A','#41664F','#4E5D38','#FFB866'
def model():
    m=Model()
    m.prism([(30,176),(60,176),(60,262),(30,258)],D,-22,22,r=6)
    m.prism(rect(60,196,100,16),D,-9,9,r=4)
    m.prism(rect(60,230,100,16),D,-9,9,r=4)
    m.prism([(60,176),(100,176),(100,262),(60,262)],G,-24,24,r=6);label(m,'Schaft')
    # Magazin (nach vorn versetzt, damit der Abzugsbereich frei bleibt)
    m.prism([(350,268),(394,268),(402,312),(356,318)],D,-14,14,r=3);label(m,'Magazin')
    m.decal('z+',14,strip([(362,284),(366,312)],4),OR,emit=True)
    m.prism([(356,316),(402,310),(416,342),(376,352)],D,-14,14,r=3)
    m.decal('z+',14,strip([(366,320),(380,346)],4),OR,emit=True)
    m.prism([(236,268),(276,268),(264,352),(224,352)],D,-16,16,r=6);label(m,'Griff')
    # Abzug + Buegel deutlich unter dem Gehaeuse
    trigger(m,286,272,OR,'#24382B',depth=68,w=42,xr=266,zt=5,zg=6)
    body=[(160,160),(420,160),(440,176),(440,262),(420,272),(170,272),(160,262)]
    m.prism(body,G,-30,30,r=10);label(m,'Gehäuse')
    m.decal('z+',30,[(162,162),(420,162),(430,170),(164,170)],HI)
    m.decal('z+',30,roundpoly([(160,246),(440,246),(440,262),(420,272),(170,272),(160,262)],5),D)
    m.decal('z+',30,roundpoly(rect(190,190,110,36),5),O)
    m.decal('z+',30,roundpoly(rect(200,204,80,6),2),OR,emit=True)
    for x in (330,360,390):m.decal('z+',30,rect(x-1.5,186,3,50),D)
    m.prism(rect(184,124,14,38),D,-8,8,r=3)
    m.prism(rect(392,124,14,38),D,-8,8,r=3)
    m.prism(rect(186,108,220,16),O,-11,11,r=6);label(m,'Tragegriff')
    # Visier separat: Diopter hinten, Korn vorn – sitzt auf dem Tragegriff (Schienenprofil oben)
    for x in range(196,400,14):m.decal('y-',108,rect(x,-9,7,18),OLD)
    m.prism(rect(198,92,28,17),D,-10,10,r=3);label(m,'Diopter');sight(m)
    m.decal('z+',10,circ(212,99,4,12),'#060807')
    m.prism(rect(382,98,24,11),D,-8,8,r=2);label(m,'Korn');sight(m)
    m.prism(rect(390,84,8,15),D,-3,3,r=1);sight(m)
    m.prism([(440,170),(560,176),(560,246),(440,252)],O,-24,24,r=6);label(m,'Handschutz')
    m.decal('z+',24,[(442,172),(558,178),(558,186),(442,182)],OL2)
    for y in (200,220):m.decal('z+',24,rect(460,y-2.5,80,5),OLD)
    m.prism([(472,250),(500,250),(496,304),(476,304)],D,-10,10,r=6)
    xs=[560,596,604,636,644,676,684,750]
    for i in range(len(xs)-1):
        a,b=xs[i],xs[i+1]
        if i%2==1:m.cyl(a,b,211,0,27,ORL,emit=True)
        else:m.cyl(a,b,211,0,25,D);label(m,'Schalldämpfer')
    m.decal('x+',750,circ(211,0,11),'#060807')
    m.decal('x+',750.5,circ(211,0,5),OR,emit=True)
    return m
