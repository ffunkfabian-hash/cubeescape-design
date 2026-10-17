"""K05: a fine needle barrel and visibly hollow triangular stock."""
from .common import *

P, M, D, A = '#DEDDEB', '#927EAE', '#343248', '#E14FBE'
META = meta('sniper', 'Orchid Needle', 'Scharfschützengewehr',
            'Nadellauf · asymmetrische Wange · Dreiecksschaft',
            ['Der lange dünne Lauf tritt klar aus der kurzen rautenförmigen Kammer hervor.',
             'Die Wange liegt links der Achse; zwei Streben halten das Dreieck des Schafts offen.',
             'Ein separat geklemmtes Zielfernrohr bleibt als vollständige Baugruppe abnehmbar.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Porzellan · Rauchlavendel · Pflaumengraphit · Orchidee')


def build():
    m = []
    plate(m,[(-68,-11),(-48,-28),(3,-23),(39,-10),(29,10),
             (-11,22),(-57,15)],-12,12,label='Gehäuse')
    plate(m,[(-54,-18),(-27,-23),(10,-15),(23,-7),(-25,-4)],
          12,15,role='medium',material='metal')
    tube(m,26,221,-7,0,4.8,2.8,label='Lauf')
    tube(m,215,233,-7,0,7.5,3.1,label='Mündung',role='dark')
    # Short vented launch cradle protects the chamber; the needle remains bare.
    rod(m,(23,-16),(65,-13),5,-7,7,role='primary')
    rod(m,(23,2),(65,0),5,-7,7,role='primary')
    tube(m,59,67,-7,0,9,5.2,role='primary')
    control_group(m,-49,top=17,grip_length=41,magazine_x=4,
                  magazine_length=29,magazine_tilt=-2,guard_width=28)
    # Open right triangle: shoulder pad joins both load-bearing spars.
    rod(m,(-140,-12),(-64,-10),7,-8,8,label='Schaft',role='primary')
    rod(m,(-132,37),(-64,-10),7,-8,8,role='primary')
    rod(m,(-140,-12),(-132,37),10,-11,11,role='dark',material='rubber')
    plate(m,[(-132,-25),(-92,-24),(-77,-13),(-128,-12)],
          4,19,label='Wangenauflage',role='medium',material='plastic')
    # Cheek spacer connects the asymmetric upper shelf to the central spar.
    block(m,-123,-111,-16,-8,0,12,role='dark',material='metal')
    rail(m,-50,24,y=-30,width=10)
    block(m,-47,-39,-26,-18,-5,5,role='dark',material='metal')
    block(m,14,22,-26,-14,-5,5,role='dark',material='metal')
    optic(m,-40,y=-30,long=True)
    block(m,-33,-12,12,17,12,15,role='accent',material='plastic')
    status(m,-20,-11,z=16,length=9)
    colors = dict(primary=P, medium=M, dark=D, accent=A)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = colors[p.role]
    return m
