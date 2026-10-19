"""KF20 Raketenpistole „Sporn“: offener Handrahmen und tiefer Magazinsporn.

Der Rahmen umgreift die Hand hinten mit einem echten Durchbruch. Das Raketenmagazin
sitzt unter dem Griff, der kurze Schlitten bleibt mit seinen Abgasschlitzen frei beweglich.
"""
from eng import rect, roundpoly
from tlib import B, grip, rail, trigger_group

MA, ME, DK, HE = '#ED8838', '#177F9B', '#24323E', '#F4E1C1'


def model():
    b = B()
    D = b.D
    # Drei getrennte Stege umschließen das Fenster hinter dem geneigten Griff.
    b.P([(190,283),(252,281),(270,307),(252,327),(204,318),(185,302)],
        ME, -17, 17, r=6, L='Rahmen')
    b.P([(185,299),(205,308),(215,402),(239,413),(228,434),(195,419),(181,337)],
        ME, -17, 17, r=7, L='Rahmen')
    b.P([(210,405),(263,410),(276,429),(258,440),(224,435),(203,421)],
        ME, -17, 17, r=5, L='Rahmen')
    b.P([(225,288),(482,288),(501,304),(489,325),(328,316),(242,319)],
        MA, -19, 19, r=5, L='Rahmen',
        dec=[D([(415,300),(478,300),(484,310),(422,310)], HE)])
    grip(b, 250, 316, DK, ME, h=110, w=58, lean=18, z=18)
    # Der Magazinfuß bildet den namensgebenden Sporn, vollständig unter dem Griff.
    b.P([(231,422),(300,422),(317,455),(304,475),(224,466),(215,449)],
        ME, -22, 22, r=5, L='Raketenmagazin',
        dec=[D(roundpoly([(233,433),(290,433),(301,455),(231,454)], 3), DK)] +
            [D([(236+15*i,450),(241+15*i,436),(247+15*i,450)], MA) for i in range(4)])
    # Hohe Stirn und eingezogene Unterkante ergeben eine Keilform statt des G-Rechtecks.
    b.P([(204,250),(281,234),(309,224),(448,224),(485,245),(492,283),
         (474,294),(225,294),(201,279)], MA, -22, 22, r=6, L='Schlitten',
        dec=[D([(224,255),(297,241),(320,241),(299,260),(226,274)], HE)] +
            [D([(365+27*i,245),(379+27*i,245),(370+27*i,276),(356+27*i,276)], DK)
             for i in range(4)])
    rail(b, 281, 439, 234, DK, ME, w=9)
    b.C(485, 572, 267, 20, DK, n=8, L='Lauf',
        cap=[(267,0,14,'#080D12',False),(267,0,5,MA,True)])
    b.P(rect(512,246,42,6), ME, -9, 9, r=2)
    trigger_group(b, 329, 316, HE, ME, grip_x0=300, depth=38)
    return b.m


META = dict(
    num='20', name='Raketenpistole', nick='SPORN', col=MA,
    pill='MANDARINE · MEERBLAU · SCHIEFER', palette=[MA,ME,DK,HE], center=(377,348,0),
    desc='Ein meerblauer Handrahmen lässt hinter dem geneigten Griff ein großes Fenster frei; unten ragt das Raketenmagazin als breiter Sporn vor. '
         'Der mandarinfarbene Keilschlitten trägt vier große Abgasschlitze und eine eingelassene Visierschiene. '
         'Die weite Rohrmündung zeigt die Spitze der nächsten Mini-Rakete.',
    form='Offener hinterer Handrahmen · Keilschlitten mit Abgasschlitzen · tiefe Visierschiene · '
         'geneigter Griff · Raketenmagazin mit Fenster und Spornfuß · freier Abzugbügel · weites Raketenrohr',
    op=dict(
        reload_de='Raketenmagazin unter dem Griff herausziehen, volles Magazin mit sechs Mini-Raketen einsetzen und den Schlitten zurückziehen.',
        action_de='Halbautomatik: Der Schlitten läuft nach jedem Schuss zurück und lädt die nächste Rakete; Abgas entweicht durch seine Schlitze.',
        fire_de='Langsame Einzelschüsse; die Rakete zündet hinter der Mündung und explodiert beim Aufprall mit Flächenschaden.',
        reload_en='Pull the rocket magazine from the grip bottom, insert a full six-rocket magazine and rack the slide.',
        action_en='Semi-automatic: the slide cycles after each shot and chambers the next rocket; exhaust escapes through its slots.',
        fire_en='Slow single shots; the rocket ignites past the muzzle and explodes on impact with area damage.'))
