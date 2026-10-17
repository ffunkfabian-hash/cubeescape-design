"""K03: scalloped coil cradle with exposed annular stages."""
from .common import *

P, M, D, A = '#157E86', '#A4DDD5', '#253D49', '#FFCB3F'
META = meta('impulse', 'Tidal Comb', 'Impulsgewehr',
            'Gezackte Kühlkrone · offener Spulenkäfig',
            ['Drei ringförmige Impulsstufen liegen zwischen zwei gewellten Lastträgern.',
             'Eine dünne durchgehende Laufseele und die offene Mündung bleiben ablesbar.',
             'Die gelben Flächen markieren Stromanschluss und verriegelbare Energiezelle.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Petrol · Gletscherminze · Tiefsee · Safran')


def build():
    m = []
    plate(m,[(-61,-13),(-47,-27),(-9,-25),(14,-9),(12,13),
             (-8,26),(-44,23),(-61,10)],-14,14,label='Gehäuse')
    # The repeated scoops are load-bearing radiator roots, not surface decals.
    plate(m,[(-5,-23),(10,-41),(22,-41),(25,-27),(37,-26),
             (46,-43),(58,-43),(62,-27),(75,-24),(87,-38),
             (99,-35),(105,-19),(94,-14),(18,-17)],-9,9,label='Kühlkrone')
    plate(m,[(-2,12),(16,15),(29,25),(45,18),(62,27),(78,18),
             (98,16),(104,23),(83,33),(61,35),(44,30),(28,35),(8,29)],
          -10,10,role='primary')
    tube(m,-1,126,-5,0,6,3.5,label='Lauf',role='dark')
    for i,x in enumerate((19,48,78)):
        tube(m,x,x+9,-5,0,20,12,label='Impulsstufe' if i==0 else '',
             role='medium',material='metal')
        # Three short side terminals describe power flow without filling gaps.
        block(m,x+1,x+7,-8,-2,18,21,role='accent',material='plastic')
    tube(m,113,133,-5,0,11,4,label='Mündung',role='primary')
    control_group(m,-47,top=22,grip_length=41,magazine_x=10,
                  magazine_length=37,magazine_tilt=-3,guard_width=29)
    block(m,6,32,54,63,-10,10,role='accent',material='plastic')
    rod(m,(-103,-7),(-57,-9),9,-10,10,label='Schaft',role='primary')
    rod(m,(-99,28),(-57,8),7,-8,8,role='primary')
    rod(m,(-103,-9),(-100,31),10,-12,12,role='dark',material='rubber')
    rail(m,-49,-9,y=-30)
    optic(m,-44,y=-30)
    status(m,-32,0,z=15,length=10)
    colors = dict(primary=P, medium=M, dark=D, accent=A)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = colors[p.role]
    return m
