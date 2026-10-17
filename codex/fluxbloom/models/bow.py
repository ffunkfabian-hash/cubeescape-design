"""Flux Bloom: angular recurve limbs, taut rear string and eccentric arrow guide."""
from .common import *

P, M, D, A = '#E5E5DD', '#E451AE', '#263C42', '#A5E759'
META = meta('bow', 'Energiebogen', 'Magnetischer Recurvebogen',
            'Hoher eckiger Recurve mit nach vorn versetztem Griff und freier Sehne.',
            ['Die gespannte Sehne verbindet beide rückgebogenen Wurfarmspitzen bei x=-50; Griff und Riser liegen deutlich davor.',
             'Lauf/Mündung bezeichnen die fiktive offene Magnet-Pfeilführung; Magazin die seitliche Energiezelle und Schaft die Unterarmstütze.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Porzellan · Pink · Tannengrau · Chartreuse')

META.update(name='Porcelain Arc', kind='Bogen')


def build():
    m=[]
    # Mirrored load-bearing limbs form a recurved outline, not a solid crescent.
    upper=[(24,-21),(48,-30),(43,-63),(14,-106),(-18,-132),(-50,-128),
           (-52,-121),(-24,-119),(-3,-98),(21,-57)]
    plate(m,upper,-8,8,P,'Oberer Wurfarm')
    plate(m,[(x,-y) for x,y in upper],-8,8,P,'Unterer Wurfarm')
    plate(m,[(25,-33),(48,-32),(58,-17),(57,8),(45,16),(31,11),(20,-9)],
          -13,13,M,'Gehäuse','medium','metal')
    # The limb tips extend across x=-50,y=+-125 and directly anchor the string.
    rod(m,(-50,-125),(-50,125),1.8,-1.5,1.5,D,'Sehne','dark','plastic')
    for sign in (-1,1):
        block(m,-53,-45,sign*125-4,sign*125+4,-10,10,D,'Sehnenkerbe','dark','metal',cut=1)
    # Eccentric riser keeps the shooting and string corridors clear of the grip.
    plate(m,[(23,6),(38,7),(39,43),(27,51),(16,42)],-9,9,D,'Griff','dark','rubber')
    rod(m,(32,42),(35,28),7,-9,9,M,'Riserbrücke','medium','metal')
    rod(m,(33,42),(51,35),5,-7,7,M,'Bügel')
    rod(m,(51,35),(59,9),5,-7,7,M)
    plate(m,[(43,9),(49,10),(47,22),(43,26),(40,23)],
          5,11,A,'Abzug','accent','metal')
    rod(m,(27,40),(-9,53),8,-7,7,M,'Schaft','medium','metal')
    block(m,-18,-6,45,62,-11,11,D,'Unterarmpolster','dark','rubber',cut=3)
    block(m,53,74,-13,6,-10,10,M,'Führungssockel','medium','metal',cut=2)
    tube(m,55,98,-8,0,4,2,M,'Lauf')
    tube(m,91,108,-8,0,6,2.5,D,'Mündung','dark',sides=8)
    plate(m,[(58,3),(74,3),(81,29),(67,34),(59,24)],
          -8,8,D,'Magazin','dark','plastic')
    block(m,47,81,-24,-12,-7,7,P,'Schienensockel',cut=1)
    rail(m,46,84,y=-28)
    optic(m,54,y=-28)
    block(m,60,70,-4,-1,10,12,A,'Ladestatus','accent','light',emit=True,cut=.5)
    for p in m:
        p.color={'primary':P,'medium':M,'dark':D,'accent':A}[p.role]
    return m
