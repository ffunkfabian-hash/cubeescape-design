"""KD17 „Lichtspalter“: breite, kurz geführte D-Energieklinge mit schwerer Wurzel."""
from tlib import B
from eng import rect, roundpoly

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#F47BC7', '#FFE0F4'


def model():
    b = B(); D = b.D
    b.C(104,146,300,23,DK,n=12,L='Knauf',cap=[(300,0,10,A,True)])
    b.P(rect(142,280,142,40),K,-20,20,r=12,L='Griff',
        dec=[D(roundpoly(rect(156+22*i,284,11,32),5),DK) for i in range(5)])
    b.P([(270,250),(326,250),(344,268),(344,334),(326,350),(270,350)],
        DK,-28,28,r=12,L='Parierblock',
        dec=[D(roundpoly(rect(280,262,44,18),7),P),D(roundpoly(rect(280,326,44,12),5),P)])
    b.P(rect(284,284,38,34),K,-30,30,r=9,L='Energiezelle',
        dec=[D(roundpoly(rect(292,291,22,20),7),A,True),D(roundpoly(rect(299,296,8,10),4),AL,True)])
    # Eine quer liegende Parierstange, keine Visieraufnahme.
    b.Y([(280,-72),(308,-68),(330,-28),(330,28),(308,68),(280,72),
         (292,24),(292,-24)],DK,282,318,r=10,L='Parierstange',
        dec=[D(roundpoly([(286,42),(304,42),(312,60),(286,63)],5),P),
             D(roundpoly([(286,-42),(304,-42),(312,-60),(286,-63)],5),P)])
    b.P([(334,254),(680,242),(764,258),(824,300),(764,342),(680,358),(334,346)],
        DK,-9,9,r=12,L='Klinge',
        dec=[D(roundpoly([(354,266),(674,256),(750,270),(790,296),(352,296)],10),P),
             D(roundpoly([(354,322),(680,336),(756,324),(798,300),(812,300),
                          (764,338),(680,352),(354,338)],6),A,True),
             D(roundpoly([(372,329),(678,341),(748,330),(752,334),(678,347),(372,335)],3),AL,True)])
    b.P([(334,292),(688,286),(754,300),(688,314),(334,308)],K,-14,14,r=8,L='Mittelrippe',
        dec=[D(roundpoly(rect(370,297,262,6),3),A,True)])
    b.P([(330,258),(378,258),(392,278),(392,324),(378,344),(330,344)],
        DK,-19,19,r=10,
        dec=[D(roundpoly(rect(342,268,30,18),7),P),D(roundpoly(rect(342,316,30,16),6),P)])
    return b.m


META=dict(num='17',name='Schwert',nick='LICHTSPALTER',col=A,
 pill='PRISMATIC-VERSION',palette=[P,DK,A,AL],center=(464,300,0),
 desc='Eine breite, gerundet zulaufende Energieklinge sitzt auf einer schweren Klingenwurzel mit dunkler Mittelrippe. Helle Deckflächen und die rosa Leuchtschneide gliedern den kompakten Spalter; Energiezelle und seitlich ausladende Parierstange schützen den kräftigen Griff.',
 form='Breite gerundete Klinge · helle Deckflächen · rosa Leuchtschneide · schwere Mittelrippe · verstärkte Klingenwurzel · Parierblock mit Energiezelle · quer liegende Parierstange · dicker Griff · großer Knauf',
 op=dict(reload_de='Die Energiezelle im Parierblock hält die Ladungen für schwere Angriffe; schwere Munition füllt sie auf.',
         action_de='Leichter Schlag ohne Ladung, schwerer Schlag verbraucht eine Ladung; Blocken mit der quer gehaltenen Klinge entlädt die Zelle.',
         fire_de='Nahkampf mit Schlagkombinationen und Sprungangriff; die rosa Schneide leuchtet beim Blocken auf.',
         reload_en='The guard-block energy cell stores heavy-attack charges; heavy ammo replenishes them.',
         action_en='Light swings cost no charge; a heavy swing spends one charge. Guarding with the blade held across the body drains the cell.',
         fire_en='Melee swing combinations and leaping strikes; the pink edge lights up while guarding.'))
