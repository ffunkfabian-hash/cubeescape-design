import math
from eng import *
def strip(pts,w):
    L=[];R=[]
    for i,p in enumerate(pts):
        a=pts[max(i-1,0)];b=pts[min(i+1,len(pts)-1)]
        dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy) or 1;nx,ny=-dy/l*w/2,dx/l*w/2
        L.append((p[0]+nx,p[1]+ny));R.append((p[0]-nx,p[1]-ny))
    return L+R[::-1]
def ell(cx,cy,rx,ry,n=24):return [(cx+rx*math.cos(2*math.pi*k/n),cy+ry*math.sin(2*math.pi*k/n)) for k in range(n)]
def qbez(p0,p1,p2,n=8):return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/n for i in range(n+1)]]
def guard(x0,y0,x1,y1,x2,y2,w=8):  # Abzugbuegel als Band
    return strip([(x0,y0),(x1,y0),(x2,y1),(x2-36+0,y2)] ,w)
def chain(m,pts,w,col,z0,z1,emit=False):
    # nicht-konvexe Baender als Kette konvexer Teilstuecke
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy) or 1
        ex,ey=dx/l*w*0.25,dy/l*w*0.25;nx,ny=-dy/l*w/2,dx/l*w/2
        a2=(a[0]-ex*(i>0),a[1]-ey*(i>0));b2=(b[0]+ex*(i<len(pts)-2),b[1]+ey*(i<len(pts)-2))
        m.prism([(a2[0]+nx,a2[1]+ny),(b2[0]+nx,b2[1]+ny),(b2[0]-nx,b2[1]-ny),(a2[0]-nx,a2[1]-ny)],col,z0,z1,emit=emit,hull=False)
def tguard(m,x0,y0,col,s=1.0):
    # Abzugbuegel: Unterkante + Vorderstrebe, beide konvex
    m.prism([(x0,y0+30*s),(x0+30*s,y0+28*s),(x0+30*s,y0+36*s),(x0,y0+38*s)],col,-5,5)
    m.prism([(x0+28*s,y0),(x0+36*s,y0),(x0+30*s,y0+36*s),(x0+24*s,y0+34*s)],col,-5,5)
