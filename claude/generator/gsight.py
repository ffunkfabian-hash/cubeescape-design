from cepaths import E3D,OUT
# Variante G: Visier-Markierung durchreichen und Visier separat im 2D-Board zeichnen
import re,math,sys
sys.path.insert(0,E3D+'')
from eng import roundpoly,OL
NOTE='VISIER · SEPARAT'
def S(s):
    """flib-Spec-Eintrag als Visierteil markieren"""
    s['sight']=True;return s
def mark(m,entries,key):
    assert len(m.parts)==len(entries),(len(m.parts),len(entries))
    for P,e in zip(m.parts,entries):
        if e.get(key):P['sight']=True
    return m
def _P(pts):return ' '.join('%.1f,%.1f'%p for p in pts)
# ---------- Geister-Umriss (Position des Visiers auf der Waffe)
def ghost_fgen(items):
    o=[]
    for it in items:
        t=it['t']
        if t=='poly':
            pts=roundpoly(it['p'],it.get('r',0)) if it.get('r') else it['p'];o.append(f'<polygon points="{_P(pts)}"/>')
        elif t=='cyl':x0,x1=it['x'];R=it['R'];o.append(f'<rect x="{x0}" y="{it["y"]-R}" width="{x1-x0}" height="{2*R}" rx="3"/>')
        elif t=='frustum':x0,x1=it['x'];a,b=it['R'],it['R1'];cy=it['y'];o.append(f'<polygon points="{x0},{cy-a} {x1},{cy-b} {x1},{cy+b} {x0},{cy+a}"/>')
        elif t=='sphere':x,y,_=it['p'];o.append(f'<circle cx="{x}" cy="{y}" r="{it["R"]}"/>')
    return '<g fill="none" stroke="#9FB3C8" stroke-width="2" stroke-dasharray="6 5" opacity="0.85">'+''.join(o)+'</g>'
def ghost_flib(spec):
    o=[]
    for s in spec:
        if s['k']=='prism':
            pr=roundpoly(s['prof'],s['r']) if s['r'] else s['prof'];o.append(f'<polygon points="{_P(pr)}"/>')
        elif s['k']=='cyl':o.append(f'<rect x="{s["x0"]}" y="{s["cy"]-s["R"]}" width="{s["x1"]-s["x0"]}" height="{2*s["R"]}" rx="3"/>')
        else:o.append(f'<polygon points="{s["x0"]},{s["cy"]-s["R0"]} {s["x1"]},{s["cy"]-s["R1"]} {s["x1"]},{s["cy"]+s["R1"]} {s["x0"]},{s["cy"]+s["R0"]}"/>')
    return '<g fill="none" stroke="#9FB3C8" stroke-width="2" stroke-dasharray="6 5" opacity="0.85">'+''.join(o)+'</g>'
def inset(body,sx0,sy0,sx1,sy1,bx,by,k,label_px=15):
    """Kasten mit separat gezeichnetem Visier; (bx,by) linke obere Ecke im Zielsystem, k Maßstab"""
    w=(sx1-sx0)*k+40;h=(sy1-sy0)*k+58
    return (f'<g><rect x="{bx:.1f}" y="{by:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="#0E1622" stroke="#4A6080" stroke-width="1.5" stroke-dasharray="7 6"/>'
            f'<text x="{bx+14:.1f}" y="{by+24:.1f}" font-family="Chakra Petch, sans-serif" font-size="{label_px}" font-weight="600" letter-spacing="2.5" fill="#C7D1DC">{NOTE}</text>'
            f'<g transform="translate({bx+20-sx0*k:.1f},{by+42-sy0*k:.1f}) scale({k:.3f})">{body}</g></g>'),w,h

def clusters(items,bboxf,gap=40):
    bs=sorted([(bboxf([it]),it) for it in items],key=lambda t:t[0][0])
    out=[]
    for b,it in bs:
        if out and b[0]<=out[-1][0][2]+gap:
            ob=out[-1][0];out[-1][0]=(min(ob[0],b[0]),min(ob[1],b[1]),max(ob[2],b[2]),max(ob[3],b[3]));out[-1][1].append(it)
        else:out.append([b,[it]])
    return out
