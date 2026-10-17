"""Deliberately slender free barrel, adjustable stock and uncluttered fore-end."""
from .common import *

META=meta('sniper','Longwatch N-9','Scharfschützengewehr',
          'LANGER FREIER LAUF · VERSTELLSCHAFT · KLARES ABZUGSFENSTER',
          'Der lange dünne Lauf bleibt ab dem kurzen Handschutz sichtbar. '
          'Magazin vor dem Abzug, abgesetzte Wangenauflage und verstellbares '
          'Schulterpolster. Das Zielfernrohr wird mit beiden Klemmen abgenommen. '
          'Schaftrohre und Schaftplatten greifen ausschließlich in Montagebünde.')

def build():
    m=[]
    plate(m,[(-68,-15),(-56,-21),(58,-21),(75,-12),(69,16),
             (46,20),(-59,20),(-70,11)],-11,11,label='Gehäuse')
    # Two narrow stock beams and an angled butt plate make an open silhouette.
    block(m,-143,-66,-5,3,-7,7,STEEL,'Schaft','medium','metal',cut=2)
    rod(m,(-140,27),(-69,9),6,-7,7,CREAM,'Unterer Schaftsteg','primary','paint')
    plate(m,[(-150,-12),(-137,-8),(-139,37),(-153,39),(-159,28),(-155,-3)],
          -12,12,CREAM,'Verstellbare Schulterplatte')
    block(m,-163,-152,-7,36,-14,14,DARK,'Schulterpolster','dark','rubber',cut=4)
    block(m,-133,-88,-16,-4,-12,12,CREAM,'Wangenauflage',cut=4)
    block(m,-118,-103,-4,3,-7,7,STEEL,'Wangenauflagenstütze','medium','metal',cut=1)
    control_group(m,-40,19,magazine_x=22,magazine_length=36,magazine_tilt=1)
    tube(m,65,238,-4,0,4.8,2.9,label='Lauf')
    plate(m,[(59,-15),(101,-13),(105,-6),(99,13),(58,13)],
          -9,9,CREAM,'Kurzer Handschutz')
    tube(m,230,253,-4,0,7,3.5,DARK,'Mündung','medium')
    rail(m,-53,48,-26)
    optic(m,-35,-26,long=True)
    side_panel(m,-49,-2,-13,4,12)
    status(m,10,-14,12,9)
    return m
