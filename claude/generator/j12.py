"""KJ12 NIGHTFANG: kompakter Facettenrevolver mit vorgezogenem Fangzahn-Laufmantel."""
import math
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222A30', '#B4F2F5', '#626D73', '#10161C'


def spec():
    return [
        K([(205,301),(260,301),(278,322),(255,424),(203,439),(185,421)],
          DK,-18,18,b=5,bz=5,label='Griff',
          dec=[([(211,327),(252,323),(238,408),(204,419)],GM,False)]),
        K([(208,260),(233,244),(295,244),(295,310),(253,321),(208,301)],
          BK,-19,19,b=5,bz=6,label='Rahmen',glow=[((0,1,4),IC,3.6)]),
        K([(282,234),(383,234),(404,246),(397,258),(282,258)],
          BK,-18,18,b=4,bz=5,label='Oberbrücke',glow=[((0,1),IC,3.6)]),
        K([(383,250),(407,250),(407,311),(383,311)],BK,-18,18,b=4,bz=4,label='Rahmen'),
        K([(289,305),(389,305),(389,322),(285,322)],BK,-15,15,b=3,bz=4,label='Unterbrücke'),
        X(299,380,282,29,GM,n=8,label='Trommel',
          cap=[(282+18*math.cos(k*math.pi/3),18*math.sin(k*math.pi/3),6,'#05090C',False) for k in range(6)]),
        K([(303,273),(375,273),(375,291),(303,291)],BK,25,30,b=2,bz=2,label='Trommel',glow=[((0,2),IC,3.6)]),
        K([(303,273),(375,273),(375,291),(303,291)],BK,-30,-25,b=2,bz=2,label='Trommel',glow=[((0,2),IC,3.6)]),
        K([(251,281),(276,281),(283,290),(275,298),(251,298)],
          GM,18,27,b=2,bz=2,label='Trommelriegel'),
        K([(221,246),(229,221),(247,218),(261,239),(249,248)],
          GM,-6,6,b=2,bz=2,label='Hahn'),
        K(rect(292,229,82,14),DK,-10,10,b=2,bz=2,label='Visierschiene',
          dec=[(rect(301+13*i,234,5,3),GM,False) for i in range(5)]),
        # Das obere Trommellager und die Laufachse liegen auf y=264.
        K([(399,244),(524,237),(573,253),(580,275),(557,300),(400,300)],
          BK,-18,18,b=5,bz=6,label='Laufmantel',glow=[((0,1,3,4),IC,3.6)],
          dec=[([(423+27*i,254),(438+27*i,253),(434+27*i,272),(419+27*i,273)],DK,False) for i in range(4)]),
        X(569,594,264,11,GM,n=6,label='Lauf',cap=[(264,0,6,'#05090C',False)]),
        X(381,516,308,4,DK,n=6,label='Ausstoßerstange'),
        K([(510,297),(524,297),(524,315),(510,315)],GM,-7,7,b=2,bz=2),
        K([(304,322),(315,322),(325,349),(314,356)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(265,367),(348,361),(355,371),(263,379)],DK,-7,7,b=2,bz=2),
        K([(348,320),(359,320),(359,371),(348,371)],DK,-7,7,b=2,bz=2),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='12',name='Handfeuerwaffe',nick='NIGHTFANG',col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(389.5,328.5,0),
    desc='Ein vorgezogener Fangzahn-Laufmantel sitzt vor dem offenen Revolverrahmen. Die achteckige Trommel trägt sechs Kammern; '
         'Hahn und Trommelriegel bleiben als getrennte Bedienteile sichtbar. Der stark geneigte Griff und der freie Abzugsbereich bilden die Hecksilhouette.',
    form='Facettenrahmen mit Ober- und Unterbrücke · achteckige Sechskammertrommel · Trommelriegel links · Hahn · '
         'Fangzahn-Laufmantel · Ausstoßerstange · geneigter Griff · Visierschiene',
    op=dict(
        reload_de='Trommelriegel drücken, Trommel nach links schwenken, sechs Patronen laden und Trommel wieder verriegeln',
        action_de='Double Action: Der Abzug spannt den Hahn und dreht die Trommel um eine Kammer weiter',
        fire_de='Ein großkalibriger Einzelschuss je Abzug; der schwere Laufmantel dämpft das Hochschlagen',
        reload_en='press the cylinder latch, swing the cylinder left, load six rounds and lock the cylinder back in place',
        action_en='double action: the trigger cocks the hammer and indexes the cylinder by one chamber',
        fire_en='one heavy single shot per pull; the weighted barrel shroud reduces muzzle rise'))
