"""KF19 Schwere Armbrust „Flügelwiege“: ergonomischer Rahmenschaft und breite, zurückgeschwungene Querwurfarme.

Der Daumendurchgriff ist ein echtes Fenster aus vier getrennten Rahmenstegen. Die Bolzenrinne bleibt oben offen:
ein Boden und zwei seitliche Wangen, darüber liegen Bolzen und Sehne. Nur der Spannhebel sitzt einseitig links.
"""
import math

from eng import rect, circ, roundpoly
from tlib import B, grip, rail, trigger_group

PE, KV, DK, HE = '#F6B58F', '#6352D8', '#241B38', '#E9DAD8'
BY = 244


def strip(b, p0, p1, width, col, y0, y1, label):
    """Schmales Sehnenband in der horizontalen Ebene; Endpunkte sind die mechanischen Anschlüsse."""
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dz)
    nx, nz = -dz / length * width / 2, dx / length * width / 2
    b.Y([(p0[0] + nx, p0[1] + nz), (p1[0] + nx, p1[1] + nz),
         (p1[0] - nx, p1[1] - nz), (p0[0] - nx, p0[1] - nz)],
        col, y0, y1, L=label)


def model():
    b = B()
    D = b.D
    # Hoher, geschwungener Rahmen: Öffnung x=150..250, y=310..380 bleibt durch die ganze Breite frei.
    b.P([(91,270),(128,267),(146,304),(141,375),(158,392),(134,414),(106,392),(94,330)],
        KV, -19, 19, r=8, L='Schaft')
    b.P([(119,272),(222,252),(289,259),(302,295),(144,307)],
        PE, -18, 18, r=8, L='Schaft',
        dec=[D([(150,280),(218,267),(248,270),(233,286),(153,296)], HE)])
    b.P([(137,384),(259,384),(306,376),(318,397),(265,416),(137,414)],
        KV, -16, 16, r=7, L='Schaft')
    b.P([(79,273),(96,270),(108,391),(97,405),(84,394)],
        DK, -21, 21, r=5, L='Schaftkappe')
    b.P([(132,266),(217,249),(267,253),(268,267),(217,264),(136,281)],
        HE, -15, 15, r=5, L='Wangenauflage')
    # Eine ruhige, große Gehäusefläche; die Unterkante steigt vor dem Abzug an und wird erst weiter vorn tiefer.
    b.P([(267,244),(343,244),(368,254),(608,254),(644,272),(627,311),
         (495,323),(434,297),(267,297)], PE, -22, 22, r=7, L='Gehäuse',
        dec=[D([(451,274),(584,274),(605,287),(494,303)], KV),
             D([(280,270),(321,270),(332,282),(280,282)], DK)])
    # Die Schiene sitzt tief im hinteren Gehäuse; kein eigenes Visier, kein Tragebügel.
    rail(b, 235, 333, 250, DK, KV, w=10)
    # Einsetzen der hinteren Schienenhälfte in den Schaft statt freischwebender Überhang.
    b.P([(221,254),(270,248),(276,274),(225,279)], PE, -17, 17, r=4, L='Schaft')
    grip(b, 274, 296, DK, KV, h=107, w=58, lean=22, z=18)
    trigger_group(b, 346, 297, HE, DK, grip_x0=310, depth=42)
    # Kurzer geneigter Vordergriff unter der breiten Gehäusefront, deutlich vor dem Abzugbügel.
    b.P([(495,316),(544,316),(540,357),(524,379),(501,375),(491,355)],
        KV, -15, 15, r=7, L='Vordergriff',
        dec=[D([(506,335),(530,335),(526,357),(510,364)], DK)])
    # Der Rinnenboden berührt den Bolzen unten (y=248), die Wangen lassen z=-4.5..4.5 offen.
    b.P(rect(373,248,287,7), DK, -4.5, 4.5, L='Führungsrinne')
    for sign in (-1, 1):
        z0, z1 = sorted((4.5 * sign, 17 * sign))
        b.P([(373,246),(647,246),(660,251),(660,268),(373,268)],
            KV, z0, z1, r=2, L='Führungsrinne')
    # Das offene Schloss fasst die Nocke hinten, ohne als Block auf dem Bolzen zu liegen.
    b.P(rect(348,238,25,18), DK, -13, 13, r=3, L='Schloss')
    b.C(373,380,BY,4,DK,n=8,L='Bolzennocke')
    b.C(379,691,BY,4,HE,n=8,L='Bolzen')
    b.F(691,727,BY,7.5,0.8,KV,n=8)  # unbenannt wie G19: Exporter verlängert den Mündungsanker bis zur Spitze
    # Leitfeder vollständig über der Bahn; keine Feder in den Rinnenboden stecken.
    b.P([(384,240),(397,229),(420,229),(413,240)], KV, -0.9, 0.9, L='Bolzenfeder')
    # Querblock unter der Geschossbahn; Wurfarmwurzeln greifen beidseitig in seine breite Aufnahme.
    b.P([(612,254),(661,254),(672,271),(655,301),(612,307)],
        DK, -32, 32, r=5, L='Bogenblock')
    for sign in (-1, 1):
        # Breite zusammenhängende Schwinge mit zwei großen Flächen statt der schmalen G-Recurve-Stäbe.
        limb = [(625,25),(671,25),(685,77),(667,132),(613,178),
                (580,193),(567,178),(606,146),(633,104),(632,66)]
        b.Y([(x,z*sign) for x,z in limb], PE, 249, 263, r=3, L='Wurfarm',
            dec=[D([(638,45*sign),(659,45*sign),(668,78*sign),
                    (651,121*sign),(635,132*sign),(647,88*sign)], KV)])
        # Eigene Spitzenkappe, die auf dem Ende der Schwinge sitzt; die Sehne endet innerhalb dieser Kappe.
        b.Y([(576,174*sign),(592,183*sign),(581,196*sign),(565,186*sign)],
            KV, 240, 263, r=2, L='Sehnenlager')
        strip(b, (577,185*sign), (374,1.5*sign), 2.6, DK, BY-1.3, BY+1.3, 'Sehne')
    # Linker Spannhebel: Achse am Vorderblock, Hebel und Griff liegen vollständig außen am Gehäuse.
    b.P(circ(620,284,10,12), KV, 22, 31, L='Spannhebelachse')
    b.P([(388,284),(616,279),(624,285),(616,292),(388,300)],
        KV, 28, 35, r=3, L='Spannhebel')
    b.P([(378,282),(405,282),(405,302),(378,304)],
        DK, 28, 39, r=4, L='Spannhebel')   # Griff schwenkt mit dem Spannhebel
    return b.m


