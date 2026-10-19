"""KG20 Raketenpistole „Funkenflug“ (claude-0.10): Pistole mit Raketenmunition (Destiny: Rocket-Assisted Sidearm, Spezialmunition).
Unterschied zur Pistole (KX01): weite Rohrbohrung mit sichtbarer Mini-Rakete, Raketenmagazin mit Fenster unter dem Griff,
Abgasschlitze im Schlitten; die Geschosse treiben sich selbst an und explodieren beim Aufprall."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    grip(b,246,300,AN,DK,h=104,w=52,lean=18)
    b.P([(224,402),(296,402),(294,446),(220,446)],CR,-19,19,r=5,L='Raketenmagazin',
        dec=[D(roundpoly(rect(232,412,56,26),4),DK)]+[D([(238+13*i,434),(244+13*i,416),(250+13*i,434)],OR) for i in range(4)])
    b.P([(226,282),(476,282),(476,304),(240,310)],AN,-16,16,r=4,L='Rahmen')
    b.P([(214,236),(470,236),(490,248),(490,282.5),(214,282.5),(204,270),(204,248)],CR,-19,19,r=4,L='Schlitten',
        dec=[D([(382+16*i,252),(392+16*i,252),(386+16*i,272),(376+16*i,272)],DK) for i in range(5)]+
            [D(roundpoly(rect(222,246,40,8),3),OR),D(roundpoly(rect(300,256,60,6),2),CY,True)])
    rail(b,236,440,236,AN,DK,w=8)
    b.C(490,566,262,18,AN,n=8,L='Lauf',cap=[(262,0,12,'#050506',False),(262,0,5,OR,True)])
    b.P(rect(504,242,48,6),DK,-8,8)
    trigger_group(b,308,310,OR,AN,grip_x0=286,depth=38)
    return b.m
META=dict(num='20',name='Raketenpistole',nick='FUNKENFLUG',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(390,340,0),
 desc='Pistole mit Raketenmunition: Der cremefarbene Schlitten trägt schräge Abgasschlitze, vorne öffnet sich eine weite Rohrbohrung, in der die Spitze der nächsten Mini-Rakete orange leuchtet. Unter dem Griff steckt das Raketenmagazin mit Sichtfenster.',
 form='Schlitten mit schrägen Abgasschlitzen · weites Raketenrohr mit sichtbarer Raketenspitze · Rahmen mit Visierschiene · Griff · Raketenmagazin mit Sichtfenster unter dem Griff · Abzug im Bügel',
 op=dict(reload_de='Raketenmagazin unten aus dem Griff ziehen, volles Magazin (6 Mini-Raketen) einsetzen, Schlitten zurückziehen',
         action_de='Halbautomatik: der Schlitten läuft nach jedem Schuss zurück und lädt die nächste Rakete; Abgas entweicht über die Schlitze',
         fire_de='langsame Einzelschüsse, die Rakete zündet nach der Mündung und explodiert beim Aufprall (Flächenschaden)',
         reload_en='pull the rocket magazine out of the grip bottom, insert a full one (6 mini rockets), rack the slide',
         action_en='semi-automatic: the slide cycles after each shot and chambers the next rocket; exhaust vents through the slots',
         fire_en='slow single shots, the rocket ignites past the muzzle and explodes on impact (area damage)'))
