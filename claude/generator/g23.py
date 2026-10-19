"""KG23 Hitze-Blaster „Hitzestau“ (claude-0.10.1): magazinloses Blaster-Impulsgewehr (Destiny: Rahmen „Dynamic Heat“, Renegades 2025).
Unterschied zum Impulsgewehr (KX03) und Raketen-Impulsgewehr (KG21): kein Magazin und keine Energiezelle; jeder Schuss heizt den
Hitzespeicher auf, ein Rippenpaket um den Lauf kühlt, zwei seitliche Entlüftungsklappen ersetzen das Nachladen, die Hitzeanzeige zeigt
den Stand."""
from tlib import B,grip,rail,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
AX=292   # Laufachse (y)
def model():
    b=B();D=b.D
    # kurzer Rahmenschaft mit Durchbruch (Lochschaft wie ein Blaster-Karabiner)
    b.P([(110,262),(140,256),(232,266),(232,306),(196,318),(118,342)],AN,-13,13,r=6,L='Schaft',
        dec=[D(roundpoly([(146,278),(204,280),(204,296),(150,312)],4),DK)])
    b.P(rect(100,252,14,98),DK,-15,15,r=4,L='Schaftkappe')
    # Gehäuse ohne Magazinschacht: glatte Unterseite, Plasmakammer mit Fenster oben links
    b.P([(228,254),(452,250),(476,262),(476,330),(452,338),(228,338)],CR,-22,22,r=8,L='Gehäuse',
        dec=[D(roundpoly([(232,316),(472,316),(472,326),(452,336),(232,336)],3),AN)])
    rail(b,246,440,250,AN,DK,w=10)
    b.P(rect(262,266,92,30),AN,22,26,r=4,L='Plasmakammer',dec=[D(roundpoly(rect(270,272,76,18),4),OR,True)])
    # Hitzeanzeige: Segmente von Cyan (kalt) nach Orange (heiß), links unter der Plasmakammer
    b.P(rect(262,302,120,10),DK,22,25,r=2,L='Hitzeanzeige',
        dec=[D(rect(266+14*i,304,10,6),CY if i<4 else OR,True) for i in range(8)])
    # zwei Entlüftungsklappen (links und rechts), am oberen Rand angeschlagen; Lamellen mit Glut dahinter
    lam=[roundpoly(rect(398+12*i,270,6,42),2) for i in range(6)]
    b.P([(390,262),(470,264),(470,318),(390,318)],AN,22,28,r=3,L='Entlüftungsklappe',dec=[D(p,OR,True) for p in lam])
    b.P([(390,262),(470,264),(470,318),(390,318)],AN,-28,-22,r=3,L='Entlüftungsklappe',xdec=[('z-',-28,p,OR,True) for p in lam])
    # Hitzespeicher um den Lauf: Kern und Rippenpaket (Kühlrippen), davor freier Lauf und Fokusring
    b.C(476,640,AX,22,AN,n=12,L='Hitzespeicher')
    for k in range(9):b.C(482+17*k,490+17*k,AX,36,CR if k%2==0 else DK,n=12,L='Kühlrippen' if k==0 else None)
    b.C(640,700,AX,10,DK,n=8,L='Lauf')
    b.C(700,722,AX,19,AN,n=12,L='Fokusring',cap=[(AX,0,11,'#050506',False),(AX,0,5,OR,True)])
    # Griff, Abzug; Vordergriff dort, wo sonst der Magazinschacht sitzt (nicht am heißen Hitzespeicher)
    grip(b,272,338,AN,DK,h=90,w=48,lean=16)
    trigger_group(b,332,338,OR,AN,grip_x0=312,depth=34)
    b.P([(420,336),(456,336),(450,398),(426,398)],AN,-13,13,r=6,L='Vordergriff')
    return b.m
META=dict(num='23',name='Hitze-Blaster',nick='HITZESTAU',col='#F07A1A',pill='CREME · ANTHRAZIT · ORANGE',
 palette=[CR,AN,OR,CY],center=(411,300,0),
 desc='Magazinloser Blaster mit Dynamic-Heat-Rahmen: Statt eines Magazins sitzt um den Lauf ein Hitzespeicher mit Rippenpaket aus cremefarbenen und dunklen Kühlrippen. Die Plasmakammer glüht im Seitenfenster, darunter steigt die Hitzeanzeige von Cyan nach Orange, und vorne am Gehäuse öffnen zwei Entlüftungsklappen mit glühenden Lamellen.',
 form='Lochschaft · Gehäuse ohne Magazinschacht · Plasmakammer mit Fenster · Hitzeanzeige · zwei seitliche Entlüftungsklappen · Hitzespeicher mit Rippenpaket · freier Lauf · Fokusring · Vordergriff',
 op=dict(reload_de='kein Nachladen: Nachladetaste öffnet beide Entlüftungsklappen und bläst die Hitze ab; Munition kommt direkt aus der Reserve',
         action_de='jeder Schuss heizt den Hitzespeicher auf, die Rippen kühlen zwischen den Salven; bei 100 % erzwungenes langes Entlüften',
         fire_de='Salven aus Plasmabolzen; rechtzeitiges Entlüften im Mittelfenster der Anzeige verkürzt die Pause',
         reload_en='no reload: the reload input opens both vent flaps and dumps heat; ammo is drawn straight from reserves',
         action_en='every shot heats the heat sink, the fins cool between bursts; at 100 % a forced long vent',
         fire_en='bursts of plasma bolts; venting in the gauge sweet spot shortens the pause'))
