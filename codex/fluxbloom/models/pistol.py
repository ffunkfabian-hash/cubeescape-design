"""K01: a split hammerhead pistol with a structural heel loop."""
from .common import *

P, M, D, A = '#7651C8', '#D4C6EE', '#29263C', '#CBF34B'
META = meta('pistol', 'Petal Hammer', 'Pistole',
            'Geteilter Hammerkopf · offener Fersenrahmen',
            ['Zwei gegeneinander versetzte Keilschalen umfassen die Laufachse.',
             'Der kurze Schaft ist ein mit dem Griff verbundener Fersenrahmen.',
             'Das Magazin sitzt im Griff; die Reflexoptik ist abnehmbar.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Iris · Flieder · Aubergine · Limette')


def build():
    m = []
    plate(m,[(-35,-32),(-13,-43),(22,-36),(72,-26),(78,-15),
             (49,-12),(13,-21),(-29,-12)],-12,12,label='Gehäuse')
    plate(m,[(-29,-11),(4,-19),(47,-8),(67,3),(48,17),
             (9,23),(-26,16)],-10,10,role='medium',material='metal')
    # Visible web is the load path between both separated wedge shells.
    block(m,-28,-14,-24,18,-9,9,role='dark',material='metal')
    tube(m,38,87,-11,0,6.5,3.8,label='Lauf')
    tube(m,80,96,-11,0,10,4.3,label='Mündung',role='dark')
    plate(m,[(49,-29),(68,-25),(72,-19),(50,-18)],-16,-11,
          role='accent',material='plastic')
    control_group(m,-21,top=18,grip_length=46,grip_width=17,guard_width=30)
    # Grip-contained cartridge, proud heel cap and visibly open U-shaped heel.
    plate(m,[(-29,42),(-18,40),(-21,76),(-35,76)],-7,7,
          label='Magazin',role='medium',material='plastic')
    block(m,-37,-18,74,81,-10,10,role='accent',material='plastic')
    rod(m,(-32,50),(-47,69),5,-10,10,label='Schaft',role='primary')
    rod(m,(-47,69),(-28,80),5,-10,10,role='primary')
    rod(m,(-28,80),(-21,67),5,-10,10,role='primary')
    rail(m,-25,30,y=-42)
    # Feet tie the rail to the angled dorsal shell.
    block(m,-23,-15,-38,-28,-5,5,role='dark',material='metal')
    block(m,20,28,-38,-31,-5,5,role='dark',material='metal')
    optic(m,-14,y=-42)
    status(m,0,-7,z=11,length=11)
    colors = dict(primary=P, medium=M, dark=D, accent=A)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = colors[p.role]
    return m
