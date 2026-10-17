from cepaths import E3D,OUT
# Große Konzeptblätter (Seite „Konzeptblätter“): Isometrie + 6 Ortho + Detail Abzug + Material/Texturen + Farbvarianten + Prompt
import math,copy,colorsys,pickle,sys,html as _h
import numpy as np
from scipy import ndimage
sys.path.insert(0,E3D+'')
from eng import *
import raster
from xlroles import *
from xlroles import _rgb,_hex,_lum,_sat,_mix
import skins
from skinraster import skin_texture

ISO=('ISOMETRISCHE ANSICHT',-45,35.264)
ORTHO=[('SEITENANSICHT LINKS',0,0),('SEITENANSICHT RECHTS',180,0),('VORDERANSICHT',-90,0),('RÜCKANSICHT',90,0),('DRAUFSICHT',0,90),('UNTERANSICHT',0,-90)]
DETAIL_LABELS=['Abzug','Abzugbügel','Bügel','Griff','Pistolengriff','Griffstück','Magazin','Energiemagazin']

def make_texture(seed=3):
    """Texturen im Objektraum: Muster hängen an Bauteil-Koordinaten (nicht an der Bildrichtung)."""
    def tex(col,pb,idb,decm,parts,SS,world=None,nrm=None):
        h,w=pb.shape
        keys=['lack','brushed','rubber','plastic','light']
        lut=np.array([keys.index(material_of(P)) for P in parts]+[-1],np.int16)
        mat=np.where(pb>=0,lut[np.clip(pb,0,len(parts))],-1);mat[decm]=-1
        out=col.copy()
        WX,WY,WZ=world;NX,NY,NZ=np.abs(nrm[0]),np.abs(nrm[1]),np.abs(nrm[2])
        # Längsachse je Teil
        ax=np.zeros(len(parts)+1,np.int8)
        for i,P in enumerate(parts):
            vs=[q for f in P['F'] for q in f['v']]
            ext=[max(q[k] for q in vs)-min(q[k] for q in vs) for k in range(3)]
            ax[i]=int(np.argmax(ext))
        A=ax[np.clip(pb,0,len(parts))]
        C=[WX,WY,WZ]
        def hsh(t):return np.sin(t*12.9898)*43758.5453%1.0
        # gebürstet: Schleifspuren entlang der Längsachse -> Muster hängt nur von den beiden Querachsen ab
        q1=np.where(A==0,WY,np.where(A==1,WX,WX));q2=np.where(A==0,WZ,np.where(A==1,WZ,WY))
        t=q1*0.9+q2*0.9
        br=0.5*np.sin(t*3.1)+0.3*np.sin(t*7.3+1.7)+0.2*np.sin(t*13.1+0.4)
        br=1+0.13*br
        # gummiert: Rautenrändel in der Flächenebene
        domx=NX>=np.maximum(NY,NZ);domy=(NY>=np.maximum(NX,NZ))&~domx
        u=np.where(domx,WY,WX);v=np.where(domx,WZ,np.where(domy,WZ,WY))
        p=4.0
        rb=1-0.34*((np.floor((u+v)/p)%2==0)&(np.floor((u-v)/p)%2==0))
        # lackiert: weicher Glanzverlauf über die Höhe des Bauteils
        g=1+0.09*np.cos(WY/26.0)+0.04*np.cos((WX+WZ)/55.0)
        # matt: feines Korn, fest am Objekt
        pl=1+0.09*(hsh(np.floor(WX*1.3)*0.37+np.floor(WY*1.3)*1.91+np.floor(WZ*1.3)*3.7)-0.5)
        for k,f in ((0,g),(1,br),(2,rb),(3,pl)):
            mk=mat==k
            out[mk]=np.clip(out[mk]*f[mk][:,None],0,255)
        return out
    return tex

