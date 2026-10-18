"""KG21 Raketen-Impulsgewehr „Salvenwerk“ (claude-0.10): Impulsgewehr mit Raketenmunition (Destiny: Rocket-Assisted Pulse Rifle,
seit „The Edge of Fate“ 2025, Spezialmunition). Unterschied zum Impulsgewehr (KX03): Salven aus kleinen Raketen statt Energieimpulsen,
Rohrlauf mit Abgasring, querliegendes Raketenmagazin mit Sichtfenster (fünf Raketen) statt Energiezelle."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.P([(92,262),(124,256),(222,266),(222,306),(180,318),(100,346)],AN,-14,14,r=6,L='Schaft',
        dec=[D(roundpoly(rect(130,280,62,10),3),DK)])
    b.P(rect(82,252,14,100),DK,-16,16,r=4,L='Schaftkappe')
    b.P([(218,254),(444,250),(470,262),(470,326),(444,336),(218,336)],CR,-22,22,r=8,L='Gehäuse',
        dec=[D(roundpoly([(222,314),(466,314),(466,324),(444,334),(222,334)],3),AN),D(roundpoly(rect(240,270,70,12),4),DK),
             D([(330,266),(390,266),(390,272),(330,272)],OR,True)])
    rail(b,238,436,250,AN,DK,w=10)
    b.P(rect(318,278,24,10),OR,20,32,r=2,L='Ladehebel')
    # Raketenmagazin quer unter dem Gehäuse, Sichtfenster mit fünf Raketen
    b.P([(388,334),(468,334),(468,372),(394,372)],AN,-24,24,r=5,L='Raketenmagazin',
        dec=[D(roundpoly(rect(398,342,62,22),4),DK)]+[D([(402+12*i,360),(407+12*i,346),(412+12*i,360)],OR) for i in range(5)])
    # Handschutz mit Abgasschlitzen, Rohrlauf mit Abgasring, Mündung
    b.P([(470,266),(588,270),(598,282),(598,310),(588,318),(470,322)],AN,-16,16,r=6,L='Handschutz',
        dec=[D([(486+22*i,282),(498+22*i,282),(492+22*i,306),(480+22*i,306)],OR) for i in range(4)])
    b.C(598,690,292,13,AN,n=8,L='Lauf')
    b.F(626,646,292,18,14,DK,n=8,L='Abgasring')
    b.C(690,708,292,17,DK,n=8,L='Mündung',cap=[(292,0,10,'#050506',False),(292,0,4,OR,True)])
    grip(b,262,336,AN,DK,h=90,w=48,lean=16)
    trigger_group(b,322,336,OR,AN,grip_x0=302,depth=34)
    b.P([(516,318),(550,318),(544,380),(522,380)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='21',name='Raketen-Impulsgewehr',nick='SALVENWERK',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(395,300,0),
 desc='Impulsgewehr für Raketensalven: Ein querliegendes Raketenmagazin unter dem cremefarbenen Gehäuse zeigt durch das Sichtfenster fünf orange Raketenspitzen. Vorne leitet ein Handschutz mit schrägen Abgasschlitzen in einen weiten Rohrlauf mit Abgasring.',
 form='Schaft · Gehäuse mit Ladehebel links · querliegendes Raketenmagazin mit Sichtfenster · Handschutz mit Abgasschlitzen · Rohrlauf mit Abgasring · weite Mündung · Griff · Vordergriff',
 op=dict(reload_de='Raketenmagazin quer nach unten ziehen, neues einsetzen (5 Raketen), Ladehebel links zurückziehen',
         action_de='Impulsabzug: jede Abzugbetätigung feuert eine Salve aus zwei Raketen; Abgas entweicht nach vorn über die Schlitze',
         fire_de='Salvenfeuer, Raketen explodieren beim Aufprall; Spezialmunition, kleiner Vorrat',
         reload_en='pull the transverse rocket magazine down, insert a new one (5 rockets), pull the left charging handle',
         action_en='pulse trigger: each pull fires a two-rocket burst; exhaust vents forward through the slots',
         fire_en='burst fire, rockets explode on impact; special ammo, small reserve'))
