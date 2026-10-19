"""KF22 Slug-Schrotflinte „Hohlrücken“: hoher offener Rückenschaft und geneigtes Slug-Magazin."""
import math

from eng import rect, roundpoly
from tlib import B, grip, rail, trigger_group

ZI, HI, DK, HE = '#D75237', '#76BDEB', '#292B3C', '#F0E6D4'


def model():
    b = B()
    D = b.D
    # Hohler, hoher Rücken statt des kompakten G-Schaftkeils; der Durchgriff bleibt offen.
    b.P([(87,266),(124,234),(175,221),(266,240),(286,266),(270,286),(175,258),(112,290)],
        HI, -19, 19, r=7, L='Schaft',
        dec=[D([(128,246),(177,234),(234,246),(228,258),(178,248),(136,260)], HE)])
    b.P([(87,268),(112,282),(120,391),(143,407),(129,431),(96,410),(83,334)],
        HI, -19, 19, r=8, L='Schaft')
    b.P([(110,400),(272,405),(298,418),(283,438),(136,437),(105,419)],
        ZI, -17, 17, r=6, L='Schaft')
    b.P([(72,271),(87,263),(102,410),(91,432),(77,414)],
        DK, -21, 21, r=5, L='Schaftkappe')
    b.P([(266,248),(452,248),(487,268),(493,298),(476,326),(266,326)],
        ZI, -24, 24, r=7, L='Gehäuse',
        dec=[D([(362,266),(445,266),(466,285),(451,307),(365,297)], HI),
             D(roundpoly(rect(280,274,56,14),3), DK)])
    rail(b, 289, 443, 248, DK, HI, w=10)
    b.P(rect(321,286,30,12), HE, 24, 38, r=3, L='Ladehebel')
    grip(b, 270, 326, DK, HI, h=106, w=52, lean=20, z=19)
    trigger_group(b, 333, 326, HE, HI, grip_x0=315, depth=35)
    # Schmaler Hals, weiter nach vorn ausschwingender Magazinfuß; hinterste Kante bleibt vor dem Bügel.
    b.P(rect(428,318,66,16), DK, -18, 18, r=3)
    b.P([(439,331),(490,331),(507,369),(525,407),(510,438),(451,431),(429,371)],
        HI, -18, 18, r=5, L='Magazin',
        dec=[D(roundpoly([(449,343),(480,343),(501,402),(460,398)],4), DK),
             D([(452,350),(478,350),(481,358),(454,358)], HE),
             D([(456,367),(484,367),(487,375),(459,375)], HE),
             D([(462,384),(490,384),(493,392),(465,392)], HE)])
    b.P([(450,422),(513,428),(517,440),(450,439)], ZI, -20, 20, r=3)
    b.P([(491,265),(618,255),(650,271),(650,301),(617,316),(491,312)],
        ZI, -18, 18, r=7, L='Laufmantel',
        dec=[D([(511+29*i,275),(527+29*i,273),(525+29*i,298),(509+29*i,298)], DK)
             for i in range(4)])
    b.P([(564,313),(599,313),(611,359),(593,393),(570,387),(555,347)],
        HI, -16, 16, r=7, L='Vordergriff',
        dec=[D([(573,331),(588,331),(597,359),(584,377),(574,364)], DK)])
    b.C(650, 750, 285, 12, DK, n=12, L='Lauf')
    b.C(750, 789, 285, 19, HI, n=8, L='Mündungsbremse',
        cap=[(285,0,10,'#08090F',False)] +
            [(285+10.5*math.sin(k*math.pi/3),10.5*math.cos(k*math.pi/3),1.6,ZI,False)
             for k in range(6)])
    b.P(rect(758,274,23,6), DK, -14, 14, r=2)
    return b.m


META = dict(
    num='22', name='Slug-Schrotflinte', nick='HOHLRÜCKEN', col=ZI,
    pill='ZINNOBER · HIMMELBLAU · NACHTGRAU', palette=[ZI,HI,DK,HE], center=(428,330,0),
    desc='Der hohe himmelblaue Schaftrücken rahmt einen großen offenen Durchgriff über der zinnoberfarbenen Unterstrebe. '
         'Ein nach vorn geneigtes Kastenmagazin zeigt drei Slug-Patronen; sein breiter Fuß bleibt deutlich vor dem Abzugbügel. '
         'Der gezogene Einzellauf endet in einer achteckigen Mündungsbremse mit runder Bohrung und sechs Zügen.',
    form='Hoher hohler Rahmenschaft · Gehäuse mit Ladehebel links und tiefer Visierschiene · geneigter Griff mit freiem Abzugbügel · '
         'ausladendes Kastenmagazin mit Slug-Fenster · belüfteter Laufmantel · kurzer Vordergriff · gezogener Lauf · Mündungsbremse',
    op=dict(
        reload_de='Kastenmagazin vor dem Abzug nach unten herausziehen, volles Magazin mit fünf Slugs einsetzen und den Ladehebel links zurückziehen.',
        action_de='Halbautomatik mit einem Geschoss je Abzug; den Ladehebel nur nach dem Magazinwechsel betätigen.',
        fire_de='Ein schweres Einzelgeschoss mit hoher Wucht und Präzision auf mittlere Distanz; kein Streukegel.',
        reload_en='Pull the box magazine down ahead of the trigger, insert a fresh five-slug magazine and pull the left charging handle.',
        action_en='Semi-automatic with one projectile per pull; operate the charging handle only after a magazine change.',
        fire_en='One heavy slug with high impact and precision at medium range; no spread cone.'))
