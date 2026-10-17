from ext import *
from smooth import stube
from ctrig import trigger
K,K2,G,GD,R,RL,RW='#18161A','#2E2A31','#D4A84B','#9C7A30','#EF4444','#FCA5A5','#FEE2E2'
def bez(p0,p1,p2,p3,n=14):
    return [tuple((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i] for i in range(2)) for t in [k/n for k in range(n+1)]]
def limb(m,sg):
    c=bez((556,12*sg),(566,60*sg),(562,110*sg),(592,158*sg))
    L=[];Rr=[]
    for i,p in enumerate(c):
        a=c[max(i-1,0)];b=c[min(i+1,len(c)-1)];dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz)
        w=7-2.5*i/len(c);nx,nz=-dz/l*w,dx/l*w
        L.append((p[0]+nx,p[1]+nz));Rr.append((p[0]-nx,p[1]-nz))
    prism_y(m,L+Rr[::-1],G,-6,6);label(m,'Wurfarm')
    for f in m.parts[-1]['F'][2:]:f['hard']=False
    m.parts[-1]['nohull']=True
    return c[-1]
def model():
    m=Model()
    prism_y(m,[(40,-18),(120,-24),(380,-14),(560,-10),(560,10),(380,14),(120,24),(40,18)],K,-14,14,r=6);label(m,'Schaft')
    decal_y(m,-14,roundpoly([(60,-12),(120,-17),(370,-9),(370,-3),(120,-6),(60,-4)],3),K2)
    prism_y(m,roundpoly(rect(28,-25,20,50),5),G,-17,17)
    prism_y(m,roundpoly(rect(160,-10,160,20),4),G,-19,-14);m.parts[-1]['bias']=40;label(m,'Wangenauflage')
    for xx in (180,200,220,240,260,280,300):decal_y(m,-19,rect(xx,-9,3,18),GD)
    m.prism([(300,14),(336,14),(330,82),(294,82)],K,-10,10,r=5);label(m,'Griff')
    trigger(m,338,14,R,K2,depth=52,w=36,xr=330,zt=4,zg=5)
    prism_y(m,roundpoly(rect(400,-30,80,60),9),K,-15,18);label(m,'Spannmechanik')
    decal_y(m,-15,circ(440,-16,10,24),R,emit=True)
    decal_y(m,-15.3,circ(437,-19,3.5,14),RW,emit=True)
    m.prism(rect(404,-29,12,14),K2,-6,6,r=2);label(m,'Kimme');sight(m)
    m.prism(rect(406,-37,8,9),K2,-6,-2,r=1);sight(m)
    m.prism(rect(406,-37,8,9),K2,2,6,r=1);sight(m)
    # Bolzen
    stube(m,[(396,-17.6,0),(656,-17.6,0)],2.6,RL,k=10);label(m,'Bolzen')
    prism_y(m,[(654,-12),(696,0),(654,12),(664,0)],G,-20.6,-14.6)
    prism_y(m,[(382,-10),(398,0),(382,10)],G,-21,-14)
    tips=[limb(m,s) for s in (-1,1)]
    for (x,z),s in zip(tips,(-1,1)):
        prism_y(m,roundpoly([(x-6,z-6*s),(x+8,z+2*s),(x+4,z+10*s),(x-10,z+2*s)],2),R,-7,7)
        stube(m,[(x,-1,z),(390,-18,0)],1.8,RL,k=8);label(m,'Sehne')
    prism_y(m,roundpoly(rect(540,-24,40,48),7),K,-15,16)
    decal_y(m,-15,roundpoly(rect(548,-10,24,20),3),R,emit=True)
    m.prism(rect(558,-29,10,14),K2,-5,5,r=2);label(m,'Korn');sight(m)
    m.prism(rect(561,-39,4,11),K2,-2,2,r=1);sight(m)
    m.decal('z+',2,circ(563,-36,1.6,8),R,emit=True)
    return m
CENTER=(368,10,0)
META=dict(name='Bogen',var='ARMBRUST',col='#F87171',pill='SCHWARZ · GOLD · ROT',
 desc='Armbrust-Version des Bogens: Die goldenen Wurfarme sitzen im vorderen Bogenblock, die Sehne läuft zur Spannmechanik zurück. Der Energiebolzen liegt in der Schiene; Kimme (Spannmechanik) und Korn (Bogenblock) sind separat gezeichnet. Griff mit Abzug unter dem Schaft, Wangenauflage hinten.',
 pal=['#18161A','#2E2A31','#D4A84B','#EF4444'],form='Schaft mit Wangenauflage · Griff mit Abzug · Spannmechanik · Bogenblock · Kimme und Korn separat · Gold-Wurfarme · Energiebolzen')
