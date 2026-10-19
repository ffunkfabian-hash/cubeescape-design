"""KG22 Slug-Schrotflinte „Treffpunkt“ (claude-0.10): halbautomatische Flinte für Einzelgeschosse (Destiny: Slug-Shotgun-Rahmen).
Unterschied zur Schrotflinte (KX04, Streuschrot): ein einzelner gezogener Lauf mit runder Bohrung und Mündungsbremse, Kastenmagazin
mit Slug-Patronen, Ladehebel statt Pumpgriff, Präzisionsvisier – auf Treffer auf mittlere Distanz ausgelegt statt Streuung."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
import math
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.P([(84,258),(118,252),(226,264),(226,312),(182,326),(92,352)],AN,-16,16,r=6,L='Schaft',
        dec=[D(roundpoly(rect(124,276,70,12),4),DK)])
    b.P(rect(74,248,14,110),DK,-18,18,r=4,L='Schaftkappe')
    b.P([(222,252),(460,248),(484,262),(484,330),(460,340),(222,340)],CR,-24,24,r=8,L='Gehäuse',
        dec=[D(roundpoly([(226,318),(480,318),(480,328),(460,338),(226,338)],3),AN),D(roundpoly(rect(300,268,70,18),4),DK),
             D(roundpoly(rect(392,270,60,6),2),OR,True)])
    rail(b,242,452,248,AN,DK,w=10)
    b.P(rect(336,276,26,10),OR,22,34,r=2,L='Ladehebel')
    # Kastenmagazin mit Patronenfenster: Slug-Köpfe statt Schrot
    b.P(rect(396,336,62,10),AN,-16,16,r=3)
    b.P([(402,344),(454,344),(460,404),(408,406)],CR,-14,14,r=4,L='Magazin',
        dec=[D(roundpoly(rect(412,354,40,40),4),DK)]+[D(roundpoly(rect(416,358+12*i,32,8),3),OR) for i in range(3)])
    b.P([(406,402),(462,400),(464,412),(406,414)],OR,-15,15,r=3)
    # Laufmantel, schwerer gezogener Lauf, Mündungsbremse mit runder Bohrung und Zügen
    b.P([(484,264),(620,268),(630,280),(630,310),(620,320),(484,324)],AN,-16,16,r=6,L='Laufmantel',
        dec=[D(roundpoly(rect(500+26*i,280,16,26),3),DK) for i in range(4)])
    b.C(630,738,294,12,DK,n=12,L='Lauf')
    b.C(738,774,294,17,AN,n=8,L='Mündungsbremse',
        cap=[(294,0,9,'#050506',False)]+[(294+9.5*math.sin(k*math.pi/3),9.5*math.cos(k*math.pi/3),1.6,OR,False) for k in range(6)])
    b.P(rect(746,284,20,5),DK,-12.5,12.5)
    grip(b,266,340,AN,DK,h=90,w=50,lean=16)
    trigger_group(b,326,340,OR,AN,grip_x0=306,depth=34)
    b.P([(540,320),(574,320),(568,384),(546,384)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='22',name='Slug-Schrotflinte',nick='TREFFPUNKT',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(424,300,0),
 desc='Halbautomatische Flinte für Einzelgeschosse: Statt Streuschrot verschießt sie schwere Slugs aus einem einzelnen gezogenen Lauf. Das Kastenmagazin zeigt im Fenster die orangen Slug-Köpfe, vorne sitzt eine Mündungsbremse mit runder Bohrung und sechs Zügen.',
 form='Schaft · breites Gehäuse mit Ladehebel links und Visierschiene · Kastenmagazin mit Slug-Fenster · belüfteter Laufmantel · schwerer gezogener Lauf · Mündungsbremse mit sechs Zügen · Vordergriff',
 op=dict(reload_de='Kastenmagazin (5 Slug-Patronen) vor dem Abzug wechseln, Ladehebel links zurückziehen',
         action_de='Halbautomatik, ein Geschoss je Abzug; der Ladehebel spannt nur nach dem Magazinwechsel',
         fire_de='Einzelgeschoss mit hoher Wucht und Präzision auf mittlere Distanz, kein Streukegel',
         reload_en='swap the 5-round slug box magazine ahead of the trigger, pull the left charging handle',
         action_en='semi-automatic, one projectile per trigger pull; charging handle only after a magazine change',
         fire_en='single heavy slug with precision at medium range, no spread cone'))
