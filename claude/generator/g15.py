"""KG15 Schwerer Granatwerfer „Trommelfeuer“ (claude-0.10): Granatwerfer mit sechsschüssiger Drehtrommel (Destiny: Grenade Launcher,
Heavy, drum-loaded). Unterschied zum Spezial-Granatwerfer (KG14): Trommel mit sechs Kammern zwischen Heckrahmen und Laufträger,
Laden über die Ladeklappe, Lauf auf Höhe der oberen Kammer."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
import math
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
AX=300   # Trommelachse (y); Lauf auf Höhe der oberen Kammer
def model():
    b=B();D=b.D
    b.P([(34,262),(68,254),(176,266),(176,318),(138,330),(44,356)],AN,-16,16,r=6,L='Schaft',
        dec=[D(roundpoly(rect(78,280,70,10),3),DK)])
    b.P(rect(24,250,14,110),DK,-18,18,r=4,L='Schaftkappe')
    # Heckrahmen mit Ladeklappe links; Griff und Abzug sitzen unter dem Heckrahmen hinter der Trommel
    b.P([(172,246),(306,242),(306,350),(172,350)],AN,-26,26,r=6,L='Gehäuse',dec=[D(roundpoly(rect(190,262,100,10),3),DK)])
    b.P(rect(240,300,56,34),OR,26,31,r=3,L='Ladeklappe')
    # Trommel mit sechs Kammern, Achse, Laufträger nur um Achse und Lauf (Kammern vorne sichtbar)
    b.C(306,428,AX,58,CR,n=12,L='Granattrommel',
        cap=[(AX-36*math.cos(k*math.pi/3),36*math.sin(k*math.pi/3),13,'#050506',False) for k in range(6)])
    for x in (330,396):b.C(x,x+8,AX,59,DK,n=12)          # Laufringe der Trommel
    b.C(286,450,AX,9,DK,n=8,L='Trommelachse')
    b.P(rect(296,226,152,18),AN,-18,18,r=5)                          # Oberbrücke über der Trommel
    rail(b,312,440,226,AN,DK,w=9)
    b.P([(428,226),(452,226),(452,316),(428,316)],AN,-24,24,r=5,L='Laufträger')
    # Lauf auf Höhe der oberen Kammer, Mündung
    b.C(452,612,AX-36,22,AN,n=12,L='Lauf')
    b.P(rect(470,AX-62,120,6),DK,-8,8)
    b.C(612,632,AX-36,27,DK,n=12,L='Mündung',cap=[(AX-36,0,18,'#050506',False)])
    # Griff, Abzug, Vordergriff unter dem Laufträger
    grip(b,186,350,AN,DK,h=88,w=48,lean=16)
    trigger_group(b,238,350,OR,AN,grip_x0=226,depth=36)
    b.P([(470,286),(506,286),(500,360),(476,360)],AN,-14,14,r=6,L='Vordergriff')
    b.P(rect(452,280,70,10),AN,-10,10,r=3)
    return b.m
META=dict(num='15',name='Schwerer Granatwerfer',nick='TROMMELFEUER',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(354,300,0),
 desc='Schwerer Granatwerfer mit Drehtrommel: Zwischen Heckrahmen und Laufträger dreht sich eine große cremefarbene Trommel mit sechs Kammern auf einer Achse. Der Lauf sitzt auf Höhe der oberen Kammer, links am Heckrahmen öffnet die orange Ladeklappe.',
 form='Heckrahmen mit Ladeklappe links · Drehtrommel mit sechs Kammern · Trommelachse · Oberbrücke mit Visierschiene · Laufträger · kurzer dicker Lauf · Vordergriff · Schaft',
 op=dict(reload_de='Ladeklappe links öffnen, Trommel Kammer für Kammer weiterdrehen und sechs Granaten einschieben, Klappe schließen',
         action_de='Trommel dreht nach jedem Schuss um eine Kammer (Federwerk in der Achse)',
         fire_de='sechs Granaten nacheinander, Aufprallzünder; schwere Munition',
         reload_en='open the left loading gate, index the drum chamber by chamber and insert six grenades, close the gate',
         action_en='the drum indexes one chamber after each shot (spring in the axle)',
         fire_en='six grenades in succession, impact fuse; heavy ammo'))
