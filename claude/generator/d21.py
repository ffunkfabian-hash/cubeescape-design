"""KD21 „Donnerfolge“: kompakter D-Salvenblock für fünf kleine Raketen."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#648EE8', '#DAE5FF'


def model():
    b = B(); D = b.D
    b.P([(96,244),(168,244),(224,264),(224,326),(174,326),(116,348),(96,348)],
        DK,-25,25,r=12,L='Schaft',
        dec=[D(roundpoly(rect(112,256,74,24),9),P),D(roundpoly(rect(116,308,44,10),4),K)])
    b.P(rect(82,238,20,120),K,-28,28,r=8,L='Schaftkappe')
    b.P([(212,232),(430,228),(466,246),(466,338),(232,338),(212,318)],
        DK,-34,34,r=12,L='Gehäuse',
        dec=[D(roundpoly([(234,246),(412,242),(438,254),(438,284),(234,292)],10),P),
             D(roundpoly(rect(248,258,148,9),4),A,True),
             D(roundpoly(rect(244,310,166,12),5),K)])
    rail(b,244,410,234,K,DK,w=14)
    b.P(rect(304,286,34,14),K,32,48,r=6,L='Ladehebel',
        dec=[D(roundpoly(rect(312,289,18,7),3),A)])
    # Der breite Querspeicher liegt deutlich vor dem freien Abzugsraum.
    b.P(rect(398,332,94,56),K,-35,35,r=10,L='Raketenmagazin',
        dec=[D(roundpoly(rect(406,342,78,34),8),P),
             D(roundpoly(rect(412,346,66,26),6),K)]+
            [D([(416+12*i,367),(421+12*i,351),(426+12*i,367)],A) for i in range(5)])
    b.P([(458,252),(562,252),(580,268),(580,320),(560,336),(458,336)],
        DK,-28,28,r=12,L='Handschutz',
        dec=[D(roundpoly(rect(476,262,80,18),7),P)]+
            [D(roundpoly([(480+22*i,292),(492+22*i,292),(486+22*i,318),(474+22*i,318)],4),A,True) for i in range(4)])
    b.C(570,654,292,17,K,n=12,L='Lauf')
    b.F(604,628,292,24,20,DK,n=12,L='Abgasring')
    b.C(650,676,292,23,DK,n=12,L='Mündung',
        cap=[(292,0,14,K,False),(292,0,6,A,True),(292,0,2.5,AL,True)])
    b.P([(260,336),(310,336),(328,432),(274,438)],K,-22,22,r=12,L='Griff',
        dec=[D(roundpoly([(280,356),(296,356),(309,412),(294,414)],6),DK)])
    b.P(arcband(310,390,336,66,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(330,337),(343,337),(354,376),(341,382)],A,-6,6,r=4,L='Abzug')
    b.P([(516,334),(550,334),(548,402),(522,406)],DK,-18,18,r=10,L='Vordergriff',
        dec=[D(roundpoly(rect(528,350,10,34),4),A,True)])
    return b.m


META=dict(num='21',name='Raketen-Impulsgewehr',nick='DONNERFOLGE',col=A,
 pill='STORM-SKIN',palette=[P,DK,A,AL],center=(380,330,0),
 desc='Ein kurzer, tief gerundeter Salvenblock trägt helle Deckplatten und blaue Leuchtstreifen. Das breite Raketenmagazin zeigt fünf Spitzen vor dem freien Abzugsraum; ein massiger Handschutz führt die Abgase zum Rohrlauf mit Abgasring.',
 form='Tiefer Schulterblock · gerundetes Gehäuse · Ladehebel links · querliegendes Raketenmagazin mit fünf Spitzen · Handschutz mit Abgasschlitzen · Rohrlauf und Abgasring · weite Mündung · gebogener Bügel · Vordergriff',
 op=dict(reload_de='Raketenmagazin vor dem Abzug nach unten wechseln (5 Raketen), Ladehebel links zurückziehen.',
         action_de='Jede Abzugbetätigung löst eine Zweier-Salve aus; Abgas strömt durch die Schlitze des Handschutzes nach vorn.',
         fire_de='Kleine Raketen explodieren beim Aufprall; Salvenfeuer mit Spezialmunition und kleinem Vorrat.',
         reload_en='Pull the rocket magazine ahead of the trigger down, insert five fresh rockets and pull the left charging handle.',
         action_en='Each trigger pull fires a two-rocket burst; exhaust escapes forward through the handguard slots.',
         fire_en='Small rockets explode on impact; burst fire with special ammo and a small reserve.'))
