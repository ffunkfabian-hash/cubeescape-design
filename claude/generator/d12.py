"""KD12 „Funkenschlag“: heller Rundrahmen und zurückgeneigter Griff um die feste Trommelachse."""
import math
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#FF914A', '#FFE0BA'
AX, RING = 290, 20


def model():
    b = B(); D = b.D
    # Der gekrümmte Griff zieht nach hinten; der helle Rahmen ist selbst das tragende Volumen.
    b.P([(244,316),(292,322),(286,356),(254,432),(216,442),(202,424),(222,352)],P,-25,25,r=12,L='Griff')
    for z0,z1 in ((24,30),(-30,-24)):
        grooves=[D(roundpoly([(240,363),(251,366),(236,402),(226,406)],5),DK)]
        b.P([(241,345),(272,350),(246,414),(222,422),(218,410)],K,z0,z1,r=10,L='Griffschale',
            dec=grooves if z0>0 else (),xdec=[('z-',z0,*d) for d in grooves] if z0<0 else ())
    b.P([(211,421),(251,414),(258,434),(218,446),(204,436)],DK,-28,28,r=9,L='Griffkappe')
    b.P([(220,268),(238,246),(276,242),(302,256),(302,319),(282,342),(244,338),(220,314)],
        P,-27,27,r=12,L='Rahmen')
    b.P(rect(248,278,34,31),DK,26,33,r=10,L='Schlossdeckel',
        dec=[D(roundpoly(rect(257,289,16,8),4),A,True)])
    # Getrennte Brücken umfassen die unveränderte Trommel, kein massiver Block im Fenster.
    b.P([(274,240),(388,238),(405,250),(402,262),(280,262)],P,-24,24,r=10,L='Oberbrücke')
    b.P([(288,320),(390,320),(400,332),(385,346),(300,342)],P,-23,23,r=9,L='Unterbrücke')
    b.P([(374,252),(401,248),(411,272),(405,320),(390,336),(374,324)],P,-27,27,r=12,L='Rahmen')
    # k=0 bleibt exakt (y=270,z=0). Zylinderachse, Kammerkreis und Lauf ändern sich nicht.
    b.C(300,374,AX,32,DK,n=16,L='Trommel',
        cap=[(AX,0,29,P,False)]+
            [(AX-RING*math.cos(k*math.pi/3),RING*math.sin(k*math.pi/3),6,'#050506',False)
             for k in range(6)]+[(AX,0,7,K,False)])
    for x in (306,358):
        b.C(x,x+8,AX,33,K,n=16,L='Trommel')
    b.C(296,303,AX,11,K,n=12,L='Trommel')
    b.P(rect(268,308,22,11),A,26,38,r=5,L='Trommelriegel')
    b.P(circ(258,260,9,16),DK,-31,31,L='Hahnachse')
    b.P([(244,250),(242,231),(254,219),(267,225),(278,253),(264,264)],A,-9,9,r=6,L='Hahn')
    rail(b,292,394,240,K,DK,w=12)
    # Ein kurzer bauchiger Mantel statt des langen G-Laufkastens.
    b.P([(399,245),(464,244),(504,258),(518,277),(510,299),(402,308)],P,-28,28,r=12,L='Laufmantel')
    b.P([(405,286),(503,280),(510,296),(494,312),(405,316)],DK,-23,23,r=10,L='Unterlaufträger')
    b.P(rect(422,253,52,18),DK,27,33,r=8,L='Kühlplatte',
        dec=[D(roundpoly(rect(431,259,32,6),3),K)])
    b.P(rect(414,278,66,9),A,27,31,r=4,L='Ladestandanzeige',emit=True)
    b.C(506,521,AX-RING,18,DK,n=12,L='Laufbund')
    b.C(518,542,AX-RING,14,K,n=12,L='Lauf',
        cap=[(AX-RING,0,10,P,False),(AX-RING,0,7,'#050506',False)])
    b.C(374,474,314,5,K,n=12,L='Ausstoßerstange')
    b.P(rect(460,299,22,24),P,-11,11,r=8,L='Ausstoßerführung')
    b.C(471,485,314,8,DK,n=12,L='Ausstoßerknopf')
    b.P(arcband(288,388,338,62,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(317,340),(331,340),(344,376),(331,381)],A,-6,6,r=5,L='Abzug')
    return b.m


META=dict(num='12',name='Handfeuerwaffe',nick='FUNKENSCHLAG',col=A,
 pill='SOLAR-VERSION',palette=[P,DK,A,AL],center=(372,332,0),
 desc='Ein heller, weich gerundeter Rahmen umfasst die dunkle Sechskammertrommel zwischen getrennten Brücken. Der zurückgeneigte Rundgriff und der kurze bauchige Laufmantel bilden eine kompakte Revolversilhouette; der orange Hahn bleibt frei sichtbar.',
 form='Heller Rundrahmen · getrennte Trommelbrücken · dunkle Sechskammertrommel · zurückgeneigter Griff mit dunklen Schalen · Trommelriegel links · freier Hahn · kurzer bauchiger Laufmantel · Ausstoßerstange · offener Abzugsbügel',
 op=dict(reload_de='Trommelriegel links drücken, Trommel nach links ausschwenken, sechs Patronen laden und die Trommel wieder einschwenken.',
         action_de='Double Action: Jeder Abzug spannt den sichtbaren Hahn und dreht die Trommel eine Kammer weiter.',
         fire_de='Ein schwerer Schuss je Abzug; der kurze Lauf fluchtet unverändert mit der oberen Trommelkammer.',
         reload_en='Press the left cylinder latch, swing the cylinder out to the left, load six rounds and swing the cylinder closed.',
         action_en='Double action: each trigger pull cocks the exposed hammer and indexes the cylinder by one chamber.',
         fire_en='One heavy shot per trigger pull; the short barrel remains aligned with the upper cylinder chamber.'))
