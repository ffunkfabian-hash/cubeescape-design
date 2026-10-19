"""KF15 WALZENWIEGE: offene Trommelwiege, tiefer Daumenrahmen und kurzer Hochlauf.

Sechs Kammern und der Lauf liegen wie bei G15 auf derselben oberen Kammerbahn.
Die Brücke lässt Luft über der drehenden Trommel; Abzug und Bügel liegen vollständig dahinter.
"""
import math

from eng import rect
from tlib import B, grip, rail, trigger_group

KB, AP, DK, HE = '#264AA5', '#F4AF67', '#182441', '#EDF0D2'
AX = 280


def model():
    b = B()
    D = b.D
    # Vier Stege bilden den offenen Schaft; x=117..207, y=286..373 bleibt wirklich leer.
    b.P([(77,248),(114,240),(236,246),(249,277),(110,284),(91,275)],
        AP, -17, 17, r=7, L='Schaft',
        dec=[D([(123,251),(206,253),(218,266),(126,270)], HE)])
    b.P([(78,253),(103,267),(115,376),(98,399),(80,378)], KB, -18, 18, r=7, L='Schaft')
    b.P([(99,378),(226,378),(250,390),(233,410),(104,405),(91,394)],
        KB, -17, 17, r=7, L='Schaft')
    b.P([(66,252),(80,249),(91,380),(81,399),(69,385)], DK, -20, 20, r=5, L='Schaftkappe')
    # Hohe hintere Schulter trägt die Oberbrücke; keine Wange über dem Abzugfenster.
    b.P([(223,246),(293,228),(326,198),(390,198),(390,302),(240,309),(222,288)],
        AP, -26, 26, r=7, L='Gehäuse',
        dec=[D([(246,257),(304,245),(324,262),(303,283),(246,288)], KB)])
    b.P([(330,263),(379,254),(379,292),(330,298)], KB, 26, 33, r=4, L='Ladeklappe')
    grip(b, 231, 306, DK, KB, h=101, w=58, lean=24, z=18)
    trigger_group(b, 305, 306, HE, DK, grip_x0=277, depth=39)
    # Die Trommel bleibt seitlich frei: nur zwei Laufringe und die mittige Achse umfassen sie.
    b.C(390,515,AX,58,HE,n=12,L='Granattrommel',
        cap=[(AX-36*math.cos(k*math.pi/3),36*math.sin(k*math.pi/3),13,DK,False)
             for k in range(6)])
    for x in (410, 487):
        b.C(x,x+8,AX,59,KB,n=12)
    b.C(372,541,AX,9,DK,n=8,L='Trommelachse')
    # Unterkante 216, Trommeloberkante 221: mechanisches Spiel statt Durchdringung.
    b.P([(365,198),(543,198),(543,216),(365,216)], KB,-18,18,r=5)
    rail(b, 378, 522, 198, DK, AP, w=10)
    b.P([(515,198),(542,198),(552,241),(544,305),(515,306)],
        KB,-25,25,r=5,L='Laufträger')
    b.C(544,697,AX-36,22,AP,n=12,L='Lauf')
    b.C(697,722,AX-36,28,KB,n=12,L='Mündung',cap=[(AX-36,0,18,DK,False)])
    # Schräger Stützgriff vor der Walze, am unteren Laufträger angeschlossen.
    b.P([(522,297),(558,286),(575,350),(560,388),(536,386),(531,347)],
        KB,-15,15,r=7,L='Vordergriff',
        dec=[D([(539,318),(552,314),(560,348),(551,368),(544,347)], DK)])
    return b.m


META = dict(
    num='15', name='Schwerer Granatwerfer', nick='WALZENWIEGE', col=KB,
    pill='KÖNIGSBLAU · APRIKOSE · TINTE', palette=[KB,AP,DK,HE], center=(394,302,0),
    desc='Ein tiefer blauer Rahmenschaft und ein geneigter Griff umschließen den großen Daumendurchgriff. '
         'Die helle Sechskammertrommel liegt offen zwischen hoher Brücke und vorderem Laufträger; der aprikosenfarbene Lauf folgt der oberen Kammer. '
         'Links im Heckgehäuse sitzt die große Ladeklappe.',
    form='Offener Daumenrahmenschaft · geneigter Griff mit freiem Abzugbügel · Ladeklappe links · '
         'Sechskammertrommel auf Trommelachse · hohe Brücke mit Visierschiene · Laufträger · Hochlauf mit Mündung · schräger Vordergriff',
    op=dict(
        reload_de='Ladeklappe links öffnen, Trommel kammerweise drehen, sechs Granaten einschieben und die Klappe schließen.',
        action_de='Das Federwerk in der Trommelachse dreht die Granattrommel nach jedem Schuss um eine Kammer weiter.',
        fire_de='Sechs schwere Granaten nacheinander; der Lauf folgt der oberen Trommelkammer, der Aufprallzünder löst am Ziel aus.',
        reload_en='Open the left loading gate, index the drum chamber by chamber, insert six grenades and close the gate.',
        action_en='The spring mechanism in the axle indexes the grenade drum by one chamber after each shot.',
        fire_en='Six heavy grenades in succession; the barrel aligns with the upper drum chamber and the impact fuse triggers on contact.'))
