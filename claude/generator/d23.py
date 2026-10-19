"""KD23 „Glutherd“: magazinloser D-Thermalblock mit zwei Entlüftungsklappen."""
from tlib import B, rail
from eng import rect, roundpoly, circ
from dmodels import arcband

M = '#3A3D44'
P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#E7AF55', '#FFF0CB'
AX = 292


def model():
    b = B(); D = b.D
    # Zwei voneinander getrennte Streben laufen in ein querliegendes Klappgelenk.
    b.P(rect(82,244,24,116),K,-26,26,r=10,L='Schaftkappe')
    b.P([(102,248),(228,238),(244,252),(230,272),(102,278)],M,-19,19,r=12,L='Schaft')
    b.P([(102,330),(222,278),(242,290),(230,308),(108,356)],M,-19,19,r=12,L='Schaft')
    b.P(circ(238,270,23,18),DK,-29,29,L='Schaftgelenk',dec=[D(circ(238,270,10,12),P)])
    b.P(rect(216,286,28,18),K,27,38,r=6,L='Schaftverriegelung')
    b.P([(246,236),(392,228),(434,244),(466,272),(466,332),(246,332),(230,312)],M,-36,36,r=12,L='Gehäuse')
    b.P(rect(250,310,194,26),K,-30,30,r=10,L='Unterrahmen')
    rail(b,262,388,238,K,DK,w=14)
    for z0,z1 in ((35,44),(-44,-35)):
        window=[D(roundpoly(rect(268,256,86,24),9),K),D(roundpoly(rect(276,264,70,8),4),A,True),D(rect(284,266,54,4),AL,True)]
        b.P(rect(256,244,110,46),P,z0,z1,r=12,L='Plasmakammer',
            dec=window if z0>0 else (),xdec=[('z-',z0,*d) for d in window] if z0<0 else ())
    for z0,z1 in ((35,43),(-43,-35)):
        seg=[D(roundpoly(rect(267+13*i,302,8,7),3),AL if i<4 else A,True) for i in range(8)]
        b.P(rect(258,294,120,22),K,z0,z1,r=8,L='Hitzeanzeige',
            dec=seg if z0>0 else (),xdec=[('z-',z0,*d) for d in seg] if z0<0 else ())
    for z0,z1 in ((35,45),(-45,-35)):
        vents=[D(roundpoly(rect(398+12*i,266,6,42),3),A,True) for i in range(5)]
        b.P([(384,246),(444,250),(460,272),(460,324),(384,324)],P,z0,z1,r=12,L='Entlüftungsklappe',
            dec=vents if z0>0 else (),xdec=[('z-',z0,*d) for d in vents] if z0<0 else ())
    # Scharnierachsen liegen an den Oberkanten der beiden Klappen.
    for z in (-41,41):
        b.C(388,444,250,5,K,n=10,cz=z,L='Klappenscharnier')
    # Unterschiedliche Rippenradien bauen einen deutlich buckligen Kühlkörper.
    b.C(450,610,AX,30,K,n=16,L='Hitzespeicher')
    b.F(450,470,AX,30,40,M,n=16,L='Kühlkörperansatz')
    for x,r in ((470,40),(488,49),(506,57),(524,61),(542,57),(560,49),(578,40)):
        b.C(x,x+10,AX,r,M if x in (488,524,560) else P,n=16,L='Kühlrippen')
    b.F(588,612,AX,40,20,M,n=16,L='Kühlkörperabschluss')
    b.C(608,654,AX,13,K,n=12,L='Lauf')
    b.C(648,676,AX,25,M,n=12,L='Fokusring',cap=[(AX,0,15,K,False),(AX,0,7,A,True),(AX,0,3,AL,True)])
    b.P([(264,330),(314,330),(334,428),(278,436)],K,-23,23,r=12,L='Griff')
    b.P(rect(278,426,56,15),M,-25,25,r=6,L='Griffabschluss')
    b.P(arcband(314,400,332,68,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(336,333),(349,333),(362,374),(348,380)],A,-6,6,r=4,L='Abzug')
    b.P([(426,330),(458,330),(454,398),(432,404)],K,-19,19,r=10,L='Vordergriff')
    return b.m

META=dict(num='23',name='Hitze-Blaster',nick='GLUTHERD',col=A,
 pill='THERMAL-VERSION',palette=[M,P,A,AL],center=(380,332,0),
 desc='Zwei Klappschaft-Streben münden in ein breites Gelenk hinter dem dunklen Thermalgehäuse. Ein rund aufgewölbtes Rippenpaket bildet den schweren Wärmebuckel vor den hellen Entlüftungsklappen. Plasmakammer und segmentierte Anzeige leuchten warmgelb; ein Magazin fehlt vollständig.',
 form='Zweistreben-Klappschaft mit Gelenk und Riegel · dunkles Thermalgehäuse · helle Plasmakammer · Hitzeanzeige · zwei Entlüftungsklappen mit Scharnierachsen · buckliges Rippenpaket · Lauf und Fokusring · Vordergriff',
 op=dict(reload_de='Kein Magazin: Nachladetaste öffnet beide Entlüftungsklappen; die Munition kommt direkt aus der Reserve.',
         action_de='Jede Salve erhitzt den Hitzespeicher. Die Rippen kühlen dazwischen; bei voller Anzeige folgt eine lange Zwangsentlüftung.',
         fire_de='Plasmabolzen in Salven; Entlüften im mittleren Anzeigebereich verkürzt die Feuerpause.',
         reload_en='No magazine: the reload input opens both vent flaps; ammunition comes directly from reserves.',
         action_en='Each burst heats the heat sink. Fins cool between bursts; a full gauge forces a long vent.',
         fire_en='Bursts of plasma bolts; venting in the middle gauge range shortens the firing pause.'))
