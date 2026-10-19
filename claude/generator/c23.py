"""KC23 „Fächerglut“: ein geschwungener Blaster mit aufgefächertem Kühlrücken."""
from eng import rect, roundpoly
from tlib import B, grip, rail, trigger_group
import ext

AS, PB, ZI, DK = '#8C919C', '#267C8A', '#F1EF8F', '#272931'
AX = 280


def model():
    b = B()
    D = b.D
    # Zwei gebogene Holme um ein echtes Schaftfenster, kein aufgemaltes Loch.
    b.P([(88,247),(143,236),(209,236),(278,250),(279,275),
         (211,257),(149,253),(98,268)], PB, -16, 16, r=9, L='Schaft')
    b.P([(89,316),(147,319),(209,294),(270,276),(279,297),
         (215,315),(151,345),(89,341)], AS, -15, 15, r=9, L='Schaft',
        dec=[D(roundpoly([(104,324),(149,327),(218,301),(249,294),
                          (218,310),(151,337),(104,334)],4), PB)])
    b.P([(78,247),(98,247),(103,340),(84,351),(73,344)], DK,
        -18, 18, r=8, L='Schaftkappe')
    b.P([(126,231),(200,231),(225,240),(209,250),(128,246)], AS,
        -13, 13, r=7, L='Wangenauflage')
    b.P([(268,245),(315,236),(454,238),(486,251),(512,272),
         (512,304),(481,326),(443,334),(269,334)], AS, -24, 24, r=9,
        L='Gehäuse', dec=[D(roundpoly([(272,314),(443,314),(489,300),
                                      (486,320),(446,332),(272,332)],5),PB)])
    rail(b, 290, 423, 240, PB, DK, w=11)
    b.P([(287,260),(367,258),(380,269),(370,291),(287,294)], PB,
        24, 29, r=7, L='Plasmakammer',
        dec=[D(roundpoly([(296,267),(362,265),(369,272),(361,284),(296,286)],5),ZI,True)])
    b.P(rect(289,299,92,10), DK, 24, 28, r=4, L='Hitzeanzeige',
        dec=[D(roundpoly(rect(294+14*i,302,9,4),1),PB if i<2 else ZI,True)
             for i in range(6)])
    # Beide Klappen sitzen bündig auf der Seitenhaut und bleiben einzeln benannt.
    flap = [(395,252),(448,251),(483,268),(483,306),(449,319),(395,315)]
    slots = [roundpoly([(403+13*i,264),(409+13*i,264),
                        (416+13*i,303),(410+13*i,303)],2) for i in range(5)]
    for side in (-1, 1):
        z0,z1 = (24,30) if side==1 else (-30,-24)
        b.P(flap, PB, z0, z1, r=7, L='Entlüftungsklappe',
            xdec=[('z+' if side==1 else 'z-',30*side,p,ZI,True) for p in slots])
    b.C(499,690,AX,21,DK,n=16,L='Hitzespeicher')
    # Die veränderlichen Radien bilden einen einzigen fächerartigen Außenbogen.
    for i,R in enumerate((29,35,42,48,51,48,41,33)):
        x=514+21*i
        b.C(x,x+10,AX,R,AS if i%2==0 else PB,n=18,L='Kühlrippen')
    b.C(683,739,AX,10,DK,n=12,L='Lauf')
    b.F(731,751,AX,15,20,PB,n=16,L='Fokusring')
    b.C(751,764,AX,20,PB,n=16,L='Fokusring',
        cap=[(AX,0,12,DK,False),(AX,0,5,ZI,True)])
    grip(b,292,334,PB,DK,h=92,w=51,lean=18)
    trigger_group(b,356,334,ZI,PB,grip_x0=331,depth=35)
    b.P([(444,330),(478,324),(485,343),(470,395),(447,389)], PB,
        -14,14,r=9,L='Vordergriff')
    # Das Leuchtband folgt dem oberen Schaftholm statt einer geraden G-Leiste.
    for z in (-16.5,16.5):
        first=len(b.m.parts)
        ext.tube(b.m,[(108,249,z),(150,244,z),(205,245,z),(263,259,z)],
                 1.7,ZI,k=8,emit=True)
        for part in b.m.parts[first:]:part['label']='Leuchtband'
    return b.m


META = dict(
    num='23',name='Hitze-Blaster',nick='FÄCHERGLUT',col=ZI,
    pill='ASCHGRAU · PFAUENBLAU · ZITRONE',palette=[AS,PB,ZI,DK],center=(419,328,0),
    desc='Ein aufgefächerter Kühlrücken wächst aus dem aschgrauen Gehäuse und läuft zum freien Lauf wieder schmal zu. '
         'Geschwungene Schaftholme greifen die Fächerkontur auf; pfauenblaue Entlüftungsklappen und zitronenhelle Fenster zeigen den Wärmekreislauf.',
    form='Gebogener Fensterschaft · Plasmakammer links · Hitzeanzeige · zwei Entlüftungsklappen · '
         'fächerförmiges Kühlrippenpaket um den Hitzespeicher · freier Lauf mit Fokusring · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Nachladetaste öffnet beide Entlüftungsklappen zum Abkühlen; kein Magazin, Munition direkt aus der Reserve',
        action_de='Salven erhitzen den Hitzespeicher; das Fächerpaket kühlt zwischen den Salven, volle Anzeige erzwingt langes Entlüften',
        fire_de='Plasmabolzen in Salven; im Mittelfenster der Hitzeanzeige entlüften, um die Pause zu verkürzen',
        reload_en='reload opens both vent flaps to dump heat; no magazine, ammunition comes straight from reserves',
        action_en='bursts heat the sink; the fan fins cool between bursts, a full gauge forces a long vent',
        fire_en='bursts of plasma bolts; vent in the middle gauge window to shorten the pause'))
