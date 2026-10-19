"""KD23 „Hitzestau“: magazinloser D-Thermalblock mit zwei Entlüftungsklappen."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#E7AF55', '#FFF0CB'
AX = 292


def model():
    b = B(); D = b.D
    # Ein geschlossener, tiefer Schulterblock ersetzt den dünnen G-Rahmenschaft.
    b.P([(102,240),(172,240),(228,260),(228,326),(176,326),(118,350),(102,350)],
        DK,-26,26,r=12,L='Schaft',
        dec=[D(roundpoly(rect(120,252,78,26),10),P),D(roundpoly(rect(122,310,44,10),4),K)])
    b.P(rect(88,234,20,126),K,-29,29,r=8,L='Schaftkappe')
    b.P([(214,230),(444,224),(480,244),(480,338),(236,338),(214,316)],
        DK,-36,36,r=12,L='Gehäuse',
        dec=[D(roundpoly([(236,244),(348,240),(366,254),(366,288),(236,292)],10),P),
             D(roundpoly(rect(244,318,136,10),4),K)])
    rail(b,246,424,232,K,DK,w=14)
    # Die Plasmakammer liegt als symmetrischer, eingelassener Deckel auf dem Gehäuse.
    for z0,z1 in ((35,40),(-40,-35)):
        window=[D(roundpoly(rect(250,254,94,24),9),K),
                D(roundpoly(rect(258,262,78,8),4),A,True),
                D(roundpoly(rect(266,264,60,4),2),AL,True)]
        b.P(rect(240,246,114,40),DK,z0,z1,r=10,L='Plasmakammer',
            dec=window if z0>0 else (),xdec=[('z-',z0,*d) for d in window] if z0<0 else ())
    for z0,z1 in ((35,40),(-40,-35)):
        seg=[D(roundpoly(rect(250+15*i,300,10,7),3),AL if i<4 else A,True) for i in range(8)]
        b.P(rect(242,294,130,20),K,z0,z1,r=8,L='Hitzeanzeige',
            dec=seg if z0>0 else (),xdec=[('z-',z0,*d) for d in seg] if z0<0 else ())
    # Beide Klappen sind eigenständige beschriftete Teile; obere Kante ist die Scharnierlinie.
    for z0,z1 in ((35,43),(-43,-35)):
        cover=([D(roundpoly(rect(394,250,60,12),5),P)]+
               [D(roundpoly(rect(394+12*i,276,6,42),3),A,True) for i in range(6)])
        b.P([(382,240),(466,240),(474,256),(474,326),(382,326)],DK,z0,z1,r=10,L='Entlüftungsklappe',
            dec=cover if z0>0 else (),xdec=[('z-',z0,*d) for d in cover] if z0<0 else ())
    # Kurzes, breites Rippenpaket statt langer, filigraner G-Laufstrecke.
    b.C(470,596,AX,24,K,n=12,L='Hitzespeicher')
    for x in (478,496,514,532,550,568,586):
        b.C(x,x+9,AX,41,DK,n=12,L='Kühlrippen')
        b.m.decal('x+',x+9,roundpoly(rect(AX-30,-13,7,26),3),P,both=False)
    b.C(594,646,AX,13,K,n=12,L='Lauf')
    b.C(642,670,AX,25,DK,n=12,L='Fokusring',
        cap=[(AX,0,15,K,False),(AX,0,7,A,True),(AX,0,3,AL,True)])
    b.P([(264,336),(314,336),(334,434),(278,440)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(284,356),(300,356),(315,414),(300,416)],6),DK)])
    b.P(arcband(314,400,336,68,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(336,337),(349,337),(362,378),(348,384)],A,-6,6,r=4,L='Abzug')
    b.P([(426,336),(462,336),(458,406),(432,412)],DK,-19,19,r=10,L='Vordergriff',
        dec=[D(roundpoly(rect(440,352,10,36),4),A,True)])
    return b.m


META=dict(num='23',name='Hitze-Blaster',nick='HITZESTAU',col=A,
 pill='THERMAL-VERSION',palette=[P,DK,A,AL],center=(380,332,0),
 desc='Ein magazinloser Thermalblock bündelt die Masse in einem tiefen Gehäuse mit heller Deckplatte und kurzem, breitem Rippenpaket. Die Plasmakammer und die segmentierte Hitzeanzeige leuchten warmgelb; zwei seitliche Entlüftungsklappen geben die gespeicherte Hitze ab.',
 form='Tiefer Schulterblock · Gehäuse ohne Magazinschacht · Plasmakammer mit Fenster · segmentierte Hitzeanzeige · zwei seitliche Entlüftungsklappen · kompakter Hitzespeicher · breite Kühlrippen · freier Lauf und Fokusring · gebogener Bügel · Vordergriff',
 op=dict(reload_de='Kein Magazin: Nachladetaste öffnet beide Entlüftungsklappen; die Munition kommt direkt aus der Reserve.',
         action_de='Jede Salve erhitzt den Hitzespeicher. Die Rippen kühlen dazwischen; bei voller Anzeige folgt eine lange Zwangsentlüftung.',
         fire_de='Plasmabolzen in Salven; Entlüften im mittleren Anzeigebereich verkürzt die Feuerpause.',
         reload_en='No magazine: the reload input opens both vent flaps; ammunition comes directly from reserves.',
         action_en='Each burst heats the heat sink. Fins cool between bursts; a full gauge forces a long vent.',
         fire_en='Bursts of plasma bolts; venting in the middle gauge range shortens the firing pause.'))
