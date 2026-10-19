"""KC15 „Walzenbogen“: ein hoher Rücken über einer frei liegenden Granattrommel."""
import math
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

TB, TE, VA, DK = '#6C8FAD', '#A8513D', '#FFE2A1', '#1E2734'
AX = 307


def model():
    b = B()
    D = b.D
    b.P([(36,268),(65,246),(110,244),(154,255),(185,270),
         (184,291),(151,283),(108,266),(76,266),(48,285)],
        TB,-18,18,r=9,L='Schaft')
    b.P([(46,338),(84,337),(122,321),(151,293),(183,283),
         (186,310),(141,345),(91,362),(48,360)],
        TE,-18,18,r=9,L='Schaftunterbogen')
    b.P([(34,265),(48,268),(58,351),(45,370),(29,362),(22,286)],
        DK,-21,21,r=8,L='Schaftkappe')
    b.P([(177,266),(200,247),(248,241),(285,251),(307,276),
         (306,335),(288,359),(201,363),(177,342)],
        TB,-27,27,r=10,L='Gehäuse',
        dec=[D(roundpoly([(192,276),(211,262),(248,256),(279,267),
                          (284,280),(266,289),(209,291)],5),DK)])
    b.P([(242,306),(280,299),(296,307),(296,334),(278,346),(242,344)],
        TE,27,34,r=7,L='Ladeklappe',
        dec=[D(roundpoly(rect(253,314,24,8),3),VA)])
    # Die hohe Brücke lässt oberhalb der Trommel ein breites Luftfenster frei.
    b.P([(271,263),(278,230),(302,202),(343,184),(393,180),
         (446,191),(490,216),(515,245),(521,267),(502,274),
         (487,250),(464,229),(431,213),(391,207),(350,211),
         (320,224),(304,244),(300,267)],
        TB,-21,21,r=10,L='Oberbrücke',
        dec=[D(roundpoly([(292,230),(310,208),(346,192),(391,188),
                          (435,197),(468,215),(442,206),(393,198),
                          (350,201),(317,215),(300,236)],4),VA)])
    b.P([(318,198),(337,183),(392,176),(433,182),(452,198),
         (443,208),(393,201),(346,207)],TE,-15,15,r=7,L='Schienensockel')
    rail(b,340,431,183,DK,VA,w=10)
    b.C(306,432,AX,57,TE,n=18,L='Granattrommel',
        cap=[(AX-36*math.cos(k*math.pi/3),36*math.sin(k*math.pi/3),
              13,DK,False) for k in range(6)])
    for x in (322,405):
        b.C(x,x+8,AX,58,DK,n=18,L='Trommellaufring')
    # Breite Rippen liegen auf den Seiten; die Kammerstirn bleibt frei sichtbar.
    drum = next(p for p in b.m.parts if p.get('label') == 'Granattrommel')
    for yy in (279,299,319,339):
        for plane,z in (('z+',55),('z-',-55)):
            drum['dec'].append((plane,z,roundpoly(rect(340,yy,54,5),2),VA,False))
    b.C(284,456,AX,9,DK,n=12,L='Trommelachse')
    # Nur zwei schmale Bereiche am Laufträger statt einer Kammern verdeckenden Platte.
    b.P([(432,251),(466,247),(487,265),(487,284),(466,289),
         (448,280),(432,280)],TB,-22,22,r=8,L='Laufträger')
    b.P([(434,300),(455,298),(466,310),(452,329),(435,323)],
        TB,-14,14,r=7,L='Achsträger')
    b.C(476,630,AX-36,22,TE,n=16,L='Lauf')
    b.P([(487,280),(521,289),(563,292),(600,284),(610,293),
         (592,309),(554,317),(515,309),(485,296)],
        TB,-16,16,r=9,L='Laufwiege',
        dec=[D(roundpoly([(511,298),(553,307),(584,301),
                          (554,313),(517,305)],3),VA)])
    b.C(625,649,AX-36,28,DK,n=16,L='Mündung',
        cap=[(AX-36,0,19,DK,False)])
    b.P([(178,356),(218,354),(231,377),(210,427),(188,449),
         (163,441),(162,426),(182,391)],TE,-20,20,r=9,L='Griff',
        dec=[D(roundpoly([(193,377),(211,378),(199,413),(182,436),
                          (174,432),(191,396)],5),DK)])
    # Der Bügel endet bei x=303; die Trommel beginnt erst bei x=306.
    trigger_group(b,238,340,VA,TE,grip_x0=211,depth=38)
    b.P([(485,299),(517,300),(530,322),(515,363),(496,381),
         (475,370),(475,351),(489,327)],TE,-17,17,r=9,L='Vordergriff',
        dec=[D(roundpoly([(494,323),(510,324),(503,352),(490,367),
                          (483,360)],5),DK)])
    return b.m


META = dict(
    num='15', name='Schwerer Granatwerfer', nick='WALZENBOGEN', col=VA,
    pill='TAUBENBLAU · TERRAKOTTA · VANILLE', palette=[TB,TE,VA,DK], center=(336,312,0),
    desc='Ein hoher taubenblauer Rücken überspannt die große terrakottafarbene Granattrommel mit deutlichem Abstand. '
         'Die sechs Kammern bleiben vor dem schmalen Laufträger sichtbar. '
         'Der kurze dicke Lauf fluchtet mit der oberen Kammer; links am Heckrahmen sitzt die Ladeklappe.',
    form='Offener Bogenschaft · Heckrahmen mit Ladeklappe links · freie Sechskammertrommel · Trommelachse · '
         'hoch gekrümmte Oberbrücke · Visierschiene · schmaler Laufträger · dicker Lauf · Vordergriff',
    op=dict(
        reload_de='Ladeklappe links öffnen, die Trommel Kammer für Kammer drehen, sechs Granaten einschieben und die Klappe schließen',
        action_de='Das Federwerk in der Trommelachse dreht die Granattrommel nach jedem Schuss um eine Kammer weiter',
        fire_de='Sechs Granaten nacheinander mit Aufprallzünder; der Lauf fluchtet mit der oberen Trommelkammer',
        reload_en='open the left loading gate, index the drum chamber by chamber, insert six grenades and close the gate',
        action_en='the spring mechanism in the axle indexes the grenade drum by one chamber after each shot',
        fire_en='six impact-fused grenades in succession; the barrel lines up with the upper drum chamber'))
