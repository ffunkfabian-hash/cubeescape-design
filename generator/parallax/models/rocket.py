"""A genuinely open launcher tube with a left-offset detachable optic."""
from .common import *

META=meta('rocket','Gatekeeper R-1','Raketenwerfer',
          'OFFENES ROHR · LINKE SEITENSCHIENE · ZWEI HALTESÄTTEL',
          'Startrohr und beide Abschlussringe haben eine durchgehende freie '
          'Öffnung; keine Vollzylinder oder Deckel. Die Visierschiene sitzt '
          'links neben dem Rohr (z positiv) auf zwei seitlichen Auslegern; '
          'Schiene bleibt, Optik einschließlich Klemmen wird abgenommen. '
          'Das Magazin ist eine unten eingeschobene Steuerenergiezelle.')

def build():
    m=[]
    tube(m,-125,147,-24,0,25,20,CREAM,'Gehäuse','primary',sides=12)
    # Exposed forward tube section is a separate annular shell, never a plug.
    tube(m,141,179,-24,0,23,20,STEEL,'Lauf','medium',sides=12)
    tube(m,172,191,-24,0,29,20.5,DARK,'Mündung','medium',sides=12)
    tube(m,-141,-121,-24,0,29,20.5,DARK,'Hinterer Öffnungsring','medium',sides=12)
    # Lower saddles deliberately overlap only the outside wall of the tube.
    for x in (-68,52):
        plate(m,[(x-13,-1),(x+13,-1),(x+17,11),(x-17,11)],
              -16,16,STEEL,'Rohrsattel','medium','metal')
    plate(m,[(-82,6),(74,6),(80,15),(72,23),(-78,23)],-12,12,CREAM,'Bediengehäuse')
    control_group(m,-34,22,grip_length=43,magazine_x=28,magazine_length=31,magazine_tilt=0)
    # Rear shoulder support anchors to the receiver, clear of the exhaust bore.
    plate(m,[(-111,1),(-79,7),(-78,18),(-101,15),(-107,37),(-119,37)],
          -12,12,CREAM,'Schaft')
    block(m,-124,-113,8,41,-15,15,DARK,'Schulterpolster','dark','rubber',cut=3)
    # Rail at z=+34 is outside the radius-25 tube, with two visible bridges.
    for x in (-50,16):
        block(m,x,x+9,-36,-28,20,38,STEEL,'Seitlicher Schienenausleger','medium','metal',cut=1)
    rail(m,-53,35,-40,z=35,width=10)
    optic(m,-42,-40,z=35)
    status(m,-19,10,13,13)
    return m
