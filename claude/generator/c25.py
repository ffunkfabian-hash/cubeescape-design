"""KC25 „Muschelhieb“: ein muschelförmig gewölbter Kipprahmen mit flacher Fächermündung."""
import math
from eng import rect, roundpoly, circ
from tlib import B, rail, trigger_group

MA, FL, PF, DK = '#237965', '#B795CA', '#FFB59A', '#1C2A29'
AXC, AX = 284, 263


def model():
    b = B()
    D = b.D
    b.P([(235,305),(286,308),(301,347),(280,398),(246,443),
         (216,448),(202,437),(230,399),(251,348)], MA,-21,21,r=10,L='Griff',
        dec=[D(roundpoly([(244,337),(268,338),(278,353),(257,403),
                          (228,432),(239,399),(259,351)],6),FL)])
    # Vier Einheiten Luft unter der Trommel lassen die Kippgruppe frei laufen.
    b.P([(221,264),(258,249),(298,250),(313,272),(304,323),
         (447,323),(461,331),(435,343),(282,334),(232,320)],MA,-22,22,r=8,L='Rahmen')
    b.P([(241,247),(258,231),(292,227),(312,242),(303,256),(272,250)],
        DK,-13,13,r=8,L='Hahnschutz')
    # Das obere Muschelprofil bildet eine breite gewölbte Brücke um die freie Trommel.
    b.P([(291,246),(305,226),(334,216),(374,216),(414,225),
         (450,238),(484,249),(493,266),(478,279),(457,261),
         (442,242),(417,236),(374,237),(338,237),(307,255)],FL,-19,19,r=9,L='Kipprahmen',
        dec=[D(roundpoly([(309,237),(337,224),(375,224),(411,232),
                          (449,246),(459,253),(412,232),(375,228),(339,228),(312,244)],3),PF,True)])
    b.P([(444,252),(477,257),(482,278),(466,320),(442,321)],
        FL,-20,20,r=9,L='Kipprahmen',
        dec=[D(roundpoly([(455,267),(466,271),(458,308),(449,307)],4),MA)])
    b.P(circ(451,324,12,16),DK,-25,25,L='Scharnier',
        dec=[D(circ(451,324,6,12),PF)])
    b.P([(286,238),(301,222),(318,227),(314,242),(297,252)],
        PF,-7,7,r=6,L='Kippriegel')
    # Eigener Schienensockel greift in die gewölbte Brücke.
    b.P([(335,207),(407,207),(410,232),(373,229),(335,231)],
        MA,-12,12,r=6,L='Schienensockel')
    rail(b,340,402,208,DK,FL,w=10)
    b.C(319,434,AXC,35,MA,n=20,L='Trommel',
        cap=[(AXC-21*math.cos(2*k*math.pi/5),21*math.sin(2*k*math.pi/5),9,PF,False)
             for k in range(5)]+
            [(AXC-21*math.cos(2*k*math.pi/5),21*math.sin(2*k*math.pi/5),5,DK,False)
             for k in range(5)])
    # Fünf lange Muschelrippen liegen als Aufkleber auf der Trommel, keine Vollkörper im Kammerraum.
    drum=b.m.parts[-1]
    for side in (-1,1):
        for y in (269,282,295):
            drum['dec'].append(('z+' if side==1 else 'z-',side*34,
                                 roundpoly([(329,y),(419,y-4),(425,y),(336,y+5)],2),FL,False))
    b.C(306,450,AXC,5,DK,n=12,L='Achsstift')
    b.C(472,550,AX,12,DK,n=12,L='Lauf')
    b.P([(476,242),(525,239),(553,250),(548,254),(478,252)],
        MA,-10,10,r=6,L='Laufschiene')
    # Der Querfächer ist vorne deutlich breiter als der kurze Lauf.
    b.Y([(546,-13),(577,-31),(599,-36),(611,-26),(611,26),
         (599,36),(577,31),(546,13)],FL,AX-16,AX+16,r=8,L='Streumündung',
        dec=[D([(555,-2),(601,-23),(605,-17),(567,0),(605,17),(601,23),(555,2)],MA)])
    muzzle=b.m.parts[-1]
    muzzle['dec'].append(('x+',611,roundpoly(rect(AX-8,-22,16,44),5),DK,False))
    for zz in (-13,0,13):
        muzzle['dec'].append(('x+',611,circ(AX,zz,2.4,10),PF,True))
    trigger_group(b,320,337,PF,MA,grip_x0=280,depth=34)
    return b.m


META = dict(
    num='25',name='Streuschuss-Handfeuerwaffe',nick='MUSCHELHIEB',col=PF,
    pill='MALACHIT · FLIEDER · PFIRSICH',palette=[MA,FL,PF,DK],center=(407,327,0),
    desc='Ein fliederfarbener Muschelrücken wölbt sich über die malachitgrüne Fünfkammertrommel und zieht bis zum vorderen Kippjoch. '
         'Der zurückgeschwungene Griff und die breite, flache Fächermündung führen das Muschelmotiv fort; pfirsichfarbene Kanten markieren die Bedienung.',
    form='Gewölbter Muschel-Kipprahmen · verdeckter Hahn · Kippriegel hinten oben · '
         'freie Fünfkammertrommel · vorderes Scharnier · kurzer Lauf · breite Fächermündung · geschwungener Griff · Visierschiene',
    op=dict(
        reload_de='Kippriegel drücken, Rahmen mit Trommel und Lauf am vorderen Scharnier abkippen, fünf Hülsen auswerfen, Schrotpatronen einsetzen, schließen',
        action_de='Double Action: jeder Abzug spannt den verdeckten Hahn und dreht die Trommel zur nächsten der fünf Kammern',
        fire_de='Ein kurzer Streuschuss je Abzug; die obere Kammer fluchtet mit dem Lauf, die breite Mündung fächert die Schrotladung flach',
        reload_en='press the top latch, tip frame with cylinder and barrel down on the front hinge, eject five cases, load shot shells and close',
        action_en='double action: each trigger pull cocks the shrouded hammer and indexes the next of five chambers',
        fire_en='one close-range spread per pull; the upper chamber aligns with the barrel, the wide muzzle fans the pellets flat'))
