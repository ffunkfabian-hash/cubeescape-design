import math
def _norm(v):
    L=math.sqrt(sum(x*x for x in v)) or 1;return tuple(x/L for x in v)
def stube(m,path,rad,col,k=10,emit=False,closed=False):
    """Glattes Rohr entlang Polylinie als EIN Teil mit korrekten Normalen (keine Segmentfugen)."""
    pts=path[:-1] if closed and path[0]==path[-1] else path
    n=len(pts);rings=[];cents=[]
    for i in range(n):
        if closed:a,b=pts[i-1],pts[(i+1)%n]
        else:a,b=pts[max(i-1,0)],pts[min(i+1,n-1)]
        d=_norm([b[j]-a[j] for j in range(3)])
        if i==0:
            up=(0,1,0) if abs(d[1])<0.9 else (1,0,0)
            u=_norm([d[1]*up[2]-d[2]*up[1],d[2]*up[0]-d[0]*up[2],d[0]*up[1]-d[1]*up[0]])
        else:  # Parallel-Transport: u gegen neue Tangente orthogonalisieren
            dot=sum(u[j]*d[j] for j in range(3));u=_norm([u[j]-dot*d[j] for j in range(3)])
        w=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
        p=pts[i];rings.append([tuple(p[j]+rad*(math.cos(2*math.pi*q/k)*u[j]+math.sin(2*math.pi*q/k)*w[j]) for j in range(3)) for q in range(k)]);cents.append(p)
    F=[]
    segs=range(n) if closed else range(n-1)
    for i in segs:
        i2=(i+1)%n;ra,rb=rings[i],rings[i2];ca,cb=cents[i],cents[i2]
        for q in range(k):
            q2=(q+1)%k;v=[ra[q],ra[q2],rb[q2],rb[q]]
            mid=[sum(p[j] for p in v)/4 for j in range(3)];cm=[(ca[j]+cb[j])/2 for j in range(3)]
            F.append(dict(v=v,n=_norm([mid[j]-cm[j] for j in range(3)]),hard=False))
    if not closed:
        for r,c,a,b in ((rings[0],cents[0],pts[0],pts[1]),(rings[-1],cents[-1],pts[-1],pts[-2])):
            F.append(dict(v=r,n=_norm([a[j]-b[j] for j in range(3)]),hard=True))
    m.parts.append(dict(F=F,col=col,emit=emit,dec=[],nohull=True));return m
def storus(m,xc,cy,cz,R,rt,col,n=40,emit=False,k=10):
    path=[(xc,cy+R*math.sin(2*math.pi*i/n),cz+R*math.cos(2*math.pi*i/n)) for i in range(n)]
    return stube(m,path,rt,col,k=k,emit=emit,closed=True)
