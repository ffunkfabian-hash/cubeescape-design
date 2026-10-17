from ext import *
from ctrig import trigger
K,K2,M,MP,Y='#1A1A1F','#2B2B33','#EC4899','#F9A8D4','#FACC15'
def band(x0,x1,y0,dep,w):
    o=[(x0+(x1-x0)*t,y0+4*t*(1-t)*dep) for t in [i/10 for i in range(11)]]
    i=[(x0+w+(x1-x0-2*w)*t,y0+4*t*(1-t)*(dep-w)) for t in [i/10 for i in range(11)]][::-1]
    return o+i
def model():
    m=Model()
    for z in (-11,11):
        tube(m,[(200,180,z),(72,172,z)],5,K,k=6,nohull=False)
        tube(m,[(200,270,z),(72,276,z)],5,K,k=6,nohull=False)
    m.prism(rect(60,164,18,124),K,-22,22,r=6);label(m,'Schaft')
    m.decal('z+',22,roundpoly(rect(62,190,14,70),4),Y)
    m.prism([(330,280),(390,280),(380,440),(318,440)],K,-22,22,r=8);label(m,'Griff')
    m.decal('z+',22,roundpoly([(340,300),(380,300),(372,420),(330,420)],5),K2)
    for i,yy in enumerate((320,340,360,380,400)):m.decal('z+',22,roundpoly(rect(344-2*i,yy,28,8),2),'#7A2550')
    m.prism(rect(314,436,72,14),Y,-26,26,r=4);label(m,'Magazin')
    trigger(m,394,280,Y,K2,depth=76,w=44,xr=382,zt=4,zg=6)
    m.prism([(200,170),(520,170),(546,192),(546,280),(200,280),(186,264),(186,186)],K,-34,34,r=10);label(m,'Gehäuse')
    m.decal('z+',34,roundpoly([(202,172),(518,172),(532,184),(196,184)],3),K2)
    m.decal('z+',34,roundpoly(rect(214,206,160,8),3),M,emit=True)
    m.decal('z+',34,roundpoly(rect(408,230,64,32),5),Y,both=False)
    m.decal('z+',34.3,roundpoly(rect(414,235,52,22),4),'#0B0B0E',both=False)
    m.prism(rect(250,146,160,26),K,-16,16,r=5);label(m,'Visierschiene')
    for x in range(258,404,14):m.decal('y-',146,rect(x,-13,7,26),K2)
    # Visier separat: Kimme hinten, Korn vorn (aufgesteckt auf die Schiene)
    m.prism(rect(266,132,28,15),K2,-10,10,r=3);label(m,'Kimme');sight(m)
    m.decal('x-',266,[(134,-4),(134,4),(140,4),(140,-4)],M,emit=True)
    m.prism(rect(368,132,24,15),K2,-8,8,r=3);label(m,'Korn');sight(m)
    m.prism(rect(376,120,8,13),K2,-3,3,r=1);sight(m)
    m.decal('z+',3,circ(380,124,2.5,10),M,emit=True)
    m.prism(rect(546,200,80,54),K2,-26,26,r=8);label(m,'Mündung')
    for xx in (556,576,596):m.decal('z+',26,roundpoly(rect(xx,210,12,34),3),K)
    m.cyl(626,656,227,0,14,K)
    m.decal('x+',656,circ(227,0,9),M,emit=True)
    m.decal('x+',656.5,circ(227,0,4.5),'#FCE7F3',emit=True)
    return m
CENTER=(360,300,0)
META=dict(name='Maschinenpistole',var='NEON',col='#F472B6',pill='SCHWARZ · MAGENTA · GELB',
 desc='Kompakte MP: Das Magazin steckt im Pistolengriff, der Abzug sitzt im Bügel direkt davor. Oben läuft die Visierschiene, Kimme und Korn sind separat gezeichnet, vorne die belüftete Mündung, hinten der Drahtschaft aus zwei Bügeln.',
 pal=['#1A1A1F','#2B2B33','#EC4899','#FACC15'],form='Magazin im Pistolengriff · Abzug im Bügel · Visierschiene (Visier separat) · Auswurföffnung · Drahtschaft aus zwei Bügeln · belüftete Mündung')
