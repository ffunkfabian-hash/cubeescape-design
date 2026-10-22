from fontcss import FONT_CSS
from cepaths import E3D,OUT
import math,sys
sys.path.insert(0,E3D+'')
from eng import Model,roundpoly,circ,lum,OL,area
import ext
def convex(p):
    s=None
    for i in range(len(p)):
        a,b,c=p[i],p[(i+1)%len(p)],p[(i+2)%len(p)]
        cr=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
        if abs(cr)<1e-6:continue
        if s is None:s=cr>0
        elif (cr>0)!=s:return False
    return True
def P(pts):return ' '.join('%.1f,%.1f'%p for p in pts)
def zfront(it):
    t=it['t']
    if t=='poly':return it['z'][1]
    if t in('cyl','frustum'):return it.get('zc',0)+max(it['R'],it.get('R1',0))
    if t=='torus':return it['R']+it['rt']
    if t=='sphere':return it['R']
def svg_side(items,fid):
    o=[]
    order=sorted(range(len(items)),key=lambda i:(zfront(items[i]),i))
    for i in order:
        it=items[i];t=it['t'];c=it['c'];e=it.get('e',False);s=[]
        if t=='poly':
            pts=roundpoly(it['p'],it.get('r',0)) if it.get('r') else it['p']
            s.append(f'<polygon points="{P(pts)}" fill="{c}" stroke="{OL}" stroke-width="3" stroke-linejoin="round"/>')
            for d in it.get('d',[]):
                dp=roundpoly(d[0],d[3]) if len(d)>3 and d[3] else d[0]
                s.append(f'<polygon points="{P(dp)}" fill="{d[1]}" stroke="{OL}" stroke-width="2" stroke-linejoin="round"/>')
        elif t=='cyl':
            x0,x1=it['x'];cy=it['y'];R=it['R']
            s.append(f'<rect x="{x0}" y="{cy-R}" width="{x1-x0}" height="{2*R}" rx="{min(R*0.3,6):.1f}" fill="{c}"/>')
            if not e:
                s.append(f'<rect x="{x0}" y="{cy-R*0.72:.1f}" width="{x1-x0}" height="{R*0.42:.1f}" fill="{lum(c,1.25)}"/>')
                s.append(f'<rect x="{x0}" y="{cy+R*0.35:.1f}" width="{x1-x0}" height="{R*0.65:.1f}" fill="{lum(c,0.7)}"/>')
            s.append(f'<rect x="{x0}" y="{cy-R}" width="{x1-x0}" height="{2*R}" rx="{min(R*0.3,6):.1f}" fill="none" stroke="{OL}" stroke-width="3"/>')
        elif t=='frustum':
            x0,x1=it['x'];cy=it['y'];R0=it['R'];R1=it['R1']
            pts=[(x0,cy-R0),(x1,cy-R1),(x1,cy+R1),(x0,cy+R0)]
            s.append(f'<polygon points="{P(pts)}" fill="{c}" stroke="{OL}" stroke-width="3" stroke-linejoin="round"/>')
        elif t=='torus':
            x=it['x'];cy=it['y'];R=it['R'];rt=it['rt']
            s.append(f'<rect x="{x-rt}" y="{cy-R-rt}" width="{2*rt}" height="{2*(R+rt)}" rx="{rt}" fill="{c}" stroke="{OL}" stroke-width="3"/>')
        elif t=='sphere':
            x,y,_=it['p'];R=it['R']
            s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{c}" stroke="{OL}" stroke-width="3"/>')
            s.append(f'<circle cx="{x-R*0.35:.1f}" cy="{y-R*0.35:.1f}" r="{R*0.22:.1f}" fill="#FFFFFF" opacity="0.6"/>')
        if e:o.append(f'<g filter="url(#{fid}Glow)" opacity="0.7">'+''.join(x.replace(f'stroke="{OL}"','stroke="none"') for x in s[:1])+'</g>')
        o+=s
    return '\n'.join(o)
def model(items):
    m=Model()
    for it in items:
        t=it['t'];c=it['c'];e=it.get('e',False)
        if t=='poly':
            assert convex(it['p']),('nicht konvex',it['p'])
            z0,z1=it['z'];assert abs(z0+z1)<1e-6 or not it.get('d')
            m.prism(it['p'],c,z0,z1,r=it.get('r',0),emit=e)
            for d in it.get('d',[]):
                dp=roundpoly(d[0],d[3]) if len(d)>3 and d[3] else d[0]
                m.decal('z+',z1,dp,d[1],emit=d[2])
            for d in it.get('xd',[]):  # Aufkleber auf der Vorderflaeche (x+)
                m.decal('x+',d[0],d[1],d[2],emit=d[3],both=False)
        elif t=='cyl':
            m.cyl(it['x'][0],it['x'][1],it['y'],it.get('zc',0),it['R'],c,n=it.get('n',24),emit=e)
            for r,cc,ee in it.get('cap',[]):m.decal('x+',it['x'][1]+0.3*(ee),circ(it['y'],it.get('zc',0),r),cc,emit=ee,both=False)
            for (yy,zz,r,cc,ee) in it.get('ends',[]):
                m.decal('x+',it['x'][1],circ(yy,zz,r,14),cc,emit=ee,both=False)
                m.decal('x-',it['x'][0],circ(yy,zz,r,14),cc,emit=ee,both=False)
        elif t=='frustum':
            ext.frustum(m,it['x'][0],it['x'][1],it['y'],it.get('zc',0),it['R'],it['R1'],c,emit=e)
            for r,cc,ee in it.get('cap',[]):m.decal('x+',it['x'][1]+0.3*(ee),circ(it['y'],0,r),cc,emit=ee,both=False)
        elif t=='torus':
            n,k=40,10;xc,cy,R,rt=it['x'],it['y'],it['R'],it['rt'];faces=[]
            for i in range(n):
                for j in range(k):
                    def Q(a,b):
                        A=2*math.pi*a/n;B=2*math.pi*b/k;rr=R+rt*math.cos(B)
                        return (xc+rt*math.sin(B),cy+rr*math.sin(A),rr*math.cos(A))
                    faces.append([Q(i,j),Q(i+1,j),Q(i+1,j+1),Q(i,j+1)])
            ext.mesh(m,faces,c,emit=e,soft=set(range(len(faces))))
            # Normalen nach aussen vom Rohrmittelpunkt korrigieren
            for f,(i,j) in zip(m.parts[-1]['F'],[(i,j) for i in range(n) for j in range(k)]):
                A=2*math.pi*(i+.5)/n;B=2*math.pi*(j+.5)/k
                f['n']=(math.sin(B),math.cos(B)*math.sin(A),math.cos(B)*math.cos(A))
        elif t=='sphere':
            ext.sphere(m,it['p'],it['R'],c,emit=e,n=it.get('n',18))
    return m
