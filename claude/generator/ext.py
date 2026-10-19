import math
from eng import *
def _n(v,c):
    nx=ny=nz=0
    for i in range(len(v)):
        a,b=v[i],v[(i+1)%len(v)]
        nx+=(a[1]-b[1])*(a[2]+b[2]);ny+=(a[2]-b[2])*(a[0]+b[0]);nz+=(a[0]-b[0])*(a[1]+b[1])
    L=math.sqrt(nx*nx+ny*ny+nz*nz) or 1;n=(nx/L,ny/L,nz/L)
    m=[sum(p[i] for p in v)/len(v) for i in range(3)]
    if sum((m[i]-c[i])*n[i] for i in range(3))<0:n=(-n[0],-n[1],-n[2])
    return n
def mesh(m,faces,col,hard=True,emit=False,nohull=False,soft=None):
    pts=[p for f in faces for p in f];c=[sum(p[i] for p in pts)/len(pts) for i in range(3)]
    F=[]
    for k,f in enumerate(faces):
        h=hard if soft is None else (k not in soft)
        F.append(dict(v=f,n=_n(f,c),hard=h))
    m.parts.append(dict(F=F,col=col,emit=emit,dec=[],nohull=nohull));return m
def prism_y(m,poly,col,y0,y1,r=0,emit=False,hardsides=False,winding=False):
    """Polygon in (x,z) vertikal von y0 (oben) bis y1 extrudiert."""
    if r:poly=roundpoly(poly,r)
    top=[(x,y0,z) for x,z in poly];bot=[(x,y1,z) for x,z in poly]
    n=len(poly);faces=[top,bot[::-1]]
    for i in range(n):
        a,b=poly[i],poly[(i+1)%n];faces.append([(a[0],y0,a[1]),(b[0],y0,b[1]),(b[0],y1,b[1]),(a[0],y1,a[1])])
    mesh(m,faces,col,emit=emit,soft=None if (hardsides or not r) else set(range(2,2+n)))
    if not winding:return m   # ältere Modelle (KC10 …) unverändert
    # winding (claude-0.11, tlib.B.Y): Seitenflächen-Normale aus dem Umlaufsinn statt vom Schwerpunkt weg. Bei hohlen Grundrissen (C-Bögen: Parierstange,
    # Schildflügel, gebogene Wurfarme) zeigte die Schwerpunkt-Regel an den Innenkanten nach innen, die Flächen fielen in den Orthos weg.
    A=sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n));sg=1 if A>0 else -1
    for i in range(n):
        a,b=poly[i],poly[(i+1)%n];dx,dz=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dz)
        if L<=1e-9:continue
        F=m.parts[-1]['F'][2+i];nx,nz=sg*dz/L,-sg*dx/L
        if F['n'][0]*nx+F['n'][2]*nz<0:F['n']=(-F['n'][0],-F['n'][1],-F['n'][2])   # nur umdrehen: konvexe Grundrisse bleiben bitgleich
    return m
def decal_y(m,val,pts,col,emit=False):
    m.parts[-1]['dec'].append(('y-',val,pts,col,emit));return m
def frustum(m,x0,x1,cy,cz,R0,R1,col,n=24,emit=False):
    r0=[(cy+R0*math.sin(2*math.pi*k/n),cz+R0*math.cos(2*math.pi*k/n)) for k in range(n)]
    r1=[(cy+R1*math.sin(2*math.pi*k/n),cz+R1*math.cos(2*math.pi*k/n)) for k in range(n)]
    faces=[[(x1,y,z) for y,z in r1],[(x0,y,z) for y,z in r0[::-1]]]
    for i in range(n):
        j=(i+1)%n;faces.append([(x0,*r0[i]),(x0,*r0[j]),(x1,*r1[j]),(x1,*r1[i])])
    return mesh(m,faces,col,emit=emit,soft=set(range(2,2+n)))
def tube(m,path,rad,col,k=6,emit=False,nohull=True):
    """Rohr entlang einer 3D-Polylinie, jedes Segment eigener Teil (sortiert sauber)."""
    for a,b in zip(path,path[1:]):
        d=[b[i]-a[i] for i in range(3)];L=math.sqrt(sum(x*x for x in d)) or 1;d=[x/L for x in d]
        up=(0,1,0) if abs(d[1])<0.9 else (1,0,0)
        u=[d[1]*up[2]-d[2]*up[1],d[2]*up[0]-d[0]*up[2],d[0]*up[1]-d[1]*up[0]];lu=math.sqrt(sum(x*x for x in u));u=[x/lu for x in u]
        w=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
        ring=lambda p:[tuple(p[i]+rad*(math.cos(2*math.pi*j/k)*u[i]+math.sin(2*math.pi*j/k)*w[i]) for i in range(3)) for j in range(k)]
        ra,rb=ring(a),ring(b);faces=[ra[::-1],rb]
        for j in range(k):faces.append([ra[j],ra[(j+1)%k],rb[(j+1)%k],rb[j]])
        mesh(m,faces,col,emit=emit,nohull=nohull,soft=set(range(0,2+k)) if nohull else set(range(2,2+k)))
    return m
def torus(m,xc,cy,cz,R,rt,col,n=28,emit=False,ry=None):
    ry=ry or R
    path=[(xc,cy+ry*math.sin(2*math.pi*i/n),cz+R*math.cos(2*math.pi*i/n)) for i in range(n+1)]
    return tube(m,path,rt,col,k=8,emit=emit)
def sphere(m,c,R,col,emit=False,n=14):
    faces=[]
    for i in range(n//2):
        t0,t1=math.pi*i/(n//2),math.pi*(i+1)/(n//2)
        for j in range(n):
            p0,p1=2*math.pi*j/n,2*math.pi*(j+1)/n
            P=lambda t,p:(c[0]+R*math.sin(t)*math.cos(p),c[1]+R*math.cos(t),c[2]+R*math.sin(t)*math.sin(p))
            f=[P(t0,p0),P(t0,p1),P(t1,p1),P(t1,p0)]
            if i==0:f=[f[0],f[2],f[3]]
            elif i==n//2-1:f=[f[0],f[1],f[2]]
            faces.append(f)
    return mesh(m,faces,col,emit=emit,soft=set(range(len(faces))))
def barrel(m,x0,x1,cy,cz,R,col,step=8,n=24):
    """Langer Lauf: Umriss-Teil ganz unten + viele kleine weiche Stuecke (saubere Sortierung)."""
    m.cyl(x0,x1,cy,cz,R,col,n=n);m.parts[-1]['bias']=-1000
    xs=list(range(int(x0),int(x1),step))+[x1]
    ring=[(cy+R*math.sin(2*math.pi*k/n),cz+R*math.cos(2*math.pi*k/n)) for k in range(n)]
    for a,b in zip(xs,xs[1:]):
        faces=[[(b,y,z) for y,z in ring],[(a,y,z) for y,z in ring[::-1]]]
        for i in range(n):
            j=(i+1)%n;faces.append([(a,*ring[i]),(a,*ring[j]),(b,*ring[j]),(b,*ring[i])])
        mesh(m,faces,col,nohull=True,soft=set(range(len(faces))))
    return m
