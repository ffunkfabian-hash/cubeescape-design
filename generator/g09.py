from flib import *
from flabel import Lb
from gsight import S
from eng import rect,circ,roundpoly
CR,K,OR,GR,CY='#EDE4CF','#1B1C20','#FF6B1A','#4A4F59','#6FD8E0'
def spec():
    s=[]
    for cz in (22,-22):
        s.append(Lb(C(170,600,280,20,CR,n=8,cz=cz),'Abschussrohre'))
        s.append(Lb(F(138,170,280,27,20,GR,cz=cz),'Abgasdüse'))
        s.append(C(135,138.5,280,19,'#050506',n=8,cz=cz))
        # offene Duese: Innenrohr ragt aus der dunklen Duesenoeffnung
        s.append(C(124,139,280,10,GR,n=8,cz=cz))
        s.append(C(121.5,124,280,6.5,'#050506',n=8,cz=cz))
        s.append(C(600,616,280,22,K,n=8,cz=cz,cap=[(280,cz,15,'#050506',False)]))
        s.append(Lb(F(608,640,280,11,2,OR,cz=cz),'Rakete'))
    for x in (226,400,566):
        s.append(P(rect(x,254,14,52),K,-46,46,r=3))
    s+=[
    # Visier auf Fuß an der mittleren Schelle
    # Visieraufnahme seitlich LINKS an den Rohren (Sichtlinie frei, wie RPG-7/Carl Gustaf):
    # Klemmschelle am linken Rohr + Schiene auf Höhe der Rohroberkante
    P(rect(394,256,34,28),K,28,47,r=3),
    Lb(P(rect(384,248,54,9),K,40,54,r=2,dec=[D(rect(x,250,6,4),GR) for x in range(388,434,10)]),'Visierschiene'),
    # Visier (separat): Fuß auf der Schiene + Visierkopf mit Linse
    S(P(rect(398,236,26,12.5),K,41,53,r=2)),
    S(Lb(P([(380,212),(440,212),(448,236),(374,236)],GR,39,55,r=4,xdec=[('x+',448,roundpoly(rect(218,41,14,12),3),CY,True)]),'Visier')),
    # Unterzug zwischen den Rohren, Schulterstütze
    P(rect(214,294,372,24),K,-16,16,r=5),
    P([(200,318),(272,318),(264,340),(208,340)],GR,-30,30,r=6),
    # Griff, Abzug, Bügel, Vordergriff
    Lb(P([(330,318),(380,318),(370,414),(316,414)],K,-16,16,r=6,dec=[D(roundpoly(rect(332,338+12*i,32,5),2),GR) for i in range(5)]),'Griff'),
    Lb(P([(392,319),(404,319),(416,360),(404,364)],OR,-6,6,r=2),'Abzug'),
    P(rect(378,380,72,9),K,-7,7,r=3),
    P(rect(442,318,9,71),K,-7,7,r=3),
    Lb(P([(498,318),(534,318),(528,386),(504,386)],CR,-12,12,r=6),'Vordergriff'),
    ]
    return s
META=dict(num='09',name='Raketenwerfer',vname='Doppelrohr',col='#FF6B1A',pill='CREME · SCHWARZ · ORANGE',
 palette=[CR,K,OR,GR],center=(390,300,0),
 aria='Raketenwerfer Variante G: zwei achteckige cremefarbene Abschussrohre nebeneinander, von drei schwarzen Schellen gehalten, Abgasdüsen hinten, orange Raketenspitzen vorne, Visier auf der mittleren Schelle, Griff und Vordergriff am Unterzug',
 desc='Zwei achteckige Rohre nebeneinander feuern nacheinander: Drei schwarze Schellen halten sie zusammen, hinten sitzen die Abgasdüsen, vorne schauen die orangen Raketenspitzen heraus.',
 form='Visier seitlich links montiert · Zwei achteckige Abschussrohre · drei Schellen · Abgasdüsen hinten · Unterzug mit Griff, Abzug und Vordergriff · Schulterstütze',
 desc3='Das Doppelrohr als Konzeptblatt: Die zwei achteckigen Rohre liegen nebeneinander und werden von drei Schellen gehalten. Das Visier sitzt seitlich links auf einer Schiene an der Rohrschelle, damit die Rohre die Sichtlinie nicht verdecken; es ist separat gezeichnet. Unter den Rohren läuft ein Unterzug, an dem Schulterstütze, Griff mit Abzug im Bügel und Vordergriff sitzen. Hinten öffnen sich die Abgasdüsen, vorne ragen die orangen Raketenspitzen aus den Mündungen.')
