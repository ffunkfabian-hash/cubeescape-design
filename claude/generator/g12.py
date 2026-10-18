"""KG12 Handfeuerwaffe „Schwerlast“ (claude-0.10): großkalibriger Revolver (Destiny: Hand Cannon).
Unterschied zur Pistole/Sidearm (KX01): Trommel mit sechs Kammern statt Magazin im Griff, Hahn statt Schlitten, schwerer Rahmen
mit Oberbrücke und langem Laufmantel."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
import math
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    # Griff mit Griffschalen, Rahmen mit Trommelfenster
    grip(b,232,300,AN,DK,h=118,w=54,lean=22)
    b.P([(218,262),(256,240),(300,240),(300,306),(250,312),(222,300)],CR,-17,17,r=5,L='Rahmen')
    b.P(rect(372,250,24,56),CR,-17,17,r=4)                      # vorderer Rahmenpfosten
    b.P(rect(292,236,112,16),CR,-15,15,r=5,dec=[D(rect(312+16*i,240,8,8),AN) for i in range(5)])   # Oberbrücke
    b.P(rect(296,301,80,14),CR,-14,14,r=4)                      # Unterbrücke unter der Trommel
    # Trommel: sechs Kammern, an der Vorderseite sichtbar; Kammerrillen seitlich
    b.C(301,368,276,25,AN,n=12,L='Trommel',
        cap=[(276+14*math.sin(k*math.pi/3),14*math.cos(k*math.pi/3),5.5,'#050506',False) for k in range(6)])
    b.P(rect(304,268,60,6),DK,-26.5,26.5)
    b.P(rect(262,288,14,8),OR,16,21,r=2,L='Trommelriegel')
    # Hahn hinten oben
    b.P([(240,238),(250,224),(268,240),(262,250)],OR,-5,5,r=2,L='Hahn')
    rail(b,302,402,236,AN,DK,w=9)
    # Laufmantel mit Lüftung, Lauf, Ausstoßerstange
    b.P([(394,246),(528,250),(538,260),(538,288),(394,294)],CR,-14,14,r=6,L='Laufmantel',
        dec=[D(roundpoly(rect(410+22*i,256,12,8),2),AN) for i in range(5)]+[D(roundpoly(rect(410,276,110,5),2),CY,True)])
    b.C(538,556,262,11,DK,n=8,L='Lauf',cap=[(262,0,6,'#050506',False)])   # Laufachse = obere Kammer der Trommel (276 − 14)
    b.C(368,470,300,4,DK,n=8,L='Ausstoßerstange')
    b.P(rect(466,292,14,14),AN,-6,6,r=2)
    trigger_group(b,302,312,OR,AN,grip_x0=276,depth=40)
    return b.m
META=dict(num='12',name='Handfeuerwaffe',nick='SCHWERLAST',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(387,320,0),
 desc='Großkalibriger Revolver als Handfeuerwaffe: Ein schwerer cremefarbener Rahmen hält die Trommel mit sechs Kammern zwischen zwei Pfosten und einer Oberbrücke. Hinten sitzt der orange Hahn, vorne ein langer belüfteter Laufmantel mit Ausstoßerstange darunter.',
 form='Schwerer Rahmen mit Oberbrücke · Trommel mit sechs Kammern · Trommelriegel links · Hahn · belüfteter Laufmantel · Ausstoßerstange · Griff mit Griffschalen',
 op=dict(reload_de='Trommelriegel drücken, Trommel nach links ausschwenken, sechs Patronen einzeln oder mit Schnelllader, Trommel einschwenken',
         action_de='Hahn spannt sich mit jedem Abzug (Double Action) und dreht die Trommel um eine Kammer weiter',
         fire_de='Einzelschuss mit hohem Kaliber und starkem Rückstoß nach oben',
         reload_en='press the cylinder latch, swing the cylinder out to the left, load six rounds (speed loader), swing back in',
         action_en='double action: each trigger pull cocks the hammer and indexes the cylinder by one chamber',
         fire_en='heavy single shots with strong upward recoil'))
