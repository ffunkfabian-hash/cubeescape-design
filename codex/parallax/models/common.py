"""Closed, stylised parts shared by the fictional concept designs.

Coordinates use x forward, y down and positive z on the observer's left.
Socket overlaps are intentional assembly joints; labels identify complete parts.
"""
import math
import numpy as np
from eng import Face, Part, prism, cyl

CREAM = '#D5CCB8'
STEEL = '#858F99'
DARK = '#303844'
ORANGE = '#F28C28'
PALETTE = [CREAM, STEEL, DARK, ORANGE]


def meta(slug, name, kind, form, notes):
    return dict(slug=slug, name=name, kind=kind, form=form,
                palette_name='Keramik · Titan · Graphit · Signalorange',
                palette=PALETTE.copy(), notes=notes)


def add(model, part, label='', role='primary', material='paint', emit=False, sight=False):
    part.label = label
    part.role = role
    part.material = material
    part.emit = emit
    part.sight = sight
    model.append(part)
    return part


def plate(model, points, z0, z1, color=CREAM, label='', role='primary',
          material='paint', sight=False, emit=False, bevel=0):
    return add(model, prism(points, color, z0, z1, r=bevel), label,
               role, material, emit, sight)


def block(model, x0, x1, y0, y1, z0, z1, color=CREAM, label='',
          role='primary', material='paint', sight=False, emit=False, cut=2):
    cut = min(cut, (x1-x0)/3, (y1-y0)/3)
    points = [(x0+cut,y0), (x1-cut,y0), (x1,y0+cut),
              (x1,y1-cut), (x1-cut,y1), (x0+cut,y1),
              (x0,y1-cut), (x0,y0+cut)]
    return plate(model, points, z0,z1,color,label,role,material,sight,emit)


def tube(model, x0, x1, y, z, radius, bore, color=STEEL, label='',
         role='medium', material='metal', sides=12, sight=False, emit=False):
    """One closed manifold annular shell, with a continuous open bore."""
    faces = []
    angles = [2*math.pi*i/sides for i in range(sides)]
    rings = {}
    for x in (x0,x1):
        for r in (radius,bore):
            rings[(x,r)] = [np.array((x,y+math.sin(a)*r,z+math.cos(a)*r),dtype=float)
                            for a in angles]
    def quad(vertices, normal, smooth_group):
        vertices = np.asarray(vertices,dtype=float)
        normal = np.asarray(normal,dtype=float)
        if np.dot(np.cross(vertices[1]-vertices[0], vertices[2]-vertices[0]),normal) < 0:
            vertices = vertices[::-1].copy()
        faces.append(Face(vertices, normal, smooth_group))
    for i in range(sides):
        j = (i+1)%sides
        mid = (angles[i]+math.pi/sides)
        ny,nz = math.sin(mid),math.cos(mid)
        quad([rings[(x0,radius)][i],rings[(x1,radius)][i],rings[(x1,radius)][j],rings[(x0,radius)][j]],(0,ny,nz),1)
        quad([rings[(x0,bore)][i],rings[(x0,bore)][j],rings[(x1,bore)][j],rings[(x1,bore)][i]],(0,-ny,-nz),2)
        for x,nx in ((x0,-1),(x1,1)):
            quad([rings[(x,radius)][i],rings[(x,radius)][j],rings[(x,bore)][j],rings[(x,bore)][i]],(nx,0,0),3 if nx<0 else 4)
    return add(model,Part(faces=faces,color=color),label,role,material,emit,sight)


def rod(model, a, b, width, z0, z1, color=STEEL, label='', role='medium',
        material='metal', sight=False):
    """Extruded XY link with squared ends and explicit thickness."""
    ax,ay=a; bx,by=b
    dx,dy=bx-ax,by-ay
    length=math.hypot(dx,dy)
    nx,ny=-dy*width/(2*length),dx*width/(2*length)
    return plate(model,[(ax+nx,ay+ny),(bx+nx,by+ny),(bx-nx,by-ny),(ax-nx,ay-ny)],
                 z0,z1,color,label,role,material,sight)