TPL_HEAD='''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{num} {name} Variante F</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT_CSS}
<style>body{{margin:0}}</style>
</helmet>
<div style="width: 1200px; height: 780px; box-sizing: border-box; padding: 40px 48px; background: #0E1622; color: #E6ECF2; font-family: Barlow, sans-serif; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; justify-content: space-between; align-items: center">
<div style="display: flex; align-items: center; gap: 22px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 64px; font-weight: 700; line-height: 1; color: {col}">{num}</span>
<div style="display: flex; flex-direction: column; gap: 4px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 36px; font-weight: 700; letter-spacing: 3px; line-height: 1.1">{NAME}</span>
<span style="font-size: 15px; letter-spacing: 4px; color: #8FA0B3">VARIANTE F · „{nick}“</span>
</div>
</div>
<span style="padding: 10px 20px; border: 1px solid {col}; border-radius: 999px; color: {col}; font-family: 'Chakra Petch', sans-serif; font-size: 15px; font-weight: 600; letter-spacing: 3px">{pill}</span>
</div>
<div style="flex: 1; min-height: 0; display: flex; gap: 32px">
<div style="flex: 1; min-width: 0; border-radius: 12px; overflow: hidden; border: 1px solid #22314A; background: #111A27">
<svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: 100%; display: block" role="img" aria-label="{alt}">
<defs>
<pattern id="{fid}Grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1A2636" stroke-width="1"/></pattern>
<filter id="{fid}Glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<rect x="-200" y="-200" width="1200" height="1000" fill="#111A27"/>
<rect x="-200" y="-200" width="1200" height="1000" fill="url(#{fid}Grid)"/>
<ellipse cx="{shx}" cy="{shy}" rx="{shrx}" ry="16" fill="#000000" opacity="0.4"/>
{body}
</svg>
</div>
<div style="width: 300px; flex-shrink: 0; display: flex; flex-direction: column; gap: 24px">
<p style="margin: 0; font-size: 17px; line-height: 1.5; color: #C7D1DC">{desc}</p>
<div style="display: flex; flex-direction: column; gap: 10px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 13px; letter-spacing: 3px; color: #8FA0B3">FARBPALETTE</span>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px">
{pal}
</div>
</div>
<div style="display: flex; flex-direction: column; gap: 8px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 13px; letter-spacing: 3px; color: #8FA0B3">FORM</span>
<span style="font-size: 16px; line-height: 1.45">{form}</span>
</div>
</div>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1200,"height":780}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
def bbox(items):
    xs=[];ys=[]
    for it in items:
        t=it['t']
        if t=='poly':xs+=[p[0] for p in it['p']];ys+=[p[1] for p in it['p']]
        elif t in('cyl','frustum'):R=max(it['R'],it.get('R1',0));xs+=list(it['x']);ys+=[it['y']-R,it['y']+R]
        elif t=='torus':xs+=[it['x']-it['rt'],it['x']+it['rt']];ys+=[it['y']-it['R']-it['rt'],it['y']+it['R']+it['rt']]
        elif t=='sphere':x,y,_=it['p'];xs+=[x-it['R'],x+it['R']];ys+=[y-it['R'],y+it['R']]
    return min(xs),min(ys),max(xs),max(ys)
def board(info,items):
    fid='f'+str(int(info['num']))
    x0,y0,x1,y1=bbox(items);cx=(x0+x1)/2;cy=(y0+y1)/2
    W=max(x1-x0+120,(y1-y0+160)*760/600);H=W*600/760
    vb=f'{cx-W/2:.0f} {cy-H/2-15:.0f} {W:.0f} {H:.0f}'
    pal=''.join(f'<div style="display: flex; flex-direction: column; gap: 6px"><div style="height: 44px; border-radius: 6px; background: {c}"></div><span style="font-size: 12px; color: #8FA0B3">{c}</span></div>\n' for c in info['pal']).rstrip('\n')
    return TPL_HEAD.format(num=info['num'],name=info['name'],NAME=info['name'].upper(),nick=info['nick'],col=info['col'],pill=info['pill'],vb=vb,alt=info['alt'],fid=fid,
        shx=f'{cx:.0f}',shy=f'{y1+30:.0f}',shrx=f'{(x1-x0)*0.45:.0f}',body=svg_side(items,fid),desc=info['desc'],pal=pal,form=info['form'],FONT_CSS=FONT_CSS)
