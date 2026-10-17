from cepaths import E3D,OUT
import sys,importlib,subprocess
sys.path.insert(0,E3D+'')
import fgen,gsight
from views import card
P=OUT+'/'
for n in [a for a in sys.argv[1:] if a!='noshot']:
    mod=importlib.import_module('g'+n);I=mod.INFO
    importlib.reload(mod)
    items2d=[it for it in mod.ITEMS if it.get('svg',True)]
    b=gsight.board_fgen(fgen,I,items2d)
    k=str(int(n))
    b=b.replace(f'f{k}Grid',f'g{k}Grid').replace(f'f{k}Glow',f'g{k}Glow').replace(' Variante F</title>',' Variante G</title>').replace('VARIANTE F · „','VARIANTE G · „')
    assert 'Variante F' not in b and 'VARIANTE F' not in b
    open(P+f'G{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_g{n}b.html','w').write(b.replace('<script src="./support.js"></script>',''))
    if 'noshot' not in sys.argv:subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_g{n}b.html',f'{E3D}/prev_g{n}b.png','1200','780'])
    m=fgen.model(mod.ITEMS)
    assert len(m.parts)==len(mod.ITEMS),(len(m.parts),len(mod.ITEMS))
    for it,Pt in zip(mod.ITEMS,m.parts):
        if it.get('L'):Pt['label']=it['L']
        if it.get('bias'):Pt['bias']=it['bias']
        if it.get('S'):Pt['sight']=True
    h=card(m,I['center'],I['num'],I['name'],f'VARIANTE G · „{I["nick"]}“ · KONZEPTBLATT',I['col'],I['pill'],I['desc'],I['pal'],I['form'],'g'+n)
    open(P+f'G3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_g{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if 'noshot' not in sys.argv:subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_g{n}.html',f'{E3D}/prev_g{n}.png','2400','1560'])
    print('ok',n)
