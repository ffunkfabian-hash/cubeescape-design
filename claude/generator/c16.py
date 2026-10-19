"""KC16 „Panzerrücken“: gewölbtes Gurt-MG mit tiefem Kasten und offenem Laufgerüst."""
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

MO, ZI, LA, DK = '#6F7849', '#B4C5CC', '#FFA285', '#20271F'


def model():
    b = B()
    D = b.D
    # Zwei gebogene Holme lassen ein echtes Schaftfenster frei.
    b.P([(65,258),(109,242),(183,243),(251,263),(274,283),
         (245,298),(188,270),(116,267),(70,281)], MO,-18,18,r=9,L='Schaft')
    b.P([(69,322),(123,326),(196,304),(247,282),(269,300),
         (203,330),(125,353),(66,347)], MO,-18,18,r=9,L='Schaft')
    b.P([(60,252),(77,255),(82,343),(64,356),(52,339)],DK,-20,20,r=7,L='Schaftkappe')
    b.P([(246,259),(294,241),(449,237),(535,260),(553,288),
         (538,326),(480,343),(270,338),(246,316)],MO,-27,27,r=10,L='Gehäuse',
        dec=[D(roundpoly([(277,314),(465,317),(515,302),(502,321),(465,333),(281,329)],6),ZI)])
    # Der gepanzerte Deckel bildet den höchsten Punkt des Rückens.
    b.P([(286,244),(326,222),(391,211),(453,218),(505,239),
         (518,258),(456,239),(392,232),(331,240),(290,258)],ZI,-25,25,r=9,L='Zuführdeckel')
    b.C(280,297,250,8,DK,n=12,L='Deckelscharnier')
    b.P(rect(340,214,108,19),MO,-13,13,r=6,L='Schienensockel')
    rail(b,347,439,214,DK,ZI,w=11)
    b.P([(464,268),(501,268),(514,278),(505,288),(466,286)],LA,27,39,r=6,L='Ladehebel')
    b.P([(331,317),(432,317),(455,345),(453,430),(430,451),
         (351,441),(328,416)],MO,27,78,r=10,L='Munitionskasten',
        dec=[D(roundpoly([(344,351),(436,353),(436,420),(421,432),(346,421)],7),DK),
             D(roundpoly([(347,331),(425,332),(436,345),(347,344)],4),LA)])
    b.P([(344,267),(384,263),(411,280),(414,322),(380,327),
         (378,297),(348,289)],ZI,26,44,r=6,L='Patronengurt',
        dec=[D(roundpoly(rect(350+9*i,271+3*i,5,20),2),MO) for i in range(6)])
    # Ober- und Unterholm mit getrennten Rippen: echte Durchblicke zum Lauf.
    b.P([(530,260),(591,244),(659,245),(722,259),(780,278),
         (778,292),(715,277),(655,264),(593,263),(537,280)],MO,-22,22,r=9,L='Laufmantel')
    b.P([(535,309),(596,322),(664,320),(727,309),(779,293),
         (783,311),(731,330),(665,341),(593,341),(536,329)],MO,-22,22,r=9,L='Laufmantel')
    for x,y in ((551,274),(624,261),(704,275),(765,287)):
        b.P([(x,y),(x+12,y+2),(x+16,326),(x+2,330)],ZI,-21,21,r=6,L='Mantelrippe')
    b.C(539,872,296,9,DK,n=14,L='Lauf')
    b.C(865,908,296,16,ZI,n=12,L='Feuerdämpfer',cap=[(296,0,8,DK,False)])
    # Drei Teile bilden den Tragegriff; der Bogen darunter bleibt offen.
    b.P([(581,252),(575,219),(585,211),(598,251)],ZI,-9,9,r=6,L='Tragegriff')
    b.P([(659,251),(653,215),(669,221),(677,256)],ZI,-9,9,r=6,L='Tragegriff')
    b.P([(574,219),(590,200),(625,194),(655,201),(672,222),
         (655,226),(637,215),(613,212),(590,229)],MO,-12,12,r=8,L='Tragegriff')
    for z in (-13,13):
        b.C(686,780,348,4,DK,n=10,cz=z,L='Zweibein')
    b.P(rect(680,328,20,24),ZI,-19,19,r=6,L='Zweibeingelenk')
    b.P([(276,334),(324,337),(317,377),(286,432),(256,427),
         (276,379)],MO,-19,19,r=9,L='Griff',
        dec=[D(roundpoly([(287,357),(306,361),(299,388),(280,417),(271,415)],6),DK)])
    trigger_group(b,342,337,LA,ZI,grip_x0=315,depth=36)
    b.P([(578,336),(617,337),(628,370),(612,400),(588,396),
         (596,369)],MO,-15,15,r=9,L='Vordergriff')
    return b.m


META = dict(
    num='16', name='Maschinengewehr', nick='PANZERRÜCKEN', col=LA,
    pill='MOOS · ZINN · LACHSLICHT', palette=[MO,ZI,LA,DK], center=(480,322,0),
    desc='Ein gewölbter Zinnrücken überspannt das moosfarbene Gurt-MG. Der tiefe seitliche Munitionskasten hängt unter der Zuführung; '
         'offene Schaftholme, ein gekrümmter Tragegriff und der durchbrochene Laufmantel halten die schwere Form lesbar.',
    form='Offener Bogenschaft · gewölbter Zuführdeckel mit Visierschiene · tiefer Munitionskasten links · Patronengurt · Ladehebel · '
         'offener Laufmantel · Tragegriff · Lauf mit Feuerdämpfer · eingeklapptes Zweibein · Vordergriff',
    op=dict(
        reload_de='Zuführdeckel hinten aufklappen, Munitionskasten links wechseln, Gurt einlegen, Deckel schließen und Ladehebel ziehen',
        action_de='Gurtzuführung: Der Verschluss zieht den Patronengurt nach jedem Schuss um eine Patrone weiter',
        fire_de='Dauerfeuer mit steigender Feuerrate; der Tragegriff ermöglicht den Laufwechsel',
        reload_en='open the rear-hinged feed cover, swap the left ammo box, lay in the belt, close the cover and pull the charging handle',
        action_en='belt feed: the bolt advances the belt by one round after each shot',
        fire_en='sustained full-auto fire with rising rate; the carry handle supports barrel changes'))
