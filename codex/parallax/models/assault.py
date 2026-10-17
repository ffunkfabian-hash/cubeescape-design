"""Balanced conventional layout with a faceted skeleton stock."""
from .common import *

META=meta('assault','Vanguard A-12','Sturmgewehr',
          'LANGER HANDSCHUTZ · SKELETTSCHAFT · GENEIGTES MAGAZIN',
          'Lauf im vorderen Gehäusebund gelagert; Magazin steckt sichtbar im '
          'verstärkten Schacht vor dem Abzug. Schulterpolster, Schaftsteg und '
          'Gehäuse sind bewusst ineinander verzapft.')

def build():
    m=[]
    plate(m,[(-63,-10),(-53,-19),(54,-19),(70,-9),(67,13),
             (47,19),(-56,19),(-65,10)],-13,13,label='Gehäuse')
    stock(m,-123,-61,-5)
    control_group(m,-37,18,magazine_x=21,magazine_length=48,magazine_tilt=11)
    tube(m,62,148,-2,0,6,3.6,label='Lauf')
    plate(m,[(49,-14),(114,-12),(121,-5),(114,15),(49,15)],
          -12,12,CREAM,'Handschutz')
    # Forward barrel remains exposed beyond the handguard.
    tube(m,143,163,-2,0,8,4.1,DARK,'Mündung','medium')
    block(m,53,111,11,20,-8,8,DARK,'Griffauflage','dark','rubber')
    rail(m,-49,57,-24)
    optic(m,-27,-24)
    side_panel(m,-46,-4,-10,6,14)
    for x in (62,78,94):
        block(m,x,x+9,-7,-1,12,14,DARK,'Kühlfenster','dark','metal',cut=1)
    status(m,5,-12,14,12)
    return m
