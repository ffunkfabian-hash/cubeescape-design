"""KF24 Mikroraketen-Granatwerfer „Rückenflosse“: hoch getragener Rohrkörper und tiefer offener Schaft.

Einseitiger Raketenvorrat links wie G24, aber keilförmig an der hinteren Flanke.
Der Ladezugang bleibt vor der kurzen hinteren Visierschiene frei.
"""
from eng import rect, roundpoly, circ
from tlib import B, grip, rail, trigger_group

LI, AZ, DK, HE = '#B9CC58', '#3B69B3', '#273344', '#F0E7CC'
AX = 270


def model():
    b = B()
    D = b.D
    # Drei verbundene Bänder um ein großes reales Schaftfenster.
    b.P([(84,258),(115,250),(154,279),(142,363),(120,388),(93,373)],
        AZ,-18,18,r=8,L='Schaft')
    b.P([(114,251),(249,237),(283,249),(283,279),(150,287)],
        LI,-17,17,r=8,L='Schaft',
        dec=[D([(151,262),(242,250),(263,258),(153,275)],HE)])
    b.P([(125,365),(256,366),(293,346),(309,368),(273,396),(112,391)],
        AZ,-15,15,r=8,L='Schaft')
    b.P([(76,257),(90,253),(106,374),(95,388),(81,378)],
        DK,-20,20,r=5,L='Schaftkappe')
    # Gestufte obere Kontur, über der Ladeklappe keine eigene Visierung.
    b.P([(249,235),(350,235),(376,247),(457,247),(488,269),(473,307),
         (436,326),(400,312),(249,312)],
        LI,-24,24,r=8,L='Gehäuse',
        dec=[D([(405,278),(458,275),(463,291),(434,310),(408,301)],AZ)])
    rail(b,256,337,238,DK,AZ,w=10)
    b.P([(354,232),(435,232),(451,242),(445,251),(354,251)],
        AZ,-17,17,r=4,L='Ladeklappe',
        dec=[D(roundpoly(rect(373,237,54,6),2),HE)])
    b.P(circ(356,245,7,12),DK,-20,20,L='Ladeklappenscharnier')
    # Breiter, schräg auslaufender Vorratskasten links; rechts bleibt die Grundschale klar.
    b.P([(271,268),(366,260),(391,277),(382,315),(283,328),(266,307)],
        AZ,24,56,r=7,L='Raketenvorrat',
        dec=[D(roundpoly([(283,277),(360,269),(377,280),(370,306),(286,318)],4),DK)]
            +[D([(288,281+9*i),(347,275+9*i),(359,278+9*i),
                 (348,281+9*i),(288,287+9*i)],HE) for i in range(4)]
            +[D([(348,275+9*i),(367,278+9*i),(348,281+9*i)],LI) for i in range(4)])
    # Leicht konisches Rohr endet weiter vorne; die große Oberfinne sitzt auf dem Rohr statt zu schweben.
    b.C(469,758,AX,16,HE,n=12,L='Abschussrohr')
    for i,x in enumerate((484,596,714)):
        b.C(x,x+16,AX,22,AZ,n=12,L='Leitring')
    b.P([(485,249),(531,223),(658,238),(720,249),(720,255),(485,255)],
        LI,-6,6,r=5,L='Rohrsteg',
        dec=[D([(538,232),(649,243),(663,248),(530,243)],AZ)])
    b.F(758,784,AX,16,23,AZ,n=12,L='Mündung')
    b.C(784,792,AX,23,DK,n=12,
        cap=[(AX,0,15,DK,False),(AX,0,6,LI,False)])
    grip(b,266,311,DK,AZ,h=99,w=54,lean=20,z=18)
    trigger_group(b,337,312,HE,DK,grip_x0=309,depth=40)
    # Der lange Vordergriff bildet einen schrägen Haken, ohne die Leitringe zu schneiden.
    b.P([(621,283),(656,283),(662,308),(641,359),(621,367),(609,351)],
        AZ,-14,14,r=7,L='Vordergriff',
        dec=[D([(629,300),(646,300),(635,342),(623,347)],DK)])
    return b.m


META = dict(
    num='24', name='Mikroraketen-Granatwerfer', nick='RÜCKENFLOSSE', col=LI,
    pill='LIMETTE · AZUR · TINTE', palette=[LI,AZ,DK,HE], center=(434,322,0),
    desc='Ein hoher limettenfarbener Rückensteg verbindet die Leitringe des schlanken Abschussrohrs. '
         'Das tiefe offene Schaftheck und der azurblaue Hakengriff prägen die Unterkante; links steckt der Vorrat von vier Mikroraketen in einem geneigten Seitenkasten.',
    form='Tiefer offener Bandschaft · gestufte Gehäuseschale · Ladeklappe oben · keilförmiger Raketenvorrat links · '
         'langes Abschussrohr mit drei Leitringen und Rückensteg · Hakenvordergriff',
    op=dict(
        reload_de='Ladeklappe vor der Schiene nach hinten öffnen, eine Mikrorakete aus dem linken Seitenkasten ins Lager legen, Klappe schließen.',
        action_de='Eine Rakete im Rohr; nach jedem Schuss neu laden. Der Raketenmotor zündet erst vor der Mündung.',
        fire_de='Schnelle Mikrorakete auf gerader Bahn mit Aufprallzünder; Spezialmunition, kein bogenförmiger Granatflug.',
        reload_en='Open the gate ahead of the rail to the rear, place one micro-missile from the left reserve box into the chamber, close the gate.',
        action_en='One missile in the tube; reload after each shot. The rocket motor ignites just past the muzzle.',
        fire_en='Fast micro-missile on a straight path with an impact fuse; special ammunition, no arcing grenade flight.'))
