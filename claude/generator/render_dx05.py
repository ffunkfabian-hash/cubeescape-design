from cepaths import E3D,OUT
import sys,re
sys.path.insert(0,E3D+'')
import dmods
from eng import svgview,extent,split_sight
P=OUT+'/'
for fn,pal,alt,col in (('D05.dc.html',['#D6C6A0','#2E2A24','#F28C28','#FFD7A8'],'Scharfschützengewehr Variante D, neue Konstruktion in Sand und Solar-Orange, ohne Visier: Rahmenschaft, Pistolengriff mit Abzug, Magazin, Visierschiene, freier Lauf mit Mündungsbremse; Zielfernrohr separat in der Ecke','#F28C28'),
                   ('X05.dc.html',['#4A4E57','#1A1C20','#A855F7','#E9D5FF'],'Scharfschützengewehr Variante E, neue Konstruktion in Graphit und Void-Violett, ohne Visier: Rahmenschaft, Pistolengriff mit Abzug, Magazin, Visierschiene, freier Lauf mit Mündungsbremse; Zielfernrohr separat in der Ecke','#C084FC')):
    h=open(P+fn).read()
    m,c=dmods.d05(*pal);g,s=split_sight(m)
    W,H=800,560
    ew,eh=extent(g,0,0,c);sc=min((W-60)/ew,(H-170)/eh)
    v=svgview(g,0,0,c,W,H,sc,ow=3.0)
    v=v.replace('<image x="0" y="0"','<image x="0" y="40"',1).replace('<ellipse cx','<ellipse transform="translate(0,40)" cx',1)
    sw,shh=250,96
    ew2,eh2=extent(s,0,0,c);sc2=min((sw-30)/ew2,(shh-34)/eh2)
    v2=svgview(s,0,0,c,sw,shh,sc2,ow=2.0,shadow=False).replace('<image x="0" y="0"','<image x="0" y="14"',1)
    corner=(f'<g transform="translate(24,20)"><rect width="{sw}" height="{shh+20}" rx="12" fill="#0E1622" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 5"/>'
            f'<text x="14" y="22" font-family="Chakra Petch, sans-serif" font-size="14" font-weight="600" letter-spacing="2.5" fill="{col}">VISIER · SEPARAT</text>'
            f'<g transform="translate(0,14)">{v2}</g></g>')
    i=h.index('<svg viewBox="0 0 800 560"');j=h.index('</svg>',i)+6
    svg=f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: 100%; display: block" role="img" aria-label="{alt}">{v}{corner}</svg>'
    h=h[:i]+svg+h[j:]
    h=re.sub(r'(WAS SICH ÄNDERT</span>\s*<span[^>]*>)(.*?)(</span>)',r'\1Neu konstruiert nach dem Qualitäts-Masterprompt: Rahmenschaft, Griff mit Abzug, Magazin im Schacht, sichtbarer Lauf. Das Zielfernrohr ist separat gezeichnet und sitzt modular auf der Visierschiene.\3',h,flags=re.S)
    open(P+fn,'w').write(h)
    open(E3D+'/prev_'+fn.replace('.dc.html','.html'),'w').write(h.replace('<script src="./support.js"></script>',''))
