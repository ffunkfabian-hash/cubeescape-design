"""KC11 „Windkamm“: ein langer Wellenschaft und ein durchbrochener Handschutz."""
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

AU, SA, LI, DK = '#57374F', '#D8BD91', '#CBE85B', '#201D27'


def model():
    b = B()
    D = b.D
    # Zwei gebogene Schaftzüge lassen das Daumenfenster wirklich offen.
    b.P([(77,257),(115,242),(162,243),(209,256),(257,258),
         (260,279),(207,278),(161,264),(116,264),(85,279)],
        AU,-15,15,r=9,L='Schaft')
    b.P([(83,325),(123,329),(168,320),(201,299),(224,275),
         (258,276),(244,307),(216,329),(175,348),(126,354),(82,347)],
        AU,-15,15,r=9,L='Schaftunterbogen',
        dec=[D(roundpoly([(99,338),(139,340),(177,329),(207,311),
                          (190,334),(145,348),(104,347)],4),SA)])
    b.P([(75,254),(88,257),(95,340),(85,357),(70,351),(65,278)],
        DK,-18,18,r=8,L='Schaftkappe')
    b.P([(116,233),(156,231),(202,243),(216,252),(199,259),(156,249),(116,251)],
        SA,-12,12,r=7,L='Wangenauflage')
    b.P([(248,257),(292,246),(377,244),(443,254),(466,272),
         (462,304),(437,321),(300,328),(251,313)],
        SA,-20,20,r=9,L='Gehäuse',
        dec=[D(roundpoly(rect(320,266,72,17),5),DK),
             D(roundpoly([(271,299),(327,310),(418,301),(446,286),
                          (440,307),(419,315),(323,320),(273,310)],5),AU),
             D(roundpoly(rect(402,267,30,6),3),LI,True)])
    rail(b,274,432,246,AU,SA,w=10)
    b.P([(360,272),(382,269),(388,278),(380,285),(360,284)],
        AU,20,33,r=6,L='Ladehebel')
    b.P([(276,322),(318,322),(332,347),(316,393),(294,426),
         (264,431),(257,420),(280,371)],AU,-18,18,r=9,L='Griff',
        dec=[D(roundpoly([(288,347),(303,349),(303,377),(284,412),
                          (274,416),(290,372)],5),DK)])
    trigger_group(b,335,322,LI,AU,grip_x0=309,depth=37)
    b.P([(405,320),(449,316),(458,327),(450,339),(405,342)],
        AU,-15,15,r=6,L='Magazinschacht')
    b.P([(411,335),(445,332),(455,376),(446,391),(415,392),(406,379)],
        SA,-13,13,r=7,L='Magazin',
        dec=[D(roundpoly(rect(419,346,17,29),4),DK),
             D(roundpoly(rect(422,351,11,5),2),LI),
             D(roundpoly(rect(422,363,11,5),2),LI)])
    b.P([(410,384),(450,381),(459,391),(449,401),(414,402)],
        AU,-15,15,r=6,L='Magazinboden')
    # Die obere und untere Welle umfassen drei offene Kühlfenster.
    b.P([(454,267),(493,253),(535,251),(580,261),(619,277),
         (622,289),(609,292),(574,278),(533,269),(495,270),(458,286)],
        AU,-14,14,r=9,L='Handschutz')
    b.P([(458,301),(497,310),(535,307),(576,292),(611,287),
         (622,298),(613,309),(582,310),(544,326),(495,331),(457,321)],
        AU,-14,14,r=9,L='Handschutzunterbogen',
        dec=[D(roundpoly([(478,317),(505,320),(543,315),(574,304),
                          (546,323),(506,327),(479,324)],3),SA)])
    for x,yt,yb in ((480,267,317),(530,263,319),(580,277,305)):
        b.P([(x,yt),(x+9,yt),(x+13,yb),(x+3,yb)],
            SA,-12,12,r=6,L='Kühlsteg')
    b.C(454,727,290,7,DK,n=12,L='Lauf')
    b.C(724,758,290,12,SA,n=12,L='Mündungsbremse',
        cap=[(290,0,6,DK,False)])
    for z0,z1 in ((10,13),(-13,-10)):
        b.P(roundpoly(rect(735,283,14,6),2),AU,z0,z1,r=2,L='Bremsenschlitz')
    return b.m


META = dict(
    num='11', name='Scout-Gewehr', nick='WINDKAMM', col=LI,
    pill='AUBERGINE · SAND · LIMETTE', palette=[AU,SA,LI,DK], center=(412,321,0),
    desc='Der lange auberginefarbene Lochschaft schwingt in zwei Wellen nach vorn. '
         'Ein durchbrochener Handschutz greift dieselbe Kurve auf; dahinter bleiben der lange Lauf '
         'und seine sandfarbene Mündungsbremse frei. Ein kurzes Magazin sitzt vor dem Abzug.',
    form='Offener Wellenschaft · Wangenauflage · schlankes Gehäuse · Ladehebel links · '
         'kurzes Kastenmagazin · gewellter offener Handschutz · langer Lauf · Mündungsbremse · Visierschiene',
    op=dict(
        reload_de='Kastenmagazin mit acht Patronen vor dem Abzug wechseln, Ladehebel links zurückziehen',
        action_de='Halbautomatik: den Verschluss nach dem Magazinwechsel einmal mit dem Ladehebel spannen',
        fire_de='Ein präziser Einzelschuss je Abzug; die Wange liegt auf der geschwungenen Wangenauflage',
        reload_en='swap the eight-round box magazine ahead of the trigger, then pull the left charging handle',
        action_en='semi-automatic: cock the bolt once with the charging handle after changing the magazine',
        fire_en='one precise shot per trigger pull; rest the cheek on the curved cheek piece'))
