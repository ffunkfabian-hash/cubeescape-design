"""KF23 Hitze-Blaster „Glutbogen“: tiefes Rahmenheck und freier, gestufter Kühlkörper.

Das große Schaftfenster besteht aus einzelnen Stegen. Beide Entlüftungsklappen liegen außen;
die markante warme Gehäuseschale bleibt ohne Magazin oder Energiezelle.
"""
from eng import rect, roundpoly
from tlib import B, grip, rail, trigger_group

MA, CY, DK, HE = '#E0A33C', '#43CDD1', '#263044', '#EFE4D5'
AX = 280


def model():
    b = B()
    D = b.D
    # Hoher Hinterbogen mit echter Öffnung, keine aufgemalte dunkle Lochfläche.
    b.P([(92,253),(128,247),(158,282),(145,374),(124,401),(100,387)],
        CY, -18, 18, r=9, L='Schaft')
    b.P([(119,250),(239,238),(286,252),(284,278),(149,283)],
        MA, -17, 17, r=8, L='Schaft',
        dec=[D([(151,258),(235,248),(257,257),(155,273)], HE)])
    b.P([(133,377),(263,377),(299,352),(316,371),(280,405),(121,402)],
        CY, -16, 16, r=8, L='Schaft')
    b.P([(82,252),(98,250),(109,387),(97,402),(83,392)],
        DK, -20, 20, r=5, L='Schaftkappe')
    # Kurze, nach vorn tiefer werdende Schale mit nur zwei großen Farbfeldern.
    b.P([(254,241),(385,241),(420,251),(475,259),(493,287),(473,327),
         (420,337),(394,308),(254,308)],
        MA, -24, 24, r=8, L='Gehäuse',
        dec=[D([(262,284),(376,284),(396,301),(262,300)], CY)])
    rail(b, 259, 380, 244, DK, CY, w=10)
    # Seitenfenster und darunter eine ruhige, breite Anzeige statt vieler Kleindetails.
    b.P([(273,253),(359,253),(371,263),(361,280),(273,280)],
        DK, 24, 28, r=4, L='Plasmakammer',
        dec=[D(roundpoly(rect(280,259,71,14),3), CY, True)])
    b.P(rect(275,287,103,12), DK, 24, 27, r=3, L='Hitzeanzeige',
        dec=[D(rect(281,291,58,4), CY, True), D(rect(343,291,27,4), MA, True)])
    # Beide Klappen an den seitlichen Schultern; dieselbe Bezeichnung auf beiden Gegenstücken.
    flap = [(399,258),(467,268),(476,286),(459,313),(414,317),(398,298)]
    slots = [roundpoly([(410+13*i,272+2*i),(416+13*i,273+2*i),
                        (423+13*i,299),(417+13*i,302)],2) for i in range(4)]
    for side in (-1, 1):
        z0,z1 = sorted((24*side,30*side))
        b.P(flap, CY, z0, z1, r=4, L='Entlüftungsklappe',
            xdec=[('z+' if side>0 else 'z-',30*side,p,MA,True) for p in slots])
    b.C(476,661,AX,21,DK,n=12,L='Hitzespeicher')
    # Wenige große Scheiben wachsen bis zur Mitte und fallen zur Mündung wieder ab.
    for i,(x,radius) in enumerate(((485,29),(510,34),(535,39),(560,42),(585,39),(610,34),(635,29))):
        b.C(x,x+12,AX,radius,MA if i%2==0 else CY,n=12,L='Kühlrippen' if i==0 else None)
    b.C(661,724,AX,10,DK,n=10,L='Lauf')
    b.F(710,734,AX,15,22,CY,n=12,L='Fokusring')
    b.C(734,741,AX,22,DK,n=12,
        cap=[(AX,0,12,DK,False),(AX,0,5,CY,True)])
    grip(b,266,307,DK,CY,h=99,w=54,lean=19,z=18)
    trigger_group(b,337,308,HE,DK,grip_x0=310,depth=40)
    b.P([(424,330),(468,320),(473,344),(451,386),(430,385),(419,365)],
        CY,-15,15,r=7,L='Vordergriff',
        dec=[D([(435,344),(457,338),(447,367),(435,370)],DK)])
    return b.m


META = dict(
    num='23', name='Hitze-Blaster', nick='GLUTBOGEN', col=CY,
    pill='MANGO · TÜRKIS · TINTE', palette=[MA,CY,DK,HE], center=(411,325,0),
    desc='Ein tiefer türkisfarbener Schaftbogen öffnet das Heck unter der mangofarbenen Gehäuseschale. '
         'Sieben große gestufte Kühlrippen fassen den Hitzespeicher; zwei seitliche Klappen und eine breite Hitzeanzeige ersetzen den Magazinwechsel.',
    form='Tiefer offener Schaftbogen · kurze Mangoschale · Plasmakammer links · breite Hitzeanzeige · '
         'zwei seitliche Entlüftungsklappen · gestuftes Rippenpaket · Fokusring · geneigter Vordergriff',
    op=dict(
        reload_de='Nachladetaste öffnet beide seitlichen Entlüftungsklappen zum Abkühlen; kein Magazin, Munition direkt aus dem Vorrat.',
        action_de='Jede Salve heizt den Speicher auf. Die großen Rippen kühlen zwischen Salven; bei voller Anzeige folgt erzwungenes Entlüften.',
        fire_de='Plasmabolzen in Salven; Entlüften im Mittelfenster der Anzeige verkürzt die Pause.',
        reload_en='Reload opens both side vent flaps to dump heat; no magazine, ammunition comes straight from reserves.',
        action_en='Each burst heats the sink. The large fins cool between bursts; a full gauge forces a long vent.',
        fire_en='Bursts of plasma bolts; vent within the gauge sweet spot for a shorter pause.'))
