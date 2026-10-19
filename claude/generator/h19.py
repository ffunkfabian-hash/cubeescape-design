"""KH19 „Seilzug“: offene Rohrrahmen-Armbrust mit nach vorn gezogenen Querwurfarmen."""
from tlib import B, grip, rail, trigger_group
from eng import rect, circ, roundpoly
import math

RR, GE, DK, HL = '#985A48', '#E3C34F', '#292827', '#E6DDC6'
BY = 260


def model():
    b = B(); D = b.D

    def bolts(points):
        return [D(circ(x,y,3,10),DK) for x,y in points]

    # Doppelrohrschaft mit leerem Rahmenfenster, nicht der geschlossene G-Schaft.
    b.C(90,286,296,9,DK,n=10,L='Schaft')
    b.C(96,268,350,6,HL,n=10,L='Schaftstrebe')
    b.P(rect(78,280,18,86),DK,-18,18,r=4,L='Schaftkappe',
        dec=[D(rect(82,290+14*i,10,5),RR) for i in range(5)])
    b.P([(250,288),(270,288),(282,338),(272,358),(256,358)],GE,-14,14,r=3,L='Schaftstrebenhalter',
        dec=bolts([(260,302),(268,346)]))
    b.C(230,248,296,15,GE,n=8,L='Schaftklemmring')
    b.P(rect(126,274,102,14),GE,-10,10,r=3,L='Wangenhalter')
    b.P([(120,260),(206,260),(230,272),(230,278),(120,278)],HL,-17,17,r=3,L='Wangenauflage')
    b.P([(266,270),(622,270),(648,282),(648,294),(266,294)],RR,-22,22,r=3,L='Gehäuse')
    b.P([(266,297),(648,297),(648,320),(622,328),(266,328)],DK,-22,22,r=3,L='Untergehäuse')
    for x in (280,604):
        for z0,z1 in ((22,27),(-27,-22)):
            screws=bolts([(x+9,285),(x+9,315)])
            b.P(rect(x,278,18,44),GE,z0,z1,r=2,L='Gehäuseklemmplatte',
                dec=screws if z0>0 else (),
                xdec=[('z-',z0,*d) for d in screws] if z0<0 else ())
    b.P(rect(422,263,260,8),HL,-5,5,L='Führungsrinne')
    b.P(rect(420,248,28,24),DK,-14,14,r=3,L='Schloss',dec=bolts([(434,258)]))
    rail(b,302,396,270,DK,HL,w=10)
    # Der Bolzen liegt vor dem Schloss und auf der Rinne; die Spitze bleibt frei.
    b.C(438,764,BY,3.5,GE,n=8,L='Bolzen')
    b.F(764,794,BY,7,1,HL,n=8,L='Bolzen')
    b.P([(442,BY),(462,BY-12),(478,BY)],RR,-1,1,L='Bolzenfeder')
    b.P([(442,BY),(462,BY+10),(478,BY)],RR,-1,1,L='Bolzenfeder')
    b.P(rect(636,270,46,60),DK,-38,38,r=3,L='Bogenblock',
        dec=[D(roundpoly(rect(644,288,30,22),3),RR)]+bolts([(646,280),(674,320)]))
    # Wurfarme laufen nach vorn, ihre beiden Sehnenhälften zurück zum Schloss.
    for s in (-1,1):
        b.Y([(642,28*s),(676,28*s),(690,98*s),(746,166*s),(730,184*s),(668,116*s)],RR,
            252,272,r=2,L='Wurfarm')
        b.Y([(642,28*s),(678,28*s),(682,66*s),(650,66*s)],GE,248,276,r=2,L='Wurfarmklemmplatte',
            dec=[D(circ(656,44*s,3,10),DK),D(circ(670,54*s,3,10),DK)])
        b.Y([(722,162*s),(742,158*s),(750,174*s),(734,186*s)],GE,250,274,r=2,L='Sehnenaufnahme')
        p0,p1=(740,174*s),(434,2*s)
        dx,dz=p1[0]-p0[0],p1[1]-p0[1]; length=math.hypot(dx,dz)
        nx,nz=-dz/length*1.3,dx/length*1.3
        b.Y([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),
             (p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],HL,BY-1.5,BY+1.5,L='Sehne')
    # Hebel liegt links außerhalb der Klemmplatten, vorderer Drehpunkt am Block.
    b.P([(416,293),(644,293),(644,305),(432,311),(416,305)],GE,27,34,r=3,L='Spannhebel',
        dec=[D(roundpoly(rect(430,298,72,5),2),DK)])
    b.P(circ(642,299,9,12),HL,26,36,L='Spannhebeldrehpunkt',dec=bolts([(642,299)]))
    grip(b,290,328,DK,RR,h=92,w=48,lean=14)
    b.P(rect(348,322,18,13),DK,-8,8,r=2,L='Abzugslager')
    trigger_group(b,350,328,GE,DK,grip_x0=328,depth=34)
    for p in b.m.parts[-2:]: p['label']='Abzugsbügel'
    b.P([(524,326),(558,326),(554,392),(530,392)],DK,-14,14,r=4,L='Vordergriff',
        dec=[D(rect(533,344+12*i,16,5),RR) for i in range(3)])
    return b.m


META=dict(num='19',name='Schwere Armbrust',nick='SEILZUG',col=GE,
 pill='ROSTROT · SIGNALGELB · DUNKEL',palette=[RR,GE,DK,HL],center=(438,305,0),
 desc='Die schwere Werkstattarmbrust sitzt auf einem offenen Doppelrohrschaft mit geklemmter Wangenauflage. Ihre rostroten Wurfarme ziehen sich quer nach vorn, zwei helle Sehnenhälften laufen zum Schloss zurück und der lange gelbe Spannhebel liegt links am geteilten Gehäuse.',
 form='Offener Rohrschaft mit Klemmring und Wangenauflage · Ober- und Untergehäuse mit Klemmplatten · Visierschiene · Führungsrinne mit Schloss · Bolzen mit Spitze und Federn · Bogenblock · zwei geklemmte Wurfarme · zwei Sehnenhälften · Spannhebel links · Griff mit Abzug · Vordergriff',
 op=dict(reload_de='Spannhebel links am vorderen Drehpunkt nach vorn-unten schwenken, Sehne ins Schloss ziehen und einen Bolzen in die Rinne legen.',
         action_de='Der Abzug löst das Schloss für einen Bolzen je Spannung. Nach dem Treffer kann der Bolzen wieder aufgenommen werden.',
         fire_de='Einzelne schwere Bolzen mit hoher Durchschlagskraft; je nach Ausführung mit Sprengkopf oder Widerhaken.',
         reload_en='Swing the left cocking lever forward and down on its front pivot, draw the string into the latch and lay a bolt in the groove.',
         action_en='The trigger releases the latch for one bolt per draw. The bolt can be recovered after impact.',
         fire_en='Single heavy bolts with high penetration; explosive or barbed heads depending on the build.'))
