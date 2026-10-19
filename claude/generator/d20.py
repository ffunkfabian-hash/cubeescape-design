"""KD20 „Glutfang“: helle Raketenpistole mit hohem Rundschlitten und kurzer geklammerter Rohrnase."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#E36548', '#FFD6C9'


def model():
    b = B(); D = b.D
    b.P([(230,306),(290,306),(304,414),(238,420)],K,-25,25,r=12,L='Griff')
    for z0,z1 in ((24,31),(-31,-24)):
        ds=[D(roundpoly(rect(252,345+15*i,22,6),3),K) for i in range(3)]
        b.P([(244,328),(276,328),(290,396),(256,402)],DK,z0,z1,r=10,L='Griffschale',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.P([(218,314),(238,314),(250,398),(238,414),(224,392)],
        P,-26,26,r=10,L='Griffrücken')
    b.P([(226,408),(308,408),(320,426),(314,456),(226,456)],
        P,-30,30,r=12,L='Raketenmagazin')
    b.P(rect(224,446,92,20),DK,-33,33,r=8,L='Magazinboden')
    for z0,z1 in ((29,35),(-35,-29)):
        ds=[D(roundpoly([(246+17*i,440),(252+17*i,424),(259+17*i,440)],3),A) for i in range(3)]
        b.P(rect(240,418,60,26),K,z0,z1,r=8,L='Magazinfenster',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.P(rect(274,310,22,18),A,24,35,r=7,L='Magazinriegel')
    b.P([(212,278),(458,278),(474,296),(466,318),(228,318),(212,304)],
        DK,-28,28,r=12,L='Rahmen')
    # Der hohe helle Schlitten trägt echte Kühlwangen, Rippen und eingelassene Leuchtleisten.
    b.P([(204,194),(410,194),(450,216),(466,246),(458,286),(218,292),(204,276)],
        P,-34,34,r=12,L='Schlitten')
    b.P([(194,208),(218,208),(218,276),(206,286),(194,272)],
        K,-35,35,r=10,L='Schlitten')
    for z0,z1 in ((33,40),(-40,-33)):
        b.P([(356,214),(414,214),(446,232),(448,270),(356,270)],
            K,z0,z1,r=10,L='Schlitten')
        rz0,rz1=(32,42) if z1>0 else (-42,-32)
        for x in (362,388,414):
            b.P([(x,222),(x+12,222),(x+22,260),(x+10,266)],
                P,rz0,rz1,r=6,L='Schlitten')
        ds=[D(roundpoly(rect(244,240,70,5),2),AL,True)]
        b.P(rect(232,238,102,10),A,z0,z1,r=5,emit=True,L='Schlitten',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    rail(b,230,398,194,K,DK,w=14)
    b.C(454,506,250,29,K,n=12,L='Lauf')
    b.C(494,532,250,36,P,n=12,L='Mündungsring',
        cap=[(250,0,27,K,False),(250,0,14,A,True),(250,0,7,AL,True)])
    b.P(rect(466,214,52,12),DK,-13,13,r=6,L='Rohrsteg')
    b.P([(394,292),(462,292),(480,308),(470,326),(400,326)],
        P,-25,25,r=10,L='Laufwiege')
    b.P(arcband(290,400,314,65,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(314,314),(328,314),(338,348),(324,352)],A,-6,6,r=4,L='Abzug')
    return b.m


META=dict(num='20',name='Raketenpistole',nick='GLUTFANG',col=A,
 pill='EMBER-SKIN',palette=[P,DK,A,AL],center=(364,330,0),
 desc='Ein hoher heller Rundschlitten und die kurze, dick geklammerte Rohrnase geben der Raketenpistole eine gedrungene Silhouette. Echte schräge Kühlrippen stehen über dunklen Abgaswangen; zwei ziegelrote Leuchtleisten gliedern die breite Schlittenfläche. Unter dem dicken Griff sitzt ein helles Raketenmagazin mit dunklen Sichtfenstern und schwerem Boden.',
 form='Hoher heller Rundschlitten · dunkle Abgaswangen · sechs schräge Kühlrippen · rote Leuchtleisten · kurze Schiene · dicke Rohrnase mit heller Klemme und Raketenspitze · helle Laufwiege · dunkler Griff mit hellem Rücken · Raketenmagazin mit Sichtfenstern · freier Bügel',
 op=dict(reload_de='Raketenmagazin unten aus dem Griff ziehen, ein volles Magazin mit 6 Mini-Raketen einsetzen und den hohen Schlitten zurückziehen.',
         action_de='Halbautomatik: Der Schlitten läuft nach jedem Schuss zurück, lädt die nächste Rakete und entlüftet zwischen den schrägen Rippen.',
         fire_de='Langsame Einzelschüsse; die Rakete zündet nach der Mündung und explodiert beim Aufprall mit Flächenschaden.',
         reload_en='Pull the rocket magazine from the grip bottom, insert a full magazine of 6 mini rockets and rack the tall slide.',
         action_en='Semi-automatic: the slide cycles after each shot, chambers the next rocket and vents exhaust between its slanted ribs.',
         fire_en='Slow single shots; the rocket ignites beyond the muzzle and explodes on impact for area damage.'))
