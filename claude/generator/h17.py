"""KH17 „Keilwerk“: geklemmtes Werkstattschwert mit Keilspitze und offenem Parierrahmen."""
from tlib import B
from eng import rect, circ, roundpoly

BG, CU, DK, HL = '#596E7C', '#C58D67', '#20292F', '#E4E7DA'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Durchgehende Griffangel, in zwei Ringen geklemmte Griffhülse und kräftiger Knauf.
    b.C(112,330,300,9,HL,n=10,L='Griffangel')
    b.C(104,132,300,22,CU,n=8,L='Knauf',cap=[(300,0,10,DK,False)])
    b.C(140,264,300,17,DK,n=10,L='Griff')
    for x in range(150,254,18):
        b.C(x,x+7,300,18,BG,n=10,L='Griffring')
    for x in (132,264):
        b.C(x,x+14,300,21,CU,n=8,L='Griffklemmring')
    # Der Parierblock ist ein geteilter Kasten, seitliche Platten überbrücken die Fuge.
    b.P([(278,250),(326,250),(346,268),(346,297),(278,297)],BG,-24,24,r=3,L='Parierblock')
    b.P([(278,300),(346,300),(346,336),(318,346),(278,340)],DK,-24,24,r=3,L='Untergehäuse')
    for z0,z1 in ((24,29),(-29,-24)):
        screws=bolts([(287,285),(287,315),(333,285),(333,315)])
        b.P(rect(280,278,60,44),CU,z0,z1,r=3,L='Parierklemmplatte',
            dec=screws if z0>0 else (),
            xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    # Zelle sitzt in einer seitlichen Aufnahme; ihr Anschluss greift in den Parierblock.
    b.P(rect(298,258,28,77),DK,29,35,r=3,L='Zellhalter')
    b.P(rect(302,268,20,57),HL,35,43,r=3,emit=True,L='Energiezelle',
        dec=[D(rect(306,280+12*i,12,4),CU) for i in range(3)])
    # Zwei quer ausladende Parierbügel bilden einen offenen, abgestützten Rohrrahmen.
    for s in (-1,1):
        b.Y([(282,20*s),(304,20*s),(314,78*s),(302,94*s),(288,84*s)],CU,287,313,r=2,L='Parierstange')
        b.Y([(314,20*s),(330,20*s),(316,84*s),(302,94*s),(302,78*s)],DK,294,306,r=2,L='Parierstrebe')
    # Stumpfe obere Schulter und lange untere Schneide ergeben eine echte Keilklinge.
    b.P([(342,258),(678,246),(760,252),(896,294),(820,324),(512,346),(342,336)],BG,-6,6,r=2,L='Klinge',
        dec=[D([(386,275),(672,263),(742,270),(724,279),(386,289)],HL)])
    b.P([(342,294),(690,283),(798,294),(692,306),(342,312)],DK,-10,10,r=2,L='Mittelrippe',
        dec=[D(roundpoly(rect(392,296,232,5),2),CU)])
    b.P([(346,330),(512,340),(818,318),(888,295),(894,294),(820,324),(512,346),(346,336)],HL,
        -6.2,6.2,emit=True,L='Schneide')
    # Breite Wurzelfassung mit separaten verschraubten Wangen hält Klinge und Parierkasten zusammen.
    b.P([(326,270),(382,268),(394,282),(394,326),(326,332)],CU,-13,13,r=3,L='Klingenwurzel',
        dec=bolts([(342,282),(378,282),(342,318),(378,318)]))
    return b.m


META=dict(num='17',name='Schwert',nick='KEILWERK',col=CU,
 pill='BLAUGRAU · KUPFER · DUNKEL',palette=[BG,CU,DK,HL],center=(500,300,0),
 desc='Ein Werkstattschwert mit breiter Keilklinge, dunkler Mittelrippe und heller Energieschneide. Kupferne Klemmplatten verbinden den geteilten Parierkasten; die seitliche Energiezelle, zwei offene Parierbügel und der ringgeklemmte Rohrgriff bleiben einzeln ablesbar.',
 form='Keilklinge mit leuchtender Schneide · Mittelrippe · verschraubte Klingenwurzel · geteilter Parierblock mit Klemmplatten · Energiezelle im Halter · zwei Parierbügel mit Streben · Rohrgriff mit Klemmringen · Knauf',
 op=dict(reload_de='Die Energiezelle am Parierblock speichert Ladungen für schwere Angriffe; schwere Munition füllt sie wieder auf.',
         action_de='Leichte Hiebe brauchen keine Ladung; schwere Hiebe verbrauchen eine. Blocken mit der quer gehaltenen Klinge zieht Zellenergie.',
         fire_de='Nahkampf mit Schlagfolgen und Sprungangriff; beim Blocken leuchtet die lange untere Schneide.',
         reload_en='The cell on the guard block stores heavy-attack charges; heavy ammo replenishes them.',
         action_en='Light swings need no charge; heavy swings spend one. Guarding with the blade held across the body drains the cell.',
         fire_en='Melee combos and a leaping strike; the long lower edge lights up while guarding.'))
