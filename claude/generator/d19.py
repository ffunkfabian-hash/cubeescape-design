"""KD19 „Dornwerk“: dunkle Recurve-Armbrust mit offenem Heck und breitem, gepanzertem Querbogen."""
import math
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#3A3D44', '#1C2027', '#39BFA8', '#CBFFF1'
BY = 250


def _string(b,p0,p1):
    dx,dz=p1[0]-p0[0],p1[1]-p0[1]
    length=math.hypot(dx,dz); nx,nz=-dz/length*1.8,dx/length*1.8
    b.Y([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),
         (p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],A,BY-2,BY+2,L='Sehne')


def model():
    b = B(); D = b.D
    # Offener, abgerundeter Heckrahmen statt des geschlossenen D-Schulterblocks.
    b.P([(82,252),(174,252),(252,270),(252,292),(174,280),(82,282)],
        DK,-23,23,r=10,L='Schaft')
    b.P([(84,326),(164,326),(232,300),(250,312),(178,350),(84,350)],
        DK,-23,23,r=10,L='Schaft')
    b.P(rect(70,246,22,112),K,-27,27,r=10,L='Schaftkappe')
    b.P(rect(110,240,100,22),P,-24,24,r=10,L='Wangenauflage')
    b.P([(230,260),(568,260),(610,280),(610,326),(248,330),(230,314)],
        DK,-29,29,r=12,L='Gehäuse')
    for z0,z1 in ((28,36),(-36,-28)):
        b.P([(254,276),(424,276),(438,290),(424,304),(254,304)],P,z0,z1,r=10,L='Deckplatte')
        ds=[D(roundpoly(rect(472,288,72,8),4),A,True)]
        b.P(rect(458,280,100,26),K,z0,z1,r=9,L='Führungswange',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    rail(b,252,364,260,K,DK,w=14)
    b.P(rect(384,BY+3,240,10),K,-7,7,r=4,L='Führungsrinne')
    b.P(rect(378,240,40,22),K,-23,23,r=10,L='Schloss',
        dec=[D(roundpoly(rect(386,245,24,9),4),A,True)])
    b.C(396,662,BY,4.5,AL,n=10,L='Bolzen')
    b.F(662,690,BY,9,1,A,n=10,L='Bolzen')
    b.P([(398,BY),(426,BY-12),(440,BY)],A,-1,1,r=2,L='Bolzenfeder')
    b.P([(564,258),(622,258),(638,282),(638,338),(614,352),(564,338)],
        DK,-35,35,r=12,L='Bogenblock')
    b.P(rect(570,326,58,26),P,-38,38,r=10,L='Bogenklemme')
    # Einteilige schwere Recurve-Arme ziehen deutlich zum Schützen zurück.
    for s in (-1,1):
        b.Y([(570,24*s),(626,24*s),(654,66*s),(632,128*s),(532,206*s),
             (490,210*s),(518,172*s),(588,116*s),(600,72*s)],
            DK,BY-4,BY+24,r=12,L='Wurfarm')
        b.Y([(586,44*s),(614,44*s),(634,70*s),(614,122*s),(526,192*s),
             (512,192*s),(536,162*s),(602,110*s),(612,70*s)],
            P,BY-10,BY+1,r=10,L='Wurfarmplatte',
            dec=[D(roundpoly([(604,62*s),(614,66*s),(602,116*s),(528,182*s),
                              (522,178*s),(592,110*s)],4),A,True)])
        b.Y([(598,52*s),(634,50*s),(642,70*s),(630,86*s),(602,82*s)],
            K,BY-10,BY+30,r=8,L='Wurfarmklemme')
        b.Y([(486,194*s),(518,186*s),(530,206*s),(504,220*s),(488,214*s)],
            K,BY-8,BY+28,r=8,L='Sehnenanker')
        _string(b,(504,202*s),(396,2*s))
    b.P(rect(416,310,184,16),A,29,45,r=7,L='Spannhebel')
    b.P(circ(594,318,17,16),K,28,49,L='Hebeldrehpunkt',
        dec=[D(circ(594,318,8,12),P)])
    b.P(rect(414,306,30,26),K,43,54,r=8,L='Hebelgriff')
    b.P([(280,328),(336,328),(350,422),(292,428)],K,-24,24,r=12,L='Griff')
    for z0,z1 in ((23,29),(-29,-23)):
        b.P([(294,348),(320,348),(334,402),(309,408)],DK,z0,z1,r=8,L='Griffschale')
    b.P(arcband(336,440,326,62,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(358,326),(372,326),(382,364),(368,368)],A,-6,6,r=4,L='Abzug')
    b.P([(480,326),(526,326),(522,394),(486,394)],K,-20,20,r=12,L='Vordergriff')
    return b.m


META=dict(num='19',name='Schwere Armbrust',nick='DORNWERK',col=A,
 pill='JADE-SKIN',palette=[DK,P,A,AL],center=(380,330,0),
 desc='Ein offener dunkler Heckrahmen trägt das gedrungene Armbrustgehäuse. Vorn breitet sich ein schwerer Querbogen mit weit zurückgezogenen Recurve-Armen aus; helle Wurfarmplatten und dunkle Wurzelklemmen zeigen den Aufbau. Jadegrüne Sehnen laufen von dicken Endankern zum Schloss hinter dem hellen Bolzen; der Spannhebel sitzt links am vorderen Drehpunkt.',
 form='Offener dunkler Heckrahmen · helle Wangenauflage und Deckplatten · hintere Schiene · Schloss und Bolzenrinne · massiver Querblock · breite Recurve-Wurfarme mit hellen Schalen · Wurzelklemmen · Sehnenanker · zwei Sehnenhälften · linker Spannhebel · freier Abzug',
 op=dict(reload_de='Linken Spannhebel am vorderen Drehpunkt nach vorn-unten schwenken: Sehne ins Schloss ziehen, dann einen Bolzen in die Führungsrinne legen.',
         action_de='Ein Bolzen je Spannung; der verschossene Bolzen bleibt am Trefferort und kann wieder aufgenommen werden.',
         fire_de='Einzelschuss mit hoher Durchschlagskraft; je nach Ausführung Explosiv- oder Widerhaken-Bolzen.',
         reload_en='Swing the left cocking lever forward and down on its front pivot to draw the string into the latch, then lay a bolt in the flight groove.',
         action_en='One bolt per draw; the fired bolt stays at the impact point and can be retrieved to replenish the reserve.',
         fire_en='Single high-impact shot; explosive or serrated bolts depending on the build.'))
