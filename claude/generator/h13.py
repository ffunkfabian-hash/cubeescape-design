"""KH13 „Richtbank“: lineare Werkstatt-Energiewaffe mit offener, dreifach geklammerter Schienenbank."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

BL, LI, DK, HL = '#496B82', '#BDD15A', '#1C2B38', '#DFE8E1'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    b.C(68,260,288,10,DK,n=12,L='Schaft')
    b.C(156,266,288,14,BL,n=12,L='Rohrschaft')
    b.C(148,168,288,19,LI,n=10,L='Schaftklemmring')
    b.P(rect(52,276,22,112),DK,-20,20,r=4,L='Schaftkappe',
        dec=[D(rect(58,290+18*i,10,6),BL) for i in range(5)])
    b.P(rect(96,268,100,14),HL,-14,14,r=3,L='Wangenauflage')
    b.P(rect(102,280,88,10),LI,-12,12,r=2,L='Wangenhalter')
    # Kurzes, hohes Maschinenbett und seitlich sichtbar verschraubte Fuge.
    b.P([(252,248),(458,248),(482,268),(482,296),(252,296)],BL,-27,27,r=4,L='Gehäuse',
        dec=[D(roundpoly(rect(314,262,96,12),3),HL)])
    b.P([(252,299),(482,299),(482,346),(458,358),(252,358)],DK,-27,27,r=4,L='Untergehäuse')
    for x in (270,438):
        for z0,z1 in ((27,33),(-33,-27)):
            screws=bolts([(x+11,283),(x+11,331)])
            b.P(rect(x,274,22,66),LI,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    rail(b,306,426,248,DK,HL,w=11)
    # Drei einzeln gefasste Kondensatoren, keine flache Fensterreihe im Gehäuse.
    b.P(rect(480,274,110,57),BL,-23,23,r=3,L='Ladeblock')
    for x in (488,522,556):
        b.P(rect(x,261,26,82),DK,-26,26,r=3,L='Kondensatorkammern',
            dec=[D(roundpoly(rect(x+6,274,14,54),3),LI,True)])
        b.P(rect(x-2,258,30,11),HL,-28,28,r=2,L='Kondensatorhalter')
        b.P(rect(x-2,335,30,11),HL,-28,28,r=2,L='Kondensatorhalter')
    # Schienen sind zwei eigenständige bewegliche Baugruppen; dazwischen bleibt Luft.
    b.P(rect(588,263,276,14),HL,-12,12,r=3,L='Beschleunigerschiene',
        dec=[D(rect(614+40*i,267,22,5),BL) for i in range(6)])
    b.P(rect(588,323,276,14),HL,-12,12,r=3,L='Beschleunigerschiene',
        dec=[D(rect(614+40*i,327,22,5),BL) for i in range(6)])
    b.C(584,884,300,5,LI,n=8,emit=True,L='Linearkern')
    # Offene Rechteckringe: je ein oberer/unterer Steg und zwei seitliche Wangen.
    for x in (624,720,816):
        b.P(rect(x,251,18,14),BL,-22,22,r=2,L='Spulenringe')
        b.P(rect(x,335,18,14),BL,-22,22,r=2,L='Spulenringe')
        for z0,z1 in ((17,22),(-22,-17)):
            screws=bolts([(x+9,259),(x+9,341)])
            b.P(rect(x,251,18,98),BL,z0,z1,r=2,L='Spulenringe',
                dec=screws if z0>0 else (),xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    b.F(860,896,300,25,15,BL,n=8,L='Emitter')
    b.C(892,908,300,15,LI,n=8,L='Mündungsring',cap=[(300,0,8,DK,False),(300,0,5,LI,True)])
    # Abzugsbügel endet bei x400, die Zelle beginnt bei x422.
    grip(b,270,358,DK,BL,h=94,w=49,lean=13)
    b.P(rect(336,355,16,8),DK,-7,7,r=2,L='Abzugslager')
    trigger_group(b,336,358,LI,DK,grip_x0=310,depth=32)
    b.P(rect(418,346,67,18),LI,-20,20,r=3,L='Zellhalter',
        dec=bolts([(429,355),(474,355)]))
    b.P([(424,362),(478,362),(474,423),(418,423)],BL,-19,19,r=4,L='Energiezelle',
        dec=[D(roundpoly(rect(432+13*i,374,7,34),2),LI,True) for i in range(3)])
    b.P(rect(538,344,30,18),LI,-16,16,r=2,L='Vordergriffhalter')
    b.P([(536,357),(572,357),(568,415),(542,415)],DK,-14,14,r=4,L='Vordergriff',
        dec=[D(rect(546,370+11*i,17,4),BL) for i in range(3)])
    return b.m


META=dict(num='13',name='Lineares Fusionsgewehr',nick='RICHTBANK',col=LI,
 pill='STAHLBLAU · LIMETTE · DUNKEL',palette=[BL,LI,DK,HL],center=(480,337,0),
 desc='Eine schwere lineare Energiewaffe wie eine tragbare Richtbank: Drei einzeln geklammerte Kondensatoren stehen vor dem kurzen Maschinengehäuse. Zwei helle Beschleunigerschienen führen den freien Linearkern durch drei offene Rahmenringe zum Emitter; stahlblaue Module und limettfarbene Klemmplatten verbinden die Baugruppen.',
 form='Rohrschaft mit Klemmring · hohes geklemmtes Gehäuse · drei gefasste Kondensatorkammern · obere und untere Beschleunigerschiene · freier Linearkern · drei offene Spulenringe · Emitter · Energiezelle vor dem Abzug · Vordergriff',
 op=dict(reload_de='Die schwere Energiezelle vor dem Abzug nach unten aus dem geklemmten Halter ziehen und eine volle Zelle einsetzen; fünf Schuss.',
         action_de='Abzug halten: Drei Kondensatorkammern laden nacheinander, die obere und untere Schiene fahren auseinander; Ladezeit etwa 0,5 Sekunden.',
         fire_de='Nach voller Ladung loslassen: Ein einzelner durchschlagender Linearstrahl verlässt den vorderen Emitter.',
         reload_en='Pull the heavy energy cell down from its clamp ahead of the trigger and insert a full cell; capacity is five shots.',
         action_en='Hold the trigger: three capacitor chambers charge in sequence while the upper and lower rails spread apart; charge takes about 0.5 seconds.',
         fire_en='Release at full charge to send one piercing linear beam through the front emitter.'))
