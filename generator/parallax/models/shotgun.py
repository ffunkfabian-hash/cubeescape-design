"""Two open bores, a broad pump and an under-receiver cassette."""
from .common import *

META=meta('shotgun','Breakwater S-2','Schrotflinte',
          'DOPPELLAUF · BREITER PUMPGRIFF · FÄCHERSCHAFT',
          'Zwei übereinander liegende offene Läufe werden durch eine gemeinsame '
          'Mündungsbrücke gehalten. Der Pumpgriff umschließt den unteren Lauf; '
          'die kompakte Kassette sitzt vor dem Abzugsbügel im Gehäuseschacht.')

def build():
    m=[]
    plate(m,[(-63,-17),(-51,-23),(26,-23),(40,-12),(37,20),
             (-50,20),(-64,8)],-12,12,label='Gehäuse')
    stock(m,-131,-61,-2,zwidth=12)
    control_group(m,-37,19,magazine_x=16,magazine_length=25,magazine_tilt=1)
    tube(m,30,151,-8,0,6,3.7,label='Lauf')
    tube(m,30,151,7,0,6,3.7)
    # The separated bores and solid bridge remain distinct from either opening.
    tube(m,145,163,-8,0,8,4,DARK,'Mündung','medium')
    tube(m,145,163,7,0,8,4,DARK,role='medium')
    block(m,146,158,-3,3,-5,5,STEEL,'Laufbrücke','medium','metal',cut=1)
    plate(m,[(55,12),(98,12),(105,17),(97,28),(54,28),(48,23)],
          -13,13,DARK,'Pumpgriff','dark','rubber')
    for x in (59,70,81,92):
        block(m,x,x+3,14,26,13,15,STEEL,'Pumpgriffrippe','medium','metal',cut=.5)
    rail(m,-48,27,-28)
    optic(m,-27,-28)
    side_panel(m,-48,-9,-14,5,13)
    status(m,0,-15,13,10)
    return m
