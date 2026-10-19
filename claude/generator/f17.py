"""KF17 WELLENZAHN: breite Wellenklinge mit zwei echten Längsfenstern um die Mittelrippe.

Die Klinge ist kein bemaltes Blatt: oberer und unterer Holm verbinden Wurzel und Spitze.
Parierblock, Energiezelle, quer geschwungene Parierstange, Griff und Knauf bleiben erhalten.
"""
from eng import rect
from tlib import B

BL, ZR, DK, HE = '#8AC9E8', '#B54432', '#243343', '#F2E7DA'


def model():
    b = B()
    D = b.D
    b.C(118,148,300,19,ZR,n=8,L='Knauf',cap=[(300,0,8,HE,False)])
    # Breiter geknickter Handballenabschluss statt des zylindrischen G-Griffs.
    b.P([(146,282),(187,272),(242,279),(275,286),(275,313),(236,322),(183,313),(146,316)],
        DK,-14,14,r=8,L='Griff',
        dec=[D([(167,290),(225,289),(252,299),(229,309),(167,303)],BL)])
    b.P([(267,258),(297,249),(326,267),(326,334),(296,351),(267,340)],
        BL,-23,23,r=7,L='Parierblock')
    b.P([(282,279),(305,276),(313,289),(310,321),(284,325)],
        ZR,-25,25,r=4,emit=True,L='Energiezelle')
    # Beide Seiten bilden einen einzigen querliegenden, nach hinten gekrümmten Handschutz.
    b.Y([(271,-78),(296,-68),(318,-29),(318,29),(296,68),(271,78),
         (275,57),(293,22),(293,-22),(275,-57)],DK,282,318,r=3,L='Parierstange')
    # Oberholm: zwei Wellenberge; die untere Kontur lässt ein langes Fenster über der Mittelrippe.
    b.P([(319,270),(435,226),(596,246),(749,214),(881,291),(864,305),
         (744,249),(596,280),(439,262),(326,300)],BL,-5,5,r=3,L='Klinge',
        dec=[D([(374,263),(439,237),(594,256),(597,267),(439,250)],HE)])
    # Unterholm mit spiegelverkehrtem Wellenrhythmus und klarer, leuchtender Schneide.
    b.P([(321,311),(451,334),(593,309),(740,333),(868,295),(881,301),
         (746,366),(591,345),(450,370),(319,342)],BL,-5,5,r=3,L='Klinge',
        dec=[D([(337,330),(450,357),(591,333),(744,353),(853,311),
                 (864,306),(746,362),(591,341),(450,366),(337,337)],ZR,True)])
    b.P([(318,292),(695,293),(876,298),(867,305),(693,307),(318,309)],
        DK,-8,8,r=2,L='Mittelrippe')
    b.P([(319,274),(345,266),(357,283),(357,326),(340,345),(319,337)],
        ZR,-9,9,r=4)
    return b.m


META = dict(
    num='17', name='Schwert', nick='WELLENZAHN', col=BL,
    pill='BLASSBLAU · ZIEGELROT · TINTE', palette=[BL,ZR,DK,HE], center=(501,294,0),
    desc='Zwei breite blassblaue Wellenholme umschließen lange offene Fenster über und unter der dunklen Mittelrippe. '
         'Die ziegelrote Schneide folgt dem unteren Wellenzug; im hohen Parierblock sitzt die Energiezelle. '
         'Eine quer zurückgeschwungene Parierstange schützt den geknickten Griff mit kräftigem Knauf.',
    form='Geteilte Wellenklinge mit zwei offenen Längsfenstern · Mittelrippe · leuchtende Schneide · '
         'Klingenwurzel · Parierblock mit Energiezelle · quer geschwungene Parierstange · geknickter Griff · Knauf',
    op=dict(
        reload_de='Die Energiezelle im Parierblock hält Ladungen für schwere Angriffe; schwere Munition füllt sie wieder auf.',
        action_de='Leichte Hiebe brauchen keine Ladung, schwere Hiebe verbrauchen eine; Blocken mit quer gehaltener Klinge zieht Energie aus der Zelle.',
        fire_de='Nahkampf mit Schlagkombinationen und Sprungangriff; beim Blocken leuchtet die ziegelrote Schneide.',
        reload_en='The energy cell in the guard block holds heavy-attack charges; heavy ammo refills it.',
        action_en='Light swings use no charge, heavy swings spend one; guarding with the blade held across the body drains the cell.',
        fire_en='Melee swing combos and leaping strikes; the brick-red cutting edge lights up while guarding.'))
