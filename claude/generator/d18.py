"""KD18 „Nachtwache“: kräftige D-Stange mit kurzem, breitem Schildklingenkopf."""
from tlib import B
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#8177D9', '#DDD8FF'


def model():
    b = B(); D = b.D
    b.C(62,108,300,22,DK,n=12,L='Knauf',cap=[(300,0,9,A,True)])
    b.C(102,636,300,14,DK,n=12,L='Stange')
    b.P(rect(112,280,124,40),K,-20,20,r=12,L='Griff',
        dec=[D(roundpoly(rect(126+22*i,285,10,30),5),DK) for i in range(5)])
    b.P([(230,268),(316,268),(340,284),(340,322),(230,322)],DK,-25,25,r=12,L='Gehäuse',
        dec=[D(roundpoly(rect(244,278,64,18),7),P),D(roundpoly(rect(250,303,68,8),4),A,True)])
    b.P(arcband(232,334,320,54,9),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(254,320),(268,320),(278,348),(264,352)],A,-6,6,r=4,L='Abzug')
    b.P(rect(390,278,104,44),K,-22,22,r=12,L='Vordergriff',
        dec=[D(roundpoly(rect(404+21*i,283,10,34),5),DK) for i in range(4)])
    b.P([(512,270),(600,270),(622,286),(622,316),(600,330),(512,330)],
        DK,-26,26,r=12,L='Energiezelle',
        dec=[D(roundpoly(rect(524,278,72,14),6),P)]+
            [D(roundpoly(rect(528+20*i,300,12,20),5),A,True) for i in range(4)])
    b.P([(606,250),(650,250),(668,270),(668,332),(650,352),(606,352)],
        K,-28,28,r=12,L='Klingenfassung',
        dec=[D(roundpoly(rect(618,262,30,18),7),P),D(roundpoly(rect(618,322,30,18),7),P)])
    # Beide Scharnierschilde bleiben einzeln beschriftet und an der Fassung verwurzelt.
    for s in (-1,1):
        b.Y([(614,22*s),(658,22*s),(670,72*s),(650,88*s),(618,76*s)],
            DK,264,336,r=10,L='Schildflügel',
            dec=[D(roundpoly([(624,38*s),(650,38*s),(658,68*s),(642,76*s),(626,68*s)],7),P),
                 D(roundpoly([(631,44*s),(639,44*s),(646,66*s),(638,68*s)],4),A,True)])
    b.P([(654,258),(726,232),(802,246),(868,300),(808,340),(712,364),(654,340)],
        DK,-9,9,r=12,L='Klinge',
        dec=[D(roundpoly([(674,266),(728,246),(792,260),(832,286),(674,286)],8),P),
             D(roundpoly([(678,320),(714,346),(800,326),(848,300),(860,300),
                          (808,336),(714,358),(678,336)],6),A,True),
             D(roundpoly([(702,336),(716,347),(794,330),(798,334),(716,353),(702,343)],3),AL,True)])
    b.C(658,868,300,12,K,n=12,L='Emitter',cap=[(300,0,8,A,True),(300,0,4,AL,True)])
    b.F(868,882,300,12,6,A,n=12,emit=True)
    return b.m


META=dict(num='18',name='Glefe',nick='NACHTWACHE',col=A,
 pill='DUSK-SKIN',palette=[P,DK,A,AL],center=(472,302,0),
 desc='Eine kräftige zweihändige Stange trägt einen kurzen, breiten Klingenkopf mit violetter Leuchtschneide und mittigem Geschossemitter. Zwei gerundete Schildflügel sitzen seitlich an der dunklen Klingenfassung; die große Energiezelle davor und der freie gebogene Abzugsbügel machen die Bedienung lesbar.',
 form='Kräftige Stange · großer Knauf · hinterer Griff · gerundetes Abzugsgehäuse · freier Bügel · Vordergriff · breite Energiezelle · massive Klingenfassung · zwei Schildflügel · kurze breite Klinge · mittiger Emitter',
 op=dict(reload_de='Die Energiezelle vor der Klingenfassung lädt durch Nahkampftreffer; zum Nachladen drehen und neu einrasten (4 Schuss).',
         action_de='Abzug feuert ein Energiegeschoss aus dem Emitter; beim Blocken klappen beide Schildflügel nach außen und bauen den Schild auf.',
         fire_de='Klingenhiebe und Fernschüsse aus der Hüfte; der vor dem Klingenkopf aufgebaute Schild hält Treffer ab.',
         reload_en='Melee hits recharge the cell behind the blade mount; twist and relock the cell to reload (4 shots).',
         action_en='The trigger fires an energy bolt from the emitter; guarding unfolds both shield wings to form the shield.',
         fire_en='Blade swings and hip-fired energy bolts; the shield projected ahead of the blade head absorbs hits.'))
