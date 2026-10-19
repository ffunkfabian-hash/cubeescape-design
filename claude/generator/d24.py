"""KD24 „Spaltkeil“: D-Mikroraketenwerfer mit Toplader und linkem Raketenvorrat."""
from tlib import B, rail
from eng import rect, roundpoly, circ
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#BA71B7', '#F8DDF5'
AX = 286


def model():
    b = B(); D = b.D
    b.P([(100,242),(170,242),(226,260),(226,326),(176,326),(118,350),(100,350)],
        DK,-26,26,r=12,L='Schaft',
        dec=[D(roundpoly(rect(116,254,80,24),9),P),D(roundpoly(rect(120,308,46,10),4),K)])
    b.P(rect(86,236,20,124),K,-29,29,r=8,L='Schaftkappe')
    b.P([(214,230),(410,224),(442,244),(442,340),(234,340),(214,320)],
        DK,-36,36,r=12,L='Gehäuse',
        dec=[D(roundpoly([(234,244),(330,240),(350,252),(350,278),(234,284)],10),P),
             D(roundpoly(rect(244,256,82,9),4),A,True)])
    rail(b,244,322,232,K,DK,w=14)
    b.P([(342,224),(412,222),(432,238),(432,248),(342,248)],DK,-24,24,r=8,L='Ladeklappe',
        dec=[D(roundpoly(rect(354,230,56,10),4),P),D(roundpoly(rect(364,233,34,4),2),A,True)])
    b.P(circ(342,239,8,12),K,-28,28,L='Ladeklappe')
    # Ein flacher, breiter Kasten links trägt vier Reservegeschosse, kein Speisemagazin.
    b.P(rect(270,278,160,58),DK,35,65,r=12,L='Raketenvorrat',
        dec=[D(roundpoly(rect(280,286,140,42),9),P),D(roundpoly(rect(286,290,128,34),7),K)]+
            [D(roundpoly(rect(294,294+8*i,86,5),2),AL) for i in range(4)]+
            [D([(380,294+8*i),(402,296.5+8*i),(380,299+8*i)],A) for i in range(4)])
    # Das lange Rohr beginnt tief im Gehäuse; drei breite Leitringe gliedern die freie Strecke.
    b.C(430,650,AX,21,DK,n=12,L='Abschussrohr')
    for x in (460,534,612):
        b.C(x,x+16,AX,29,K,n=12,L='Leitring')
        b.m.decal('x+',x+16,roundpoly(rect(AX-23,-12,6,24),3),P,both=False)
    b.F(648,676,AX,21,31,DK,n=12,L='Mündung')
    b.C(674,686,AX,31,K,n=12,L='Mündung',
        cap=[(AX,0,21,K,False),(AX,0,8,A,False),(AX,0,3,AL,True)])
    b.P([(264,338),(314,338),(334,436),(278,442)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(284,358),(300,358),(315,416),(300,418)],6),DK)])
    b.P(arcband(314,404,338,70,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(338,339),(351,339),(364,380),(350,386)],A,-6,6,r=4,L='Abzug')
    b.P([(556,300),(590,300),(588,386),(562,392)],DK,-18,18,r=10,L='Vordergriff',
        dec=[D(roundpoly(rect(570,326,10,42),4),A,True)])
    return b.m


META=dict(num='24',name='Mikroraketen-Granatwerfer',nick='SPALTKEIL',col=A,
 pill='PHASE-SKIN',palette=[P,DK,A,AL],center=(386,332,0),
 desc='Ein kompakter, schwerer Toplader trägt einen langen dunklen Rohrfortsatz mit drei kräftigen Leitringen. Die helle Deckplatte und violette Lichtstreifen fassen den Ladeblock ein; links liegen vier Mikroraketen im breiten Sichtkasten, eine weitere sitzt im Abschussrohr.',
 form='Tiefer Schulterblock · gerundetes Gehäuse · Ladeklappe oben · linker Raketenvorrat mit vier Spitzen · langes Abschussrohr · drei breite Leitringe · aufgeweitete Mündung · gebogener Bügel · Vordergriff',
 op=dict(reload_de='Obere Ladeklappe nach hinten öffnen, eine Mikrorakete aus dem linken Vorrat ins Patronenlager legen und die Klappe schließen.',
         action_de='Einschüssig: eine Mikrorakete im Rohr, nach jedem Schuss neu laden; der Treibsatz zündet erst vor der Mündung.',
         fire_de='Eine schnelle, gerade fliegende Mikrorakete mit Aufprallzünder; Spezialmunition und geringer Eigenschaden.',
         reload_en='Open the top loading gate to the rear, place one micro-missile from the left reserve into the chamber, then close the gate.',
         action_en='Single shot: one micro-missile in the tube; reload after each shot. Its motor ignites just past the muzzle.',
         fire_en='One fast, straight-flying micro-missile with an impact fuse; special ammo and low self-damage.'))