def swatch_svg(kind,w,h,col):
    """kleines Musterfeld je Material (Vektor)"""
    cid=f'sw{kind}{abs(hash(col))%9999}'
    if kind=='lack':return f'<defs><linearGradient id="{cid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{_mix(col,"#FFFFFF",0.25)}"/><stop offset="0.55" stop-color="{col}"/><stop offset="1" stop-color="{_mix(col,"#000000",0.2)}"/></linearGradient></defs><rect width="{w}" height="{h}" rx="10" fill="url(#{cid})"/>'
    if kind=='brushed':
        lines=''.join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{_mix(col,"#FFFFFF" if (y*7)%3 else "#000000",0.18)}" stroke-width="1"/>' for y in range(2,h,3))
        return f'<rect width="{w}" height="{h}" rx="10" fill="{col}"/><g clip-path="inset(0 round 10px)">{lines}</g>'
    if kind=='rubber':
        d=''.join(f'<rect x="{x}" y="{y}" width="6" height="6" transform="rotate(45 {x+3} {y+3})" fill="{_mix(col,"#000000",0.35)}"/>' for x in range(4,w-4,12) for y in range(4,h-4,12))
        return f'<rect width="{w}" height="{h}" rx="10" fill="{col}"/>{d}'
    if kind=='plastic':
        import random;r=random.Random(5)
        d=''.join(f'<circle cx="{r.uniform(0,w):.1f}" cy="{r.uniform(0,h):.1f}" r="0.9" fill="{_mix(col,"#FFFFFF",0.2)}"/>' for _ in range(120))
        return f'<rect width="{w}" height="{h}" rx="10" fill="{col}"/>{d}'
    return f'<defs><radialGradient id="{cid}"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.35" stop-color="{col}"/><stop offset="1" stop-color="{_mix(col,"#000000",0.55)}"/></radialGradient></defs><rect width="{w}" height="{h}" rx="10" fill="url(#{cid})"/>'

def _bbox(parts):
    vs=[q for P in parts for f in P['F'] for q in f['v']]
    return [(min(q[i] for q in vs),max(q[i] for q in vs)) for i in range(3)]

def detail_view(m,center,W,H,ow=3.0):
    core=[P for P in m.parts if (P.get('label') or '') in DETAIL_LABELS[:6]]
    sel=core or [P for P in m.parts if (P.get('label') or '') in DETAIL_LABELS]
    if not sel:return None,None
    bb=_bbox(sel)
    yaw,pitch=-28,-22
    c3=[(a+b)/2 for a,b in bb]
    yw,pt=math.radians(yaw),math.radians(pitch)
    o=tf((c3[0]-center[0],c3[1]-center[1],c3[2]-center[2]),yw,pt)
    corners=[(x,y,z) for x in bb[0] for y in bb[1] for z in bb[2]]
    pr=[tf((x-center[0],y-center[1],z-center[2]),yw,pt) for x,y,z in corners]
    hw=max(abs(p[0]-o[0]) for p in pr);hh=max(abs(p[1]-o[1]) for p in pr)
    sc=min((W/2-40)/max(hw*1.8,1),(H/2-50)/max(hh*1.8,1),4.5)
    v=svgview(m,yaw,pitch,center,W,H,sc,ow=ow,origin=(o[0],o[1]),shadow=False)
    names=sorted({P['label'] for P in sel},key=DETAIL_LABELS.index)
    return v,names

def _callouts(anchors,MW,MH,col,cy_model,k=1.0):
    def pillw(lb):return (len(lb)*13.5+40)*k
    call=''
    items=sorted(anchors.items(),key=lambda kv:kv[1][0])
    top=[it for it in items if it[1][1]<cy_model];bot=[it for it in items if it[1][1]>=cy_model]
    for grp,yl in ((top,86*k),(bot,MH-66*k)):
        n=len(grp)
        if not n:continue
        wds=[pillw(lb) for lb,_ in grp]
        xsl=[0.5*MW*(i+1)/(n+1)+0.5*a[0] for i,(lb,a) in enumerate(grp)]
        for i in range(1,n):
            mn=xsl[i-1]+(wds[i-1]+wds[i])/2+16
            if xsl[i]<mn:xsl[i]=mn
        if xsl[-1]+wds[-1]/2>MW-28:
            xsl[-1]=MW-28-wds[-1]/2
            for i in range(n-2,-1,-1):
                mx_=xsl[i+1]-(wds[i]+wds[i+1])/2-16
                if xsl[i]>mx_:xsl[i]=mx_
        if xsl[0]-wds[0]/2<28:
            sh=28-(xsl[0]-wds[0]/2);xsl=[x+sh for x in xsl]
        for k_,(lb,(ax,ay)) in enumerate(grp):
            lx=xsl[k_];y0=yl+(16*k if yl<MH/2 else -34*k)
            # Knick-Hinweislinie: senkrecht vom Etikett, dann zum Anker
            ky=y0+(ay-y0)*0.35
            call+=f'<polyline points="{lx:.0f},{y0:.0f} {lx:.0f},{ky:.0f} {ax:.0f},{ay:.0f}" fill="none" stroke="#E6ECF2" stroke-width="1.8" opacity="0.9"/><circle cx="{ax:.0f}" cy="{ay:.0f}" r="{6*k:.0f}" fill="#E6ECF2" stroke="#0A0A0D" stroke-width="2"/>'
            w_=pillw(lb)
            call+=f'<g transform="translate({lx:.0f},{yl:.0f})"><rect x="{-w_/2:.0f}" y="{-34*k:.0f}" width="{w_:.0f}" height="{46*k:.0f}" rx="{23*k:.0f}" fill="#0E1622" stroke="{col}" stroke-width="1.8"/><text x="0" y="{-4*k:.0f}" text-anchor="middle" font-family="Chakra Petch, sans-serif" font-size="{19*k:.0f}" font-weight="600" letter-spacing="1.6" fill="#E6ECF2">{_h.escape(lb.upper())}</text></g>'
    return call

