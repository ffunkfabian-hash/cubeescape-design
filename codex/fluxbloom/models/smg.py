"""Flux Bloom: compact rear-fed coral frame with an asymmetric side cartridge."""
from .common import *

P, M, D, A = '#F45373', '#BBC7F0', '#272E47', '#E4F65A'
META = meta('smg', 'Maschinenpistole', 'SMG',
            'Kurzer Bullpup-Rahmen mit seitlichem Servicekeil und offenem Heck.',
            ['Das Magazin liegt hinter dem Griff; der kurze Lauf sitzt im vorderen Keilsockel.',
             'Das offene Schulterdreieck ist tragend; die linke Seitenkassette bleibt innerhalb der Heckkontur.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P, M, D, A],
            palette_name='Koralle · Lavendel · Nachtblau · Limette')

META.update(name='Coral Loop', kind='Maschinenpistole')


def build():
    m = []
    plate(m, [(-75,-22),(18,-22),(57,-10),(64,6),(44,22),(-66,22),(-80,8)],
          -14,14,P,'Gehäuse')
    # Rear triangle carries the shoulder pad without filling its negative space.
    rod(m,(-107,-22),(-66,-20),9,-10,10,P,'Schaft','primary','paint')
    rod(m,(-105,27),(-69,8),9,-10,10,P,role='primary',material='paint')
    block(m,-115,-103,-26,32,-13,13,D,'Schulterpolster','dark','rubber',cut=4)
    plate(m,[(-71,-15),(-28,-15),(-15,-4),(-34,12),(-71,12)],
          14,22,M,'Einspeisekassette','medium','metal')
    plate(m,[(25,-15),(56,-6),(56,10),(42,17),(24,11)],
          -18,18,M,'Laufsockel','medium','metal')
    tube(m,48,91,-3,0,8,4,M,'Lauf')
    tube(m,86,105,-3,0,11,5,D,'Mündung','dark',sides=8)
    control_group(m,-5,top=20,grip_length=37,magazine_x=-57,
                  magazine_length=40,magazine_tilt=-10,guard_width=29)
    block(m,-21,14,-27,-20,-7,7,P,'Schienensockel',cut=1)
    rail(m,-26,24,y=-31)
    optic(m,-16,y=-31)
    block(m,-67,-45,-6,-3,22,23,A,'Ladestatus','accent','light',emit=True,cut=.5)
    # Role mapping also colors the common removable optic and control assembly.
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = {'primary':P,'medium':M,'dark':D,'accent':A}[p.role]
    return m