META = dict(
    num='19', name='Schwere Armbrust', nick='FLÜGELWIEGE', col=KV,
    pill='PFIRSICH · KOBALTVIOLETT · TINTE', palette=[PE,KV,DK,HE], center=(403,322,0),
    desc='Ein tiefer Rahmenschaft umschließt den großen Daumendurchgriff; der geneigte Griff schließt seine Vorderkante. '
         'Breite pfirsichfarbene Wurfarme schwingen quer zurück, die Sehne läuft zum Schloss und der helle Bolzen liegt in einer offenen Führungsrinne. '
         'Kobaltviolett fasst den Rahmen und markiert den Spannhebel links.',
    form='Großer offener Rahmenschaft mit Wangenauflage · geneigter Griff mit freiem Abzugbügel · tiefe Visierschiene · '
         'kurzer Vordergriff · offene Führungsrinne mit Bolzen · Schloss · breite quer geschwungene Wurfarme · Sehne · Spannhebel links',
    op=dict(
        reload_de='Spannhebel links um die vordere Achse nach vorn-unten schwenken, Sehne ins Schloss ziehen und einen Bolzen in die offene Rinne legen.',
        action_de='Ein Bolzen je Spannung. Der verschossene Bolzen bleibt am Trefferort liegen und kann zum Auffüllen des Vorrats wieder aufgenommen werden.',
        fire_de='Einzelschuss mit hoher Durchschlagskraft; das Schloss gibt die Sehne frei und der Bolzen verlässt die Führungsrinne nach vorn.',
        reload_en='Swing the left cocking lever forward and down on its front pivot, draw the string into the latch and place a bolt in the open groove.',
        action_en='One bolt per draw. The fired bolt stays at the impact point and can be recovered to refill the reserve.',
        fire_en='Single high-impact shot; the latch releases the string and the bolt leaves the flight groove to the front.'))
