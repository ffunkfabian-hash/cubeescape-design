"""Geometry-only sight evidence: dense parallel-ray and solid collision checks."""
import numpy as np
from vs_models import contour


def inside_many(points,polygon):
    """Vectorized parity crossing, including concave polygons."""
    x,y=points.T;out=np.zeros(len(points),bool)
    for a,b in zip(polygon,np.roll(polygon,-1,axis=0)):
        if abs(b[1]-a[1])<1e-12:continue
        out^=((a[1]>y)!=(b[1]>y)) & (x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])
    return out


def aperture_rays(design,step=.5,margin=.3):
    w,h,c=design['opening'];r=design.get('bore')
    if r:w=h=r*2
    xs=np.arange(-w/2+margin,w/2-margin+1e-8,step)
    zs=np.arange(-h/2+margin,h/2-margin+1e-8,step)
    xx,zz=np.meshgrid(xs,zs);points=np.column_stack((xx.ravel(),zz.ravel()))
    shape='round' if r else design['shape']
    polygon=contour(w-2*margin,h-2*margin,shape,max(0,c-margin))
    return points[inside_many(points,polygon)]+np.asarray(design['reticle'])[[0,2]]


def aperture_blockers(parts,design):
    """All opaque faces through the full opening, not just the central ray.

    Parts and points are in the independent sight's millimetre frame (+Y rear).
    """
    points=aperture_rays(design);blocked=[]
    for part in parts:
        if part.material=='glass':continue
        if any(abs(f.normal[1])>1e-8 and inside_many(points,f.vertices[:,[0,2]]).any() for f in part.faces):blocked.append(part.label)
    return len(points),blocked


def weapon_aperture_clearance(parts,design,mount,mm):
    """Trace the complete opening from the eye/rear rim towards target -Y.

    Inputs use native model coordinates (+X forward); mm is mm/model unit.
    Bounds only reject impossible candidates. Every hit is on an actual face,
    including rays beginning inside an opaque solid. Sight parts are excluded.
    """
    from eng import bounds
    mount=np.asarray(mount)
    aperture=aperture_rays(design)
    points=np.column_stack((mount[1]-aperture[:,1]/mm,mount[2]+aperture[:,0]/mm))
    rear=max(design['rear'],design['eye'][1] if design['eye'] is not None else design['rear'])
    start=mount[0]-rear/mm
    weapons=[(i,p) for i,p in enumerate(parts) if not p.sight and p.material!='glass']
    end=max([start]+[bounds([p])[1][0] for _,p in weapons])+1000/mm
    blocked=np.zeros(len(points),bool);blockers=[]
    for index,part in weapons:
        lo,hi=bounds([part])
        candidate=np.all((points>=lo[1:]-1e-9)&(points<=hi[1:]+1e-9),axis=1)
        if hi[0]<start or lo[0]>end or not candidate.any():continue
        sample=points[candidate];hit=np.zeros(len(sample),bool);winding=np.zeros(len(sample))
        for face in part.faces:
            nx=face.normal[0]
            if abs(nx)<1e-9:continue
            inside=inside_many(sample,face.vertices[:,1:])
            x=face.vertices[0,0]-(sample-face.vertices[0,1:])@face.normal[1:]/nx
            hit|=inside&(x>=start-1e-9)&(x<=end+1e-9)
            winding+=inside*(x<start)*(-np.sign(nx))
        hit|=winding>0
        if hit.any():
            blocked[np.flatnonzero(candidate)[hit]]=True
            blockers.append(f'p{index:03d}')
    total=len(points);free=int((~blocked).sum())
    return {'rays':total,'free_rays':free,'free_fraction':free/total,
            'blocked_by':blockers,'line_clear_of_weapon':not bool(blocked.any()),
            'step_m':.0005,'margin_m':.0003}


def _ray_intervals(part,points):
    events=[]
    for face in part.faces:
        nx=face.normal[0]
        if abs(nx)<1e-9:continue
        valid=inside_many(points,face.vertices[:,1:])
        x=face.vertices[0,0]-(points-face.vertices[0,1:])@face.normal[1:]/nx
        events.append((np.where(valid,x,np.inf),np.where(valid,-np.sign(nx),0)))
    if not events:return np.empty((len(points),0)),np.empty((len(points),0)),np.empty((len(points),0),bool)
    x=np.array([e[0] for e in events]).T;sign=np.array([e[1] for e in events]).T
    order=np.argsort(x,axis=1);x=np.take_along_axis(x,order,axis=1);sign=np.take_along_axis(sign,order,axis=1)
    inside=np.cumsum(sign,axis=1)[:,:-1]>0
    return x[:,:-1],x[:,1:],inside


def solids_overlap(a,b,step,tolerance):
    """Independent solid-volume test using oriented parallel crossings.

    Union winding handles hollow shells and parts containing several solids;
    mere AABB overlap and touching mount surfaces do not count as collision.
    Sampling pitch and penetration tolerance are explicit physical quantities.
    """
    from eng import bounds
    alo,ahi=bounds([a]);blo,bhi=bounds([b]);lo=np.maximum(alo,blo);hi=np.minimum(ahi,bhi)
    if (hi-lo<=tolerance).any():return False
    axes=[np.linspace(lo[i]+tolerance/2,hi[i]-tolerance/2,max(2,int(np.ceil((hi[i]-lo[i])/step))+1)) for i in (1,2)]
    yy,zz=np.meshgrid(*axes);points=np.column_stack((yy.ravel(),zz.ravel()))
    ax,bx,ai=_ray_intervals(a,points);cx,dx,bi=_ray_intervals(b,points)
    # Compare only intervals with positive union winding, masking infinite misses.
    for i in range(ax.shape[1]):
        if not ai[:,i].any():continue
        for j in range(cx.shape[1]):
            valid=ai[:,i]&bi[:,j]&np.isfinite(bx[:,i])&np.isfinite(dx[:,j])
            if not valid.any():continue
            if np.any(np.minimum(bx[valid,i],dx[valid,j])-np.maximum(ax[valid,i],cx[valid,j])>tolerance):return True
    return False
