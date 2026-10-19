"""KG24 Mikroraketen-Granatwerfer „Zielstrich“ (claude-0.10.1): einschüssiger Werfer für Mikroraketen (Destiny: Grenade Launcher,
Micro-Missile Frame, Spezialmunition; die Rakete fliegt gerade und schnell statt im Bogen). Unterschied zum Spezial-Granatwerfer (KG14,
Kipplauf) und zum Raketenwerfer (KX09): schlankes langes Abschussrohr mit Leitringen, Laden von oben durch die Ladeklappe, schwerer
Raketenvorrat mit vier Ersatz-Mikroraketen links am Gehäuse."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly,circ
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
AX=286   # Rohrachse (y)
def model():
    b=B();D=b.D
    b.P([(96,262),(128,256),(236,268),(236,312),(196,324),(104,352)],AN,-15,15,r=6,L='Schaft',
        dec=[D(roundpoly(rect(136,280,70,12),4),DK)])
    b.P(rect(86,252,14,106),DK,-17,17,r=4,L='Schaftkappe')
    # breites Gehäuse; oben hinten die Visierschiene, davor die Ladeklappe über dem Patronenlager
    b.P([(232,256),(424,250),(444,264),(444,336),(424,344),(232,344)],CR,-24,24,r=8,L='Gehäuse',
        dec=[D(roundpoly([(236,322),(440,322),(440,332),(424,342),(236,342)],3),AN)])
    rail(b,246,330,256,AN,DK,w=10)
    b.P([(340,240),(424,238),(434,252),(340,254)],OR,-16,16,r=3,L='Ladeklappe',dec=[D(rect(352+18*i,244,10,5),AN) for i in range(4)])
    b.P(circ(338,248,6,10),DK,-17,17)                                    # Scharnier der Ladeklappe (hinten, quer)
    # Raketenvorrat links: Kasten mit Sichtfenster und vier Ersatz-Mikroraketen (Spitzen nach vorn)
    b.P(rect(286,272,132,64),AN,24,56,r=6,L='Raketenvorrat',
        dec=[D(roundpoly(rect(296,280,112,48),5),DK)]+
            [D(roundpoly(rect(302,284+11*i,78,6),2),CR) for i in range(4)]+
            [D([(380,284+11*i),(398,287+11*i),(380,290+11*i)],OR) for i in range(4)])
    # Abschussrohr: schlank und lang, Leitringe, Abgasschlitze hinten, Mündung mit sichtbarer Raketenspitze
    b.C(430,676,AX,17,CR,n=12,L='Abschussrohr')
    for x in (470,560,640):b.C(x,x+10,AX,21,AN,n=12,L='Leitring' if x==470 else None)
    b.F(676,700,AX,17,24,AN,n=12,L='Mündung')
    b.C(700,706,AX,24,DK,n=12,cap=[(AX,0,16,'#050506',False),(AX,0,6,OR,False)])
    # Griff, Abzug, Vordergriff direkt am Rohr zwischen den Leitringen
    grip(b,280,344,AN,DK,h=88,w=48,lean=16)
    trigger_group(b,340,344,OR,AN,grip_x0=320,depth=34)
    b.P([(588,AX+14),(624,AX+14),(618,AX+82),(594,AX+82)],AN,-12,12,r=6,L='Vordergriff')
    return b.m
META=dict(num='24',name='Mikroraketen-Granatwerfer',nick='ZIELSTRICH',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(396,300,0),
 desc='Einschüssiger Werfer für Mikroraketen: Ein schlankes, langes cremefarbenes Abschussrohr mit drei Leitringen schickt die Rakete gerade und schnell ins Ziel, in der Mündung blitzt ihre orange Spitze. Geladen wird von oben durch die orange Ladeklappe, links am breiten Gehäuse trägt ein schwerer Raketenvorrat vier Ersatzraketen hinter einem Sichtfenster.',
 form='Schaft · breites Gehäuse mit Ladeklappe oben · Raketenvorrat links mit Sichtfenster und vier Mikroraketen · schlankes Abschussrohr mit drei Leitringen · Mündung mit Raketenspitze · Vordergriff',
 op=dict(reload_de='Ladeklappe oben nach hinten aufklappen, eine Mikrorakete aus dem Raketenvorrat links ins Patronenlager legen, Klappe schließen',
         action_de='einschüssig: eine Rakete im Rohr, nach jedem Schuss neu laden; der Treibsatz zündet erst vor der Mündung',
         fire_de='Mikrorakete fliegt schnell und gerade statt im Bogen, Aufprallzünder, geringer Eigenschaden; Spezialmunition',
         reload_en='flip the top loading gate open to the rear, take one micro-missile from the left reserve box into the chamber, close the gate',
         action_en='single shot: one missile in the tube, reload after every shot; the motor ignites just past the muzzle',
         fire_en='fast micro-missile on a straight line instead of an arc, impact fuse, low self-damage; special ammo'))
