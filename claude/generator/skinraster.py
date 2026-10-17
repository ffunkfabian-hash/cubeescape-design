"""Skin-Muster im Raster (claude-0.3): malt die aufgelösten Lagen aus skins.resolve() im Objektraum.

Die Schattierungsstufe (eng.shadef, vier Stufen) jedes Bildpunkts wird aus seiner Helligkeit zurückgelesen, damit neue
Farben dieselbe Toon-Schattierung bekommen. Poliertes Gold/Chrom: eigene Tonleiter plus Glanzstreifen im Objektraum.
Kantenabnutzung: blankes Metall entlang harter Kanten, fleckig über ein Zellrauschen im Objektraum.
"""
import numpy as np
from scipy import ndimage
from eng import lum
from xlroles import _mix,_lum
import skins

LEVELS=(1.28,1.08,0.88,0.62)
def _rgb(c):c=c.lstrip('#');return np.array([int(c[i:i+2],16) for i in (0,2,4)],np.float32)
def tones(c,fin):
    """Farben für die Stufen hell, mittel, schattig, dunkel und Glanzstreifen"""
    if fin=='polished_gold':
        return [_mix(c,'#FFF4D0',0.35),c,_mix(c,'#5A3A08',0.45),_mix(c,'#2A1A04',0.72),_mix(c,'#FFFFFF',0.8)]
    if fin=='polished_chrome':
        return [_mix(c,'#FFFFFF',0.5),c,_mix(c,'#1C2128',0.5),_mix(c,'#1C2128',0.8),'#FFFFFF']
    if fin=='neon':
        return [_mix(c,'#FFFFFF',0.25)]*4+[_mix(c,'#FFFFFF',0.25)]
    return [lum(c,f) for f in LEVELS]+[lum(c,LEVELS[0])]
def _inpoly(X,Y,poly):
    c=np.zeros(X.shape,bool);n=len(poly)
    for i in range(n):
        (x0,y0),(x1,y1)=poly[i],poly[i-1]
        if y0==y1:continue
        hit=((y0>Y)!=(y1>Y))&(X<(x1-x0)*(Y-y0)/(y1-y0)+x0)
        c^=hit
    return c
def _hsh(t):return np.sin(t*12.9898)*43758.5453%1.0

def skin_texture(rs,colors):
    """rs: skins.resolve(), colors: skins.slot_colors() -> Textur-Funktion für raster.rasterview"""
    fr=rs['frame'];Hb=fr['hi'][1]-fr['lo'][1]
    def tex(col,pb,idb,decm,parts,SS,world=None,nrm=None,scale=1.0):
        h,w=pb.shape;n=len(parts)
        WX,WY,WZ=world
        valid=(pb>=0)&~decm
        pbc=np.where(pb>=0,pb,n)
        sk=np.array([P.get('_sk',-1) for P in parts]+[-1],np.int32);bi=sk[pbc];bi[~valid]=-1
        # Schattierungsstufe aus der Helligkeit
        Ls=np.full((n+1,4),-9.0,np.float32)
        for k,P in enumerate(parts):
            for j,f in enumerate(LEVELS):Ls[k,j]=_lum(lum(P['col'],f))*255
        Lp=col[...,0]*0.2126+col[...,1]*0.7152+col[...,2]*0.0722
        fidx=np.argmin(np.abs(Ls[pbc]-Lp[...,None]),axis=-1).astype(np.int8)
        pal=[];pidx={}
        def ci(c,fin):
            if (c,fin) not in pidx:pidx[(c,fin)]=len(pal);pal.append((c,fin))
            return pidx[(c,fin)]
        CI=np.full((h,w),-1,np.int16)
        def tgt(ids):return valid&np.isin(bi,list(ids))
        for L in rs['layers']:
            t=L['type']
            if t in ('finish','side_block','bands','gradient','rings'):m=tgt(L['parts'])
            if t=='finish':
                c,fin,_=colors[L['slot']];CI[m]=ci(c,fin)
            elif t=='side_block':
                m&=_inpoly(WX,WY,L['poly']);c,fin,_=colors[L['slot']];CI[m]=ci(c,fin)
            elif t=='bands':
                d=L['dir'];tt=WX*d[0]+WY*d[1]+WZ*d[2]-L['t0'];per=L['period'] or L['width']
                k=np.floor(tt/per);inb=m&(tt>=0)&((tt-k*per)<L['width'])&(k<L['count'])
                if L.get('window'):inb&=_inpoly(WX,WY,L['window'])
                ns=len(L['slots'])
                for j,sl in enumerate(L['slots']):
                    c,fin,_=colors[sl];CI[inb&((k%ns)==j)]=ci(c,fin)
            elif t=='gradient':
                d=L['dir'];tt=WX*d[0]+WY*d[1]+WZ*d[2];s_=np.clip((tt-L['t0'])/(L['t1']-L['t0']),0,0.9999)
                st=(s_*L['steps']).astype(np.int16);ca=colors[L['slots'][0]][0];cb=colors[L['slots'][1]][0]
                for j in range(L['steps']):CI[m&(st==j)]=ci(_mix(ca,cb,j/max(1,L['steps']-1)),'paint')
            elif t=='rings':
                cx,cy=L['center'];r=np.hypot(WX-cx,WY-cy)-L['r0'];per=L['width']+L['gap']
                k=np.floor(r/per);inr=m&(r>=0)&((r-k*per)<L['width'])&(k<L['count']);ns=len(L['slots'])
                for j,sl in enumerate(L['slots']):
                    c,fin,_=colors[sl];CI[inr&((k%ns)==j)]=ci(c,fin)
        for k,P in enumerate(parts):
            if P.get('_skslot'):
                c,fin,_=colors[P['_skslot']];CI[(pb==k)&~decm]=ci(c,fin)
        out=col.copy()
        streak=((WX*0.55-WY+WZ*0.35)/(0.42*Hb))%1.0<0.13
        for j,(c,fin) in enumerate(pal):
            m=CI==j
            if not m.any():continue
            tn=np.stack([_rgb(x) for x in tones(c,fin)])
            idx=fidx[m].astype(np.int16)
            if fin in ('polished_gold','polished_chrome'):idx=np.where(streak[m],4,idx)
            out[m]=tn[idx]
        # Kantenabnutzung
        for L in rs['layers']:
            if L['type']!='edge_wear':continue
            m=tgt(L['parts'])
            if not m.any():continue
            e=np.zeros((h,w),bool)
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):e|=idb!=np.roll(np.roll(idb,dy,0),dx,1)
            dist=ndimage.distance_transform_edt(~e)
            # zusammenhängende Abschnitte: Zellen von etwa sechs Abnutzungsbreiten, Breite je Zelle 60–100 %
            wpx=L['width']*scale;cell=L['width']*6.0
            nz=_hsh(np.floor(WX/cell)*0.37+np.floor(WY/cell)*1.91+np.floor(WZ/cell)*3.7)
            wm=m&(dist<wpx*(0.6+0.4*nz))&(nz>1-L['coverage'])
            tn=np.stack([_rgb(x) for x in tones(L['color'],'paint')])
            out[wm]=tn[fidx[wm].astype(np.int16)]
        return out
    tex.wants_scale=True
    return tex
