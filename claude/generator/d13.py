"""KD13 „Kernwucht“: kompakter, schwerer D-Ladeblock vor einer offenen Linearstrecke."""
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#B6E65A', '#EAFFD3'


def model():
    b = B(); D = b.D
    # Tiefer, kompakter Schulterblock statt des langen G-Skelettschafts.
    b.P([(66,238),(168,238),(220,256),(220,318),(170,318),(108,346),(66,346)],
        DK,-24,24,r=12,L='Schaft',
        dec=[D(roundpoly(rect(82,250,88,24),9),P),D(roundpoly(rect(86,287,64,10),4),K)])
    b.P(rect(54,232,20,124),K,-27,27,r=8,L='Schaftkappe')
    b.P([(208,222),(448,212),(486,232),(486,340),(228,340),(208,320)],
        DK,-34,34,r=12,L='Gehäuse',
        dec=[D(roundpoly([(228,236),(408,226),(438,238),(438,276),(228,286)],10),P),
             D(roundpoly(rect(244,250,152,10),5),A,True),
             D(roundpoly(rect(244,308,166,13),6),K)])
    rail(b,244,414,224,K,DK,w=14)
    # Drei einzelne Kammerfenster in einem breiten, weich eingefassten Ladeblock.
    b.P([(460,222),(552,222),(584,246),(584,322),(560,344),(460,344)],
        P,-38,38,r=12,L='Kondensatorkammern',
        dec=[D(roundpoly(rect(474+30*i,246,22,66),10),K) for i in range(3)]+
            [D(roundpoly(rect(480+30*i,254,10,48),5),A,True) for i in range(3)]+
            [D(roundpoly(rect(483+30*i,262,4,30),2),AL,True) for i in range(3)])
    # Zwei vollständige bewegliche Schienen. Die Ringe haben echte freie Öffnungen.
    for y in (242,320):
        b.P(rect(576,y,220,18),P,-12,12,r=8,L='Beschleunigerschiene',
            dec=[D(roundpoly(rect(592+46*i,y+6,28,6),3),A,True) for i in range(4)])
    b.C(576,822,290,6,AL,n=12,emit=True,L='Linearkern')
    for x in (614,684,754):
        b.P(rect(x,228,18,16),DK,-26,26,r=6,L='Spulenringe')
        b.P(rect(x,336,18,16),DK,-26,26,r=6,L='Spulenringe')
        for z0,z1 in ((20,26),(-26,-20)):
            strip = D(roundpoly(rect(x+5,270,8,36),4),A,True)
            b.P(rect(x,228,18,124),DK,z0,z1,r=5,L='Spulenringe',
                dec=[strip] if z0>0 else (),
                xdec=[('z-',z0,*strip)] if z0<0 else ())
    # Vier Wangen des Emitters lassen auch an der Mündung den Strahlkanal frei.
    b.P(rect(792,240,34,28),K,-28,28,r=8,L='Emitter')
    b.P(rect(792,312,34,28),K,-28,28,r=8,L='Emitter')
    for z0,z1 in ((18,28),(-28,-18)):
        strip = D(roundpoly(rect(802,272,12,36),6),A,True)
        b.P(rect(792,240,34,100),K,z0,z1,r=8,L='Emitter',
            dec=[strip] if z0>0 else (),
            xdec=[('z-',z0,*strip)] if z0<0 else ())
    # Zelle vor dem freien Abzugsraum, Griff und gebogener D-Bügel.
    b.P([(448,338),(508,338),(504,418),(454,418)],K,-22,22,r=10,L='Energiezelle',
        dec=[D(roundpoly(rect(464,354,28,44),9),A,True),D(roundpoly(rect(472,362,12,26),5),AL,True)])
    b.P([(276,336),(330,336),(348,432),(290,438)],K,-21,21,r=12,L='Griff',
        dec=[D(roundpoly([(298,356),(312,356),(326,410),(312,412)],6),DK)])
    b.P(arcband(330,430,338,64,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(350,339),(363,339),(372,381),(359,385)],A,-6,6,r=4,L='Abzug')
    b.P([(550,340),(582,336),(578,402),(554,406)],DK,-15,15,r=10,L='Vordergriff')
    return b.m


META=dict(num='13',name='Lineares Fusionsgewehr',nick='KERNWUCHT',col=A,
 pill='STRAND-VERSION',palette=[P,DK,A,AL],center=(440,325,0),
 desc='Ein kompakter, schwer gerundeter Ladeblock lädt drei limettengrüne Kondensatorkammern auf. Zwei helle Beschleunigerschienen führen den einzelnen Linearstrahl durch offene Spulenringe zum vierteiligen Emitter; die schwere Energiezelle sitzt vor dem freien Abzugsraum.',
 form='Tiefer Schulterblock · gerundetes Gehäuse mit heller Deckplatte · drei Kondensatorkammern · zwei Beschleunigerschienen · freier Linearkern · offene Spulenringe · offener Emitter · Energiezelle vor dem Abzug · gebogener Bügel',
 op=dict(reload_de='Schwere Energiezelle vor dem Abzug nach unten ziehen und neu einsetzen (5 Schuss).',
         action_de='Abzug halten: drei Kondensatorkammern leuchten nacheinander; beide Beschleunigerschienen fahren auseinander (ca. 0,5 s).',
         fire_de='Nach voller Ladung loslassen: ein einzelner durchschlagender Linearstrahl durch den offenen Emitter.',
         reload_en='Pull the heavy energy cell ahead of the trigger down and seat a new one (5 shots).',
         action_en='Hold the trigger: three capacitor chambers light up in turn; both accelerator rails spread apart (about 0.5 s).',
         fire_en='Release after full charge for one piercing linear beam through the open emitter.'))
