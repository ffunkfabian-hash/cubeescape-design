from cepaths import E3D,OUT
import sys,importlib,subprocess
sys.path.insert(0,E3D+'')
import fgen,fsight
from views import card
P=OUT+'/'
args=[a for a in sys.argv[1:] if a!='noshot'];shot='noshot' not in sys.argv
for n in args:
    mod=importlib.import_module('f'+n);I=mod.INFO
    gun2d=[it for it in mod.ITEMS if it.get('svg',True) and not it.get('S')]
    sig2d=[it for it in mod.ITEMS if it.get('svg',True) and it.get('S')]
    b=fgen.board(I,gun2d)
    if sig2d:
        rail=[it for it in gun2d if it.get('L') in ('Visierschiene','Tragebügel')]
        rp=None
        if rail:
            x0,y0,x1,y1=fgen.bbox(rail[:1]);rp=((x0+x1)/2,y0)
        b=fsight.inject(b,fsight.clusters_of(sig2d,fgen.bbox,lambda g:fgen.svg_side(g,'f'+str(int(n)))),rail=rp)
    open(P+f'F{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_f{n}b.html','w').write(b.replace('<script src="./support.js"></script>',''))
    if shot:subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_f{n}b.html',f'{E3D}/prev_f{n}b.png','1200','780'])
    m=fgen.model(mod.ITEMS)
    assert len(m.parts)==len(mod.ITEMS),(len(m.parts),len(mod.ITEMS))
    for it,Pt in zip(mod.ITEMS,m.parts):
        if it.get('L'):Pt['label']=it['L']
        if it.get('bias'):Pt['bias']=it['bias']
        if it.get('S'):Pt['sight']=True
    h=card(m,I['center'],I['num'],I['name'],f'VARIANTE F · „{I["nick"]}“ · KONZEPTBLATT',I['col'],I['pill'],I['desc'],I['pal'],I['form'],'f'+n)
    open(P+f'F3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_f{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if shot:subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_f{n}.html',f'{E3D}/prev_f{n}.png','2400','1560'])
