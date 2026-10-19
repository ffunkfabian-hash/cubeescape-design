"""K11–K25: independent split-shell Flux Bloom mechanisms.

All dimensions are concept units; +X is forward, +Y down, +Z left.
Moving labels describe proposals, never an implemented animation.
"""
import math
import numpy as np
from eng import Face, Part, cyl
from .common import meta, add, plate, block, tube, rod, control_group


PALETTES = (
 ('#7042D0','#DBD1F4','#29223F','#64E7B8','Iris · Flieder · Aubergine · Mint'),
 ('#A749B5','#E4C7DE','#37243E','#D4F14C','Orchidee · Perlmutt · Pflaume · Limette'),
 ('#42C7B0','#D0F1EA','#263A46','#B76EFF','Mint · Eisgrün · Schiefer · Violett'),
 ('#8154D9','#D6C9F0','#302743','#FF857A','Violett · Lavendel · Aubergine · Koralle'),
 ('#A5C43E','#DFE7BE','#333B2C','#BA6DF2','Limette · Salbei · Graphit · Orchidee'),
 ('#B359D0','#E2CDEF','#302740','#73EABD','Malve · Flieder · Aubergine · Mint'),
 ('#6650C7','#D4CEF0','#28283D','#D7F448','Veilchen · Perlmutt · Graphit · Limette'),
 ('#3ABAA7','#CCE8DD','#203C3E','#FD8A97','Jade · Eisgrün · Petrol · Koralle'),
 ('#9D52CD','#E3CDF0','#33263F','#BDED52','Orchidee · Flieder · Pflaume · Limette'),
 ('#FA837C','#F4D2D0','#462D40','#8BF1CB','Koralle · Blüte · Pflaume · Mint'),
 ('#7751D5','#CDC9EE','#292B44','#7CF0C4','Iris · Flieder · Schiefer · Mint'),
 ('#53C8A4','#D7EEE0','#283D37','#CE83ED','Mint · Salbei · Tannengrün · Orchidee'),
 ('#C862B7','#EAD3E5','#3B2940','#D4F659','Azalee · Perlmutt · Pflaume · Limette'),
 ('#8F60D4','#DDD2ED','#352B44','#FF9A7E','Lavendel · Flieder · Aubergine · Koralle'),
 ('#C64E92','#F1CDDC','#40243A','#86F2CF','Fuchsie · Blüte · Pflaume · Mint'),
)


def link3(m, a, b, width, depth=None, label='', role='medium', material='metal'):
    """Rectangular closed strut in any direction, including the transverse bow."""
    a,b=np.asarray(a,float),np.asarray(b,float)
    u=b-a; length=np.linalg.norm(u); u/=length
    ref=np.array((0.,1.,0.)) if abs(u[1])<.9 else np.array((0.,0.,1.))
    v=np.cross(u,ref); v/=np.linalg.norm(v); w=np.cross(u,v)
    q=block([],0,length,-width/2,width/2,-(depth or width)/2,(depth or width)/2,cut=0)
    basis=np.column_stack((u,v,w))
    for f in q.faces:
        f.vertices=f.vertices@basis.T+a; f.normal=basis@f.normal
    return add(m,q,label,role,material)


def controls(m,x,top=18,length=43,width=29):
    control_group(m,x,top=top,grip_length=length,guard_width=width)
    for p in m:
        if p.label=='Abzug': p.role='accent'


def rail_on(m,x0,x1,y):
    # A flat continuous saddle, with a full contact face under the rail.
    block(m,x0,x1,y,y+8,-7,7,label='Schienensockel',role='primary',cut=1)
    block(m,x0-2,x1+2,y-4,y+1,-6,6,label='Visierschiene',role='medium',material='metal',cut=1)
    for x in range(int(x0),int(x1)-2,9):
        block(m,x,x+4,y-6,y-3,-6,6,role='dark',material='metal',cut=.5)


def shoulder(m,a,b,top=-15,bottom=27):
    rod(m,(a,top),(b,top+4),9,-9,9,label='Schaft')
    rod(m,(a,bottom),(b,8),8,-9,9,label='Schaft')
    block(m,a-7,a+3,top-5,bottom+8,-13,13,label='Schulterpolster',role='dark',material='rubber',cut=3)


def mag(m,x,top=19,length=35,label='Magazin',tilt=7):
    block(m,x-3,x+22,top-4,top+5,-12,12,label='Magazinschacht',role='medium',material='metal')
    plate(m,[(x,top),(x+19,top),(x+19+tilt,top+length),(x+tilt,top+length+2)],-9,9,label=label,role='dark',material='plastic')
    block(m,x+tilt-2,x+tilt+21,top+length-2,top+length+5,-11,11,label='Magazinboden',role='accent',material='plastic')


