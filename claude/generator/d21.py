"""KD21 „Donnerfolge“: heller D-Salvenblock mit echtem Lochschaft für fünf kleine Raketen."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#648EE8', '#DAE5FF'


def model():
    b = B(); D = b.D
    # Drei tragende Streben bilden einen echten Durchbruch, keine aufgemalte Tasche.
    b.P(rect(84,238,26,122),K,-27,27,r=10,L='Schaftkappe')
    b.P([(102,240),(248,232),(248,266),(102,276)],P,-23,23,r=12,L='Schaft')
    b.P([(102,326),(154,324),(208,378),(274,414),(276,438),
         (220,420),(154,354),(108,356)],P,-23,23,r=12,L='Schaft')
    b.P(rect(226,250,30,76),DK,-25,25,r=10,L='Schaftanschluss')
    # Helle Hauptvolumen steigen vom vorderen Lager zum hinteren Verschluss an.
    b.P([(246,218),(394,218),(426,236),(426,332),(246,332),(228,312),(228,242)],P,-35,35,r=12,L='Gehäuse')
    b.P([(414,246),(480,246),(500,268),(500,334),(414,334)],P,-32,32,r=12,L='Vordergehäuse')
    b.P(rect(248,308,180,26),DK,-31,31,r=10,L='Unterrahmen')
    b.P(rect(256,222,132,20),DK,-25,25,r=8,L='Verschlussdeckel')
    rail(b,258,390,224,K,DK,w=14)
    for z0,z1 in ((34,42),(-42,-34)):
        panel=[D(roundpoly(rect(264,252,118,12),5),A,True),D(roundpoly(rect(270,280,94,12),5),K)]
        b.P(rect(248,244,154,62),P,z0,z1,r=12,L='Serviceplatte',
            dec=panel if z0>0 else (),xdec=[('z-',z0,*d) for d in panel] if z0<0 else ())
    b.P(rect(300,276,38,16),K,40,56,r=6,L='Ladehebel',dec=[D(rect(308,281,20,5),A)])
    # Magazin sitzt im eigenen tiefen Lager vor dem Bügel.
    b.P(rect(402,324,90,20),DK,-38,38,r=8,L='Magazinaufnahme')
    b.P(rect(408,340,78,58),K,-34,34,r=10,L='Raketenmagazin',
        dec=[D(roundpoly(rect(416,348,62,36),8),P),D(roundpoly(rect(421,352,52,28),5),K)]+
            [D([(423+10*i,376),(427+10*i,357),(431+10*i,376)],A) for i in range(5)])
    b.P(rect(406,390,82,14),DK,-36,36,r=6,L='Magazinboden')
    b.P(rect(388,326,20,22),K,28,42,r=6,L='Magazinriegel')
    b.C(490,602,292,22,K,n=12,L='Laufbett')
    b.P([(492,252),(554,252),(574,272),(574,286),(492,286)],P,-29,29,r=12,L='Handschutz')
    b.P(rect(492,304,82,30),DK,-27,27,r=10,L='Handschutz')
    for x in (506,538,570):
        b.C(x,x+12,292,28,DK,n=12,L='Abgasring',cap=[(272,0,3,A,True)])
    b.C(596,660,292,16,K,n=12,L='Lauf')
    b.F(622,640,292,23,19,P,n=12,L='Abgasring')
    b.C(654,682,292,24,DK,n=12,L='Mündung',cap=[(292,0,14,K,False),(292,0,6,A,True),(292,0,2.5,AL,True)])
    b.P([(260,330),(310,330),(328,426),(274,434)],K,-22,22,r=12,L='Griff')
    b.P(rect(274,422,54,15),DK,-24,24,r=6,L='Griffabschluss')
    b.P(arcband(310,390,332,66,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(330,333),(343,333),(354,372),(341,378)],A,-6,6,r=4,L='Abzug')
    b.P([(520,328),(552,328),(548,394),(526,400)],K,-18,18,r=10,L='Vordergriff')
    return b.m

META=dict(num='21',name='Raketen-Impulsgewehr',nick='DONNERFOLGE',col=A,
 pill='STORM-SKIN',palette=[P,DK,A,AL],center=(380,330,0),
 desc='Ein heller, gestufter Salvenkörper ruht auf einem tiefen Daumenloch-Rahmen, dessen gebogene Unterstrebe bis an den Griff zurückläuft. Sein tiefes Quermagazin zeigt fünf Raketenspitzen; drei Abgasringe verbinden den geteilten Handschutz mit dem kurzen Rohrlauf. Blaue Fenster sitzen in den Serviceplatten.',
 form='Tiefer Daumenloch-Rahmen bis zum Griff · heller Stufenkörper · Serviceplatten · Ladehebel links · Quermagazin mit Boden und Riegel · geteilter Handschutz · drei Abgasringe · Rohrlauf · Mündung · Vordergriff',
 op=dict(reload_de='Raketenmagazin vor dem Abzug nach unten wechseln (5 Raketen), Ladehebel links zurückziehen.',
         action_de='Jede Abzugbetätigung löst eine Zweier-Salve aus; Abgas strömt durch die Schlitze des Handschutzes nach vorn.',
         fire_de='Kleine Raketen explodieren beim Aufprall; Salvenfeuer mit Spezialmunition und kleinem Vorrat.',
         reload_en='Pull the rocket magazine ahead of the trigger down, insert five fresh rockets and pull the left charging handle.',
         action_en='Each trigger pull fires a two-rocket burst; exhaust escapes forward through the handguard slots.',
         fire_en='Small rockets explode on impact; burst fire with special ammo and a small reserve.'))
