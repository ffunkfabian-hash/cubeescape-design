from cepaths import E3D,OUT
import math
from eng import *
import ext
OLc='#0A0A0D'
def P(prof,col,z0,z1,r=0,emit=False,dec=(),xdec=(),smooth=False):
    return dict(k='prism',prof=prof,col=col,z0=z0,z1=z1,r=r,emit=emit,dec=list(dec),xdec=list(xdec),smooth=smooth)
def C(x0,x1,cy,R,col,n=24,emit=False,cap=(),cz=0):
    return dict(k='cyl',x0=x0,x1=x1,cy=cy,R=R,col=col,n=n,emit=emit,cap=list(cap),z1=R+cz,cz=cz)
def F(x0,x1,cy,R0,R1,col,emit=False,cz=0):
    return dict(k='frus',x0=x0,x1=x1,cy=cy,R0=R0,R1=R1,col=col,emit=emit,z1=max(R0,R1)+cz,cz=cz)
def D(pts,col,emit=False):return (pts,col,emit)
def model(spec):
    m=Model()
    for s in spec:
        if s['k']=='prism':
            m.prism(s['prof'],s['col'],s['z0'],s['z1'],r=s['r'],emit=s['emit'],smooth=s.get('smooth',False))
            for pts,c,e in s['dec']:
                m.decal('z+',s['z1'],pts,c,emit=e,both=False)
                if s['z0']==-s['z1']:m.decal('z-',s['z0'],pts,c,emit=e,both=False)
            for plane,val,pts,c,e in s['xdec']:m.decal(plane,val,pts,c,emit=e,both=False)
        elif s['k']=='cyl':
            m.cyl(s['x0'],s['x1'],s['cy'],s.get('cz',0),s['R'],s['col'],n=s['n'],emit=s['emit'])
            for cy,cz,r,c,e in s['cap']:m.decal('x+',s['x1'],circ(cy,cz,r),c,emit=e,both=False)
        elif s['k']=='frus':
            ext.frustum(m,s['x0'],s['x1'],s['cy'],s.get('cz',0),s['R0'],s['R1'],s['col'],emit=s['emit'])
    return m
def bbox(spec):
    xs=[];ys=[]
    for s in spec:
        if s['k']=='prism':xs+=[p[0] for p in s['prof']];ys+=[p[1] for p in s['prof']]
        elif s['k']=='cyl':xs+=[s['x0'],s['x1']];ys+=[s['cy']-s['R'],s['cy']+s['R']]
        else:R=max(s['R0'],s['R1']);xs+=[s['x0'],s['x1']];ys+=[s['cy']-R,s['cy']+R]
    return min(xs),min(ys),max(xs),max(ys)
def fit(spec):
    x0,y0,x1,y1=bbox(spec);sc=min(640/(x1-x0),420/(y1-y0),1.25)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    return f'translate({380-cx*sc:.1f},{280-cy*sc:.1f}) scale({sc:.3f})'
