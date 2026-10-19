"""KD16 „Stahlhagel“: heller Bullpup-Gurtkasten, hoher Heckverschluss, kurzer Vorderkörper."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#F1CA57', '#FFF2BB'


def model():
    b = B(); D = b.D
    # Der Schulteranschlag ist die Rückwand des hohen Verschlusskastens, kein separater Schaft.
    b.P([(82,208),(214,208),(214,350),(114,350),(82,328)],
        P,-36,36,r=12,L='Schaft')
    b.P([(202,208),(330,208),(368,228),(464,242),(498,266),(498,342),
         (352,350),(202,350)],P,-36,36,r=12,L='Gehäuse')
    b.P(rect(70,214,24,130),K,-34,34,r=10,L='Schaftkappe')
    b.P([(106,198),(240,198),(266,210),(260,228),(106,228)],DK,-27,27,r=10,L='Wangenauflage')
    b.P([(166,194),(330,194),(352,210),(342,232),(166,232)],K,-29,29,r=10,L='Zuführdeckel')
    b.C(158,180,212,12,DK,n=12,L='Deckelscharnier')
    rail(b,198,324,194,K,DK,w=14)
    # Dicke, aufgesetzte Wartungswangen und eine getrennte Ladeführung.
    for z0,z1 in ((35,43),(-43,-35)):
        b.P([(106,246),(192,238),(212,254),(212,314),(106,320)],DK,z0,z1,r=10,L='Wartungsplatte')
        ds=[D(roundpoly(rect(344,262,70,9),4),A,True)]
        b.P([(326,250),(430,256),(452,272),(444,302),(326,302)],DK,z0,z1,r=10,L='Verschlusswange',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    b.P(rect(352,312,100,18),K,35,44,r=8,L='Ladeführung')
    b.P(rect(394,314,34,14),A,43,58,r=6,L='Ladehebel')
    # Der Kasten liegt hinter dem Griff. Die Gurtmechanik bleibt unverändert.
    b.P([(176,326),(296,326),(310,344),(302,426),(186,426),(176,408)],
        DK,35,98,r=12,L='Munitionskasten',
        dec=[D(roundpoly(rect(194,350,90,34),10),K),D(roundpoly(rect(204,362,70,9),4),A)])
    b.P(rect(180,330,126,20),P,38,102,r=8,L='Kastendeckel')
    b.P(rect(184,410,120,22),K,38,101,r=8,L='Kastenfuß')
    b.P([(232,250),(286,250),(298,334),(232,338)],A,36,51,r=8,L='Patronengurt',
        dec=[D(roundpoly(rect(240+11*i,260,5,64),2),K) for i in range(4)])
    b.P([(478,254),(634,254),(664,274),(664,314),(642,338),(478,338)],
        P,-29,29,r=12,L='Laufmantel')
    for z0,z1 in ((28,36),(-36,-28)):
        ds=[D(roundpoly(rect(516+25*i,284,12,22),5),DK) for i in range(4)]
        b.P(rect(506,274,122,43),K,z0,z1,r=10,L='Kühlplatte',
            dec=ds if z1>0 else (),xdec=[('z-',z0,*d) for d in ds] if z1<0 else ())
    for x in (500,626):
        b.P(rect(x,250,16,92),DK,-32,32,r=8,L='Laufklemme')
    b.P(rect(526,224,14,34),K,-10,10,r=6,L='Griffstütze')
    b.P(rect(610,224,14,34),K,-10,10,r=6,L='Griffstütze')
    b.P(rect(516,210,118,22),P,-15,15,r=10,L='Tragegriff')
    b.C(658,716,296,13,K,n=12,L='Lauf')
    b.C(708,754,296,23,DK,n=12,L='Feuerdämpfer',
        cap=[(296,0,15,K,False),(296,0,7,AL,True)])
    b.P(rect(604,332,24,24),K,-22,22,r=8,L='Zweibeinlager')
    for z in (-17,17):
        b.C(616,698,352,7,DK,n=12,cz=z,L='Zweibein')
    b.P([(360,346),(418,346),(436,440),(374,448)],K,-24,24,r=12,L='Griff')
    for z0,z1 in ((23,29),(-29,-23)):
        b.P([(374,366),(404,366),(418,422),(391,428)],DK,z0,z1,r=8,L='Griffschale')
    b.P(arcband(418,526,336,64,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(440,346),(454,346),(464,380),(450,384)],A,-6,6,r=4,L='Abzug')
    b.P([(552,336),(590,336),(588,400),(558,400)],K,-20,20,r=10,L='Vordergriff')
    return b.m


META=dict(num='16',name='Maschinengewehr',nick='STAHLHAGEL',col=A,
 pill='ELITE-SKIN',palette=[P,DK,A,AL],center=(408,320,0),
 desc='Der helle Bullpup-Kasten bildet zugleich Verschlussgehäuse und Schulteranschlag. Hinter dem Griff hängt links der tiefe Gurtkasten; sein goldener Gurt steigt zum hohen Zuführdeckel. Ein kurzer, geklammerter Laufmantel mit Tragegriff und eingeklapptem Zweibein bildet den deutlich niedrigeren Vorderkörper.',
 form='Hoher heller Bullpup-Verschlusskasten · integrierter Heckanschlag · hintere Gurtzuführung · Kasten hinter dem Griff · dicke Wartungswangen · kurzer geklammerter Laufmantel · Tragegriff · Feuerdämpfer · Zweibein · freier Abzugsraum',
 op=dict(reload_de='Hinteren Zuführdeckel aufklappen, Kasten links hinter dem Griff einhängen, Gurt einlegen, Deckel schließen und Ladehebel links ziehen.',
         action_de='Der Verschluss zieht je Schuss eine Patrone aus dem hinteren Gurtkasten; die gelbe Leiste zeigt Bereitschaft.',
         fire_de='Dauerfeuer mit steigender Feuerrate beim Halten; der Tragegriff dient zum Wechsel des schweren Laufs.',
         reload_en='Open the rear feed cover, hang the box left behind the grip, lay in the belt, close the cover and pull the left charging handle.',
         action_en='The bolt feeds one round per shot from the rear belt box; the yellow strip indicates readiness.',
         fire_en='Sustained automatic fire builds rate while held; the carry handle serves for heavy barrel changes.'))
