"""KJ15 GLACIERMAW: tiefe Sechskant-Drehtrommel unter einem abgewinkelten Rücken."""
import math
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#232C30', '#BBF1F4', '#626D73', '#10171C'


def spec():
    return [
        K([(26,231),(48,223),(66,234),(66,346),(44,361),(26,349)],
          DK,-19,19,b=4,bz=5,label='Schaftkappe'),
        K([(57,236),(158,249),(198,272),(198,300),(145,291),(57,266)],
          BK,-17,17,b=5,bz=5,label='Schaft',glow=[((0,1,3),IC,3.6)]),
        K([(57,334),(145,309),(191,286),(202,307),(151,335),(57,354)],
          BK,-17,17,b=4,bz=5,label='Schaft',glow=[((0,3),IC,3.0)]),
        K([(189,259),(263,238),(307,252),(307,352),(189,345)],
          BK,-27,27,b=6,bz=8,label='Gehäuse',glow=[((0,1,3),IC,3.6)],
          dec=[([(209,275),(260,261),(285,270),(282,285),(209,299)],DK,False)]),
        K([(245,301),(293,301),(293,335),(245,335)],GM,26,34,b=3,bz=2,label='Ladeklappe',
          dec=[(rect(255,310,28,5),DK,False)]),
        # Sechs Kammern im achteckigen Trommelkörper; obere Kammer y=264.
        X(307,433,300,59,BK,n=8,label='Granattrommel',
          cap=[(300-36*math.cos(k*math.pi/3),36*math.sin(k*math.pi/3),13,'#05090C',False) for k in range(6)]),
        X(322,332,300,61,GM,n=8,label='Granattrommel'),
        X(406,416,300,61,GM,n=8,label='Granattrommel'),
        K(rect(338,281,62,38),BK,53,59,b=3,bz=2,label='Granattrommel',glow=[((0,1,2,3),IC,3.6)]),
        K(rect(338,281,62,38),BK,-59,-53,b=3,bz=2,label='Granattrommel',glow=[((0,1,2,3),IC,3.6)]),
        X(286,455,300,8,DK,n=6,label='Trommelachse'),
        K([(297,230),(407,218),(450,234),(450,247),(297,247)],
          BK,-19,19,b=3,bz=5,label='Oberbrücke',glow=[((0,1,3),IC,3.6)]),
        K(rect(315,208,91,29),DK,-10,10,b=2,bz=2,label='Visierschiene',
          dec=[(rect(323+13*i,215,5,3),GM,False) for i in range(6)]),
        K([(433,237),(459,237),(472,257),(463,322),(433,322)],
          BK,-25,25,b=4,bz=6,label='Laufträger',glow=[((1,2,3),IC,3.0)]),
        X(460,627,264,23,DK,n=6,label='Lauf'),
        K([(468,238),(584,232),(620,249),(608,260),(468,257)],
          BK,-16,16,b=3,bz=4,label='Lauf',glow=[((0,1,3),IC,3.6)]),
        K([(469,280),(608,280),(621,294),(585,309),(469,298)],
          BK,-16,16,b=3,bz=4,label='Lauf',glow=[((0,2,3),IC,3.6)]),
        X(622,647,264,29,GM,n=8,label='Mündung',cap=[(264,0,19,'#05090C',False)]),
        K([(199,342),(242,342),(229,429),(187,436)],DK,-17,17,b=4,bz=5,label='Griff',
          dec=[([(208,364),(229,366),(219,415),(198,420)],GM,False)]),
        K([(260,349),(271,349),(282,374),(271,382)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(236,396),(294,391),(302,402),(235,408)],DK,-7,7,b=2,bz=2),
        K([(290,351),(302,351),(302,402),(290,402)],DK,-7,7,b=2,bz=2),
        K([(487,303),(522,303),(511,374),(485,369)],DK,-14,14,b=4,bz=4,label='Vordergriff'),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='15',name='Schwerer Granatwerfer',nick='GLACIERMAW',col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(336.5,322,0),
    desc='Eine breite achteckige Granattrommel hängt unter einer ansteigenden Rückenbrücke. Der hohe offene Schaft und das kurze '
         'keilförmige Laufmaul geben dem schweren Werfer eine tiefe Silhouette. Sechs Kammern liegen um die Trommelachse; der Lauf fluchtet mit der oberen Kammer.',
    form='Hoher Keilschaft · Heckgehäuse mit Ladeklappe links · achteckige Sechskammertrommel · Trommelachse · '
         'steigende Oberbrücke · Laufträger · kurzes Laufmaul · Mündung · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Linke Ladeklappe öffnen, Trommel Kammer für Kammer weiterdrehen, sechs Granaten einsetzen und Klappe schließen',
        action_de='Das Federwerk der Trommelachse dreht die Granattrommel nach jedem Schuss um genau eine Kammer weiter',
        fire_de='Sechs schwere Granaten nacheinander; der Lauf feuert jeweils aus der oberen Trommelkammer',
        reload_en='open the left loading gate, index the drum chamber by chamber, insert six grenades and close the gate',
        action_en='the spring mechanism in the axle indexes the grenade drum by one chamber after each shot',
        fire_en='fire six heavy grenades in succession through the upper drum chamber'))
