"""K04: a wide staggered twin bore with a floating-profile pump saddle."""
from .common import *

P, M, D, A = '#D69E32', '#E6D9BA', '#263443', '#F47585'
META = meta('shotgun', 'Saffron Duet', 'Schrotflinte',
            'Gestaffelte Doppelläufe · breite Pumpmanschette',
            ['Zwei seitlich versetzte Läufe enden gestaffelt und besitzen echte offene Bohrungen.',
             'Die breite Pumpmanschette läuft unter beiden Rohren auf einer Führung.',
             'Der offene Schaft und das nach unten entnehmbare Magazin trennen die Funktionen.'])
META.update(variant='K', variant_name='Flux Bloom', palette=[P,M,D,A],
            palette_name='Ocker · Sandporzellan · Tintenblau · Flamingo')


def build():
    m = []
    plate(m,[(-82,-14),(-59,-34),(-16,-31),(22,-20),(36,-9),
             (8,5),(-4,22),(-65,22),(-80,9)],-18,18,label='Gehäuse')
    plate(m,[(-66,-24),(-32,-27),(-3,-20),(12,-11),(-48,-8)],
          18,21,role='medium',material='metal')
    # Tube ends are separated across z and deliberately unequal along x.
    for z,end in ((-10,141),(10,153)):
        tube(m,5,end-8,-8,z,8.2,5.2,label='Lauf' if z<0 else 'Zweiter Lauf')
        tube(m,end-15,end,-8,z,10.4,5.7,
             label='Mündung' if z<0 else 'Zweite Mündung',role='dark')
    rod(m,(2,12),(111,12),5,-5,5,role='medium',material='metal')
    plate(m,[(39,9),(92,9),(108,18),(100,34),(49,34),(34,23)],
          -21,21,label='Pumpmanschette',role='dark',material='rubber')
    plate(m,[(49,12),(88,12),(98,19),(94,25),(53,25),(44,19)],
          21,23,role='accent',material='plastic')
    control_group(m,-67,top=21,grip_length=43,magazine_x=-12,
                  magazine_length=39,magazine_tilt=3,guard_width=30)
    rod(m,(-137,-7),(-78,-10),9,-11,11,label='Schaft',role='primary')
    rod(m,(-137,34),(-78,7),8,-9,9,role='primary')
    rod(m,(-137,-8),(-137,37),11,-14,14,role='dark',material='rubber')
    plate(m,[(-132,-20),(-101,-20),(-82,-11),(-126,-9)],-13,13,
          role='medium',material='plastic')
    rail(m,-55,-2,y=-36,width=12)
    block(m,-53,-45,-32,-23,-6,6,role='dark',material='metal')
    block(m,-12,-4,-32,-22,-6,6,role='dark',material='metal')
    optic(m,-44,y=-36)
    status(m,-47,5,z=18.5,length=10)
    colors = dict(primary=P, medium=M, dark=D, accent=A)
    for p in m:
        if p.label == 'Abzug':
            p.role = 'accent'
        p.color = colors[p.role]
    return m
