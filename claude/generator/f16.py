"""KF16 BRÜCKENLAST: Gurt-MG mit offenem Laufträger und geknicktem Daumenrahmen.

Der linke Munitionskasten sitzt vor dem vollständigen Abzugfenster. Zwei große Fenster
im Laufmantel und unter dem Tragegriff sind echte Öffnungen zwischen getrennten Stegen.
"""
from eng import rect
from tlib import B, grip, rail, trigger_group

OL, OR, DK, HE = '#777D32', '#E68FCE', '#293021', '#E9E6CC'


def model():
    b = B()
    D = b.D
    # Hohe Schulter, gebogener Rücksteg und niedriger Untergurt lassen ein großes Daumenfenster frei.
    b.P([(77,240),(118,234),(242,249),(255,282),(108,272),(88,261)],
        OR,-17,17,r=7,L='Schaft',dec=[D([(125,244),(213,253),(227,269),(128,260)], HE)])
    b.P([(78,246),(102,258),(118,372),(100,394),(81,374)],OL,-18,18,r=7,L='Schaft')
    b.P([(103,374),(252,379),(280,398),(258,416),(106,404),(93,392)],OL,-17,17,r=7,L='Schaft')
    b.P([(66,244),(80,240),(92,376),(81,396),(69,383)],DK,-20,20,r=5,L='Schaftkappe')
    b.P([(239,244),(306,231),(529,236),(568,256),(568,312),(524,329),(242,319)],
        OL,-26,26,r=8,L='Gehäuse',
        dec=[D([(263,255),(361,247),(395,265),(370,286),(266,281)],HE)])
    grip(b,260,318,DK,OL,h=96,w=56,lean=20,z=18)
    trigger_group(b,330,319,OR,DK,grip_x0=304,depth=39)
    # Deckel und tief eingelassene Schiene: das hintere Scharnier bleibt ablesbar.
    b.P([(298,220),(474,217),(494,234),(483,244),(298,241)],OR,-23,23,r=5,L='Zuführdeckel')
    b.C(288,302,232,7,DK,n=8)
    rail(b,316,465,219,DK,OL,w=10)
    b.P([(499,276),(525,270),(532,281),(506,289)],OR,26,39,r=3,L='Ladehebel')
    # Kasten beginnt 28 Einheiten vor dem Bügel und hängt ausschließlich links.
    b.P([(422,306),(513,306),(532,326),(523,391),(435,398),(420,375)],
        OR,26,73,r=6,L='Munitionskasten',
        dec=[D([(438,328),(510,326),(508,365),(443,374)],HE)])
    b.P([(442,260),(498,260),(504,311),(437,311)],HE,26,41,r=3,L='Patronengurt',
        dec=[D(rect(446+11*i,265,6,39),DK) for i in range(5)])
    # Ober- und Untergurt des Mantels; das dunkle Laufrohr bleibt durch das große Fenster sichtbar.
    b.P([(561,254),(809,254),(828,270),(814,278),(568,274)],OL,-18,18,r=6,L='Laufmantel')
    b.P([(568,324),(812,326),(827,338),(811,350),(574,344)],OL,-18,18,r=6,L='Laufmantel',
        dec=[D([(597,331),(766,333),(786,342),(600,338)],OR)])
    b.P([(562,259),(583,263),(586,336),(567,340)],OL,-18,18,r=4,L='Laufmantel')
    b.P([(806,260),(827,270),(827,338),(808,344)],OL,-18,18,r=4,L='Laufmantel')
    b.C(568,868,296,9,DK,n=12,L='Lauf')
    b.C(868,908,296,15,OR,n=8,L='Feuerdämpfer',cap=[(296,0,7,DK,False)])
    # Offener Tragebogen: zwei Füße und eine lange Handauflage, kein massiver Block.
    b.P([(619,218),(639,218),(649,259),(629,259)],DK,-9,9,r=4)
    b.P([(732,218),(752,223),(744,258),(726,258)],DK,-9,9,r=4)
    b.P([(613,205),(728,205),(755,219),(742,233),(619,228)],HE,-11,11,r=6,L='Tragegriff')
    b.P([(614,340),(652,341),(649,390),(629,412),(608,401)],
        OR,-14,14,r=7,L='Vordergriff',dec=[D([(623,356),(640,357),(637,383),(626,393)],DK)])
    # Beide eingeklappten Beine tragen dasselbe Bewegungs-/Bauteillabel.
    b.P(rect(718,341,22,17),DK,-24,24,r=3)
    for z in (-20,20):
        b.C(731,816,354,5,DK,n=8,cz=z,L='Zweibein')
    return b.m


META = dict(
    num='16', name='Maschinengewehr', nick='BRÜCKENLAST', col=OL,
    pill='OLIV · ORCHIDEE · KREIDE', palette=[OL,OR,DK,HE], center=(487,308,0),
    desc='Der olivfarbene Rahmenschaft geht in ein tiefes Gehäuse über, während der lange Lauf in einem offenen Brückenträger liegt. '
         'Orchideenfarbener Zuführdeckel und linker Munitionskasten rahmen den hellen Patronengurt; vor dem freien Abzugbereich bleibt Abstand. '
         'Ein hoher Tragebogen, der geneigte Vordergriff und zwei eingeklappte Zweibeine bestimmen die Front.',
    form='Offener Daumenrahmenschaft · Griff mit freiem Abzugbügel · Zuführdeckel mit Visierschiene · '
         'Ladehebel links · Munitionskasten links mit Patronengurt · offener Laufmantel · Tragebogen · Vordergriff · Zweibein · Feuerdämpfer',
    op=dict(
        reload_de='Zuführdeckel am hinteren Scharnier öffnen, links neuen Kasten einhängen, Gurt einlegen, Deckel schließen und Ladehebel ziehen.',
        action_de='Die Gurtzuführung zieht bei jedem Schuss eine Patrone weiter; der Zuführdeckel hält den Gurt über dem Verschluss.',
        fire_de='Dauerfeuer mit steigender Feuerrate beim Halten; der Tragegriff dient dem Laufwechsel, das Zweibein stützt die Waffe.',
        reload_en='Open the feed cover on its rear hinge, hang a new box on the left, lay in the belt, close the cover and pull the charging handle.',
        action_en='The belt feed advances one cartridge per shot; the feed cover holds the belt above the bolt.',
        fire_en='Sustained full-auto fire, with rate increasing while held; use the carry handle for barrel swaps and the bipod for support.'))
