"""Class-specific modular optic frames with explicit, unobstructed apertures."""
import numpy as np
from eng import prism, Face, Part

SIGHT_TYPES = dict(pistol='reflex',assault='holo',impulse='precision',shotgun='reflex',
                   sniper='sniper',smg='machine',fusion='energy',trace='trace',rocket='rocket',bow='pin')


def _block(x0,x1,y0,y1,z0,z1,color,label,channel='MT_Metal',emit=False):
    p=prism([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],color,z0,z1,r=.4)
    p.label=label;p.sight=True;p.role='accent' if emit else 'medium'
    p.material='light' if emit else 'metal';p.emit=emit;p.channel=channel
    return p


def _tube(x0,x1,y,z,radius,bore,color,label):
    # Annular, closed wall with empty interior; never a capped solid cylinder.
    faces=[];angles=np.arange(16)*2*np.pi/16
    rings={(x,r):np.array([[x,y+np.sin(a)*r,z+np.cos(a)*r] for a in angles])
           for x in (x0,x1) for r in (radius,bore)}
    def face(v,group):
        v=np.asarray(v);n=np.cross(v[1]-v[0],v[2]-v[0]);faces.append(Face(v,n,group))
    for i in range(16):
        j=(i+1)%16
        # Orientation verified against radial outward/inward normals.
        for r,group,flip in ((radius,1,False),(bore,2,True)):
            v=[rings[(x0,r)][i],rings[(x1,r)][i],rings[(x1,r)][j],rings[(x0,r)][j]]
            desired=np.array([0,np.sin(angles[i]+np.pi/16),np.cos(angles[i]+np.pi/16)])*(-1 if flip else 1)
            if np.dot(np.cross(v[1]-v[0],v[2]-v[0]),desired)<0:v=v[::-1]
            face(v,group)
        for x,nx,g in ((x0,-1,3),(x1,1,4)):
            v=[rings[(x,radius)][i],rings[(x,radius)][j],rings[(x,bore)][j],rings[(x,bore)][i]]
            if np.cross(v[1]-v[0],v[2]-v[0])[0]*nx<0:v=v[::-1]
            face(v,g)
    p=Part(faces,color,label=label,sight=True,material='metal',role='medium');p.channel='MT_Metal'
    return p


def replace_optics(meta, model):
    slug=meta['slug'];kind=SIGHT_TYPES[slug]
    rail=next((p for p in model if p.label=='Visierschiene'),None)
    if rail is None:raise ValueError('A modular optic needs a rail')
    v=rail.vertices;lo=v.min(axis=0);hi=v.max(axis=0)
    x=(lo[0]+hi[0])/2;rail_z=(lo[2]+hi[2])/2;z=rail_z;top=lo[1]
    # Bow sightline runs beside the limbs/string; the impulse crown needs
    # a slightly taller clamp. Keep the physical bridges on the rail.
    if slug=='bow':z=30.
    lift=6. if slug=='impulse' and meta.get('series')=='fluxbloom' else 0.
    colors=meta['palette'];metal=colors[1];dark=colors[2];accent=colors[3]
    model[:]=[p for p in model if not p.sight]
    width,height,length={'reflex':(15,20,24),'holo':(23,23,29),'precision':(14,14,34),
        'sniper':(17,17,52),'machine':(18,17,20),'energy':(27,23,32),
        'trace':(30,24,31),'rocket':(33,26,37),'pin':(14,25,18)}[kind]
    if slug=='shotgun':width,height=25,23
    # All clamp geometry stays within the existing rail length.
    length=min(length,max(12,hi[0]-lo[0]-4));x0=x-length/2;x1=x+length/2
    if slug=='bow':
        model.append(_block(x0,x1,top-5,top+2,rail_z-5,z+5,metal,'Visierausleger'))
    for mountx in (x0+3,x1-3):
        model.append(_block(mountx-3,mountx+3,top-7-lift,top+2,z-5,z+5,dark,'Visierklemme','MT_Detail'))
    floor=top-7-lift;cy=floor-height/2;aperture_x=x1-5
    if kind in ('precision','sniper'):
        radius=height/2
        body=_tube(x0,x1,cy,z,radius,radius-2,metal,'Optikröhre')
        # Rings overlap the clamp upper edges and the thin-walled tube.
        model.append(body)
        model.append(_tube(x0-2,x0+4,cy,z,radius+1,radius-2,dark,'Okularfassung'))
        model.append(_tube(x1-4,x1+3,cy,z,radius+2,radius-2,metal,'Objektivfassung'))
        aperture_x=x1+3
        window=body
        width=height=2*(radius-2)
    else:
        half=width/2;thick=2.2
        model.append(_block(x0,x1,floor-3,floor,z-half-2,z+half+2,metal,'Visierfuß'))
        # Opening is a true empty YZ rectangle facing along the barrel axis.
        window=_block(aperture_x-2,aperture_x+2,floor-height-2,floor-height,z-half-2,z+half+2,metal,'Fensterrahmen')
        model.append(window)
        for side in (-1,1):
            model.append(_block(aperture_x-2,aperture_x+2,floor-height,floor-2,
                z+side*half-thick/2,z+side*half+thick/2,metal,'Fensterstrebe'))
        model.append(_block(aperture_x-2,aperture_x+2,floor-3,floor-1,z-half,z+half,metal,'Fenstersockel'))
        if kind in ('energy','trace','holo'):
            for side in (-1,1):
                model.append(_block(aperture_x-2.5,aperture_x+2.5,floor-height+1,floor-height+5,
                    z+side*half-1,z+side*half+1,accent,'Markierungsrahmen','MT_Emission',True))
        if kind=='rocket':
            # Offset range posts remain on the frame, not across the sightline.
            for i in range(3):
                model.append(_block(aperture_x-2,aperture_x+3,floor-height+4+i*5,floor-height+5+i*5,
                    z+half,z+half+4,accent,'Entfernungsmarke','MT_Accent'))
    if kind not in ('precision','sniper'):cy=floor-(height+3)/2
    window.sight_window=True
    window.window_geometry={'center_model':[float(aperture_x),float(cy),float(z)],
        'normal_model':[1.,0.,0.], 'width_model':float(width-3.2 if kind not in ('precision','sniper') else width),
        'height_model':float(height-4 if kind not in ('precision','sniper') else height),
        'source':'explicit unobstructed frame aperture, along model +X'}
    meta['sight_type']=kind;meta['sight_frame']='open' if kind not in ('precision','sniper') else 'industrial'
    return model
