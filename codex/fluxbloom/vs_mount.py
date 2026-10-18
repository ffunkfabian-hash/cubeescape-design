"""Mount independently authored VS sights without changing weapon identities."""
import math
import numpy as np
from eng import bounds, prism
from vs_models import DESIGNS, build_sight
from skins import channel_for, channel_palette
from sight_validation import weapon_aperture_clearance

SLUGS=('pistol','assault','impulse','shotgun','sniper','smg','fusion','trace','rocket')
# target-mm to native model: +X forward, +Y down, +Z left.
TO_NATIVE=np.array([[0,-1,0],[0,0,-1],[1,0,0.]])


def overlaps(a,b,tol=1e-7):
    return bool(np.all(np.minimum(a[1],b[1])-np.maximum(a[0],b[0])>tol))


def line_blockers(model,center,start):
    """Diagnostic centre ray only; clearance requires weapon_aperture_clearance."""
    from authoring import _inside
    c=np.asarray(center);found=[]
    for p in model:
        if p.sight or p.material=='glass':continue
        lo,hi=bounds([p])
        if np.any(c[1:]<lo[1:]-1e-7) or np.any(c[1:]>hi[1:]+1e-7) or hi[0]<start:continue
        for f in p.faces:
            if abs(f.normal[0])<1e-9:continue
            if not _inside(c[1:],f.vertices[:,1:]):continue
            x=f.vertices[0,0]-np.dot(f.normal[1:],c[1:]-f.vertices[0,1:])/f.normal[0]
            if start-1e-7<=x:found.append(p);break
    return found


