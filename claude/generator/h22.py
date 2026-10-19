"""KH22 „Zugstange“: langgestreckte Werkstatt-Slugflinte mit offenem Unterrahmen."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly
import math

PL, CU, DK, HL = '#3F5265', '#B68A42', '#20262D', '#DFE1DB'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x, y, 3, 10), DK) for x, y in points]

    # Zwei echte Rohre mit freiem Zwischenraum, schmaler Schaftkappe und geklemmter Wangenauflage.
    b.C(80, 280, 278, 9, DK, n=12, L='Rohrschaft')
    b.C(80, 267, 314, 6, HL, n=10, L='Schaftstrebe')
    b.P(rect(64, 262, 20, 112), DK, -19, 19, r=4, L='Schaftkappe',
        dec=[D(rect(69, 278+18*i, 10, 6), PL) for i in range(5)])
    b.P(rect(101, 251, 112, 18), PL, -19, 19, r=3, L='Wangenauflage',
        dec=[D(rect(112, 257, 88, 5), HL)])
    for x in (112, 196):
        b.P(rect(x, 267, 12, 18), CU, -13, 13, r=2, L='Wangenhalter', dec=bolts([(x+6, 275)]))
    b.C(228, 252, 278, 16, CU, n=12, L='Schaftklemmring')
    b.P(rect(249, 267, 22, 54), PL, -18, 18, r=3, L='Schaftaufnahme')
    # Gehäusefuge bleibt als dunkler Spalt unter den zwei seitlichen Klemmplatten sichtbar.
    b.P([(264, 246), (520, 246), (548, 260), (548, 294), (264, 294)], PL, -25, 25,
        r=4, L='Gehäuse', dec=[D(roundpoly(rect(290, 258, 74, 8), 3), HL)])
    b.P([(264, 298), (548, 298), (548, 328), (526, 339), (264, 339)], DK, -25, 25,
        r=4, L='Untergehäuse')
    for x in (276, 518):
        for z0, z1 in ((25, 31), (-31, -25)):
            screws = bolts([(x+9, 283), (x+9, 311)])
            b.P(rect(x, 275, 18, 44), CU, z0, z1, r=3, L='Gehäuseklemmplatte',
                dec=screws if z0 > 0 else (),
                xdec=[('z-', z0, *d) for d in screws] if z0 < 0 else ())
    rail(b, 302, 500, 246, DK, HL, w=11)
    b.P(rect(374, 263, 92, 17), DK, 25, 29, r=3, L='Verschlussbahn')
    b.P(rect(388, 267, 48, 10), HL, 29, 34, r=2, L='Verschluss')
    b.P(rect(397, 269, 16, 8), CU, 34, 51, r=2, L='Ladehebel')
    # Schlankes Kastenmagazin sitzt deutlich vor dem freien Abzugsbügel.
    b.P(rect(461, 331, 65, 16), CU, -18, 18, r=3, L='Magazinhalter',
        dec=bolts([(469, 339), (517, 339)]))
    b.P([(468, 345), (520, 345), (528, 414), (473, 418)], PL, -17, 17, r=4, L='Magazin',
        dec=[D(roundpoly(rect(478, 354, 34, 47), 3), DK)] +
            [D(roundpoly(rect(482, 360+13*i, 26, 7), 2), CU) for i in range(3)])
    b.P([(469, 410), (529, 406), (531, 420), (470, 424)], CU, -19, 19, r=3, L='Magazinboden')
    # Kurzer Mantel, lange freie Laufstrecke und darüber eine getrennte, beidseitig abgestützte Zugstange.
    b.P([(546, 264), (651, 264), (673, 276), (673, 313), (546, 320)], PL, -18, 18,
        r=4, L='Laufmantel', dec=[D(roundpoly(rect(560+27*i, 278, 16, 22), 3), DK) for i in range(4)])
    b.C(665, 818, 292, 12, DK, n=12, L='Lauf')
    b.C(550, 738, 248, 5, HL, n=10, L='Zugstange')
    for x in (550, 724):
        b.P(rect(x, 242, 13, 47), CU, -10, 10, r=3, L='Zugstangenhalter',
            dec=bolts([(x+6, 251), (x+6, 280)]))
    b.C(716, 744, 292, 19, CU, n=10, L='Laufschelle')
    b.C(812, 860, 292, 20, CU, n=8, L='Mündungsbremse',
        cap=[(292, 0, 9, DK, False)] +
            [(292+10*math.sin(k*math.pi/3), 10*math.cos(k*math.pi/3), 1.5, HL, False) for k in range(6)])
    # Rohrunterzug trägt den Vordergriff; die sichtbaren Halter schließen den Rahmen an beiden Enden.
    b.C(544, 716, 340, 5, HL, n=10, L='Rohrrahmen')
    for x, top in ((547, 317), (699, 300)):
        b.P(rect(x, top, 14, 345-top), CU, -10, 10, r=2, L='Unterzughalter',
            dec=bolts([(x+7, 333)]))
    grip(b, 280, 339, DK, PL, h=96, w=50, lean=14)
    b.P(rect(345, 336, 16, 8), DK, -7, 7, r=2, L='Abzugslager')
    trigger_group(b, 345, 339, CU, DK, grip_x0=321, depth=35)
    b.P([(614, 337), (650, 337), (644, 403), (620, 403)], DK, -15, 15, r=5, L='Vordergriff',
        dec=[D(rect(622, 353+12*i, 20, 5), PL) for i in range(4)])
    return b.m


META = dict(num='22', name='Slug-Schrotflinte', nick='ZUGSTANGE', col=CU,
    pill='KOHLENBLAU · OCKER · DUNKEL', palette=[PL, CU, DK, HL], center=(462, 325, 0),
    desc='Die gestreckte Werkstatt-Slugflinte verbindet einen zweirohrigen Schaft mit einem niedrigen, geklemmten Gehäuse. Eine helle Zugstange über dem freien Lauf und ein offener Rohrunterzug unter dem Mantel bilden ihre lange Silhouette; vor dem Abzug sitzt das Magazin mit drei sichtbaren Slug-Köpfen.',
    form='Zweirohrschaft mit Klemmring · Ober- und Untergehäuse mit Klemmplatten · Verschluss und Ladehebel links · Slug-Kastenmagazin · Zugstange über dem Lauf · offener Rohrunterzug · gezogener Lauf mit Mündungsbremse · Vordergriff',
    op=dict(
        reload_de='Slug-Kastenmagazin vor dem Abzug wechseln und den linken Ladehebel zurückziehen.',
        action_de='Halbautomatik: Der Verschluss läuft im Obergehäuse; der Vordergriff bleibt fest am Rohrunterzug.',
        fire_de='Ein schweres Einzelgeschoss je Abzug; der gezogene Lauf und die Mündungsbremse dienen präzisen Treffern auf mittlere Distanz.',
        reload_en='Replace the slug box magazine ahead of the trigger, then pull the left charging handle.',
        action_en='Semi-automatic: the bolt travels in the upper receiver; the foregrip stays fixed to the lower tube frame.',
        fire_en='One heavy slug per trigger pull; the rifled barrel and muzzle brake support accurate hits at medium range.'))
