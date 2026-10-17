from helpers import *
from ctrig import trigger,rail
P,PD,B,T,B2,TL='#E7E4EE','#A9A3B8','#141820','#2DD4BF','#262C38','#A7F3EA'
def model():
    m=Model()
    m.prism([(30,200),(140,160),(150,170),(150,250),(140,262),(40,240)],B,-20,20,r=6);label(m,'Schaft')
    m.decal('z+',20,[(40,200),(60,196),(60,236),(44,234)],T,emit=True)
    m.prism([(290,266),(330,266),(318,346),(278,346)],B,-14,14,r=6);label(m,'Griff')
    trigger(m,334,268,T,B,depth=72,w=40,xr=316,zt=5,zg=6)
    body=[(150,170),(280,120),(420,170),(440,210),(420,250),(280,290),(150,250),(140,210)]
    m.prism(body,P,-34,34,r=8);label(m,'Gehäuse')
    m.decal('z+',34,[(152,172),(280,124),(280,210),(144,210)],'#F7F5FB')
    m.decal('z+',34,[(280,124),(418,172),(436,210),(280,210)],'#D2CEDC')
    m.decal('z+',34,[(144,210),(280,210),(280,286),(152,248)],'#BDB8C9')
    m.decal('z+',34,[(280,210),(436,210),(418,248),(280,286)],PD)
    m.decal('z+',34,[(230,210),(280,166),(330,210),(280,254)],B)
    # Kristallkern steckt quer im Gehaeuse und tritt beidseitig leicht hervor
    m.prism([(244,210),(280,178),(316,210),(280,242)],T,-37,37,emit=True);label(m,'Kristallkern')
    m.decal('z+',37,[(248,210),(280,182),(280,210)],TL,emit=True)
    m.decal('z+',34,rect(170,208,50,4),B);m.decal('z+',34,rect(340,208,80,4),B)
    # Visierbasis auf dem Rautengrat (bleibt an der Waffe)
    m.prism([(244,133.8),(244,128),(254,112),(281,112),(281,119.6)],B,-11,11);label(m,'Visierschiene')
    m.prism([(279,119.6),(279,112),(306,112),(316,128),(316,133.8)],B,-11,11)
    for x in (258,270,286,298):m.decal('y-',112,rect(x,-8,6,16),B2)
    # Visier separat: facettiertes Kristall-Reflexvisier
    m.prism([(252,112),(252,100),(262,88),(300,88),(308,100),(308,112)],B2,-10,10,r=2);label(m,'Reflexvisier');sight(m)
    m.decal('x+',308,[(92,-6),(92,6),(108,6),(108,-6)],T,emit=True)
    m.decal('x-',252,[(94,-5),(94,5),(106,5),(106,-5)],TL)
    rings=[(500,510,36),(570,579,31),(632,640,26)]
    xs=[436]
    for a,b,_ in rings:xs+=[a,b]
    xs.append(700)
    for i in range(0,len(xs)-1,2):m.cyl(xs[i],xs[i+1],210,0,15,B);label(m,'Lauf')
    for a,b,R in rings:
        c=(a+b)/2
        m.cyl(c-2,c+2,210,0,R+4,T,emit=True)
        m.cyl(a,c-2,210,0,R,P);m.cyl(c+2,b,210,0,R,P)
    m.cyl(700,716,210,0,19,B2);label(m,'Mündung')
    m.decal('x+',716,circ(210,0,9),'#05070A');m.decal('x+',716.4,circ(210,0,5),T,emit=True)
    return m
