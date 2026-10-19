"""KD25 „Splitterkrone“: massiger D-Kipprahmen mit fünf Schrotkammern."""
from tlib import B, rail
from eng import rect, roundpoly, circ
from dmodels import arcband
import math

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#74B8E5', '#E0F3FF'
AXC = 288
BX = AXC - 20  # obere Trommelkammer, z=0; Lauf und Streumündung auf derselben Achse


def model():
    b = B(); D = b.D
    b.P([(222,318),(276,318),(298,424),(238,434)],K,-24,24,r=12,L='Griff',
        dec=[D(roundpoly([(242,342),(260,342),(278,404),(260,408)],7),DK),
             D(roundpoly(rect(250,356,8,26),4),A,True)])
    # Fester Unterrahmen und verdeckter Hahn, obere Baugruppe am vorderen Gelenk kippbar.
    b.P([(212,272),(246,252),(284,252),(294,320),(390,320),(390,344),(244,344),(220,326)],
        DK,-23,23,r=10,L='Rahmen',
        dec=[D(roundpoly([(226,278),(246,268),(270,268),(276,310),(234,310)],8),P),
             D(roundpoly(rect(290,328,78,8),4),A,True)])
    b.P([(224,254),(260,240),(282,246),(290,262),(242,274)],K,-16,16,r=8,L='Hahnschutz',
        dec=[D(roundpoly(rect(246,250,24,8),4),P)])
    b.P(circ(382,326,11,16),K,-28,28,L='Scharnier',
        dec=[D(circ(382,326,5,12),A)])
    # Oberbrücke und vorderes Joch bleiben als offene, zusammenhängende Kipprahmenform lesbar.
    b.P([(280,230),(392,230),(404,246),(404,316),(378,316),(378,252),(280,252)],
        DK,-20,20,r=8,L='Kipprahmen',
        dec=[D(roundpoly(rect(294,235,82,10),4),P),D(roundpoly(rect(386,270,10,32),4),A,True)])
    b.P([(262,240),(280,230),(294,240),(284,254),(268,254)],K,-12,12,r=6,L='Kippriegel',
        dec=[D(roundpoly(rect(273,237,10,7),3),A)])
    rail(b,294,372,232,K,DK,w=12)
    b.C(298,366,AXC,34,DK,n=10,L='Trommel',
        cap=[(AXC-20*math.cos(2*k*math.pi/5),20*math.sin(2*k*math.pi/5),9,A,False) for k in range(5)]+
            [(AXC-20*math.cos(2*k*math.pi/5),20*math.sin(2*k*math.pi/5),4.8,K,False) for k in range(5)])
    b.C(290,382,AXC,5,K,n=10,L='Trommel')
    # Seitliche eingelassene Rillen, keine abstehende Scheibe vor den Kammern.
    for z0,z1 in ((31,35),(-35,-31)):
        band=[D(roundpoly(rect(310,282,42,12),5),P),D(roundpoly(rect(316,286,30,4),2),A,True)]
        b.P(rect(304,278,56,20),DK,z0,z1,r=8,L='Trommel',
            dec=band if z0>0 else (),xdec=[('z-',z0,*d) for d in band] if z0<0 else ())
    b.C(398,458,BX,18,K,n=12,L='Lauf')
    b.P(rect(400,BX-23,56,10),DK,-9,9,r=4,L='Lauf',
        dec=[D(roundpoly(rect(410,BX-20,34,4),2),A,True)])
    b.Y([(454,-18),(484,-34),(502,-34),(508,-26),(508,26),(502,34),(484,34),(454,18)],
        DK,BX-17,BX+17,r=8,L='Streumündung',
        dec=[D(roundpoly([(464,-12),(496,-24),(500,-18),(470,-6)],3),P),
             D(roundpoly([(464,12),(496,24),(500,18),(470,6)],3),P),
             D(roundpoly(rect(468,-3,30,6),3),A,True)])
    b.m.parts[-1]['dec'].append(('x+',508,roundpoly(rect(BX-8,-18,16,36),6),K,False))
    for z in (-12,0,12):
        b.m.parts[-1]['dec'].append(('x+',508.5,circ(BX,z,2.8,10),AL,True))
    b.P(arcband(278,370,342,70,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(302,343),(315,343),(328,384),(314,390)],A,-6,6,r=4,L='Abzug')
    return b.m


META=dict(num='25',name='Streuschuss-Handfeuerwaffe',nick='SPLITTERKRONE',col=A,
 pill='POLAR-SKIN',palette=[P,DK,A,AL],center=(361,327,0),
 desc='Ein kurzer, massiger Kipprahmen-Revolver trägt fünf Schrotkammern in einer breiten Trommel und einen tiefen, gerundeten Griff. Helle Deckplatten und eisblaue Leuchtstreifen gliedern den dunklen Rahmen; der kurze Lauf sitzt auf der oberen Kammer und endet in einer flachen, seitlich aufgefächerten Streumündung.',
 form='Massiger Rahmen · verkleideter Hahn · offene Kipprahmenbrücke mit Joch · Kippriegel hinten oben · kurze dicke Trommel mit fünf Schrotkammern · Scharnier vorne unten · kurzer Lauf auf oberer Kammer · breite flache Streumündung · gebogener Bügel',
 op=dict(reload_de='Kippriegel drücken, Lauf und Trommel am vorderen Scharnier abkippen. Sternauswerfer hebt fünf Hülsen; Schrotpatronen einsetzen, schließen.',
         action_de='Double Action: Der verdeckte Hahn spannt bei jedem Abzug, die Trommel dreht um eine der fünf Kammern weiter.',
         fire_de='Schrotkugeln streuen flach aus der breiten Mündung; langsame Feuerrate und hohe Wirkung auf kurze Distanz.',
         reload_en='Press the latch and tip barrel and cylinder down on the front hinge. The star extractor lifts five shells; insert shot shells and close.',
         action_en='Double action: each trigger pull cocks the shrouded hammer and indexes the cylinder by one of five chambers.',
         fire_en='Pellets fan flat from the wide muzzle; slow rate of fire and strong close-range impact.'))
