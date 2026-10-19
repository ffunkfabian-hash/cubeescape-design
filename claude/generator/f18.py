"""KF18 GABELKRONE: Glefe mit offener Doppelzinkenklinge und breiten Schildflügeln.

Der Emitter liegt frei zwischen den Klingenholmen. Der hintere Daumenrahmen und der
vordere Ringgriff sind echte Durchgriffe; beide Schildflügel besitzen dasselbe exakte Label.
"""
from eng import rect
from tlib import B, grip, trigger_group

SM, HI, DK, HE = '#159B72', '#DC3B78', '#132B2D', '#E5EDCF'


def model():
    b = B()
    D = b.D
    b.C(62,90,298,17,HI,n=8,L='Knauf',cap=[(298,0,7,HE,False)])
    b.C(90,646,298,10,DK,n=8,L='Stange')
    # Geknickter rückwärtiger Handrahmen: nicht mit einer ausgefüllten Schaftplatte verschlossen.
    b.P([(86,284),(103,282),(113,393),(101,409),(87,393)],SM,-16,16,r=6)
    b.P([(101,391),(159,391),(175,404),(159,420),(101,412),(94,404)],SM,-16,16,r=6)
    b.P([(151,278),(247,274),(279,292),(277,320),(154,325)],
        SM,-19,19,r=6,L='Gehäuse',
        dec=[D([(174,287),(237,285),(258,297),(176,302)],HE,True)])
    grip(b,151,321,DK,SM,h=94,w=54,lean=17,z=17)
    trigger_group(b,213,322,HI,DK,grip_x0=193,depth=34)
    # Vorderer Ringgriff lässt x=416..473, y=338..367 frei.
    b.P([(389,303),(483,303),(504,327),(484,338),(398,332)],HI,-16,16,r=6,L='Vordergriff')
    b.P([(389,323),(410,326),(419,376),(399,388),(389,367)],HI,-16,16,r=6,L='Vordergriff')
    b.P([(481,326),(502,323),(500,376),(483,391),(471,377)],HI,-16,16,r=6,L='Vordergriff')
    b.P([(402,371),(482,371),(494,384),(480,397),(404,392),(394,381)],HI,-16,16,r=6,L='Vordergriff')
    b.P([(555,277),(616,274),(635,287),(632,311),(615,323),(555,320)],
        SM,-18,18,r=6,L='Energiezelle',
        dec=[D([(568,287),(612,285),(619,298),(608,312),(568,309)],HE,True)])
    b.P([(632,264),(664,257),(683,276),(683,324),(660,339),(632,329)],
        DK,-21,21,r=5,L='Klingenfassung')
    # Spiegelbildliche breite Schwingflügel, jeweils an der seitlichen Wurzel gefasst.
    for sign in (-1,1):
        b.Y([(x,z*sign) for x,z in [(638,19),(667,19),(679,56),(655,97),
                                   (626,105),(619,89),(644,63)]],
            HI,272,326,r=3,L='Schildflügel',
            dec=[D([(642,35*sign),(656,35*sign),(663,55*sign),
                    (648,83*sign),(634,89*sign),(652,58*sign)],HE)])
    # Die breite Krone hat zwei getrennte Zinken und eine offene Bahn für den Emitter.
    b.P([(666,264),(780,226),(886,248),(944,276),(942,284),
         (916,280),(870,271),(782,262),(680,288)],SM,-5,5,r=3,L='Klinge',
        dec=[D([(710,263),(781,239),(868,256),(871,266),(783,252),(713,275)],HE)])
    b.P([(666,312),(782,312),(874,310),(924,310),(944,314),
         (938,323),(883,337),(783,351),(666,336)],SM,-5,5,r=3,L='Klinge',
        dec=[D([(682,327),(782,339),(881,327),(931,316),(936,317),
                 (883,333),(783,346),(682,333)],HI,True)])
    b.C(666,928,298,5,DK,n=8,L='Emitter')
    b.F(928,945,298,5,2,HE,n=8,emit=True)
    return b.m


META = dict(
    num='18', name='Glefe', nick='GABELKRONE', col=SM,
    pill='SMARAGD · HIMBEERE · KREIDE', palette=[SM,HI,DK,HE], center=(503,312,0),
    desc='Eine offene smaragdgrüne Doppelzinkenklinge führt oberhalb und unterhalb der freien Emitterbahn bis zu zwei getrennten Spitzen. '
         'Breite himbeerfarbene Schildflügel sitzen beidseitig an der Klingenfassung; die Energiezelle liegt direkt dahinter. '
         'Ein tiefer Daumenrahmen mit freiem Abzug und ein großer vorderer Ringgriff geben der langen Stange zwei klare Handpositionen.',
    form='Lange Stange mit Knauf · tiefer Daumenrahmen mit Griff und Abzugbügel · offener Ringvordergriff · '
         'Energiezelle · Klingenfassung · zwei breite Schildflügel · offene Doppelzinkenklinge mit Schneide · freier Emitter',
    op=dict(
        reload_de='Nahkampftreffer laden die Energiezelle vor der Klingenfassung; zum Nachladen die Zelle drehen und für vier Schüsse neu einrasten.',
        action_de='Der Abzug löst ein Energiegeschoss aus dem Emitter; beim Blocken klappen beide Schildflügel zum Schild vor der Klinge aus.',
        fire_de='Klingenhiebe und Fernschüsse aus der Hüfte; der aufgebaute Schild fängt Treffer ab.',
        reload_en='Melee hits recharge the cell behind the blade mount; twist and relock the cell to reload four shots.',
        action_en='The trigger fires an energy bolt from the emitter; guarding unfolds both shield wings into a shield ahead of the blade.',
        fire_en='Blade swings and ranged shots fired from the hip; the deployed shield absorbs incoming hits.'))