def drum_chambers(m,x0,x1,cy=15,radius=25,count=6,label='Trommel'):
    # Top chamber is exactly on y=cy-radius, z=0. Each chamber is a tube.
    add(m,cyl(x0+4,x1-4,cy,0,8,'#888888'),'Trommelnabe','medium','metal')
    for i in range(count):
        t=2*math.pi*i/count
        y,z=cy-radius*math.cos(t),radius*math.sin(t)
        tube(m,x0,x1,y,z,10,6.7,label=label,role='medium',sides=10)
        # Spokes stop in the inner chamber wall, leaving its bore empty.
        d=np.array((-math.cos(t),math.sin(t)))
        link3(m,(x0+7,cy+d[0]*6,d[1]*6),(x0+7,cy+d[0]*(radius-8.4),d[1]*(radius-8.4)),4,label='Trommelspeiche')
    return cy-radius


def scout():
    m=[]
    plate(m,[(-80,-22),(-27,-31),(17,-20),(27,-9),(9,8),(-72,12)],-12,12,label='Gehäuse')
    plate(m,[(-67,18),(16,12),(67,17),(76,29),(4,30),(-49,25)],-10,10,label='Untergehäuse',role='medium',material='metal')
    for z in (-15,11):
        plate(m,[(9,-20),(94,-28),(116,-19),(61,-11),(17,-10)],z,z+4,label='Vorderschale')
        block(m,13,23,-16,23,z,z+4,label='Gehäusesteg',role='medium',material='metal')
    tube(m,15,155,-5,0,7.5,3.5,label='Lauf')
    tube(m,147,167,-5,0,10,4.2,label='Mündung',role='dark')
    block(m,-48,-16,-17,-5,11,16,label='Verschluss',role='medium',material='metal')
    controls(m,-64,top=17,width=27); mag(m,2,top=28,length=35,tilt=4)
    shoulder(m,-136,-75,top=-17,bottom=24)
    rail_on(m,-62,-8,-29)
    return m


def handcannon():
    m=[]
    # Open bridge and belly cradle carry an exposed six-chamber cylinder.
    plate(m,[(-76,-23),(-53,-31),(-23,-27),(-16,-18),(-62,-12),(-69,13),(-81,16)],-12,12,label='Gehäuse')
    for z in (-15,10):
        plate(m,[(-63,-21),(42,-26),(59,-20),(59,-12),(-62,-12)],z,z+5,label='Rahmenbrücke')
        rod(m,(-52,34),(42,48),6,z,z+5,label='Trommelrahmen')
        rod(m,(42,48),(54,-16),6,z,z+5,label='Trommelrahmen')
    drum_chambers(m,-17,27,cy=15,radius=25,count=6)
    tube(m,26,110,-10,0,9,5,label='Lauf')
    tube(m,102,127,-10,0,13,6,label='Mündung',role='dark')
    plate(m,[(40,-25),(86,-37),(113,-21),(63,-18)],-15,-10,label='Laufschale')
    block(m,-33,-22,8,21,-9,9,label='Trommelachse',role='dark',material='metal')
    plate(m,[(-68,-22),(-73,-43),(-61,-42),(-54,-23)],-6,6,label='Hahn',role='accent',material='metal')
    controls(m,-79,top=15,length=51,width=24)
    rail_on(m,-56,-21,-30)
    return m


def linear():
    m=[]
    plate(m,[(-86,-21),(-31,-34),(8,-21),(18,8),(-14,25),(-76,22)],-15,15,label='Gehäuse')
    shoulder(m,-149,-80,top=-16,bottom=31)
    tube(m,-23,31,-5,0,21,8,label='Ladekammer',role='dark')
    tube(m,17,36,-5,0,6,3,label='Lauf')
    tube(m,10,23,-5,0,11,3,label='Kernsitz',role='medium')
    for x in (29,92,143):
        tube(m,x,x+8,-5,0,25,17,label='Feldring',role='medium',sides=8)
    # Two cantilever rails run beside, never across, the beam axis.
    for z in (-24,17):
        plate(m,[(0,-18),(91,-33),(156,-24),(153,-14),(43,-9),(1,8)],z,z+7,label='Beschleunigerschiene')
        block(m,27,37,-13,3,z,z+7,label='Ringhalter',role='medium',material='metal')
        block(m,91,102,-13,3,z,z+7,label='Ringhalter',role='medium',material='metal')
        block(m,141,151,-13,3,z,z+7,label='Ringhalter',role='medium',material='metal')
    tube(m,149,173,-5,0,20,4,label='Mündung',role='accent',material='metal')
    controls(m,-65,top=22,width=29)
    block(m,-12,8,20,48,-12,12,label='Energiezelle',role='accent',material='plastic')
    rail_on(m,-68,-22,-31)
    return m


