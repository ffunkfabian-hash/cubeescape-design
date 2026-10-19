"""KD14 „Dämmerbruch“: heller kompakter Kipplauf mit Strebenbügel statt Schulterblock."""
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#A27CF5', '#EBDDFF'


def model():
    b = B(); D = b.D
    # Klappbarer Heckbügel: zwei getrennte Streben und eine schmale hintere Auflage.
    b.P([(236,252),(218,246),(140,278),(140,294),(222,268),(242,272)],DK,-18,18,r=9,L='Schaft')
    b.P([(234,292),(218,302),(144,326),(144,344),(226,318),(244,308)],DK,-18,18,r=9,L='Schaft')
    b.P(rect(130,276,22,72),K,-23,23,r=10,L='Schaftkappe')
    b.P(circ(232,275,17,20),K,-26,26,L='Schaftgelenk',
        dec=[D(circ(232,275,9,16),P)])
    b.P(rect(221,288,22,20),A,25,34,r=8,L='Schaftverriegelung')
    # Die Stufe über dem Verschluss und die tiefe Griffneigung bestimmen die Silhouette.
    b.P([(228,252),(260,240),(302,240),(316,252),(360,252),(386,270),(386,322),(362,336),(246,336),(226,316)],
        P,-31,31,r=12,L='Gehäuse')
    b.P(rect(252,230,54,18),P,-24,24,r=8,L='Verschlussdach')
    b.P([(240,312),(362,312),(384,302),(384,330),(362,344),(246,344)],DK,-26,26,r=10,L='Verschlusswanne')
    rail(b,258,300,231,K,DK,w=12)
    b.P([(350,254),(362,230),(378,230),(394,250),(380,264)],A,-9,9,r=6,L='Verriegelungshebel')
    # Ersatzgranate liegt auf einer durchgehenden, am Körper verschraubten Seitenkonsole.
    b.P(rect(250,278,84,36),K,30,39,r=10,L='Granathalter')
    b.C(258,312,295,12,A,n=12,cz=45,L='Ersatzgranate')
    b.F(312,331,295,12,6,AL,n=12,cz=45,L='Ersatzgranate')
    for x in (264,299):
        b.C(x,x+7,295,14,DK,n=12,cz=45,L='Granathalter')
    b.P(rect(282,278,12,9),P,38,47,r=4,L='Granathalterriegel')
    # Der Lauf trägt das exakte Kipplauf-Label; Endring und Handauflage bleiben wie G separat benannt.
    b.P(circ(394,314,18,20),K,-35,35,L='Scharnier',
        dec=[D(circ(394,314,10,16),P),D(circ(394,314,4,12),A,True)])
    b.P([(385,298),(418,298),(418,325),(394,332),(382,324)],DK,-28,28,r=9,L='Kipplauf')
    b.C(384,408,282,36,DK,n=16,L='Kipplauf')
    b.C(405,526,282,34,P,n=16,L='Kipplauf')
    b.P(rect(417,254,96,50),P,23,33,r=12,L='Kipplauf',
        dec=[D(roundpoly(rect(430,269,68,10),5),K),D(roundpoly(rect(439,287,50,8),4),A,True)])
    b.P(rect(417,254,96,50),P,-33,-23,r=12,L='Kipplauf')
    b.P(rect(422,308,82,19),DK,-23,23,r=8,L='Vordergriff')
    b.F(522,542,282,34,39,DK,n=16,L='Kipplauf')
    b.C(540,558,282,39,K,n=16,L='Mündung',
        cap=[(282,0,32,P,False),(282,0,26,'#050506',False),(282,0,9,K,False)])
    b.P([(246,338),(294,338),(284,366),(248,426),(216,438),(204,420)],K,-23,23,r=12,L='Griff')
    for z0,z1 in ((22,28),(-28,-22)):
        b.P([(248,356),(274,358),(242,414),(221,422)],DK,z0,z1,r=10,L='Griffschale')
    b.P([(209,419),(246,411),(256,427),(220,444),(206,435)],P,-26,26,r=9,L='Griffkappe')
    b.P(arcband(294,366,338,61,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(314,339),(327,339),(339,375),(326,380)],A,-6,6,r=5,L='Abzug')
    return b.m


META=dict(num='14',name='Spezial-Granatwerfer',nick='DÄMMERBRUCH',col=A,
 pill='VOID-VERSION',palette=[P,DK,A,AL],center=(344,334,0),
 desc='Der kompakte helle Kipplaufwerfer besitzt ein gestuftes Verschlussdach, einen stark zurückgeneigten Griff und einen offenen klappbaren Strebenbügel. Die Ersatzgranate sitzt links am Gehäuse in einer verbundenen Konsole; der dicke Lauf kippt am unteren Scharnier.',
 form='Offener klappbarer Strebenbügel · Schaftgelenk · gestuftes helles Gehäuse · stark geneigter Griff · Ersatzgranate in Seitenkonsole · Verriegelungshebel · unteres Scharnier · heller Kipplauf mit Handauflage · breiter Mündungsring',
 op=dict(reload_de='Verriegelungshebel nach rechts drücken, Lauf nach unten kippen, Hülse auswerfen, eine Granate einsetzen und Lauf schließen.',
         action_de='Ein Schuss je Ladung; Ersatzgranate links am Gehäuse. Zum Transport den entriegelten Strebenbügel seitlich einklappen.',
         fire_de='Granate im Bogen abfeuern; Aufprallzünder oder Fernzündung durch erneuten Abzug. Handauflage sitzt unter dem Kipplauf.',
         reload_en='Push the locking lever right, tip the barrel down, eject the case, insert one grenade and close the barrel.',
         action_en='One shot per load; spare grenade on the left receiver. Release and fold the rear strut brace sideways for transport.',
         fire_en='Lob one grenade; impact fuse or remote detonation with a second trigger pull. The hand rest is under the break-action barrel.'))
