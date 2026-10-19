"""KJ13 WHITEOUT: langer offener Schienenbeschleuniger mit abgestuftem Keilheck."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#242D30', '#B9EFF3', '#606C72', '#10171D'


def spec():
    s = [
        K([(57,243),(81,234),(104,244),(104,335),(77,351),(57,340)],
          DK,-18,18,b=4,bz=5,label='Schaftkappe'),
        K([(94,247),(190,258),(233,281),(233,304),(191,302),(94,274)],
          BK,-15,15,b=5,bz=5,label='Schaft',glow=[((0,1,3),IC,3.6)]),
        K([(94,324),(185,309),(231,291),(239,310),(189,334),(94,345)],
          BK,-15,15,b=4,bz=4,label='Schaft'),
        K([(226,258),(387,237),(466,247),(493,270),(493,326),(456,343),(226,330)],
          BK,-25,25,b=7,bz=8,label='Gehäuse',glow=[((0,1,4,5),IC,3.6)],
          dec=[([(258,282),(372,267),(418,276),(402,295),(258,306)],DK,False)]),
        K(rect(275,224,157,39),DK,-11,11,b=2,bz=3,label='Visierschiene',
          dec=[(rect(285+15*i,233,5,3),GM,False) for i in range(9)]),
        K([(489,263),(576,253),(617,267),(617,322),(578,334),(489,326)],
          BK,-23,23,b=5,bz=6,label='Kondensatorkammern',glow=[((0,1,3,4),IC,3.6)],
          dec=[(rect(508+30*i,276,18,32),DK,False) for i in range(3)]+
              [(rect(512+30*i,281,10,22),IC,True) for i in range(3)]),
        # Zwei einzeln benannte Schienen; der Raum um den Linearkern ist offen.
        K([(609,261),(848,249),(893,266),(881,278),(610,278)],
          BK,-12,12,b=3,bz=4,label='Beschleunigerschiene',glow=[((0,1,3),IC,3.6)]),
        K([(610,304),(881,304),(893,316),(848,333),(609,321)],
          BK,-12,12,b=3,bz=4,label='Beschleunigerschiene',glow=[((0,2,3),IC,3.6)]),
        X(610,905,291,5,IC,n=6,emit=True,label='Linearkern'),
    ]
    # Hohlrahmen aus vier Stücken: kein massiver Ring im Strahlkanal.
    for x in (649,741,833):
        s.extend([
            K(rect(x,250,15,13),GM,-19,19,b=2,bz=3,label='Spulenringe'),
            K(rect(x,321,15,13),GM,-19,19,b=2,bz=3,label='Spulenringe'),
            K(rect(x,250,15,84),GM,16,21,b=2,bz=1.5,label='Spulenringe'),
            K(rect(x,250,15,84),GM,-21,-16,b=2,bz=1.5,label='Spulenringe'),
        ])
    s.extend([
        T(884,910,291,25,14,BK,n=8,label='Emitter'),
        X(910,920,291,13,DK,n=8,label='Emitter',cap=[(291,0,7,IC,True)]),
        K([(413,340),(474,334),(490,389),(429,404)],
          BK,-18,18,b=5,bz=5,label='Energiezelle',glow=[((1,2),IC,3.6)],
          dec=[([(435+12*i,352),(441+12*i,351),(450+12*i,380),(444+12*i,382)],IC,True) for i in range(3)]),
        K([(272,330),(316,330),(304,423),(261,429)],DK,-17,17,b=4,bz=5,label='Griff',
          dec=[([(282,352),(302,353),(293,409),(273,412)],GM,False)]),
        K([(335,332),(346,332),(358,363),(346,371)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(311,384),(388,380),(394,391),(310,396)],DK,-7,7,b=2,bz=2),
        K([(384,338),(395,338),(395,391),(384,391)],DK,-7,7,b=2,bz=2),
        K([(545,330),(578,330),(565,400),(540,392)],DK,-14,14,b=4,bz=4,label='Vordergriff'),
    ])
    return s


def model():
    return jlib.model(spec())


META = dict(
    num='13',name='Lineares Fusionsgewehr',nick='WHITEOUT',col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(488.5,326.5,0),
    desc='Ein abgestuftes Keilheck trägt einen langen offenen Schienenbeschleuniger. Drei helle Kondensatorfenster speisen den dünnen '
         'sechskantigen Linearkern; getrennte obere und untere Schienen laufen durch drei hohle Facettenrahmen. Eine schräge schwere Energiezelle sitzt vor dem Abzug.',
    form='Offener Keilschaft · Facettengehäuse · drei Kondensatorkammern · zwei getrennte Beschleunigerschienen · freier Linearkern · '
         'drei offene Spulenringe · Emitter · schräge Energiezelle · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Schwere Energiezelle vor dem Abzug schräg nach unten ziehen, frische Fünf-Schuss-Zelle einsetzen und verriegeln',
        action_de='Abzug halten: Drei Kondensatorkammern laden nacheinander, obere und untere Schiene fahren auseinander',
        fire_de='Nach vollem Aufladen loslassen: Ein einzelner gebündelter Linearstrahl verlässt den Emitter',
        reload_en='pull the heavy energy cell ahead of the trigger down at an angle, insert and lock a fresh five-shot cell',
        action_en='hold the trigger: three capacitor chambers charge in sequence while the upper and lower rails spread apart',
        fire_en='release at full charge to send one focused linear beam through the emitter'))