def breech():
    m=[]
    plate(m,[(-89,-20),(-52,-28),(-20,-16),(-16,14),(-65,23),(-89,8)],-13,13,label='Gehäuse')
    # Single hinged barrel is supported below the breech, with open upper shells.
    tube(m,-18,123,-8,0,17,12,label='Kipplauf',role='medium')
    tube(m,23,112,-8,0,19,16.8,label='Lauf',role='primary',material='paint')
    tube(m,112,140,-8,0,23,13,label='Mündung',role='dark')
    for z in (-17,12):
        plate(m,[(-33,4),(7,5),(17,25),(-24,31),(-37,19)],z,z+5,label='Scharnierträger')
        block(m,-24,-10,15,28,z-1,z+6,label='Scharnier',role='medium',material='metal')
        plate(m,[(17,-23),(96,-37),(117,-28),(101,-20),(20,-16)],z,z+5,label='Laufblatt')
    block(m,-39,-17,-31,-20,-6,6,label='Verriegelung',role='accent',material='metal')
    controls(m,-78,top=18,width=27)
    shoulder(m,-132,-83,top=-13,bottom=26)
    rail_on(m,-76,-38,-27)
    return m


def drum():
    m=[]
    plate(m,[(-100,-20),(-67,-34),(-38,-21),(-33,15),(-59,28),(-94,22)],-15,15,label='Gehäuse')
    shoulder(m,-151,-94,top=-15,bottom=29)
    drum_chambers(m,-29,31,cy=18,radius=29,count=6,label='Granattrommel')
    for z in (-19,13):
        rod(m,(-55,-22),(41,-24),8,z,z+6,label='Trommelträger')
        rod(m,(-54,28),(40,53),7,z,z+6,label='Trommelträger')
        rod(m,(40,53),(43,-21),7,z,z+6,label='Trommelträger')
    tube(m,31,125,-11,0,13,8,label='Lauf')
    tube(m,119,149,-11,0,18,9,label='Mündung',role='dark')
    plate(m,[(41,-24),(93,-33),(122,-25),(119,-18),(46,-16)],-17,17,label='Laufkamm')
    block(m,-33,-24,9,33,24,35,label='Ladeklappe',role='accent',material='metal')
    block(m,-42,-27,10,26,12,29,label='Klappenscharnier',role='medium',material='metal')
    controls(m,-91,top=23,width=29)
    rail_on(m,-88,-50,-33)
    return m


def machine():
    m=[]
    plate(m,[(-88,-21),(-53,-36),(20,-26),(45,-11),(34,18),(-73,23)],-17,17,label='Gehäuse')
    # Upper and lower petals expose the long cooling barrel.
    for z in (-17,12):
        plate(m,[(20,-22),(108,-31),(134,-20),(123,-12),(29,-10)],z,z+5,label='Kühlmantel')
        plate(m,[(27,8),(126,10),(119,22),(37,24)],z,z+5,label='Kühlmantel')
        block(m,75,84,-21,19,z,z+5,label='Kühlklammer',role='medium',material='metal')
    tube(m,23,157,-4,0,8,4,label='Lauf')
    tube(m,149,178,-4,0,13,5,label='Mündung',role='dark')
    shoulder(m,-147,-81,top=-17,bottom=29)
    controls(m,-69,top=21,width=28)
    block(m,-17,29,27,69,20,48,label='Munitionskasten',role='primary',material='paint',cut=5)
    block(m,-11,26,13,34,18,28,label='Kastenhalter',role='dark',material='metal')
    block(m,-37,10,-34,-22,-18,19,label='Zuführdeckel',role='medium',material='metal')
    block(m,-57,-31,-12,0,-20,-16,label='Verschluss',role='medium',material='metal')
    # Arc of individually readable cartridges and explicit belt links.
    path=[(-4,-23,18),(-4,-19,28),(-4,-10,36),(-4,1,41),(-4,13,42),(-4,28,39)]
    for i,(x,y,z) in enumerate(path):
        tube(m,x-9,x+10,y,z,3.6,1,label='Patronengurt',role='accent',sides=8)
        if i:
            link3(m,path[i-1],path[i],3,label='Gurtverbinder',role='dark')
    rail_on(m,-76,-43,-31)
    return m


def sword():
    m=[]
    # A broad crescent blade forks around a dark tang and rejoins at the tip.
    plate(m,[(0,-11),(56,-32),(171,-47),(209,-26),(248,-5),(182,-17),(75,-11),(9,7)],-6,6,label='Klinge')
    plate(m,[(0,8),(76,18),(176,4),(248,-5),(201,20),(70,35),(5,20)],-6,6,label='Klinge',role='medium',material='metal')
    rod(m,(6,2),(180,-7),6,-4,4,label='Klingenrücken',role='dark',material='metal')
    plate(m,[(-16,-23),(7,-23),(17,0),(10,25),(-15,24),(-24,0)],-10,10,label='Gehäuse')
    plate(m,[(-10,-45),(2,-42),(3,-17),(17,29),(5,44),(-5,39),(-10,15)],-8,8,label='Parierstange',role='primary')
    block(m,-76,-18,-8,8,-8,8,label='Griff',role='dark',material='rubber',cut=3)
    for x in (-67,-55,-43):
        block(m,x,x+4,-9,9,-9,9,label='Griffband',role='medium',material='metal',cut=1)
    block(m,-82,-72,-13,13,-11,11,label='Knauf',role='primary')
    block(m,-18,0,-11,11,9,15,label='Energiezelle',role='accent',material='light',emit=True)
    return m


