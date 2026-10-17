from cepaths import E3D,OUT
import sys,subprocess,importlib,re
sys.path.insert(0,E3D+'')
from views import card
import flib,flabel,fsight
PROJ=OUT+'/'
args=[a for a in sys.argv[1:] if a!='noshot'];shot='noshot' not in sys.argv
for n in args:
    mod=importlib.import_module('f'+n);M=mod.META;sp=mod.spec()
    gun=[s for s in sp if not s.get('S')];sig=[s for s in sp if s.get('S')]
    fid='f'+str(int(n))
    b=flib.board2d(gun,M['num'],M['name'],M['vname'],M['col'],M['pill'],M['aria'],M['desc'],M['palette'],M['form'],fid,M.get('ty',0))
    if sig:
        tr=re.match(r'translate\(([-\d.]+),([-\d.]+)\) scale\(([-\d.]+)\)',flib.fit(gun));tx,ty,sc=map(float,tr.groups())
        rail=[s for s in gun if s.get('label')=='Visierschiene'];rp=None
        if rail:
            x0,y0,x1,y1=flib.bbox(rail[:1]);rp=((x0+x1)/2,y0)
        b=fsight.inject(b,fsight.clusters_of(sig,flib.bbox,lambda g:flib.svg2d(g,fid)),rail=rp,to_vb=lambda p:(tx+sc*p[0],ty+sc*p[1]))
    open(PROJ+f'F{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_f{n}_2d.html','w').write(b.replace('<script src="./support.js"></script>',''))
    m=flabel.apply(flib.model(sp),sp)
    fsight.flag_parts(m,[bool(s.get('S')) for s in sp])
    h=card(m,M['center'],M['num'],M['name'],f"VARIANTE F · „{M['vname'].upper()}“ · KONZEPTBLATT",M['col'],M['pill'],M['desc3'],M['palette'],M['form'],'f'+n)
    open(PROJ+f'F3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_f{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if shot:
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_f{n}_2d.html',f'{E3D}/prev_f{n}_2d.png','1200','780'])
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_f{n}.html',f'{E3D}/prev_f{n}.png','2400','1560'])
