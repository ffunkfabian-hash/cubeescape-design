"""KF11 Scout-Gewehr „Kieselband“: breiter Kieselschaft mit echtem Daumenfenster und schlanker Laufnase."""
from eng import rect
from tlib import B, rail, trigger_group

TU, AU, DK, HE = '#32B8B1', '#58264C', '#172E35', '#F6DFCB'


def model():
    b = B()
    D = b.D
    # Drei getrennte Bänder um ein wirklich offenes, tropfenförmiges Daumenfenster.
    b.P([(83,267),(115,245),(192,238),(268,254),(285,281),(247,295),(169,278),(112,287)],
        TU, -20, 20, r=9, L='Schaft',
        dec=[D([(123,255),(185,248),(223,258),(192,267),(131,272)], HE)])
    b.P([(83,270),(113,279),(126,340),(157,373),(144,399),(107,379),(87,333)],
        AU, -19, 19, r=9, L='Schaft')
    b.P([(142,375),(239,368),(279,346),(286,372),(244,397),(145,399)],
        TU, -17, 17, r=8, L='Schaft')
    b.P([(75,267),(88,259),(102,331),(117,375),(107,390),(92,374),(76,317)],
        DK, -23, 23, r=6, L='Schaftkappe')
    b.P([(120,242),(191,231),(240,242),(243,258),(191,247),(120,258)],
        HE, -15, 15, r=5, L='Wangenauflage')
    # Breiter, flacher Kieselkörper; der Handschutz steigt vorn zur schlanken Laufnase an.
    b.P([(246,256),(344,247),(451,253),(477,274),(469,310),(433,328),(273,328),(249,307)],
        TU, -23, 23, r=10, L='Gehäuse',
        dec=[D([(281,272),(339,267),(366,280),(355,293),(287,296)], AU),
             D([(388,274),(444,278),(449,289),(391,286)], HE)])
    rail(b, 270, 426, 254, DK, AU, w=10)
    # Auswurffenster rechts und Ladehebel links sind funktionale, große Einzelteile.
    b.P([(326,275),(369,275),(369,293),(326,293)], DK, -25, -23, r=3, L='Auswurffenster')
    b.P([(336,276),(366,276),(373,283),(364,289),(336,289)],
        AU, 23, 36, r=3, L='Ladehebel')
    b.P([(255,324),(306,324),(297,359),(279,404),(251,414),(234,399),(246,356)],
        AU, -18, 18, r=8, L='Griff',
        dec=[D([(261,346),(287,346),(279,376),(261,392),(250,388)], DK)])
    trigger_group(b, 323, 328, HE, DK, grip_x0=284, depth=39)
    # Der Bügel endet x=388; das Magazin beginnt erst x=412.
    b.P([(408,320),(456,320),(461,338),(410,340)], AU, -16, 16, r=4, L='Magazinschacht')
    b.P([(416,335),(452,335),(465,382),(452,397),(419,390),(408,352)],
        HE, -13, 13, r=5, L='Magazin',
        dec=[D([(424,345),(443,345),(451,377),(433,375)], AU)])
    b.P([(418,387),(465,382),(469,395),(452,405),(420,400)], AU, -15, 15, r=3, L='Magazinboden')
    b.P([(468,272),(526,263),(587,269),(620,286),(609,304),(552,320),(469,313)],
        AU, -18, 18, r=8, L='Handschutz',
        dec=[D([(489,281),(548,275),(582,280),(575,290),(491,298)], HE),
             D([(495,286),(535,282),(534,288),(495,292)], DK)])
    b.C(609, 735, 289, 7, DK, n=12, L='Lauf')
    b.P([(731,277),(760,277),(769,285),(769,296),(760,303),(731,300)],
        AU, -12, 12, r=3, L='Mündungsbremse')
    b.C(760, 772, 289, 8, DK, n=10, L='Mündungsbremse',
        cap=[(289,0,6,HE,False),(289,0,4,DK,False)])
    return b.m


META = dict(
    num='11', name='Scout-Gewehr', nick='KIESELBAND', col=TU,
    pill='TÜRKIS · AUBERGINE · TIEFBLAU', palette=[TU,AU,DK,HE], center=(424,320,0),
    desc='Ein breiter türkisfarbener Kieselschaft umschließt ein echtes Daumenfenster und führt in den flachen Gehäusekörper. '
         'Ein kurzes helles Kastenmagazin sitzt vor dem freien Abzugbügel; der auberginefarbene Handschutz verjüngt sich zum langen Lauf mit Mündungsbremse.',
    form='Offener Kieselschaft mit Wangenauflage · geschwungener Griff · breite ruhige Gehäusefläche · Visierschiene · '
         'Auswurffenster rechts · Ladehebel links · kurzes Kastenmagazin · belüfteter Handschutz · langer Lauf · Mündungsbremse',
    op=dict(
        reload_de='Kurzes Kastenmagazin mit acht Patronen vor dem Abzug wechseln und den Ladehebel links zurückziehen.',
        action_de='Halbautomatik: Nach dem Magazinwechsel spannt der Ladehebel den Verschluss; danach lädt jeder Schuss selbsttätig nach.',
        fire_de='Präzises Einzelfeuer auf Distanz; die Wange liegt auf dem hellen Polster des offenen Schafts.',
        reload_en='Replace the short eight-round box magazine ahead of the trigger and pull the left charging handle back.',
        action_en='Semi-automatic: the handle cocks the bolt after a reload; each shot then cycles the action.',
        fire_en='Precise single shots at range, with the cheek resting on the pale pad of the open stock.'))
