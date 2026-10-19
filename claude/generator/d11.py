"""KD11 „Weitblick“: heller, abfallender Scout-Körper über offenem Skelettschaft."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#4D9CFF', '#CFEBFF'


def model():
    b = B(); D = b.D
    # Ober- und Unterstrebe sind getrennte Volumen: dazwischen bleibt ein echtes Fenster.
    b.P([(80,248),(220,240),(226,264),(94,278),(80,270)],P,-22,22,r=10,L='Schaft')
    b.P([(82,330),(194,304),(224,310),(224,332),(92,356),(82,348)],P,-22,22,r=10,L='Schaft')
    b.P(rect(64,242,24,120),K,-27,27,r=10,L='Schaftkappe')
    b.P(rect(108,232,92,22),DK,-24,24,r=9,L='Wangenauflage',
        dec=[D(roundpoly(rect(120,237,66,7),3),P)])
    b.P([(196,244),(224,242),(232,330),(208,336),(196,314)],K,-24,24,r=10,L='Schaftaufnahme')
    # Die hohe hintere Schulter fällt nach vorn deutlich zum Lauf ab.
    b.P([(216,230),(348,234),(422,250),(448,268),(448,316),(422,332),(224,332),(208,310)],
        P,-31,31,r=12,L='Gehäuse',
        dec=[D(roundpoly(rect(244,247,104,10),5),A,True),
             D(roundpoly(rect(370,276,48,10),5),K)])
    b.P([(222,310),(424,310),(448,302),(448,328),(422,342),(238,342)],DK,-26,26,r=10,L='Verschlusswanne')
    # Echte seitliche Verschlussplatte mit daran befestigtem Ladehebel.
    b.P(rect(282,268,78,26),DK,30,38,r=9,L='Verschluss',
        dec=[D(roundpoly(rect(294,277,46,7),3),K)])
    b.P(rect(334,277,30,12),A,37,49,r=5,L='Ladehebel')
    rail(b,236,348,235,K,DK,w=13)
    b.P([(258,336),(308,336),(326,426),(274,438),(260,414)],K,-22,22,r=12,L='Griff')
    for z0,z1 in ((22,27),(-27,-22)):
        b.P([(272,354),(298,351),(312,411),(284,418)],DK,z0,z1,r=9,L='Griffschale')
    b.P([(272,424),(324,414),(330,430),(278,444)],K,-25,25,r=8,L='Griffkappe')
    b.P(arcband(308,398,342,60,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(328,341),(341,341),(350,377),(338,381)],A,-6,6,r=5,L='Abzug')
    b.P(rect(410,330,54,17),DK,-24,24,r=8,L='Magazinschacht')
    b.P([(418,344),(458,344),(468,398),(428,404)],P,-20,20,r=10,L='Magazin',
        dec=[D(roundpoly(rect(433,356,17,30),7),K),D(roundpoly(rect(438,360,7,22),3),A,True)])
    b.P([(426,392),(468,386),(474,403),(430,410)],K,-23,23,r=8,L='Magazinboden')
    b.P(rect(402,332,16,13),A,23,34,r=5,L='Magazinriegel')
    b.P([(444,262),(534,268),(564,282),(566,306),(448,322)],P,-26,26,r=12,L='Handschutz',
        dec=[D(roundpoly(rect(470+25*i,280,14,16),5),K) for i in range(3)])
    b.P([(452,262),(528,266),(552,276),(548,286),(452,279)],DK,-17,17,r=9,L='Handschutzdeckel')
    b.P([(450,307),(562,296),(562,313),(450,328)],K,-20,20,r=8,L='Handschutzsohle')
    b.C(552,580,288,18,DK,n=16,L='Laufaufnahme')
    b.C(576,704,288,9,K,n=12,L='Lauf')
    b.C(580,596,288,12,P,n=12,L='Laufbund')
    b.F(700,714,288,10,17,DK,n=12,L='Mündungsbremse')
    b.C(712,744,288,17,DK,n=12,L='Mündungsbremse',
        cap=[(288,0,11,P,False),(288,0,6,'#050506',False)])
    b.P(rect(719,278,18,6),K,-17,17,r=3,L='Mündungsbremse')
    return b.m


META=dict(num='11',name='Scout-Gewehr',nick='WEITBLICK',col=A,
 pill='ARC-VERSION',palette=[P,DK,A,AL],center=(404,334,0),
 desc='Zwei helle, weich gerundete Schaftstreben lassen ein offenes Fenster unter der dunklen Wangenauflage. Der helle Scout-Körper fällt zum kurzen Handschutz ab; ein langer freier Lauf und das kurze Kastenmagazin kennzeichnen die Präzisionswaffe.',
 form='Offener Skelettschaft · zwei helle Streben · Wangenauflage · abfallender heller Körper · Verschlussplatte und Ladehebel links · kurzes Magazin · gerundeter Handschutz · langer freier Lauf · Mündungsbremse',
 op=dict(reload_de='Kurzes Kastenmagazin vor dem Abzug nach unten wechseln (8 Patronen), danach den Ladehebel links zurückziehen.',
         action_de='Halbautomatik: Verschlussplatte und Ladehebel laufen längs; nach dem Magazinwechsel einmal von Hand spannen.',
         fire_de='Ein präziser Schuss je Abzug; Wangenauflage und langer freier Lauf unterstützen ruhige Einzelschüsse.',
         reload_en='Pull down and replace the short box magazine ahead of the trigger (8 rounds), then pull the left charging handle.',
         action_en='Semi-automatic: bolt plate and charging handle travel lengthwise; cock once by hand after changing the magazine.',
         fire_en='One precise shot per trigger pull; the cheek rest and long free barrel support steady single shots.'))
