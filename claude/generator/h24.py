"""KH24 „Hubrohr“: Werkstatt-Mikroraketenwerfer mit tiefem Schaft und offenem Rohrrahmen."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

PL, CU, DK, HL = '#765B5C', '#B89B61', '#29262A', '#E4DED1'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x, y, 3, 10), DK) for x, y in points]

    # Der Schaft liegt tief unter der Rohrachse; eine offene Stütze hebt die Wangenauflage an.
    b.C(80, 252, 316, 11, DK, n=12, L='Rohrschaft')
    b.C(80, 242, 285, 5, HL, n=10, L='Schaftoberzug')
    b.P(rect(64, 267, 20, 112), DK, -20, 20, r=4, L='Schaftkappe',
        dec=[D(rect(69, 282+18*i, 10, 6), PL) for i in range(5)])
    b.C(204, 230, 316, 18, CU, n=12, L='Schaftklemmring')
    b.P(rect(98, 257, 102, 18), PL, -20, 20, r=3, L='Wangenauflage',
        dec=[D(rect(109, 263, 80, 5), HL)])
    for x in (110, 182):
        b.P(rect(x, 273, 12, 19), CU, -12, 12, r=2, L='Wangenhalter', dec=bolts([(x+6, 283)]))
    b.P(rect(231, 276, 21, 54), PL, -18, 18, r=3, L='Schaftaufnahme',
        dec=bolts([(241, 309)]))
    # Ladekammer und unterer Abzugsrahmen werden über die horizontale Fuge geklemmt.
    b.P([(246, 246), (432, 246), (454, 257), (454, 296), (246, 296)], PL, -26, 26,
        r=4, L='Gehäuse', dec=[D(rect(260, 254, 63, 5), HL)])
    b.P([(246, 300), (454, 300), (454, 329), (431, 341), (246, 341)], DK, -26, 26,
        r=4, L='Untergehäuse')
    for x in (253, 432):
        for z0, z1 in ((26, 32), (-32, -26)):
            screws = bolts([(x+8, 284), (x+8, 317)])
            b.P(rect(x, 276, 16, 49), CU, z0, z1, r=3, L='Gehäuseklemmplatte',
                dec=screws if z0 > 0 else (),
                xdec=[('z-', z0, *d) for d in screws] if z0 < 0 else ())
    rail(b, 270, 330, 246, DK, HL, w=11)
    b.P([(345, 233), (426, 233), (441, 245), (441, 250), (345, 250)], CU, -19, 19,
        r=3, L='Ladeklappe', dec=[D(rect(360+17*i, 239, 9, 5), DK) for i in range(4)] +
        bolts([(351, 242), (432, 242)]))
    b.P(circ(345, 246, 6, 12), DK, -23, 23, L='Ladeklappenscharnier')
    # Abgesetzter Vorratskasten links, mit eigenem Halter und genau vier sichtbaren Ersatzraketen.
    b.P(rect(278, 267, 143, 61), CU, 26, 38, r=3, L='Vorratshalter',
        dec=bolts([(286, 275), (413, 320)]))
    b.P(rect(286, 274, 127, 51), PL, 38, 70, r=4, L='Raketenvorrat',
        dec=[D(roundpoly(rect(295, 281, 109, 37), 3), DK)] +
            [D(roundpoly(rect(302, 285+8*i, 72, 5), 2), HL) for i in range(4)] +
            [D([(374, 285+8*i), (394, 287.5+8*i), (374, 290+8*i)], CU) for i in range(4)])
    # Langes schlankes Rohr; drei wirkliche Leitringe statt bloßer farbiger Streifen.
    b.C(446, 768, 275, 18, PL, n=12, L='Abschussrohr')
    b.P(rect(451, 268, 31, 14), DK, -19, 19, r=2, L='Abgasblock',
        dec=[D(rect(455+7*i, 271, 3, 8), CU) for i in range(4)])
    for x in (490, 612, 736):
        b.C(x, x+12, 275, 24, CU, n=12, L='Leitring')
    b.F(766, 796, 275, 18, 27, CU, n=12, L='Mündung')
    b.C(796, 805, 275, 27, DK, n=12, L='Mündungsring',
        cap=[(275, 0, 17, DK, False), (275, 0, 7, CU, False)])
    # Offener Unterrahmen parallel zum Abschussrohr; große negative Fläche über dem Vordergriff.
    b.C(448, 716, 337, 6, HL, n=10, L='Rohrrahmen')
    for x, top in ((451, 294), (698, 289)):
        b.P(rect(x, top, 16, 343-top), CU, -12, 12, r=3, L='Rohrrahmenhalter',
            dec=bolts([(x+8, top+10), (x+8, 332)]))
    b.P([(633, 333), (673, 333), (666, 405), (639, 405)], DK, -15, 15, r=5, L='Vordergriff',
        dec=[D(rect(642, 352+12*i, 22, 5), PL) for i in range(4)])
    grip(b, 272, 341, DK, PL, h=94, w=50, lean=14)
    b.P(rect(336, 338, 16, 8), DK, -7, 7, r=2, L='Abzugslager')
    trigger_group(b, 336, 341, CU, DK, grip_x0=313, depth=34)
    return b.m


META = dict(num='24', name='Mikroraketen-Granatwerfer', nick='HUBROHR', col=CU,
    pill='ROTGRAU · MESSING · DUNKEL', palette=[PL, CU, DK, HL], center=(435, 322, 0),
    desc='Ein einschüssiger Werkstatt-Werfer mit tiefem Rohrschaft und langem, von drei messingfarbenen Leitringen gefasstem Abschussrohr. Der offene Unterrahmen trägt den Vordergriff; oben wird durch die angeschlagene Ladeklappe geladen, links hält ein eigener Kasten vier Ersatz-Mikroraketen bereit.',
    form='Tiefer Rohrschaft mit Klemmring · geklemmtes Ober- und Untergehäuse · Ladeklappe oben · Raketenvorrat links mit vier Ersatzraketen · schlankes Abschussrohr · drei Leitringe · offene Rohrrahmenstütze · Vordergriff · aufgeweitete Mündung',
    op=dict(
        reload_de='Obere Ladeklappe nach hinten öffnen, eine Rakete aus dem linken Vorratskasten ins Patronenlager legen, Klappe schließen.',
        action_de='Einschüssig: Nach jeder Rakete von oben neu laden; der Treibsatz zündet erst vor der aufgeweiteten Mündung.',
        fire_de='Spezialmunition: schnelle, gerade fliegende Mikrorakete mit Aufprallzünder und geringem Eigenschaden.',
        reload_en='Open the top loading hatch to the rear, take one missile from the left reserve box into the chamber, then close the hatch.',
        action_en='Single shot: reload from above after every missile; its motor ignites only beyond the flared muzzle.',
        fire_en='Special ammunition: a fast, straight-flying micro-missile with an impact fuse and low self-damage.'))
