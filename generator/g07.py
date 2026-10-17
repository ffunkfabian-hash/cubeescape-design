from flib import *
from flabel import Lb
from gsight import S
from eng import rect,circ,roundpoly
W,K,CY,OR,GR='#F4F5F7','#17181C','#38D9E8','#FF8A2A','#3A3D45'
def cell(x):
    return [Lb(P(circ(x,212,24,8),K,-30,30,r=2,dec=[D(roundpoly(rect(x-18,206,36,12),3),GR)]),'Kondensatorzelle'),
            P(circ(x,212,13,8),CY,-31.5,31.5,emit=True)]
def spec():
    return [
    Lb(P([(96,262),(184,256),(198,300),(198,338),(150,352),(96,348)],K,-20,20,r=8,
      dec=[D(roundpoly(rect(110,276,56,10),3),GR)]),'Schaft'),
    P(rect(88,258,12,94),GR,-21,21,r=4),
    Lb(P([(192,248),(470,248),(520,272),(520,330),(482,346),(192,346)],W,-28,28,r=10,
      dec=[D(roundpoly([(196,322),(516,322),(516,330),(482,344),(196,344)],3),K),
           D(roundpoly(rect(214,268,120,30),6),K),
           D(roundpoly(rect(224,278,100,10),3),CY,True),
           D(roundpoly(rect(372,268,12,40),3),GR),D(roundpoly(rect(392,268,12,40),3),GR),D(roundpoly(rect(412,268,12,40),3),GR)]),'Gehäuse'),
    P(rect(250,236,170,14),K,-24,24,r=3),
    *cell(292),*cell(372),
    # Visier auf Fuß vorne am Gehäuse
    P(rect(438,243,40,6),K,-8,8,r=2),  # Visierbasis (bleibt)
    S(P(rect(446,231,24,13),K,-7,7,r=2)),
    S(Lb(P([(440,213),(482,213),(486,231),(436,231)],GR,-9,9,r=3,xdec=[('x+',486,roundpoly(rect(216,-5,12,10),3),CY,True)]),'Visier')),
    # Emitterblock, Kühlrippen, Emitterkegel
    P([(520,266),(604,270),(604,326),(520,334)],K,-22,22,r=6),
    Lb(P(rect(540,256,9,86),W,-26,26,r=3),'Kühlrippen'),
    Lb(P(rect(560,258,9,82),W,-25,25,r=3),'Kühlrippen'),
    Lb(P(rect(580,260,9,78),W,-24,24,r=3),'Kühlrippen'),
    Lb(F(604,652,298,22,12,W),'Emitter'),
    C(652,668,298,13,K,n=8,cap=[(298,0,8,'#050506',False),(298,0,4,CY,True)]),
    # Griff, Abzug, Bügel, Vordergriff
    Lb(P([(332,346),(382,346),(372,442),(318,442)],K,-18,18,r=6,dec=[D(roundpoly(rect(334,366+12*i,32,5),2),GR) for i in range(5)]),'Griff'),
    Lb(P([(394,347),(406,347),(418,388),(406,392)],OR,-6,6,r=2),'Abzug'),
    P(rect(380,408,72,9),K,-7,7,r=3),
    P(rect(444,346,9,71),K,-7,7,r=3),
    Lb(P([(500,338),(536,336),(530,394),(506,394)],GR,-13,13,r=6),'Vordergriff'),
    ]
META=dict(num='07',name='Fusionsgewehr',vname='Zwilling',col='#38D9E8',pill='WEISS · SCHWARZ · CYAN',
 palette=[W,K,CY,OR],center=(380,300,0),
 aria='Fusionsgewehr Variante G: weißes, abgeschrägtes Gehäuse mit zwei quer liegenden achteckigen Kondensatorzellen oben, Kühlrippen und weißem Emitterkegel, schwarzer Schaft und Griff',
 desc='Zwei quer liegende Kondensatorzellen laden den Schuss: Sie sitzen in einer Wiege auf dem weißen Gehäuse und leuchten an beiden Enden cyan. Vorne kühlen drei Rippen den Emitterkegel.',
 form='Zwei achteckige Kondensatorzellen quer in einer Wiege · Visier auf Fuß · drei Kühlrippen · Emitterkegel · Griff mit Abzug im Bügel · Vordergriff',
 desc3='Der Zwilling als Konzeptblatt: Die beiden achteckigen Kondensatorzellen liegen quer in der schwarzen Wiege auf dem Gehäuse und ragen an beiden Seiten mit cyan Kern heraus. Davor steht das Visier auf seinem Fuß. Drei weiße Kühlrippen umfassen den Emitterblock, dahinter liegt der Abzug im Bügel vor dem Griff.')
