"""KG16 Maschinengewehr „Dauerläufer“ (claude-0.10): gurtgespeistes Maschinengewehr mit Munitionskasten (Destiny: Machine Gun).
Unterschied zum Sturmgewehr (KX02): Patronengurt aus dem Munitionskasten links in den Zuführdeckel, schwerer Laufmantel, Tragegriff,
eingeklapptes Zweibein, Schaft für Dauerfeuer."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK,BR='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D','#C9A25A'
def model():
    b=B();D=b.D
    b.P([(66,256),(104,250),(232,262),(232,318),(184,332),(76,356)],AN,-16,16,r=6,L='Schaft',
        dec=[D(roundpoly(rect(110,272,90,12),4),DK)])
    b.P(rect(56,246,14,114),DK,-18,18,r=4,L='Schaftkappe')
    b.P([(228,246),(524,242),(546,256),(546,334),(524,344),(228,344)],CR,-26,26,r=8,L='Gehäuse',
        dec=[D(roundpoly([(232,322),(542,322),(542,332),(524,342),(232,342)],3),AN),D(roundpoly(rect(456,262,60,8),3),CY,True)])
    # Zuführdeckel mit Scharnier hinten, Visierschiene darauf
    b.P([(300,230),(470,228),(482,244),(300,246)],AN,-22,22,r=4,L='Zuführdeckel')
    b.C(292,304,240,6,DK,n=8)
    rail(b,318,462,228,AN,DK,w=10)
    b.P(rect(470,282,26,10),OR,26,38,r=2,L='Ladehebel')
    # Munitionskasten links unten am Gehäuse, Patronengurt hinauf in die Zuführung
    b.P(rect(334,300,116,86),AN,26,74,r=6,L='Munitionskasten',
        dec=[D(roundpoly(rect(346,316,92,14),3),OR),D(roundpoly(rect(346,340,92,30),4),DK)])
    b.P([(354,262),(420,262),(424,302),(350,302)],BR,26,40,r=2,L='Patronengurt',
        dec=[D(rect(358+9*i,266,4,32),'#8E6F38') for i in range(7)])
    # Laufmantel mit Lüftung, Tragegriff, Lauf, Feuerdämpfer
    b.P([(546,258),(766,262),(776,276),(776,318),(766,330),(546,334)],AN,-18,18,r=6,L='Laufmantel',
        dec=[D(roundpoly(rect(566+26*i,276,14,30),3),DK) for i in range(8)])
    b.P(rect(586,224,10,36),DK,-6,6,r=2)
    b.P(rect(654,226,10,36),DK,-6,6,r=2)
    b.P(rect(578,214,96,14),CR,-8,8,r=5,L='Tragegriff')
    b.C(776,868,296,9,DK,n=12,L='Lauf')
    b.C(868,904,296,14,AN,n=8,L='Feuerdämpfer',cap=[(296,0,7,'#050506',False)])
    # eingeklapptes Zweibein unter dem Laufmantel
    b.C(690,770,340,4,DK,n=8,cz=10,L='Zweibein')
    b.C(690,770,340,4,DK,n=8,cz=-10)
    b.P(rect(680,330,16,16),AN,-14,14,r=3)
    # Griff, Abzug, Vordergriff
    grip(b,274,344,AN,DK,h=92,w=50,lean=16)
    trigger_group(b,334,344,OR,AN,grip_x0=316,depth=36)
    b.P([(586,330),(622,330),(616,396),(592,396)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='16',name='Maschinengewehr',nick='DAUERLÄUFER',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,BR],center=(480,300,0),
 desc='Gurtgespeistes Maschinengewehr für Dauerfeuer: Links hängt der anthrazitfarbene Munitionskasten, aus dem der messingfarbene Patronengurt in die Zuführung unter dem Deckel läuft. Vorne ein langer belüfteter Laufmantel mit Tragegriff und eingeklapptem Zweibein.',
 form='Schwerer Schaft · Gehäuse mit Zuführdeckel und Visierschiene · Munitionskasten links mit Patronengurt · belüfteter Laufmantel · Tragegriff · Feuerdämpfer · eingeklapptes Zweibein · Vordergriff',
 op=dict(reload_de='Zuführdeckel hinten am Scharnier aufklappen, neuen Munitionskasten links einhängen, Gurt einlegen, Deckel schließen, Ladehebel ziehen',
         action_de='Gurtzuführung: der Verschluss zieht den Gurt bei jedem Schuss um eine Patrone weiter',
         fire_de='Dauerfeuer, Feuerrate steigt beim Halten; Tragegriff zum Laufwechsel',
         reload_en='flip the feed cover open on its rear hinge, hang a new ammo box on the left, lay in the belt, close the cover, pull the charging handle',
         action_en='belt feed: the bolt pulls the belt one round further with every shot',
         fire_en='sustained full-auto fire, rate climbs while held; carry handle for barrel swaps'))