def glaive():
    m=[]
    block(m,-151,69,-6,6,-7,7,label='Stange',role='medium',material='metal',cut=1)
    block(m,-117,-54,-10,10,-10,10,label='Griff',role='dark',material='rubber')
    block(m,-160,-145,-12,12,-12,12,label='Endkappe',role='primary')
    for z0,z1 in ((-14,-7),(7,14)):
        plate(m,[(37,-18),(80,-25),(104,-12),(111,8),(85,22),(39,14)],z0,z1,label='Gehäuse')
    block(m,51,76,-21,-12,-14,14,label='Kopfbrücke',role='medium',material='metal')
    # Blade lies above the shaft; the lower emitter has a clear forward exit.
    plate(m,[(73,-22),(96,-49),(154,-66),(177,-55),(128,-31),(98,-14)],-5,5,label='Klinge',role='primary')
    plate(m,[(96,-49),(154,-66),(177,-55),(139,-48),(107,-28)],5,7,label='Schneide',role='medium',material='metal')
    tube(m,86,123,8,0,10,5,label='Emitter',role='accent',material='metal')
    tube(m,105,130,8,0,12,6,label='Mündung',role='dark')
    tube(m,62,106,8,0,7,3,label='Lauf',role='medium')
    for z in (-29,17):
        plate(m,[(36,-13),(61,-35),(78,-23),(70,25),(48,39),(34,19)],z,z+12,label='Schildflügel')
        block(m,43,54,-8,10,min(z, -14) if z<0 else 12,max(z+12,-12) if z<0 else 20,label='Schildgelenk',role='medium',material='metal')
    # Local trigger cradle deliberately hugs the shaft, not the forward emitter.
    controls(m,-49,top=4,length=35,width=25)
    block(m,-59,-43,-7,9,-10,10,label='Griffanschluss',role='primary')
    return m


def crossbow():
    m=[]
    plate(m,[(-88,-19),(-39,-28),(25,-18),(34,9),(-8,22),(-82,19)],-12,12,label='Gehäuse')
    shoulder(m,-145,-82,top=-16,bottom=29)
    controls(m,-66,top=19,width=28)
    # Transverse YZ limbs, visibly curved in top view, attached to forward yoke.
    block(m,38,56,-11,12,-33,33,label='Wurfarmjoch',role='medium',material='metal')
    for s in (-1,1):
        link3(m,(47,0,s*24),(76,-3,s*64),10,8,label='Wurfarm',role='primary',material='paint')
        link3(m,(76,-3,s*64),(58,-9,s*99),8,6,label='Wurfarm',role='primary',material='paint')
        link3(m,(-20,-15,0),(58,-9,s*99),2.8,label='Sehne',role='accent')
    # Two long guide cheeks leave the bolt path open between them.
    for z in (-11,6):
        block(m,-23,140,-10,-2,z,z+5,label='Bolzenauflage',role='medium',material='metal',cut=1)
        plate(m,[(49,8),(119,8),(134,17),(70,23),(40,16)],z-2,z+7,label='Führungsschale')
    tube(m,105,151,-15,0,7,4,label='Lauf')
    tube(m,104,116,-15,0,10,4,label='Führungssattel',role='primary',material='paint')
    tube(m,142,163,-15,0,10,4.5,label='Mündung',role='dark')
    block(m,-29,-16,-20,-5,-7,7,label='Sehnenschloss',role='dark',material='metal')
    rod(m,(-32,17),(12,40),6,13,19,label='Spannhebel',role='accent',material='metal')
    block(m,-37,-25,5,22,9,19,label='Spannlager',role='medium',material='metal')
    rail_on(m,-76,-34,-27)
    return m


