from flib import *
from flabel import Lb
from gsight import S,late
from eng import rect,circ,roundpoly
BE,AN,OR,CY,DK='#D9C7A3','#33363D','#F26A1B','#6FD8E0','#1E2025'
def spec():
    return [
    # Skelettschaft: Kappe, obere und untere Strebe
    P(rect(86,250,14,102),BE,-20,20,r=4),
    Lb(P([(98,256),(200,262),(200,284),(98,280)],AN,-11,11,r=4),'Schaft'),
    P([(98,322),(200,314),(200,336),(98,348)],AN,-11,11,r=4),
    # Gehäuse
    Lb(P([(196,250),(440,244),(472,262),(472,330),(440,342),(196,342)],BE,-26,26,r=8,
      dec=[D(roundpoly([(200,318),(468,318),(468,328),(440,340),(200,340)],3),AN),
           D(roundpoly(rect(226,280,190,22),5),AN),
           D(roundpoly(rect(234,287,174,8),3),OR,True)]),'Gehäuse'),
    # Energiezelle oben eingesetzt
    Lb(P(rect(230,228,142,18),AN,-18,18,r=4,dec=[D(roundpoly(rect(240+22*i,233,14,8),2),DK) for i in range(5)]),'Energiezelle'),
    P(rect(352,231,16,10),OR,-18.8,18.8,r=2,emit=True),
    # Zielfernrohr auf zwei Ringen mit Füßen (Erstentwurf; das XL-Blatt ersetzt die Visierteile durch VS08, vsmount.apply)
    P(rect(382,240,62,6),DK,-9,9,r=2),  # Visierbasis (bleibt)
    S(P(rect(388,228,14,13),AN,-7,7,r=2)),
    S(P(rect(424,228,14,13),AN,-7,7,r=2)),
    S(P(rect(390,198,10,32),AN,-16,16,r=3)),
    S(P(rect(426,198,10,32),AN,-16,16,r=3)),
    S(Lb(C(366,494,214,14,AN,n=8,cap=[(214,0,9,CY,True)]),'Zielfernrohr')),
    S(C(348,366,214,10,DK,n=8)),
    # Handschutz, sichtbarer Lauf, Fächeremitter
    P([(472,272),(560,276),(560,320),(472,326)],BE,-20,20,r=6,dec=[D(roundpoly(rect(484+18*i,288,10,22),3),AN) for i in range(4)]),
    C(560,610,298,9,DK,n=8),
    Lb(P([(604,284),(654,266),(654,330),(604,312)],AN,-32,32,r=4,
      xdec=[('x+',654,roundpoly(rect(293,-27,10,54),3),OR,True)]),'Fächeremitter'),
    P(rect(600,280,10,36),DK,-22,22,r=2),
    # Griff, Abzug, Bügel
    Lb(P([(318,342),(368,342),(358,442),(304,442)],AN,-18,18,r=6,dec=[D(roundpoly(rect(320,362+12*i,32,5),2),DK) for i in range(5)]),'Griff'),
    Lb(P([(380,343),(392,343),(404,384),(392,388)],OR,-6,6,r=2),'Abzug'),
    P(rect(366,404,72,9),AN,-7,7,r=3),
    P(rect(430,342,9,71),AN,-7,7,r=3),
    # Vordergriff (claude-0.15.1): unter Gehäusefront und Handschutz, Mitte x 472 = 0,25 m vor dem Griff (wie Toolgen-Korrektur KG02)
    late(Lb(P([(458,322),(486,322),(486,392),(480,400),(464,400),(458,392)],AN,-14,14,r=4,
      dec=[D(roundpoly(rect(463,340+12*i,18,5),2),DK) for i in range(4)]),'Vordergriff')),
    ]
META=dict(num='08',name='Spurgewehr',vname='Fächer',col='#F26A1B',pill='BEIGE · ANTHRAZIT · ORANGE',
 palette=[BE,AN,OR,CY],center=(370,300,0),
 aria='Spurgewehr Variante G: beigefarbenes Gehäuse mit oben eingesetzter Energiezelle, Zielverfolgungs-Visier mit Markierungsrahmen, kurzem Lauf und breitem flachem Fächeremitter mit orangem Strahlschlitz, Skelettschaft',
 desc='Das Spurgewehr spannt seinen Strahl wie einen Fächer auf: Vorne sitzt ein breiter, flacher Emitter mit orangem Schlitz. Die Energiezelle steckt oben im beigen Gehäuse, darüber sitzt das Zielverfolgungs-Visier mit offenem Markierungsrahmen.',
 form='Skelettschaft · Energiezelle oben im Gehäuse · Zielverfolgungs-Visier auf der Visierbasis · belüfteter Handschutz · sichtbarer Lauf · breiter Fächeremitter',
 desc3='Der Fächer als Konzeptblatt: Die Energiezelle liegt oben eingesetzt im Gehäuse, ihre orange Ladeanzeige zeigt nach vorne. Das Zielverfolgungs-Visier sitzt ohne Röhre auf der Visierbasis: ein Leichtbau-Rahmen mit vier Markierungsecken. Vorne tritt der kurze Lauf aus dem Handschutz in den breiten Fächeremitter, dessen orangener Schlitz den flachen Strahl formt. Unten liegt der Abzug im Bügel vor dem Griff.')
