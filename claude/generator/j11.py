"""KJ11 „Rimewing“: langes Scout-Gewehr aus breiten Stealth-Facetten mit echtem Lochschaft."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222B30', '#9CE5EB', '#626D73', '#10161C'


def spec():
    return [
        # Drei getrennte Stege bilden ein echtes offenes Schaftfenster.
        K([(68,249),(92,239),(111,248),(111,353),(88,364),(68,350)],
          DK,-16,16,b=4,bz=4,label='Schaftkappe'),
        K([(103,248),(222,242),(262,259),(262,282),(216,268),(103,272)],
          BK,-13,13,b=5,bz=5,label='Schaft',glow=[((0,),IC,2.8)]),
        K([(103,336),(174,321),(245,284),(265,299),(188,342),(104,357)],
          BK,-13,13,b=4,bz=4,label='Schaft'),
        K([(124,239),(203,235),(222,243),(216,253),(124,257)],
          GM,-10,10,b=3,bz=3,label='Wangenauflage'),
        # Langer flacher Jet-Flügel statt des hohen G-Gehäuses.
        K([(254,253),(430,244),(493,256),(529,274),(518,303),
           (450,319),(254,319),(242,303),(242,269)],
          BK,-21,21,b=7,bz=8,label='Gehäuse',glow=[((0,1),IC,3.4)],
          dec=[([(290,276),(366,273),(380,281),(368,288),(290,290)],DK,False),
               ([(394,280),(447,279),(474,290),(398,292)],GM,False)]),
        # Die Unterkante greift in die schräge Gehäuseoberseite.
        K(rect(275,237,153,22),DK,-10,10,
          b=2,bz=2,label='Visierschiene',
          dec=[(rect(286+14*i,246,5,3),GM,False) for i in range(9)]),
        K([(337,282),(359,282),(369,290),(359,299),(337,299)],
          GM,20,33,b=2,bz=3,label='Ladehebel'),
        K([(274,319),(320,319),(308,411),(263,418)],
          DK,-17,17,b=5,bz=5,label='Griff',
          dec=[([(283,340),(302,339),(295,391),(275,398)],GM,False)]),
        K([(336,321),(347,321),(358,350),(347,355)],
          GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(311,371),(384,365),(390,374),(312,381)],DK,-7,7,b=2,bz=2),
        K([(382,319),(392,319),(392,374),(382,374)],DK,-7,7,b=2,bz=2),
        # Das schräg vorgesetzte Magazin bleibt deutlich vor dem Abzugbügel.
        K([(420,319),(465,315),(484,375),(443,389)],
          BK,-13,13,b=4,bz=5,label='Magazin',glow=[((1,),IC,3.0)],
          dec=[([(434,333),(453,329),(466,368),(449,374)],DK,False)]),
        K([(440,382),(484,368),(490,379),(446,394)],
          GM,-14,14,b=2,bz=3,label='Magazinboden'),
        # Kurzer, keilförmiger Handschutz: der lange Sechskantlauf bleibt sichtbar.
        K([(518,264),(592,260),(642,270),(664,282),(642,302),(518,307)],
          BK,-14,14,b=5,bz=5,label='Handschutz',glow=[((0,1),IC,2.8)],
          dec=[([(540,280),(574,275),(564,292),(532,297)],DK,False),
               ([(587,274),(614,278),(605,292),(578,294)],DK,False)]),
        X(650,826,282,7,GM,n=6,label='Lauf'),
        X(662,677,282,10,DK,n=8,label='Laufbund'),
        T(820,836,282,11,14,BK,n=6,label='Mündungsbremse'),
        K([(832,270),(861,270),(877,278),(877,286),(861,294),(832,294)],
          DK,-12,12,b=3,bz=3,label='Mündungsbremse',
          dec=[(rect(840+8*i,278,4,8),GM,False) for i in range(3)],
          xdec=[('x+',877,[(277,-4),(277,4),(287,4),(287,-4)],'#06090C',False)]),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='11', name='Scout-Gewehr', nick='RIMEWING', col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL', palette=[BK,IC,GM,DK], center=(472.5,326.5,0),
    desc='Ein flaches, flügelartig gebrochenes Gehäuse und ein offener Dreieckschaft prägen dieses Scout-Gewehr der Black-Ice-Serie. '
         'Vor dem kurzen Keilhandschutz liegt ein langer gezogener Sechskantlauf; das geneigte Kastenmagazin sitzt vor dem freien Abzugbügel. '
         'Raueisfarbene Leuchtkanten markieren nur die oberen Facetten.',
    form='Offener Dreieck-Lochschaft · Wangenauflage · flaches Facettengehäuse · Ladehebel links · '
         'geneigtes Kastenmagazin · Keilhandschutz · langer gezogener Sechskantlauf · Mündungsbremse · Visierschiene',
    op=dict(
        reload_de='Kastenmagazin vor dem Abzug schräg nach unten abziehen, neues Acht-Schuss-Magazin einsetzen, Ladehebel links ziehen',
        action_de='Halbautomatik: Nach dem Laden Ladehebel zurückziehen und freigeben; der Verschluss führt die erste Patrone zu',
        fire_de='Ein gezielter Einzelschuss je Abzug; die Wangenauflage am offenen Schaft stabilisiert den Anschlag',
        reload_en='pull the box magazine down at an angle, insert a fresh eight-round magazine, pull the left charging handle',
        action_en='semi-automatic: pull and release the charging handle after loading; the bolt chambers the first round',
        fire_en='one precise shot per pull; the cheek rest on the open stock supports a steady aim'))
