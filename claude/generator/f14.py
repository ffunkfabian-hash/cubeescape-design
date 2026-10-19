"""KF14 Spezial-Granatwerfer „Schwenkbogen“: hoher offener Bogenschaft, tiefes Scharnier und kurzer Kipplauf."""
from eng import circ
from tlib import B, rail, trigger_group

FL, OR, DK, HE = '#B39DE5', '#F27832', '#30233D', '#F4E5CC'


def model():
    b = B()
    D = b.D
    # Ein hoher, nach oben ausgezogener Bogenschaft mit großer echter Öffnung.
    b.P([(95,269),(122,237),(171,221),(222,232),(270,264),(273,287),
         (248,294),(211,265),(169,250),(135,264)], FL, -20, 20, r=9, L='Schaft')
    b.P([(96,267),(125,264),(132,328),(153,361),(142,389),(113,368),(99,326)],
        OR, -20, 20, r=8, L='Schaft')
    b.P([(142,365),(231,358),(266,335),(279,359),(244,388),(146,390)],
        FL, -17, 17, r=7, L='Schaft')
    b.P([(85,268),(100,257),(112,326),(129,368),(119,382),(103,367),(89,317)],
        DK, -23, 23, r=5, L='Schaftkappe')
    b.P([(139,234),(170,218),(207,224),(222,237),(212,247),(171,235),(143,250)],
        HE, -15, 15, r=5, L='Wangenauflage')
    # Die Ersatzgranate liegt links quer zur Halterbacke, klar außerhalb des Bogens.
    b.P([(145,272),(206,272),(218,297),(204,310),(146,306)],
        DK, 20, 29, r=5, L='Granathalter')
    b.C(150, 204, 291, 11, OR, n=10, cz=39, L='Ersatzgranate')
    b.F(204, 223, 291, 11, 3, HE, n=10, cz=39, L='Ersatzgranate')
    b.P([(250,269),(322,250),(389,258),(409,279),(410,325),(381,343),(270,329),(249,310)],
        FL, -24, 24, r=8, L='Gehäuse',
        dec=[D([(277,279),(323,267),(370,272),(379,290),(324,309),(282,304)], OR),
             D([(291,284),(325,277),(347,280),(327,293),(294,297)], HE)])
    rail(b, 270, 370, 258, DK, OR, w=10)
    b.P([(374,254),(388,240),(405,251),(402,264),(384,273)],
        OR, -7, 7, r=3, L='Verriegelungshebel')
    # Achse durch den unteren Laufhaken; das schwere Vorderteil kann darunter abkippen.
    b.P(circ(411,323,13,12), OR, -28, 28, L='Scharnier')
    b.P([(407,297),(436,297),(442,315),(420,334),(407,331)],
        OR, -19, 19, r=4, L='Kipplauf')
    b.C(402, 584, 284, 27, FL, n=12, L='Kipplauf')
    # Breite asymmetrische Seitenwangen lassen die runde Laufnase und die Unterseite frei.
    for z0,z1 in ((21,28),(-28,-21)):
        b.P([(423,269),(474,252),(531,260),(558,277),(551,299),(489,309),(426,298)],
            FL, z0, z1, r=7, L='Kipplauf',
            dec=[D([(445,276),(480,265),(521,272),(527,284),(487,297),(448,289)], OR)] if z0 > 0 else (),
            xdec=[('z-',z0,[(445,276),(480,265),(521,272),(527,284),(487,297),(448,289)],OR,False)]
            if z0 < 0 else ())
    b.C(580, 598, 284, 31, DK, n=12, L='Mündung',
        cap=[(284,0,23,HE,False),(284,0,20,DK,False)])
    b.P([(267,328),(316,336),(311,366),(293,407),(268,419),(247,401),(256,362)],
        OR, -19, 19, r=8, L='Griff',
        dec=[D([(273,348),(298,352),(292,383),(273,401),(261,393)], DK)])
    trigger_group(b, 332, 337, HE, DK, grip_x0=299, depth=35)
    # Der Vordergriff ist eine breite rückwärts geschwungene Flosse, weit vor dem Bügel.
    b.P([(472,307),(522,309),(527,329),(510,372),(491,389),(467,380),(474,343)],
        OR, -18, 18, r=8, L='Vordergriff',
        dec=[D([(485,328),(510,329),(498,364),(483,373)], DK)])
    return b.m


META = dict(
    num='14', name='Spezial-Granatwerfer', nick='SCHWENKBOGEN', col=FL,
    pill='FLIEDER · ORANGE · PFLAUME', palette=[FL,OR,DK,HE], center=(341,319,0),
    desc='Ein hoher fliederfarbener Bogenschaft spannt sich über einer großen offenen Daumenmulde; links trägt er eine einzelne Ersatzgranate. '
         'Der kurze runde Kipplauf sitzt auf einem tiefen orangefarbenen Scharnier, während der zurückgeschwungene Vordergriff die breite Laufnase unterstützt.',
    form='Hoher offener Bogenschaft mit Wangenauflage · Ersatzgranate im Halter links · kurzes Gehäuse · tiefe Visierschiene · '
         'Verriegelungshebel · Kipplauf am tiefen Scharnier · großer Mündungsring · gebogener Vordergriff · freier Abzugbügel',
    op=dict(
        reload_de='Verriegelungshebel nach rechts drücken, Kipplauf am Scharnier nach unten kippen, leere Hülse auswerfen, Granate einsetzen und zuklappen.',
        action_de='Eine Granate je Ladung; die Ersatzgranate im Halter links am Bogenschaft verkürzt den Nachladeweg.',
        fire_de='Die Granate fliegt im Bogen und zündet bei Aufprall oder mit einem zweiten Druck auf den Abzug.',
        reload_en='Push the latch right, tip the barrel down on its hinge, eject the case, insert one grenade and close the barrel.',
        action_en='One grenade per load; the spare on the left side of the arched stock shortens the reload reach.',
        fire_en='The grenade follows an arc and detonates on impact or on a second trigger pull.'))
