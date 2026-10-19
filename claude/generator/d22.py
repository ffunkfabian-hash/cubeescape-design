"""KD22 „Felsenbrecher“: schwere D-Slug-Flinte mit gerundetem Laufmantel."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband
import math

M = '#3A3D44'
P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#C39A63', '#FBE4C3'


def model():
    b = B(); D = b.D
    # Der Schaft fällt am hinteren Ende nach unten; kein geschlossener Schulterquader.
    b.P([(88,274),(118,250),(150,252),(196,272),(242,264),(244,302),(188,306),(140,284),(118,306),(100,366),(78,358)],
        M,-25,25,r=12,L='Schaft')
    b.P([(78,322),(104,328),(100,372),(74,366)],K,-28,28,r=10,L='Schaftkappe')
    b.P([(112,258),(142,260),(188,280),(222,278),(222,290),(182,292),(136,274),(108,280)],P,-26,26,r=8,L='Schaftauflage')
    b.P(rect(222,264,30,44),K,-28,28,r=10,L='Schaftanschluss')
    # Der nach vorn abfallende Oberkörper ist ein einziges dunkles Keilvolumen.
    b.P([(240,244),(328,208),(462,236),(484,260),(484,326),(240,326),(224,306),(224,266)],M,-37,37,r=12,L='Gehäuse')
    b.P(rect(248,310,226,20),K,-30,30,r=8,L='Unterrahmen')
    b.P(rect(288,202,58,48),K,-15,15,r=8,L='Schienenbett')
    rail(b,288,346,208,K,DK,w=14)
    for z0,z1 in ((36,44),(-44,-36)):
        marks=[D(roundpoly([(272,258),(326,234),(414,250),(414,266),(272,282)],8),P),D(roundpoly(rect(274,294,128,8),4),A,True)]
        b.P([(252,254),(326,224),(442,248),(454,266),(454,304),(252,304)],M,z0,z1,r=12,L='Verschlussplatte',
            dec=marks if z0>0 else (),xdec=[('z-',z0,*d) for d in marks] if z0<0 else ())
    b.P(rect(308,270,40,16),K,43,59,r=6,L='Ladehebel',dec=[D(rect(316,275,22,5),A)])
    b.P(rect(410,322,62,22),DK,-27,27,r=8,L='Magazinaufnahme')
    b.P([(414,338),(466,338),(476,416),(420,424)],K,-24,24,r=10,L='Magazin',
        dec=[D(roundpoly(rect(426,352,32,52),7),P)]+[D(rect(432,358+13*i,20,7),A) for i in range(3)])
    b.P(rect(418,414,60,15),M,-27,27,r=6,L='Magazinboden')
    b.P(rect(394,322,20,20),K,27,40,r=6,L='Magazinriegel')
    b.C(476,634,282,24,K,n=12,L='Laufbett')
    b.P([(474,244),(582,250),(614,270),(614,302),(590,322),(474,322)],M,-31,31,r=12,L='Laufmantel')
    for z0,z1 in ((30,38),(-38,-30)):
        marks=[D(roundpoly(rect(502,270,74,10),4),K),D(roundpoly(rect(506,290,68,6),3),A,True)]
        b.P([(490,258),(582,264),(598,278),(590,306),(490,306)],P,z0,z1,r=12,L='Wärmeschutzplatte',
            dec=marks if z0>0 else (),xdec=[('z-',z0,*d) for d in marks] if z0<0 else ())
    b.C(606,622,282,32,DK,n=12,L='Laufklemmung')
    b.C(622,688,282,16,K,n=12,L='Lauf')
    b.C(650,664,282,21,M,n=12,L='Laufring')
    b.C(682,720,282,25,M,n=12,L='Mündungsbremse',cap=[(282,0,11,K,False)]+
        [(282+13*math.sin(k*math.pi/3),13*math.cos(k*math.pi/3),2,A,False) for k in range(6)])
    for z0,z1 in ((22,27),(-27,-22)):
        slots=[D(roundpoly(rect(692,274,20,5),2),K),D(roundpoly(rect(692,284,20,5),2),K)]
        b.P(rect(686,266,30,32),P,z0,z1,r=8,L='Bremsbacke',dec=slots if z0>0 else (),xdec=[('z-',z0,*d) for d in slots] if z0<0 else ())
    b.P([(260,326),(310,326),(330,426),(274,434)],K,-23,23,r=12,L='Griff')
    b.P(rect(274,424,56,15),M,-25,25,r=6,L='Griffabschluss')
    b.P(arcband(310,392,328,68,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(330,329),(343,329),(355,370),(342,376)],A,-6,6,r=4,L='Abzug')
    b.P([(526,318),(560,318),(556,388),(532,394)],K,-19,19,r=10,L='Vordergriff')
    return b.m

META=dict(num='22',name='Slug-Schrotflinte',nick='FELSENBRECHER',col=A,
 pill='RELIKT-SKIN',palette=[M,P,A,AL],center=(398,336,0),
 desc='Eine dunkle Slug-Flinte mit hochgezogenem Keilkörper und nach unten gebogenem Hakenschaft. Helle Wärmeschutzplatten umfassen den langen, tiefen Laufmantel; unter dem vorderen Verschluss sitzt das Slug-Magazin. Sandfarbene Fenster führen zur breiten Mündungsbremse.',
 form='Abgesenkter Hakenschaft · Keilgehäuse · seitliche Verschlussplatten · Ladehebel · Kastenmagazin mit Boden · tiefer Laufmantel · helle Wärmeschutzplatten · freier gezogener Lauf · Mündungsbremse mit Bremsbacken · Vordergriff',
 op=dict(reload_de='Kastenmagazin vor dem Abzug wechseln (5 Slug-Patronen), danach Ladehebel links zurückziehen.',
         action_de='Halbautomatik: ein Einzelgeschoss je Abzug; der Ladehebel spannt nach dem Magazinwechsel.',
         fire_de='Schweres Einzelgeschoss mit hoher Wucht und Präzision auf mittlere Distanz, ohne Streukegel.',
         reload_en='Swap the five-round slug box magazine ahead of the trigger, then pull the left charging handle.',
         action_en='Semi-automatic: one slug per trigger pull; use the charging handle after a magazine change.',
         fire_en='A heavy single slug delivers high impact and precision at medium range without a spread cone.'))
