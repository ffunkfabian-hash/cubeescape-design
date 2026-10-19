"""Fifteen independently constructed Parallax concepts, types 11–25.

These are functional design intentions, not simulated or production mechanisms.
All solids are closed individually; launch channels and ring bores stay open.
"""
from .common import *


def _beam(m, a, b, radius, color, label, role='medium', material='metal'):
    """Closed twelve-sided strut in any direction, including transverse limbs."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    axis = b-a
    length = np.linalg.norm(axis)
    axis /= length
    seed = np.array((0., 1., 0.)) if abs(axis[1]) < .9 else np.array((0., 0., 1.))
    normal = np.cross(axis, seed)
    normal /= np.linalg.norm(normal)
    rotation = np.column_stack((axis, normal, np.cross(axis, normal)))
    part = cyl(0, length, 0, 0, radius, color)
    for face in part.faces:
        face.vertices = face.vertices @ rotation.T + a
        face.normal = rotation @ face.normal
    return add(m, part, label, role, material)


def _transverse(m, points, y0, y1, color, label, role='primary', material='paint'):
    """Extruded XZ profile; rotation preserves outward winding."""
    part = prism(points, color, -y1, -y0)
    rotation = np.array(((1,0,0),(0,0,-1),(0,1,0)))
    for face in part.faces:
        face.vertices = face.vertices @ rotation.T
        face.normal = rotation @ face.normal
    return add(m, part, label, role, material)


def _grip(m, x, top, length=42, width=18, guard=34):
    plate(m, [(x-8,top-3),(x+width-7,top-3),(x+width-14,top+length),
              (x-18,top+length-2)], -10,10,DARK,'Griff','dark','rubber')
    gx=x+width-9
    rod(m,(gx-5,top+18),(gx,top+28),4,-7,7,STEEL,'Bügel')
    rod(m,(gx,top+28),(gx+guard-3,top+28),4,-7,7,STEEL,'Bügel')
    rod(m,(gx+guard-3,top+28),(gx+guard,top-2),4,-7,7,STEEL,'Bügel')
    plate(m,[(gx+10,top-2),(gx+16,top-2),(gx+12,top+12),
             (gx+14,top+17),(gx+9,top+20),(gx+7,top+11)],
          4,11,ORANGE,'Abzug','medium','metal')


def _mag(m, x, top, length=40, width=21, tilt=3, label='Magazin'):
    block(m,x-3,x+width+3,top-3,top+6,-12,12,STEEL,'Magazinschacht','medium','metal')
    plate(m,[(x,top+3),(x+width,top+3),(x+width+tilt,top+length),
             (x+tilt,top+length+2)],-9,9,DARK,label,'dark','plastic')
    block(m,x+tilt-2,x+width+tilt+2,top+length-2,top+length+5,-11,11,
          STEEL,'Magazinboden','medium','metal')


def _rail(m, x0,x1, y, support_top):
    block(m,x0,x1,y+3,support_top+1,-6,6,CREAM,'Schienensockel',cut=1)
    block(m,x0,x1,y,y+4,-7,7,STEEL,'Visierschiene','medium','metal',cut=1)
    for x in range(int(x0)+3,int(x1)-2,9):
        block(m,x,x+4,y-1,y+1,-7,7,DARK,'Schienensteg','dark','metal',cut=.4)


def _bolt(m,x,y,z):
    block(m,x,x+25,y,y+8,z,z+3,STEEL,'Verschluss','medium','metal',cut=1)
    _beam(m,(x+6,y+4,z+2),(x+6,y+8,z+12),2.4,DARK,'Verschluss')


def _cylinder(m, x0,x1, cy,radius,count,bore,label):
    """A chamber bundle with a solid hub and open annular chamber shells.

    The uppermost chamber is centered at cy-radius and aligned with the barrel.
    Spokes terminate in the inner walls; none crosses a chamber's bore.
    """
    add(m,cyl(x0-8,x1-2,cy,0,5.5,STEEL),'Trommelachse','medium','metal')
    outer=bore+2.6
    for i in range(count):
        angle=-math.pi/2+2*math.pi*i/count
        dy,dz=math.sin(angle),math.cos(angle)
        y,z=cy+radius*dy,radius*dz
        tube(m,x0,x1,y,z,outer,bore,CREAM,label,'primary',sides=12)
        _beam(m,((x0+x1)/2,cy+4*dy,4*dz),
              ((x0+x1)/2,cy+(radius-outer+.7)*dy,(radius-outer+.7)*dz),
              1.5,STEEL,'Trommelsteg')
    # Narrow inter-chamber bands close the bundle only along outer tangencies.
    for i in range(count):
        a=-math.pi/2+2*math.pi*i/count
        b=a+2*math.pi/count
        tangent_radius=radius+outer-1
        _beam(m,((x0+x1)/2,cy+tangent_radius*math.sin(a),tangent_radius*math.cos(a)),
              ((x0+x1)/2,cy+tangent_radius*math.sin(b),tangent_radius*math.cos(b)),
              1.2,DARK,'Trommelverbinder','dark')


def scout():
    m=[]
    plate(m,[(-79,-19),(-65,-25),(29,-25),(46,-13),(42,17),(-62,18),(-80,7)],
          -12,12,label='Gehäuse')
    stock(m,-139,-77,-4)
    block(m,-125,-81,-19,-9,-11,11,CREAM,'Wangenauflage')
    _grip(m,-54,17)
    _mag(m,9,17,34,20,0)
    plate(m,[(38,-16),(101,-14),(108,-6),(100,11),(40,14)],-10,10,CREAM,'Handschutz')
    tube(m,43,182,-5,0,5,2.8,STEEL,'Lauf')
    tube(m,177,195,-5,0,8,3.2,DARK,'Mündung','dark')
    for z in (-11,11):
        block(m,54,91,-2,4,z-1,z+1,DARK,'Handschutzbelüftung','dark','metal',cut=1)
    _bolt(m,-31,-16,12)
    _rail(m,-62,22,-31,-25)
    return m


def handcannon():
    m=[]
    # Separate rear wall, top bridge and side cheeks leave the drum exposed.
    block(m,-68,-14,-35,29,-18,18,CREAM,'Gehäuse')
    block(m,-20,53,-35,-28,-13,13,CREAM,'Trommelrahmen')
    for z in (-25,25):
        rod(m,(-18,23),(50,23),5,z-3,z+3,STEEL,'Trommelrahmen')
        block(m,43,53,-27,27,z-3,z+3,CREAM,'Trommelwange')
    _cylinder(m,-12,44,0,17,6,6,'Trommel')
    tube(m,42,132,-17,0,9,5.8,STEEL,'Lauf')
    tube(m,126,145,-17,0,13,6.3,DARK,'Mündung','dark')
    block(m,48,117,-31,-24,-12,12,CREAM,'Laufmantel')
    for z in (-11,11):
        block(m,48,117,-25,-10,z-3,z+3,CREAM,'Laufmantel')
    _grip(m,-61,28,49,22,28)
    plate(m,[(-69,-18),(-78,-32),(-87,-36),(-91,-31),(-65,-17),(-65,-7)],
          -6,6,STEEL,'Hahn','medium','metal')
    block(m,-62,-46,6,14,17,23,ORANGE,'Trommelriegel','medium','metal')
    _rail(m,-61,-23,-41,-35)
    return m


def linear():
    m=[]
    plate(m,[(-108,-22),(-93,-29),(-20,-29),(-2,-14),(-1,19),(-94,22),(-110,9)],
          -16,16,label='Gehäuse')
    stock(m,-150,-105,-6,13)
    _grip(m,-82,21,44)
    for z in (-20,20):
        block(m,-39,-4,-20,17,z-7,z+7,CREAM,'Ladekammer',cut=5)
        block(m,-30,-10,-13,9,z+(-8 if z<0 else 6),z+(-6 if z<0 else 8),
              ORANGE,'Ladefenster','accent','light',emit=True,cut=1)
    # Two lateral rails and three annuli leave the entire flight axis free.
    for z in (-21,21):
        block(m,-5,149,-9,3,z-4,z+4,STEEL,'Beschleunigerschiene','medium','metal')
        block(m,16,132,-5,-1,z+(-5 if z<0 else 3),z+(-3 if z<0 else 5),
              ORANGE,'Schienenkontakt','accent','light',emit=True,cut=.5)
    for x in (6,61,121):
        tube(m,x,x+9,-3,0,23,17,CREAM,'Beschleunigerring','primary',sides=12)
    tube(m,142,157,-3,0,23,17,DARK,'Mündung','dark')
    tube(m,-8,8,-3,0,16,11,STEEL,'Lauf')
    block(m,-108,-90,20,35,-13,13,DARK,'Energiezelle','dark','plastic')
    _rail(m,-96,-48,-35,-29)
    return m


def breech():
    m=[]
    plate(m,[(-72,-19),(-54,-25),(-12,-25),(5,-9),(-3,19),(-64,20),(-76,8)],
          -14,14,label='Gehäuse')
    stock(m,-121,-71,-3,12)
    _grip(m,-57,20,43,19,30)
    # Pivot sits below the chamber, leaving the open barrel bore untouched.
    _beam(m,(-3,15,-21),(-3,15,21),7,STEEL,'Laufscharnier')
    tube(m,-1,105,-6,0,16,11,CREAM,'Kipplauf','primary')
    tube(m,97,120,-6,0,19,12,DARK,'Mündung','dark')
    tube(m,4,100,-6,0,12,10,STEEL,'Lauf')
    for z in (-17,17):
        rod(m,(-3,15),(34,8),7,z-3,z+3,CREAM,'Kipplauf')
    block(m,-20,16,-30,-23,-9,9,STEEL,'Verriegelung','medium','metal')
    block(m,-29,-15,-34,-25,-8,8,ORANGE,'Entriegelungshebel','medium','metal')
    _rail(m,-60,-26,-31,-25)
    return m


def drum():
    m=[]
    plate(m,[(-98,-31),(-75,-37),(-32,-37),(-17,-23),(-23,29),(-88,27),(-100,13)],
          -19,19,label='Gehäuse')
    stock(m,-145,-98,-6,14)
    _grip(m,-77,28,43,20,28)
    # Six distinct large chambers around a low drum axis; upper chamber fires.
    _cylinder(m,-13,63,3,28,6,10,'Granattrommel')
    for z in (-43,43):
        block(m,-30,75,-2,8,z-3,z+3,STEEL,'Trommelträger','medium','metal')
        block(m,64,75,-26,35,z-3,z+3,CREAM,'Vorderer Trommelträger')
    block(m,-30,-18,-23,36,-43,43,CREAM,'Hinterer Trommelträger')
    tube(m,62,137,-25,0,16,10,STEEL,'Lauf')
    tube(m,130,151,-25,0,20,11,DARK,'Mündung','dark')
    block(m,2,47,-7,23,40,46,CREAM,'Ladeklappe',cut=4)
    block(m,38,48,3,15,45,50,ORANGE,'Klappenriegel','medium','metal',cut=1)
    _rail(m,-82,-40,-43,-37)
    return m


def machine():
    m=[]
    plate(m,[(-83,-24),(-62,-31),(41,-31),(57,-17),(51,24),(-68,24),(-85,11)],
          -18,18,label='Gehäuse')
    stock(m,-142,-81,-2,14)
    _grip(m,-61,24,43,20,31)
    block(m,-45,33,-36,-29,-18,18,CREAM,'Zuführdeckel')
    _bolt(m,-20,-20,-21)
    tube(m,43,170,-8,0,8,4,STEEL,'Lauf')
    tube(m,162,185,-8,0,12,5,DARK,'Mündung','dark')
    block(m,48,108,-21,10,-14,14,CREAM,'Handschutz')
    for x in (57,69,81,93):
        for z in (-15,15):
            block(m,x,x+5,-15,3,z-1,z+1,DARK,'Kühlschlitz','dark','metal',cut=.5)
    # Left box and connector straps physically meet the receiver.
    block(m,-13,27,2,61,35,65,DARK,'Munitionskasten','dark','metal',cut=5)
    for x in (-8,22):
        block(m,x,x+5,-5,14,15,40,STEEL,'Kastenhalter','medium','metal')
    # Cartridge axes follow +X, the linked belt turns from the box into the lid.
    feed=[(4,57),(-6,53),(-15,47),(-23,40),(-28,32),(-29,23),(-29,16)]
    for y,z in feed:
        add(m,cyl(-9,15,y,z,2.8,STEEL),'Patronengurt','medium','metal')
    for (y0,z0),(y1,z1) in zip(feed,feed[1:]):
        _beam(m,(2,y0,z0),(2,y1,z1),1.6,DARK,'Gurtverbinder','dark')
    for z in (-14,14):
        _beam(m,(110,2,z),(94,49,z*2),3,STEEL,'Zweibein')
    _rail(m,-61,21,-42,-36)
    return m


def sword():
    m=[]
    # Grip, guard cell and a single long faceted blade; no firearm controls.
    plate(m,[(-112,-8),(-105,-12),(-27,-12),(-20,-6),(-27,9),(-104,9)],
          -8,8,DARK,'Griff','dark','rubber')
    block(m,-118,-105,-15,13,-12,12,STEEL,'Knauf','medium','metal')
    plate(m,[(-28,-17),(-12,-23),(13,-15),(23,-5),(15,16),(-17,20),(-30,8)],
          -14,14,CREAM,'Gehäuse')
    _transverse(m,[(-19,-37),(-5,-39),(18,-15),(18,15),(-5,39),(-19,37),(-4,10),(-4,-10)],
                -5,5,STEEL,'Parierstange','medium','metal')
    block(m,-21,3,-10,10,-17,-12,DARK,'Energiezelle','dark','plastic')
    block(m,-17,-1,-6,6,-19,-16,ORANGE,'Zellkontakt','accent','light',emit=True)
    plate(m,[(13,-11),(154,-16),(210,-3),(159,13),(13,11)],-3,3,
          STEEL,'Klinge','medium','metal')
    plate(m,[(19,-5),(149,-10),(187,-3),(148,5),(19,5)],-4,4,CREAM,'Klingenrücken')
    for z in (-4.5,3.5):
        plate(m,[(20,7),(150,9),(188,-2),(153,5),(20,3)],z,z+1,
              ORANGE,'Energiesaum','accent','light',emit=True)
    return m


def glaive():
    m=[]
    add(m,cyl(-159,66,0,0,7,STEEL),'Stange','medium','metal')
    tube(m,-148,-109,0,0,10,7,DARK,'Griff','dark','rubber')
    tube(m,-49,-11,0,0,11,7,DARK,'Vordergriff','dark','rubber')
    block(m,-96,-39,-12,14,-13,13,CREAM,'Gehäuse')
    _grip(m,-88,13,27,18,29)
    tube(m,-165,-151,0,0,11,6,DARK,'Stangenabschluss','dark')
    block(m,49,79,-18,18,-16,16,CREAM,'Klingensockel')
    tube(m,75,96,0,0,13,8,STEEL,'Emitter')
    # Blade rises from the upper socket; the emitter's +X axis is free.
    plate(m,[(61,-16),(102,-53),(167,-54),(151,-28),(90,-12)],
          -4,4,STEEL,'Klinge','medium','metal')
    plate(m,[(75,-20),(108,-47),(153,-48),(143,-36),(95,-20)],-5,5,
          CREAM,'Klingenrücken')
    for side in (-1,1):
        pts=[(44,side*12),(62,side*16),(79,side*42),(53,side*47),(37,side*25)]
        _transverse(m,pts,-9,3,CREAM,'Schildflügel')
        _beam(m,(48,-2,side*14),(56,-2,side*36),2.2,ORANGE,'Schildkante','accent','light')
    block(m,-74,-45,-17,-11,-8,8,DARK,'Energiezelle','dark','plastic')
    return m


def crossbow():
    m=[]
    plate(m,[(-90,-17),(-66,-23),(47,-23),(63,-10),(58,17),(-73,17),(-92,6)],
          -13,13,label='Gehäuse')
    stock(m,-142,-88,-3,12)
    _grip(m,-66,17,42,20,31)
    # Open bolt support: two parallel walls and a low bed, no roof over bolt.
    block(m,-48,130,-30,-22,-8,8,STEEL,'Bolzenauflage','medium','metal')
    for z in (-9,9):
        block(m,-41,139,-39,-25,z-2,z+2,CREAM,'Lauf','primary')
        block(m,126,145,-40,-24,z-3,z+3,DARK,'Mündung','dark','metal')
    block(m,68,88,-29,9,-30,30,STEEL,'Bogenaufnahme','medium','metal')
    # Both limbs span Z, with swept rearward tips and matching labels.
    for side in (-1,1):
        _transverse(m,[(72,side*18),(87,side*22),(83,side*58),(52,side*101),
                      (34,side*109),(29,side*103),(65,side*53)],
                    -38,-28,CREAM,'Wurfarm')
        _beam(m,(31,-34,side*104),(-46,-34,0),1.1,DARK,'Sehne','dark','plastic')
        _beam(m,(-37,12,side*14),(31,22,side*23),3,STEEL,'Spannhebel')
        _beam(m,(31,22,side*23),(48,10,side*18),3,STEEL,'Spannhebel')
        block(m,-40,39,10,16,side*16-2,side*16+2,DARK,'Spannführung','dark','metal')
    block(m,-53,-36,-39,-26,-7,7,STEEL,'Sehnenschloss','medium','metal')
    _rail(m,-83,-56,-29,-23)
    # One open frame, two equally named walls, central functional anchor.
    cheeks = [p for p in m if p.label == 'Mündung']
    cheeks[0].faces = [f for p in cheeks for f in p.faces]
    m[:] = [p for p in m if p not in cheeks[1:]]
    return m


def rocketside():
    m=[]
    plate(m,[(-77,-26),(-62,-36),(14,-36),(34,-20),(31,17),(-65,19),(-79,5)],
          -17,17,label='Gehäuse')
    tube(m,16,119,-10,0,18,11,CREAM,'Raketenrohr','primary')
    tube(m,22,126,-10,0,12,9.5,STEEL,'Lauf')
    tube(m,114,135,-10,0,22,11,DARK,'Mündung','dark')
    _grip(m,-64,18,47,22,28)
    _mag(m,-3,16,42,27,-3,'Raketenmagazin')
    # Lower ports are attached housings with open bores, not black decals.
    for x in (27,47,67):
        tube(m,x,x+9,7,0,7,4,DARK,'Abgasöffnung','dark',sides=8)
    block(m,-57,16,-42,-35,-11,11,STEEL,'Schlitten','medium','metal')
    _rail(m,-52,-11,-48,-42)
    return m


def rocketpulse():
    m=[]
    # Elevated rear receiver and a dropped forward magazine make a distinct step.
    plate(m,[(-96,-34),(-76,-43),(-3,-43),(20,-20),(49,-16),(43,21),(-81,22),(-97,7)],
          -15,15,label='Gehäuse')
    stock(m,-148,-95,-17,12)
    _grip(m,-68,21,43,19,30)
    _mag(m,3,20,50,29,9,'Raketenmagazin')
    tube(m,37,139,-4,0,12,7.5,STEEL,'Lauf')
    tube(m,130,155,-4,0,17,8.5,DARK,'Mündung','dark')
    plate(m,[(36,-19),(93,-19),(107,-8),(97,14),(43,14)],
          -17,17,CREAM,'Raketenrohrmantel')
    for z in (-18,18):
        block(m,47,88,-6,3,z-1,z+1,DARK,'Abgasleiste','dark','metal')
    _bolt(m,-52,-30,15)
    _rail(m,-77,-12,-49,-43)
    return m


def slug():
    m=[]
    plate(m,[(-85,-18),(-64,-26),(15,-26),(34,-12),(28,21),(-70,21),(-87,8)],
          -13,13,label='Gehäuse')
    # Sculpted continuous cheek stock differs from the long scout skeleton.
    plate(m,[(-143,-19),(-81,-16),(-77,1),(-104,6),(-126,30),(-145,30)],
          -13,13,CREAM,'Schaft')
    block(m,-150,-141,-19,31,-15,15,DARK,'Schulterpolster','dark','rubber')
    _grip(m,-59,20,41,20,28)
    _mag(m,-1,21,30,24,0,'Slug-Magazin')
    tube(m,24,154,-4,0,8,4.5,STEEL,'Lauf')
    # The subtly spiralling lands stop short of the crown; conceptual rifling.
    for i in range(6):
        a=2*math.pi*i/6
        _beam(m,(135,-4+4.1*math.sin(a),4.1*math.cos(a)),
              (153,-4+4.1*math.sin(a+.22),4.1*math.cos(a+.22)),
              .55,DARK,'Laufzug','dark')
    plate(m,[(27,-14),(81,-14),(90,-6),(83,15),(27,15)],-12,12,
          CREAM,'Fester Handschutz')
    tube(m,149,171,-4,0,11,4.6,DARK,'Mündung','dark')
    _bolt(m,-45,-18,13)
    _rail(m,-63,10,-32,-26)
    return m


def heat():
    m=[]
    plate(m,[(-94,-21),(-76,-31),(4,-31),(24,-19),(20,23),(-77,23),(-96,11)],
          -16,16,label='Gehäuse')
    stock(m,-142,-94,-3,13)
    _grip(m,-69,23,42,20,31)
    # Receiver has an integrated closed energy store; no exchange magazine.
    block(m,-31,13,20,34,-13,13,DARK,'Hitzespeicher','dark','metal',cut=4)
    tube(m,16,102,-3,0,20,9,STEEL,'Wärmekern')
    for x in range(26,93,11):
        tube(m,x,x+4,-3,0,26,9,CREAM,'Kühlrippe','primary')
    for z in (-26,26):
        block(m,19,102,-13,6,z-2,z+2,CREAM,'Entlüftungsklappe')
        _beam(m,(19,-14,z),(101,-14,z),2,STEEL,'Klappenscharnier')
    tube(m,96,136,-3,0,10,5,STEEL,'Lauf')
    tube(m,127,150,-3,0,15,6,DARK,'Mündung','dark')
    block(m,-49,-19,-19,-5,16,19,DARK,'Anzeigefassung','dark','metal')
    for i in range(4):
        block(m,-45+i*6,-42+i*6,-16,-8,18,20,ORANGE,'Hitzeanzeige',
              'accent','light',emit=True,cut=.4)
    _rail(m,-78,-13,-37,-31)
    return m


def micro():
    m=[]
    # Long single-shot tube with a compact rear action; external reserve rack.
    plate(m,[(-88,-24),(-69,-32),(-24,-32),(-9,-14),(-17,21),(-73,21),(-90,8)],
          -15,15,label='Gehäuse')
    stock(m,-137,-88,-7,12)
    _grip(m,-64,21,43,19,30)
    tube(m,-14,137,-8,0,18,11,CREAM,'Raketenrohr','primary')
    tube(m,-8,146,-8,0,12,10,STEEL,'Lauf')
    tube(m,132,156,-8,0,22,11,DARK,'Mündung','dark')
    block(m,-23,15,-29,-23,-12,12,STEEL,'Ladeklappe','medium','metal')
    _beam(m,(-22,-25,-15),(14,-25,-15),2.5,DARK,'Klappenscharnier','dark')
    block(m,-22,-12,-34,-27,6,12,ORANGE,'Klappenriegel','medium','metal')
    # A single reserve rocket is visibly clipped outside the firing tube.
    for x in (25,80):
        block(m,x,x+8,-1,8,14,32,STEEL,'Vorratshalter','medium','metal')
    add(m,cyl(19,99,5,30,7,DARK),'Raketenvorrat','dark','metal')
    tube(m,91,103,5,30,8,3,STEEL,'Raketenkopf')
    _rail(m,-69,-29,-38,-32)
    return m


def spread():
    m=[]
    block(m,-85,-30,-32,29,-19,19,CREAM,'Gehäuse')
    _grip(m,-72,28,51,23,29)
    # Five real chambers in a break-open frame. Lower pivot joins the frame.
    _cylinder(m,-24,44,0,20,5,7,'Trommel')
    block(m,-32,55,-39,-32,-13,13,CREAM,'Kipprahmen')
    for z in (-31,31):
        rod(m,(-30,26),(54,26),6,z-3,z+3,STEEL,'Kipprahmen')
        block(m,46,58,-32,28,z-3,z+3,CREAM,'Kipprahmen')
    _beam(m,(51,26,-35),(51,26,35),7,DARK,'Kipprahmenscharnier','dark')
    tube(m,44,104,-20,0,11,7,STEEL,'Lauf')
    # Broad horizontal spread muzzle remains an actual hollow aperture.
    for y0,y1 in ((-30,-27),(-13,-10)):
        _transverse(m,[(96,-10),(133,-27),(146,-27),(146,27),(133,27),(96,10)],
                    y0,y1,CREAM,'Streumündungsmantel')
    # Two cheeks and roof/floor form a wide rectangular open crown.
    for z in (-25,25):
        block(m,130,146,-30,-10,z-3,z+3,DARK,'Mündung','dark','metal',cut=1)
    block(m,-45,-26,-43,-31,-9,9,ORANGE,'Rahmenriegel','medium','metal')
    plate(m,[(-86,-16),(-98,-29),(-105,-30),(-106,-24),(-82,-13),(-82,-5)],
          -6,6,STEEL,'Hahn','medium','metal')
    _rail(m,-77,-46,-38,-32)
    # The two cheeks form one labelled open muzzle frame. Keeping the assembly
    # together makes its centreline anchor describe the aperture, not one cheek.
    cheeks = [p for p in m if p.label == 'Mündung']
    cheeks[0].faces = [f for p in cheeks for f in p.faces]
    m[:] = [p for p in m if p not in cheeks[1:]]
    return m


def _info(number,slug,name,kind,form,notes,reload,action,fire,motions=()):
    data=meta(slug,name,kind,form,notes)
    data.update(type_number=number,series='parallax',variant='A',variant_name='Parallax',
                motion_labels=list(motions),operation_intent=dict(
                    reload=dict(de=reload[0],en=reload[1]),
                    action=dict(de=action[0],en=action[1]),fire=dict(de=fire[0],en=fire[1])))
    return data


CATALOG=(
    (_info(11,'scout','Waymark S-4','Scout-Gewehr','LANGER EINZELLAUF · FLACHER HANDSCHUTZ · KASTENMAGAZIN',
           'Halbautomatischer Präzisionsentwurf mit kurzem Handschutz, sichtbarem Verschluss und offener Skelettstütze.',
           ('Kastenmagazin vor dem Abzug wechseln.','Replace the box magazine ahead of the trigger.'),
           ('Verschluss am seitlichen Ladehebel zurückziehen.','Pull the side charging handle to chamber a round.'),
           ('Ein Abzugsdruck löst einen Präzisionsschuss aus.','Each trigger press releases one precision shot.'),('Verschluss',)),scout),
    (_info(12,'handcannon','Redoubt H-6','Handfeuerwaffe','SECHS OFFENE KAMMERN · AUSSENHAHN · FREIER TROMMELRAHMEN',
           'Sechs Einzelkammern um die Laufachse; der Lauf fluchtet mit der oberen Kammer. Rahmen und Hahn sind von außen lesbar.',
           ('Trommel entriegeln und die sechs Kammern einzeln bestücken.','Release the cylinder and refill its six chambers.'),
           ('Außenhahn spannen; die obere Kammer rastet zum Lauf ein.','Cock the external hammer; the upper chamber aligns with the barrel.'),
           ('Der Abzug gibt den Hahn für einen einzelnen Schuss frei.','The trigger releases the hammer for one shot.'),('Trommel','Hahn')),handcannon),
    (_info(13,'linear','Ionspan L-3','Lineares Fusionsgewehr','SEITENSCHIENEN · OFFENE RINGSTRECKE · ZWEI LADEKAMMERN',
           'Freie Strahlachse durch drei hohle Ringe. Seitliche Beschleunigerschienen sitzen an den Ringwänden, nicht in der Achse.',
           ('Die hintere Energiezelle im Gehäusesockel wechseln.','Replace the rear energy cell in its receiver socket.'),
           ('Ladekammern sammeln Energie vor dem Schienenimpuls.','The charge chambers accumulate energy before the rail pulse.'),
           ('Der Abzug entlädt einen fokussierten Impuls entlang der freien Achse.','The trigger releases a focused pulse along the open axis.'),
           ('Beschleunigerschiene','Ladekammer')),linear),
    (_info(14,'breech','Latch B-1','Spezial-Granatwerfer','EINZELKAMMER · TIEFER DREHPUNKT · KIPPLAUFVERRIEGELUNG',
           'Einschüssiger Kipplauf mit beidseitigen Scharnierwangen unter der Kammer; kein Magazin.',
           ('Riegel lösen, Lauf abkippen und eine Granate einsetzen.','Release the latch, tip the barrel and insert one grenade.'),
           ('Kipplauf hochschwenken und oben verriegeln.','Swing the barrel closed and engage the upper latch.'),
           ('Ein Abzugsdruck zündet die geladene Einzelkammer.','One trigger press fires the loaded single chamber.'),('Kipplauf',)),breech),
    (_info(15,'drum','Orbiter D-6','Schwerer Granatwerfer','TIEFE SECHSKAMMERTROMMEL · SEITENKLAPPE · KURZER LAUF',
           'Sechs hohle Granatkammern, obere Kammer zum Lauf ausgerichtet. Ladeklappe sitzt seitlich außerhalb des Abzugsfensters.',
           ('Seitliche Ladeklappe öffnen und Trommelkammern bestücken.','Open the side hatch and load the drum chambers.'),
           ('Trommel auf die obere Laufkammer weiterschalten.','Index the drum to its upper firing chamber.'),
           ('Der Abzug zündet eine Granate aus der ausgerichteten Kammer.','The trigger fires one grenade from the aligned chamber.'),
           ('Granattrommel','Ladeklappe')),drum),
    (_info(16,'machine','Causeway M-8','Maschinengewehr','LINKER KASTEN · VERBUNDENER GURT · DECKELVERSCHLUSS',
           'Der sichtbare Patronengurt läuft vom linken Kasten in den oberen Zuführdeckel. Langer Lauf und aufgeklapptes Zweibein.',
           ('Linken Kasten wechseln und Gurt unter dem Zuführdeckel einlegen.','Replace the left box and lay the belt under the feed cover.'),
           ('Deckel schließen und Verschluss am Seitenhebel zurückziehen.','Close the cover and pull the side charging handle.'),
           ('Gehaltenen Abzug als Entwurf für gurtgespeistes Feuer verstehen.','A held trigger is the design intent for belt-fed fire.'),
           ('Zuführdeckel','Verschluss','Patronengurt','Munitionskasten')),machine),
    (_info(17,'sword','Daybreak E-2','Schwert','FACETTENKLINGE · QUERPARIERSTANGE · ZELLBLOCK',
           'Energieverstärkte Klinge mit freier Spitze, eigenständigem Parierblock und wechselbarer Zelle; ohne Visier und Feuerwaffengriff.',
           ('Energiezelle seitlich aus dem Parierblock wechseln.','Replace the energy cell at the side of the guard block.'),
           ('Zellkontakt aktiviert den leuchtenden Klingensaum.','The cell contact powers the illuminated blade edge.'),
           ('Die geführte Klinge wirkt durch Hieb und Stoß.','The guided blade acts through cuts and thrusts.'),('Klinge',)),sword),
    (_info(18,'glaive','Sentinel G-2','Glefe','LANGSTANGE · FREIER EMITTER · PAARIGE SCHILDFLÜGEL',
           'Oberhalb des offenen Emitters angesetzte Klinge; seitliche Schildflügel besitzen freie Entfaltungsräume.',
           ('Zelle oberhalb des hinteren Stangengriffs wechseln.','Replace the cell above the rear pole grip.'),
           ('Emitter laden und beide Schildflügel seitlich ausstellen.','Charge the emitter and extend both shield wings sideways.'),
           ('Abzug für den Impuls; Klinge separat mit der Stange führen.','Use the trigger for the pulse and guide the blade with the pole.'),
           ('Schildflügel','Emitter','Klinge')),glaive),
    (_info(19,'crossbow','Outrigger C-5','Schwere Armbrust','QUERWURFARME · SEHNENSCHLOSS · OFFENE BOLZENRINNE',
           'Wurfarme und Sehne liegen quer in Z. Seitliche Spannhebel ziehen das Sehnenschloss entlang der offenen Bolzenauflage zurück.',
           ('Einen schweren Bolzen von oben in die offene Auflage legen.','Place one heavy bolt into the open top cradle.'),
           ('Beide Spannhebel zurückführen, bis das Sehnenschloss einrastet.','Draw both cocking levers until the string latch engages.'),
           ('Der Abzug löst das Sehnenschloss und beschleunigt den Bolzen.','The trigger releases the string latch to launch the bolt.'),
           ('Spannhebel','Sehne','Wurfarm','Bolzenauflage')),crossbow),
    (_info(20,'rocketside','Flarecap R-2','Raketenpistole','WEITES RAKETENROHR · TIEFES MAGAZIN · OFFENE ABGASSTUTZEN',
           'Kurze Raketenpistole mit oberer beweglicher Zuführführung und drei offenen unteren Abgasstutzen; ohne Schaft.',
           ('Das kurze Raketenmagazin vor dem Abzug austauschen.','Exchange the short rocket magazine ahead of the trigger.'),
           ('Obere Zuführführung zurückziehen und wieder einrasten lassen.','Retract the upper feed guide and let it lock forward.'),
           ('Der Abzug startet eine Rakete aus dem weiten Rohr.','The trigger launches one rocket through the wide tube.'),('Schlitten',)),rocketside),
    (_info(21,'rocketpulse','Firestep R-3','Raketen-Impulsgewehr','HOHER HINTERKASTEN · TIEFER RAKETENSCHACHT · ROHRLAUF',
           'Stufenförmiges Gehäuse mit langem Raketenmagazin, kurzem Rohrmantel und sichtbarem Seitenverschluss.',
           ('Das tiefe Raketenmagazin am vorderen Schacht wechseln.','Replace the deep rocket magazine at the forward well.'),
           ('Seitlichen Verschluss betätigen und erste Rakete zuführen.','Cycle the side bolt to feed the first rocket.'),
           ('Der Abzug fordert eine kurze Folge einzelner Raketenimpulse an.','The trigger requests a short sequence of rocket pulses.'),('Verschluss',)),rocketpulse),
    (_info(22,'slug','Boreline S-1','Slug-Schrotflinte','GEZOGENER EINZELLAUF · KURZMAGAZIN · FESTER HANDSCHUTZ',
           'Einzelgeschoss-Entwurf mit kurzen sichtbaren Laufzügen an der Krone; fester Handschutz ohne Pumpmechanik.',
           ('Kurzes Slug-Magazin von unten austauschen.','Replace the short slug magazine from below.'),
           ('Verschluss am Seitenhebel schließen und ein Slug zuführen.','Close the side bolt to chamber one slug.'),
           ('Ein Abzugsdruck verschießt ein Einzelgeschoss durch den gezogenen Lauf.','Each trigger press sends one slug through the rifled barrel.'),('Verschluss',)),slug),
    (_info(23,'heat','Afterglow H-3','Hitze-Blaster','RIPPENKERN · PAARIGE KLAPPEN · MAGAZINLOSER SPEICHER',
           'Impulsgewehr mit eingebautem Hitzespeicher statt Magazin. Beidseitige Klappen liegen an den Kühlrippen, Anzeige auf der linken Gehäuseseite.',
           ('Entlüftungsklappen öffnen und den Hitzespeicher kühlen; die Versorgung bleibt aus der Reserve.','Open the vent flaps to cool the heat store; supply continues from reserve.'),
           ('Impulskern laden; die Wärmeanzeige meldet den Speicherzustand.','Charge the pulse core; the heat gauge shows the store condition.'),
           ('Impulsfeuer erwärmt den Kern; beide Klappen öffnen zum Kühlen.','Pulse fire heats the core; both vent flaps open for cooling.'),('Entlüftungsklappe',)),heat),
    (_info(24,'micro','Sparelight M-1','Mikroraketen-Granatwerfer','EINSCHUSSROHR · OBERE LADEKLAPPE · AUSSENRESERVE',
           'Ein Schuss im Rohr, eine separate außen geklemmte Reserve ohne automatische Zufuhr; obere Klappe hinter dem freien Rohr.',
           ('Ladeklappe öffnen und eine einzelne Mikrorakete von Hand einsetzen.','Open the loading hatch and insert one micro missile by hand.'),
           ('Klappe verriegeln; die außen geklemmte Reserve bleibt getrennt.','Lock the hatch; the externally clipped reserve stays separate.'),
           ('Der Abzug startet die einzige im Rohr geladene Mikrorakete.','The trigger launches the single micro missile loaded in the tube.'),('Ladeklappe',)),micro),
    (_info(25,'spread','Fanbreak F-5','Streuschuss-Handfeuerwaffe','FÜNFKAMMERTROMMEL · KIPPRAHMEN · BREITE STREUMÜNDUNG',
           'Fünf reale Kammern im Kipprahmen mit unterem Drehpunkt, oberem Riegel und hohler querbreiter Streumündung.',
           ('Oberen Riegel lösen, Rahmen abkippen und fünf Kammern bestücken.','Release the upper latch, tip the frame and load five chambers.'),
           ('Kipprahmen schließen und Außenhahn spannen.','Close the break frame and cock the external hammer.'),
           ('Ein Abzugsdruck löst eine Streuladung durch die breite Mündung aus.','Each trigger press releases a spread charge through the wide muzzle.'),
           ('Kipprahmen','Trommel')),spread),
)


def load_new():
    """Return metadata and fresh assemblies in the stable type order 11–25."""
    return [(metadata.copy(), builder()) for metadata,builder in CATALOG]