def DEFS(fid):return f'<defs><filter id="gl{fid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter><pattern id="gr{fid}" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1A2636" stroke-width="1"/></pattern></defs>'

def panel(inner,w,h,label,fid,aria,small=False):
    return f'''<div style="position:relative;width:{w}px;height:{h}px;border-radius:18px;border:1px solid #22314A;background:#111A27;overflow:hidden;flex-shrink:0">
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block" role="img" aria-label="{_h.escape(aria)}">{DEFS(fid)}<rect width="{w}" height="{h}" fill="url(#gr{fid})"/>{inner}</svg>
<span style="position:absolute;left:12px;top:10px;padding:4px 10px;border-radius:8px;background:rgba(14,22,34,0.85);font-family:'Chakra Petch',sans-serif;font-size:{13 if small else 19}px;letter-spacing:3px;color:#8FA0B3">{label}</span></div>'''

EN={'Gehäuse':'receiver','Griff':'pistol grip','Abzug':'trigger with guard','Magazin':'magazine','Lauf':'barrel','Mündung':'muzzle','Mündungsbremse':'muzzle brake','Zielfernrohr':'scope on mounting rings','Visier':'sight','Schaft':'stock','Energiezelle':'energy cell','Kühlrippen':'cooling fins','Montageringe':'scope rings','Laufverkleidung':'barrel shroud','Vordergriff':'foregrip','Doppellauf':'double barrel','Trommel':'revolver cylinder','Sehne':'string','Wurfarm':'limb','Pfeil':'arrow','Umlenkrolle':'cam pulley','Pfeilauflage':'arrow rest','Stabilisator':'stabilizer','Rohr':'launch tube','Heckdüse':'rear exhaust','Abgasdüse':'rear exhaust','Raketenrohre':'rocket tubes','Handschutz':'handguard','Tragegriff':'carry handle','Kimme':'rear sight','Korn':'front sight','Ladeleiste':'charge indicator rail','Mündungsring':'muzzle ring','Schaftkappe':'butt plate','Wangenauflage':'cheek rest','Trommelmagazin':'drum magazine','Röhrenmagazin':'tube magazine','Pumpgriff':'pump grip','Kristallkern':'crystal core','Energiekugel':'energy orb','Bündelring':'focusing ring','Fokusring':'focusing ring','Fokusringe':'focusing rings','Laufmantel':'barrel jacket','Feuerkern':'fire core','Oberkiefer':'upper jaw','Unterkiefer':'lower jaw','Visierschiene':'sight rail','Ringvisier':'ring sight','Trichterheck':'flared rear funnel','Sicherungsmodul':'safety module','Rakete':'rocket','Spannmechanik':'cocking mechanism','Bolzen':'bolt','Mittelstück':'riser','Energie-Auge':'energy eye','Kondensator':'capacitor','Emitter':'emitter','Raketenkasten':'rocket pod','Heckkappe':'end cap','Verschluss':'breech','Kastenvisier':'box sight','Laufhülle':'barrel shroud','Laufkasten':'barrel housing','Ladekammer':'charging chamber','Beschleunigerring':'accelerator ring','Energiespule':'energy coil','Abschussrohr':'launch tube','Schalldämpfer':'suppressor','Montage':'mount','Rahmen':'frame','Energiekern':'energy core','Fokuskern':'focus core','Tragebügel mit Visier':'carry handle with sights','Oberlauf':'upper barrel','Unterlauf':'lower barrel','Energiemagazin':'energy magazine','Mittelstück':'riser','Abzugbügel':'trigger guard','Zweibein':'folded bipod','Kompensator':'compensator','Schlitten':'slide','Energiewürfel':'energy cube','Reflexvisier':'reflex sight','Käfig':'cage','Pulswürfel':'pulse cube','Feuerdämpfer':'flash hider','Kondensatorzelle':'capacitor cell','Fächeremitter':'fan emitter','Abschussrohre':'launch tubes','Kammerstängel':'bolt handle','Patronenfenster':'shell window','Klappschaft':'folding stock'}

