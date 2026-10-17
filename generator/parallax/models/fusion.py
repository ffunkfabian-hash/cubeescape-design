"""Large faceted energy chamber held between explicit structural collars."""
from .common import *

META=meta('fusion','Helion F-3','Fusionsgewehr',
          'BREITE REAKTORKAMMER · HALTERINGE · TIEF SITZENDE ENERGIEZELLE',
          'Die Reaktorkammer ist zwischen hinterem Gehäuse und vorderem '
          'Kopfring verspannt. Leuchtende Fenster liegen auf angeschlossenen '
          'Kammerwänden; untere Zelle im Schacht. Ein offener Düsenring '
          'schließt den kurzen freien Lauf ab.')

def build():
    m=[]
    plate(m,[(-66,-19),(-51,-27),(22,-27),(36,-15),(32,24),
             (-48,26),(-67,12)],-15,15,label='Gehäuse')
    stock(m,-121,-64,-3,zwidth=13)
    control_group(m,-39,25,magazine_x=20,magazine_length=43,magazine_tilt=2)
    tube(m,25,85,-2,0,25,17,CREAM,'Reaktorkammer','primary',sides=10)
    tube(m,27,35,-2,0,27,16,DARK,'Hinterer Kammerring','medium')
    tube(m,79,90,-2,0,27,7,STEEL,'Vorderer Kammerring')
    tube(m,84,135,-2,0,8,4.2,label='Lauf')
    tube(m,127,145,-2,0,14,5.5,DARK,'Mündung','medium')
    # Mechanical tie rods run from one chamber collar to the other.
    for z in (-19,19):
        block(m,31,86,-18,-12,z-3,z+3,STEEL,'Kammerzugstange','medium','metal',cut=1)
        block(m,39,74,-6,1,z+(-6 if z<0 else 3),z+(-3 if z<0 else 6),
              ORANGE,'Kammerfenster','accent','light',emit=True,cut=1)
    block(m,29,88,18,26,-10,10,DARK,'Kammerwiege','medium','metal')
    rail(m,-52,17,-32)
    optic(m,-35,-32)
    side_panel(m,-51,-7,-16,6,16)
    return m