def rocketside():
    m=[]
    plate(m,[(-82,-27),(-49,-38),(-17,-28),(1,-13),(-6,11),(-65,15),(-83,3)],-13,13,label='Gehäuse')
    tube(m,-11,104,-13,0,14,9,label='Rohr',role='medium')
    tube(m,5,108,-13,0,15,13.8,label='Lauf',role='primary',material='paint')
    tube(m,100,125,-13,0,19,10,label='Mündung',role='dark')
    # Winged slide guides the outer tube, leaving its forward mouth open.
    for z in (-18,13):
        plate(m,[(-55,-29),(76,-35),(97,-26),(40,-20),(-55,-20)],z,z+5,label='Schlitten')
        block(m,-53,-39,-24,1,z,z+5,label='Schlittenführung',role='medium',material='metal')
    controls(m,-75,top=12,length=48,width=24)
    # Seat the cartridge inside the rear grip wall, clear of the guard's rear link.
    plate(m,[(-86,35),(-75,31),(-72,68),(-88,75)],-8,8,label='Raketenmagazin',role='medium',material='plastic')
    block(m,-91,-68,68,78,-11,11,label='Magazinboden',role='accent',material='metal')
    for z in (-17,13):
        for x in (24,40,56):
            tube(m,x,x+8,-13,z,3.8,2,label='Abgasöffnungen',role='dark',sides=8)
    rail_on(m,-65,-21,-36)
    return m


def rocketpulse():
    m=[]
    # Tall rear triangular reservoir creates a distinct bullpup silhouette.
    plate(m,[(-108,-32),(-50,-29),(-9,-14),(12,7),(-21,30),(-93,24),(-112,4)],-15,15,label='Gehäuse')
    plate(m,[(-111,24),(-90,26),(-101,48),(-123,36),(-128,-16),(-114,-24)],-13,13,label='Schaft')
    block(m,-130,-119,-20,39,-16,16,label='Schulterpolster',role='dark',material='rubber')
    tube(m,-7,142,-8,0,12,7,label='Rohr',role='medium')
    tube(m,18,134,-8,0,14,11.8,label='Lauf',role='dark')
    tube(m,132,163,-8,0,19,8,label='Mündung',role='accent',material='metal')
    for z in (-19,13):
        plate(m,[(1,-17),(67,-31),(133,-20),(134,-12),(75,-14),(12,-7)],z,z+6,label='Vorderflügel')
        block(m,11,24,-15,7,z,z+6,label='Rohrhalter',role='medium',material='metal')
        block(m,115,124,-17,5,z,z+6,label='Rohrhalter',role='medium',material='metal')
    mag(m,-94,top=24,length=41,label='Raketenmagazin',tilt=-8)
    controls(m,-26,top=24,width=31)
    block(m,-61,-30,-18,-6,15,19,label='Verschluss',role='medium',material='metal')
    rail_on(m,-89,-40,-34)
    return m


def slug():
    m=[]
    plate(m,[(-76,-18),(-32,-30),(16,-19),(23,10),(-5,24),(-65,22)],-14,14,label='Gehäuse')
    shoulder(m,-149,-70,top=-15,bottom=31)
    tube(m,11,149,-6,0,10,5.6,label='Lauf')
    tube(m,140,169,-6,0,14,6,label='Mündung',role='dark')
    # Four lands on the muzzle's inner wall imply one rifled bore, not a bundle.
    for y,z in ((-11.7,0),(-.3,0),(-6,5.7),(-6,-5.7)):
        tube(m,145,166,y,z,.7,.3,label='Laufzug',role='medium',sides=8)
    for z in (-16,11):
        plate(m,[(23,9),(91,8),(115,20),(84,31),(20,25)],z,z+5,label='Vorderschale')
        block(m,40,50,-9,20,z,z+5,label='Laufklammer',role='medium',material='metal')
        block(m,96,105,-9,21,z,z+5,label='Laufklammer',role='medium',material='metal')
    for x0,x1 in ((40,50),(96,105)):
        tube(m,x0,x1,-6,0,13,5.6,label='Laufsattel',role='medium')
    controls(m,-61,top=22,width=26); mag(m,2,top=24,length=40,label='Slug-Magazin',tilt=10)
    block(m,-41,-10,-17,-6,14,18,label='Verschluss',role='medium',material='metal')
    rail_on(m,-59,-13,-29)
    return m


def heat():
    m=[]
    plate(m,[(-90,-26),(-43,-38),(-7,-24),(10,0),(-12,22),(-77,22)],-14,14,label='Gehäuse')
    shoulder(m,-146,-83,top=-19,bottom=28)
    controls(m,-67,top=20,width=29)
    # A fixed underslung heat store replaces a removable ammunition module.
    plate(m,[(-23,19),(39,15),(76,24),(63,42),(0,40),(-23,29)],-18,18,label='Hitzespeicher',role='dark',material='metal')
    tube(m,1,131,-8,0,10,4.5,label='Lauf')
    tube(m,123,157,-8,0,16,6,label='Mündung',role='medium')
    for z in (-24,18):
        plate(m,[(1,-25),(76,-38),(117,-22),(102,-16),(10,-12)],z,z+6,label='Entlüftungsklappe')
        block(m,4,17,-21,2,z,z+6,label='Klappengelenk',role='medium',material='metal')
        for x in (21,37,53,69,85):
            block(m,x,x+5,-17,19,z-1,z+7,label='Kühlrippen',role='medium',material='metal',cut=1)
    block(m,-31,-7,-6,-2,14,18,label='Hitzeanzeige',role='accent',material='light',emit=True,cut=.5)
    rail_on(m,-72,-30,-36)
    return m


