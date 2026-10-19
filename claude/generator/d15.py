"""KD15 „Eiswalze“: dunkler Buckeltrommelwerfer mit geklemmtem Rohrschaft."""
import math
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, MC, DK, K, A, AL = '#D8DCE0', '#3A3D44', '#2A2F38', '#1C2027', '#55CEDB', '#D5FAFF'
AX, RING = 302, 42


def model():
    b = B(); D = b.D
    # Rohr, zwei Klemmen und die separate Kappe ersetzen den üblichen Schulterblock.
    b.C(66,204,282,12,DK,n=16,L='Schaft')
    for x in (88,172):
        b.C(x,x+20,282,18,K,n=16,L='Schaftklemme')
    b.P(rect(48,246,24,112),K,-29,29,r=11,L='Schaftkappe')
    b.P(rect(49,258,10,84),P,-30,30,r=8,L='Schulterpolster')
    b.P(rect(100,253,76,22),P,-20,20,r=10,L='Wangenauflage')
    b.P(rect(178,267,32,29),MC,-25,25,r=10,L='Schaftaufnahme')
    b.P([(196,246),(280,236),(312,254),(312,372),(206,372),(186,350),(186,266)],
        MC,-35,35,r=12,L='Gehäuse')
    for z0,z1 in ((34,41),(-41,-34)):
        b.P([(204,259),(270,250),(290,266),(290,288),(204,296)],P,z0,z1,r=10,L='Gehäuseplatte',
            dec=[D(roundpoly(rect(216,271,56,9),4),A,True)])
    b.P(rect(242,312,62,42),K,34,44,r=10,L='Ladeklappe',
        dec=[D(roundpoly(rect(252,322,40,19),8),P)])
    b.P(rect(275,326,23,10),A,43,51,r=4,L='Klappenriegel')
    # Ein hoher gerundeter Rücken macht die Trommelmasse auch von der Seite lesbar.
    b.P([(282,238),(308,216),(354,206),(404,214),(438,234),(444,254),(290,254)],
        MC,-25,25,r=12,L='Oberbrücke')
    b.P([(311,215),(350,207),(372,210),(374,224),(320,232)],P,-26,26,r=9,L='Rückenplatte')
    rail(b,326,390,210,K,DK,w=14)
    # Kurze, hohe Walze mit echten hellen Stirnringen und dunklen Laufringen.
    b.C(312,424,AX,68,MC,n=20,L='Granattrommel')
    b.C(312,323,AX,69,P,n=20,L='Granattrommel')
    for x in (330,398):
        b.C(x,x+10,AX,70,K,n=20,L='Granattrommel')
    b.C(415,426,AX,68,P,n=20,L='Granattrommel',
        cap=[(AX-RING*math.cos(k*math.pi/3),RING*math.sin(k*math.pi/3),13,'#050506',False)
             for k in range(6)]+[(AX,0,13,K,False),(AX,0,6,A,True)])
    for z0,z1 in ((61,69),(-69,-61)):
        b.P([(344,285),(384,285),(392,296),(388,321),(344,321)],P,z0,z1,r=10,L='Granattrommel',
            dec=[D(roundpoly(rect(353,298,26,8),4),A,True)])
    b.C(294,450,AX,10,K,n=12,L='Trommelachse')
    b.P([(424,236),(446,238),(458,258),(456,316),(440,334),(424,328)],MC,-30,30,r=12,L='Laufträger')
    b.P(rect(438,281,14,36),P,29,36,r=7,L='Lagerdeckel')
    b.P(rect(438,281,14,36),P,-36,-29,r=7,L='Lagerdeckel')
    b.C(448,548,AX-RING,27,MC,n=16,L='Lauf')
    b.C(452,468,AX-RING,30,DK,n=16,L='Laufbund')
    b.P(rect(470,238,62,37),P,20,28,r=10,L='Laufplatte',
        dec=[D(roundpoly(rect(479,251,43,9),4),K)])
    b.P(rect(470,238,62,37),P,-28,-20,r=10,L='Laufplatte',
        xdec=[('z-',-28,roundpoly(rect(479,251,43,9),4),K,False)])
    b.C(546,572,AX-RING,33,K,n=16,L='Mündung',
        cap=[(AX-RING,0,27,P,False),(AX-RING,0,20,'#050506',False)])
    # Der Abzug liegt vollständig hinter und unter der Trommel.
    b.P([(206,368),(250,368),(270,452),(220,466),(204,448)],K,-23,23,r=12,L='Griff')
    b.P([(220,388),(239,384),(254,439),(230,447)],DK,22,28,r=9,L='Griffschale')
    b.P([(220,388),(239,384),(254,439),(230,447)],DK,-28,-22,r=9,L='Griffschale')
    b.P(arcband(250,308,369,60,9),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(266,368),(278,368),(286,404),(274,408)],A,-6,6,r=5,L='Abzug')
    b.P([(464,282),(502,282),(498,308),(488,378),(462,378),(458,354)],K,-20,20,r=11,L='Vordergriff',
        dec=[D(roundpoly(rect(468,312,17,43),8),P)])
    return b.m


META=dict(num='15',name='Schwerer Granatwerfer',nick='EISWALZE',col=A,
 pill='STASIS-VERSION',palette=[MC,P,A,AL],center=(316,346,0),
 desc='Eine hohe kurze Granattrommel und der gewölbte Rücken geben dem dunklen Werfer eine bucklige schwere Silhouette. Helle Stirnringe und echte Seitenplatten gliedern die Walze. Hinten trägt ein Rohrschaft mit zwei Klemmen die separate Schulterkappe und Wangenauflage.',
 form='Rohrschaft · zwei Schaftklemmen · separate Schulterkappe · helle Wangenauflage · dunkles Heckgehäuse mit hellen Platten · Ladeklappe links · hoher Trommelbuckel · Sechskammerwalze · Trommelachse · kurzer dicker Lauf · Vordergriff',
 op=dict(reload_de='Ladeklappe links öffnen, Trommel Kammer für Kammer drehen, sechs Granaten einsetzen und Klappe schließen.',
         action_de='Nach jedem Schuss dreht das Federwerk in der Trommelachse die schwere Granattrommel eine Kammer weiter.',
         fire_de='Sechs schwere Granaten nacheinander; die obere Kammer fluchtet mit dem kurzen Lauf, Zündung beim Aufprall.',
         reload_en='Open the left loading gate, index the drum chamber by chamber, insert six grenades and close the gate.',
         action_en='After each shot, the spring in the axle indexes the heavy grenade drum by one chamber.',
         fire_en='Fire six heavy grenades in succession; the upper chamber aligns with the short barrel, with impact detonation.'))
