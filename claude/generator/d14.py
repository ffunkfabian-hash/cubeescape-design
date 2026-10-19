"""KD14 „Dämmerbruch“: gedrungener Kipplaufwerfer mit breiter Schulterauflage."""
from tlib import B, rail
from eng import rect, circ, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#A27CF5', '#EBDDFF'


def model():
    b = B(); D = b.D
    b.P([(100,246),(188,246),(232,264),(232,328),(180,336),(110,354),(100,344)],
        DK,-25,25,r=12,L='Schaft',
        dec=[D(roundpoly(rect(118,258,70,22),9),P)])
    b.P(rect(84,242,22,118),K,-28,28,r=9,L='Schaftkappe')
    # Der linke Halter umfasst die Reservegranate und ist im Schaft verankert.
    b.P(rect(126,286,76,30),K,24,34,r=9,L='Granathalter')
    b.C(132,182,301,12,A,n=12,cz=42,L='Ersatzgranate')
    b.F(182,202,301,12,6,AL,n=12,cz=42,L='Ersatzgranate')
    b.P([(220,250),(362,244),(392,260),(392,330),(238,338),(220,320)],
        DK,-30,30,r=12,L='Gehäuse',
        dec=[D(roundpoly([(240,262),(350,256),(366,268),(366,292),(240,298)],10),P),
             D(roundpoly(rect(254,274,90,10),5),A,True),
             D(roundpoly(rect(256,312,96,8),4),K)])
    rail(b,246,354,250,K,DK,w=13)
    b.P([(358,250),(368,228),(382,228),(398,248),(388,260)],A,-8,8,r=5,L='Verriegelungshebel')
    # Das Scharnier unterhalb der Laufachse verbindet Gehäuse und Kipplauf.
    b.P(circ(394,314,17,20),K,-34,34,L='Scharnier',
        dec=[D(circ(394,314,9,16),P),D(circ(394,314,4,12),A,True)])
    b.C(388,548,282,36,DK,n=16,L='Kipplauf')
    b.P(rect(414,252,116,60),DK,-31,31,r=12,L='Kipplauf',
        dec=[D(roundpoly(rect(426,260,92,25),10),P),
             D(roundpoly(rect(430,292,84,8),4),A,True),
             D(roundpoly(rect(442,268,58,7),3),K)])
    b.C(548,572,282,40,K,n=16,L='Mündung',
        cap=[(282,0,33,P,False),(282,0,27,'#050506',False),(282,0,10,K,False)])
    b.P([(246,334),(298,334),(318,428),(260,436)],K,-22,22,r=12,L='Griff',
        dec=[D(roundpoly([(266,352),(282,352),(298,410),(282,414)],6),DK)])
    b.P(arcband(298,392,334,64,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(320,335),(333,335),(345,376),(332,380)],A,-6,6,r=4,L='Abzug')
    b.P([(454,312),(494,312),(488,384),(460,384)],K,-18,18,r=11,L='Vordergriff',
        dec=[D(roundpoly(rect(465,330,16,36),7),P)])
    return b.m


META=dict(num='14',name='Spezial-Granatwerfer',nick='DÄMMERBRUCH',col=A,
 pill='VOID-VERSION',palette=[P,DK,A,AL],center=(330,334,0),
 desc='Ein kurzer, dickwandiger Kipplauf sitzt vor dem schweren gerundeten Verschlussblock mit heller Deckplatte. Die breite Schulterauflage trägt links eine Ersatzgranate; der violette Verriegelungshebel löst den Lauf am deutlich sichtbaren unteren Scharnier.',
 form='Breite Schulterauflage · Ersatzgranate im Halter links · gerundeter Verschlussblock · Verriegelungshebel oben · unteres Scharnier · kurzer dicker Kipplauf · großer Mündungsring · Vordergriff · gebogener Bügel',
 op=dict(reload_de='Verriegelungshebel nach rechts drücken, Kipplauf nach unten kippen, leere Hülse auswerfen, eine Granate einschieben und Lauf schließen.',
         action_de='Ein Schuss je Ladung; die Ersatzgranate im Halter links am Schaft liegt für den nächsten Ladevorgang bereit.',
         fire_de='Granate im Bogen abfeuern; Aufprallzünder oder Fernzündung durch erneuten Abzug.',
         reload_en='Push the locking lever right, tip the barrel down, eject the empty case, insert one grenade and close the barrel.',
         action_en='One shot per load; the spare grenade in the left stock holder is ready for the next reload.',
         fire_en='Lob one grenade; impact fuse or remote detonation with a second trigger pull.'))
