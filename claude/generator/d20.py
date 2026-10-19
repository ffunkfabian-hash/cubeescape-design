"""KD20 „Glutfang“: gedrungene Raketenpistole mit tiefem Rundschlitten und breitem Rohr."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#E36548', '#FFD6C9'


def model():
    b = B(); D = b.D
    b.P([(230,306),(290,306),(304,414),(238,420)],K,-25,25,r=12,L='Griff',
        dec=[D(roundpoly([(244,328),(278,328),(290,396),(256,400)],8),DK),
             D(roundpoly(rect(251,340,18,38),7),P)])
    b.P([(228,408),(310,408),(322,426),(316,458),(228,458)],DK,-29,29,r=12,L='Raketenmagazin',
        dec=[D(roundpoly(rect(242,420,60,26),8),K)]+
            [D(roundpoly([(248+17*i,442),(254+17*i,426),(261+17*i,442)],3),A) for i in range(3)])
    b.P([(212,278),(460,278),(472,292),(466,316),(228,316),(212,304)],
        K,-27,27,r=10,L='Rahmen',
        dec=[D(roundpoly(rect(234,290,208,10),5),P)])
    b.P([(204,216),(430,216),(474,238),(480,274),(460,290),(218,290),(204,276)],
        DK,-32,32,r=12,L='Schlitten',
        dec=[D(roundpoly([(220,230),(368,230),(394,244),(386,264),(220,266)],10),P),
             D(roundpoly(rect(236,243,122,9),4),A,True)])
    for i in range(4):
        b.m.decal('z+',32,roundpoly([(402+16*i,240),(412+16*i,246),
                                  (402+16*i,270),(392+16*i,266)],4),K)
    rail(b,236,408,216,K,DK,w=13)
    b.C(470,530,254,27,K,n=12,L='Lauf',
        cap=[(254,0,20,K,False),(254,0,12,A,True),(254,0,6,AL,True)])
    # Beide Bandenden greifen in den Rahmen; die Raketen bleiben hinter dem Griff.
    b.P(arcband(290,400,314,65,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(314,314),(328,314),(338,348),(324,352)],A,-6,6,r=4,L='Abzug')
    return b.m


META=dict(num='20',name='Raketenpistole',nick='GLUTFANG',col=A,
 pill='EMBER-SKIN',palette=[P,DK,A,AL],center=(364,334,0),
 desc='Die gedrungene Raketenpistole bündelt den kurzen Lauf in einem tiefen, weich gerundeten Schlitten mit heller Deckplatte. Schräge Abgasschlitze, die sichtbare Mini-Raketenspitze im breiten Rohr und das Fenster des schweren Griffmagazins erklären die Raketenmechanik.',
 form='Tiefer Rundschlitten · helle Deckplatte mit Leuchtstreifen · schräge Abgasschlitze · kurze Visierschiene · breites Raketenrohr mit Raketenspitze · kräftiger Rahmen · dicker Griff · Raketenmagazin mit Fenster · freier gebogener Abzugsbügel',
 op=dict(reload_de='Raketenmagazin unten aus dem Griff ziehen, ein volles Magazin mit 6 Mini-Raketen einsetzen und den Schlitten zurückziehen.',
         action_de='Halbautomatik: Der Schlitten läuft nach jedem Schuss zurück, lädt die nächste Rakete und entlüftet über die schrägen Schlitze.',
         fire_de='Langsame Einzelschüsse; die Rakete zündet nach der Mündung und explodiert beim Aufprall mit Flächenschaden.',
         reload_en='Pull the rocket magazine from the grip bottom, insert a full magazine of 6 mini rockets and rack the slide.',
         action_en='Semi-automatic: the slide cycles after each shot, chambers the next rocket and vents exhaust through its slanted slots.',
         fire_en='Slow single shots; the rocket ignites beyond the muzzle and explodes on impact for area damage.'))
