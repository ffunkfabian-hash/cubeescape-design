"""KJ25 BLACKSQUALL: facettierter Kipprahmen-Revolver mit flacher Fächermündung."""
import math
from eng import rect
import jlib
from jlib import K, X

BK, IC, GM, DK = '#242D30', '#B8ECF2', '#606A6E', '#10161C'
AXC, BX = 286, 267


def spec():
    return [
        K([(230,319),(286,319),(281,359),(265,442),(225,458),(210,435)],
          BK,-19,19,b=6,bz=6,label='Griff',glow=[((3,4),IC,3.6)],
          dec=[([(236,346),(267,341),(252,423),(228,434),(224,421)],DK,False)]),
        K([(219,278),(245,257),(283,260),(299,281),(299,329),(237,340),(218,322)],
          BK,-18,18,b=5,bz=6,label='Rahmen',glow=[((0,1,4),IC,3.6)]),
        K([(285,317),(415,317),(430,327),(418,339),(285,339)],
          BK,-16,16,b=4,bz=4,label='Rahmen',glow=[((0,2),IC,3.2)]),
        K([(223,266),(241,237),(264,229),(284,250),(278,270)],
          DK,-13,13,b=4,bz=4,label='Hahnschutz',glow=[((0,1),IC,3.0)]),
        K([(411,316),(428,316),(436,325),(428,334),(411,334),(403,325)],
          GM,-22,22,b=3,bz=4,label='Scharnier'),
        # Oberbrücke und vorderes Joch sind dieselbe bewegliche Baugruppe.
        K([(283,237),(394,226),(433,242),(433,259),(396,247),(283,255)],
          BK,-17,17,b=4,bz=5,label='Kipprahmen',glow=[((0,1,4),IC,3.6)]),
        K([(408,251),(433,251),(433,319),(420,330),(404,317),(404,298)],
          BK,-17,17,b=4,bz=5,label='Kipprahmen',glow=[((1,3),IC,3.0)],
          dec=[(rect(416,270,7,34),GM,False)]),
        K([(270,241),(284,229),(301,238),(290,253)],GM,-8,8,b=2,bz=2,label='Kippriegel'),
        K(rect(306,210,83,36),DK,-9,9,b=2,bz=3,label='Visierschiene',
          dec=[(rect(314+13*i,217,5,4),GM,False) for i in range(5)]),
        # Achtkantige Trommel, fünf ebenfalls polygonale Schrotkammern.
        X(302,394,AXC,34,BK,n=8,label='Trommel',
          cap=[(AXC-19*math.cos(2*k*math.pi/5),19*math.sin(2*k*math.pi/5),7.5,GM,False)
               for k in range(5)]+
              [(AXC-19*math.cos(2*k*math.pi/5),19*math.sin(2*k*math.pi/5),4.5,'#05090C',False)
               for k in range(5)]),
        X(298,408,AXC,5,DK,n=8,label='Achsstift'),
        K([(313,273),(380,273),(386,281),(380,287),(313,287)],
          DK,30,35,b=2,bz=1.5,label='Trommel',glow=[((0,3),IC,3.0)]),
        K([(313,273),(380,273),(386,281),(380,287),(313,287)],
          DK,-35,-30,b=2,bz=1.5,label='Trommel',glow=[((0,3),IC,3.0)]),
        X(427,504,BX,11,GM,n=6,label='Lauf'),
        K([(431,248),(485,248),(507,256),(507,261),(431,261)],
          BK,-9,9,b=2,bz=3,label='Laufschiene',glow=[((0,1),IC,3.0)]),
        K([(496,254),(517,254),(528,262),(528,274),(517,280),(496,280)],
          DK,-19,19,b=3,bz=4,label='Streumündung'),
        K([(520,250),(563,250),(582,258),(582,276),(563,284),(520,284)],
          BK,-35,35,b=3,bz=5,label='Streumündung',glow=[((0,4),IC,3.6)],
          dec=[([(533,263),(562,262),(570,266),(562,271),(533,271)],DK,False)],
          xdec=[('x+',582,[(262,-26),(262,26),(272,26),(272,-26)],'#05090C',False)]+
               [('x+',582,[(265,z-2),(265,z+2),(269,z+2),(269,z-2)],IC,True) for z in (-16,0,16)]),
        K([(314,338),(326,338),(338,370),(326,377)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(270,392),(371,381),(380,391),(270,403)],DK,-7,7,b=2,bz=2),
        K([(370,339),(380,339),(380,391),(370,391)],DK,-7,7,b=2,bz=2),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='25',name='Streuschuss-Handfeuerwaffe',nick='BLACKSQUALL',col=IC,
    pill='NACHTSCHIEFER · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(396.0, 334.0, 0),
    desc='Eine tief geneigte Griffkeilfläche, ein hochgezogener Hahnschutz und die nach vorn abfallende Oberbrücke prägen diesen Black-Ice-Revolver. '
         'Seine achtkantige Trommel trägt fünf Schrotkammern; Der kurze Lauf liegt auf der obersten Kammerachse und endet in einer breiten, '
         'flachen Fächermündung mit Querschlitz. Lauf, Trommel und Brücke kippen gemeinsam um das vordere untere Scharnier.',
    form='Facettenrahmen · verdeckter Hahn unter Hahnschutz · Kipprahmen mit Oberbrücke und Joch · Kippriegel · '
         'Achtkant-Trommel mit fünf Schrotkammern · vorderes unteres Scharnier · kurzer Sechskantlauf · breite flache Streumündung · Griff',
    op=dict(
        reload_de='Kippriegel drücken, Lauf und Trommel am vorderen Scharnier abkippen; Auswerfer hebt fünf Hülsen, Schrotpatronen einsetzen und zuklappen',
        action_de='Double Action: Der verdeckte Hahn spannt und die Trommel dreht bei jedem Abzug um eine der fünf Kammern weiter',
        fire_de='Kurzer, flach gefächerter Streuschuss aus Schrotkugeln; langsame Feuerrate, wirksam auf kurze Distanz',
        reload_en='press the latch, tip barrel and cylinder down at the front hinge; eject five shells, insert shot cartridges and close',
        action_en='double action: every pull cocks the shrouded hammer and indexes the cylinder by one of five chambers',
        fire_en='a short, flat fan of pellets; slow rate of fire, effective at close range'))
