from ext import *
from smooth import stube
from ctrig import trigger,rail
G,G2,S,SL,D,L,LL='#2A2D34','#3C4049','#B8BEC8','#DDE1E7','#1C1E23','#A78BFA','#EDE7FF'
def model():
    m=Model()
    m.prism([(34,176),(150,162),(150,260),(60,276),(34,268)],G,-24,24,r=8);label(m,'Schaft')
    m.decal('z+',24,roundpoly([(36,178),(150,164),(150,174),(40,188)],3),G2)
    m.decal('z+',24,roundpoly([(56,196),(128,188),(128,238),(62,246)],5),S)
    m.prism([(280,276),(320,276),(308,356),(268,356)],D,-18,18,r=6);label(m,'Griff')
    trigger(m,322,280,L,'#33363E',depth=74,w=40,xr=310,zt=4,zg=6)
    # Energiezelle hinter dem Griff, ragt deutlich unter das Gehaeuse
    m.prism(rect(176,270,88,74),D,-22,22,r=10);label(m,'Energiezelle')
    m.decal('z+',22,roundpoly(rect(188,314,56,14),5),L,emit=True)
    m.prism([(150,150),(400,150),(426,172),(426,262),(400,280),(170,280),(150,262)],G,-34,34,r=10);label(m,'Gehäuse')
    m.decal('z+',34,roundpoly([(152,152),(400,152),(414,164),(156,164)],3),G2)
    m.decal('z+',34,roundpoly([(180,180),(330,180),(340,206),(330,232),(180,232)],5),S)
    m.decal('z+',34.2,roundpoly([(182,181),(330,181),(334,190),(182,190)],3),SL)
    m.prism(circ(380,206,20,24),D,-39,39,smooth=True)
    m.decal('z+',39,circ(380,206,10,20),L,emit=True)
    rail(m,206,354,140,D,'#0E0F12',z=12,h=11)
    # Visier separat: Zielfernrohr-Block mit Lavendel-Linse
    m.prism([(220,140),(220,124),(232,112),(338,112),(350,124),(350,140)],D,-14,14,r=5);label(m,'Zielvisier');sight(m)
    m.decal('x+',350,circ(126,0,8,16),L,emit=True)
    m.cyl(426,716,208,0,12,D,n=28);label(m,'Lauf')
    m.prism(rect(430,176,14,64),S,-30,30,r=4)
    m.prism(rect(716,180,30,56),S,-26,26,r=8)
    m.decal('x+',746,circ(208,0,12),D)
    m.decal('x+',746.5,circ(208,0,6),L,emit=True)
    turns=3.5;n=int(turns*18)
    pts=[(446+268*i/n,208-15.6*math.sin(2*math.pi*turns*i/n),15.6*math.cos(2*math.pi*turns*i/n)) for i in range(n+1)]
    stube(m,pts,3.6,'#C4B5FD',k=10);label(m,'Energiespule')
    return m
CENTER=(390,236,0)
META=dict(name='Spurgewehr',var='SPIRALE',col='#A78BFA',pill='GRAPHIT · SILBER · LAVENDEL',
 desc='Die Lavendel-Energiespule liegt direkt auf dem Lauf und läuft vom silbernen Laufring bis zur Mündung. Der Fokus-Kern steht beidseitig als runder Knopf aus dem Gehäuse, die Energiezelle ragt hinter dem Griff unter das Gehäuse. Das Zielvisier ist separat gezeichnet, auf dem Gehäuse bleibt die Schiene.',
 pal=['#2A2D34','#B8BEC8','#1C1E23','#A78BFA'],form='Energiespule auf dem Lauf · Laufring und Mündungsblock als Halter · Fokus-Kern beidseitig · Energiezelle hinter dem Griff · Visierschiene (Visier separat)')
