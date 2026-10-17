"""Short wedge receiver, short exposed barrel and heel-supported grip."""
from .common import *

META = meta('pistol','Cinder P-7','Pistole',
            'KURZER KEIL · FERSENSTÜTZE · OFFENE MÜNDUNG',
            'Fiktive Energiepistole. Die Zelle steckt von unten im Griffschacht; '
            'die kompakte Schaftstütze verbindet Griff und hinteres Gehäuse. '
            'Laufhülse und Mündungsring besitzen eine durchgehende Öffnung.')

def build():
    m=[]
    plate(m,[(-34,-12),(-25,-20),(35,-20),(45,-11),(41,13),
             (26,18),(-28,18),(-36,9)],-12,12,label='Gehäuse')
    block(m,10,40,-10,8,-10,10,STEEL,role='medium',material='metal')
    tube(m,38,75,-3,0,7,3.8,label='Lauf')
    tube(m,71,85,-3,0,9,4.6,DARK,'Mündung','medium')
    control_group(m,-15,18,grip_length=39,guard_width=26)
    plate(m,[(-27,49),(-9,49),(-10,62),(-30,62)],-8,8,DARK,'Magazin','dark','plastic')
    block(m,-32,-8,59,65,-10,10,STEEL,'Zellensockel','medium','metal')
    plate(m,[(-35,7),(-29,5),(-29,30),(-37,52),(-44,52),(-39,27)],
          -10,10,CREAM,'Schaft')
    rail(m,-24,24,-25)
    optic(m,-17,-25)
    side_panel(m,-23,5,-10,4,13)
    status(m,12,-13,13,14)
    return m
