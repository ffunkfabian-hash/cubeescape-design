"""Open dual accelerator rails carried by one lower structural keel."""
from .common import *

META=meta('trace','Parallax T-8','Spurgewehr',
          'ZWEI FREIE BESCHLEUNIGERSCHIENEN · OFFENE SPUR · KEILHECK',
          'Die zwei getrennten Beschleunigerschienen sind hinten im Gehäuse '
          'und vorne im offenen Mündungsrahmen gefasst; ihr Zwischenraum '
          'bleibt frei. Die Unterseite trägt beide über eine verbundene '
          'Kielstruktur. Beschleunigerschienen sind gemeinsam als Lauf bezeichnet.')

def build():
    m=[]
    plate(m,[(-68,-16),(-49,-26),(34,-26),(49,-13),(42,20),
             (13,24),(-56,24),(-69,9)],-14,14,label='Gehäuse')
    stock(m,-126,-66,-4,zwidth=12)
    control_group(m,-39,23,magazine_x=19,magazine_length=39,magazine_tilt=7)
    # Thin, widely separated side rails reveal the central acceleration gap.
    for index,z in enumerate((-13,13)):
        block(m,39,177,-9,9,z-4,z+4,STEEL,'Lauf' if index==0 else 'Zweite Beschleunigerschiene',
              'medium','metal',cut=3)
        block(m,52,166,-3,1,z+(-5 if z<0 else 4),z+(-4 if z<0 else 5),
              ORANGE,'Spuranzeige','accent','light',emit=True,cut=.5)
        rod(m,(47,7),(64,18),5,z-4,z+4,DARK,'Schienenstütze','medium','metal')
        rod(m,(160,18),(174,7),5,z-4,z+4,DARK,'Vordere Schienenstütze','medium','metal')
    block(m,37,175,16,23,-8,8,DARK,'Tragkiel','medium','metal')
    # Side braces tie the keel to both rails without filling their central gap.
    block(m,59,68,14,20,-17,17,STEEL,'Hintere Querbrücke','medium','metal')
    block(m,156,164,14,20,-17,17,STEEL,'Vordere Querbrücke','medium','metal')
    tube(m,171,188,0,0,19,11,DARK,'Mündung','medium',sides=8)
    rail(m,-51,24,-31)
    optic(m,-32,-31,long=True)
    side_panel(m,-51,-9,-16,5,15)
    return m
