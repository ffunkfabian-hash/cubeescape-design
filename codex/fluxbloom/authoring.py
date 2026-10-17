"""Shared Codex authoring upgrades; preserves the two series' model identities."""
import math
import numpy as np
from eng import prism
from optics import replace_optics


def _inside(point, polygon):
    x,y=point;cross=False
    for a,b in zip(polygon,np.roll(polygon,-1,axis=0)):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:cross=not cross
    return cross


def _patch(profile,z0,z1,color,label,role,material,channel):
    p=prism(profile,color,z0,z1);p.label=label;p.role=role;p.material=material;p.channel=channel
    p.authoring_detail=True
    return p


def polish_model(meta, model):
    # Functional panels and fasteners attach to verified flat housing faces.
    receiver=next((p for p in model if p.label=='Gehäuse'),None)
    if receiver is None:raise ValueError('Missing receiver')
    additions=[]
    for face in receiver.faces:
        if abs(face.normal[2])<.999:continue
        xy=face.vertices[:,:2];lo=xy.min(axis=0);hi=xy.max(axis=0);c=(lo+hi)/2
        w,h=(hi-lo)*np.array([.48,.42])
        if min(w,h)<6:continue
        profile=np.array([[c[0]-w/2+2,c[1]-h/2],[c[0]+w/2-2,c[1]-h/2],
            [c[0]+w/2,c[1]-h/2+2],[c[0]+w/2,c[1]+h/2-2],
            [c[0]+w/2-2,c[1]+h/2],[c[0]-w/2+2,c[1]+h/2],
            [c[0]-w/2,c[1]+h/2-2],[c[0]-w/2,c[1]-h/2+2]])
        if not all(_inside(p,xy) for p in profile):continue
        side=float(np.sign(face.normal[2]));z=float(face.vertices[0,2])
        additions.append(_patch(profile,z-side*.3,z+side*1.5,meta['palette'][1],
            'Serviceplatte','medium','metal','MT_Secondary'))
        for dx in (-w*.38,w*.38):
            for dy in (-h*.28,h*.28):
                cx,cy=c+[dx,dy];rad=min(1.5,h*.08)
                bolt=[(cx+math.cos(a)*rad,cy+math.sin(a)*rad) for a in np.arange(8)*math.pi/4]
                additions.append(_patch(bolt,z+side*1.1,z+side*2.3,meta['palette'][2],
                    'Plattenverschluss','dark','metal','MT_Detail'))
    model.extend(additions)
    for p in model:
        if not hasattr(p,'channel'):
            p.channel=('MT_Emission' if p.emit else 'MT_Detail' if p.material=='rubber' else
                       'MT_Metal' if p.material=='metal' else 'MT_Primary' if p.role=='primary' else
                       'MT_Secondary' if p.role=='medium' else 'MT_Accent' if p.role=='accent' else 'MT_Detail')
        if p.label=='Abzug':p.role='accent';p.channel='MT_Accent';p.color=meta['palette'][3]
    replace_optics(meta,model)
    return model


def upgrade_bow(meta, model):
    """Move the riser beside the real arrow corridor and expose a nocked arrow."""
    from eng import cyl
    receiver=next(p for p in model if p.label=='Gehäuse')
    attached=[receiver]+([p for p in model if p.label in ('Wartungsplatte','Ladestatus')] if meta.get('series')=='parallax' else [])
    for face in [f for part in attached for f in part.faces]:
        face.vertices[:,2]=face.vertices[:,2]*.5+13
        face.normal=np.array([face.normal[0],face.normal[1],face.normal[2]*2])
        face.normal/=np.linalg.norm(face.normal)
    if meta.get('series')=='parallax':
        mount=next(p for p in model if p.label=='Schienensockel')
        for face in mount.faces:
            face.vertices[:,2]*=1.8
            face.normal[2]/=1.8
            face.normal/=np.linalg.norm(face.normal)
    # The existing guide foot must not occupy its own bore.
    for i,p in enumerate(model):
        if p.label!='Führungssockel':continue
        lo=p.vertices.min(axis=0);hi=p.vertices.max(axis=0)
        q=prism([(lo[0],-5),(hi[0],-5),(hi[0],hi[1]),(lo[0],hi[1])],p.color,lo[2],hi[2],r=1)
        q.label=p.label;q.role=p.role;q.material=p.material
        model[i]=q
    barrel=next(p for p in model if p.label=='Lauf')
    lo=barrel.vertices.min(axis=0);hi=barrel.vertices.max(axis=0)
    cy=(lo[1]+hi[1])/2;cz=(lo[2]+hi[2])/2
    string=next(p for p in model if p.label=='Sehne')
    # Authored string nocks: Flux straight string, Parallax two string limbs.
    sx=-120. if meta.get('series')=='parallax' else -50.
    muzzle=next(p for p in model if p.label=='Mündung');front=float(muzzle.vertices[:,0].max())
    arrow=cyl(sx,front+3,cy,cz,.7,meta['palette'][1]);arrow.label='Pfeilschaft';arrow.role='medium';arrow.channel='MT_Metal';arrow.projectile=True
    model.append(arrow)
    tip=prism([(front+1,cy-2.3),(front+14,cy),(front+1,cy+2.3)],meta['palette'][3],cz-.9,cz+.9)
    tip.label='Pfeilspitze';tip.role='accent';tip.channel='MT_Accent';tip.projectile=True;model.append(tip)
    rest=prism([(lo[0]+2,cy+3),(lo[0]+13,cy+3),(lo[0]+13,cy+6),(lo[0]+2,cy+6)],meta['palette'][1],cz-4,cz+4)
    rest.label='Pfeilauflage';rest.role='medium';rest.material='metal';rest.channel='MT_Metal';model.append(rest)
    meta['notes']=list(meta['notes']) if isinstance(meta['notes'],list) else [meta['notes']]
    meta['moving_parts']={'root_moves':False,'frame':'native model +X', 'items':[{'labels':['Pfeilschaft','Pfeilspitze'],'type':'projectile','direction_model':[1,0,0],'travel_m':None,'null_reason':'Release trajectory and travel are not simulated.','source':'Explicit independent arrow assembly in authoring.upgrade_bow'}]}
    meta['notes'].append('Der seitlich versetzte Riser lässt die Pfeilachse frei; Pfeilschaft und Spitze sind als bewegliches Geschoss separat ausgewiesen.')
    return model
