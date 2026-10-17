"""Flux Bloom: a faceted annular induction cage around an exposed core."""
from .common import *

P, M, D, A = '#00B5A5', '#BDD8D9', '#183B47', '#FFB83E'
META = meta('fusion', 'Fusionsgewehr', 'Energiegewehr',
            'Große facettierte Turbinenkammer mit freiliegendem Kern und Heckflosse.',
            ['Die Speichen verbinden den schmalen Laufkern mit den beiden Induktionsringen.',
             'Die hellen Ringe sind geschlossene Bauteile mit offenem Zentrum; der kleine Kernlauf bleibt ablesbar.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Petrol · Eisgrau · Tiefsee · Safran')

META.update(name='Ion Orchid', kind='Fusionsgewehr')


def build():
    m = []
    plate(m,[(-82,-22),(-34,-28),(-10,-18),(1,14),(-15,28),(-72,25),(-87,8)],
          -16,16,P,'Gehäuse')
    rod(m,(-137,-22),(-77,-15),11,-11,11,P,'Schaft','primary','paint')
    rod(m,(-133,35),(-78,11),10,-11,11,P,role='primary',material='paint')
    block(m,-144,-132,-25,41,-15,15,D,'Schulterpolster','dark','rubber',cut=5)
    tube(m,-12,94,-4,0,11,5,M,'Lauf')
    # Polygonal outer bearing rings. Four radial spokes touch each ring and core.
    for x in (-6,57):
        tube(m,x,x+10,-4,0,33,25,P,'Induktionsring','primary','paint',sides=8)
        block(m,x+1,x+9,-31,-13,-5,5,M,'Kernsattel','medium','metal',cut=1)
        block(m,x+1,x+9,5,23,-5,5,M,'Kernsattel','medium','metal',cut=1)
        block(m,x+1,x+9,-9,1,-28,-9,M,'Kernsattel','medium','metal',cut=1)
        block(m,x+1,x+9,-9,1,9,28,M,'Kernsattel','medium','metal',cut=1)
    # Three broad axial vanes read as a turbine cage, leaving visible gaps.
    for z0,z1 in ((-24,-17),(17,24)):
        plate(m,[(-2,-24),(58,-25),(65,-16),(3,-14)],z0,z1,P,'Kühlflügel')
        plate(m,[(-2,16),(62,16),(65,24),(3,25)],z0,z1,P,'Kühlflügel')
    block(m,-1,63,-36,-28,-6,6,M,'Käfigrücken','medium','metal',cut=2)
    tube(m,87,107,-4,0,16,7,D,'Mündung','dark',sides=8)
    control_group(m,-66,top=23,grip_length=42,magazine_x=-16,
                  magazine_length=37,magazine_tilt=7,guard_width=28)
    block(m,-65,-18,-32,-23,-8,8,P,'Schienensockel',cut=2)
    rail(m,-70,-16,y=-36)
    optic(m,-58,y=-36)
    for x in (12,28,44):
        block(m,x,x+8,-8,-5,10,12,A,'Feldstatus','accent','light',emit=True,cut=.5)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = {'primary':P,'medium':M,'dark':D,'accent':A}[p.role]
    return m
