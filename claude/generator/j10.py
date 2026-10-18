import math
from jlib import *
BK,IC,GM,DK='#22272F','#9EE7FF','#626A76','#101216'
def quads(pts,w0,w1):
    """Band entlang einer Linie als Vierecke (je Segment ein Facettenteil), Breite w0 → w1"""
    n=len(pts);L=[];R=[]
    for i,p in enumerate(pts):
        w=(w0+(w1-w0)*i/(n-1))/2;a=pts[max(i-1,0)];b=pts[min(i+1,n-1)]
        d=(b[0]-a[0],b[1]-a[1]);l=math.hypot(*d);nm=(-d[1]/l,d[0]/l)
        L.append((p[0]+nm[0]*w,p[1]+nm[1]*w));R.append((p[0]-nm[0]*w,p[1]-nm[1]*w))
    return [[L[i],L[i+1],R[i+1],R[i]] for i in range(n-1)]
UP=[(382,190),(374,160),(358,128),(336,102),(312,82)]
CX,CT,CB,CR=300,72,528,16
def limb(sign):
    q=quads([(x,300+sign*(y-300)) for x,y in UP],26,12)
    out=[]
    for k,p in enumerate(q):
        if sign>0:p=p[::-1]
        out.append(K(p,BK,-10,10,b=2.5,bz=4,label='Wurfarm',glow=[((1,),IC,1.6)] if k%2==0 else []))
    return out
def cam(cy):
    s=1 if cy<300 else -1
    return [K(circ(CX,cy,CR,8),GM,-6,6,b=2,bz=2,label='Umlenkrolle',dec=[(circ(CX,cy,8,8),DK,False)]),
            K(circ(CX,cy,5,6),DK,-13,13,b=1,bz=1),
            K([(CX-4,cy),(CX+8,cy),(CX+14,cy+20*s),(CX+2,cy+20*s)],DK,-13,-8,b=1,bz=1),
            K([(CX-4,cy),(CX+8,cy),(CX+14,cy+20*s),(CX+2,cy+20*s)],DK,8,13,b=1,bz=1)]
def spec():
    s=limb(-1)+limb(1)+cam(CT)+cam(CB)
    s+=[
    K([(362,184),(402,190),(404,280),(364,280)],BK,-12,12,b=4,bz=4,label='Mittelstück',glow=[((1,),IC,2.0)]),
    K(rect(364,280,40,40),BK,-14,-4,b=2,bz=2),
    K([(364,320),(404,320),(402,414),(362,416)],DK,-12,12,b=4,bz=4,label='Griff'),
    K(rect(360,176,46,14),GM,-14,14,b=3,bz=3),
    K(rect(360,410,46,14),GM,-14,14,b=3,bz=3),
    K(rect(CX-CR-1.5,CT,3,CB-CT),IC,-1.5,1.5,b=0,bz=0,label='Sehne'),
    K(rect(366,303,30,5),GM,-4,3.5,b=1,bz=1,label='Pfeilauflage'),
    X(CX-CR+2,560,300,3,'#C8D2DC',n=6,label='Pfeil'),
    T(560,586,300,7,1,IC,n=6),
    K(rect(CX-CR-4,296,10,8),DK,-3,3,b=1,bz=1),
    K([(CX-CR+12,300),(CX-CR+36,291),(CX-CR+36,300)],IC,-0.8,0.8,b=0,bz=0),
    K([(CX-CR+12,300),(CX-CR+36,300),(CX-CR+36,309)],IC,-0.8,0.8,b=0,bz=0),
    K(rect(404,226,30,8),DK,-4,4,b=1,bz=1),
    # --- Pin-Visier separat
    K(rect(432,208,18,34),BK,-8,8,b=3,bz=3,sight=True,label='Visier',xdec=[('x-',432,rect(222,-3,6,6),IC,True)]),   # Leuchtpunkt auf der Rückseite, zum Schützen (claude-0.7; bis 0.6 seitlich)
    X(404,488,372,6,DK,n=6,label='Stabilisator'),
    T(488,510,372,8,11,GM,n=6),
    ]
    return s
META=dict(sight=('pin','glass'),num='10',name='Bogen',nick='NORTHWIND',col=IC,pill='NORDNACHT · EISBLAU · GUNMETAL',palette=[BK,IC,GM,DK],center=(400,300,0),
 desc='Stealth-Compoundbogen der Black-Ice-Serie: Die Wurfarme sind aus Facettensegmenten mit eisblauen Leuchtkanten gebaut, das Mittelstück ist ein kantiger Keil mit Pfeilfenster und Gunmetal-Klemmplatten. Achtkant-Umlenkrollen laufen in Gabelwangen, die Sehne liegt tangential an ihrer Vorderseite. Pfeil auf der Auflage, sechskantiger Stabilisator. Das Pin-Visier ist separat.',
 form='Facettierte Wurfarme mit Leuchtkanten · Keil-Mittelstück mit Pfeilfenster · Klemmplatten · Achtkant-Umlenkrollen in Gabelwangen · tangentiale Sehne · Pfeil auf Auflage · Stabilisator · Pin-Visier separat')
