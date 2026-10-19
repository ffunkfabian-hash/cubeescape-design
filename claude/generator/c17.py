"""KC17 „Gezeiten“: breite Flutklinge und offener, geteilter Parierbogen."""
from eng import rect, roundpoly
from tlib import B

SA, ZO, PE, DK = '#314B78', '#D96043', '#E8DDD9', '#192332'


def model():
    b = B()
    D = b.D
    b.P([(111,290),(123,278),(146,282),(156,299),(144,320),
         (120,324),(108,310)],SA,-19,19,r=8,L='Knauf',
        dec=[D(roundpoly(rect(119,294,22,11),4),ZO,True)])
    b.P([(146,286),(194,277),(246,281),(276,291),(276,312),
         (239,307),(197,304),(146,317)],DK,-14,14,r=9,L='Griff',
        dec=[D(roundpoly([(162+16*i,286),(168+16*i,284),(174+16*i,307),(168+16*i,309)],3),SA) for i in range(6)])
    b.P([(267,272),(296,262),(323,276),(328,310),(310,336),
         (278,329),(264,310)],SA,-23,23,r=9,L='Parierblock')
    b.P([(281,284),(298,278),(312,288),(312,309),(298,319),(282,311)],PE,-26,26,r=6,emit=True,L='Energiezelle')
    # Geteilte seitliche Bögen liegen quer zur Klinge. Der Zwischenraum ist Geometrie, kein dunkler Aufkleber.
    for s in (-1,1):
        b.Y([(272,17*s),(257,46*s),(259,75*s),(281,99*s),
             (308,106*s),(336,93*s),(353,71*s),(339,68*s),
             (319,86*s),(300,89*s),(281,76*s),(275,55*s),
             (291,20*s)],ZO,286,314,r=8,L='Parierstange')
    # Die Flutklinge bäumt sich zunächst auf und läuft in einer abwärts schwingenden Spitze aus.
    b.P([(317,273),(373,249),(438,225),(512,212),(592,216),
         (663,235),(736,264),(803,274),(851,264),(899,244),
         (876,294),(838,329),(786,349),(718,351),(642,337),
         (570,319),(496,314),(417,322),(352,334),(317,323)],PE,-5,5,r=9,L='Klinge',
        dec=[D(roundpoly([(335,315),(420,306),(499,299),(574,305),
                          (648,324),(720,337),(782,334),(832,315),
                          (873,282),(863,304),(838,328),(786,344),
                          (718,345),(642,331),(570,313),(497,308),
                          (417,316),(338,329)],4),ZO,True)])
    b.P([(321,282),(389,264),(458,249),(525,243),(594,250),
         (666,270),(732,294),(789,304),(822,299),(796,316),
         (744,312),(669,289),(596,270),(525,262),(460,266),
         (391,281),(323,301)],SA,-9,9,r=8,L='Mittelrippe')
    b.P([(317,274),(345,263),(363,284),(360,313),(337,329),
         (316,319)],ZO,-11,11,r=7,L='Klingenwurzel')
    # Ein gespaltener Rückenholm schafft ein echtes Fenster oberhalb der Klingenwurzel.
    b.P([(333,271),(373,232),(414,211),(452,208),(484,216),
         (472,227),(447,224),(415,228),(383,245),(351,279)],SA,-6,6,r=8,L='Klingenrücken')
    return b.m


META = dict(
    num='17', name='Schwert', nick='GEZEITEN', col=PE,
    pill='SAPHIR · ZINNOBER · PERLMUTT', palette=[SA,ZO,PE,DK], center=(507,282,0),
    desc='Eine breite perlmuttfarbene Flutklinge schwingt über die saphirblaue Mittelrippe. Zwei zinnoberfarbene Parierbögen '
         'öffnen sich seitlich um den Energieblock; der zurücklaufende Klingenrücken lässt ein echtes Fenster frei.',
    form='Geschwungene Flutklinge · leuchtende Schneide · gebogene Mittelrippe · offene Rückenbrücke · Klingenwurzel · '
         'Parierblock mit Energiezelle · geteilter Parierbogen quer · geschwungener Griff · Knauf',
    op=dict(
        reload_de='Die Energiezelle im Parierblock hält die Ladungen für schwere Angriffe; schwere Munition füllt sie wieder auf',
        action_de='Leichter Schlag ohne Ladung; schwerer Schlag verbraucht eine Ladung. Blocken mit der Klinge zieht Energie aus der Zelle',
        fire_de='Nahkampf mit Schlagkombinationen und Sprungangriff; beim Blocken leuchtet die Schneide',
        reload_en='the energy cell in the guard block stores heavy-attack charges; heavy ammo replenishes them',
        action_en='light swings need no charge; heavy swings spend one charge; guarding with the blade drains the cell',
        fire_en='melee swing combos and leaping strikes; the blade edge lights up while guarding'))
