"""KF21 Raketen-Impulsgewehr „Querwind“: tiefer Fensterschaft und breites Quermagazin."""
from eng import rect, roundpoly
from tlib import B, grip, rail, trigger_group

FU, CH, DK, HE = '#BE3C9C', '#D2E45E', '#302237', '#EFEAD5'


def model():
    b = B()
    D = b.D
    # Der Schaft besteht aus drei Stegen; das große Daumenfenster ist kein Aufkleber.
    b.P([(93,264),(166,248),(263,251),(282,283),(252,302),(116,295)],
        FU, -19, 19, r=7, L='Schaft',
        dec=[D([(129,266),(196,259),(235,265),(225,279),(132,282)], HE)])
    b.P([(87,278),(115,288),(123,395),(148,412),(130,432),(99,416),(86,337)],
        FU, -19, 19, r=7, L='Schaft')
    b.P([(115,403),(280,408),(305,420),(290,439),(140,438),(110,422)],
        CH, -17, 17, r=6, L='Schaft')
    b.P([(75,276),(89,272),(104,417),(94,433),(80,415)],
        DK, -21, 21, r=5, L='Schaftkappe')
    b.P([(252,249),(452,249),(478,263),(487,295),(466,317),(415,313),(252,313)],
        FU, -23, 23, r=7, L='Gehäuse',
        dec=[D([(356,270),(428,270),(453,288),(432,300),(356,293)], HE),
             D(roundpoly(rect(270,268,57,14),3), DK)])
    rail(b, 283, 433, 249, DK, CH, w=10)
    b.P(rect(300,280,30,12), CH, 23, 37, r=3, L='Ladehebel')
    grip(b, 274, 313, DK, FU, h=113, w=52, lean=20, z=19)
    trigger_group(b, 338, 313, HE, CH, grip_x0=319, depth=36)
    # Deutlich quer ausladende Kassette: das schmale Seitengesicht zeigt fünf Raketen.
    b.P([(432,311),(503,311),(517,335),(512,384),(491,402),(445,392)],
        CH, -43, 43, r=6, L='Raketenmagazin',
        dec=[D(roundpoly([(444,330),(498,330),(500,371),(449,376)],4), DK)] +
            [D([(446+10*i,365),(450+10*i,337),(455+10*i,365)], FU) for i in range(5)])
    b.P([(482,263),(596,253),(628,270),(628,304),(596,326),(511,316),(482,294)],
        CH, -19, 19, r=7, L='Handschutz',
        dec=[D([(507+28*i,273),(522+28*i,271),(516+28*i,302),(501+28*i,300)], DK)
             for i in range(4)])
    b.P([(559,320),(595,320),(606,367),(589,395),(565,389),(550,354)],
        FU, -16, 16, r=7, L='Vordergriff',
        dec=[D([(567,338),(584,338),(592,366),(580,378),(569,369)], DK)])
    b.C(628, 708, 286, 14, DK, n=8, L='Lauf')
    b.F(658, 681, 286, 20, 16, FU, n=8, L='Abgasring')
    b.C(708, 730, 286, 19, DK, n=8, L='Mündung',
        cap=[(286,0,12,'#09070D',False),(286,0,4,CH,True)])
    return b.m


META = dict(
    num='21', name='Raketen-Impulsgewehr', nick='QUERWIND', col=FU,
    pill='FUCHSIA · CHARTREUSE · AUBERGINE', palette=[FU,CH,DK,HE], center=(402,344,0),
    desc='Ein tiefer fuchsiafarbener Rahmenschaft umschließt das große Daumenfenster und endet in einer chartreusefarbenen Unterstrebe. '
         'Das quer ausladende Raketenmagazin zeigt fünf Raketenspitzen im breiten Fenster; davor sitzt der kurze geneigte Vordergriff. '
         'Große Abgasschlitze, Rohrlauf und Abgasring kennzeichnen die Raketensalven-Mechanik.',
    form='Offener tiefer Daumenlochschaft · kompaktes Gehäuse mit Ladehebel links · eingelassene Visierschiene · '
         'quer ausladendes Raketenmagazin mit Fenster · geschlitzter Handschutz · geneigter Vordergriff · Rohrlauf mit Abgasring und Mündung',
    op=dict(
        reload_de='Breites Raketenmagazin nach unten ziehen, neue Kassette mit fünf Raketen einsetzen und den Ladehebel links zurückziehen.',
        action_de='Jede Abzugbetätigung feuert eine Salve aus zwei Raketen; das Abgas entweicht nach vorn durch die Handschutzschlitze.',
        fire_de='Raketensalven mit Explosion beim Aufprall; Spezialmunition und kleiner Vorrat.',
        reload_en='Pull the wide rocket magazine down, insert a fresh five-rocket cassette and pull the left charging handle.',
        action_en='Each trigger pull fires a two-rocket burst; exhaust vents forward through the handguard slots.',
        fire_en='Rocket bursts explode on impact; special ammunition with a small reserve.'))
