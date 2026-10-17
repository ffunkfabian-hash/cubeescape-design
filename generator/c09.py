from ext import *
from smooth import stube
from ctrig import trigger
CR,CR2,GN,GN2,DK,RD,RD2,RDD='#EDE3C8','#CFC3A2','#3F4A2C','#55623B','#1E2416','#EF4444','#F87171','#B91C1C'
def model():
    m=Model()
    m.prism([(310,246),(350,246),(340,350),(300,350)],GN,-18,18,r=6);label(m,'Griff')
    trigger(m,352,252,RD,GN,depth=72,w=42,xr=342,zt=4,zg=6)
    m.prism([(440,246),(476,246),(470,330),(434,330)],GN,-16,16,r=6);label(m,'Vordergriff')
    frustum(m,20,90,212,0,70,38,GN);label(m,'Trichterheck')
    m.decal('x-',20,circ(212,0,62,32),DK)
    for a,b in ((90,140),(180,400),(440,600),(630,650)):
        m.cyl(a,b,212,0,42,CR,n=32);label(m,'Abschussrohr')
    m.decal('z+',41.5,roundpoly(rect(210,196,160,10),3),GN)
    m.decal('z+',41.5,roundpoly(rect(210,214,110,10),3),GN)
    for a,b in ((140,180),(400,440),(600,630)):
        m.cyl(a,b,212,0,46,GN,n=32)
    for z0,z1,pl,z in ((36,46,'z+',46),(-46,-36,'z-',-46)):
        m.prism(roundpoly(rect(460,194,40,30),6),RD,z0,z1);label(m,'Sicherungsmodul')
        m.decal(pl,z,[(467,200),(471,200),(493,218),(489,218)],CR,both=False)
        m.decal(pl,z,[(489,200),(493,200),(471,218),(467,218)],CR,both=False)
    # Visierschiene seitlich LINKS am Rohr (wie RPG-7/Carl Gustaf: das Rohr wuerde eine mittige Sichtlinie verdecken)
    for x0 in (240,530):m.prism(rect(x0,170,30,22),GN2,18,47,r=3)          # Montageklammern greifen ins Rohr
    m.prism(rect(214,170,358,11),GN2,44,56,r=2);label(m,'Visierschiene')
    for x in range(222,566,14):m.decal('y-',170,rect(x,45,7,10),DK)
    # Visier separat: Ringvisier hinten, Korn vorn – beide auf der seitlichen Schiene
    m.prism(rect(250,132,12,39),GN,46,54,r=3);sight(m)
    ring=[(256+16*math.cos(2*math.pi*i/36),116+16*math.sin(2*math.pi*i/36),50) for i in range(36)]
    stube(m,ring,3,GN2,k=10,closed=True);label(m,'Ringvisier');sight(m)
    stube(m,[(241,116,50),(271,116,50)],1.4,GN2,k=6);sight(m)
    stube(m,[(256,101,50),(256,131,50)],1.4,GN2,k=6);sight(m)
    m.prism(rect(541,140,10,31),GN,46,54,r=2);sight(m)
    m.prism([(530,130),(562,130),(558,140),(534,140)],GN,43,57);label(m,'Korn');sight(m)
    m.cyl(650,670,212,0,36,GN,n=32)
    m.decal('x+',670,circ(212,0,24,28),DK)
    m.cyl(670,716,212,0,16,RD,n=24)
    m.cyl(680,688,212,0,16.6,RDD,n=24)
    frustum(m,716,750,212,0,16,2,RD);label(m,'Rakete')
    return m
CENTER=(385,230,0)
META=dict(name='Raketenwerfer',var='RETRO-ROHR',col='#EF4444',pill='CREME · ARMEEGRÜN · ROT',
 desc='Langes Abschussrohr mit grünen Verstärkungsringen und trichterförmigem Abgasheck. Griff mit Abzug und Vordergriff sitzen direkt unter dem Rohr, Ringvisier und Korn sind separat gezeichnet; ihre Schiene sitzt seitlich links am Rohr (das Rohr würde eine mittige Sichtlinie verdecken). Vorne ragt die rote Rakete aus der Mündung.',
 pal=['#EDE3C8','#CFC3A2','#3F4A2C','#EF4444'],form='Einzelrohr mit Verstärkungsringen · Trichterheck · Visierschiene seitlich links (Ringvisier und Korn separat) · Griff mit Abzug, Vordergriff · beidseitiges Sicherungsmodul')
