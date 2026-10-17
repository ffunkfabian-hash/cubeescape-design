from cepaths import E3D,OUT
import sys;from views import *;import dmodels
O=OUT+'/'
INFO={
'06':('Maschinenpistole','BERNSTEIN','#F5B014','BELOHNUNGS-SKIN',['#D8DCE0','#2A2F38','#F5B014','#FFE7A3'],'Die MP im Bernstein-Skin von Variante D, rundum gezeichnet und etwas weicher abgerundet. Von vorne sieht man die zwei Mündungen, von oben der Tragegriff. Kimme und Korn sind separat gezeichnet (modular auf dem Tragegriff). Abzug und Bügel hängen sichtbar unter dem Gehäuse.','Kurzer Lauf mit großem Frontblock · Magazin vorne, Pistolengriff mit Abzug hinten · Klappschaft · Tragegriff als Visierbasis'),
'07':('Fusionsgewehr','FROST','#22D3EE','KRYO-VERSION',['#CFE0F0','#1E2A38','#22D3EE','#CFFAFE'],'Das Fusionsgewehr in Frost-Farben, rundum gezeichnet. Die Kryo-Röhre leuchtet durch das Fenster im Lauf, die Ladekammer sitzt im hellen Mittelteil. Das Visier ist separat gezeichnet, auf der Waffe bleibt die Visierschiene.','Langer Laufkasten mit Sichtfenster · Ladekammer mit Visierschiene · Abzug im Bügel · Lüftungsschlitze unten'),
'08':('Spurgewehr','BLUTMOND','#F25555','BOSS-SKIN',['#3A3D44','#18191C','#EF2B2B','#FFB4B4'],'Das Spurgewehr im Blutmond-Skin, rundum gezeichnet. Der rote Strahl läuft durch den ganzen Lauf, das runde Auge in der Mitte ist von beiden Seiten sichtbar. Das Zielfernrohr ist separat gezeichnet, modular auf der Visierschiene.','Langer Lauf mit Leuchtröhre · rundes Energie-Auge · Visierschiene (Zielfernrohr separat) · Abzug im Bügel · zwei Griffe'),
'09':('Raketenwerfer','SOG','#EC4FA6','GRAVITY-VERSION',['#D8DCE0','#2A2F38','#EC4FA6','#FBCFE8'],'Der Raketenwerfer in der Gravity-Version, rundum gezeichnet. Von vorne sieht man die große achteckige Mündung mit Magenta-Glut. Das Visier sitzt seitlich links montiert auf einer Schiene, weil das dicke Rohr oben die Sichtlinie verdecken würde; es ist separat gezeichnet.','Dickes Rohr aus drei Segmenten · achteckige Mündung · Visierschiene seitlich links montiert (Visier separat) · Abzug im Bügel · zwei Griffe'),
'10':('Bogen','OBSIDIAN-GOLD','#F2C230','NACHT-SKIN',['#3A3D44','#17181B','#F2C230','#FFF1B8'],'Der Energiebogen als Obsidian-Gold-Nachtversion, rundum gezeichnet. Dunkle Wurfarme mit goldenen Linien; die Sehne läuft tangential hinter den gelagerten Umlenkrollen, der Pfeil liegt mit der Nocke auf der Sehne.','Geschwungene Wurfarme · gelagerte Umlenkrollen mit Achse · Griffstück mit Pfeilauflage'),
}
for n in sys.argv[1:]:
    name,nick,col,pill,pal,desc,form=INFO[n]
    m,cen=getattr(dmodels,'d'+n)()
    h=card(m,cen,n,name,f'VARIANTE D · „{nick}“ · ALLE PERSPEKTIVEN, GEZEICHNET',col,pill,desc,pal,form,'d'+n)
    open(O+f'D3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_d{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
