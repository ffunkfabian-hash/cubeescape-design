"""Compact rear-fed receiver, short sleeve and folding shoulder strut."""
from .common import *

META=meta('smg','Switchback M-6','Maschinenpistole',
          'KOMPAKTER BULLPUP · KURZE HÜLSE · FALTSCHAFT',
          'Kurze bullpupartige Silhouette mit Magazin hinter dem Griff. '
          'Der gefaltete Schaftsteg bildet einen sichtbaren Abstand zum Griff; '
          'sein vorderes Gelenk sitzt direkt am Gehäuseheck.')

def build():
    m=[]
    plate(m,[(-65,-17),(-51,-24),(43,-24),(57,-13),(53,17),
             (38,23),(-56,23),(-67,11)],-13,13,label='Gehäuse')
    # Shoulder arm attaches high on the rear, never through the rear magazine.
    plate(m,[(-93,-17),(-63,-13),(-63,-4),(-86,-7),(-88,22),(-98,22)],
          -9,9,STEEL,'Schaft','medium','metal')
    block(m,-102,-92,-18,27,-12,12,DARK,'Schulterpolster','dark','rubber',cut=3)
    control_group(m,-15,22,grip_length=36,magazine_x=-51,
                  magazine_length=35,magazine_tilt=-3,guard_width=26)
    tube(m,47,84,-3,0,7,4,label='Lauf')
    tube(m,70,95,-3,0,12,4.5,DARK,'Mündung','medium')
    block(m,34,54,16,32,-9,9,DARK,'Vorderer Handstopp','dark','rubber',cut=3)
    rail(m,-47,39,-29)
    optic(m,-23,-29)
    side_panel(m,-44,-7,-15,4,14)
    status(m,11,-16,14,11)
    return m
