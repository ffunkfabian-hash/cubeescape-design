from cepaths import E3D,OUT
import sys,subprocess,importlib
sys.path.insert(0,E3D+'')
from views import card
import flib,hxlib as hlib
from eng import split_sight,svgview,extent
PROJ=OUT+'/'
args=[a for a in sys.argv[1:] if a not in('noshot','split')]
for n in args:
    mod=importlib.import_module('h'+n);importlib.reload(mod);M=mod.META;sp=mod.spec()
    b=hlib.board2d(sp,M['num'],M['name'],M['vname'],M['col'],M['pill'],M['aria'],M['desc'],M['palette'],M['form'],'h'+str(int(n)))
    if M.get('snote'):b=b.replace('VISIER · SEPARAT</text>','VISIER · SEPARAT</text>'+f'<text x="552" y="142" font-family="Barlow, sans-serif" font-size="12" fill="#C7D1DC">{M["snote"]}</text>',1)
    open(PROJ+f'H{n}.dc.html','w').write(b)
    open(f'{E3D}/prev_h{n}_2d.html','w').write(b.replace('<script src="./support.js"></script>',''))
    m=hlib.apply(flib.model(sp),sp)
    h=card(m,M['center'],M['num'],M['name'],f"VARIANTE H · „{M['vname'].upper()}“ · KONZEPTBLATT",M['col'],M['pill'],M['desc3'],M['palette'],M['form'],'h'+n)
    open(PROJ+f'H3D{n}.dc.html','w').write(h)
    open(f'{E3D}/prev_h{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    if 'split' in sys.argv:
        g,s=split_sight(m);c=M['center']
        out=''
        for mm,(yw,pt),lab in ((g,(-45,35.264),'Waffe ohne Visier · Isometrie'),(g,(0,0),'Waffe ohne Visier · links'),(s,(-45,35.264),'Visier separat')):
            if not mm.parts:continue
            ew,eh=extent(mm,yw,pt,c);sc=min(1100/ew,600/eh,4)
            out+=f'<div style="color:#ccc;font:16px sans-serif">{lab}</div><svg width="1200" height="700" style="background:#111A27;display:block">{svgview(mm,yw,pt,c,1200,700,sc,ow=3)}</svg>'
        open(f'{E3D}/prev_h{n}_split.html','w').write(f'<html><body style="margin:0;background:#0E1622">{out}</body></html>')
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_h{n}_split.html',f'{E3D}/prev_h{n}_split.png','1200','2200'])
    if 'noshot' not in sys.argv:
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_h{n}_2d.html',f'{E3D}/prev_h{n}_2d.png','1200','780'])
        subprocess.run(['python3',E3D+'/shot.py',f'{E3D}/prev_h{n}.html',f'{E3D}/prev_h{n}.png','2400','1560'])
