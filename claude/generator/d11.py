"""KD11 „Weitblick“: kurzer D-Schulterblock und breiter Präzisionsverschluss."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#4D9CFF', '#CFEBFF'


def model():
    b = B(); D = b.D
    b.P([(78,242),(182,242),(224,262),(224,326),(174,334),(110,354),(78,354)],
        DK,-25,25,r=12,L='Schaft',
        dec=[D(roundpoly(rect(96,258,82,26),10),P),
             D(roundpoly(rect(106,312,60,10),5),K)])
    b.P(rect(64,238,20,122),K,-28,28,r=9,L='Schaftkappe')
    b.P(rect(108,230,94,22),K,-22,22,r=9,L='Wangenauflage',
        dec=[D(roundpoly(rect(122,236,64,8),4),P)])
    b.P([(208,242),(420,236),(454,252),(454,336),(228,336),(208,318)],
        DK,-30,30,r=12,L='Gehäuse',
        dec=[D(roundpoly([(228,254),(408,248),(428,258),(428,282),(228,288)],10),P),
             D(roundpoly(rect(246,264,90,9),4),A,True),
             D(roundpoly(rect(278,302,76,16),6),K),
             D(roundpoly(rect(378,304,40,7),3),AL,True)])
    rail(b,238,416,242,K,DK,w=13)
    # Der Ladehebel sitzt ausschließlich links, auf der breiten Gehäusewange.
    b.P(rect(334,298,30,12),A,29,43,r=5,L='Ladehebel')
    b.P([(258,334),(308,334),(328,432),(274,438)],K,-21,21,r=12,L='Griff',
        dec=[D(roundpoly([(278,352),(294,352),(308,410),(292,414)],6),DK)])
    b.P(arcband(308,398,334,64,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(328,335),(341,335),(351,376),(338,380)],A,-6,6,r=4,L='Abzug')
    b.P([(418,332),(458,332),(468,402),(426,406)],K,-19,19,r=9,L='Magazin',
        dec=[D(roundpoly(rect(430,348,20,38),7),P),
             D(roundpoly(rect(436,354,8,26),4),A,True)])
    b.P([(448,252),(558,258),(580,274),(580,312),(448,324)],DK,-24,24,r=12,L='Handschutz',
        dec=[D(roundpoly([(464,266),(546,270),(558,282),(558,294),(464,304)],9),P)]+
            [D(roundpoly(rect(476+24*i,278,13,17),5),K) for i in range(3)])
    # Ein freier, langer Lauf bleibt gegenüber Energiegewehren klar erkennbar.
    b.C(576,704,288,9,K,n=12,L='Lauf')
    b.C(704,742,288,15,DK,n=12,L='Mündungsbremse',
        cap=[(288,0,10,P,False),(288,0,6,'#050506',False)])
    b.P(rect(712,278,22,6),K,-15,15,r=3,L='Mündungsbremse')
    return b.m


META=dict(num='11',name='Scout-Gewehr',nick='WEITBLICK',col=A,
 pill='ARC-VERSION',palette=[P,DK,A,AL],center=(404,334,0),
 desc='Ein kurzer, schwer gerundeter Schulterblock trägt den breiten Präzisionsverschluss mit heller Deckplatte. Das kurze Kastenmagazin sitzt vor dem freien Abzugsraum; hinter dem kompakten Handschutz bleibt der lange gezogene Lauf mit Mündungsbremse frei.',
 form='Tiefer Schulterblock · Wangenauflage · breiter Verschlusskasten mit heller Deckplatte · Ladehebel links · kurzes Kastenmagazin · gerundeter Handschutz · langer freier Lauf · Mündungsbremse · gebogener Bügel',
 op=dict(reload_de='Kastenmagazin vor dem Abzug nach unten wechseln (8 Patronen), dann den Ladehebel links zurückziehen.',
         action_de='Halbautomatik: Der Ladehebel spannt den Verschluss einmal nach dem Magazinwechsel.',
         fire_de='Ein präziser Schuss je Abzug; Wangenauflage und Mündungsbremse stabilisieren die Schussfolge.',
         reload_en='Pull the box magazine ahead of the trigger down and replace it (8 rounds), then pull the left charging handle.',
         action_en='Semi-automatic: the charging handle cocks the bolt once after replacing the magazine.',
         fire_en='One precise shot per trigger pull; the cheek rest and muzzle brake steady the follow-up shot.'))
