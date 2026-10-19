"""KD16 „Stahlhagel“: kurzer, tiefer Gurtkasten mit schwerem D-Laufmantel."""
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#F1CA57', '#FFF2BB'


def model():
    b = B(); D = b.D
    b.P([(70,242),(168,242),(228,266),(228,330),(166,330),(104,354),(70,354)],
        DK,-25,25,r=12,L='Schaft',
        dec=[D(roundpoly(rect(88,254,92,24),9),P),D(roundpoly(rect(92,294,66,12),5),K)])
    b.P(rect(58,236,20,128),K,-28,28,r=8,L='Schaftkappe')
    b.P([(214,232),(492,228),(554,252),(554,346),(234,346),(214,326)],
        DK,-34,34,r=12,L='Gehäuse',
        dec=[D(roundpoly([(234,248),(420,244),(458,256),(458,288),(234,296)],10),P),
             D(roundpoly(rect(252,260,146,10),5),A,True),
             D(roundpoly(rect(242,320,196,12),5),K)])
    b.P([(294,220),(514,220),(530,234),(294,240)],K,-28,28,r=8,L='Zuführdeckel',
        dec=[D(roundpoly(rect(316,224,170,8),4),P)])
    b.C(286,304,232,9,DK,n=12)
    rail(b,314,478,220,K,DK,w=14)
    b.P(rect(438,282,32,12),A,34,48,r=5,L='Ladehebel')
    # Der seitliche Kasten sitzt vor dem Abzug; der Gurt steigt zum Deckel auf.
    b.P([(476,314),(568,314),(582,330),(582,412),(476,412)],K,34,88,r=12,L='Munitionskasten',
        dec=[D(roundpoly(rect(490,330,74,22),8),P),D(roundpoly(rect(490,370,74,12),5),A)])
    b.P([(492,254),(544,254),(556,318),(492,324)],A,34,50,r=8,L='Patronengurt',
        dec=[D(roundpoly(rect(498+10*i,268,5,40),2),K) for i in range(4)])
    b.P([(546,252),(710,252),(740,270),(740,326),(712,346),(546,346)],
        DK,-28,28,r=12,L='Laufmantel',
        dec=[D(roundpoly(rect(566,264,138,22),8),P)])
    # Separate Lüftungsfenster als Decals auf dem durchgehenden Mantel.
    for i in range(5):
        b.m.decal('z+',28,roundpoly(rect(572+28*i,300,16,28),6),K)
    b.P(rect(592,222,16,40),K,-10,10,r=7)
    b.P(rect(674,222,16,40),K,-10,10,r=7)
    b.P(rect(584,208,114,22),DK,-13,13,r=10,L='Tragegriff',
        dec=[D(roundpoly(rect(602,214,78,8),4),P)])
    b.C(734,784,298,12,K,n=12,L='Lauf')
    b.C(780,830,298,21,DK,n=12,L='Feuerdämpfer',
        cap=[(298,0,13,K,False),(298,0,6,AL,True)])
    b.P(rect(650,330,24,26),K,-22,22,r=8)
    for z in (-16,16):
        b.C(654,738,352,6,DK,n=10,cz=z,L='Zweibein')
    b.P([(270,342),(326,342),(344,438),(284,442)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(288,362),(310,362),(324,416),(302,418)],7),DK)])
    b.P(arcband(326,438,344,66,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(350,344),(364,344),(374,378),(360,382)],A,-6,6,r=4,L='Abzug')
    b.P([(600,342),(640,342),(636,410),(606,410)],K,-18,18,r=10,L='Vordergriff')
    return b.m


META=dict(num='16',name='Maschinengewehr',nick='STAHLHAGEL',col=A,
 pill='ELITE-SKIN',palette=[P,DK,A,AL],center=(444,326,0),
 desc='Ein kurzer, tiefer Gurtkasten verbindet den schweren Schulterblock mit einem gerundeten Laufmantel. Der goldene Patronengurt steigt links aus dem vorgezogenen Munitionskasten zum Zuführdeckel; Tragegriff und eingeklapptes Zweibein bleiben klar vom freien Abzugsraum getrennt.',
 form='Tiefer Schulterblock · dunkles Rundgehäuse mit heller Deckplatte · Zuführdeckel mit Schiene · Munitionskasten links vorn · sichtbarer Patronengurt · kurzer Laufmantel · Tragegriff · Feuerdämpfer · eingeklapptes Zweibein · freier Abzugsbügel',
 op=dict(reload_de='Zuführdeckel am hinteren Scharnier öffnen, Kasten links einhängen, Gurt einlegen, Deckel schließen und linken Ladehebel ziehen.',
         action_de='Der Verschluss zieht den Gurt bei jedem Schuss eine Patrone weiter; die gelbe Leuchtleiste zeigt die Bereitschaft.',
         fire_de='Dauerfeuer mit steigender Feuerrate beim Halten; der Tragegriff dient zum Wechsel des schweren Laufs.',
         reload_en='Open the feed cover on its rear hinge, fit the left ammo box, lay in the belt, close the cover and pull the left charging handle.',
         action_en='The bolt advances the belt one round with each shot; the yellow light strip indicates readiness.',
         fire_en='Sustained automatic fire builds rate while held; the carry handle serves for heavy barrel changes.'))
