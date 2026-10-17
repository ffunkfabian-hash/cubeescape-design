from helpers import *
from ctrig import trigger,rail
J,JD,BR,F,JH,BRH,BRD,BO='#0F766E','#0B3B37','#B4783C','#FF7A2E','#14A196','#D69A5C','#7A4E22','#E8E0D0'
def model():
    m=Model()
    m.prism([(40,186),(160,170),(166,260),(70,282),(40,274)],JD,-22,22,r=8);label(m,'Schaft')
    m.prism([(30,186),(44,186),(44,276),(30,274)],BR,-24,24,r=4)
    m.prism([(300,280),(342,280),(330,362),(290,362)],JD,-16,16,r=6);label(m,'Griff')
    trigger(m,346,286,F,'#0E4F4A',depth=72,w=40,xr=330,zt=5,zg=6)
    m.prism(circ(470,310,54,28),JD,-22,22,smooth=True);label(m,'Trommelmagazin')
    m.decal('z+',22,circ(470,310,40,28),BRD)
    m.decal('z+',22.3,circ(470,310,36,28),BR)
    m.decal('z+',22.6,circ(470,310,14,18),F,emit=True)
    for p in (rect(467.5,272,5,18),rect(467.5,330,5,18),rect(490,307.5,18,5),rect(432,307.5,18,5)):m.decal('z+',22.6,p,BRD)
    body=[(160,156),(520,150),(548,172),(548,272),(520,286),(180,286),(160,268)]
    m.prism(body,J,-32,32,r=10);label(m,'Gehäuse')
    m.decal('z+',32,[(162,158),(520,152),(536,164),(166,170)],JH)
    m.decal('z+',32,roundpoly([(160,252),(548,252),(548,272),(520,286),(180,286),(160,268)],5),JD)
    for x0 in (190,300):
        m.decal('z+',32,roundpoly([(x0,184),(x0+90,180),(x0+110,206),(x0+90,232),(x0,232)],4),BR)
        m.decal('z+',32.3,[(x0,184),(x0+90,180),(x0+94,188),(x0,192)],BRH)
    m.decal('z+',32,roundpoly(rect(420,196,100,10),3),F,emit=True)
    rail(m,226,352,141,'#0B3B37','#062724',z=10,h=12,slope=-1.5/126)
    # Visier separat: flaches Kastenvisier mit Feuer-Linse
    m.prism([(236,122),(326,120),(338,141),(230,141)],JD,-10,10,r=4);label(m,'Kastenvisier');sight(m)
    m.decal('x+',338,[(126,-6),(126,6),(136,6),(136,-6)],F,emit=True)
    # Drachenmaul
    # Lauf tritt aus dem Gehaeuse ins Maul, der Feuerkern sitzt auf der Laufmuendung
    m.cyl(548,628,218,0,17,'#16524C');label(m,'Lauf')
    m.prism(ell(652,218,30,17),F,-16,16,emit=True,smooth=True)
    m.decal('z+',16,ell(642,218,16,8),'#FFD3A8',emit=True)
    m.prism([(548,254),(620,238),(640,270),(548,266)],BRD,-20,20)
    m.prism([(620,238),(700,250),(742,290),(716,300),(640,270)],BRD,-20,20)
    for t in ([(700,250),(712,236),(690,242)],[(680,244),(690,228),(670,236)]):m.prism(t,BO,-12,12)
    m.prism([(548,166),(640,160),(620,196),(548,200)],BR,-20,20)
    m.decal('z+',20,[(550,168),(640,162),(638,170),(550,176)],BRH)
    m.decal('z+',20,circ(600,180,6,12),F,emit=True)
    m.prism([(640,160),(716,128),(742,140),(700,184),(620,196)],BR,-20,20);label(m,'Drachenmaul')
    m.decal('z+',20,[(642,162),(716,130),(726,134),(640,170)],BRH)
    for t in ([(700,184),(712,198),(690,192)],[(680,190),(690,206),(670,198)]):m.prism(t,BO,-12,12)
    return m