def inset2(sig,bboxf,drawf,ref_w,maxk=2.0,bx=0,by=0,label_px=15):
    """Visierteile gruppiert nebeneinander; Maßstab k relativ zur Waffe (bis 2:1 bei kleinen Visieren)"""
    cl=clusters(sig,bboxf)
    tw=sum(b[2]-b[0] for b,_ in cl);th=max(b[3]-b[1] for b,_ in cl)
    k=min(maxk,0.42*ref_w/max(tw,1),110/max(th,1)*1.0 if th*maxk>110 else maxk)
    k=max(k,0.35)
    gapx=26
    lab=NOTE+(f' · M {k:.1f}:1'.replace('.',',') if abs(k-1)>0.15 else ' · M 1:1')
    w=max(tw*k+gapx*(len(cl)-1)+40,len(lab)*label_px*0.78+30);h=th*k+64
    o=[f'<rect x="{bx:.1f}" y="{by:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="#0E1622" stroke="#4A6080" stroke-width="1.5" stroke-dasharray="7 6"/>',
       f'<text x="{bx+14:.1f}" y="{by+24:.1f}" font-family="Chakra Petch, sans-serif" font-size="{label_px}" font-weight="600" letter-spacing="2.5" fill="#C7D1DC">{lab}</text>']
    x=bx+20
    for b,its in cl:
        cw=(b[2]-b[0])*k;ch=(b[3]-b[1])*k
        y=by+44+(th*k-ch)/2
        o.append(f'<g transform="translate({x-b[0]*k:.1f},{y-b[1]*k:.1f}) scale({k:.3f})">{drawf(its)}</g>')
        x+=cw+gapx
    return '<g>'+''.join(o)+'</g>',w,h,k
def board_fgen(fgen,info,items):
    gun=[it for it in items if not it.get('S')];sig=[it for it in items if it.get('S')]
    if not sig:return fgen.board(info,gun)
    info=dict(info);info['form']=info['form']+' · Visier separat (modular auf Schiene, gestrichelt: Einbauposition)'
    b=fgen.board(info,gun)
    fid='f'+str(int(info['num']))
    gx0,gy0,gx1,gy1=fgen.bbox(gun)
    dr=lambda its:fgen.svg_side(its,fid)
    ins,w,h,k=inset2(sig,fgen.bbox,dr,gx1-gx0)
    sy0=fgen.bbox(sig)[1]
    bx=gx1-w;by=min(gy0,sy0)-h-28
    ins,w,h,k=inset2(sig,fgen.bbox,dr,gx1-gx0,bx=bx,by=by)
    x0=min(gx0,bx);y0=by;x1=gx1;y1=gy1
    cx=(x0+x1)/2;cy=(y0+y1)/2
    W=max(x1-x0+110,(y1-y0+120)*760/600);H=W*600/760
    vb=f'{cx-W/2:.0f} {cy-H/2+10:.0f} {W:.0f} {H:.0f}'
    b=re.sub(r'<svg viewBox="[^"]+"',f'<svg viewBox="{vb}"',b,count=1)
    b=b.replace('</svg>',ghost_fgen(sig)+ins+'\n</svg>',1)
    return b
def board_flib(flib,spec,*a,**kw):
    gun=[s for s in spec if not s.get('sight')];sig=[s for s in spec if s.get('sight')]
    if not sig:return flib.board2d(spec,*a,**kw)
    a=list(a);a[8]=a[8]+' · Visier separat (modular, gestrichelt: Einbauposition)'
    b=flib.board2d(gun,*a,**kw)
    fid=a[9]
    gx0,gy0,gx1,gy1=flib.bbox(gun);sx0,sy0,sx1,sy1=flib.bbox(sig)
    dx,dy=gx1-gx0,gy1-gy0
    dr=lambda its:flib.svg2d(its,fid)
    sc=min(640/dx,420/dy,1.25)
    for _ in range(3):
        _,w,h,k=inset2(sig,flib.bbox,dr,dx)
        ih=h*sc  # Kasten skaliert mit der Waffe
        top=16+ih+18;avail=548-top
        sc=min(640/dx,avail/dy,1.25)
    cxg,cyg=(gx0+gx1)/2,(gy0+gy1)/2;ty=top+avail/2
    tr=f'translate({380-cxg*sc:.1f},{ty-cyg*sc:.1f}) scale({sc:.3f})'
    b=re.sub(r'<g transform="translate\([^)]*\) scale\([^)]*\)">',f'<g transform="{tr}">',b,count=1)
    b=re.sub(r'<ellipse cx="380" cy="520"',f'<ellipse cx="380" cy="{ty+dy*sc/2+22:.0f}"',b,count=1)
    ins,w,h,k=inset2(sig,flib.bbox,dr,dx,bx=0,by=0,label_px=15/sc)
    bxv=min(744,380+dx*sc/2)-w*sc;byv=16
    ins=f'<g transform="translate({bxv:.1f},{byv:.1f}) scale({sc:.3f})">'+ins+'</g>'
    gh=f'<g transform="{tr}">'+ghost_flib(sig)+'</g>'
    b=b.replace('</svg>',gh+ins+'\n</svg>',1)
    return b
