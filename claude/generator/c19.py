"""KC19 „Flügelrad“: schwere Armbrust mit offenen Schaftbögen und weit geschwungenen Querarmen."""
import math
from eng import rect, roundpoly, circ
from tlib import B, rail, trigger_group

ST, RO, PI, DK = '#3C6982', '#A86574', '#D8EAA0', '#172A33'
BY = 252


def string(b, p0, p1):
    dx, dz = p1[0]-p0[0], p1[1]-p0[1]
    length = math.hypot(dx,dz)
    nx, nz = -dz/length*1.2, dx/length*1.2
    b.Y([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),
         (p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],DK,BY-1.5,BY+1.5,L='Sehne')


def model():
    b = B()
    D = b.D
    # Zwei fließende Schaftbögen um einen großen, tatsächlich offenen Durchgriff.
    b.P([(78,263),(117,245),(169,240),(219,248),(262,268),
         (278,287),(258,300),(216,272),(169,263),(124,267),
         (83,285)],ST,-18,18,r=9,L='Schaft')
    b.P([(84,328),(129,338),(174,326),(217,303),(259,279),
         (275,301),(227,329),(180,351),(130,361),(82,349)],ST,-18,18,r=9,L='Schaft')
    b.P([(69,258),(85,263),(93,340),(80,358),(66,347)],DK,-20,20,r=8,L='Schaftkappe')
    b.P([(119,244),(157,234),(194,237),(221,247),(214,261),
         (175,254),(129,261)],RO,-15,15,r=8,L='Wangenauflage')
    b.P([(250,266),(314,261),(378,267),(451,276),(520,272),
         (592,255),(638,263),(645,287),(615,310),(543,328),
         (469,334),(393,323),(318,312),(252,314)],ST,-18,18,r=9,L='Gehäuse',
        dec=[D(roundpoly([(272,296),(328,293),(393,307),(470,318),
                          (539,313),(597,298),(582,310),(540,320),
                          (468,327),(390,316),(325,303),(273,307)],4),RO)])
    # Führungsrinne und Bolzen bleiben gerade, während der tragende Schaft darunter schwingt.
    b.P(rect(402,BY+3,241,6),DK,-5,5,r=6,L='Führungsrinne')
    b.P([(391,242),(412,236),(431,244),(428,262),(395,264)],RO,-16,16,r=7,L='Schloss')
    b.P([(273,273),(279,246),(365,246),(382,274)],ST,-13,13,r=6,L='Schienensockel')
    rail(b,280,371,247,DK,RO,w=11)
    b.C(414,700,BY,3.5,RO,n=10,L='Bolzen')
    b.F(697,731,BY,8,1,RO,n=10)
    b.P([(416,BY),(438,BY-12),(450,BY),(435,BY+2)],PI,-1,1,r=6,L='Bolzenfedern')
    b.P([(601,262),(621,251),(648,259),(659,280),(649,308),
         (622,320),(600,306)],RO,-31,31,r=9,L='Bogenblock')
    # Je ein zusammenhängender Recurve-Flügel links und rechts: breite Wurzeln, stark zurücklaufende Spitzen.
    for s in (-1,1):
        b.Y([(616,24*s),(648,25*s),(654,64*s),(640,106*s),
             (609,151*s),(576,184*s),(559,200*s),(563,221*s),
             (542,218*s),(534,196*s),(553,168*s),(581,132*s),
             (604,93*s),(613,58*s)],ST,BY-3,BY+13,r=9,L='Wurfarm',
            dec=[D(roundpoly([(624,41*s),(637,45*s),(637,77*s),
                              (621,112*s),(593,153*s),(561,187*s),
                              (552,201*s),(550,192*s),(584,147*s),
                              (611,105*s),(623,72*s)],4),PI,True)])
        b.Y([(538,195*s),(551,190*s),(566,206*s),(563,223*s),
             (544,219*s)],RO,BY-6,BY+16,r=6,L='Wurfarmkappe')
        string(b,(554,211*s),(416,2*s))
    b.P([(383,287),(431,289),(497,296),(557,285),(608,273),
         (611,286),(560,301),(500,311),(431,302),(384,299)],RO,19,28,r=7,L='Spannhebel')
    b.P(circ(607,282,9,14),DK,18,31,r=6,L='Spannhebelgelenk')
    b.P([(281,310),(326,315),(326,348),(300,406),(273,420),
         (256,410),(279,350)],ST,-19,19,r=9,L='Griff',
        dec=[D(roundpoly([(290,335),(311,339),(304,365),(281,405),(268,407)],5),DK)])
    trigger_group(b,345,316,RO,ST,grip_x0=316,depth=35)
    b.P([(491,329),(530,325),(540,352),(531,383),(505,390),
         (507,357)],ST,-15,15,r=8,L='Vordergriff')
    return b.m


META = dict(
    num='19', name='Schwere Armbrust', nick='FLÜGELRAD', col=PI,
    pill='STAHLBLAU · ROSENHOLZ · PISTAZIE', palette=[ST,RO,PI,DK], center=(397,316,0),
    desc='Weit zurückgebogene stahlblaue Wurfarme öffnen sich wie zwei Flügel quer zur Bolzenbahn. Der offene Bogenschaft führt '
         'die Kurve unter dem geraden Bolzen fort; rosenholzfarbene Mechanikteile markieren Schloss, Bogenblock und Spannhebel.',
    form='Offener Bogenschaft mit Wangenauflage · geschwungenes Gehäuse · gerade Führungsrinne · Visierschiene · Schloss · Bolzen · '
         'Bogenblock mit zwei breiten Recurve-Wurfarmen · zwei Sehnenhälften · Spannhebel links · Griff mit Abzug · Vordergriff',
    op=dict(
        reload_de='Spannhebel links nach vorn-unten schwenken, bis die Sehne im Schloss sitzt; einen Bolzen in die Führungsrinne legen',
        action_de='Ein Bolzen je Spannung; der Bolzen bleibt am Trefferpunkt und kann zum Auffüllen des Vorrats wieder aufgenommen werden',
        fire_de='Einzelschuss mit hoher Durchschlagskraft; je Ausführung Explosiv- oder Widerhaken-Bolzen',
        reload_en='swing the left cocking lever forward and down until the string latches; place one bolt in the flight groove',
        action_en='one bolt per draw; recover the bolt at the impact point to refill the reserve',
        fire_en='single high-impact shot; explosive or serrated bolts depending on the build'))
