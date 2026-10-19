"""KD17 „Lichtspalter“: dunkler, bauchiger Spalter mit versetzten Deckplatten und rosa Schneide."""
from tlib import B
from eng import rect, roundpoly

P, DK, K, A, AL = '#D8DCE0', '#3A3D44', '#1C2027', '#F47BC7', '#FFE0F4'


def model():
    b = B(); D = b.D
    b.C(94,140,300,27,DK,n=12,L='Knauf',cap=[(300,0,15,K,False),(300,0,8,A,True)])
    b.C(130,150,300,24,P,n=12,L='Knaufklemme')
    b.P(rect(144,280,142,40),K,-20,20,r=12,L='Griff')
    for x in (158,182,206,230,254):
        b.P(rect(x,278,12,44),DK,-23,23,r=6,L='Griffring')
    b.P([(274,246),(328,246),(350,264),(350,338),(328,358),(274,358)],
        DK,-29,29,r=12,L='Parierblock')
    b.P(rect(288,282,38,38),K,-32,32,r=10,L='Energiezelle',
        dec=[D(roundpoly(rect(296,290,22,22),7),A,True),D(roundpoly(rect(303,295,8,12),4),AL,True)])
    for y in (258,330):
        b.P(rect(280,y,50,16),P,-32,32,r=7,L='Zellenklemme')
    # Breite Querparierstange mit verdickten Endkappen, keine Visieraufnahme.
    b.Y([(282,-80),(310,-76),(336,-30),(336,30),(310,76),(282,80),
         (294,26),(294,-26)],DK,280,322,r=10,L='Parierstange')
    for s in (-1,1):
        b.Y([(282,62*s),(316,60*s),(324,76*s),(310,90*s),(280,90*s)],
            P,278,324,r=8,L='Parierkappe')
    # Ein gekrümmter breiter Bauch statt der langen, geraden G-Klinge.
    b.P([(340,250),(486,234),(686,214),(768,228),(834,270),(810,316),
         (712,374),(528,368),(340,342)],DK,-10,10,r=12,L='Klinge')
    b.P([(350,328),(530,352),(706,358),(800,302),
         (810,316),(712,374),(528,368),(350,342)],A,-11,11,r=8,emit=True,L='Leuchtschneide',
        dec=[D(roundpoly([(388,339),(530,358),(706,364),(776,326),
                          (780,332),(708,370),(528,364),(388,345)],3),AL,True)])
    # Die terminale Schneidenkappe definiert die Spitze, unabhängig vom tiefen Schneidenbauch.
    b.P([(790,314),(820,270),(834,270),(810,316),(800,322)],
        A,-11,11,r=8,emit=True,L='Klingenspitze')
    b.P([(340,290),(538,278),(734,274),(776,290),(724,310),(538,312),(340,308)],
        K,-18,18,r=10,L='Mittelrippe',
        dec=[D(roundpoly([(382,295),(538,286),(712,284),(730,290),
                          (710,296),(538,298),(382,303)],4),A,True)])
    b.P([(332,254),(382,250),(402,274),(402,322),(380,346),(332,340)],
        K,-23,23,r=10,L='Klingenwurzel')
    for z0,z1 in ((9,15),(-15,-9)):
        b.P([(406,256),(534,244),(548,260),(536,278),(406,286)],P,z0,z1,r=10,L='Klingendeckplatte')
        b.P([(558,240),(682,228),(748,240),(776,260),(742,272),(556,278)],
            P,z0,z1,r=10,L='Klingendeckplatte')
        for x,y in ((452,316),(530,322),(608,324)):
            b.P([(x,y),(x+14,y+2),(x+34,y+30),(x+18,y+28)],
                K,z0,z1,r=6,L='Klingenrippe')
    return b.m


META=dict(num='17',name='Schwert',nick='LICHTSPALTER',col=A,
 pill='PRISMATIC-VERSION',palette=[DK,P,A,AL],center=(466,298,0),
 desc='Ein bauchiger dunkler Spalter mit hochgezogenem Rücken und schwerer Schneidenwölbung. Versetzte helle Deckplatten sitzen als eigene Schalen über dem Klingenkörper; eine breite rosa Leuchtschneide folgt dem unteren Bogen. Mittelrippe, kräftige Wurzel und gekappte Querparierstange leiten die Last zum dicken Ringgriff.',
 form='Dunkler bauchiger Spalter · hochgezogener Rücken · rosa Schneidenbogen mit eigener Spitze · vier helle Deckplatten · sechs Klingenrippen · schwere Mittelrippe · Klingenwurzel · Energiezelle · gekappte Querparierstange · Ringgriff · Knauf',
 op=dict(reload_de='Die Energiezelle im Parierblock hält die Ladungen für schwere Angriffe; schwere Munition füllt sie auf.',
         action_de='Leichter Schlag ohne Ladung, schwerer Schlag verbraucht eine Ladung; Blocken mit der quer gehaltenen Klinge entlädt die Zelle.',
         fire_de='Nahkampf mit Schlagkombinationen und Sprungangriff; die rosa Schneide leuchtet beim Blocken auf.',
         reload_en='The guard-block energy cell stores heavy-attack charges; heavy ammo replenishes them.',
         action_en='Light swings cost no charge; a heavy swing spends one charge. Guarding with the blade held across the body drains the cell.',
         fire_en='Melee swing combinations and leaping strikes; the pink edge lights up while guarding.'))
