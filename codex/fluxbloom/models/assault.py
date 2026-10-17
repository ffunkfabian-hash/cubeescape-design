"""K02: offset split shells and an open diagonal rear truss."""
from .common import *

P, M, D, A = '#295AD1', '#B5CAE7', '#253147', '#FF765F'
META = meta('assault', 'Split Current', 'Sturmgewehr',
            'Versetzte Keilschalen · diagonaler Heckträger',
            ['Oberer Lastträger und untere Schale lassen das Verschlussfenster offen.',
             'Der dreieckige Schaft führt die Last über zwei sichtbare Streben.',
             'Ein kompakter Reflexaufsatz sitzt auf einer eigenen Schienenbrücke.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Kobalt · Eisblau · Tintenblau · Koralle')


def build():
    m = []
    plate(m,[(-64,-24),(-37,-30),(47,-42),(99,-31),(109,-19),
             (84,-17),(42,-25),(-41,-12),(-64,-9)],-12,9,label='Gehäuse')
    plate(m,[(-61,4),(-32,0),(33,7),(88,-1),(103,9),(82,23),
             (13,30),(-55,23)],-9,13,role='primary')
    plate(m,[(-61,-22),(-39,-24),(-31,21),(-58,22)],-11,11,
          role='medium',material='metal')
    block(m,-36,91,-9,-2,-5,5,role='dark',material='metal')
    # Forward junction joins both shells; narrow bore proceeds through it.
    plate(m,[(84,-24),(98,-26),(109,-13),(104,12),(90,19),
             (86,3)],-11,11,role='medium',material='metal')
    tube(m,90,148,-7,0,6,3.6,label='Lauf')
    tube(m,139,159,-7,0,9,4.2,label='Mündung',role='dark')
    plate(m,[(26,-32),(58,-35),(83,-29),(59,-26)],10,14,
          role='accent',material='plastic')
    control_group(m,-45,top=22,grip_length=42,magazine_x=27,
                  magazine_length=45,magazine_tilt=9,guard_width=30)
    rod(m,(-125,-13),(-61,-13),8,-9,9,label='Schaft',role='primary')
    rod(m,(-125,34),(-61,-13),8,-9,9,role='primary')
    rod(m,(-125,-13),(-125,34),10,-10,10,role='dark',material='rubber')
    plate(m,[(-119,-23),(-84,-23),(-66,-13),(-112,-13)],-12,12,
          role='medium',material='plastic')
    rail(m,-35,30,y=-39)
    block(m,-33,-25,-35,-22,-5,5,role='dark',material='metal')
    block(m,20,28,-35,-28,-5,5,role='dark',material='metal')
    optic(m,-26,y=-39)
    status(m,-20,12,z=14,length=12)
    colors = dict(primary=P, medium=M, dark=D, accent=A)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = colors[p.role]
    return m
