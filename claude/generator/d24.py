"""KD24 „Spaltkeil“: D-Mikroraketenwerfer mit Toplader und linkem Raketenvorrat."""
from tlib import B, rail
from eng import rect, roundpoly, circ
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#BA71B7', '#F8DDF5'
AX = 286


def model():
    b = B(); D = b.D
    # Ein langer axialer Rohrschaft ersetzt den üblichen Gehäuse-Schaftblock.
    b.P(rect(66,252,24,102),K,-27,27,r=10,L='Schaftkappe')
    b.C(84,264,AX,15,P,n=12,L='Schaft')
    b.C(88,110,AX,26,DK,n=12,L='Axialverschluss')
    for x in (132,212):
        b.C(x,x+18,AX,23,DK,n=12,L='Klemmring')
        b.P(rect(x+2,300,14,16),K,-8,8,r=5,L='Klemmschraube')
    b.P(rect(248,252,30,66),DK,-30,30,r=10,L='Schaftaufnahme')
    b.P([(274,228),(392,228),(432,248),(448,274),(448,334),(274,334),(258,314),(258,250)],P,-37,37,r=12,L='Gehäuse')
    b.P(rect(280,312,144,26),DK,-31,31,r=10,L='Unterrahmen')
    rail(b,276,326,234,K,DK,w=14)
    b.P([(338,222),(406,222),(432,238),(432,250),(338,250)],P,-25,25,r=10,L='Ladeklappe',
        dec=[D(roundpoly(rect(352,230,56,10),4),A,True)])
    b.P(circ(340,240,8,12),K,-29,29,L='Klappenscharnier')
    b.P(rect(420,240,20,20),K,23,38,r=6,L='Klappenriegel')
    # Eigenständige Halteschiene verbindet den linken Vorratskasten mit dem Hauptkörper.
    b.P(rect(290,270,126,48),DK,36,44,r=10,L='Vorratshalter')
    b.P(rect(284,276,144,58),DK,43,69,r=12,L='Raketenvorrat',
        dec=[D(roundpoly(rect(294,284,124,42),9),P),D(roundpoly(rect(300,288,112,34),7),K)]+
            [D(roundpoly(rect(306,292+8*i,76,5),2),AL) for i in range(4)]+
            [D([(382,292+8*i),(402,294.5+8*i),(382,297+8*i)],A) for i in range(4)])
    b.P(rect(292,328,128,14),P,45,68,r=6,L='Vorratsboden')
    b.C(436,688,AX,21,P,n=12,L='Abschussrohr')
    for x in (460,542,624):
        b.C(x,x+18,AX,29,DK,n=12,L='Leitring')
        b.m.decal('x+',x+18,roundpoly(rect(AX-23,-12,6,24),3),A,emit=True,both=False)
    b.F(684,710,AX,21,31,P,n=12,L='Mündung')
    b.C(706,722,AX,31,K,n=12,L='Mündung',cap=[(AX,0,21,K,False),(AX,0,8,A,False),(AX,0,3,AL,True)])
    b.P([(280,334),(330,334),(350,432),(294,440)],K,-23,23,r=12,L='Griff')
    b.P(rect(294,430,56,15),DK,-25,25,r=6,L='Griffabschluss')
    b.P(arcband(330,416,336,70,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(350,337),(363,337),(376,378),(362,384)],A,-6,6,r=4,L='Abzug')
    b.C(576,598,AX,29,DK,n=12,L='Griffschelle')
    b.P([(578,306),(604,306),(602,378),(584,386)],K,-18,18,r=10,L='Vordergriff')
    return b.m

META=dict(num='24',name='Mikroraketen-Granatwerfer',nick='SPALTKEIL',col=A,
 pill='PHASE-SKIN',palette=[P,DK,A,AL],center=(386,332,0),
 desc='Ein langer heller Rohrschaft mit zwei Klemmringen endet axial im kompakten Toplader. Dessen heller Hauptkörper trägt links vier Mikroraketen in einem tiefen Sichtkasten; vorne setzt sich das helle Abschussrohr durch drei dunkle Leitringe fort. Violette Fenster markieren Klappe und Ringe.',
 form='Langer Rohrschaft · axialer Verschluss · zwei Klemmringe · heller Toplader · obere Ladeklappe mit Riegel · linker Raketenvorrat auf Halteschiene · helles Abschussrohr · drei Leitringe · Mündung · Vordergriff an Schelle',
 op=dict(reload_de='Obere Ladeklappe nach hinten öffnen, eine Mikrorakete aus dem linken Vorrat ins Patronenlager legen und die Klappe schließen.',
         action_de='Einschüssig: eine Mikrorakete im Rohr, nach jedem Schuss neu laden; der Treibsatz zündet erst vor der Mündung.',
         fire_de='Eine schnelle, gerade fliegende Mikrorakete mit Aufprallzünder; Spezialmunition und geringer Eigenschaden.',
         reload_en='Open the top loading gate to the rear, place one micro-missile from the left reserve into the chamber, then close the gate.',
         action_en='Single shot: one micro-missile in the tube; reload after each shot. Its motor ignites just past the muzzle.',
         fire_en='One fast, straight-flying micro-missile with an impact fuse; special ammo and low self-damage.'))
