"""KD18 „Nachtwache“: helle Hakenglefe mit geklammertem Stiel und breiten Schildflügeln."""
from tlib import B
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#8177D9', '#DDD8FF'


def model():
    b = B(); D = b.D
    b.C(62,108,300,24,DK,n=12,L='Knauf',cap=[(300,0,11,A,True)])
    b.C(102,648,300,15,P,n=12,L='Stange')
    b.P(rect(112,280,124,40),K,-20,20,r=12,L='Griff')
    for x in (122,150,178,206):
        b.P(rect(x,278,12,44),DK,-23,23,r=6,L='Griffring')
    b.P([(230,268),(314,268),(340,284),(340,322),(230,322)],P,-26,26,r=12,L='Gehäuse')
    for z0,z1 in ((25,32),(-32,-25)):
        ds=[D(roundpoly(rect(254,288,46,8),4),A,True)]
        b.P(rect(244,278,66,32),DK,z0,z1,r=10,L='Bedienwange',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.P(arcband(232,334,320,54,9),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(254,320),(268,320),(278,348),(264,352)],A,-6,6,r=4,L='Abzug')
    b.P(rect(390,278,104,44),K,-22,22,r=12,L='Vordergriff')
    for x in (402,432,462):
        b.P(rect(x,276,14,48),DK,-25,25,r=7,L='Griffring')
    # Drehzelle mit zwei tragenden Klemmen und eigenen seitlichen Kühlwangen.
    b.P([(512,268),(596,268),(618,286),(618,316),(596,332),(512,332)],
        P,-28,28,r=12,L='Energiezelle')
    for x in (506,596):
        b.C(x,x+20,300,32,DK,n=12,L='Zellenklemme')
    for z0,z1 in ((27,34),(-34,-27)):
        ds=[D(roundpoly(rect(542+13*i,288,7,24),3),A,True) for i in range(3)]
        b.P(rect(534,281,52,38),K,z0,z1,r=10,L='Zellenwange',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.P(rect(552,262,28,16),DK,-12,12,r=6,L='Zellenriegel')
    b.P([(614,244),(652,244),(672,266),(672,334),(650,356),(614,356)],
        DK,-31,31,r=12,L='Klingenfassung')
    # Breite gerundete Flügel sitzen auf getrennten seitlichen Scharnierkappen.
    for s in (-1,1):
        z0,z1=(29,42) if s>0 else (-42,-29)
        b.P(circ(640,300,22,16),K,z0,z1,L='Schildscharnier',
            dec=[D(circ(640,300,10,12),A,True)])
        b.Y([(620,36*s),(658,36*s),(690,84*s),(672,108*s),(634,100*s),(616,74*s)],
            P,266,334,r=12,L='Schildflügel',
            dec=[D(roundpoly([(632,48*s),(650,48*s),(676,84*s),(664,94*s),
                              (640,88*s),(628,70*s)],7),DK),
                 D(roundpoly([(638,54*s),(646,54*s),(668,82*s),(662,86*s)],4),A,True)])
    # Hoher, rückwärts gekrümmter Haken und kurzer Emitterkopf unterscheiden die Glefe vom Spalter.
    b.P([(654,258),(678,210),(722,178),(756,188),(790,228),(848,258),
         (878,300),(820,342),(716,360),(654,338)],P,-10,10,r=12,L='Klinge')
    b.P([(666,326),(718,346),(814,330),(860,300),(878,300),(820,342),
         (716,360),(666,340)],A,-11,11,r=8,emit=True,L='Leuchtschneide',
        dec=[D(roundpoly([(698,337),(720,347),(808,332),(812,337),
                          (720,354),(698,344)],3),AL,True)])
    for z0,z1 in ((9,17),(-17,-9)):
        ds=[D(roundpoly([(706,236),(728,216),(738,222),(716,244)],4),A,True)]
        b.P([(678,258),(696,222),(726,200),(746,208),(766,234),(774,264),
             (742,278),(678,282)],DK,z0,z1,r=10,L='Hakenrippe',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.C(658,878,300,13,K,n=12,L='Emitter',cap=[(300,0,9,A,True),(300,0,4,AL,True)])
    b.C(852,878,300,20,DK,n=12,L='Emitterfassung')
    b.F(878,892,300,13,6,A,n=12,emit=True,L='Emitter')
    return b.m


META=dict(num='18',name='Glefe',nick='NACHTWACHE',col=A,
 pill='DUSK-SKIN',palette=[P,DK,A,AL],center=(478,284,0),
 desc='Die helle Hakenglefe setzt einen hohen, rückwärts gekrümmten Klingenkopf auf eine kräftige helle Stange. Dunkle Hakenrippen und eine violette Leuchtschneide fassen den mittigen Geschossemitter ein. Breite seitliche Schildflügel sitzen auf eigenen Scharnierkappen; Drehzelle, zwei Griffe und freier Abzugsbügel bleiben deutlich ablesbar.',
 form='Helle Stange · Ringgriffe · helles Abzugsgehäuse mit dunklen Wangen · freier Bügel · geklammerte Drehzelle · dunkle Klingenfassung · zwei breite Schildflügel · hoher heller Hakenkopf · violette Schneide · kurzer mittiger Emitter',
 op=dict(reload_de='Die Energiezelle hinter der Klingenfassung lädt durch Nahkampftreffer; zum Nachladen zwischen den Klemmen drehen und einrasten (4 Schuss).',
         action_de='Abzug feuert ein Energiegeschoss aus dem Emitter; beim Blocken klappen beide Schildflügel nach außen und bauen den Schild auf.',
         fire_de='Klingenhiebe und Fernschüsse aus der Hüfte; der vor dem Klingenkopf aufgebaute Schild hält Treffer ab.',
         reload_en='Melee hits recharge the cell behind the blade mount; twist it between the clamps and relock to reload (4 shots).',
         action_en='The trigger fires an energy bolt from the emitter; guarding unfolds both shield wings to form the shield.',
         fire_en='Blade swings and hip-fired energy bolts; the shield projected ahead of the blade head absorbs hits.'))
