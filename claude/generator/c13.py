"""KC13 „Glasspalt“: eine offene Stimmgabel mit freiem linearem Strahlkanal."""
from eng import rect, roundpoly
from tlib import B, rail, trigger_group

KO, BA, AZ, DK = '#B85C58', '#343A41', '#71CFFF', '#191D26'


def model():
    b = B()
    D = b.D
    # Der Schaft hat ein echtes langes Fenster, keine aufgemalte Aussparung.
    b.P([(63,261),(96,243),(142,243),(203,257),(230,266),(232,285),
         (201,282),(140,263),(103,263),(76,280)],KO,-16,16,r=9,L='Schaft')
    b.P([(72,330),(109,330),(153,315),(200,283),(228,280),(230,303),
         (164,340),(115,353),(73,350)],BA,-16,16,r=9,L='Schaftunterbogen')
    b.P([(59,258),(74,257),(83,341),(72,360),(56,350),(50,279)],
        DK,-19,19,r=8,L='Schaftkappe')
    b.P([(219,259),(260,239),(336,233),(421,241),(469,260),
         (491,285),(478,316),(436,338),(269,343),(221,320)],
        KO,-25,25,r=10,L='Gehäuse',
        dec=[D(roundpoly([(243,278),(274,258),(342,252),(399,258),
                          (411,271),(394,287),(273,294)],7),BA),
             D(roundpoly([(262,273),(285,265),(342,260),(389,265),
                          (390,272),(343,270),(286,275)],3),AZ,True)])
    b.P([(260,239),(272,214),(423,214),(437,241),(432,249),
         (325,244),(265,252)],BA,-14,14,r=7,L='Schienensockel')
    rail(b,272,423,214,BA,KO,w=10)
    # Drei Kammern folgen dem geteilten Gabelansatz.
    b.P([(476,261),(515,248),(573,250),(615,267),(620,309),
         (581,327),(523,332),(479,318)],BA,-23,23,r=9,L='Kondensatorkammern',
        dec=[D(roundpoly([(492+35*i,273),(511+35*i,273),
                          (515+35*i,306),(494+35*i,310)],5),DK) for i in range(3)]+
            [D(roundpoly(rect(498+35*i,280,10,21),4),AZ,True) for i in range(3)])
    # Die Schienen biegen zuerst auseinander, dann zum Emitter zurück.
    b.P([(604,264),(648,241),(711,224),(780,225),(846,246),
         (887,266),(884,278),(867,279),(838,263),(776,243),
         (715,243),(655,258),(612,282)],KO,-13,13,r=9,L='Beschleunigerschiene',
        dec=[D(roundpoly([(645,252),(713,231),(777,232),(832,249),
                          (775,239),(714,239),(649,259)],3),AZ,True)])
    b.P([(611,300),(653,320),(714,337),(776,337),(838,318),
         (867,302),(885,302),(889,314),(848,335),(782,355),
         (709,355),(646,337),(605,318)],KO,-13,13,r=9,L='Beschleunigerschiene',
        dec=[D(roundpoly([(646,327),(713,347),(777,347),(831,330),
                          (775,340),(714,341),(650,320)],3),AZ,True)])
    b.C(610,903,290,5,AZ,n=10,emit=True,L='Linearkern')
    # Echte offene Ringe in yz: nur Kappen und schmale seitliche Stege.
    for x,top,bottom in ((660,237,343),(752,220,360),(842,241,339)):
        b.P(rect(x,top,16,12),BA,-25,25,r=6,L='Spulenringe')
        b.P(rect(x,bottom-12,16,12),BA,-25,25,r=6,L='Ringunterseite')
        for z0,z1 in ((19,25),(-25,-19)):
            b.P([(x,top+6),(x+16,top+6),(x+16,bottom-6),(x,bottom-6)],
                BA,z0,z1,r=6,L='Ringsteg')
    b.F(884,909,290,25,15,BA,n=12,L='Emitter')
    b.C(909,922,290,15,DK,n=12,L='Emitter',
        cap=[(290,0,9,AZ,True)])
    b.P([(421,336),(479,328),(499,345),(491,398),(471,410),(432,401)],
        BA,-19,19,r=9,L='Energiezelle',
        dec=[D(roundpoly([(440+14*i,349),(448+14*i,348),
                          (447+14*i,387),(439+14*i,386)],3),AZ,True) for i in range(3)])
    b.P([(288,337),(330,337),(340,363),(314,432),(291,443),
         (266,430),(287,382)],BA,-19,19,r=9,L='Griff',
        dec=[D(roundpoly([(297,360),(315,361),(303,407),(289,424),
                          (283,414)],5),DK)])
    trigger_group(b,350,339,AZ,BA,grip_x0=324,depth=38)
    b.P([(544,325),(578,325),(588,348),(571,396),(551,408),
         (533,395),(546,356)],BA,-15,15,r=9,L='Vordergriff')
    return b.m


META = dict(
    num='13', name='Lineares Fusionsgewehr', nick='GLASSPALT', col=AZ,
    pill='KORALLROT · BASALT · AZUR', palette=[KO,BA,AZ,DK], center=(485,326,0),
    desc='Zwei korallrote Bögen bilden eine lange Stimmgabel um den freien azurblauen Linearkern. '
         'Drei offene Spulenringe fassen die Gabel; drei Kondensatorkammern speisen sie aus dem breiten Heckkörper. '
         'Die schwere Energiezelle sitzt vor dem Abzug.',
    form='Offener Schaft · gespaltener Gabelkörper · drei Kondensatorkammern · zwei gebogene Beschleunigerschienen · '
         'freier Linearkern · drei offene Spulenringe · Emitter · Energiezelle · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Schwere Energiezelle vor dem Abzug nach unten ziehen und eine neue Zelle für fünf Schuss einsetzen',
        action_de='Abzug halten: drei Kondensatorkammern laden nacheinander; beide Schienen fahren beim Aufladen auseinander',
        fire_de='Nach vollem Aufladen loslassen: ein einzelner durchschlagender Linearstrahl folgt dem freien Kanal',
        reload_en='pull the heavy energy cell ahead of the trigger down and insert a fresh five-shot cell',
        action_en='hold the trigger: three capacitor chambers charge in sequence; the two accelerator rails spread apart',
        fire_en='release after a full charge to fire one piercing linear beam along the open channel'))
