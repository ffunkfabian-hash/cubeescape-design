"""KD25 „Splitterkrone“: massiger D-Kipprahmen mit fünf Schrotkammern."""
from tlib import B, rail
from eng import rect, roundpoly, circ
from dmodels import arcband
import math

M = '#3A3D44'
P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#74B8E5', '#E0F3FF'
AXC = 294
BX = AXC - 30  # obere Trommelkammer, z=0; Lauf und Streumündung auf derselben Achse


def model():
    b = B(); D = b.D
    # Tief heruntergezogener Handrahmen und breite Trommel, kein verkleinerter Gewehrkörper.
    b.P([(208,330),(266,330),(294,426),(238,444),(216,410)],K,-25,25,r=12,L='Griff')
    for z0,z1 in ((24,31),(-31,-24)):
        pad=[D(roundpoly([(228,352),(250,352),(270,408),(248,414)],8),P),D(roundpoly(rect(238,370,8,22),4),A,True)]
        b.P([(216,342),(260,342),(280,416),(238,430)],M,z0,z1,r=12,L='Griffschale',
            dec=pad if z0>0 else (),xdec=[('z-',z0,*d) for d in pad] if z0<0 else ())
    b.P(rect(236,426,60,18),M,-27,27,r=8,L='Griffabschluss')
    b.P([(202,270),(240,248),(278,258),(292,326),(388,326),(388,352),(242,352),(210,328)],M,-25,25,r=12,L='Rahmen')
    b.P([(210,266),(232,238),(258,238),(282,264),(276,284),(232,282)],M,-24,24,r=12,L='Hahnschutz')
    b.P(rect(218,280,36,22),P,24,32,r=8,L='Schlossplatte')
    b.P(circ(382,338,15,18),K,-34,34,L='Scharnier',dec=[D(circ(382,338,7,12),P)])
    # Die Oberbrücke hält nur die Trommeloberkante; seitliche Joche führen zum Scharnier.
    b.P([(270,226),(380,226),(398,238),(398,249),(278,249)],M,-24,24,r=8,L='Kipprahmen')   # endet über der Trommel (Oberkante y 250)
    for z0,z1 in ((30,40),(-40,-30)):
        marks=[D(roundpoly(rect(373,274,12,44),5),P)]
        b.P([(366,252),(396,252),(396,338),(370,346)],M,z0,z1,r=10,L='Kipprahmen',
            dec=marks if z0>0 else (),xdec=[('z-',z0,*d) for d in marks] if z0<0 else ())
    b.P([(258,244),(274,230),(292,240),(286,260),(266,266)],K,-17,17,r=8,L='Kippriegel',dec=[D(rect(270,241,12,6),A)])
    rail(b,290,364,226,K,DK,w=13)   # reicht 6 in den Kipprahmen (Oberkante y 226)
    b.C(294,362,AXC,44,M,n=16,L='Trommel',cap=[
        (AXC-30*math.cos(2*k*math.pi/5),30*math.sin(2*k*math.pi/5),10,A,False) for k in range(5)]+
        [(AXC-30*math.cos(2*k*math.pi/5),30*math.sin(2*k*math.pi/5),5.5,K,False) for k in range(5)])
    b.C(288,298,AXC,43,DK,n=16,L='Trommel')
    b.C(360,370,AXC,43,DK,n=16,L='Trommel',cap=[
        (AXC-30*math.cos(2*k*math.pi/5),30*math.sin(2*k*math.pi/5),9,A,False) for k in range(5)]+
        [(AXC-30*math.cos(2*k*math.pi/5),30*math.sin(2*k*math.pi/5),5,K,False) for k in range(5)])
    b.C(282,382,AXC,6,K,n=12,L='Trommel')
    # Erhabene Trommelbänder sitzen auf dem breiten Mantel, nicht vor den Kammern.
    for z0,z1 in ((41,47),(-47,-41)):
        marks=[D(roundpoly(rect(312,284,32,8),4),A,True)]
        b.P(rect(302,276,52,24),P,z0,z1,r=10,L='Trommel',
            dec=marks if z0>0 else (),xdec=[('z-',z0,*d) for d in marks] if z0<0 else ())
    b.C(390,460,BX,20,K,n=12,L='Lauf')
    b.P(rect(394,BX-25,60,14),M,-13,13,r=6,L='Lauf')
    b.C(430,446,BX,25,M,n=12,L='Lauf')
    b.Y([(454,-20),(486,-42),(510,-42),(518,-30),(518,30),(510,42),(486,42),(454,20)],M,BX-21,BX+21,r=10,L='Streumündung',
        dec=[D(roundpoly([(464,-15),(500,-30),(506,-22),(470,-8)],4),P),
             D(roundpoly([(464,15),(500,30),(506,22),(470,8)],4),P)])
    b.m.parts[-1]['dec'].append(('x+',518,roundpoly(rect(BX-11,-28,22,56),8),K,False))
    for z in (-18,0,18):b.m.parts[-1]['dec'].append(('x+',518.5,circ(BX,z,3,10),AL,True))
    # Zwei kurze seitliche Kappen bilden die austauschbaren Streubacken.
    for z0,z1 in ((36,44),(-44,-36)):
        b.P(rect(486,BX-14,24,28),P,z0,z1,r=8,L='Streumündung')
    b.P(arcband(278,370,350,70,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(302,351),(315,351),(328,392),(314,398)],A,-6,6,r=4,L='Abzug')
    return b.m

META=dict(num='25',name='Streuschuss-Handfeuerwaffe',nick='SPLITTERKRONE',col=A,
 pill='POLAR-SKIN',palette=[M,P,A,AL],center=(361,327,0),
 desc='Eine sehr breite Fünfkammer-Trommel sitzt in einer offenen, dunklen Kippwiege mit seitlichen Jochen. Der tiefe Handrahmen und helle Griffschalen balancieren die kurze, aufgefächerte Streumündung mit austauschbaren Backen. Eisblau leuchten Trommelbänder und Griff; der Lauf fluchtet mit der oberen Kammer.',
 form='Tiefer Handrahmen · helle Griffschalen · Hahnschutz · offene Kippwiege mit seitlichen Jochen · Kippriegel · breite Fünfkammer-Trommel · Stirnringe und Achse · vorderes Scharnier · kurzer Lauf auf oberer Kammer · Fächermündung mit Streubacken',
 op=dict(reload_de='Kippriegel drücken, Lauf und Trommel am vorderen Scharnier abkippen. Sternauswerfer hebt fünf Hülsen; Schrotpatronen einsetzen, schließen.',
         action_de='Double Action: Der verdeckte Hahn spannt bei jedem Abzug, die Trommel dreht um eine der fünf Kammern weiter.',
         fire_de='Schrotkugeln streuen flach aus der breiten Mündung; langsame Feuerrate und hohe Wirkung auf kurze Distanz.',
         reload_en='Press the latch and tip barrel and cylinder down on the front hinge. The star extractor lifts five shells; insert shot shells and close.',
         action_en='Double action: each trigger pull cocks the shrouded hammer and indexes the cylinder by one of five chambers.',
         fire_en='Pellets fan flat from the wide muzzle; slow rate of fire and strong close-range impact.'))
