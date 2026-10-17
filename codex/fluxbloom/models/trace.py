"""Flux Bloom: a long open tuning fork with a recessed needle emitter."""
from .common import *

P, M, D, A = '#7847D4', '#C6C1F2', '#29243F', '#3CE6C1'
META = meta('trace', 'Strahlengewehr', 'Präzisions-Energiegewehr',
            'Offene, nach vorn gespreizte Beschleunigergabel mit dünnem Kernlauf.',
            ['Obere und untere Zinke umrahmen den schmalen zentralen Emitter; seitliche Klammern tragen beide Zinken.',
             'Das Magazin ist eine Energiezelle; kurze leuchtende Kontakte zeigen nur den Ladezustand.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Violett · Flieder · Aubergine · Mint')

META.update(name='Violet Fork', kind='Spurgewehr')


def build():
    m=[]
    plate(m,[(-81,-25),(-32,-28),(24,-16),(32,8),(7,25),(-69,24),(-83,5)],
          -14,14,P,'Gehäuse')
    rod(m,(-143,-24),(-74,-18),10,-10,10,P,'Schaft','primary','paint')
    rod(m,(-140,29),(-78,7),9,-10,10,M,role='medium',material='metal')
    block(m,-151,-140,-28,35,-14,14,D,'Schulterpolster','dark','rubber',cut=4)
    # Separated prongs deliberately expose the central beam axis.
    plate(m,[(11,-21),(81,-26),(151,-33),(157,-26),(83,-15),(17,-10)],
          -10,10,P,'Beschleuniger oben')
    plate(m,[(13,8),(82,11),(149,22),(156,30),(79,23),(9,20)],
          -10,10,P,'Beschleuniger unten')
    tube(m,13,148,-3,0,4.5,2,M,'Lauf')
    tube(m,141,165,-3,0,7,3,D,'Mündung','dark',sides=8)
    # Side ties bypass the bore; the far/near surfaces reveal fork depth.
    for z0,z1 in ((-16,-10),(10,16)):
        for x,y0,y1 in ((24,-22,21),(86,-24,23)):
            block(m,x,x+7,y0,y1,z0,z1,M,'Feldklammer','medium','metal',cut=1)
    control_group(m,-59,top=22,grip_length=42,magazine_x=-10,
                  magazine_length=36,magazine_tilt=5,guard_width=28)
    block(m,-58,-5,-33,-24,-7,7,P,'Schienensockel',cut=1)
    rail(m,-62,1,y=-37)
    optic(m,-58,y=-37,long=True)
    block(m,-32,-14,-3,0,14,16,A,'Ladestatus','accent','light',emit=True,cut=.5)
    for p in m:
        if p.label == 'Abzug':
            p.role='accent'
        p.color={'primary':P,'medium':M,'dark':D,'accent':A}[p.role]
    return m
