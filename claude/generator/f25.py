"""KF25 Streuschuss-Handfeuerwaffe „Fächerfaust“: breiter kurzer Kippkopf über schlankem gebogenem Griff.

Fünf Schrotkammern, verdeckter Hahn und vorderes Kippgelenk wie G25.
Das hochgezogene Joch und die seitlich gepfeilte Streumündung schaffen die eigene Silhouette.
"""
import math

from eng import rect, roundpoly, circ
from tlib import B, grip, rail, trigger_group

RO, VI, DK, HE = '#EA9D9C', '#453D83', '#2B223B', '#F1E3CF'
AXC = 279
BX = AXC - 18


def model():
    b = B()
    D = b.D
    grip(b,218,313,VI,DK,h=119,w=60,lean=28,z=20)
    # Geschwungener Griffsporn und unterer fester Rahmen hinter dem großen Trommelfenster.
    b.P([(204,265),(229,248),(279,254),(287,273),(282,319),(255,336),(220,323)],
        RO,-19,19,r=8,L='Rahmen',
        dec=[D([(214,277),(245,263),(262,273),(254,306),(227,311)],HE)])
    b.P([(260,315),(373,315),(407,302),(419,315),(401,337),(260,335)],
        RO,-16,16,r=6,L='Rahmen')
    b.P([(204,260),(212,236),(260,236),(278,252),(267,265),(227,259)],
        VI,-12,12,r=4,L='Hahnschutz')
    # Die Kurzschiene bleibt am festen Hahnschutz, vollständig hinter Riegel und Kippkopf.
    rail(b,214,258,236,DK,VI,w=10)
    b.P(circ(403,319,11,12),VI,-22,22,L='Scharnier')
    # Ein hochgezogenes Joch mit langer Oberbrücke; das Fenster unter der Brücke ist wirklich frei.
    b.P([(282,226),(381,226),(419,242),(422,311),(398,314),
         (397,258),(376,244),(282,244)],
        RO,-17,17,r=6,L='Kipprahmen',
        dec=[D([(402,258),(414,259),(414,299),(403,305)],VI)])
    b.P([(264,233),(285,220),(302,231),(293,246),(274,250)],
        HE,-7,7,r=4,L='Kippriegel')
    # Oberste Kammer ist genau auf der Laufachse, nicht auf der Trommelmitte.
    caps=[]
    for k in range(5):
        y,z=AXC-18*math.cos(2*k*math.pi/5),18*math.sin(2*k*math.pi/5)
        caps.extend([(y,z,8.5,RO,False),(y,z,4.5,DK,False)])
    b.C(285,381,AXC,32,VI,n=10,L='Trommel',cap=caps)
    b.C(278,398,AXC,5,DK,n=10,L='Trommel')
    b.P([(296,274),(368,274),(375,279),(368,284),(296,284)],
        DK,-32.5,32.5,r=3,L='Kammerrille')
    b.C(419,474,BX,13,DK,n=10,L='Lauf')
    b.P([(420,240),(457,240),(478,248),(474,254),(420,250)],
        VI,-8,8,r=3,L='Lauf')
    # Breite gepfeilte Mündung, kurzer Hals; keine lange G25-Fächerplatte.
    b.Y([(469,-14),(486,-36),(520,-42),(537,-31),(537,31),
         (520,42),(486,36),(469,14)],RO,BX-16,BX+16,r=5,L='Streumündung',
        dec=[D([(486,-29),(519,-34),(525,-23),(489,-18)],VI),
             D([(486,29),(519,34),(525,23),(489,18)],VI)])
    b.m.parts[-1]['dec'].append(('x+',537,roundpoly(rect(BX-8,-25,16,50),4),DK,False))
    for z in (-15,0,15):
        b.m.parts[-1]['dec'].append(('x+',537,circ(BX,z,2.5,8),HE,False))
    # Unter der Trommel: freier Bügel vor dem Griff, der nicht in die Trommel greift.
    trigger_group(b,300,335,HE,DK,grip_x0=266,depth=38)
    return b.m


META = dict(
    num='25', name='Streuschuss-Handfeuerwaffe', nick='FÄCHERFAUST', col=RO,
    pill='ALTROSA · IRIS · TINTE', palette=[RO,VI,DK,HE], center=(363,329,0),
    desc='Ein hochgezogenes altrosafarbenes Joch fasst die dicke fünfkammerige Trommel über dem geschwungenen Irisgriff. '
         'Der kurze Lauf endet in einer breiten gepfeilten Streumündung; die gesamte obere Baugruppe kippt am großen vorderen Gelenk nach unten.',
    form='Gebogener Griff mit Sporn · Hahnschutz mit fester Kurzschiene · hoher Kipprahmen mit echtem Fenster · fünfkammerige Trommel · '
         'Kippriegel hinten · großes vorderes Scharnier · kurzer Lauf · gepfeilte breite Streumündung',
    op=dict(
        reload_de='Kippriegel lösen, Kopf mit Trommel und Lauf am vorderen Gelenk abkippen; Auswerfer hebt fünf Hülsen. Schrotpatronen einsetzen, zuklappen.',
        action_de='Double Action: der verdeckte Hahn spannt bei jedem Abzug und dreht die Trommel um eine der fünf Kammern weiter.',
        fire_de='Langsamer Einzelschuss aus Schrotkugeln; die breite Streumündung fächert die Ladung flach auf kurze Entfernung.',
        reload_en='Release the latch, tip the head with cylinder and barrel down at the front hinge; the extractor lifts five shells. Load shot shells and close.',
        action_en='Double action: each trigger pull cocks the shrouded hammer and indexes the cylinder by one of its five chambers.',
        fire_en='Slow single shots of pellets; the wide spread muzzle fans the load flat at close range.'))