def pts2(p):return ' '.join('%.1f,%.1f'%q for q in p)
def svg2d(spec,fid):
    out=[];order=sorted(range(len(spec)),key=lambda i:(spec[i]['z1'],i))
    for i in order:
        s=spec[i];g=[]
        if s['k']=='prism':
            pr=roundpoly(s['prof'],s['r']) if s['r'] else s['prof']
            if s['emit']:g.append(f'<polygon points="{pts2(pr)}" fill="{s["col"]}" filter="url(#{fid}Glow)" opacity="0.7"/>')
            g.append(f'<polygon points="{pts2(pr)}" fill="{s["col"]}" stroke="{OLc}" stroke-width="3" stroke-linejoin="round"/>')
            # Lichtkante oben
            for pts,c,e in s['dec']:
                if e:g.append(f'<polygon points="{pts2(pts)}" fill="{c}" filter="url(#{fid}Glow)" opacity="0.8"/>')
                g.append(f'<polygon points="{pts2(pts)}" fill="{c}" stroke="{OLc}" stroke-width="1.6" stroke-linejoin="round"/>')
        elif s['k']=='cyl':
            x0,x1,cy,R=s['x0'],s['x1'],s['cy'],s['R']
            if s['n']<12:R=R*math.cos(math.pi/s['n']) if s['n']%4 else R
            if s['emit']:g.append(f'<rect x="{x0}" y="{cy-R}" width="{x1-x0}" height="{2*R}" rx="{min(4,R/3):.1f}" fill="{s["col"]}" filter="url(#{fid}Glow)" opacity="0.7"/>')
            g.append(f'<rect x="{x0}" y="{cy-R:.1f}" width="{x1-x0}" height="{2*R:.1f}" rx="{min(4,R/3):.1f}" fill="{s["col"]}" stroke="{OLc}" stroke-width="3"/>')
            if not s['emit'] and R>5:g.append(f'<rect x="{x0+2}" y="{cy-R*0.62:.1f}" width="{x1-x0-4}" height="{R*0.28:.1f}" fill="{lum(s["col"],1.3)}" opacity="0.8"/>')
        else:
            x0,x1,cy,a,b=s['x0'],s['x1'],s['cy'],s['R0'],s['R1']
            g.append(f'<polygon points="{x0},{cy-a} {x1},{cy-b} {x1},{cy+b} {x0},{cy+a}" fill="{s["col"]}" stroke="{OLc}" stroke-width="3" stroke-linejoin="round"/>')
        out+=g
    return '\n'.join(out)
TPL=open(OUT+'/V06.dc.html').read()
def board2d(spec,num,name,vname,col,pill,aria,desc,palette,form,fid,ty=0):
    sw=''.join(f'<div style="display: flex; flex-direction: column; gap: 6px"><div style="height: 44px; border-radius: 6px; background: {c}"></div><span style="font-size: 12px; color: #8FA0B3">{c}</span></div>\n' for c in palette)
    svg=f'''<svg viewBox="0 0 760 600" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: 100%; display: block" role="img" aria-label="{aria}">
<defs>
<pattern id="{fid}Grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1A2636" stroke-width="1"/></pattern>
<filter id="{fid}Glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="760" height="600" fill="#111A27"/>
<rect width="760" height="600" fill="url(#{fid}Grid)"/>
<ellipse cx="380" cy="520" rx="300" ry="16" fill="#000000" opacity="0.4"/>
<g transform="{fit(spec)}">
{svg2d(spec,fid)}
</g>
</svg>'''
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{num} {name} Variante F</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}</style>
</helmet>
<div style="width: 1200px; height: 780px; box-sizing: border-box; padding: 40px 48px; background: #0E1622; color: #E6ECF2; font-family: Barlow, sans-serif; display: flex; flex-direction: column; gap: 24px">
<div style="display: flex; justify-content: space-between; align-items: center">
<div style="display: flex; align-items: center; gap: 22px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 64px; font-weight: 700; line-height: 1; color: {col}">{num}</span>
<div style="display: flex; flex-direction: column; gap: 4px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 36px; font-weight: 700; letter-spacing: 3px; line-height: 1.1">{name.upper()}</span>
<span style="font-size: 15px; letter-spacing: 4px; color: #8FA0B3">VARIANTE F · „{vname.upper()}“</span>
</div>
</div>
<span style="padding: 10px 20px; border: 1px solid {col}; border-radius: 999px; color: {col}; font-family: 'Chakra Petch', sans-serif; font-size: 15px; font-weight: 600; letter-spacing: 3px">{pill}</span>
</div>
<div style="flex: 1; min-height: 0; display: flex; gap: 32px">
<div style="flex: 1; min-width: 0; border-radius: 12px; overflow: hidden; border: 1px solid #22314A; background: #111A27">
{svg}
</div>
<div style="width: 300px; flex-shrink: 0; display: flex; flex-direction: column; gap: 24px">
<p style="margin: 0; font-size: 17px; line-height: 1.5; color: #C7D1DC">{desc}</p>
<div style="display: flex; flex-direction: column; gap: 10px">
<span style="font-family: 'Chakra Petch', sans-serif; font-size: 13px; letter-spacing: 3px; color: #8FA0B3">FARBPALETTE</span>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px">
{sw}</div>
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
