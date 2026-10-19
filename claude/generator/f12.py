"""KF12 Handfeuerwaffe „Keilherz“: hoher Trommelrahmen, tiefer gekrümmter Griff, keilförmiger Laufmantel."""
import math

from eng import rect
from tlib import B, rail, trigger_group

SA, VI, DK, HE = '#F2B632', '#595C98', '#262239', '#F2E9C9'


def model():
    b = B()
    D = b.D
    # Der Griff beschreibt einen kräftigen Bogen nach hinten statt des geraden G-Griffs.
    b.P([(233,305),(283,306),(290,335),(274,369),(248,414),(214,430),
         (190,414),(199,387),(219,356)], VI, -22, 22, r=9, L='Griff',
        dec=[D([(239,328),(269,331),(254,369),(233,400),(214,409),(212,390)], DK)])
    b.P([(219,254),(243,234),(292,236),(308,254),(307,312),(281,329),(237,319),(220,291)],
        SA, -20, 20, r=7, L='Rahmen',
        dec=[D([(239,261),(278,253),(288,263),(285,286),(245,292)], HE)])
    # Freies Trommelfenster x=307..388, y=249..317, nur oben/unten verbunden.
    b.P([(286,235),(408,235),(421,243),(416,249),(290,249)],
        SA, -18, 18, r=4, L='Oberbrücke')
    b.P([(294,317),(405,317),(411,330),(285,332)], SA, -17, 17, r=5, L='Unterbrücke')
    b.P([(387,246),(411,245),(421,276),(411,325),(389,325)],
        VI, -19, 19, r=4, L='Rahmen')
    # Die Kammern liegen mit dem ersten Winkel -pi/2 exakt oben: Laufachse y=280-18=262,z=0.
    b.C(308, 385, 280, 30, VI, n=12, L='Trommel',
        cap=[(280+18*math.sin(k*math.pi/3-math.pi/2),
              18*math.cos(k*math.pi/3-math.pi/2), 6, DK, False) for k in range(6)])
    for z0, z1 in ((29.5,31),(-31,-29.5)):
        b.P([(318,273),(374,273),(374,286),(318,286)], SA, z0, z1, r=3, L='Trommelfläche')
    b.P([(257,293),(277,289),(282,296),(276,305),(258,306)],
        VI, 20, 28, r=3, L='Trommelriegel')
    b.P([(234,239),(245,218),(257,214),(270,236),(263,247)],
        VI, -7, 7, r=3, L='Hahn')
    # Keilmantel: breit am Rahmen, höher werdende Nase, große ungeteilte Safranfläche.
    b.P([(409,244),(532,233),(566,242),(577,258),(568,284),(528,310),(410,317)],
        SA, -19, 19, r=7, L='Laufmantel',
        dec=[D([(431,260),(530,249),(552,258),(534,278),(436,293)], VI),
             D([(437,266),(507,259),(510,267),(440,277)], HE)])
    rail(b, 302, 413, 236, DK, VI, w=10)
    # Lauf sitzt durchgehend auf der oberen Kammerachse; die Mündung bleibt als eigener Zylinder lesbar.
    b.C(384, 582, 262, 9, DK, n=12, L='Lauf',
        cap=[(262,0,7,HE,False),(262,0,5,DK,False)])
    # Sichtbar unterhalb des Keilmantels, hinten am Vorderrahmen und vorn am Lager gehalten.
    b.C(385, 512, 328, 4, DK, n=8, L='Ausstoßerstange')
    b.P([(505,303),(520,302),(520,337),(505,337)], VI, -7, 7, r=2, L='Stangenlager')
    # Der gesamte Bügel beginnt unterhalb des Trommelfensters und bleibt bis y=392 offen.
    trigger_group(b, 310, 332, HE, DK, grip_x0=260, depth=40)
    return b.m


META = dict(
    num='12', name='Handfeuerwaffe', nick='KEILHERZ', col=SA,
    pill='SAFRAN · STAHLVIOLETT · NACHTVIOLETT', palette=[SA,VI,DK,HE], center=(384,322,0),
    desc='Ein safranfarbener Keilmantel wächst aus dem hohen offenen Trommelrahmen; der stahlviolette Griff schwingt tief nach hinten. '
         'Die obere der sechs Kammern liegt exakt auf der Laufachse, während Hahn, Oberbrücke und die Ausstoßerstange als eigene Funktionsteile lesbar bleiben.',
    form='Keilförmiger Laufmantel · offener Rahmen mit Ober- und Unterbrücke · Trommel mit sechs Kammern · '
         'Trommelriegel links · freier Hahn · integrierte Visierschiene · Ausstoßerstange · gekrümmter Griff · freier Abzugbügel',
    op=dict(
        reload_de='Trommelriegel links drücken, Trommel nach links ausschwenken, Hülsen ausstoßen, sechs Patronen einsetzen und Trommel schließen.',
        action_de='Double Action: Jeder Abzug spannt den Hahn und dreht die Trommel um eine Kammer auf die obere Laufachse.',
        fire_de='Ein schwerer Einzelschuss je Abzug; der breite Griffbogen stützt die Hand gegen den Rückstoß.',
        reload_en='Press the left latch, swing the cylinder left, eject the cases, load six rounds and close the cylinder.',
        action_en='Double action: each trigger pull cocks the hammer and aligns the next chamber with the upper bore axis.',
        fire_en='One heavy shot per trigger pull; the broad curved grip supports the hand against recoil.'))
