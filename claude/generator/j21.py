"""KJ21 „Icevein“: flaches Raketen-Impulsgewehr mit offenem Schaft und kantigem Abgasring."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222C30', '#B2EFF3', '#606C73', '#10171D'


def spec():
    return [
        K([(74,252),(98,242),(112,254),(112,355),(91,368),(74,357)],
          DK,-17,17,b=4,bz=4,label='Schaftkappe'),
        K([(105,250),(206,244),(255,265),(255,284),(200,269),(105,273)],
          BK,-14,14,b=4,bz=4,label='Schaft',glow=[((0,1),IC,3.6)]),
        K([(107,339),(177,320),(238,284),(256,302),(191,344),(107,361)],
          BK,-14,14,b=4,bz=4,label='Schaft',glow=[((1,3),IC,3.6)]),
        K([(248,257),(423,248),(490,265),(503,289),(486,326),
           (421,337),(249,328),(237,310),(237,275)],
          BK,-24,24,b=7,bz=7,label='Gehäuse',glow=[((0,1,4,5),IC,3.6)],
          dec=[([(269,276),(325,272),(339,283),(326,291),(269,293)],GM,False),
               ([(365,276),(414,274),(438,284),(430,294),(365,294)],DK,False)]),
        K(rect(264,241,150,23),DK,-11,11,b=2,bz=3,label='Visierschiene',
          dec=[(rect(276+15*i,249,6,4),GM,False) for i in range(8)]),
        K([(341,287),(364,287),(374,296),(364,305),(341,305)],
          GM,23,36,b=2,bz=3,label='Ladehebel'),
        K([(271,329),(319,331),(306,425),(253,429)],
          DK,-18,18,b=5,bz=5,label='Griff',
          dec=[([(281,349),(308,350),(298,410),(266,414)],GM,False)]),
        K([(338,333),(349,334),(361,365),(350,372)],
          GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(312,386),(399,382),(400,393),(310,397)],DK,-8,8,b=2,bz=2),
        K([(389,333),(400,333),(400,389),(389,389)],DK,-8,8,b=2,bz=2),
        # Das querliegende Magazin sitzt vor dem vollständigen Abzugbügel.
        K([(416,335),(491,326),(505,339),(505,379),(428,391),(416,378)],
          BK,-32,32,b=5,bz=6,label='Raketenmagazin',glow=[((0,2,3),IC,3.6)],
          dec=[([(428,348),(491,339),(493,370),(430,379)],DK,False)]+
              [([(436+11*i,371-1.5*i),(439+11*i,352-1.5*i),(445+11*i,370-1.5*i)],GM,False) for i in range(5)]),
        K([(492,267),(579,260),(622,276),(643,293),(624,315),(494,321)],
          BK,-18,18,b=6,bz=5,label='Handschutz',glow=[((0,1,4),IC,3.6)],
          dec=[([(513+25*i,280),(525+25*i,278),(519+25*i,301),(507+25*i,303)],DK,False) for i in range(4)]),
        K([(538,319),(569,319),(578,376),(554,388),(542,375)],
          DK,-14,14,b=4,bz=4,label='Vordergriff'),
        X(628,728,293,13,GM,n=8,label='Lauf'),
        T(657,678,293,21,15,DK,n=8,label='Abgasring'),
        K([(724,274),(749,274),(761,284),(761,302),(749,312),(724,312)],
          BK,-19,19,b=3,bz=4,label='Mündung',glow=[((0,4),IC,3.2)],
          xdec=[('x+',761,[(284,-9),(284,9),(302,9),(302,-9)],'#060B10',False),
                ('x+',761,[(289,-4),(289,4),(297,4),(297,-4)],IC,True)]),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='21', name='Raketen-Impulsgewehr', nick='ICEVEIN', col=IC,
    pill='POLARNACHT · EISWEISS · GUNMETAL', palette=[BK,IC,GM,DK], center=(417.5,335,0),
    desc='Ein offener Dreieckschaft führt in das lange, flach gebrochene Stealth-Gehäuse. '
         'Das breite querliegende Raketenmagazin vor dem freien Abzugbügel zeigt fünf Raketenspitzen. '
         'Keilhandschutz, Vordergriff und freier Achtkantlauf mit facettiertem Abgasring bilden die lange Front.',
    form='Offener Dreieckschaft · Facettengehäuse · Ladehebel links · eingelassene Visierschiene · '
         'querliegendes Fenster-Raketenmagazin · Griff mit freiem Abzugbügel · Keilhandschutz · Vordergriff · Achtkantlauf mit Abgasring · Mündung',
    op=dict(
        reload_de='Querliegendes Raketenmagazin vor dem Abzug nach unten ziehen, neues mit fünf Raketen einsetzen und Ladehebel links zurückziehen',
        action_de='Jede Abzugbetätigung löst eine Salve aus zwei Raketen aus; Abgase entweichen nach vorn über Handschutz und Abgasring',
        fire_de='Raketensalven mit Explosion beim Aufprall; Spezialmunition mit kleinem Vorrat',
        reload_en='Pull the transverse rocket magazine down ahead of the trigger, insert five fresh rockets and pull the left charging handle',
        action_en='Each trigger pull fires a two-rocket burst; exhaust vents forward through the handguard slots and exhaust ring',
        fire_en='Rocket bursts explode on impact; special ammunition with a small reserve'))
