"""KC12 „Mondsichel“: ein sichelförmiger Brückenrahmen um eine frei liegende Revolvertrommel."""
import math
from eng import rect, roundpoly
from tlib import B, rail, trigger_group
import ext

KB, KU, MI, DK = '#2449A4', '#D99564', '#86F0DA', '#141C2B'


def model():
    b = B()
    D = b.D
    # Die rückwärts geschwungene Griffwurzel führt die Sichel bis zum Griffende fort.
    b.P([(263,307),(313,306),(337,343),(319,381),(292,437),
         (258,457),(226,451),(252,418),(273,351)], KB, -20, 20, r=9,
        L='Griff', dec=[D(roundpoly([(267,338),(292,340),(303,369),
                                      (276,427),(248,441),(267,402)],6), KU)])
    b.P([(286,244),(326,246),(337,269),(337,311),(312,338),(280,323)],
        KB, -21, 21, r=8, L='Rahmen')
    b.P([(320,318),(446,318),(466,303),(474,318),(448,336),(316,337)],
        KU, -18, 18, r=7, L='Unterbrücke')
    b.P([(444,248),(467,246),(478,274),(465,325),(445,325)],
        KB, -20, 20, r=7, L='Rahmenpfosten')
    # Eine lange gekrümmte Oberbrücke statt des geraden G-Rahmens.
    b.P([(284,244),(328,231),(398,215),(478,214),(566,225),
         (644,239),(699,252),(709,264),(687,271),(625,255),
         (548,244),(474,239),(406,239),(341,254),(291,272)],
        KB, -19, 19, r=8, L='Oberbrücke',
        dec=[D(roundpoly([(308,247),(398,224),(476,223),(561,234),
                          (624,247),(553,239),(476,231),(402,232),(311,255)],3), MI, True)])
    b.P([(342,208),(446,208),(446,240),(398,244),(342,255)],
        KB,-13,13,r=6,L='Schienensockel')
    rail(b, 348, 438, 208, DK, KU, w=10)
    # Sechs Kammern: die obere Kammer liegt exakt auf y=260, der Laufachse.
    b.C(337, 444, 282, 34, KU, n=18, L='Trommel',
        cap=[(282-22*math.cos(k*math.pi/3),22*math.sin(k*math.pi/3),
              7,DK,False) for k in range(6)])
    # Aufgelegte, breite Trommelrippen; die Trommel bleibt ein einziges bewegliches Teil.
    drum = b.m.parts[-1]
    for yy in (268, 282, 296):
        for plane, z in (('z+', 32), ('z-', -32)):
            drum['dec'].append((plane,z,roundpoly(rect(351,yy-2,77,4),2),KB,False))
    b.P([(292,245),(281,224),(287,211),(305,227),(315,244)],
        KU,-6,6,r=6,L='Hahn')
    b.P(rect(302,290,20,11), MI, 21, 27, r=4, L='Trommelriegel')
    # Unter dem Lauf zieht eine zweite Sichel bis zur Mündung; vorne ist der Lauf frei.
    b.P([(467,268),(526,275),(602,277),(666,270),(687,266),
         (680,285),(621,305),(543,322),(472,319),(462,307)],
        KB,-15,15,r=9,L='Laufmantel',
        dec=[D(roundpoly([(487,299),(541,306),(606,293),(649,281),
                          (608,302),(544,316),(488,310)],3),KU)])
    b.C(464, 704, 260, 10, DK, n=16, L='Lauf',
        cap=[(260,0,6,DK,False)])
    b.C(696, 722, 260, 14, KU, n=16, L='Mündung',
        cap=[(260,0,7,DK,False)])
    b.C(444, 577, 309, 4, DK, n=10, cz=21, L='Ausstoßerstange')
    b.P(rect(560,299,15,20),KU,14,27,r=5,L='Stangenhalter')
    trigger_group(b, 345, 337, KU, DK, grip_x0=308, depth=36)
    # Ein gebogenes Leuchtband sitzt auf beiden Seiten des vorderen Mantels.
    for z in (-15.8, 15.8):
        start = len(b.m.parts)
        ext.tube(b.m, [(484,287,z),(516,290,z),(550,290,z),(581,286,z)],
                 1.8, MI, k=8, emit=True)
        for part in b.m.parts[start:]:
            part['label'] = 'Leuchtband'
    return b.m


META = dict(
    num='12', name='Handfeuerwaffe', nick='MONDSICHEL', col=MI,
    pill='KOBALT · KUPFER · MINT', palette=[KB,KU,MI,DK], center=(476,327,0),
    desc='Eine lange kobaltblaue Sichel bildet die Oberbrücke über der kupfernen Sechskammertrommel. '
         'Die zweite Sichel am Laufmantel und der zurückgeschwungene Griff geben dem Revolver seine gebogene Leitform; '
         'mintfarbene Bänder zeichnen die Kurven nach.',
    form='Sichelförmige Oberbrücke · freie Sechskammertrommel · geschwungener Griffrahmen · '
         'Hahn · Trommelriegel links · gebogener Laufmantel · Ausstoßerstange links · Visierschiene',
    op=dict(
        reload_de='Trommelriegel links drücken, Trommel ausschwenken, Ausstoßerstange drücken, sechs Patronen laden und Trommel schließen',
        action_de='Double Action: Abzug spannt den Hahn und dreht die Trommel um eine Kammer; der Hahn lässt sich auch von Hand spannen',
        fire_de='Ein schwerer Einzelschuss je Abzug; die obere Trommelkammer fluchtet mit dem Lauf',
        reload_en='press the left latch, swing out the cylinder, press the ejector rod, load six rounds and close the cylinder',
        action_en='double action: the trigger cocks the hammer and indexes one chamber; the hammer can also be cocked by hand',
        fire_en='one heavy shot per pull; the upper cylinder chamber lines up with the barrel'))