def prompts(d,labels,mats,variant_letter,skin=None):
    pal=', '.join(d['palette'])
    de=(f"Erstelle ein technisches Low-Poly-Concept-Art-Blatt für das Spiel Cube Escape: {d['name']}, Variante {variant_letter} „{d['nick']}“. "
        f"Form: {d['form']}. {d['desc']} "
        f"Pflicht-Bauteile, alle sichtbar und nachvollziehbar verbunden: {', '.join(labels)}. "
        f"Farbpalette: {pal}. Materialien: {', '.join(mats)}. "
        "Ansichten: große isometrische Hauptansicht mit deutschen Bauteil-Beschriftungen, dazu Seitenansicht links und rechts, Vorder-, Rück-, Drauf- und Unteransicht – orthografisch, gleicher Maßstab, gemeinsame Bezugslinien – plus Detailansicht des Abzugsbereichs. "
        "Stil: futuristisch, industrial, Hard-Surface, abgeschrägte Gehäuse, kantige Panzerplatten, klare dunkle Konturen, flache Toon-Schattierung, dunkelblauer Rasterhintergrund. "
        "Konstruktion: Abzug mit Bügel klar erkennbar, Magazin im Schacht, Lauf sichtbar aus dem Gehäuse, konsistente Achsen. Visier bzw. Zielfernrohr NICHT montiert zeichnen, sondern separat als modulares Anbauteil daneben; auf der Waffe bleibt nur die freie Visierschiene als Aufnahme. "
        +(f"Hauptskin „{skin[0]}“: {skin[1]}. " if skin else "")+
        "Vermeiden: schwebende Teile, unbeabsichtigte Überschneidungen, zufällige Leuchtstreifen, Bloom, Unschärfe, Nebel, realistische Militärwaffen-Kopien.")
    if d['name']=='Raketenwerfer':
        de=de.replace('auf der Waffe bleibt nur die freie Visierschiene als Aufnahme.','auf der Waffe bleibt nur die freie Visierschiene als Aufnahme – seitlich links am Rohr montiert, damit das Rohr die Sichtlinie nicht verdeckt.')
    en_parts=', '.join(EN.get(l,l) for l in labels)
    en=(f"Low-poly sci-fi weapon concept sheet for the game Cube Escape: futuristic {d.get('en_type','weapon')}, variant {variant_letter} \"{d['nick']}\". "
        f"Visible, logically connected parts: {en_parts}. Color palette {pal}. "
        "Large isometric hero view with labeled callouts plus orthographic left, right, front, back, top and bottom views at identical scale, trigger-area detail. Draw the sight/scope detached as a separate modular attachment next to the weapon; the weapon shows only the empty sight rail. "
        +("Sight rail mounted on the left side of the tube, offset from the bore axis. " if d['name']=='Raketenwerfer' else "")+
        (f"Skin \"{skin[0]}\": {skin[2]}. " if skin else "")+
        "Hard-surface industrial design, chamfered housings, clean dark outlines, flat cel shading, dark blue grid background, no bloom, no blur, no floating parts.")
    return de,en

TYPE_EN={'Pistole':'pistol','Sturmgewehr':'assault rifle','Impulsgewehr':'pulse rifle','Schrotflinte':'shotgun','Scharfschützengewehr':'sniper rifle','Maschinenpistole':'submachine gun','Fusionsgewehr':'fusion rifle','Spurgewehr':'trace rifle','Raketenwerfer':'rocket launcher','Bogen':'bow'}

PRIO=['Gehäuse','Griff','Abzug','Magazin','Energiezelle','Energiemagazin','Trommelmagazin','Röhrenmagazin','Lauf','Doppellauf','Mündung','Mündungsbremse','Schaft','Visierschiene','Rohr','Abschussrohr','Abschussrohre','Wurfarm','Sehne','Pfeil','Mittelstück','Umlenkrolle','Pfeilauflage','Handschutz','Laufmantel','Laufverkleidung','Emitter']
def pick_labels(anchors,n=8):
    ks=sorted(anchors,key=lambda k:(PRIO.index(k) if k in PRIO else 50,k))[:n]
    return {k:anchors[k] for k in ks},[k for k in anchors if k not in ks]

def _shift_part(P,dx):
    Q=dict(P);Q['F']=[dict(f,v=[(x-dx,y,z) for x,y,z in f['v']]) for f in P['F']]
    dec=[]
    for plane,val,pts,c,em in P['dec']:
        if plane[0]=='z':pts=[(x-dx,y) for x,y in pts]
        elif plane[0]=='x':val=val-dx
        else:pts=[(x-dx,z) for x,z in pts]
        dec.append((plane,val,pts,c,em))
    Q['dec']=dec;return Q

