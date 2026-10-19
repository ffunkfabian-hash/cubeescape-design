"""KH23 „Wärmefalle“: magazinloser Werkstatt-Blaster mit geklemmtem Rippenblock."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

PL, CU, DK, HL = '#555D6B', '#D0B742', '#24262D', '#DFE1DA'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x, y, 3, 10), DK) for x, y in points]

    b.C(90, 264, 274, 11, DK, n=12, L='Rohrschaft')
    b.P(rect(76, 259, 20, 108), DK, -20, 20, r=4, L='Schaftkappe',
        dec=[D(rect(81, 273+17*i, 10, 6), PL) for i in range(5)])
    b.C(208, 234, 274, 18, CU, n=12, L='Schaftklemmring')
    b.P(rect(115, 235, 94, 18), PL, -20, 20, r=3, L='Wangenauflage',
        dec=[D(rect(128, 240, 68, 5), HL)])
    for x in (124, 192):
        b.P(rect(x, 251, 12, 28), CU, -12, 12, r=2, L='Wangenhalter', dec=bolts([(x+6, 266)]))
    b.C(96, 260, 327, 5, HL, n=10, L='Schaftunterzug')
    b.P(rect(246, 278, 16, 54), CU, -12, 12, r=3, L='Schaftstütze',
        dec=bolts([(254, 316)]))
    # Hoches, kurzes Obermodul; kein Magazin oder Zellenhalter unter dem unteren Rahmen.
    b.P([(260, 228), (502, 228), (530, 246), (530, 289), (260, 289)], PL, -25, 25,
        r=4, L='Gehäuse', dec=[D(rect(282, 237, 110, 5), HL)])
    b.P([(260, 293), (530, 293), (530, 315), (505, 330), (260, 330)], DK, -25, 25,
        r=4, L='Untergehäuse')
    for x in (269, 402):
        for z0, z1 in ((25, 31), (-31, -25)):
            screws = bolts([(x+8, 278), (x+8, 311)])
            b.P(rect(x, 270, 16, 49), CU, z0, z1, r=3, L='Gehäuseklemmplatte',
                dec=screws if z0 > 0 else (),
                xdec=[('z-', z0, *d) for d in screws] if z0 < 0 else ())
    rail(b, 294, 480, 228, DK, HL, w=11)
    b.P(rect(294, 251, 94, 28), DK, 25, 30, r=4, L='Plasmakammer',
        dec=[D(roundpoly(rect(302, 257, 78, 16), 3), CU, True)] + bolts([(298, 264), (384, 264)]))
    b.P(rect(294, 297, 94, 13), PL, 25, 30, r=2, L='Hitzeanzeige',
        dec=[D(rect(300+13*i, 300, 8, 7), HL if i < 3 else CU, True) for i in range(6)])
    # Zwei getrennte, am oberen Rand angeschlagene Klappen, mit Lamellen auf ihrer jeweiligen Außenseite.
    vents = [D(roundpoly(rect(442+12*i, 259, 6, 42), 2), CU, True) for i in range(6)]
    for z0, z1 in ((25, 34), (-34, -25)):
        b.P([(431, 248), (520, 248), (520, 307), (431, 313)], PL, z0, z1, r=3,
            L='Entlüftungsklappe', dec=vents if z0 > 0 else (),
            xdec=[('z-', z0, *d) for d in vents] if z0 < 0 else ())
        b.C(432, 520, 247, 4, CU, n=10, cz=31 if z0 > 0 else -31, L='Klappenscharnier')
    # Deutlich gestuftes Rippenpaket ist zwischen zwei Schellen verspannt.
    b.C(528, 696, 284, 21, DK, n=12, L='Hitzespeicher')
    for i in range(9):
        b.C(539+16*i, 546+16*i, 284, 34 if i % 2 else 39, PL if i % 2 else HL,
            n=8, L='Kühlrippen')
    for x in (529, 683):
        b.C(x, x+13, 284, 31, CU, n=8, L='Speicherklemmring')
    # Beidseitige äußere Spannrohre sitzen neben dem heißen Block und enden in sichtbaren Laschen.
    for z in (-43, 43):
        b.C(533, 695, 303, 4, HL, n=10, cz=z, L='Spannrohr')
        for x in (529, 683):
            b.P(rect(x, 280, 13, 30), CU, min(z, 0)-4, max(z, 0)+4, r=2, L='Speicherhalter',
                dec=bolts([(x+6, 300)]))
    b.C(694, 760, 284, 10, DK, n=12, L='Lauf')
    b.C(754, 784, 284, 20, CU, n=12, L='Fokusring',
        cap=[(284, 0, 11, DK, False), (284, 0, 5, CU, True)])
    # Kühle Griffzone vollständig hinter dem Rippenpaket; keine Magazinsilhouette.
    grip(b, 279, 330, DK, PL, h=94, w=50, lean=12)
    b.P(rect(344, 327, 16, 8), DK, -7, 7, r=2, L='Abzugslager')
    trigger_group(b, 344, 330, CU, DK, grip_x0=320, depth=34)
    b.P([(452, 329), (488, 329), (482, 394), (458, 394)], DK, -15, 15, r=5, L='Vordergriff',
        dec=[D(rect(460, 346+12*i, 20, 5), PL) for i in range(4)])
    b.C(489, 696, 340, 5, HL, n=10, L='Rohrrahmen')
    for x, top in ((492, 315), (682, 309)):
        b.P(rect(x, top, 14, 345-top), CU, -10, 10, r=2, L='Rahmenhalter',
            dec=bolts([(x+7, 333)]))
    return b.m


META = dict(num='23', name='Hitze-Blaster', nick='WÄRMEFALLE', col=CU,
    pill='TINTENGRAU · SIGNALGELB · DUNKEL', palette=[PL, CU, DK, HL], center=(430, 313, 0),
    desc='Ein kompakter Werkstatt-Blaster mit hohem, geklemmtem Kammerblock und freiem Raum unter dem Gehäuse. Der stufige Hitzespeicher ist zwischen gelben Schellen und zwei äußeren Spannrohren eingefasst; zwei einzeln angeschlagene Entlüftungsklappen und die segmentierte Anzeige übernehmen die Nachladefunktion.',
    form='Rohrschaft mit Klemmring und Unterzug · geklemmtes Ober- und Untergehäuse · Plasmakammer · Hitzeanzeige · zwei seitliche Entlüftungsklappen · neun Kühlrippen · beidseitige Spannrohre · Fokusring · kühle Griffzone',
    op=dict(
        reload_de='Kein Magazinwechsel: Nachladetaste öffnet beide seitlichen Entlüftungsklappen; Munition kommt direkt aus der Reserve.',
        action_de='Jeder Schuss heizt den Speicher; neun Rippen kühlen zwischen Salven. Bei voller Anzeige wird langes Entlüften erzwungen.',
        fire_de='Plasmabolzen in Salven; rechtzeitiges Entlüften im Mittelfeld der Hitzeanzeige verkürzt die Schusspause.',
        reload_en='No magazine change: reload opens both side vent flaps; ammunition comes directly from reserves.',
        action_en='Every shot heats the sink; nine fins cool it between bursts. A full gauge forces a long vent cycle.',
        fire_en='Bursts of plasma bolts; timely venting in the middle zone of the heat gauge shortens the firing pause.'))