def mount_sight(meta,model):
    from spec import LENGTHS_M
    number=SLUGS.index(meta['slug'])+1;d=DESIGNS[number]
    old=[p.label for p in model if p.sight];model[:]=[p for p in model if not p.sight]
    lo,hi=bounds(model);unit=LENGTHS_M[meta['slug']]/(hi[0]-lo[0]);mm=unit*1000
    channels=channel_palette(model);used={channel_for(p) for p in model}
    from spec import _surface_area
    for channel in used:
        areas={}
        for p in model:
            if channel_for(p)==channel:areas[p.color]=areas.get(p.color,0)+_surface_area(p)
        channels[channel]=min(areas,key=lambda color:(-areas[color],color))
    # The existing Codex palette maps the metal slot to the medium swatch.
    # A smaller replacement optic must not turn KK09's steel channel dark.
    if meta.get('series')=='fluxbloom' and meta['slug']=='rocket':channels['MT_Metal']=meta['palette'][1]
    base_channels=dict(zip(('MT_Primary','MT_Secondary','MT_Accent','MT_Metal','MT_Energy','MT_Emission','MT_Detail'),
                           (meta['palette'][i] for i in (0,1,3,1,3,3,2))))
    base_channels.update({c:channels[c] for c in used})
    rail=next((p for p in model if p.label=='Visierschiene'),None);added=rail is None
    if added:
        from authoring import _inside
        x=(lo[0]+hi[0])/2;roof=[]
        for weapon in model:
            for f in weapon.faces:
                if f.normal[1]>=-1e-8:continue
                for xx in np.linspace(x-14/mm,x+14/mm,9):
                    for zz in (-7/mm,0,7/mm):
                        if _inside((xx,zz),f.vertices[:,[0,2]]):
                            roof.append(f.vertices[0,1]-(f.normal[0]*(xx-f.vertices[0,0])+f.normal[2]*(zz-f.vertices[0,2]))/f.normal[1])
        if not roof:raise ValueError('No weapon roof beneath added sight rail')
        roof_y=min(roof);y=roof_y-6/mm
        # Integral pedestal closes the 2 mm gap below the 4 mm rail body.
        rail=prism([(x-30/mm,y),(x+30/mm,y),(x+30/mm,y+4/mm),(x+14/mm,y+4/mm),
                    (x+14/mm,roof_y),(x-14/mm,roof_y),(x-14/mm,y+4/mm),(x-30/mm,y+4/mm)],channels['MT_Metal'],-7/mm,7/mm)
        rail.label='Visierschiene';rail.channel='MT_Metal';rail.material='metal';model.append(rail)
    rlo,rhi=bounds([rail]);seat=(rlo+rhi)/2;seat[1]=rlo[1]
    local=build_sight(number)
    local_lo,local_hi=bounds(local)
    # Never alter longitudinal reference length when adding the optic.
    seat[0]=np.clip(seat[0],lo[0]+local_hi[1]/mm,hi[0]+local_lo[1]/mm)
    # Conservative envelope collision clearance, rounded to 0.5 mm + 0.5 mm air.
    # At zero height the 14 mm clamp slot is checked separately against rail width.
    rise=0.
    if (rhi[2]-rlo[2])*mm>14+1e-6:rise=3.5
    weapon_boxes=[(p,bounds([p])) for p in model]
    for p in local:
        if p.material=='glass':continue
        vertices=p.vertices@TO_NATIVE.T/mm+seat
        a=(vertices.min(axis=0),vertices.max(axis=0))
        for weapon,b in weapon_boxes:
            if weapon is rail:continue
            if min(a[1][0],b[1][0])-max(a[0][0],b[0][0])<=1e-7 or min(a[1][2],b[1][2])-max(a[0][2],b[0][2])<=1e-7:continue
            rise=max(rise,(a[1][1]-b[0][1])*mm+.5)
    if rise>0:rise=math.ceil(rise*2-1e-9)/2
    while True:
        mount=seat-np.array([0,rise/mm,0])
        clearance=weapon_aperture_clearance(model,d,mount,mm)
        if clearance['line_clear_of_weapon']:break
        rise+=.5
        if rise>500:raise ValueError('No free sight aperture')
    mount=seat-np.array([0,rise/mm,0])
    for p in local:
        if p.material!='glass':
            ch=p.channel
            if ch not in used:
                alternatives={'MT_Primary':('MT_Secondary','MT_Accent','MT_Detail','MT_Metal'),
                    'MT_Secondary':('MT_Accent','MT_Primary','MT_Detail','MT_Metal'),
                    'MT_Accent':('MT_Secondary','MT_Detail','MT_Primary','MT_Metal'),
                    'MT_Metal':('MT_Secondary','MT_Detail','MT_Accent'),
                    'MT_Detail':('MT_Secondary','MT_Accent','MT_Metal'),
                    'MT_Energy':('MT_Emission',),'MT_Emission':('MT_Energy',)}
                ch=next((c for c in alternatives[ch] if c in used),ch)
            p.channel=ch;p.color=channels[ch] if ch in used else channels['MT_Accent']
        for f in p.faces:
            f.vertices=f.vertices@TO_NATIVE.T/mm+mount
            f.normal=TO_NATIVE@f.normal
    model.extend(local)
    if rise:
        # The riser sits on the clear rail segment under the complete clamp.
        half=min((rhi[0]-rlo[0])/2,(-d['parts'][0][3][1])/mm)
        # Bridge clears the rail ribs; feet occupy only unobstructed rail gaps.
        from authoring import _inside
        bridge_y=mount[1]+min(3.,rise/2)/mm
        steps=max(2,int(math.ceil(2*half*mm/.5)))
        edges=np.linspace(seat[0]-half,seat[0]+half,steps+1)
        obstacles=[(p,b) for p,b in weapon_boxes if p is not rail and b[0][1]<seat[1]-1e-6
                   and b[1][0]>edges[0] and b[0][0]<edges[-1]
                   and b[1][2]>seat[2]-7/mm and b[0][2]<seat[2]+7/mm]
        free=[]
        for a,b in zip(edges,edges[1:]):
            clear=True
            for x in (a+1e-6,(a+b)/2,b-1e-6):
                for z in (seat[2]-7/mm+1e-6,seat[2],seat[2]+7/mm-1e-6):
                    for weapon,(wlo,whi) in obstacles:
                        if not (wlo[0]-1e-7<=x<=whi[0]+1e-7 and wlo[2]-1e-7<=z<=whi[2]+1e-7):continue
                        for f in weapon.faces:
                            if f.normal[1]>=-1e-8 or not _inside((x,z),f.vertices[:,[0,2]]):continue
                            y=f.vertices[0,1]-(f.normal[0]*(x-f.vertices[0,0])+f.normal[2]*(z-f.vertices[0,2]))/f.normal[1]
                            if y<seat[1]-1e-6:clear=False;break
                        if not clear:break
                    if not clear:break
                if not clear:break
            free.append(clear)
        starts=[i for i,v in enumerate(free) if v and (i==0 or not free[i-1])]
        ends=[i+1 for i,v in enumerate(free) if v and (i==len(free)-1 or not free[i+1])]
        if not starts:raise ValueError(f'{meta["slug"]}: rail has no clear riser seat')
        profile=[(edges[0],mount[1]),(edges[-1],mount[1]),(edges[-1],bridge_y)]
        for a,b in reversed(list(zip(starts,ends))):
            profile.extend([(edges[b],bridge_y),(edges[b],seat[1]),
                            (edges[a],seat[1]),(edges[a],bridge_y)])
        profile.append((edges[0],bridge_y))
        riser=prism(profile,channels['MT_Metal'],seat[2]-7/mm,seat[2]+7/mm)
        riser.label='Erhöhung';riser.sight=True;riser.material='metal';riser.channel='MT_Metal';riser.role='medium'
        model.append(riser)
    meta.update(sight_type=d['type'],sight_frame=d['frame'],sight_mount_model=seat.tolist(),
                vs_number=number,vs_mount_model=mount.tolist(),vs_riser_m=rise*.001,
                vs_rail_added=added,vs_replaced=old,vs_base_channels=base_channels)
    return model
