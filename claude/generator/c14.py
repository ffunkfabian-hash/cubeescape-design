"""KC14 „Schnecke“: ein spiralig gebogener Rücken um einen kurzen Kipplauf."""
from eng import rect, roundpoly, circ
from tlib import B, rail, trigger_group

OC, PF, EI, DK = '#B68B30', '#654064', '#FFB9CF', '#29212C'


def model():
    b = B()
    D = b.D
    b.P([(99,271),(129,252),(177,251),(222,264),(250,280),
         (247,304),(214,293),(174,277),(136,277),(112,292)],
        PF,-16,16,r=9,L='Schaft')
    b.P([(110,329),(148,328),(188,309),(221,285),(247,288),
         (244,313),(200,340),(150,353),(111,351)],
        PF,-16,16,r=9,L='Schaftunterbogen')
    b.P([(98,267),(113,271),(121,342),(109,360),(94,352),(87,287)],
        DK,-19,19,r=8,L='Schaftkappe')
    # Die Ersatzgranate bleibt links neben dem offenen Schaft, im echten Halter.
    b.P([(148,275),(202,278),(213,291),(202,307),(149,305),(140,291)],
        OC,16,24,r=7,L='Granathalter')
    b.C(151,192,291,10,EI,n=12,cz=33,L='Granathülse')
    b.F(192,209,291,10,4,PF,n=12,cz=33,L='Ersatzgranate')
    b.P([(236,275),(265,257),(317,250),(357,262),(393,286),
         (398,315),(375,336),(263,338),(237,319)],
        OC,-22,22,r=9,L='Gehäuse',
        dec=[D(roundpoly([(254,291),(276,278),(321,274),(350,283),
                          (353,299),(328,310),(271,314)],6),PF),
             D(roundpoly(rect(270,290,47,7),3),EI,True)])
    b.P([(264,255),(282,242),(326,241),(354,254),(349,266),
         (285,265)],PF,-14,14,r=7,L='Schienensockel')
    rail(b,276,345,248,PF,OC,w=10)
    b.P([(354,262),(367,244),(386,243),(395,255),(384,271),
         (367,277)],EI,-7,7,r=6,L='Verriegelungshebel')
    b.P(circ(398,319,13,16),PF,-26,26,L='Scharnier',
        dec=[D(circ(398,319,6,12),EI)])
    # Kurzer Funktionslauf, frei vor der Schneckenwindung.
    b.C(394,559,290,25,PF,n=16,L='Kipplauf')
    b.C(553,578,290,30,OC,n=16,L='Mündung',
        cap=[(290,0,21,DK,False),(290,0,15,DK,False)])
    # Zwei seitliche Spiralwangen lassen den zentralen Sichtkanal z=-10..10 frei.
    # Ihre Füße greifen seitlich in die Laufwurzel, ohne den Kanal zu überbrücken.
    spiral = [(399,271),(385,251),(384,221),(399,195),(428,180),
         (461,180),(492,196),(506,219),(506,244),(490,264),
         (467,271),(446,264),(435,250),(437,233),(453,226),
         (468,231),(472,242),(461,247),(455,241),(454,246),
         (465,253),(481,248),(490,235),(488,218),(478,204),
         (459,196),(434,197),(413,207),(402,225),(404,245),(416,262)]
    spiral_band = roundpoly([(400,234),(406,212),(428,197),(453,192),
                             (475,199),(487,213),(477,206),(456,200),
                             (433,204),(416,217),(410,236),(416,254),
                             (409,254)],3)
    for z0,z1 in ((10,22),(-22,-10)):
        b.P(spiral,OC,z0,z1,r=7,L='Schneckenbogen')
        plane,z = ('z+',z1) if z0>0 else ('z-',z0)
        b.m.parts[-1]['dec'].append((plane,z,spiral_band,EI,True))
        b.P([(398,264),(410,260),(423,282),(414,297),(398,290)],
            OC,z0,z1,r=6,L='Schneckenfuß')
    b.P([(411,306),(440,305),(457,317),(462,337),(450,350),
         (426,343),(409,328)],OC,-17,17,r=8,L='Laufwiege')
    b.P([(274,333),(313,332),(326,354),(309,403),(286,430),
         (262,427),(257,413),(277,371)],PF,-18,18,r=9,L='Griff',
        dec=[D(roundpoly([(287,352),(306,354),(295,390),(276,416),
                          (269,412),(286,376)],5),DK)])
    trigger_group(b,333,313,EI,PF,grip_x0=307,depth=37)
    b.P([(457,313),(486,313),(500,330),(490,369),(474,385),
         (453,377),(449,362),(460,338)],PF,-15,15,r=9,L='Vordergriff',
        dec=[D(roundpoly([(466,337),(482,337),(477,363),(466,373),
                          (461,365)],4),DK)])
    return b.m


META = dict(
    num='14', name='Spezial-Granatwerfer', nick='SCHNECKE', col=EI,
    pill='OCKER · PFLAUME · EISROSA', palette=[OC,PF,EI,DK], center=(334,303,0),
    desc='Ein ockerfarbener Spiralbogen rollt sich über der Wurzel des kurzen pflaumenfarbenen Kipplaufs ein. '
         'Das offene Schneckenfenster und der gebogene Schaft geben dem einschüssigen Werfer seine Silhouette. '
         'Links am Schaft steckt eine eisrosa Ersatzgranate im Halter.',
    form='Offener Bogenschaft · Ersatzgranate im Halter links · kurzes Gehäuse · offener Schneckenbogen · '
         'Kipplauf · Verriegelungshebel · Scharnier · Mündungsring · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Verriegelungshebel rechts drücken, Kipplauf am Scharnier abkippen, Hülse auswerfen, eine Granate einschieben und zuklappen',
        action_de='Ein Schuss je Ladung; die Ersatzgranate sitzt links am Schaft, der Schneckenbogen kippt mit dem Lauf',
        fire_de='Granate im Bogen; Aufprallzünder oder Fernzündung durch erneutes Drücken des Abzugs',
        reload_en='push the locking lever right, tip the barrel down on its hinge, eject the case, insert one grenade and close',
        action_en='one shot per load; a spare grenade sits on the left stock, and the spiral shell tips with the barrel',
        fire_en='lobbed grenade; impact fuse or remote detonation with a second trigger pull'))
