from cepaths import E3D,OUT
import sys;from views import *;import dmods
D={1:('Pistole','Eisblau','ARC-VERSION',['#D8DCE0','#2A2F38','#3BA3E8','#BFE6FF'],'#3BA3E8',
 'Die Pistole aus Variante D „Eisblau“, rundum gezeichnet und etwas weicher abgerundet. Von vorne sieht man die große Mündung mit dem eisblauen Leuchtring. Oben sitzt die Visierschiene, das Visier ist separat gezeichnet.',
 'Großes rundes Mündungsgehäuse · helles Frontpaneel mit Ladeblock unten · nach hinten geneigter Griff · Visierschiene oben (Visier separat)'),
 2:('Sturmgewehr','Nachtschicht','STEALTH-SKIN',['#3A3D44','#1A1C20','#E11D2E','#FF8A94'],'#F04452',
 'Das Sturmgewehr aus Variante D „Nachtschicht“ in Graphit mit Signalrot, rundum gezeichnet. Oben sitzt die Visierschiene, das kastenförmige Visier ist separat gezeichnet; hinten der breite Schaft.',
 'Visierschiene oben (Kastenvisier separat) · Pistolengriff mit Abzugbügel · Magazin vor dem Abzug · langer Handschutz · breiter Schaft'),
 3:('Impulsgewehr','Gold-Void','EXOTIC-SKIN',['#D9B97A','#2A2530','#A855F7','#E9D5FF'],'#D9B97A',
 'Das Impulsgewehr aus Variante D „Gold-Void“, rundum gezeichnet. Der violette Energiekanal läuft an beiden Seiten der Laufhülle entlang, der Schaft ist offen. Das Visier ist separat gezeichnet, auf dem Gehäuse bleibt die Visierschiene.',
 'Offener Rahmenschaft · Abzugbügel mit Energiezelle davor · violetter Energiekanal an der Laufhülle · Visierschiene (Visier separat)'),
 4:('Schrotflinte','Säure','TOXIN-VERSION',['#D8DCE0','#24282E','#22C55E','#BBF7D0'],'#22C55E',
 'Die Schrotflinte aus Variante D „Säure“, rundum gezeichnet. Zwei Läufe übereinander, der obere mit giftgrünem Leuchtpaneel, darunter der breite Trommelkasten. Auf dem oberen Gehäuse bleibt die Visierschiene, das Visier ist separat gezeichnet.',
 'Zwei Läufe übereinander · Trommelmagazin unter dem Gehäuse · Abzugbügel vor dem Griff · helle Deckplatte oben · Visierschiene (Visier separat)'),
 5:('Scharfschützengewehr','Wüste','SOLAR-VERSION',['#D6C6A0','#2E2A24','#F28C28','#FFD7A8'],'#F28C28',
 'Neu konstruiert: Auf dem Gehäuse sitzt eine Visierschiene, das Zielfernrohr mit zwei Ringen ist separat gezeichnet. Der Lauf tritt sichtbar aus der schlanken Verkleidung aus. Magazin vor dem Abzug, Pistolengriff mit Bügel, Schaft als Rahmen mit Wangenauflage.',
 'Rahmenschaft mit Wangenauflage · Pistolengriff mit Abzugbügel · Magazin vor dem Abzug · Visierschiene (Zielfernrohr separat) · freier Lauf mit Mündungsbremse')}
for i in map(int,sys.argv[1:]):
    w,nm,pill,pal,col,desc,form=D[i]
    m,c=getattr(dmods,'d%02d'%i)(*pal)
    h=card(m,c,'%02d'%i,w,'VARIANTE D · „%s“ · ALLE PERSPEKTIVEN, GEZEICHNET'%nm.upper(),col,pill,desc,pal,form,'d%02d'%i)
    open(OUT+'/D3D%02d.dc.html'%i,'w').write(h)
    open(E3D+'/prev_d%02d.html'%i,'w').write(h.replace('<script src="./support.js"></script>',''))
    import subprocess;subprocess.run(['python3',E3D+'/shot.py',E3D+'/prev_d%02d.html'%i,E3D+'/prev_d%02d.png'%i,'2400','1560'])
