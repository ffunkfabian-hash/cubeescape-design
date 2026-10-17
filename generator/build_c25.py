from cepaths import E3D,OUT
import sys,importlib
sys.path.insert(0,E3D+'')
from views import card
INFO={
'02':((390,230,0),'Sturmgewehr','WALDLÄUFER','#FF8C1A','WALDGRÜN · OLIV · ORANGE',['#2F4F3A','#6B7F4E','#1C2A20','#FF8C1A'],
 'Das waldgrüne Sturmgewehr aus Variante C: Der Tragegriff trägt oben ein Schienenprofil, Diopter und Korn sind abnehmbar und separat gezeichnet. Abzug und Bügel hängen frei vor dem Griff, das gebogene Magazin sitzt davor, vorne der Schalldämpfer mit Leuchtringen.',
 'Tragegriff mit Schienenprofil (Visier separat) · Abzug im Bügel · gebogenes Magazin · Teleskopschaft · Schalldämpfer'),
'03':((390,230,0),'Impulsgewehr','KRISTALL','#2DD4BF','PERLMUTT · SCHWARZ · TÜRKIS',['#E7E4EE','#A9A3B8','#141820','#2DD4BF'],
 'Das facettierte Impulsgewehr aus Variante C: Der türkise Kristallkern steckt quer im Rautengehäuse, drei Fokusringe sitzen auf dem kräftigen Lauf. Auf dem Grat bleibt die Visierbasis, das Kristall-Reflexvisier ist separat gezeichnet.',
 'Rautenförmiges Facetten-Gehäuse · Kristallkern · Lauf mit drei Fokusringen · Abzug im Bügel · Visierbasis (Visier separat)'),
'04':((390,240,0),'Schrotflinte','DRACHENMAUL','#FF7A2E','JADE · BRONZE · FEUER',['#0F766E','#0B3B37','#B4783C','#FF7A2E'],
 'Die Drachenmaul-Schrotflinte aus Variante C: Der Lauf führt sichtbar ins Maul, der Feuerkern sitzt auf der Mündung zwischen Ober- und Unterkiefer. Darunter das Trommelmagazin, davor Abzug und Bügel. Das Kastenvisier ist separat gezeichnet, oben bleibt die Schiene.',
 'Drachenmaul-Mündung · sichtbarer Lauf · Trommelmagazin · Abzug im Bügel · Visierschiene (Visier separat) · Bronze-Schuppenplatten'),
'05':((400,230,0),'Scharfschützengewehr','MONOLITH','#F5C542','MATTSCHWARZ · GRAPHIT · GOLD',['#24262B','#34373E','#16171A','#F5C542'],
 'Der Monolith aus Variante C, konstruktiv überarbeitet: offener Skelettschaft mit Wangenauflage, Pistolengriff mit Abzug und Bügel, das Magazin sitzt davor im Schacht. Der schlanke Lauf tritt sichtbar aus der kurzen Verkleidung und endet in einer kastenförmigen Mündungsbremse. Das achteckige Zielfernrohr mit Montageringen ist separat gezeichnet, auf dem Gehäuse bleibt die Schiene; der Kammerstängel sitzt links.',
 'Skelettschaft · Pistolengriff mit Abzug · Magazin vor dem Griff · sichtbarer Lauf · Kasten-Mündungsbremse · Montageschiene (Zielfernrohr separat)'),
}
n=sys.argv[1]
c,name,nick,col,pill,pal,desc,form=INFO[n]
m=importlib.import_module('c'+n).model()
h=card(m,c,n,name,f'VARIANTE C · „{nick}“ · ALLE PERSPEKTIVEN, GEZEICHNET',col,pill,desc,pal,form,'c'+n)
open(f'{OUT}/C3D{n}.dc.html','w').write(h)
open(f'{E3D}/prev_c{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
