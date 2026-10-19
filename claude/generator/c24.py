"""KC24 „Kometenschweif“: ein geschwungener unterer Träger umfasst das Mikroraketenrohr."""
from eng import rect, roundpoly, circ
from tlib import B, rail, trigger_group

UL, RO, EI, DK = '#383A8E', '#B36D42', '#9DEBC0', '#1B2032'
AX = 279


def model():
    b = B()
    D = b.D
    b.P([(95,274),(128,257),(181,259),(238,276),(241,310),
         (191,320),(149,343),(106,353),(111,329),(175,297),(126,292)],
        UL, -16, 16, r=9, L='Schaft')
    b.P([(94,268),(108,271),(119,314),(112,353),(96,362),
         (84,346),(89,307)], DK, -18, 18, r=8, L='Schaftkappe')
    b.P([(230,258),(285,247),(365,246),(425,253),(448,270),
         (445,318),(422,338),(288,344),(233,328)], UL, -24, 24,
        r=9, L='Gehäuse', dec=[D(roundpoly([(246,314),(290,330),(370,328),
                                             (429,313),(427,328),(371,338),(290,339),(245,326)],5), RO)])
    b.P([(250,245),(319,245),(332,258),(243,265)], RO, -13, 13,
        r=6, L='Schienensockel')
    rail(b, 255, 317, 245, DK, EI, w=10)
    b.P([(341,239),(375,231),(416,237),(434,250),(427,258),(342,258)],
        RO, -17, 17, r=8, L='Ladeklappe',
        dec=[D(roundpoly([(355,244),(376,239),(410,244),(418,249),(355,250)],3), EI)])
    b.P(circ(341,252,7,12), DK, -19, 19, L='Klappenscharnier')
    # Der seitliche Raketenvorrat besteht aus vier Rahmenleisten. Die vier
    # Ersatzraketen sind Volumen im Fenster, keine aufgemalten Dreiecke.
    for profile in (
        [(284,266),(417,266),(427,278),(285,279)],
        [(284,328),(424,328),(420,341),(287,341)],
        [(283,272),(295,272),(298,334),(284,335)],
        [(410,273),(424,273),(427,334),(413,334)],
    ):
        b.P(profile, RO, 24, 56, r=6, L='Raketenvorrat')
    for y in (283,294,305,316):
        b.P([(296,y),(383,y),(402,y+4),(383,y+8),(296,y+8)],
            EI, 33, 44, r=2, L='Ersatz-Mikrorakete')
    b.C(431, 697, AX, 16, UL, n=16, L='Abschussrohr')
    for x in (473,559,646):
        b.C(x, x+11, AX, 21, RO, n=16, L='Leitring')
    b.F(697, 718, AX, 16, 23, RO, n=16, L='Mündung')
    b.C(718, 726, AX, 23, DK, n=16, L='Mündung',
        cap=[(AX,0,15,DK,False),(AX,0,6,EI,True)])
    # Das Schweifband hängt unter dem Rohr und kehrt vor der Mündung zurück.
    # Zwischen Rohr und Band bleibt ein großer freier Durchblick.
    b.P([(418,312),(456,329),(505,343),(556,348),(603,340),
         (644,320),(666,292),(682,292),(676,312),(653,339),
         (610,360),(558,371),(501,366),(452,349),(418,333)],
        UL, -15, 15, r=10, L='Rohrträger',
        dec=[D(roundpoly([(436,330),(461,339),(506,353),(557,358),
                          (606,349),(647,330),(671,302),(653,336),
                          (610,355),(558,364),(504,359),(457,344),(435,337)],3), EI, True)])
    # Abgasfenster an der Rohrwurzel, vor dem Gehäuse sichtbar.
    for x in (445,456):
        b.P([(x,266),(x+5,266),(x+5,291),(x,291)], RO, -16.5, 16.5,
            r=2, L='Abgasrippe')
    b.P([(272,338),(315,337),(329,357),(304,402),(286,433),
         (251,438),(263,409),(283,361)], RO, -18, 18, r=9, L='Griff',
        dec=[D(roundpoly([(289,360),(308,357),(292,399),(269,422),(278,391)],5), UL)])
    trigger_group(b, 338, 337, EI, DK, grip_x0=315, depth=34)
    b.P([(585,351),(612,343),(624,361),(607,401),(584,417),
         (572,407),(594,370)], RO, -14, 14, r=8, L='Vordergriff')
    return b.m


META = dict(
    num='24', name='Mikroraketen-Granatwerfer', nick='KOMETENSCHWEIF', col=EI,
    pill='ULTRAMARIN · ROST · EISGRÜN', palette=[UL,RO,EI,DK], center=(406,323,0),
    desc='Ein ultramarinfarbener Schweif trägt das schlanke Abschussrohr von unten und schwingt vor der Mündung wieder nach oben. '
         'Drei Rostringe fassen das Rohr; die obere Ladeklappe und vier eisgrüne Ersatz-Mikroraketen im offenen Seitenvorrat erklären den Ladevorgang.',
    form='Geschwungener Schaft · Schaftkappe · Gehäuse · Ladeklappe oben mit hinterem Scharnier · '
         'Raketenvorrat links mit echtem Fenster und vier Mikroraketen · schlankes Abschussrohr mit drei Leitringen · '
         'Mündung mit Raketenspitze · unterer Schweifträger · Griff · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Obere Ladeklappe nach hinten öffnen, eine Mikrorakete aus dem Vorrat links ins Patronenlager legen und die Klappe schließen',
        action_de='Einschüssig: eine Rakete im Rohr, nach jedem Schuss neu laden; der Treibsatz zündet erst vor der Mündung',
        fire_de='Die Mikrorakete fliegt schnell und gerade statt im Bogen; Aufprallzünder, geringer Eigenschaden, Spezialmunition',
        reload_en='open the top gate to the rear, take one micro-missile from the left reserve into the chamber and close the gate',
        action_en='single shot: one missile in the tube, reload after each shot; the motor ignites just past the muzzle',
        fire_en='the micro-missile flies fast and straight instead of an arc; impact fuse, low self-damage, special ammunition'))
