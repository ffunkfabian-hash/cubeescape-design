"""KH21 „Taktrohr“: Rahmengewehr für Raketensalven mit breitem Quermagazin und freiem Rohrlauf."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly

MG, CU, DK, HL = '#66745A', '#C58A64', '#252C26', '#E1E4D1'


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Gestaffelte Rohrschulter mit tiefer Gegenstrebe und getrennter Wangenauflage.
    b.C(94,294,284,9,DK,n=10,L='Schaft')
    b.C(104,262,344,6,HL,n=10,L='Schaftstrebe')
    b.P(rect(82,268,18,96),DK,-19,19,r=4,L='Schaftkappe',
        dec=[D(rect(87,280+15*i,8,5),MG) for i in range(5)])
    b.P([(244,278),(268,278),(280,328),(266,352),(252,352)],CU,-15,15,r=3,L='Schaftstrebenhalter',
        dec=bolts([(256,292),(262,340)]))
    b.C(220,240,284,16,CU,n=8,L='Schaftklemmring')
    b.P(rect(118,263,96,13),CU,-11,11,r=3,L='Wangenhalter')
    b.P([(112,248),(196,248),(220,260),(220,268),(112,268)],HL,-18,18,r=3,L='Wangenauflage')
    b.P([(278,246),(504,246),(534,266),(534,295),(278,295)],MG,-25,25,r=3,L='Gehäuse',
        dec=[D(roundpoly(rect(300,259,64,8),3),HL),D(rect(426,258,48,5),CU)])
    b.P([(278,298),(534,298),(534,330),(508,340),(278,340)],DK,-25,25,r=3,L='Untergehäuse')
    for x in (292,502):
        for z0,z1 in ((25,30),(-30,-25)):
            screws=bolts([(x+9,283),(x+9,318)])
            b.P(rect(x,275,18,51),CU,z0,z1,r=3,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),
                xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    rail(b,322,486,246,DK,HL,w=11)
    b.P(rect(350,273,70,17),HL,25,31,r=3,L='Verschluss')
    b.P(rect(378,277,19,9),CU,31,47,r=2,L='Ladehebel')
    # Breites Quermagazin ist vor dem Abzugsbügel im angesetzten Schacht verriegelt.
    b.P(rect(454,328,80,18),CU,-31,31,r=3,L='Magazinschacht',dec=bolts([(464,336),(524,336)]))
    b.P([(458,340),(534,340),(540,352),(540,386),(458,386)],MG,-58,58,r=4,L='Raketenmagazin',
        dec=[D(roundpoly(rect(466,350,64,26),3),DK)]+
            [D([(470+12*i,372),(475+12*i,354),(480+12*i,372)],CU) for i in range(5)])
    b.P(rect(456,380,86,10),CU,-60,60,r=2,L='Magazinboden')
    # Offener Handschutz: zwei gelochte Holme fassen den sichtbaren Rohrlauf ein.
    b.P(rect(532,262,162,17),MG,-19,19,r=3,L='Handschutz',
        dec=[D([(548+27*i,266),(562+27*i,266),(556+27*i,275),(542+27*i,275)],DK) for i in range(5)])
    b.P(rect(532,312,162,17),DK,-19,19,r=3,L='Handschutz',
        dec=[D(rect(548+27*i,317,16,5),CU) for i in range(5)])
    b.C(528,786,294,12,HL,n=12,L='Lauf')
    for x in (534,670):
        b.C(x,x+18,294,29,CU,n=8,L='Laufrahmenschelle')
    b.P(rect(574,326,48,12),CU,-17,17,r=2,L='Vordergriffhalter',
        dec=bolts([(584,332),(612,332)]))
    b.F(716,742,294,24,17,DK,n=10,L='Abgasring')
    b.C(786,824,294,19,CU,n=8,L='Mündung',
        cap=[(294,0,12,DK,False),(294,0,4,HL,True)])
    # Der Griff sitzt hinter dem Magazin, der Bügel hält Abstand zum breiten Kasten.
    grip(b,294,340,DK,MG,h=92,w=48,lean=14)
    b.P(rect(352,334,18,13),DK,-8,8,r=2,L='Abzugslager')
    trigger_group(b,354,340,CU,DK,grip_x0=332,depth=34)
    for p in b.m.parts[-2:]: p['label']='Abzugsbügel'
    b.P([(580,336),(616,336),(610,404),(586,404)],DK,-15,15,r=4,L='Vordergriff',
        dec=[D(rect(589,352+12*i,17,5),MG) for i in range(4)])
    return b.m


META=dict(num='21',name='Raketen-Impulsgewehr',nick='TAKTROHR',col=CU,
 pill='MOOSGRÜN · KUPFER · DUNKEL',palette=[MG,CU,DK,HL],center=(453,319,0),
 desc='Das Werkstattgewehr für Raketensalven besitzt einen offenen Rohrschaft und einen sichtbaren Lauf zwischen gelochten Handschutzholmen. Kupferne Klemmplatten halten die geteilte moosgrüne Gehäuseschale; das breite Quermagazin sitzt vor dem Abzug, und der Ladehebel liegt links auf dem Verschluss.',
 form='Offener Rohrschaft mit Klemmring und Wangenauflage · Ober- und Untergehäuse mit Klemmplatten · Visierschiene · Verschluss und Ladehebel links · querliegendes Raketenmagazin mit fünf Spitzen im Fenster · offener Handschutz mit Abgasschlitzen · Rohrlauf · Abgasring und Mündung · Griff mit Abzug · Vordergriff',
 op=dict(reload_de='Das Quermagazin vor dem Abzug nach unten ziehen, ein neues mit fünf Raketen einsetzen und den linken Ladehebel zurückziehen.',
         action_de='Jeder Abzug feuert eine Salve aus zwei Raketen; der Verschluss führt nach, Abgas entweicht über Handschutzschlitze und Abgasring.',
         fire_de='Zweiersalven aus Spezialmunition mit kleinem Vorrat; die Raketen explodieren beim Aufprall.',
         reload_en='Pull the transverse magazine ahead of the trigger down, insert a fresh five-rocket magazine and pull the left charging handle.',
         action_en='Each trigger pull fires a two-rocket burst; the bolt feeds the next rocket, while handguard slots and the gas ring vent exhaust.',
         fire_en='Two-rocket bursts using special ammo with a small reserve; rockets explode on impact.'))
