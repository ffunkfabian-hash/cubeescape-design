"""KC22 „Dornbogen“: spitz auslaufender Bogenschaft und schlanker gezogener Lauf."""
import math
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

ES, SE, BE, DK = '#59453A', '#63B1A2', '#F6B84E', '#211F20'


def model():
    b = B()
    D = b.D
    # Zwei gekrümmte Schaftarme treffen sich in einer langen, stumpfen Dornspitze.
    b.P([(73,286),(126,263),(186,250),(250,250),(265,263),(256,279),
         (192,271),(137,279),(84,300)], ES, -16, 16, r=9, L='Schaft',
        dec=[D(roundpoly([(101,282),(139,270),(191,259),(240,259),
                          (238,265),(191,266),(140,276),(103,288)],3), SE)])
    b.P([(81,294),(127,308),(182,318),(244,310),(259,321),
         (235,336),(179,343),(125,327),(72,306)], ES, -16, 16,
        r=9, L='Schaft')
    b.P([(69,284),(83,284),(95,296),(85,311),(72,314),(63,304)],
        DK, -18, 18, r=6, L='Schaftkappe')
    b.P([(246,251),(296,242),(377,247),(465,256),(492,272),
         (481,311),(459,331),(303,338),(247,324)], ES, -23, 23,
        r=9, L='Gehäuse', dec=[D(roundpoly([(262,308),(311,321),(399,316),
                                             (467,298),(459,320),(400,330),(306,333),(261,320)],5), SE),
                               D(roundpoly(rect(384,266,65,7),3), BE, True)])
    b.P([(274,239),(367,239),(386,251),(267,258)], SE, -13, 13,
        r=6, L='Schienensockel')
    rail(b, 283, 361, 239, DK, BE, w=10)
    b.P([(327,269),(351,269),(359,280),(330,285)], BE, 22, 35,
        r=6, L='Ladehebel')
    # Das Slug-Fenster ist eine echte Öffnung im vierteiligen Magazinrahmen.
    for profile in (
        [(404,328),(457,328),(465,343),(405,344)],
        [(406,397),(468,395),(474,410),(409,414)],
        [(405,337),(418,338),(421,405),(408,407)],
        [(451,338),(464,337),(470,402),(457,403)],
    ):
        b.P(profile, SE, -17, 17, r=6, L='Magazin')
    for y in (352,367,382):
        b.P([(418,y),(443,y),(453,y+5),(443,y+10),(419,y+10)],
            BE, -7, 7, r=3, L='Slug-Patrone')
    # Ein zweiter, lang auslaufender Bogen trägt den vorderen Laufmantel.
    b.P([(479,264),(532,260),(582,266),(628,278),(644,285),
         (619,288),(580,279),(533,275),(482,279)], ES, -15, 15,
        r=8, L='Laufmantel')
    b.P([(479,310),(535,314),(586,304),(626,286),(644,285),
         (630,302),(590,321),(535,331),(478,325)], ES, -15, 15,
        r=8, L='Laufmantel')
    for x, yt, yb in ((496,272,319),(530,270,321),(565,275,314),(600,281,302)):
        b.P([(x,yt),(x+10,yt+2),(x+5,yb),(x-6,yb)], SE, -15, 15,
            r=6, L='Laufmantel')
    b.C(483, 748, 285, 10, DK, n=16, L='Lauf')
    b.C(748, 782, 285, 16, ES, n=16, L='Mündungsbremse',
        cap=[(285,0,8.5,DK,False)] +
            [(285+9*math.sin(k*math.pi/3),9*math.cos(k*math.pi/3),1.4,BE,False)
             for k in range(6)])
    b.P([(752,276),(773,276),(776,280),(751,280)], SE, -13, 13,
        r=3, L='Bremsenschlitz')
    b.P([(280,331),(319,331),(330,350),(303,398),(287,429),
         (251,435),(263,407),(286,355)], ES, -18, 18, r=9, L='Griff',
        dec=[D(roundpoly([(290,354),(309,353),(293,394),(269,421),(277,393)],5), SE)])
    trigger_group(b, 337, 331, BE, DK, grip_x0=316, depth=34)
    b.P([(540,324),(568,319),(579,337),(561,378),(540,392),
         (528,382),(550,342)], SE, -13, 13, r=8, L='Vordergriff')
    return b.m


META = dict(
    num='22', name='Slug-Schrotflinte', nick='DORNBOGEN', col=BE,
    pill='ESPRESSO · SEEGRÜN · BERNSTEIN', palette=[ES,SE,BE,DK], center=(423,322,0),
    desc='Ein langer espressofarbener Bogenschaft läuft hinten in einer gerundeten Dornspitze zusammen. '
         'Der geschwungene Laufmantel gibt einen schlanken gezogenen Lauf frei; im seegrünen Magazinrahmen stehen bernsteinfarbene Slug-Patronen.',
    form='Spitz zulaufender offener Bogenschaft · Schaftkappe · Gehäuse mit Ladehebel links · '
         'Kastenmagazin mit echtem Slug-Fenster · durchbrochener Bogen-Laufmantel · gezogener Lauf · '
         'Mündungsbremse mit sechs Zügen · Griff · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Kastenmagazin mit fünf Slug-Patronen vor dem Abzug wechseln und den Ladehebel links zurückziehen',
        action_de='Halbautomatik: ein Geschoss je Abzug; den Ladehebel nach dem Magazinwechsel betätigen',
        fire_de='Ein schwerer Slug mit hoher Präzision auf mittlere Distanz; kein Streukegel',
        reload_en='swap the five-round slug box magazine ahead of the trigger and pull the left charging handle',
        action_en='semi-automatic: one projectile per pull; operate the charging handle after changing the magazine',
        fire_en='one heavy slug with precision at medium range; no spread cone'))
