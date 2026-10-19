"""KJ23 HYPOTHERM: magazinloser Facettenblaster mit gestaffeltem Kühlkamm."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222C30', '#B0EBF1', '#5F6A6E', '#10171C'
AX = 282


def spec():
    s = [
        K([(87,270),(105,259),(119,271),(119,365),(101,377),(87,363)],DK,-15,15,b=4,bz=4,label='Schaftkappe'),
        K([(112,267),(181,247),(250,259),(250,281),(181,269),(112,291)],
          BK,-13,13,b=4,bz=4,label='Schaft',glow=[((0,1),IC,3.2)]),
        K([(112,345),(185,321),(245,286),(257,305),(192,344),(112,368)],
          BK,-13,13,b=4,bz=4,label='Schaft',glow=[((3,4),IC,3.1)]),
        K([(241,253),(338,234),(423,242),(475,259),(483,289),(461,320),
           (243,320),(230,304),(230,273)],BK,-22,22,b=7,bz=8,label='Gehäuse',
          glow=[((0,1,4),IC,3.6)]),
        K(rect(264,219,133,37),DK,-9,9,b=2,bz=3,label='Visierschiene',
          dec=[(rect(275+14*i,226,5,4),GM,False) for i in range(8)]),
        K([(263,265),(337,254),(357,269),(350,287),(264,292)],
          GM,22,28,b=3,bz=2,label='Plasmakammer',glow=[((0,3),IC,3.2)],
          dec=[([(274,271),(334,263),(344,273),(338,280),(274,284)],IC,True)]),
        K(rect(262,299,99,12),DK,22,27,b=2,bz=2,label='Hitzeanzeige',
          dec=[(rect(269+11*i,303,7,4),IC if i<5 else GM,i<5) for i in range(8)]),
    ]
    # Beide getrennten Klappen sind benannt und öffnen um die obere Längskante.
    flap=[(376,259),(456,253),(470,270),(459,307),(376,311)]
    vents=[([(388+11*i,271),(394+11*i,270),(390+11*i,297),(384+11*i,298)],IC,True)
           for i in range(6)]
    for z0,z1 in ((22,30),(-30,-22)):
        s.append(K(flap,BK,z0,z1,b=3,bz=2,label='Entlüftungsklappe',
                   glow=[((0,3),IC,3.2)],dec=vents))
    s += [
        K([(270,320),(317,320),(303,407),(261,420),(253,405)],DK,-16,16,b=5,bz=5,label='Griff',
          dec=[([(278,339),(303,335),(291,390),(266,399)],GM,False)]),
        K([(335,319),(347,319),(359,350),(347,357)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(310,367),(384,360),(392,371),(310,378)],DK,-7,7,b=2,bz=2),
        K([(382,320),(392,320),(392,371),(382,371)],DK,-7,7,b=2,bz=2),
        K([(417,320),(453,320),(446,380),(425,393),(413,380)],
          DK,-13,13,b=4,bz=4,label='Vordergriff',glow=[((1,2),IC,3.0)]),
        X(476,661,AX,20,GM,n=8,label='Hitzespeicher'),
    ]
    # Der gezackte Kühlkamm steigt vorne an; keine zylindrischen Lamellen.
    for i in range(8):
        x=483+21*i
        top=252-3*i
        s.append(K([(x,top+8),(x+8,top),(x+14,top+8),(x+14,312),
                    (x+7,323),(x,315)],BK if i%2==0 else DK,-29,29,b=2,bz=5,
                   label='Kühlrippen',glow=[((0,1,3),IC,3.0)]))
    s += [
        X(655,713,AX,9,GM,n=6,label='Lauf'),
        T(707,724,AX,11,19,BK,n=8,label='Fokusring'),
        X(722,735,AX,19,DK,n=8,label='Fokusring',
          cap=[(AX,0,11,'#05090C',False),(AX,0,5,IC,True)]),
    ]
    return s


def model():
    return jlib.model(spec())


META = dict(
    num='23',name='Hitze-Blaster',nick='HYPOTHERM',col=IC,
    pill='NACHTSCHIEFER · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(411.0, 319.5, 0),
    desc='Ein offener Knickrahmenschaft mündet in ein niedriges, magazinloses Facettengehäuse. '
         'Vor ihm steigt ein gezackter Kühlkamm aus acht abgeschrägten Platten an. Zwei seitliche Entlüftungsklappen, '
         'ein Eisfenster der Plasmakammer und die segmentierte Hitzeanzeige erklären den Dynamic-Heat-Antrieb.',
    form='Offener Knickrahmenschaft · magazinloses Facettengehäuse · Plasmakammer · Hitzeanzeige · '
         'zwei seitliche Entlüftungsklappen · acht Kühlrippen auf dem Hitzespeicher · freier Sechskantlauf · Fokusring · Vordergriff',
    op=dict(
        reload_de='Kein Magazin: Nachladetaste öffnet beide seitlichen Entlüftungsklappen; die Munition kommt direkt aus der Reserve',
        action_de='Schüsse heizen den Hitzespeicher auf; bei voller Anzeige folgt eine lange Zwangsentlüftung',
        fire_de='Plasmabolzen in Salven; Entlüften im markierten Mittelfenster verkürzt die Feuerpause',
        reload_en='no magazine: reload opens both side vent flaps; ammunition is drawn straight from reserves',
        action_en='shots heat the sink; a full gauge forces a long vent cycle',
        fire_en='bursts of plasma bolts; venting in the marked middle window shortens the pause'))
