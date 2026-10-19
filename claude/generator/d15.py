"""KD15 „Eiswalze“: kurzer schwerer D-Trommelwerfer mit großer Sechskammerwalze."""
import math
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#55CEDB', '#D5FAFF'
AX, RING = 302, 42


def model():
    b = B(); D = b.D
    b.P([(68,246),(148,246),(190,264),(190,334),(130,344),(76,362),(68,350)],
        DK,-29,29,r=12,L='Schaft',
        dec=[D(roundpoly(rect(84,260,68,28),10),P),
             D(roundpoly(rect(92,316,46,10),5),K)])
    b.P(rect(50,240,24,128),K,-32,32,r=10,L='Schaftkappe')
    b.P([(180,236),(292,230),(312,246),(312,372),(196,372),(180,352)],
        DK,-34,34,r=12,L='Gehäuse',
        dec=[D(roundpoly([(198,250),(278,244),(290,258),(290,286),(198,292)],10),P),
             D(roundpoly(rect(208,264,66,10),5),A,True)])
    b.P(rect(238,310,62,44),K,33,42,r=10,L='Ladeklappe',
        dec=[D(roundpoly(rect(248,318,42,27),8),P),
             D(roundpoly(rect(254,328,30,7),3),A,True)])
    # Die kurze, breite Trommel ist sichtbar größer als der Verschlussblock.
    b.C(312,416,AX,64,DK,n=18,L='Granattrommel',
        cap=[(AX,0,59,P,False)]+
            [(AX-RING*math.cos(k*math.pi/3),RING*math.sin(k*math.pi/3),13,'#050506',False)
             for k in range(6)]+[(AX,0,13,K,False),(AX,0,6,A,True)])
    for x in (324,394):
        b.C(x,x+9,AX,65,K,n=18,L='Granattrommel')
    b.C(294,446,AX,10,K,n=12,L='Trommelachse')
    b.P(rect(296,222,142,20),DK,-22,22,r=8,L='Oberbrücke',
        dec=[D(roundpoly(rect(312,227,108,9),4),P)])
    rail(b,212,290,236,K,DK,w=14)
    b.P([(416,236),(444,236),(450,256),(450,328),(416,328)],DK,-29,29,r=10,L='Laufträger',
        dec=[D(roundpoly(rect(426,278,14,34),6),P)])
    b.C(444,554,AX-RING,26,DK,n=16,L='Lauf')
    b.P(rect(460,242,80,36),DK,-23,23,r=10,L='Lauf',
        dec=[D(roundpoly(rect(470,248,60,14),6),P),
             D(roundpoly(rect(476,268,48,6),3),A,True)])
    b.C(554,580,AX-RING,32,K,n=16,L='Mündung',
        cap=[(AX-RING,0,26,P,False),(AX-RING,0,20,'#050506',False)])
    # Der gesamte Abzugsraum bleibt hinter und unter der Trommel frei.
    b.P([(198,370),(248,370),(268,462),(210,468)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(218,388),(232,388),(248,444),(232,448)],6),DK)])
    b.P(arcband(248,306,370,62,9),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(264,371),(276,371),(284,406),(272,410)],A,-6,6,r=4,L='Abzug')
    b.P([(458,284),(496,284),(490,378),(464,378)],K,-19,19,r=11,L='Vordergriff',
        dec=[D(roundpoly(rect(468,306,17,42),8),P)])
    return b.m


META=dict(num='15',name='Schwerer Granatwerfer',nick='EISWALZE',col=A,
 pill='STASIS-VERSION',palette=[P,DK,A,AL],center=(316,346,0),
 desc='Eine kurze, breite Sechskammerwalze prägt den schweren gerundeten Werfer zwischen Schulterblock und kurzem Laufträger. Helle Deckplatten gliedern das dunkle Gehäuse; die Ladeklappe sitzt links und der Lauf fluchtet mit der oberen Trommelkammer.',
 form='Tiefer Schulterblock · massiger Heckrahmen · Ladeklappe links · breite Granattrommel mit sechs Kammern · Trommelachse · Oberbrücke · kurzer Laufträger · dicker Lauf · Vordergriff · Abzug hinter der Trommel · gebogener Bügel',
 op=dict(reload_de='Ladeklappe links öffnen, Trommel Kammer für Kammer drehen, sechs Granaten einsetzen und Klappe schließen.',
         action_de='Nach jedem Schuss dreht das Federwerk in der Trommelachse die Granattrommel um eine Kammer weiter.',
         fire_de='Sechs schwere Granaten nacheinander; die obere Kammer speist den kurzen Lauf, Zündung beim Aufprall.',
         reload_en='Open the left loading gate, turn the drum chamber by chamber, insert six grenades and close the gate.',
         action_en='After each shot, the spring in the axle indexes the grenade drum by one chamber.',
         fire_en='Fire six heavy grenades in succession; the upper chamber feeds the short barrel, with impact detonation.'))
