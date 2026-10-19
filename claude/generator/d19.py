"""KD19 „Dornwerk“: gedrungene Armbrust mit dicken, nach hinten gezogenen D-Wurfarmen."""
import math
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#39BFA8', '#CBFFF1'
BY = 250


def _string(b,p0,p1):
    dx,dz=p1[0]-p0[0],p1[1]-p0[1]
    length=math.hypot(dx,dz); nx,nz=-dz/length*1.8,dx/length*1.8
    b.Y([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),
         (p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],A,BY-2,BY+2,L='Sehne')


def model():
    b = B(); D = b.D
    b.P([(82,252),(178,252),(246,272),(246,334),(184,334),(114,358),(82,358)],
        DK,-25,25,r=12,L='Schaft',
        dec=[D(roundpoly(rect(100,268,94,22),8),P),D(roundpoly(rect(102,306,72,12),5),K)])
    b.P(rect(70,246,20,122),K,-28,28,r=8,L='Schaftkappe')
    b.P(rect(114,238,98,24),DK,-21,21,r=10,L='Wangenauflage',
        dec=[D(roundpoly(rect(128,243,70,9),4),P)])
    b.P([(230,260),(574,258),(606,276),(606,334),(246,334),(230,318)],
        DK,-28,28,r=12,L='Gehäuse',
        dec=[D(roundpoly(rect(250,276,182,24),9),P),
             D(roundpoly(rect(464,278,104,10),5),A,True),D(roundpoly(rect(254,314,174,9),4),K)])
    rail(b,252,364,260,K,DK,w=13)
    b.P(rect(384,BY+3,240,10),K,-7,7,r=4,L='Führungsrinne')
    b.P(rect(378,234,38,28),K,-22,22,r=9,L='Schloss',
        dec=[D(roundpoly(rect(386,240,22,10),4),A,True)])
    b.C(396,662,BY,4.5,AL,n=10,L='Bolzen')
    b.F(662,690,BY,9,1,A,n=10)
    b.P([(398,BY),(426,BY-12),(440,BY)],A,-1,1,r=2)
    b.P(rect(572,256,60,80),K,-34,34,r=12,L='Bogenblock',
        dec=[D(roundpoly(rect(584,280,34,32),10),P),D(roundpoly(rect(594,289,14,14),6),A,True)])
    # Einteilige breite Recurve-Bögen statt der schmalen G-Segmente.
    for s in (-1,1):
        b.Y([(590,24*s),(632,24*s),(646,56*s),(632,116*s),(582,174*s),
             (550,170*s),(580,118*s),(596,72*s)],
            DK,BY-7,BY+15,r=12,L='Wurfarm',
            dec=[D(roundpoly([(604,42*s),(624,44*s),(630,66*s),(616,112*s),
                              (576,158*s),(566,158*s),(596,108*s),(610,68*s)],7),P),
                 D(roundpoly([(608,62*s),(618,64*s),(606,110*s),(574,150*s),
                              (570,146*s),(598,104*s)],4),A,True)])
        _string(b,(566,164*s),(396,2*s))
    b.P(rect(422,302,176,16),A,28,42,r=7,L='Spannhebel')
    b.P(circ(594,310,13,14),DK,26,46,
        dec=[D(circ(594,310,6,12),P)])
    b.P([(280,332),(336,332),(350,422),(292,428)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(298,352),(320,352),(330,404),(308,408)],7),DK)])
    b.P(arcband(336,440,334,62,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(358,334),(372,334),(382,366),(368,370)],A,-6,6,r=4,L='Abzug')
    b.P([(480,332),(526,332),(522,394),(486,394)],K,-19,19,r=12,L='Vordergriff')
    return b.m


META=dict(num='19',name='Schwere Armbrust',nick='DORNWERK',col=A,
 pill='JADE-SKIN',palette=[P,DK,A,AL],center=(380,330,0),
 desc='Eine gedrungene schwere Armbrust kombiniert einen tiefen Schulterblock mit zwei breiten, weich zurückgezogenen Recurve-Wurfarmen. Jadegrüne Sehnenhälften laufen zum Schloss hinter dem hellen Bolzen; der Spannhebel sitzt links am massiven Bogenblock und der Abzug bleibt frei zugänglich.',
 form='Tiefer Schaft mit Wangenauflage · kompaktes Rundgehäuse · hintere Visierschiene · Schloss · Führungsrinne mit Bolzen · massiver Bogenblock · zwei breite Recurve-Wurfarme · zwei Sehnenhälften · Spannhebel links · freier Abzugsbügel · Vordergriff',
 op=dict(reload_de='Linken Spannhebel am vorderen Drehpunkt nach vorn-unten schwenken: Sehne ins Schloss ziehen, dann einen Bolzen in die Führungsrinne legen.',
         action_de='Ein Bolzen je Spannung; der verschossene Bolzen bleibt am Trefferort und kann wieder aufgenommen werden.',
         fire_de='Einzelschuss mit hoher Durchschlagskraft; je nach Ausführung Explosiv- oder Widerhaken-Bolzen.',
         reload_en='Swing the left cocking lever forward and down on its front pivot to draw the string into the latch, then lay a bolt in the flight groove.',
         action_en='One bolt per draw; the fired bolt stays at the impact point and can be retrieved to replenish the reserve.',
         fire_en='Single high-impact shot; explosive or serrated bolts depending on the build.'))
