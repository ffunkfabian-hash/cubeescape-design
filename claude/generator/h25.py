"""KH25 „Fächerblock“: gedrungener Werkstatt-Kipprahmenrevolver mit flacher Fächermündung."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly
import math

PL, CU, DK, HL = '#797285', '#B3C75D', '#28262D', '#E4E0D8'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x, y, 3, 10), DK) for x, y in points]

    # Griffrahmen und kurze, feste Rückwand: der Revolver braucht keinen Gewehrschaft.
    grip(b, 236, 340, DK, PL, h=108, w=54, lean=22, z=19)
    b.P([(224, 252), (262, 244), (301, 254), (301, 316), (287, 326), (238, 326), (224, 311)],
        PL, -24, 24, r=4, L='Gehäuse', dec=[D(roundpoly(rect(239, 270, 38, 16), 3), HL)])
    b.P([(237, 330), (439, 330), (450, 342), (436, 351), (237, 351)], DK, -23, 23,
        r=4, L='Rahmen')
    # Separate feste Unterkassette, mit beidseitigen Platten über der sichtbaren Fuge an der Rückwand.
    b.P(rect(235, 326, 65, 18), PL, -24, 24, r=3, L='Untergehäuse')
    for x in (241, 278):
        for z0, z1 in ((24, 30), (-30, -24)):
            screws = bolts([(x+7, 315), (x+7, 337)])
            b.P(rect(x, 307, 14, 38), CU, z0, z1, r=2, L='Gehäuseklemmplatte',
                dec=screws if z0 > 0 else (),
                xdec=[('z-', z0, *d) for d in screws] if z0 < 0 else ())
    # Verkleideter Hahn, mechanischer Kippriegel; keine frei stehende Visierung.
    b.P([(228, 247), (242, 230), (275, 230), (295, 247), (277, 257), (242, 257)],
        DK, -14, 14, r=3, L='Hahnschutz', dec=[D(rect(244, 237, 24, 5), PL)])
    b.P([(277, 241), (291, 224), (309, 231), (304, 246), (288, 251)],
        CU, -8, 8, r=2, L='Kippriegel')
    # Oberbrücke und vorderes Joch sind ein durchgehendes Bauteil, das am vorderen Gelenk kippt.
    b.P([(295, 228), (438, 228), (452, 242), (452, 333), (426, 333), (426, 247), (295, 247)],
        PL, -20, 20, r=3, L='Kipprahmen',
        dec=[D(rect(433, 255, 11, 54), DK)] + bolts([(435, 241), (438, 316)]))
    rail(b, 314, 418, 228, DK, HL, w=11)
    b.P(circ(438, 336, 11, 12), CU, -29, 29, L='Scharnier',
        dec=[D(circ(438, 336, 4, 10), DK)])
    # Fünf Schrotkammern; dicke, kurze Trommel und geklemmter Achsstift im offenen Joch.
    chambers = [(286-20*math.cos(2*k*math.pi/5), 20*math.sin(2*k*math.pi/5)) for k in range(5)]
    b.C(310, 405, 286, 34, PL, n=10, L='Trommel',
        cap=[(y, z, 9, CU, False) for y, z in chambers] +
            [(y, z, 5, DK, False) for y, z in chambers])
    b.C(299, 432, 286, 5, HL, n=10, L='Achsstift')
    b.C(408, 426, 286, 11, CU, n=10, L='Achsklemmring')
    b.P(rect(322, 279, 68, 14), DK, -35, 35, r=3, L='Kammerrillen',
        dec=[D(rect(330, 283, 50, 5), CU)])
    # Zwei seitliche Rohrstreben stützen das feste Untergestell und lassen den Abzugsraum frei.
    for z in (-19, 19):
        b.C(295, 436, 340, 4, HL, n=10, cz=z, L='Rohrrahmen')
        b.P(rect(422, 328, 15, 18), CU, z-6, z+6, r=2, L='Rohrrahmenhalter',
            dec=bolts([(429, 336)]))
    b.C(446, 522, 266, 16, DK, n=12, L='Lauf')
    b.P(rect(450, 243, 66, 10), CU, -10, 10, r=2, L='Laufschiene',
        dec=[D(rect(458+14*i, 246, 6, 4), DK) for i in range(4)])
    # Grundriss fächert deutlich seitlich auf, die Höhe bleibt flach. Auslass ist ein einzelner Querschlitz.
    b.Y([(516, -17), (558, -39), (580, -39), (580, 39), (558, 39), (516, 17)],
        PL, 251, 281, r=3, L='Streumündung',
        dec=[D([(527, -2+z*0.4), (569, -2+z), (569, 2+z), (527, 2+z*0.4)], CU)
             for z in (-23, 0, 23)])
    b.m.parts[-1]['dec'].append(('x+', 580, roundpoly(rect(260, -30, 12, 60), 4), DK, False))
    trigger_group(b, 309, 350, CU, DK, grip_x0=279, depth=34)
    return b.m


META = dict(num='25', name='Streuschuss-Handfeuerwaffe', nick='FÄCHERBLOCK', col=CU,
    pill='LAVENDELGRAU · LIMETTE · DUNKEL', palette=[PL, CU, DK, HL], center=(402, 331, 0),
    desc='Ein gedrungener Werkstatt-Revolver mit dicker Fünfkammer-Trommel unter einer verschraubten Oberbrücke. Der kurze Lauf endet in einem breiten, flachen Fächerblock; der feste Griffrahmen trägt seitliche Rohrstreben, während Lauf und Trommel am vorderen Scharnier gemeinsam nach unten kippen.',
    form='Geklemmter Griffrahmen · verkleideter Hahn · Kipprahmen mit Oberbrücke und Joch · Kippriegel · dicke Trommel mit fünf Schrotkammern · Achsstift mit Klemmring · vorderes Scharnier · kurzer Lauf mit Laufschiene · flache Fächermündung',
    op=dict(
        reload_de='Kippriegel drücken, Lauf und Trommel am vorderen Scharnier abkippen; Sternauswerfer hebt fünf Hülsen. Schrotpatronen einsetzen, schließen.',
        action_de='Double Action: Der verdeckte Hahn spannt mit dem Abzug; die Trommel dreht jeweils eine der fünf Schrotkammern weiter.',
        fire_de='Kurzer Streuschuss durch den flachen Querschlitz der Fächermündung; langsame Feuerrate und hohe Wirkung auf kurze Distanz.',
        reload_en='Press the latch, tip barrel and cylinder down at the front hinge; the star extractor lifts five cases. Insert shot shells and close.',
        action_en='Double action: the shrouded hammer cocks with the trigger; the cylinder indexes one of its five shot chambers.',
        fire_en='A short pellet spread through the flat cross-slot of the fan muzzle; a slow rate of fire and high impact at close range.'))