def compact_sight(ms,gap=30):
    """Getrennte Visierteile (Kimme hinten, Korn vorne) rücken für die Visier-Ansicht zusammen,
    sonst bestimmt der Abstand über die ganze Waffenlänge den Maßstab und die Teile werden winzig."""
    xs=[(min(q[0] for f in P['F'] for q in f['v']),max(q[0] for f in P['F'] for q in f['v']),P) for P in ms.parts]
    cl=[]
    for x0,x1,P in sorted(xs,key=lambda t:t[0]):
        if cl and x0<=cl[-1][1]+gap:cl[-1][1]=max(cl[-1][1],x1);cl[-1][2].append(P)
        else:cl.append([x0,x1,[P]])
    if len(cl)<2:return ms,False
    out=Model();shift=0
    for i,(x0,x1,Ps) in enumerate(cl):
        if i:shift+=max(0,x0-cl[i-1][1]-gap)
        out.parts+=[_shift_part(P,shift) if shift else P for P in Ps]
    return out,shift>0

def sight_panel(ms,center,w,h,fid,name,col,small=False):
    if ms.parts:ms,_=compact_sight(ms)
    if not ms.parts:
        inner=f'<text x="{w/2}" y="{h/2}" text-anchor="middle" font-family="Chakra Petch, sans-serif" font-size="22" fill="#8FA0B3">Keine Optik – Visierschiene frei</text>'
        return panel(inner,w,h,'VISIER · SEPARAT',fid,name+' ohne separates Visier')
    hw_=w/2-24
    e1,e2=extent(ms,ISO[1],ISO[2],center);s1=min((hw_-40)/e1,(h-(60 if small else 130))/e2,6)
    v1=svgview(ms,ISO[1],ISO[2],center,int(hw_),h-40,s1,ow=2.6,shadow=False)
    e3,e4=extent(ms,0,0,center);s2=min((hw_-40)/e3,(h-(60 if small else 130))/e4,6)
    v2=svgview(ms,0,0,center,int(hw_),h-40,s2,ow=2.6,shadow=False)
    labs=sorted({P['label'] for P in ms.parts if P.get('label')})
    inner=(f'<g transform="translate(16,24)">{v1}</g><g transform="translate({w/2+8:.0f},24)">{v2}</g>'
           f'<line x1="{w/2}" y1="56" x2="{w/2}" y2="{h-60}" stroke="#22314A" stroke-width="1.5"/>'
           f'<text x="{14 if small else 24}" y="{h-(12 if small else 26)}" font-family="Chakra Petch, sans-serif" font-size="{13 if small else 19}" letter-spacing="1.2" fill="#E6ECF2">{_h.escape(" · ".join(labs) if labs else "Visier")} · modular auf Schiene, nicht fest verbaut</text>')
    return panel(inner,w,h,'VISIER · SEPARAT' if small else 'VISIER · SEPARAT (ISOMETRIE / SEITE)',fid,name+' Visier separat gezeichnet',small)

def _chip(x,y,c,fin,label):
    """Farbfeld eines Skin-Slots: Lack flach, poliert mit Verlauf und Glanzstreifen, Neon mit Leuchtrand"""
    from skinraster import tones
    if fin in ('polished_gold','polished_chrome'):
        t=tones(c,fin);gid=f'ch{abs(hash((c,fin)))%99999}'
        sw=(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t[0]}"/><stop offset="0.42" stop-color="{t[1]}"/>'
            f'<stop offset="0.5" stop-color="{t[4]}"/><stop offset="0.58" stop-color="{t[1]}"/><stop offset="1" stop-color="{t[3]}"/></linearGradient></defs>'
            f'<rect x="{x}" y="{y}" width="34" height="34" rx="8" fill="url(#{gid})" stroke="#0A0A0D" stroke-width="1.5"/>')
    elif fin=='neon':sw=f'<rect x="{x-3}" y="{y-3}" width="40" height="40" rx="10" fill="{c}" opacity="0.35"/><rect x="{x}" y="{y}" width="34" height="34" rx="8" fill="{c}" stroke="#0A0A0D" stroke-width="1.5"/>'
    else:sw=f'<rect x="{x}" y="{y}" width="34" height="34" rx="8" fill="{c}" stroke="#0A0A0D" stroke-width="1.5"/>'
    return sw+f'<text x="{x+44}" y="{y+24}" font-family="Barlow, sans-serif" font-size="19" fill="#C7D1DC">{_h.escape(label)}</text>'

