from cepaths import E3D,OUT
import sys,re,os,ast,importlib,html as _h
sys.path.insert(0,E3D+'')
from eng import *
P=OUT+'/'
def texts(n):
    if n=='01':
        src=open(E3D+'/build_v01.py').read()
        strs=re.findall(r"'([^']{40,})'",src)
        d=[x for x in strs if x.startswith('Die Doppelkammer')][0];f=[x for x in strs if x.startswith('Zwei Läufe')][0]
        return d,f
    if n in ('02','03','04','05'):
        src=open(E3D+'/build_c25.py').read();src=src[src.index('INFO='):src.index('n=sys.argv')]
        ns={};exec(src,ns);c,name,nick,col,pill,pal,desc,form=ns['INFO'][n];return desc,form
    mod=importlib.import_module('c'+n);return mod.META['desc'],mod.META['form']
def model(n):
    if n=='01':
        import v01m;return v01m.model(),(400,250,0)
    mod=importlib.import_module('c'+n)
    c=getattr(mod,'CENTER',None)
    if c is None:
        src=open(E3D+'/build_c25.py').read();src=src[src.index('INFO='):src.index('n=sys.argv')]
        ns={};exec(src,ns);c=ns['INFO'][n][0]
    return mod.model(),c
for n in sys.argv[1:]:
    fn=P+f'V{n}.dc.html';h=open(fn).read()
    bak=f'{E3D}/V{n}_old.dc.html'
    if not os.path.exists(bak):open(bak,'w').write(h)
    m,c=model(n);g,s=split_sight(m)
    W,H=760,600
    ew,eh=extent(g,0,0,c);sc=min((W-60)/ew,(H-170)/eh)
    gv=svgview(g,0,0,c,W,H-130,sc,ow=3.0)
    sv=''
    if s.parts:
        bw,bh=(300 if n=='09' else 230),124
        e1,e2=extent(s,0,0,c);ss=min((bw-30)/e1,(bh-40)/e2,sc*2.6)
        sv=svgview(s,0,0,c,bw,bh-16,ss,ow=2.4,shadow=False)
        sv=(f'<g transform="translate({W-bw-14},12)"><rect width="{bw}" height="{bh}" rx="10" fill="#0E1622" stroke="#2E405A" stroke-width="1.5" stroke-dasharray="6 5"/>'
            f'<g transform="translate(0,16)">{sv}</g><text x="12" y="20" font-family="Chakra Petch, sans-serif" font-size="13" font-weight="600" letter-spacing="2" fill="#8FA0B3">{'VISIER · SEPARAT · SEITLICH LINKS' if n=='09' else 'VISIER · SEPARAT'}</text></g>')
    aria=f"Variante C, Seitenansicht aus dem 3D-Modell, Waffe ohne Visier; das Visier ist oben rechts separat gezeichnet"
    i=h.index('<svg viewBox="0 0 760 600"');j=h.index('</svg>',i)+6
    new=(f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: 100%; display: block" role="img" aria-label="{aria}">'
         f'<defs><pattern id="v{int(n)}Grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1A2636" stroke-width="1"/></pattern></defs>'
         f'<rect width="{W}" height="{H}" fill="#111A27"/><rect width="{W}" height="{H}" fill="url(#v{int(n)}Grid)"/>'
         f'<g transform="translate(0,130)">{gv}</g>{sv}</svg>')
    h=h[:i]+new+h[j:]
    desc,form=texts(n)
    h=re.sub(r'(<p style="margin: 0; font-size: 17px[^>]*>)(.*?)(</p>)',lambda mm:mm.group(1)+_h.escape(desc,quote=False)+mm.group(3),h,count=1,flags=re.S)
    h=re.sub(r'(>FORM</span>\s*<span[^>]*>)(.*?)(</span>)',lambda mm:mm.group(1)+_h.escape(form,quote=False)+mm.group(3),h,count=1,flags=re.S)
    h=h.replace('· DRAUFSICHT','· SEITENANSICHT')
    open(fn,'w').write(h)
    open(f'{E3D}/chk/V{n}.html','w').write(h.replace('<script src="./support.js"></script>',''))
    print('V'+n,'ok',len(h)//1024,'KB')