def micro():
    m=[]
    plate(m,[(-89,-20),(-49,-31),(-15,-19),(-8,10),(-27,27),(-78,21)],-14,14,label='Gehäuse')
    shoulder(m,-142,-83,top=-15,bottom=29)
    controls(m,-72,top=19,width=28)
    tube(m,-9,129,-8,0,18,12,label='Rohr',role='medium')
    tube(m,4,121,-8,0,19,17.8,label='Lauf',role='primary',material='paint')
    tube(m,121,151,-8,0,23,13,label='Mündung',role='dark')
    # Exactly one live missile is inside, recessed behind the muzzle.
    add(m,cyl(21,99,-8,0,8,'#888888'),'Mikrorakete','accent','metal')
    for z in (-20,15):
        plate(m,[(1,-25),(89,-36),(119,-25),(109,-18),(3,-17)],z,z+5,label='Rohrschale')
    block(m,-12,10,-30,-22,-13,13,label='Ladeklappe',role='accent',material='metal')
    block(m,-18,-7,-25,-14,-17,17,label='Klappenscharnier',role='medium',material='metal')
    # External hand-loaded reserve is separate from the bore and has no feed path.
    block(m,18,87,26,34,-16,16,label='Vorratsträger',role='medium',material='metal')
    block(m,20,30,7,30,-7,7,label='Vorratshalter',role='dark',material='metal')
    for z in (-10,10):
        add(m,cyl(23,83,40,z,5,'#888888'),'Raketenvorrat','accent','metal')
        block(m,34,41,30,46,z-6,z+6,label='Halteclip',role='dark',material='metal',cut=1)
    rail_on(m,-75,-32,-30)
    return m


def spread():
    m=[]
    plate(m,[(-87,-23),(-58,-35),(-32,-20),(-26,6),(-64,20),(-89,10)],-13,13,label='Gehäuse')
    for z in (-17,11):
        plate(m,[(-40,-26),(47,-31),(58,-18),(45,-14),(-38,-15)],z,z+6,label='Kipprahmen')
        rod(m,(-37,28),(40,44),7,z,z+6,label='Kipprahmen')
        rod(m,(40,44),(50,-18),7,z,z+6,label='Kipprahmen')
    drum_chambers(m,-24,22,cy=15,radius=25,count=5)
    tube(m,22,89,-10,0,12,7,label='Lauf')
    # One broad annular muzzle; its part bounds are centered on the open channel.
    tube(m,78,122,-10,0,22,12,label='Mündung',role='dark',sides=10)
    for z in (-17,12):
        plate(m,[(28,-25),(71,-37),(92,-28),(78,-20),(28,-16)],z,z+5,label='Laufschale')
        block(m,-37,-23,23,37,z-1,z+6,label='Scharnier',role='medium',material='metal')
    block(m,-45,-27,-34,-25,-8,8,label='Riegel',role='accent',material='metal')
    plate(m,[(-69,-22),(-74,-39),(-62,-40),(-56,-24)],-6,6,label='Hahn',role='accent',material='metal')
    controls(m,-83,top=17,length=50,width=23)
    rail_on(m,-63,-29,-34)
    return m


