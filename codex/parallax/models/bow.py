"""Recurved vertical limbs, real string segments and a fictional magnetic guide."""
from .common import *

META=meta('bow','Arcfall B-5','Bogen',
          'REKURVE WURFARME · SICHTBARE SEHNE · MAGNETISCHE PFEILFÜHRUNG',
          'Fiktiver Energiebogen mit vertikalen Rekurvearmen. Dünne geschlossene '
          'Stäbe bilden die gespannte Sehne. Lauf bezeichnet die offene '
          'magnetische Pfeilführung; Mündung ist deren vorderer offener Ring, '
          'kein konventioneller Waffenlauf. Die Zelle sitzt im unteren '
          'Griffschacht; ein kurzer Schaftsteg verbindet Unterarm und Gehäuse.')

def build():
    m=[]
    plate(m,[(-22,-24),(-8,-33),(20,-28),(31,-15),(30,15),
             (18,29),(-18,25),(-29,12),(-28,-12)],-12,12,label='Gehäuse')
    # Each broad limb is one connected faceted plate, with recurved outer tips.
    plate(m,[(4,-23),(26,-23),(43,-62),(38,-102),(21,-128),
             (7,-125),(24,-98),(27,-65)],-7,7,CREAM,'Oberer Rekurvearm')
    plate(m,[(12,23),(29,20),(44,64),(38,104),(20,129),
             (6,125),(24,99),(28,65)],-7,7,CREAM,'Unterer Rekurvearm')
    # Cable is anchored within the limb tips and nocked at x=-120,y=-6.
    rod(m,(12,-125),(-120,-6),1.5,-1,1,DARK,'Sehne','dark','plastic')
    rod(m,(-120,-6),(12,125),1.5,-1,1,DARK,'Untere Sehne','dark','plastic')
    control_group(m,-17,24,grip_length=39,guard_width=28)
    plate(m,[(-29,55),(-12,55),(-12,72),(-31,72)],-8,8,DARK,'Magazin','dark','plastic')
    block(m,-34,-10,69,76,-10,10,STEEL,'Zellensockel','medium','metal')
    plate(m,[(-49,13),(-24,13),(-23,22),(-41,23),(-44,48),(-53,48)],
          -8,8,STEEL,'Schaft','medium','metal')
    # Hollow guide above the hand, seated in receiver front. Its small front
    # collar remains open; it is an energy guide rather than a firearm barrel.
    tube(m,19,77,-6,0,5,3.3,STEEL,'Lauf','medium',sides=8)
    tube(m,71,84,-6,0,8,3.8,DARK,'Mündung','medium',sides=8)
    rail(m,-21,22,-38)
    # Short mount stem physically bridges the top of the central riser.
    block(m,-20,21,-34,-27,-5,5,STEEL,'Schienensockel','medium','metal',cut=1)
    optic(m,-18,-38)
    side_panel(m,-17,15,-18,6,13)
    status(m,-9,9,13,11)
    return m
