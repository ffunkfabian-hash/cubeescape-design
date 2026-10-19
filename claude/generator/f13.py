"""KF13 Lineares Fusionsgewehr „Fensterstrom“: offener Tragrahmen, zwei Schienen und drei echte Spulenfenster."""
from eng import rect
from tlib import B, rail, trigger_group

LA, GR, DK, HE = '#F27D92', '#18564A', '#162E2A', '#ECE5C9'


def model():
    b = B()
    D = b.D
    # Tiefer Tragrahmen: langer heller Oberbogen und kurze grüne Unterwiege statt eines Blockschafts.
    b.P([(70,271),(104,246),(181,237),(252,254),(290,283),(268,304),(205,279),(119,284)],
        LA, -21, 21, r=9, L='Schaft')
    b.P([(72,272),(104,279),(117,342),(152,376),(139,399),(100,375),(79,331)],
        GR, -21, 21, r=8, L='Schaft')
    b.P([(138,376),(244,374),(289,344),(303,363),(259,402),(142,401)],
        LA, -17, 17, r=7, L='Schaft')
    b.P([(61,271),(76,262),(90,329),(111,374),(101,387),(83,372),(66,321)],
        DK, -24, 24, r=5, L='Schaftkappe')
    b.P([(111,245),(179,230),(230,242),(236,258),(180,247),(115,263)],
        HE, -16, 16, r=5, L='Wangenauflage')
    b.P([(250,258),(340,243),(457,245),(498,259),(516,288),(495,323),
         (414,342),(286,328),(266,309)], LA, -27, 27, r=10, L='Gehäuse',
        dec=[D([(303,270),(404,259),(464,271),(440,295),(316,300)], GR),
             D([(322,275),(392,267),(400,277),(332,288)], HE)])
    rail(b, 282, 466, 250, DK, GR, w=11)
    # Das Kondensatorpaket trägt drei große Fenster; es endet hinter der freien Schienenstrecke.
    b.P([(495,258),(602,246),(636,265),(636,322),(585,339),(503,321)],
        GR, -25, 25, r=7, L='Kondensatorkammern',
        dec=[D([(511+35*i,274),(533+35*i,270),(533+35*i,311),(511+35*i,315)], HE, True)
             for i in range(3)])
    # Schienen oben/unten sind je ein durchgehendes bewegliches Teil, beide exakt gleich benannt.
    b.P([(631,252),(873,252),(898,267),(898,272),(631,272)],
        LA, -13, 13, r=4, L='Beschleunigerschiene',
        dec=[D([(660,258),(855,258),(870,265),(660,265)], GR)])
    b.P([(631,308),(898,308),(898,313),(873,328),(631,328)],
        LA, -13, 13, r=4, L='Beschleunigerschiene',
        dec=[D([(660,315),(870,315),(855,322),(660,322)], GR)])
    # Ein dünner leuchtender Energiekern, kein materieller Lauf im Strahlkanal.
    b.C(636, 925, 290, 4, HE, n=8, emit=True, L='Linearkern', ch='MT_Energy')
    for x in (672, 760, 848):
        # Freier Ringinnenraum: y=252..328 und z=-22..22, einschließlich des Strahlkanals.
        b.P(rect(x,240,16,12), GR, -28, 28, r=3, L='Spulenringe')
        b.P(rect(x,328,16,12), GR, -28, 28, r=3, L='Spulenringe')
        for z0, z1 in ((22,28),(-28,-22)):
            b.P(rect(x,250,16,80), GR, z0, z1, r=3, L='Spulenringe')
    # Emitter als offener vierteiliger Rahmen statt massivem Kegel im Strahlkanal.
    b.P([(895,254),(924,265),(932,273),(895,273)], DK, -23, 23, r=3, L='Emitter')
    b.P([(895,307),(932,307),(924,315),(895,326)], DK, -23, 23, r=3, L='Emitter')
    for z0,z1 in ((17,23),(-23,-17)):
        b.P([(895,266),(931,271),(931,309),(895,314)], DK, z0, z1, r=3, L='Emitter')
    b.P([(286,325),(343,329),(336,363),(320,405),(295,416),(273,399),(279,359)],
        GR, -20, 20, r=8, L='Griff',
        dec=[D([(295,345),(324,347),(317,381),(298,399),(287,391)], DK)])
    trigger_group(b, 356, 337, HE, DK, grip_x0=324, depth=35)
    # Bügel endet bei x=421; die Energiezelle liegt vollständig davor.
    b.P([(444,334),(502,325),(517,352),(505,399),(470,412),(445,390)],
        GR, -21, 21, r=6, L='Energiezelle',
        dec=[D([(459,349),(489,343),(499,355),(492,388),(472,397),(458,382)], HE, True)])
    b.P([(550,336),(591,336),(594,355),(579,398),(555,399),(544,379)],
        LA, -17, 17, r=7, L='Vordergriff',
        dec=[D([(557,351),(579,351),(574,380),(560,386)], GR)])
    return b.m


META = dict(
    num='13', name='Lineares Fusionsgewehr', nick='FENSTERSTROM', col=LA,
    pill='LACHS · TANNENGRÜN · KREIDE', palette=[LA,GR,DK,HE], center=(496,323,0),
    desc='Der lachsfarbene offene Rahmenschaft trägt einen flachen, breiten Ladeblock mit drei großen hellen Kondensatorfenstern. '
         'Zwei lange Beschleunigerschienen führen durch drei offene grüne Spulenrahmen bis zum ebenfalls offenen Emitter; die schwere Zelle sitzt vor dem freien Abzugbügel.',
    form='Offener Tragrahmen mit Wangenauflage · tiefe Visierschiene · drei Kondensatorkammern · zwei Beschleunigerschienen · '
         'dünner Linearkern · drei offene Spulenringe · offener Emitter · schwere Energiezelle · geschwungener Griff · Vordergriff',
    op=dict(
        reload_de='Schwere Energiezelle vor dem Abzug nach unten entnehmen und eine geladene Zelle für fünf Schüsse einsetzen.',
        action_de='Abzug halten: Drei Kondensatorkammern laden nacheinander, die beiden Schienen fahren auseinander; Ladezeit etwa 0,5 Sekunden.',
        fire_de='Nach voller Ladung loslassen: Ein einzelner durchschlagender Linearstrahl tritt durch den offenen Emitter aus.',
        reload_en='Pull the heavy cell ahead of the trigger down and insert a charged cell holding five shots.',
        action_en='Hold the trigger: three capacitor chambers charge in sequence and both rails spread apart, taking about 0.5 seconds.',
        fire_en='Release at full charge to send one piercing linear beam through the open emitter.'))
