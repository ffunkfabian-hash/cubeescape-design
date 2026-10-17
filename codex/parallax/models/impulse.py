"""Exposed coaxial pulsed coils anchored to a continuous lower spine."""
from .common import *

META=meta('impulse','Relay I-4','Impulsgewehr',
          'FREIE PULSSPULEN · DURCHGEHENDER TRÄGER · HOHE ENERGIEZELLE',
          'Vier hohle Pulsspulen sitzen auf dem Lauf und berühren den unteren '
          'Träger; keine schwebenden Ringe. Die orangefarbenen schmalen '
          'Spulenbänder markieren ausschließlich aktive Funktionsflächen.')

def build():
    m=[]
    plate(m,[(-67,-14),(-51,-24),(28,-24),(43,-11),(41,18),
             (15,24),(-56,24),(-68,12)],-15,15,label='Gehäuse')
    stock(m,-112,-65,-2,zwidth=12)
    control_group(m,-39,23,magazine_x=20,magazine_length=43,magazine_tilt=-4)
    tube(m,34,149,-1,0,8,4.2,label='Lauf')
    block(m,30,139,16,25,-8,8,DARK,'Spulenträger','medium','metal')
    for x in (48,73,98,123):
        tube(m,x,x+10,-1,0,18,7.3,STEEL,'Pulsspule')
        tube(m,x+3,x+6,-1,0,18.6,17.8,ORANGE,'Spulenanzeige','accent','light',emit=True)
    tube(m,141,157,-1,0,11,5,CREAM,'Mündung')
    rail(m,-54,20,-29)
    optic(m,-34,-29)
    side_panel(m,-50,-7,-14,6,16)
    status(m,4,-14,16,13)
    return m
