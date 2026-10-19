"""KH18 „Flanschwacht“: teleskopierte Werkstattglefe mit breitem Flanschkopf und Schildflügelpaar."""
from tlib import B, trigger_group
from eng import rect, circ, roundpoly

TG, LI, DK, HL = '#79796C', '#B9CE62', '#252B27', '#E2E1CC'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,2.8,10),DK) for x,y in points]

    b.C(54,82,300,20,TG,n=8,L='Knauf',cap=[(300,0,8,LI,False)])
    b.C(80,338,300,11,DK,n=12,L='Stange')
    b.C(330,624,300,8,HL,n=10,L='Teleskopstange')
    for x in (84,182,322,502,606):
        b.C(x,x+16,300,16,LI,n=8,L='Stangenklemmring')
    b.C(100,182,300,15,DK,n=10,L='Griff')
    for x in range(112,174,15):
        b.C(x,x+5,300,16,TG,n=10,L='Griffring')
    # Ober- und Untergehäuse fassen die Stange; der Abzug liegt vor dem hinteren Griff.
    b.P([(198,276),(262,276),(278,286),(278,298),(198,298)],TG,-18,18,r=3,L='Gehäuse',
        dec=[D(roundpoly(rect(214,284,44,6),2),HL)])
    b.P(rect(198,301,80,23),DK,-18,18,r=3,L='Untergehäuse')
    for z0,z1 in ((18,23),(-23,-18)):
        screws=bolts([(205,289),(205,314),(269,289),(269,314)])
        b.P(rect(200,282,74,37),LI,z0,z1,r=3,L='Gehäuseklemmplatte',
            dec=screws if z0>0 else (),
            xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    b.P(rect(210,318,18,13),DK,-8,8,r=2,L='Abzugslager')
    trigger_group(b,212,324,LI,DK,grip_x0=198,depth=28)
    for p in b.m.parts[-2:]: p['label']='Abzugsbügel'
    b.C(388,480,300,15,DK,n=10,L='Vordergriff')
    for x in range(398,474,16):
        b.C(x,x+5,300,16,TG,n=10,L='Vordergriffring')
    # Der Zellenkäfig sitzt vollständig auf der Stange vor der Kopfaufnahme.
    b.P([(524,276),(588,276),(602,286),(602,314),(588,324),(524,324)],TG,-19,19,r=3,L='Zellhalter',
        dec=bolts([(534,285),(590,315)]))
    b.P(rect(536,286,52,28),HL,-20,20,r=3,emit=True,L='Energiezelle',
        dec=[D(rect(544+14*i,288,5,24),LI) for i in range(3)])
    b.C(608,638,300,23,LI,n=8,L='Kopfklemmring')
    b.P([(628,246),(666,246),(684,266),(684,334),(666,354),(628,354)],DK,-26,26,r=3,L='Klingenfassung',
        dec=bolts([(640,261),(640,339)]))
    # Beide symmetrischen Flügel tragen das exakte Bewegungslabel Schildflügel.
    for s in (-1,1):
        b.Y([(642,24*s),(676,24*s),(698,70*s),(680,88*s),(648,70*s)],LI,274,326,r=3,L='Schildflügel')
        b.Y([(644,24*s),(656,24*s),(662,48*s),(650,48*s)],HL,286,314,r=2,L='Schildgelenk')
    # Breiter, oben gezogener Flanschkopf; der Emitter bleibt auf der Stangenachse.
    b.P([(678,248),(728,210),(800,218),(852,252),(920,300),(848,336),(750,348),(678,334)],TG,
        -7,7,r=2,L='Klinge',dec=[D([(696,256),(736,226),(794,234),(824,252),(780,244),(738,239)],HL)])
    b.P([(680,328),(750,342),(846,330),(912,300),(920,300),(848,336),(750,348),(680,334)],LI,
        -7.2,7.2,emit=True,L='Schneide')
    b.C(676,900,300,6,DK,n=8,L='Emitter')
    b.F(900,924,300,6,2,HL,n=8,emit=True,L='Emitter')
    # Zwei sichtbare Stützen sichern den Energiepfad an der breiten Klingenwurzel.
    b.P(rect(674,278,62,9),LI,-11,11,r=2,L='Emitterhalter',dec=bolts([(686,282),(726,282)]))
    b.P(rect(674,314,62,9),LI,-11,11,r=2,L='Emitterhalter',dec=bolts([(686,318),(726,318)]))
    return b.m


META=dict(num='18',name='Glefe',nick='FLANSCHWACHT',col=LI,
 pill='TONGRAU · LIMETTE · DUNKEL',palette=[TG,LI,DK,HL],center=(489,294,0),
 desc='Die Werkstattglefe verbindet eine teleskopierte Rohrstange mit einem breiten, hochgezogenen Flanschkopf. Vor dem Klingenkopf sitzt die Energiezelle im verschraubten Käfig; zwei limettengrüne Schildflügel flankieren den axialen Emitter, während hinten Abzug und zwei Griffzonen liegen.',
 form='Teleskopstange mit Klemmringen und Knauf · hinterer Griff · geteiltes Abzugsgehäuse mit Klemmplatten · Abzug im Bügel · Vordergriff · Energiezelle im Käfig · Klingenfassung · zwei Schildflügel · breite Klinge mit Schneide · Emitter und Spitze',
 op=dict(reload_de='Nahkampftreffer laden die Zelle vor dem Kopf. Zum Nachladen die Zelle im Halter drehen und für vier Schuss einrasten.',
         action_de='Der Abzug feuert aus dem Emitter in der Klinge; beim Blocken klappen beide Schildflügel seitlich aus und bauen den Schild auf.',
         fire_de='Zweihändige Hiebe oder Energiegeschosse aus der Hüfte; die ausgeklappten Flügel halten den Schild vor dem Kopf.',
         reload_en='Melee hits charge the cell before the head. To reload, twist the cell in its holder and lock it for four shots.',
         action_en='The trigger fires from the blade emitter; guarding swings both shield wings outward to form a shield.',
         fire_en='Two-handed swings or hip-fired energy bolts; the deployed wings hold the shield ahead of the head.'))
