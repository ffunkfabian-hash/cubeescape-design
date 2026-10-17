"""Flux Bloom: an unobstructed annular launcher with a low eccentric saddle."""
from .common import *

P, M, D, A = '#F4BD30', '#BBC7D3', '#24354B', '#FF597C'
META = meta('rocket', 'Raketenwerfer', 'Schulterwerfer',
            'Durchgehend offenes Achteckrohr über einem asymmetrischen Untersattel.',
            ['Hauptrohr, Heckring und Mündung besitzen denselben freien Durchlass; kein Sockel ragt in den Innenkanal.',
             'Visierschiene und abnehmbares Reflexvisier sitzen links bei positivem z; Schulter und Griff bleiben unter dem Rohr.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Sonnengelb · Wolkengrau · Marine · Koralle')

META.update(name='Solar Halo', kind='Raketenwerfer')


def build():
    m=[]
    # Every bore is coaxial and has radius 22; there are no rear caps.
    tube(m,-117,141,-12,0,27,22,P,'Lauf','primary','paint',sides=12)
    tube(m,-125,-108,-12,0,31,22,D,'Heckring','dark',sides=12)
    tube(m,132,155,-12,0,34,22,M,'Mündung','medium',sides=12)
    # y >= 12 is outside the free bore (axis y=-12, bore radius 22).
    plate(m,[(-64,12),(35,12),(55,21),(46,37),(-49,37),(-69,27)],
          -16,16,D,'Gehäuse','dark','metal')
    plate(m,[(-60,15),(10,15),(26,25),(15,33),(-54,33)],
          16,22,P,'Servicesattel')
    rod(m,(-116,21),(-61,21),13,-14,14,P,'Schaft','primary','paint')
    block(m,-125,-113,17,49,-19,19,D,'Schulterpolster','dark','rubber',cut=4)
    control_group(m,-37,top=34,grip_length=45,magazine_x=15,
                  magazine_length=33,magazine_tilt=5,guard_width=28)
    plate(m,[(67,13),(101,13),(108,20),(99,35),(76,33),(64,23)],
          -13,13,P,'Vordergriff')
    # z >= 24 bypasses the entire 22-unit bore, including the rail supports.
    for x in (-34,24):
        block(m,x,x+10,-29,-17,24,33,P,'Linker Schienensattel',cut=1)
    rail(m,-39,43,y=-33,z=30,width=11)
    optic(m,-24,y=-33,z=30)
    block(m,-41,-20,23,26,22,24,A,'Ladestatus','accent','light',emit=True,cut=.5)
    for p in m:
        if p.label=='Abzug':
            p.role='accent'
        p.color={'primary':P,'medium':M,'dark':D,'accent':A}[p.role]
    return m