def control_group(model, x, top=16, grip_length=42, magazine_x=None, magazine_length=37,
                  magazine_tilt=4, grip_width=17, guard_width=32):
    """Grip, inset magazine socket and an open, deep trigger guard.

    The trigger pivots in the receiver, between the open guard rails. Its
    visible near face stands proud of the rail, allowing the hero view to read it.
    """
    plate(model,[(x-7,top-3),(x+grip_width-6,top-3),
                 (x+grip_width-14,top+grip_length),(x-17,top+grip_length-2)],
          -9,9,DARK,'Griff','dark','rubber')
    # Three connected links form an open U, joined to receiver and grip.
    # Near-side trigger occupies z=4..10, guard z=-6..6.
    gx=x+grip_width-8; ex=gx+guard_width
    rod(model,(gx,top+28),(ex-3,top+30),4,-6,6,STEEL,'Bügel')
    rod(model,(ex-3,top+30),(ex+1,top-2),4,-6,6)
    rod(model,(gx,top+28),(gx-4,top+17),4,-6,6)
    plate(model,[(gx+10,top-3),(gx+16,top-3),(gx+12,top+13),
                 (gx+14,top+18),(gx+9,top+21),(gx+7,top+12)],
          4,10,ORANGE,'Abzug','dark','metal')
    if magazine_x is not None:
        mx=magazine_x
        block(model,mx-3,mx+20,top-4,top+6,-11,11,STEEL,'Magazinschacht','medium','metal')
        plate(model,[(mx,top+2),(mx+17,top+2),(mx+17+magazine_tilt,top+magazine_length),
                     (mx+magazine_tilt,top+magazine_length+2)],
              -8,8,DARK,'Magazin','dark','plastic')
        block(model,mx+magazine_tilt-2,mx+magazine_tilt+20,
              top+magazine_length-2,top+magazine_length+4,-10,10,
              STEEL,'Magazinboden','medium','metal')


def rail(model, x0,x1, y=-18, z=0, width=10):
    block(model,x0,x1,y,y+5,z-width/2,z+width/2,STEEL,'Visierschiene','medium','metal',cut=1)
    for x in range(int(x0)+3,int(x1)-2,9):
        block(model,x,x+4,y-2,y+1,z-width/2,z+width/2,DARK,role='medium',material='metal',cut=.5)


def optic(model, x=8, y=-18, z=0, long=False):
    """All clamps, bridges and the optical body are detachable sight parts."""
    length=52 if long else 28
    for mountx in (x+5,x+length-7):
        block(model,mountx-4,mountx+4,y-10,y+1,z-6,z+6,DARK,
              'Visierklemme','dark','metal',sight=True,cut=1)
    if long:
        add(model,cyl(x,x+length,y-15,z,6,STEEL),'Zielfernrohr','medium','metal',sight=True)
        tube(model,x+length-3,x+length+5,y-15,z,9,6,DARK,'Objektivfassung','dark','metal',sight=True)
        tube(model,x-4,x+5,y-15,z,8,5,DARK,'Okularfassung','dark','metal',sight=True)
        add(model,cyl(x+length+3,x+length+4,y-15,z,5.8,ORANGE),'Optikglas','accent','light',True,True)
    else:
        # Open reflex hood, with a stem physically connected to the clamps.
        block(model,x,x+length,y-12,y-7,z-7,z+7,CREAM,'Visierfuß','primary','metal',sight=True)
        for side in (-1,1):
            block(model,x+length-9,x+length-3,y-28,y-10,z+side*9-2,z+side*9+2,
                  CREAM,'Reflexrahmen','primary','paint',sight=True)
        block(model,x+length-9,x+length-3,y-30,y-25,z-11,z+11,CREAM,
              'Reflexbrücke','primary','paint',sight=True)


def stock(model, x0, x1, y=-7, zwidth=11, label='Schaft'):
    """An angled skeleton strut and a faceted shoulder pad."""
    plate(model,[(x0,y-8),(x1,y-4),(x1,y+7),(x0+12,y+12),
                 (x0+7,y+30),(x0-2,y+29)],-zwidth,zwidth,
          CREAM,label)
    block(model,x0-6,x0+3,y-9,y+33,-zwidth-2,zwidth+2,DARK,
          'Schulterpolster','dark','rubber',cut=3)


def side_panel(model,x0,x1,y0,y1,z=13):
    for side in (-1,1):
        block(model,x0,x1,y0,y1,side*z-1.5,side*z+1.5,STEEL,
              'Wartungsplatte','medium','metal',cut=3)


def status(model,x,y,z=15,length=10):
    block(model,x,x+length,y,y+2,z-1.2,z+1.0,ORANGE,'Ladestatus','accent','light',emit=True,cut=.5)
