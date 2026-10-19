"""KC20 „Kiesel“: gerundete Raketenpistole mit offen gefasstem Raketenmagazin."""
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

LE, PE, HO, DK = '#AD7861', '#2B6669', '#FFCC73', '#252629'


def model():
    b = B()
    D = b.D
    # Die Griffwurzel geht weich in das flache, kieselförmige Untergehäuse über.
    b.P([(232,290),(289,290),(310,316),(291,363),(282,403),
         (260,415),(224,404),(239,358),(245,326)], PE, -19, 19, r=9,
        L='Griff', dec=[D(roundpoly([(251,330),(280,328),(278,351),
                                     (262,390),(243,389),(257,348)],6), LE)])
    b.P([(218,276),(267,269),(411,278),(491,274),(504,289),
         (473,306),(387,319),(293,316),(231,306)], PE, -18, 18, r=10,
        L='Rahmen')
    # Ober- und Unterbogen des Schlittens begrenzen echte Abgasfenster.
    b.P([(209,259),(220,241),(260,224),(329,217),(399,223),
         (470,239),(499,256),(492,267),(459,255),(396,240),
         (330,233),(268,240),(231,254),(224,270)], LE, -21, 21, r=9,
        L='Schlitten', dec=[D(roundpoly([(250,236),(330,224),(395,230),
                                         (434,240),(394,236),(329,231),(253,242)],3), HO, True)])
    b.P([(214,271),(278,265),(366,270),(452,267),(493,261),
         (500,280),(464,289),(369,290),(281,282),(216,288)], LE, -21, 21,
        r=8, L='Schlitten')
    for x, yt, yb in ((230,251,274),(278,235,273),(321,229,278),
                       (365,232,280),(409,242,278),(452,253,275),(481,260,272)):
        b.P([(x,yt),(x+9,yt+1),(x+2,yb),(x-7,yb)], LE, -21, 21,
            r=6, L='Schlitten')
    # Kurzer Schienensockel wächst aus der flachen Scheitelzone des Schlittens.
    b.P([(281,208),(363,208),(382,229),(280,233)], PE, -13, 13,
        r=6, L='Schienensockel')
    rail(b, 290, 358, 208, DK, HO, w=10)
    b.C(489, 568, 265, 18, PE, n=16, L='Lauf',
        cap=[(265,0,12,DK,False),(265,0,5,HO,True)])
    b.P([(500,278),(533,276),(558,280),(552,291),(520,300),(489,295)],
        LE, -14, 14, r=8, L='Rohrträger')
    # Das Magazin ist ein offener Rahmen: vier Raketen stehen im Durchblick.
    for profile in (
        [(223,399),(283,399),(291,411),(218,412)],
        [(216,438),(291,438),(287,451),(218,451)],
        [(222,406),(233,406),(228,444),(216,444)],
        [(280,405),(290,407),(295,442),(283,444)],
    ):
        b.P(profile, LE, -19, 19, r=6, L='Raketenmagazin')
    for x in (235,248,261,274):
        b.P([(x,440),(x,421),(x+4,413),(x+8,421),(x+8,440)],
            HO, -7, 7, r=2, L='Mini-Rakete')
    trigger_group(b, 311, 315, HO, PE, grip_x0=286, depth=36)
    return b.m


META = dict(
    num='20', name='Raketenpistole', nick='KIESEL', col=HO,
    pill='LEHM · PETROL · HONIG', palette=[LE,PE,HO,DK], center=(394,333,0),
    desc='Ein gerundeter Lehmschlitten wölbt sich wie ein Kiesel über dem petrolfarbenen Rahmen. '
         'Durchbrochene Abgasfenster folgen seiner Kurve; im offenen Magazin unter dem geschwungenen Griff stehen honigfarbene Mini-Raketen.',
    form='Kieselförmiger Schlitten mit echten Abgasfenstern · Rahmen · geschwungener Griff · '
         'offen gefasstes Raketenmagazin · weites Raketenrohr mit Raketenspitze · Abzug im Bügel · Visierschiene',
    op=dict(
        reload_de='Raketenmagazin unten aus dem Griff ziehen, volles Magazin mit sechs Mini-Raketen einsetzen und den Schlitten zurückziehen',
        action_de='Halbautomatik: der Schlitten lädt nach jedem Schuss die nächste Rakete; Abgas entweicht durch die offenen Schlittenfenster',
        fire_de='Langsame Einzelschüsse; die Rakete zündet nach der Mündung und explodiert beim Aufprall mit Flächenschaden',
        reload_en='pull the rocket magazine from the grip bottom, insert six mini rockets in a full magazine and rack the slide',
        action_en='semi-automatic: the slide chambers the next rocket after each shot; exhaust escapes through the open slide windows',
        fire_en='slow single shots; the rocket ignites past the muzzle and explodes on impact with area damage'))
