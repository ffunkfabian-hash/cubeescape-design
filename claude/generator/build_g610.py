from cepaths import E3D,OUT
import sys,subprocess,importlib
sys.path.insert(0,E3D+'')
from views import card
import flib,flabel,gsight
PROJ=OUT+'/'
args=[a for a in sys.argv[1:] if a!='noshot']
for n in args:
    mod=importlib.import_module('g'+n);importlib.reload(mod);M=mod.META;sp=mod.spec()
    b=gsight.board_flib(flib,sp,M['num'],M['name'],M['vname'],M['col'],M['pill'],M['aria'],M['desc'],M['palette'],M['form'],'g'+str(int(n)),M.get('ty',0))
    b=b.replace('Variante F</title>','Variante G</title>').replace('VARIANTE F · „','VARIANTE G · „')
    open(PROJ+f'G{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_g{n}_2d.html','w').write(b.replace('<script src="./support.js"></script>',''))
    h=card(gsight.mark(flabel.apply(flib.model(sp),sp),sp,'sight'),M['center'],M['num'],M['name'],f"VARIANTE G · „{M['vname'].upper()}“ · KONZEPTBLATT",M['col'],M['pill'],M['desc3'],M['palette'],M['form'],'g'+n)
    open(PROJ+f'G3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_g{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if 'noshot' not in sys.argv:
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_g{n}_2d.html',f'{E3D}/prev_g{n}_2d.png','1200','780'])
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_g{n}.html',f'{E3D}/prev_g{n}.png','2400','1560'])
