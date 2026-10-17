from cepaths import E3D,OUT
from views import *;from v01m import model
h=card(model(),(400,250,0),'01','Pistole','VARIANTE C · „DOPPELKAMMER“ · ALLE PERSPEKTIVEN, GEZEICHNET','#FFD166','WEINROT · SCHWARZ · GOLD',
'Die Doppelkammer-Pistole aus Variante C: zwei Läufe übereinander, die goldene Energiezelle steckt quer im Gehäuse. Abzug und Bügel hängen gut sichtbar unter dem Gehäuse. Kimme und Korn sind abnehmbar und separat gezeichnet; auf dem Gehäuse bleibt die Visierschiene.',
['#8E1F2F','#5E1420','#1C181C','#FFD166'],'Zwei Läufe übereinander · Energiezelle quer im Gehäuse · Abzug im Bügel · Visierschiene (Visier separat) · breiter Griff','v01')
open(OUT+'/C3D01.dc.html','w').write(h)
open(E3D+'/prev.html','w').write(h.replace('<script src="./support.js"></script>',''))
