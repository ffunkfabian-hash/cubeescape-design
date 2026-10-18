"""KG11 Scout-Gewehr „Fernlicht“ (claude-0.10): halbautomatisches Präzisionsgewehr mit langem, schlankem Lauf.
Unterschied zum Spurgewehr (KX08): Patronen aus dem Kastenmagazin, gezogener Lauf mit Mündungsbremse, Ladehebel – kein Strahl-Emitter.
Unterschied zum Sturmgewehr (KX02): halbautomatisch, langer freiliegender Lauf, Lochschaft mit Wangenauflage, kurzes Magazin."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    # Lochschaft mit Wangenauflage und Schaftkappe
    b.P([(84,258),(212,262),(212,300),(176,306),(162,342),(88,350)],AN,-14,14,r=6,L='Schaft',
        dec=[D(roundpoly([(118,316),(150,312),(146,334),(116,338)],4),DK)])
    b.P(rect(74,252,14,104),DK,-16,16,r=4,L='Schaftkappe')
    b.P(rect(122,246,82,16),CR,-11,11,r=5,L='Wangenauflage')
    # Gehäuse, schlank, mit Auswurffenster und Ladeanzeige
    b.P([(208,256),(440,252),(462,262),(462,316),(440,326),(208,326)],CR,-19,19,r=7,L='Gehäuse',
        dec=[D(roundpoly(rect(300,270,62,16),4),DK),D(roundpoly(rect(392,272,40,6),2),CY,True),
             D(roundpoly([(212,306),(458,306),(458,314),(440,324),(212,324)],3),AN)])
    rail(b,236,430,252,AN,DK)
    b.P(rect(336,274,26,10),OR,18,30,r=2,L='Ladehebel')
    # Griff, Abzug im Bügel, kurzes Kastenmagazin davor
    grip(b,256,326,AN,DK,h=92,w=48,lean=16)
    trigger_group(b,318,326,OR,AN,grip_x0=296)
    b.P(rect(396,320,48,10),AN,-14,14,r=3)                       # Magazinschacht
    b.P([(402,328),(438,328),(446,388),(410,390)],CR,-12,12,r=4,L='Magazin',
        dec=[D(roundpoly(rect(412,340,22,32),3),DK)]+[D(roundpoly(rect(416,344+9*i,14,5),1.5),OR) for i in range(3)])
    b.P([(408,386),(448,384),(450,396),(408,398)],OR,-13,13,r=3)  # Bodenplatte
    # Handschutz mit Lüftungsschlitzen, langer gezogener Lauf, Mündungsbremse
    b.P([(462,268),(606,272),(614,284),(614,306),(606,314),(462,318)],AN,-13,13,r=5,L='Handschutz',
        dec=[D(roundpoly(rect(482+24*i,282,14,20),3),DK) for i in range(5)])
    b.C(614,720,290,7,DK,n=12,L='Lauf')
    b.C(720,752,290,10,AN,n=8,L='Mündungsbremse',cap=[(290,0,5,'#050506',False)])
    b.P(rect(728,282,16,4),DK,-10.5,10.5)
    return b.m
META=dict(num='11',name='Scout-Gewehr',nick='FERNLICHT',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(413,300,0),
 desc='Halbautomatisches Präzisionsgewehr für mittlere bis weite Distanz: ein schlankes cremefarbenes Gehäuse, ein langer, frei liegender gezogener Lauf mit Mündungsbremse und ein kurzes Kastenmagazin mit Patronenfenster. Hinten ein Lochschaft mit Wangenauflage, vorne ein belüfteter Handschutz.',
 form='Lochschaft mit Wangenauflage · schlankes Gehäuse mit Auswurffenster · Ladehebel links · kurzes Kastenmagazin vor dem Abzug · belüfteter Handschutz · langer gezogener Lauf · Mündungsbremse',
 op=dict(reload_de='Kastenmagazin (8 Patronen) vor dem Abzug wechseln, Ladehebel links zurückziehen',
         action_de='Halbautomatik: Ladehebel spannt den Verschluss einmal nach dem Magazinwechsel',
         fire_de='Einzelfeuer, präzise auf Distanz; ruhig über die Wangenauflage zielen',
         reload_en='swap the 8-round box magazine ahead of the trigger, pull the left charging handle',
         action_en='semi-automatic, charging handle cocks the bolt once after a reload',
         fire_en='single precise shots at range, cheek weld on the cheek rest'))