def skin_row(rsl,skinned,full,center,cw,ch,fid,name):
    """Feld SKIN/MUSTER: fünf Skins aus dem Katalog in der Basis-Palette, je mit Slots und Bausteinen"""
    out=''
    for j,rs in enumerate(rsl):
        mm,tx_,cs=skinned(0,rs,full)
        vh=ch-230
        e1,e2=extent(mm,ISO[1],ISO[2],center);sc=min((cw-70)/e1,(vh-70)/e2)
        vv=svgview(mm,ISO[1],ISO[2],center,cw,vh,sc,ow=2.6,texture=tx_).replace('<image x="0" y="0"','<image x="0" y="26"',1)
        inner=vv;y0=vh+24
        for k,sl in enumerate(skins.slots_used(rs)[:6]):
            c,fin,src=cs[sl]
            lab=skins.SLOT_DE[sl]+(' · '+skins.FINISH_DE[fin] if fin!='paint' else '')+(' *' if src=='swatch' else '')
            inner+=_chip(24+(k%2)*((cw-40)//2),y0+(k//2)*46,c,fin,lab)
        bl=' · '.join(skins.BLOCKS[b] for b in skins.summary(rs))
        inner+=f'<text x="24" y="{ch-22}" font-family="Chakra Petch, sans-serif" font-size="18" letter-spacing="1.2" fill="#8FA0B3">{_h.escape(bl.upper())}</text>'
        lab=f'SKIN/MUSTER {j+1}/5 · {rs["name"].upper()}'+(' · HAUPTSKIN' if j==0 else '')
        out+=panel(inner,cw,ch,lab,fid,f'{name} Skin {rs["name"]}')
    return out

def sheet(d,variant_letter):
    full=d['m'];center=d['center'];fid='x'+d['fid'];col=d['col']
    m,ms=split_sight(full)
    # ---------- Skins (claude-0.3): fünf je Blatt, der erste ist der Hauptskin (Isometrie, Orthos, Farbvarianten)
    sid=f'K{variant_letter}{d["num"]}'
    rsl=[skins.resolve(full,k,sid,d['num']) for k in skins.pick(sid,full,d['num'])];hero=rsl[0]
    cpal,_=channel_palettes(full,m,d['palette'],d['pill'],CHANNELS)
    roles=color_roles(m)
    def skinned(j,rs,mf):
        cs=skins.slot_colors(rs,cpal[j]['channels'],cpal[j]['swatches'])
        return split_sight(skins.apply(mf,rs,cs))[0],skin_texture(rs,cs),cs
    mh,htex,_=skinned(0,hero,full)
    SKH=1000
    W,H0=4800,3400;PAD=80;G=32;H=H0+G+SKH
    # ---------- Isometrie mit Beschriftungen
    MW,MH=2700,1800
    ew,eh=extent(mh,ISO[1],ISO[2],center)
    sm=min((MW-200)/ew,(MH-420)/eh,6.0)
    v=svgview(mh,ISO[1],ISO[2],center,MW,MH,sm,ow=4.6,texture=htex)
    anchors,rest=pick_labels(dict(raster.LAST.get('anchors',{})))
    call=_callouts(anchors,MW,MH,col,MH/2,k=1.35)
    if rest:call+=f'<text x="28" y="{MH-24}" font-family="Barlow, sans-serif" font-size="20" fill="#8FA0B3">Weitere Bauteile: {_h.escape(", ".join(sorted(rest)))}</text>'
    iso=panel(v+call,MW,MH,ISO[0]+' · OHNE VISIER · HAUPTSKIN '+hero['name'].upper(),fid,f"{d['name']} isometrische Ansicht mit Bauteilbeschriftungen, Visier separat")
    # ---------- Ortho
    RW=W-2*PAD-MW-G
    geo={lb:model_origin(mh,y,p,center) for lb,y,p in ORTHO}
    hwL,hhL=geo['SEITENANSICHT LINKS'][1],geo['SEITENANSICHT LINKS'][2];hhT=geo['DRAUFSICHT'][2];hwF=geo['VORDERANSICHT'][1]
    def obox(lb,yw,pt,w,h,ss):
        o,hw,hh=geo[lb]
        vv=svgview(mh,yw,pt,center,w,h,ss,ow=3.0,origin=o,texture=htex).replace('<image x="0" y="0"','<image x="0" y="12"',1)
        cy=h/2+12;cx=w/2;ref=''
        if pt==0:
            for yy in (cy-hh*ss,cy+hh*ss):ref+=f'<line x1="0" y1="{yy:.1f}" x2="{w}" y2="{yy:.1f}" stroke="#4A6080" stroke-width="1.4" stroke-dasharray="8 8"/>'
            ref+=f'<line x1="{cx}" y1="0" x2="{cx}" y2="{h}" stroke="#2E405A" stroke-width="1.2" stroke-dasharray="2 8"/>'
        else:
            for xx in (cx-hw*ss,cx+hw*ss):ref+=f'<line x1="{xx:.1f}" y1="0" x2="{xx:.1f}" y2="{h}" stroke="#4A6080" stroke-width="1.4" stroke-dasharray="8 8"/>'
            ref+=f'<line x1="0" y1="{cy}" x2="{w}" y2="{cy}" stroke="#2E405A" stroke-width="1.2" stroke-dasharray="2 8"/>'
        return panel(ref+vv,w,h,lb,fid,f"{d['name']} {lb.lower()}")
    AV=MH
    if hwL>2.0*hhL:
        g=18
        ss=min((RW-90)/(2*hwL),(AV-5*90-4*g)/(2*(3*hhL+2*hhT)),((RW-g)/2-70)/(2*hwF))
        hL=int(2*hhL*ss+90);hT=int(2*hhT*ss+90);hF=AV-2*hL-2*hT-4*g
        rows=[obox('SEITENANSICHT LINKS',0,0,RW,hL,ss),obox('SEITENANSICHT RECHTS',180,0,RW,hL,ss)]
        fr=obox('VORDERANSICHT',-90,0,(RW-g)//2,hF,ss)+obox('RÜCKANSICHT',90,0,(RW-g)//2,hF,ss)
        ortho=f'<div style="display:flex;flex-direction:column;gap:{g}px;width:{RW}px;height:{AV}px">'+rows[0]+rows[1]+f'<div style="display:flex;gap:{g}px">{fr}</div>'+obox('DRAUFSICHT',0,90,RW,hT,ss)+obox('UNTERANSICHT',0,-90,RW,hT,ss)+'</div>'
    else:
        g=22;bw=(RW-g)//2;bh=(AV-2*g)//3
        ss=min(min((bw/2-46)/hw,(bh/2-66)/hh) for _,hw,hh in geo.values())
        ortho=f'<div style="display:grid;grid-template-columns:repeat(2,{bw}px);grid-auto-rows:{bh}px;gap:{g}px">'+''.join(obox(lb,y,p,bw,bh,ss) for lb,y,p in ORTHO)+'</div>'
    # ---------- untere Reihe
    BH=H0-2*PAD-180-G-MH-G
    DW=900;ph=(BH-20)//2
    dv,dnames=detail_view(m,center,DW,ph)
    if dv is None:dv,dnames='',[]
    det=panel(dv,DW,ph,'DETAIL · ABZUGSBEREICH ('+(", ".join(dnames) if dnames else "Griff")+')',fid,f"{d['name']} Detailansicht Abzugsbereich von schräg unten")
    sp=sight_panel(ms,center,DW,ph,fid,d['name'],col)
    det=f'<div style="display:flex;flex-direction:column;gap:20px;width:{DW}px">{det}{sp}</div>'
    # Material
    MWd=1180;mh=BH-190
    me,mhh=extent(m,ISO[1],ISO[2],center)
    msc=min((MWd-90)/me,(mh-90)/mhh)
    mv=svgview(m,ISO[1],ISO[2],center,MWd,mh,msc,ow=3.0,texture=make_texture())
    used={}
    for P in m.parts:
        k=material_of(P);used.setdefault(k,P['col'])
    sw=''
    for nm,k in MATS:
        if k not in used:continue
        sw+=f'<div style="display:flex;flex-direction:column;gap:8px;width:210px"><svg width="210" height="96" viewBox="0 0 210 96" role="img" aria-label="Muster {nm.lower()}">{swatch_svg(k,210,96,used[k])}</svg><span style="font-family:\'Chakra Petch\',sans-serif;font-size:16px;letter-spacing:1.5px;color:#C7D1DC;line-height:1.25">{nm}</span></div>'
    matp=f'<div style="display:flex;flex-direction:column;gap:18px;width:{MWd}px">{panel(mv,MWd,mh,"MATERIAL & TEXTUREN",fid,d["name"]+" Materialansicht mit Texturen")}<div style="display:flex;gap:18px">{sw}</div></div>'
    # Farbvarianten
    VW=1380;vw=(VW-24)//2;vh=(BH-24)//2
    vs=''
    base=('BASIS · '+d['pill'],d['palette'])
    for j,(vn,pal) in enumerate([base]+VARIANTS[:3]):
        mm,tx_,_=skinned(j,hero,recolor(full,pal,role=roles) if j else full)
        e1,e2=extent(mm,ISO[1],ISO[2],center);sc=min((vw-60)/e1,(vh-110)/e2)
        vv=svgview(mm,ISO[1],ISO[2],center,vw,vh,sc,ow=2.4,texture=tx_)
        dots=''.join(f'<rect x="{24+i*36}" y="{vh-46}" width="28" height="28" rx="7" fill="{c}" stroke="#0A0A0D" stroke-width="1"/>' for i,c in enumerate(pal))
        vs+=panel(vv+dots,vw,vh,vn if len(vn)<44 else vn[:42]+'…',fid,f"{d['name']} Farbvariante {vn}")
    varp=f'<div style="display:grid;grid-template-columns:repeat(2,{vw}px);grid-auto-rows:{vh}px;gap:24px;width:{VW}px">{vs}</div>'
    # Prompt
    m=full
    labels=sorted({P['label'] for P in m.parts if P.get('label')})
    mats=[nm.title() for nm,k in MATS if k in used]
    d2=dict(d);d2['en_type']=TYPE_EN.get(d['name'],'weapon')
    de,en=prompts(d2,labels,mats,variant_letter,skin=(hero['name'],)+skins.DESC[hero['id']])
    PW=W-2*PAD-DW-MWd-VW-3*G
    pr=f'''<div style="width:{PW}px;height:{BH}px;box-sizing:border-box;border-radius:18px;border:1px solid #22314A;background:#0B121C;padding:26px 28px;display:flex;flex-direction:column;gap:14px;overflow:hidden">
<span style="font-family:'Chakra Petch',sans-serif;font-size:19px;letter-spacing:3px;color:#8FA0B3">PROMPT · DEUTSCH</span>
<p style="margin:0;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:18px;line-height:1.5;color:#E6ECF2;user-select:all">{_h.escape(de)}</p>
<span style="font-family:'Chakra Petch',sans-serif;font-size:19px;letter-spacing:3px;color:#8FA0B3;margin-top:8px">PROMPT · ENGLISCH (BILDGENERATOR)</span>
<p style="margin:0;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:18px;line-height:1.5;color:#C7D1DC;user-select:all">{_h.escape(en)}</p></div>'''
    pal=''.join(f'<div style="display:flex;align-items:center;gap:10px"><div style="width:50px;height:50px;border-radius:12px;background:{c}"></div><span style="font-size:19px;color:#8FA0B3">{c}</span></div>' for c in d['palette'])
    page=f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{d['num']} {d['name']} Variante {variant_letter} Konzeptblatt XL</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}</style>
</helmet>
<div style="width:{W}px;height:{H}px;box-sizing:border-box;padding:{PAD}px;background:#0E1622;color:#E6ECF2;font-family:Barlow,sans-serif;display:flex;flex-direction:column;gap:{G}px">
<div style="height:180px;display:flex;justify-content:space-between;align-items:center;gap:40px">
<div style="display:flex;align-items:center;gap:30px;min-width:0">
<span style="font-family:'Chakra Petch',sans-serif;font-size:140px;font-weight:700;line-height:1;color:{col}">{d['num']}</span>
<div style="display:flex;flex-direction:column;gap:8px;min-width:0">
<span style="font-family:'Chakra Petch',sans-serif;font-size:74px;font-weight:700;letter-spacing:6px;line-height:1.05">{_h.escape(d['name'].upper())} · VARIANTE {variant_letter}</span>
<span style="font-size:25px;letter-spacing:4px;color:#8FA0B3">„{_h.escape(d['nick'].upper())}“ · KONZEPTBLATT XL · VISIER SEPARAT · HAUPTSKIN {_h.escape(hero['name'].upper())} · {_h.escape(d['form'])}</span>
</div>
</div>
<div style="display:flex;align-items:center;gap:30px;flex-shrink:0">
<div style="display:flex;gap:20px">{pal}</div>
<span style="padding:16px 32px;border:1.5px solid {col};border-radius:999px;color:{col};font-family:'Chakra Petch',sans-serif;font-size:24px;font-weight:600;letter-spacing:3px;white-space:nowrap">{_h.escape(d['pill'])}</span>
</div>
</div>
<div style="display:flex;gap:{G}px;height:{MH}px">{iso}{ortho}</div>
<div style="display:flex;gap:{G}px;height:{BH}px">{det}{matp}{varp}{pr}</div>
<div style="display:flex;gap:{G}px;height:{SKH}px">{skin_row(rsl,skinned,full,center,(W-2*PAD-4*G)//5,SKH,fid,d['name'])}</div>
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
'''
    return page,de,en
