"""KG13 Lineares Fusionsgewehr „Lichtlinie“ (claude-0.10): schwere Präzisions-Energiewaffe mit Beschleunigerschienen.
Unterschied zum Fusionsgewehr (KX07): ein einzelner gebündelter Strahl über eine lange offene Schienenstrecke statt Streuladung aus
einem kurzen Emitter; Aufladen über drei Kondensatorkammern, Zielfernrohr wie das Scharfschützengewehr, schwere Energiezelle."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.P([(66,262),(96,256),(204,266),(204,302),(156,320),(72,342)],AN,-14,14,r=6,L='Schaft',
        dec=[D(roundpoly(rect(104,276,70,10),3),DK)])
    b.P(rect(56,252,14,98),DK,-16,16,r=4,L='Schaftkappe')
    b.P([(200,250),(474,246),(504,258),(504,326),(474,336),(200,336)],CR,-24,24,r=8,L='Gehäuse',
        dec=[D(roundpoly([(204,314),(500,314),(500,324),(474,334),(204,334)],3),AN),
             D(roundpoly(rect(226,266,150,22),5),AN),D(roundpoly(rect(236,273,130,8),3),CY,True)])
    rail(b,228,470,246,AN,DK)
    # Kondensatorkammern: drei leuchtende Fenster im Ladeblock
    b.P([(504,256),(612,260),(612,324),(504,330)],AN,-22,22,r=6,L='Kondensatorkammern',
        dec=[D(roundpoly(rect(516+32*i,274,22,36),4),DK) for i in range(3)]+[D(roundpoly(rect(520+32*i,278,14,28),3),CY,True) for i in range(3)])
    # Beschleunigerschienen oben und unten, Linearkern dazwischen, Spulenringe halten sie zusammen
    b.P(rect(612,262,262,13),CR,-11,11,r=4,L='Beschleunigerschiene',dec=[D(rect(640+40*i,266,18,4),AN) for i in range(6)])
    b.P(rect(612,305,262,13),CR,-11,11,r=4,L='Beschleunigerschiene',dec=[D(rect(640+40*i,309,18,4),AN) for i in range(6)])
    b.C(612,890,290,6,CY,n=8,emit=True,L='Linearkern')
    for k,x in enumerate((650,740,830)):   # offene Ringe: oben, unten, zwei Seitenwangen; Linearkern läuft frei hindurch
        b.P(rect(x,252,16,12),AN,-16,16,r=3,L='Spulenringe' if k==0 else None)
        b.P(rect(x,316,16,12),AN,-16,16,r=3)
        for z0,z1 in ((12,16),(-16,-12)):b.P(rect(x,252,16,76),AN,z0,z1,r=2)
    b.F(874,904,290,22,13,AN,L='Emitter')
    b.C(904,914,290,12,DK,n=8,cap=[(290,0,7,CY,True)])
    # Energiezelle vor dem Abzug, Griff, Abzug, Vordergriff unter dem Ladeblock
    b.P([(430,334),(500,334),(500,388),(438,388)],AN,-18,18,r=5,L='Energiezelle',
        dec=[D(roundpoly(rect(444+14*i,348,8,26),2),CY,True) for i in range(4)])
    grip(b,300,336,AN,DK,h=92,w=48,lean=16)
    trigger_group(b,358,336,OR,AN,grip_x0=338,depth=34)
    b.P([(540,328),(576,328),(570,392),(546,392)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='13',name='Lineares Fusionsgewehr',nick='LICHTLINIE',col='#6FD8E0',pill='CREME · ANTHRAZIT · CYAN',
 palette=[CR,AN,CY,OR],center=(485,300,0),
 desc='Schwere Präzisions-Energiewaffe: Hinter dem langen cremefarbenen Gehäuse laden drei Kondensatorkammern den Schuss auf, dann jagt ein einzelner gebündelter Strahl über die offene Strecke zwischen zwei Beschleunigerschienen. Drei Spulenringe halten die Schienen, vorne bündelt der Emitter den Strahl.',
 form='Skelettschaft · langes Gehäuse · Ladeblock mit drei Kondensatorkammern · zwei Beschleunigerschienen mit Linearkern · drei Spulenringe · Emitter · schwere Energiezelle vor dem Abzug · Vordergriff',
 op=dict(reload_de='schwere Energiezelle vor dem Abzug nach unten ziehen und neu einsetzen (5 Schuss)',
         action_de='Abzug halten: die drei Kondensatorkammern leuchten nacheinander auf, die Schienen fahren auseinander (Aufladen ca. 0,5 s)',
         fire_de='beim Loslassen nach vollem Aufladen ein einzelner durchschlagender Linearstrahl',
         reload_en='pull the heavy energy cell ahead of the trigger down and seat a new one (5 shots)',
         action_en='hold the trigger: the three capacitor chambers light up in turn and the rails spread apart (charge about 0.5 s)',
         fire_en='release after full charge for one piercing linear beam'))
