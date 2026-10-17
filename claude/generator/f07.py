from flib import *
from flabel import Lb
from fsight import Sg
from eng import rect,circ,roundpoly
PF,M,S,K='#5B2A6E','#6EE7B7','#C9D1DB','#1E1424'
def spec():
    return [
    P([(84,262),(204,250),(224,258),(224,336),(156,336),(92,310)],S,-22,22,r=12,dec=[D(roundpoly(rect(110,276,80,10),4),PF)]),
    Lb(P([(204,226),(420,216),(440,236),(440,336),(204,336)],PF,-30,30,r=14,
      dec=[D(roundpoly(rect(232,248,130,30),8),K),D(roundpoly(rect(240,256,114,14),5),M,True),
           D(roundpoly([(224,300),(420,296),(420,306),(224,310)],3),S)]),'Gehäuse'),
    # Visier auf Montagefuß, der auf der schrägen Oberseite sitzt
    Lb(P([(294,211),(354,211),(354,220.8),(294,223.5)],K,-7,7),'Visierschiene'),
    Sg(Lb(P(rect(282,194,84,18),S,-9,9,r=5,xdec=[('x+',366,circ(203,0,5),M,True)]),'Visier')),
    Lb(C(436,516,272,58,S,n=6),'Kondensator'),
    C(462,484,272,61,M,n=6,emit=True),
    C(514,648,272,17,K),
    Lb(C(548,560,272,30,S,n=16),'Kühlrippen'),
    Lb(C(590,602,272,30,S,n=16),'Kühlrippen'),
    Lb(P([(628,238),(700,246),(700,258),(628,256)],PF,-10,10,r=4),'Emitter'),
    Lb(P([(628,288),(700,286),(700,298),(628,306)],PF,-10,10,r=4),'Emitter'),
    C(648,668,272,10,M,emit=True),
    Lb(P([(250,336),(300,336),(292,428),(240,428)],K,-18,18,r=8),'Griff'),
    # Abzug im Bügel direkt vor dem Griff
    Lb(P([(306,338),(316,338),(323,380),(314,382)],M,-3.5,3.5,r=1),'Abzug'),
    Lb(P(rect(291,388,64,7),K,-5,5,r=3),'Abzug'),
    P(rect(348,336,7,59),K,-5,5,r=3),
    P([(354,336),(424,336),(414,358),(362,358)],K,-24,24,r=6,dec=[D(roundpoly(rect(x,342,14,8),3),'#3A2A44') for x in (370,392)]),
    ]
META=dict(num='07',name='Fusionsgewehr',vname='Prisma',col='#6EE7B7',pill='PFLAUME · MINT · SILBER',
 palette=[PF,M,S,K],center=(392,312,0),
 aria='Fusionsgewehr Variante F: pflaumenfarbenes Gehäuse mit sechseckiger silberner Kondensator-Trommel, mintgrünem Leuchtring, Kühlrippen und gegabeltem Emitter',
 desc='Die Ladung sammelt sich in einer sechseckigen Kondensator-Trommel mit mintgrünem Leuchtring. Vorne bündelt ein gegabelter Emitter den Strahl. Pflaume, Mint und Silber.',
 form='Sechseckige Kondensator-Trommel · Montagefuß als Visieraufnahme, Visier separat · Abzug mit Bügel · Kühlrippen am Lauf · gegabelter Emitter',
 desc3='Das Prisma als Konzeptblatt: Vor dem Gehäuse sitzt die sechseckige Kondensator-Trommel mit mintgrünem Ladering, dahinter der Lauf mit zwei Kühlrippen. Vorne halten zwei Gabelzinken den Emitterkern. Der Montagefuß nimmt das separat gezeichnete Visier auf, der Abzug liegt im Bügel vor dem Griff.')
