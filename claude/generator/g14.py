"""KG14 Spezial-Granatwerfer „Kipper“ (claude-0.10): einschüssiger Granatwerfer mit Kipplauf (Destiny: Grenade Launcher, Special,
breech-loaded). Unterschied zum schweren Granatwerfer (KG15): eine Granate im Lauf, Laden über das Abkippen des Laufs am Scharnier."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly,circ
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.P([(104,262),(134,256),(244,272),(244,314),(204,324),(112,352)],AN,-14,14,r=6,L='Schaft',
        dec=[D(roundpoly(rect(146,282,64,10),3),DK)])
    b.P(rect(94,252,14,104),DK,-16,16,r=4,L='Schaftkappe')
    # Ersatzgranate im Halter links am Schaft
    b.P(rect(150,280,64,26),AN,13,22,r=4,L='Granathalter')
    b.C(156,198,293,10,OR,n=10,cz=31)
    b.F(198,212,293,10,5,OR,n=10,cz=31,L='Ersatzgranate')
    # Gehäuse mit Verriegelungshebel oben, Scharnier vorne unten
    b.P([(240,266),(384,260),(396,274),(396,326),(240,330)],CR,-20,20,r=6,L='Gehäuse',
        dec=[D(roundpoly(rect(262,290,90,14),4),AN),D(roundpoly(rect(268,294,40,6),2),OR,True)])
    rail(b,262,372,262,AN,DK,w=9)
    b.P([(372,250),(388,244),(398,258),(384,264)],OR,-5,5,r=2,L='Verriegelungshebel')
    b.P(circ(398,318,11,12),AN,-23,23,L='Scharnier')
    # Kipplauf: dicker Lauf, kippt am Scharnier nach unten; Mündungsring
    b.C(396,566,292,26,CR,n=12,L='Kipplauf')
    b.P(rect(410,262,140,5),AN,-6,6)
    b.C(566,582,292,30,AN,n=12,L='Mündung',cap=[(292,0,21,'#050506',False),(292,0,8,DK,False)])
    # Griff, Abzug, Vordergriff unter dem Lauf
    grip(b,272,330,AN,DK,h=88,w=48,lean=16)
    trigger_group(b,330,330,OR,AN,grip_x0=310,depth=36)
    b.P([(452,316),(490,316),(484,380),(458,380)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='14',name='Spezial-Granatwerfer',nick='KIPPER',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(338,300,0),
 desc='Einschüssiger Granatwerfer mit Kipplauf: Der dicke cremefarbene Lauf hängt vorne unten am Scharnier des kurzen Gehäuses und kippt zum Laden nach unten ab. Oben sitzt der orange Verriegelungshebel, links am Schaft steckt eine Ersatzgranate im Halter.',
 form='Kurzes Gehäuse · dicker Kipplauf am Scharnier · Verriegelungshebel oben · großer Mündungsring · Ersatzgranate im Halter links am Schaft · Vordergriff unter dem Lauf',
 op=dict(reload_de='Verriegelungshebel nach rechts drücken, Kipplauf am Scharnier nach unten abkippen, Hülse fällt heraus, Granate einschieben, Lauf zuklappen',
         action_de='einzelner Schuss je Ladung; die Ersatzgranate links am Schaft beschleunigt das Nachladen',
         fire_de='Granate im Bogen, Zünder bei Aufprall oder Fernzündung (Abzug erneut)',
         reload_en='push the locking lever right, tip the break-action barrel down on its hinge, the case drops out, insert a grenade, close',
         action_en='one shot per load; the spare grenade on the left of the stock speeds up the reload',
         fire_en='lobbed grenade, impact fuse or remote detonation with a second trigger pull'))
