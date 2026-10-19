"""KH20 „Düsenkern“: gestufte Rohrpistole mit geklemmtem Düsenkäfig und kurzem Rohrrücken."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

PG, MS, DK, HL = '#536F70', '#C7AC70', '#232D30', '#E2E5D9'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Ein kurzer Rohrsporn mit Klemmring bildet den Rücken, keinen massiven Schaft.
    b.C(178,238,300,9,DK,n=10,L='Rohrrücken')
    b.C(208,224,300,14,MS,n=8,L='Rückenklemmring')
    b.P(rect(164,280,16,52),DK,-15,15,r=4,L='Rückenkappe',
        dec=[D(rect(169,290+12*i,6,5),PG) for i in range(3)])
    # Der bewegliche Schlitten sitzt hinten; die Klemmplatten sichern allein den festen Düsenkäfig.
    b.P([(224,306),(528,306),(528,326),(250,334),(224,324)],DK,-20,20,r=3,L='Rahmen')
    b.P([(226,254),(320,254),(338,270),(338,307),(226,307),(216,296),(216,270)],PG,
        -23,23,r=3,L='Schlitten',
        dec=[D(rect(232+15*i,266,6,28),DK) for i in range(4)]+
            [D(roundpoly(rect(296,268,24,7),2),HL)])
    b.P([(334,248),(502,248),(536,264),(536,306),(334,306)],PG,-25,25,r=3,L='Düsengehäuse',
        dec=[D([(388+22*i,265),(401+22*i,265),(394+22*i,287),(382+22*i,287)],DK) for i in range(5)])
    # Auch der Schlitten selbst hat echte, ablesbare Abgasschlitze als Flächendekor.
    b.P(rect(278,286,42,8),DK,-23.1,23.1,L='Schlitten',   # Schlitzplatte fährt mit dem Schlitten
        dec=[D(rect(284+12*i,287,4,6),MS) for i in range(3)])
    for x in (346,500):
        for z0,z1 in ((25,30),(-30,-25)):
            screws=bolts([(x+9,292),(x+9,318)])
            b.P(rect(x,284,18,40),MS,z0,z1,r=2,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),
                xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    # Schmale Auflager verbinden den oberen Düsenkäfig und den unteren Rahmen über die Fuge.
    for x in (346,500):
        b.P(rect(x,302,18,14),DK,-25,25,L='Rahmenauflager')
    rail(b,348,490,248,DK,HL,w=10)
    b.C(528,608,280,21,DK,n=10,L='Lauf')
    b.C(532,550,280,27,MS,n=8,L='Laufklemmring')
    b.C(592,618,280,25,PG,n=8,L='Mündung',
        cap=[(280,0,16,DK,False),(280,0,6,MS,True)])
    # Halter liegen unten, lassen die weite Bohrung mit Raketenspitze vollständig frei.
    b.P(rect(540,306,54,9),MS,-10,10,r=2,L='Düsenhalter',dec=bolts([(548,310),(586,310)]))
    grip(b,264,332,DK,PG,h=100,w=52,lean=14)
    b.P([(247,428),(314,428),(312,474),(242,474)],PG,-21,21,r=4,L='Raketenmagazin',
        dec=[D(roundpoly(rect(251,438,53,26),3),DK)]+
            [D([(256+12*i,459),(261+12*i,442),(266+12*i,459)],MS) for i in range(4)])
    b.P(rect(240,466,76,10),MS,-23,23,r=3,L='Magazinboden')
    b.P(rect(324,326,18,13),DK,-8,8,r=2,L='Abzugslager')
    trigger_group(b,326,332,MS,DK,grip_x0=306,depth=36)
    for p in b.m.parts[-2:]: p['label']='Abzugsbügel'
    return b.m


META=dict(num='20',name='Raketenpistole',nick='DÜSENKERN',col=MS,
 pill='PETROLGRAU · MESSING · DUNKEL',palette=[PG,MS,DK,HL],center=(393,354,0),
 desc='Eine kompakte Werkstatt-Raketenpistole mit kurzem Rohrrücken, gestuftem Düsenkäfig und messingfarbenen Schellen. Der kurze Schlitten läuft hinter dem fest geklemmten Vordergehäuse; die weite Mündung zeigt die nächste Raketenspitze, das Magazin unter dem Griff vier Spitzen im Sichtfenster.',
 form='Kurzer Rohrrücken mit Klemmring · Schlitten mit Abgasschlitzen · festes Düsengehäuse mit Klemmplatten · Rahmen und Visierschiene · weiter Rohrlauf mit Schelle · Düsenmündung mit sichtbarer Raketenspitze · Griff · Raketenmagazin mit Fenster · Abzug im Bügel',
 op=dict(reload_de='Magazin unter dem Griff nach unten ziehen, ein volles Magazin mit sechs Mini-Raketen einsetzen und den hinteren Schlitten zurückziehen.',
         action_de='Der kurze Schlitten läuft nach jedem Schuss zurück und führt die nächste Rakete zu; Schlitze im Schlitten und Düsenkäfig leiten Abgas ab.',
         fire_de='Langsame halbautomatische Einzelschüsse; die Mini-Rakete zündet nach der weiten Mündung und explodiert beim Aufprall.',
         reload_en='Pull the magazine down from the grip, insert a full six-rocket magazine and rack the rear slide.',
         action_en='The short slide cycles after each shot to feed the next rocket; slots in the slide and fixed nozzle cage vent exhaust.',
         fire_en='Slow semi-automatic shots; each mini rocket ignites beyond the wide muzzle and explodes on impact.'))
