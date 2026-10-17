from ext import *
from smooth import storus
from ctrig import trigger,rail
W,WH,N,C,CL='#F1F5F9','#FFFFFF','#152238','#67E8F9','#E0FCFF'
def model():
    m=Model()
    m.prism([(40,180),(150,168),(150,260),(64,278),(40,270)],N,-26,26,r=8);label(m,'Schaft')
    m.prism([(30,180),(42,180),(42,272),(30,270)],C,-28,28,r=4)
    m.prism([(280,280),(320,280),(308,360),(268,360)],N,-18,18,r=6);label(m,'Griff')
    trigger(m,322,288,C,N,depth=74,w=40,xr=310,zt=4,zg=6)
    m.prism([(150,150),(380,150),(410,174),(410,266),(380,288),(170,288),(150,268)],W,-34,34,r=10);label(m,'Gehäuse')
    m.decal('z+',34,roundpoly([(152,152),(380,152),(396,164),(156,164)],3),WH)
    m.decal('z+',34,roundpoly([(152,248),(408,248),(408,264),(380,286),(170,286),(152,268)],4),N)
    m.decal('z+',34,roundpoly(rect(180,184,190,48),22),N)
    m.decal('z+',34,roundpoly(rect(192,196,130,24),11),C,emit=True)
    m.decal('z+',34,roundpoly(rect(200,200,50,8),4),CL,emit=True)
    rail(m,222,340,140,N,'#0A1220',z=11,h=11)
    # Visier separat: Reflexvisier mit Eiscyan-Linse
    m.prism([(232,140),(232,120),(244,110),(320,110),(330,120),(330,140)],N,-13,13,r=4);label(m,'Reflexvisier');sight(m)
    m.decal('x+',330,[(116,-8),(116,8),(134,8),(134,-8)],C,emit=True)
    # offener Rahmen: hintere und vordere Rahmenplatte, zwei Schienen, Fuehrungsdorn
    m.prism(rect(410,140,20,156),N,-14,14,r=4)
    m.prism(rect(426,140,304,10),N,-8,8,r=4);label(m,'Rahmen')
    m.prism(rect(426,286,304,10),N,-8,8,r=4);label(m,'Rahmen')
    m.prism(rect(726,140,18,156),N,-14,14,r=4)
    m.decal('x+',744,roundpoly(rect(208,-10,20,20),6),C,emit=True)
    m.cyl(430,726,218,0,6,'#2A3A58')
    for xx in (460,520,640,700):
        m.prism(rect(xx-6,150,12,9),N,-6,6,r=2)
        m.prism(rect(xx-6,277,12,9),N,-6,6,r=2)
    sphere(m,(580,218,0),24,C);label(m,'Energiekern')
    sphere(m,(574,212,6),10,CL)
    m.parts[-1]['bias']=5
    for xx in (460,520,640,700):storus(m,xx,218,0,58,7,W,n=40);label(m,'Beschleunigerring')
    return m
CENTER=(385,240,0)
META=dict(name='Fusionsgewehr',var='BESCHLEUNIGER',col='#67E8F9',pill='WEISS · NACHTBLAU · EISCYAN',
 desc='Statt eines Laufs ein offener Rahmen: Vier Beschleunigerringe sind oben und unten an den Schienen verschraubt, der Energiekern sitzt auf dem Führungsdorn in ihrer Mitte. Vorne schließt eine Rahmenplatte mit Austrittsöffnung ab. Das Reflexvisier ist separat gezeichnet, oben bleibt die Schiene.',
 pal=['#F1F5F9','#152238','#67E8F9','#E0FCFF'],form='Offener Rahmen mit zwei Schienen · vier Ringe auf Halteklammern · Energiekern auf Führungsdorn · Pistolengriff mit Abzug · Visierschiene (Visier separat)')