DESIGNS = (
 ('scout','Mint Heron','Scout-Gewehr','Schlanker Langlauf mit offenem Blätter-Vorderschaft.',scout,
  ('Kastenmagazin unter dem vorderen Gehäuse entriegeln und nach unten wechseln.','Release and replace the box magazine below the forward receiver.'),
  ('Seitlichen Verschluss am fliederfarbenen Einsatz zurückziehen und freigeben.','Pull and release the side bolt in the lilac insert.'),
  ('Ein Druck löst einen Einzelschuss aus; die Mechanik lädt halbautomatisch nach.','Each press fires one shot; the mechanism cycles semi-automatically.')),
 ('handcannon','Lime Dahlia','Handfeuerwaffe','Offener Brückenrahmen um sechs einzelne Trommelkammern.',handcannon,
  ('Trommel aus dem offenen unteren Träger schwenken und die sechs Kammern einzeln bestücken.','Swing the cylinder out of its open lower cradle and load the six chambers individually.'),
  ('Den limettfarbenen Hahn nach hinten spannen; die obere Kammer fluchtet mit dem Lauf.','Cock the lime hammer; the upper chamber aligns with the barrel.'),
  ('Abzug drücken; der Hahn zündet die obere Kammer hinter dem kurzen Rohrlauf.','Press the trigger; the hammer ignites the upper chamber behind the short barrel.')),
 ('linear','Orchid Lattice','Lineares Fusionsgewehr','Seitlich gespreizte Schienen mit drei offenen Feldringen.',linear,
  ('Die untere Energiezelle lösen und durch eine geladene Zelle ersetzen.','Release the lower energy cell and insert a charged replacement.'),
  ('Abzug halten: Die Ladekammer speist die beiden seitlichen Beschleunigerschienen.','Hold the trigger: the charge chamber feeds both lateral accelerator rails.'),
  ('Nach dem Laden tritt der Impuls durch den freien Ringkanal an der Mint-Gabel aus.','After charging, the pulse exits through the open ring channel of the mint fork.')),
 ('breech','Coral Snap','Spezial-Granatwerfer','Einzelner Kipplauf mit zwei seitlichen Blattflügeln.',breech,
  ('Korallriegel lösen, den einzelnen Lauf am unteren Scharnier abkippen und eine Granate einlegen.','Release the coral lock, tilt the single barrel on its lower hinge and insert one grenade.'),
  ('Den Kipplauf hochschwenken, bis die obere Verriegelung einrastet.','Swing the break barrel up until the upper latch locks.'),
  ('Abzug drücken; die einzelne Granate verlässt die breite offene Mündung.','Press the trigger; the single grenade leaves the broad open muzzle.')),
 ('drum','Lime Carousel','Schwerer Granatwerfer','Sechs freiliegende Granatkammern in offenem Zweibogen-Träger.',drum,
  ('Seitliche violette Ladeklappe öffnen und jede Granatkammer beim Weiterdrehen einzeln laden.','Open the violet side hatch and load each grenade chamber while indexing the drum.'),
  ('Klappe schließen und die obere Kammer hinter dem Rohr verriegeln.','Close the hatch and lock the upper chamber behind the barrel.'),
  ('Ein Abzugsdruck verschießt die obere Granate; die Trommel taktet zur nächsten Kammer.','Each press fires the upper grenade; the drum indexes to the next chamber.')),
 ('machine','Mint Loom','Maschinengewehr','Offener Blättermantel mit außen geführtem Patronengurt.',machine,
  ('Munitionskasten ansetzen, Deckel öffnen und den sichtbaren Gurt in die Zuführung legen.','Attach the ammunition box, open the cover and lay the visible belt into the feed.'),
  ('Zuführdeckel schließen und den seitlichen Verschluss nach hinten ziehen.','Close the feed cover and pull the side bolt rearward.'),
  ('Gehaltene Abzugbetätigung führt den Gurt aus dem Kasten über die sichtbaren Verbinder nach.','Holding the trigger draws the belt from the box over its visible connecting links.')),
 ('sword','Lunar Petal','Schwert','Zweiteilige Sichelklinge um einen freiliegenden dunklen Erl.',sword,
  ('Die seitliche Energiezelle am Parierblock entriegeln und wechseln.','Release and replace the side energy cell on the guard housing.'),
  ('Den Zellkontakt am Parierblock aktivieren; die geteilte Klinge lädt sich auf.','Activate the cell contact at the guard housing to charge the split blade.'),
  ('Über den gummierten Griff führen; die breite Parierstange schützt die Hand.','Guide the blade with the rubber grip; the broad crossguard protects the hand.')),
 ('glaive','Jade Canopy','Glefe','Blattschneide über freiem Emitter mit paarigen Schildblättern.',glaive,
  ('Den Energiespeicher im Kopfgehäuse über den hinteren Servicekontakt laden.','Charge the head housing energy store through its rear service contact.'),
  ('Schildflügel über ihre seitlichen Gelenke nach außen stellen.','Deploy both shield wings on their lateral joints.'),
  ('Abzug an der Stange drücken: Der unter der Klinge liegende Emitter strahlt nach vorn.','Press the shaft trigger: the emitter beneath the blade projects forward.')),
 ('crossbow','Violet Span','Schwere Armbrust','Breit gespannte Querarme über offener doppelter Bolzenauflage.',crossbow,
  ('Einen schweren Bolzen zwischen die beiden offenen Führungswangen legen.','Lay one heavy bolt between the two open guide cheeks.'),
  ('Den seitlichen Spannhebel ziehen; die Sehne wird vom Querarm zum hinteren Schloss gespannt.','Pull the side cocking lever to tension the string from both transverse tips to the rear latch.'),
  ('Abzug drücken: Die Sehne läuft von beiden Armspitzen vor und beschleunigt den Bolzen.','Press the trigger: the string moves forward from both limb tips and accelerates the bolt.')),
 ('rocketside','Coral Pod','Raketenpistole','Korallener Rohrkopf mit seitlich geführten Schlittenflügeln.',rocketside,
  ('Das Mint-bekappte Raketenmagazin im Griff lösen und von unten ersetzen.','Release the mint-capped rocket magazine in the grip and replace it from below.'),
  ('Die beiden verbundenen Schlittenwangen nach hinten ziehen und freigeben.','Pull and release the paired slide cheeks.'),
  ('Ein Druck startet eine Rakete; seitliche Abgasöffnungen entlasten das Rohr.','Each press launches one rocket; lateral exhaust ports relieve the tube.')),
 ('rocketpulse','Mint Cluster','Raketen-Impulsgewehr','Hoher Heckkeil mit zurückgesetztem Raketenmagazin und Rohrgabel.',rocketpulse,
  ('Das schräg hinter dem Griff sitzende Raketenmagazin nach unten herausziehen und wechseln.','Pull down and replace the angled rocket magazine behind the grip.'),
  ('Den Flieder-Verschluss über dem hinteren Magazin einmal durchziehen.','Cycle the lilac bolt above the rear magazine.'),
  ('Abzug drücken: Die Impulsfolge führt Raketen nacheinander in das einzelne Rohr.','Press the trigger: the pulse sequence feeds rockets successively into the single tube.')),
 ('slug','Jade Reed','Slug-Schrotflinte','Langer gezogener Einzellauf über konkaven Vorderschaftblättern.',slug,
  ('Das gekrümmte Slug-Magazin vor dem Abzugsbügel lösen und nach unten wechseln.','Release and replace the curved slug magazine ahead of the trigger guard.'),
  ('Den seitlichen Verschluss zurückziehen, um einen einzelnen Slug zuzuführen.','Retract the side bolt to chamber a single slug.'),
  ('Abzug drücken: Ein Slug läuft durch den gezogenen Einzellauf zur offenen Mündung.','Press the trigger: one slug travels through the single rifled barrel to the open muzzle.')),
 ('heat','Azalea Furnace','Hitze-Blaster','Fester unterer Wärmespeicher zwischen zwei aufklappbaren Kühlblättern.',heat,
  ('Kein Magazinwechsel: Die Reserve speist das System; den festen Hitzespeicher kontrollieren.','No magazine exchange: reserve ammunition feeds the system; monitor the fixed heat store.'),
  ('Die beiden seitlichen Entlüftungsklappen zum Abkühlen der Rippen öffnen.','Open both lateral vent flaps to cool the fins.'),
  ('Abzug drücken für Impulssalven; die limettfarbene Anzeige zeigt die steigende Hitze.','Press for pulse bursts; the lime indicator shows rising heat.')),
 ('micro','Coral Courier','Mikroraketen-Granatwerfer','Einzelrohr mit separatem offenem Vorrat unter dem Vorderschaft.',micro,
  ('Ladeklappe öffnen und eine einzelne Mikrorakete von Hand aus dem Außenvorrat einlegen.','Open the loading hatch and manually insert one micro-missile from the external reserve.'),
  ('Die korallfarbene Ladeklappe schließen und verriegeln; der Außenvorrat bleibt getrennt.','Close and lock the coral loading hatch; the external reserve remains separate.'),
  ('Abzug drücken: Nur die einzelne Rakete im Rohr startet, ohne automatische Zuführung.','Press the trigger: only the single missile in the tube launches, without automatic feed.')),
 ('spread','Mint Poppy','Streuschuss-Handfeuerwaffe','Fünfkammer-Kipprahmen mit großer offener Blütenmündung.',spread,
  ('Mint-Riegel lösen, den Rahmen am unteren Scharnier abkippen und fünf Kammern einzeln laden.','Release the mint latch, tilt the frame on its lower hinge and load all five chambers individually.'),
  ('Rahmen hochklappen und verriegeln; den Mint-Hahn spannen.','Swing the frame shut, lock it and cock the mint hammer.'),
  ('Abzug drücken: Die obere Trommelkammer gibt die Ladung durch die breite Streumündung ab.','Press the trigger: the upper cylinder chamber discharges through the broad spread muzzle.')),
)


def load_new():
    result=[]
    for n,(row,palette) in enumerate(zip(DESIGNS,PALETTES),11):
        slug,name,kind,form,builder,reload,action,fire=row
        colors=dict(zip(('primary','medium','dark','accent'),palette[:4]))
        metadata=meta(slug,name,kind,form,[form,'Eigenständiges K-Konzept; Bedienung und bewegliche Teile sind Vorschläge.'])
        metadata.update(type_number=n,series='fluxbloom',variant='K',variant_name='Flux Bloom',palette=list(palette[:4]),palette_name=palette[4])
        metadata['operation_intent']={k:dict(zip(('de','en'),v)) for k,v in (('reload',reload),('action',action),('fire',fire))}
        model=builder()
        for part in model:
            if part.label=='Abzug': part.role='accent'
            part.color=colors[part.role]
        result.append((metadata,model))
    return result
