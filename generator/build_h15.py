from cepaths import E3D,OUT
import sys,importlib,subprocess
sys.path.insert(0,E3D+'')
import fgen
from views import card
P=OUT+'/'
def sight_inset(b,gun,sight,fid):
    """Visier separat in die rechte obere Ecke der Zeichenflaeche (gleiches viewBox wie fgen.board)"""
    if not sight:return b
    x0,y0,x1,y1=fgen.bbox(gun);cx=(x0+x1)/2;cy=(y0+y1)/2
    W=max(x1-x0+120,(y1-y0+160)*760/600);H=W*600/760
    vx,vy=cx-W/2,cy-H/2-15
    sx0,sy0,sx1,sy1=fgen.bbox(sight)
    bw,bh=W*0.30,H*0.26
    sc=min((bw-30)/(sx1-sx0),(bh-50)/(sy1-sy0),1.6)
    boxes=[fgen.bbox([it]) for it in gun]
    def ov(ox,oy):
        a=0
        for bx0,by0,bx1,by1 in boxes:
            w=min(bx1,ox+bw)-max(bx0,ox);h=min(by1,oy+bh)-max(by0,oy)
            if w>0 and h>0:a+=w*h
        return a
    cands=[(vx+W-bw-12,vy+12),(vx+W-bw-12,vy+H-bh-12),(vx+12,vy+12),(vx+12,vy+H-bh-12)]
    ox,oy=min(cands,key=lambda c:(ov(*c),cands.index(c)))
    tx=ox+bw/2-(sx0+sx1)/2*sc;ty=oy+30+(bh-30)/2-(sy0+sy1)/2*sc
    fs=W/760*13
    g=(f'<g><rect x="{ox:.1f}" y="{oy:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{fs*0.8:.1f}" fill="#0E1622" stroke="#4A6080" stroke-width="{W/760*1.4:.2f}" stroke-dasharray="{fs*0.5:.1f} {fs*0.4:.1f}"/>'
       f'<text x="{ox+fs*0.9:.1f}" y="{oy+fs*1.6:.1f}" font-family="Chakra Petch, sans-serif" font-size="{fs:.1f}" font-weight="600" letter-spacing="{fs*0.18:.1f}" fill="#8FA0B3">VISIER · SEPARAT</text>'
       f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.3f})">{fgen.svg_side(sight,fid)}</g></g>')
    i=b.index('</svg>')
    return b[:i]+g+'\n'+b[i:]
for n in sys.argv[1:]:
    if n=='noshot':continue
    mod=importlib.import_module('h'+n);importlib.reload(mod);I=mod.INFO
    k=str(int(n))
    gun=[it for it in mod.ITEMS if it.get('svg',True) and not it.get('S')]
    sight=[it for it in mod.ITEMS if it.get('svg',True) and it.get('S')]
    b=fgen.board(I,gun)
    b=sight_inset(b,gun,sight,'f'+k)
    b=b.replace(f'f{k}Grid',f'h{k}Grid').replace(f'f{k}Glow',f'h{k}Glow').replace(' Variante F</title>',' Variante H</title>').replace('VARIANTE F · „','VARIANTE H · „')
    assert 'Variante F' not in b and 'VARIANTE F' not in b
    open(P+f'H{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_h{n}b.html','w').write(b.replace('<script src="./support.js"></script>',''))
    m=fgen.model(mod.ITEMS)
    assert len(m.parts)==len(mod.ITEMS),(len(m.parts),len(mod.ITEMS))
    for it,Pt in zip(mod.ITEMS,m.parts):
        if it.get('L'):Pt['label']=it['L']
        if it.get('bias'):Pt['bias']=it['bias']
        if it.get('S'):Pt['sight']=True
    labs={it['L'] for it in mod.ITEMS if it.get('L') and not it.get('S')}
    assert len(labs)<=8,('zu viele Labels',labs)
    h=card(m,I['center'],I['num'],I['name'],f'VARIANTE H · „{I["nick"]}“ · KONZEPTBLATT',I['col'],I['pill'],I['desc'],I['pal'],I['form'],'h'+n)
    open(P+f'H3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_h{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if 'noshot' not in sys.argv:
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_h{n}b.html',f'{E3D}/prev_h{n}b.png','1200','780'])
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_h{n}.html',f'{E3D}/prev_h{n}.png','2400','1560'])
    print('ok',n,sorted(labs))
