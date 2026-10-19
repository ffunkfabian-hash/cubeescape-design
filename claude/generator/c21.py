"""KC21 „Sturmsegel“: hoher, an beiden Enden verwurzelter Segelrücken für Raketensalven."""
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

SC, BR, AP, DK = '#596675', '#873F67', '#FFC58F', '#20212C'


def model():
    b = B()
    D = b.D
    b.P([(92,277),(126,261),(183,264),(231,280),(233,311),
         (184,322),(142,342),(104,349),(109,325),(166,300),(122,293)],
        SC, -16, 16, r=9, L='Schaft')
    b.P([(92,270),(109,272),(119,315),(111,352),(94,360),(83,344),(87,307)],
        DK, -18, 18, r=8, L='Schaftkappe')
    b.P([(216,269),(287,265),(387,272),(459,268),(481,281),
         (481,313),(455,333),(291,337),(216,325)], SC, -23, 23,
        r=9, L='Gehäuse', dec=[D(roundpoly([(230,310),(291,320),(391,319),
                                             (458,309),(462,320),(391,331),(289,332),(228,321)],5), BR)])
    # Der hohe Segelrücken ist ein Bogen, kein aufgefüllter Keil. Beide Wurzeln
    # laufen bis ins Gehäuse; der Durchblick unter dem Scheitel bleibt offen.
    b.P([(190,278),(224,237),(275,200),(313,182),(366,178),(405,193),
         (448,226),(486,277),(463,281),(435,246),(395,217),
         (363,205),(321,207),(287,222),(244,251),(218,284)],
        BR, -17, 17, r=10, L='Segelrücken',
        dec=[D(roundpoly([(215,267),(240,239),(282,211),(320,192),(365,187),
                          (400,201),(437,232),(402,210),(364,196),(322,201),
                          (285,219),(245,247),(219,273)],3), AP, True)])
    b.P([(320,176),(371,176),(386,190),(315,194)], SC, -12, 12,
        r=6, L='Schienensockel')
    rail(b, 324, 370, 176, DK, AP, w=10)
    b.P([(317,282),(345,282),(351,294),(319,297)], AP, 22, 35,
        r=6, L='Ladehebel')
    # Querliegendes Raketenmagazin mit freiem Fenster und fünf sichtbaren Spitzen.
    for profile in (
        [(389,328),(473,328),(479,341),(389,342)],
        [(390,367),(477,367),(471,381),(397,381)],
        [(389,337),(401,337),(405,372),(393,372)],
        [(465,337),(478,337),(480,374),(466,374)],
    ):
        b.P(profile, BR, -25, 25, r=6, L='Raketenmagazin')
    for x in (404,416,428,440,452):
        b.P([(x,369),(x,352),(x+4,344),(x+8,352),(x+8,369)],
            AP, -8, 8, r=2, L='Mini-Rakete')
    # Offener Handschutz: obere und untere Schale mit schrägen Rippen.
    b.P([(476,271),(519,266),(567,270),(605,282),(598,292),
         (563,285),(519,282),(476,286)], SC, -17, 17, r=8, L='Handschutz')
    b.P([(476,311),(522,316),(565,307),(599,294),(604,309),
         (572,323),(525,333),(477,326)], SC, -17, 17, r=8, L='Handschutz')
    for x in (491,519,547,575):
        b.P([(x,278),(x+10,279),(x+1,321),(x-9,323)], BR, -17, 17,
            r=6, L='Handschutz')
    b.C(597, 702, 293, 13, DK, n=16, L='Lauf')
    b.F(631, 652, 293, 19, 14, BR, n=16, L='Abgasring')
    b.C(701, 722, 293, 18, BR, n=16, L='Mündung',
        cap=[(293,0,11,DK,False),(293,0,4,AP,True)])
    b.P([(259,330),(304,330),(316,351),(291,398),(275,428),
         (243,431),(249,402),(272,354)], BR, -18, 18, r=9, L='Griff',
        dec=[D(roundpoly([(276,352),(294,352),(278,395),(259,415),(266,386)],5), SC)])
    trigger_group(b, 322, 334, AP, DK, grip_x0=301, depth=34)
    b.P([(524,324),(552,320),(566,340),(547,382),(526,393),
         (516,380),(536,343)], BR, -14, 14, r=8, L='Vordergriff')
    return b.m


META = dict(
    num='21', name='Raketen-Impulsgewehr', nick='STURMSEGEL', col=AP,
    pill='SCHIEFER · BROMBEER · APRIKOSE', palette=[SC,BR,AP,DK], center=(404,302,0),
    desc='Ein hoher brombeerfarbener Segelrücken wächst aus beiden Enden des schieferfarbenen Gehäuses. '
         'Sein offener Bogen trägt die Visierschiene; unter dem Gehäuse zeigt ein querliegendes Rahmenmagazin fünf Mini-Raketen.',
    form='Geschwungener Schaft · Schaftkappe · Gehäuse mit Ladehebel links · hoher offener Segelrücken · '
         'querliegendes Raketenmagazin mit echtem Fenster · offener Handschutz · Rohrlauf mit Abgasring · Mündung · Griff · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Querliegendes Raketenmagazin nach unten ziehen, neues Magazin mit fünf Raketen einsetzen und den Ladehebel links zurückziehen',
        action_de='Impulsabzug: jede Betätigung feuert zwei Raketen als Salve; Abgas entweicht durch die offenen Schlitze im Handschutz',
        fire_de='Raketensalven explodieren beim Aufprall; Spezialmunition mit kleinem Vorrat',
        reload_en='pull the transverse rocket magazine down, insert a full five-rocket magazine and pull the left charging handle',
        action_en='pulse trigger: each pull fires a two-rocket burst; exhaust escapes through the open handguard slots',
        fire_en='rocket bursts explode on impact; special ammunition with a small reserve'))
