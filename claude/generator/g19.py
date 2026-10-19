"""KG19 Schwere Armbrust „Bolzenwerk“ (claude-0.10): schwere Armbrust mit wiederaufnehmbarem Bolzen (Destiny: Crossbow, schwerer
Typ seit „The Edge of Fate“, 2025). Unterschied zum Bogen (KX10): Schaft mit Abzug und Schloss, quer liegende Wurfarme am Bogenblock,
Spannhebel links, Bolzen in der Führungsrinne, Zielfernrohr auf der Schiene. KC10 bleibt Bogen (ID nicht umgedeutet)."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly,circ
import math
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
BY=252     # Höhe von Bolzen und Sehne
def strip(b,p0,p1,w,col,y0,y1,L=None):
    """Sehne als schmales Band in der Ebene x-z"""
    dx,dz=p1[0]-p0[0],p1[1]-p0[1];l=math.hypot(dx,dz);nx,nz=-dz/l*w/2,dx/l*w/2
    b.Y([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),(p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],col,y0,y1,L=L)
def model():
    b=B();D=b.D
    b.P([(84,262),(116,256),(244,268),(244,312),(200,326),(92,350)],AN,-14,14,r=6,L='Schaft',
        dec=[D(roundpoly(rect(120,282,80,10),3),DK)])
    b.P(rect(74,252,14,104),DK,-16,16,r=4,L='Schaftkappe')
    b.P(rect(126,246,84,16),CR,-11,11,r=5,L='Wangenauflage')
    # Gehäuse mit Führungsrinne, Schloss, Visierschiene hinten
    b.P([(240,258),(618,256),(632,266),(632,304),(240,308)],CR,-16,16,r=6,L='Gehäuse',
        dec=[D(roundpoly(rect(270,276,120,12),4),AN),D(roundpoly(rect(470,274,120,6),2),CY,True)])
    b.P(rect(398,BY+2,236,4),AN,-4,4)             # Führungsrinne
    b.P(rect(392,240,34,18),AN,-14,14,r=4,L='Schloss')
    rail(b,262,384,258,AN,DK,w=9)
    # Bolzen mit Spitze und Federn
    b.C(410,694,BY,3.5,OR,n=8,L='Bolzen')
    b.F(694,722,BY,7,1,OR,n=8)
    b.P([(414,BY),(440,BY-10),(446,BY)],CY,-0.8,0.8)
    # Bogenblock und quer liegende Wurfarme (Recurve), Sehne zum Schloss
    b.P(rect(604,257,42,53),AN,-26,26,r=6,L='Bogenblock',dec=[D(roundpoly(rect(612,282,26,16),3),DK)])   # unter der Bolzenbahn
    for s in (1,-1):
        b.Y([(612,24*s),(642,24*s),(632,96*s),(608,96*s)],CR,BY-3,BY+11,r=2,L='Wurfarm')
        b.Y([(608,96*s),(632,96*s),(604,158*s),(588,154*s)],CR,BY-2,BY+10,r=2,L='Wurfarm')
        b.Y([(584,150*s),(600,148*s),(602,166*s),(586,168*s)],OR,BY-6,BY+10,r=2)
        strip(b,(594,158*s),(412,2*s),2.4,DK,BY-1.5,BY+1.5,L='Sehne')
    # Spannhebel links mit Drehpunkt vorne, Griff, Abzug, Vordergriff
    b.P(rect(380,280,224,10),OR,16,22,r=3,L='Spannhebel')
    b.P(circ(598,285,8,10),AN,15,24)
    grip(b,282,308,AN,DK,h=90,w=48,lean=16)
    trigger_group(b,342,308,OR,AN,grip_x0=322,depth=34)
    b.P([(486,304),(522,304),(516,368),(492,368)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='19',name='Schwere Armbrust',nick='BOLZENWERK',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(398,300,0),
 desc='Schwere Armbrust mit wiederaufnehmbarem Bolzen: Am anthrazitfarbenen Bogenblock sitzen quer zwei cremefarbene Recurve-Wurfarme, die Sehne läuft zum Schloss auf dem Gehäuse zurück. Der orange Bolzen liegt in der Führungsrinne, links am Gehäuse der lange Spannhebel.',
 form='Schaft mit Wangenauflage · Gehäuse mit Führungsrinne und Visierschiene · Schloss · Bolzen · Bogenblock mit quer liegenden Recurve-Wurfarmen · Sehne · Spannhebel links · Griff mit Abzug · Vordergriff',
 op=dict(reload_de='Spannhebel links am vorderen Drehpunkt nach vorn-unten schwenken: der Schlitten zieht die Sehne ins Schloss; Bolzen in die Führungsrinne legen',
         action_de='ein Bolzen je Spannung; der Bolzen bleibt nach dem Treffer liegen und wird wieder aufgenommen (ergänzt den Vorrat)',
         fire_de='Einzelschuss mit hoher Durchschlagskraft, Explosiv- oder Widerhaken-Bolzen je nach Ausführung',
         reload_en='swing the left cocking lever forward and down on its front pivot: the slide draws the string into the latch; lay a bolt in the flight groove',
         action_en='one bolt per draw; the bolt stays at the impact point and can be picked up again (refills the reserve)',
         fire_en='single high-impact shot, explosive or serrated bolts depending on the build'))
