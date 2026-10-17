from flib import *
from flabel import Lb
from fsight import Sg
from eng import rect,circ,roundpoly
TB,SE,EW,RT,K='#1D3557','#D4A017','#EEF1F0','#E63946','#12141A'
def spec():
    return [
    Lb(P([(70,250),(222,246),(222,258),(70,264)],TB,-10,10,r=4),'Schaft'),
    Lb(P([(80,320),(222,314),(222,326),(88,334)],TB,-10,10,r=4),'Schaft'),
    P([(60,244),(86,244),(92,340),(66,340)],SE,-14,14,r=6),
    Lb(P([(210,236),(400,236),(422,258),(422,322),(210,322)],EW,-26,26,r=12,
      dec=[D(roundpoly([(222,300),(410,300),(410,309),(222,309)],3),SE),
           D(circ(318,272,22),TB),D(circ(318,272,11),RT,True)]),'Fokuskern'),
    # Zielfernrohr auf zwei Montageringen mit Füßen
    Lb(P(rect(246,229,140,7.5),K,-8,8,r=1,dec=[D(rect(x,230.5,6,3.5),TB) for x in range(252,384,12)]),'Visierschiene'),
    Sg(P(rect(268,214,18,15.5),K,-6,6,r=3)),
    Sg(P(rect(352,214,18,15.5),K,-6,6,r=3)),
    Sg(Lb(C(250,384,200,15,TB,cap=[(200,0,9,'#05060A',False),(200,0,5,RT,True)]),'Zielfernrohr')),
    Sg(C(266,288,200,17,K)),
    Sg(C(350,372,200,17,K)),
    Lb(C(418,704,272,8,K),'Lauf'),
    P([(418,246),(650,252),(650,260),(418,258)],TB,-8,8,r=3),
    P([(418,286),(610,284),(610,292),(418,296)],TB,-8,8,r=3),
    Lb(C(470,478,272,14,RT,emit=True),'Fokusringe'),Lb(C(540,548,272,14,RT,emit=True),'Fokusringe'),Lb(C(610,618,272,14,RT,emit=True),'Fokusringe'),
    F(704,736,272,9,1.5,SE),
    Lb(P([(250,322),(296,322),(288,414),(240,414)],TB,-18,18,r=8,dec=[D(roundpoly(rect(252,350,30,6),2),SE)]),'Griff'),
    # Abzug im Bügel vor dem Griff
    Lb(P([(304,324),(314,324),(321,364),(312,366)],RT,-3.5,3.5,r=1),'Abzug'),
    Lb(P(rect(289,372,59,7),K,-5,5,r=3),'Abzug'),
    P(rect(341,322,7,57),K,-5,5,r=3),
    P([(440,296),(472,296),(468,352),(444,352)],SE,-10,10,r=6),
    ]
META=dict(num='08',name='Spurgewehr',vname='Nadel',col='#E63946',pill='TIEFBLAU · SENF · ROT',
 palette=[TB,SE,EW,RT],center=(398,290,0),
 aria='Spurgewehr Variante F: schlankes Gewehr mit eisweißem Gehäuse, langem nadeldünnem Lauf zwischen zwei tiefblauen Schienen, roten Leuchtringen, Skelettschaft und rundem Fokus-Auge',
 desc='Extrem schlank: ein nadeldünner Lauf zwischen zwei Schienen, rote Fokusringe markieren die Strahlbahn. Hinten ein offener Skelettschaft. Tiefblau, Eisweiß, Senf und Signalrot.',
 form='Nadellauf zwischen zwei Schienen · rote Fokusringe · Visierschiene, Zielfernrohr separat · Skelettschaft · Abzug mit Bügel',
 desc3='Die Nadel als Konzeptblatt: Der dünne Lauf tritt vorne aus dem Gehäuse und wird von zwei Schienen geführt, die drei roten Fokusringe verbinden Lauf und Schienen. Auf der Visierschiene wird das separat gezeichnete Zielfernrohr mit zwei Montageringen befestigt, der Fokuskern liegt in beiden Flanken, der Abzug im Bügel vor dem Griff.')
