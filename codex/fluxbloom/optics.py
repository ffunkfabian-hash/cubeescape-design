"""Codex bow pin sight; VS01–09 are authored separately in vs_models.py."""
from eng import prism


def _block(x0,x1,y0,y1,z0,z1,color,label,channel='MT_Metal',emit=False):
    p=prism([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],color,z0,z1,r=.4)
    p.label=label;p.sight=True;p.role='accent' if emit else 'medium'
    p.material='light' if emit else 'metal';p.emit=emit;p.channel=channel
    return p


def _bow_optics(meta,model):
    rail=next(p for p in model if p.label=='Visierschiene')
    lo=rail.vertices.min(axis=0);hi=rail.vertices.max(axis=0)
    x=(lo[0]+hi[0])/2;rail_z=(lo[2]+hi[2])/2;z=30.;top=lo[1]
    metal=meta['palette'][1];dark=meta['palette'][2];accent=meta['palette'][3]
    model[:]=[p for p in model if not p.sight]
    length=min(18,max(12,hi[0]-lo[0]-4));x0=x-length/2;x1=x+length/2
    model.append(_block(x0,x1,top-5,top,rail_z-5,z+5,metal,'Visierausleger'))
    for mountx in (x0+3,x1-3):
        model.append(_block(mountx-3,mountx+3,top-7,top,z-5,z+5,dark,'Visierklemme','MT_Detail'))
    floor=top-7;height=25;half=7;thick=2.2;aperture_x=x1-5
    model.append(_block(x0,x1,floor-3,floor,z-half-2,z+half+2,metal,'Visierfuß'))
    model.append(_block(aperture_x-2,aperture_x+2,floor-height-2,floor-height,z-half-2,z+half+2,metal,'Fensterrahmen'))
    for side in (-1,1):
        model.append(_block(aperture_x-2,aperture_x+2,floor-height,floor-2,
            z+side*half-thick/2,z+side*half+thick/2,metal,'Fensterstrebe'))
    model.append(_block(aperture_x-2,aperture_x+2,floor-3,floor-1,z-half,z+half,metal,'Fenstersockel'))
    cy=floor-(height+3)/2
    pin=_block(aperture_x-1,aperture_x+1,cy,floor-1,z-.6,z+.6,metal,'Visierpin')
    pin_y=(cy+floor-1)/2
    dot=_block(aperture_x-1.25,aperture_x-1.05,pin_y-.7,pin_y+.7,z-.7,z+.7,accent,'Leuchtpunkt','MT_Emission',True)
    dot.sight_window=True;model.extend([pin,dot])
    meta['sight_type']='pin';meta['sight_frame']='open'
    # Bow Socket_Sight is derived from the complete assembly, not the rail.
    meta.pop('sight_mount_model',None)
    return model


def replace_optics(meta,model):
    if meta['slug']=='bow':return _bow_optics(meta,model)
    from vs_mount import mount_sight
    return mount_sight(meta,model)
