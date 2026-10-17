from fontcss import FONT_CSS
from cepaths import E3D,OUT
from eng import *
ISO=('ISOMETRISCHE ANSICHT',-45,35.264)
ORTHO=[('SEITENANSICHT LINKS',0,0),('SEITENANSICHT RECHTS',180,0),('VORDERANSICHT',-90,0),('RÜCKANSICHT',90,0),('DRAUFSICHT',0,90),('UNTERANSICHT',0,-90)]
VIEWS=[ISO]+ORTHO
DEFS='<defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter><pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1A2636" stroke-width="1"/></pattern></defs>'

import raster
def _esc(t):return t.replace('&','&amp;').replace('<','&lt;')
def card(m,center,num,name,sub,col,pill,desc,palette,form,fid):
    import pickle
    try:pickle.dump(dict(m=m,center=center,num=num,name=name,sub=sub,col=col,pill=pill,desc=desc,palette=palette,form=form,fid=fid),open(f'{E3D}/reg/{fid}.pkl','wb'))
    except Exception as e:print('reg',e)
    W,H=2400,1560
    m_full=m;m,ms=split_sight(m_full)
    MW,MH=1420,1140;SW,SH=430,380
    # Isometrie
    ew,eh=extent(m,ISO[1],ISO[2],center);hw0,hh0=ew/2,eh/2
    labs=sorted({P['label'] for P in m.parts if P.get('label')})
    wide=hw0>=hh0*1.1
    padx=60 if wide else 250;pady=200 if wide else 70
    sm=min((MW/2-padx)/hw0,(MH/2-pady)/hh0,3.4)
    v=svgview(m,ISO[1],ISO[2],center,MW,MH,sm,ow=3.4)
    anchors=dict(raster.LAST.get('anchors',{}))
    # Beschriftungen mit Hinweislinien
    import xl as _xl
    call=_xl._callouts(anchors,MW,MH,col,MH/2) if anchors else ''
    defs=DEFS.replace('id="gl"',f'id="gl{fid}"').replace('id="gr"',f'id="gr{fid}"')
    mainbox=f"""<div style="position:relative;width:{MW}px;height:{MH}px;border-radius:16px;border:1px solid #22314A;background:#111A27;overflow:hidden">
<svg width="{MW}" height="{MH}" viewBox="0 0 {MW} {MH}" style="display:block" role="img" aria-label="{name} isometrische Ansicht mit Bauteilbeschriftungen">{defs}<rect width="{MW}" height="{MH}" fill="url(#gr{fid})"/>{v}{call}</svg>
<span style="position:absolute;left:18px;top:14px;font-family:'Chakra Petch',sans-serif;font-size:15px;letter-spacing:3px;color:#8FA0B3">{ISO[0]}</span></div>"""
    # Orthografische Ansichten: gemeinsamer Maßstab, gemeinsamer Bezugspunkt
    geo=[model_origin(m,y,p,center) for _,y,p in ORTHO]
    G={lb:g for (lb,_,_),g in zip(ORTHO,geo)}
    hwL,hhL=G['SEITENANSICHT LINKS'][1],G['SEITENANSICHT LINKS'][2]
    hhT=G['DRAUFSICHT'][2];hwF=G['VORDERANSICHT'][1]
    RW=2*SW+20;AV=1236
    def obox(lb,yw,pt,o,hw,hh,w,h,ss):
        vv=svgview(m,yw,pt,center,w,h,ss,ow=2.4,origin=o)
        cy=h/2+8;cx=w/2
        vv=vv.replace('<image x="0" y="0"',f'<image x="0" y="8"',1)
        ref=''
        if pt==0:
            for yy in (cy-hh*ss,cy+hh*ss):ref+=f'<line x1="0" y1="{yy:.1f}" x2="{w}" y2="{yy:.1f}" stroke="#4A6080" stroke-width="1" stroke-dasharray="6 6"/>'
            ref+=f'<line x1="{cx}" y1="0" x2="{cx}" y2="{h}" stroke="#2E405A" stroke-width="1" stroke-dasharray="2 6"/>'
        else:
            for xx in (cx-hw*ss,cx+hw*ss):ref+=f'<line x1="{xx:.1f}" y1="0" x2="{xx:.1f}" y2="{h}" stroke="#4A6080" stroke-width="1" stroke-dasharray="6 6"/>'
            ref+=f'<line x1="0" y1="{cy}" x2="{w}" y2="{cy}" stroke="#2E405A" stroke-width="1" stroke-dasharray="2 6"/>'
        return f"""<div style="position:relative;width:{w}px;height:{h}px;border-radius:16px;border:1px solid #22314A;background:#111A27;overflow:hidden;flex-shrink:0">
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block" role="img" aria-label="{name} {lb.lower()}">{defs}<rect width="{w}" height="{h}" fill="url(#gr{fid})"/>{ref}{vv}</svg>
<span style="position:absolute;left:16px;top:10px;font-family:'Chakra Petch',sans-serif;font-size:13px;letter-spacing:3px;color:#8FA0B3">{lb}</span></div>"""
    if hwL>2.0*hhL:
        # Lange Waffe: Seiten-, Drauf- und Unteransicht über die volle Breite
        ss=min((RW-70)/(2*hwL),(AV-5*76-5*14)/(2*(3*hhL+2*hhT)),(SW-60)/(2*hwF))
        hL=int(2*hhL*ss+76);hT=int(2*hhT*ss+76);hF=max(int(2*hhL*ss+76),170)
        rows=[]
        for lb,yw,pt in ORTHO:
            o,hw,hh=G[lb]
            if lb in ('SEITENANSICHT LINKS','SEITENANSICHT RECHTS'):rows.append(obox(lb,yw,pt,o,hw,hh,RW,hL,ss))
            elif lb in ('DRAUFSICHT','UNTERANSICHT'):rows.append(obox(lb,yw,pt,o,hw,hh,RW,hT,ss))
        fr=''.join(obox(lb,yw,pt,G[lb][0],G[lb][1],G[lb][2],SW,hF,ss) for lb,yw,pt in ORTHO if lb in ('VORDERANSICHT','RÜCKANSICHT'))
        boxes=f'<div style="display:flex;flex-direction:column;gap:14px;width:{RW}px">'+rows[0]+rows[1]+f'<div style="display:flex;gap:20px">{fr}</div>'+rows[2]+rows[3]+'</div>'
    else:
        ss=min(min((SW/2-34)/hw,(SH/2-52)/hh) for _,hw,hh in geo)
        boxes=f'<div style="display:grid;grid-template-columns:repeat(2,{SW}px);grid-auto-rows:{SH}px;gap:20px">'+''.join(obox(lb,yw,pt,o,hw,hh,SW,SH,ss) for (lb,yw,pt),(o,hw,hh) in zip(ORTHO,geo))+'</div>'
    import xl as _x2
    sightbox=_x2.sight_panel(ms,center,520,176,fid+'s',name,col,small=True) if ms.parts else ''
    pal=''.join(f'<div style="display:flex;align-items:center;gap:8px"><div style="width:34px;height:34px;border-radius:8px;background:{c}"></div><span style="font-size:14px;color:#8FA0B3">{c}</span></div>' for c in palette)
    sub2=sub.replace('ALLE PERSPEKTIVEN, GEZEICHNET','KONZEPTBLATT')
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{num} {name} Konzeptblatt</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT_CSS}
<style>body{{margin:0}}</style>
</helmet>
<div style="width:{W}px;height:{H}px;box-sizing:border-box;padding:48px 56px;background:#0E1622;color:#E6ECF2;font-family:Barlow,sans-serif;display:flex;flex-direction:column;gap:26px">
<div style="display:flex;justify-content:space-between;align-items:center;gap:32px">
<div style="display:flex;align-items:center;gap:26px">
<span style="font-family:'Chakra Petch',sans-serif;font-size:84px;font-weight:700;line-height:1;color:{col}">{num}</span>
<div style="display:flex;flex-direction:column;gap:6px">
<span style="font-family:'Chakra Petch',sans-serif;font-size:46px;font-weight:700;letter-spacing:4px;line-height:1.1">{name.upper()} · KONZEPTBLATT</span>
<span style="font-size:18px;letter-spacing:4px;color:#8FA0B3">{sub2}</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:28px">
<div style="display:flex;gap:18px">{pal}</div>
<span style="padding:12px 24px;border:1px solid {col};border-radius:999px;color:{col};font-family:'Chakra Petch',sans-serif;font-size:17px;font-weight:600;letter-spacing:3px;white-space:nowrap">{pill}</span>
</div>
</div>
<div style="flex:1;min-height:0;display:flex;gap:28px">
<div style="display:flex;flex-direction:column;gap:20px">
{mainbox}
<div style="display:flex;gap:28px;font-size:17px;line-height:1.45;color:#C7D1DC"><p style="margin:0;flex:1">{desc}</p><p style="margin:0;width:330px;color:#E6ECF2"><span style="font-family:'Chakra Petch',sans-serif;font-size:14px;letter-spacing:3px;color:#8FA0B3">FORM</span><br>{form}</p>{sightbox}</div>
</div>
<div style="display:flex;flex-direction:column;gap:14px">
{boxes}
<p style="margin:0;font-size:15px;line-height:1.45;color:#8FA0B3;width:{2*SW+20}px">Technische Ansichten orthografisch, alle im gleichen Maßstab und aus demselben 3D-Modell erzeugt. Gestrichelt: gemeinsame Bezugslinien für Höhe bzw. Breite. Gestalterische Referenz, keine bemaßte Fertigungszeichnung.</p>
</div>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""
