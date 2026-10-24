"""Visier der Visier-Serie VS01–VS09 auf den Waffenblättern (claude-0.7; Entscheidung des Nutzers „Danach Waffenblätter umstellen“).

Die Geometrie kommt aus vsmodels.py (eine Wahrheit, keine Kopie): das Standardvisier des Waffentyps wird in mm geladen, mit dem
Maßstab des Waffen-Specs in Modelleinheiten umgerechnet und so gesetzt, dass Socket_Mount (Unterkante Mitte der Halterung) auf der
Visierschiene liegt (Raketenwerfer: seitliche Schiene links am Rohr, wie bisher). Die alten Visierteile des Blatts entfallen.
Farben: je MT_-Kanal die Kanalfarbe der Waffe (Basis-Palette des Blatts, xlroles.channel_palettes); nutzt die Waffe einen Kanal nicht,
gilt der erste belegte aus xlroles.FALLBACK, und das Teil bekommt diesen Kanal. Glas behält die Tönung des Visiers.
Bögen haben kein VS-Ziel und behalten ihr Pin-Visier. Neue Waffentypen (claude-0.10) tragen das Visier aus wtypes (verwandter Typ),
Schwert und Glefe keines.

Ohne numpy (Spec-Export ohne Bildstufe). Aufruf: sheetmodels.load() und build_xl.py (Kartenweg über reg/*.pkl).
"""
import math
import vsmodels as V
from eng import Model,CHANNELS
from xlroles import FALLBACK,channel_palettes

VS_OF={s['weapon']:f'VS{s["num"]}' for s in V.SERIES}   # Waffe (Blattname) -> Standardvisier
import wtypes
VS_OF.update({n:t['vs'] for n,t in wtypes.NEW.items() if t['vs']})   # neue Waffentypen (claude-0.10): Visier des verwandten Typs
# Ausnahmen je Blatt (claude-0.15.1): Blatt -> (Visier, Begründung); vor der Typregel (VS_TYPE), KG03 behält so seinen Begründungstext
VS_SHEET={'KG01':(None,'Entscheidung des Nutzers 24.10.2026: Pistole mit Kimme und Korn fest auf dem Schlitten statt Reflexvisier VS01 (Toolgen docs/ENTSCHEIDUNGEN.md, Sidearm 0.27)'),
          'KG03':('VS02','Entscheidung des Nutzers 22.10.2026: Zielfernrohre nur an Präzisionswaffen (Scout, Scharfschütze, lineare Fusion, '
                         'Armbrust); KG03 trägt das Holo-Visier VS02 wie KG02 statt der Präzisions-Röhre VS03')}
# Typregeln (claude-0.15.2): Waffe (Blattname) -> (Visier, Begründung) für alle Blätter des Typs; eine Ausnahme je Blatt geht vor
VS_TYPE={'Impulsgewehr':('VS02','Typregel des Nutzers 22.10.2026: Zielfernrohre nur an Präzisionswaffen (Scout, Scharfschütze, lineare Fusion, '
                                'Armbrust); das Impulsgewehr trägt das Holo-Visier VS02 wie das Sturmgewehr statt der Präzisions-Röhre VS03 (CE 0.111.1)')}
def choice_of(sheet,name):
    """Visier-Wahl (Visier, Begründung) abweichend vom Standardvisier der Serie oder None: Blatt vor Typ"""
    return VS_SHEET.get(sheet) or VS_TYPE.get(name)
def sheet_of(fid):return 'K'+('C' if fid[0]=='v' else fid[0].upper())+fid[1:]
RAIL_H_MM=6.0        # neue Visierschiene (Blätter ohne Schiene): Höhe über der höchsten Stelle der Waffe unter der Halterung
RAIL_W_MM=14.0       # Breite (zwischen den Klemmbacken der Halterung, vsmodels.mount: Backen 3 mm innen)
JAW_MM=3.0           # Klemmbacken reichen so weit unter Socket_Mount (vsmodels.mount)
CLUSTER_GAP=30       # Abstand zwischen getrennten alten Visierteilen (Kimme hinten, Korn vorn), wie xl.compact_sight

def _verts(parts):return [q for P in parts for f in P['F'] for q in f['v']]
def _bb(parts):
    v=_verts(parts);return [min(q[i] for q in v) for i in range(3)],[max(q[i] for q in v) for i in range(3)]
def _newell(v):
    n=[0.0,0.0,0.0]
    for i in range(len(v)):
        (x0,y0,z0),(x1,y1,z1)=v[i],v[(i+1)%len(v)]
        n[0]+=(y0-y1)*(z0+z1);n[1]+=(z0-z1)*(x0+x1);n[2]+=(x0-x1)*(y0+y1)
    return n
def _inside2(px,pz,poly):
    c=False;n=len(poly)
    for i in range(n):
        (ax,az),(bx,bz)=poly[i],poly[(i+1)%n]
        if (az>pz)!=(bz>pz) and px<ax+(pz-az)*(bx-ax)/(bz-az):c=not c
    return c
class Faces:
    """Flächen mit Grundriss-Hülle (x, z) für top_y; einmal je Teilmenge aufbauen"""
    def __init__(s,parts):
        s.f=[]
        for P in parts:
            for f in P['F']:
                v=f['v'];n=_newell(v)
                if abs(n[1])<1e-9*(abs(n[0])+abs(n[2])+1):continue
                xs=[q[0] for q in v];zs=[q[2] for q in v]
                s.f.append((min(xs),max(xs),min(zs),max(zs),v,n,[(q[0],q[2]) for q in v]))
def top_y(parts,x,z):
    """höchste Fläche (kleinstes y, Modell y = unten) der Teile über dem Punkt (x, z); None, wenn keine Fläche darüber liegt.
    parts: Liste von Teilen oder Faces"""
    F=parts if isinstance(parts,Faces) else Faces(parts);best=None
    for x0,x1,z0,z1,v,n,poly in F.f:
        if x<x0 or x>x1 or z<z0 or z>z1 or not _inside2(x,z,poly):continue
        y=v[0][1]-(n[0]*(x-v[0][0])+n[2]*(z-v[0][2]))/n[1]
        if best is None or y<best:best=y
    return best

def _clusters(parts):
    xs=sorted(((min(q[0] for f in P['F'] for q in f['v']),max(q[0] for f in P['F'] for q in f['v']),P) for P in parts),key=lambda t:t[0])
    cl=[]
    for x0,x1,P in xs:
        if cl and x0<=cl[-1][1]+CLUSTER_GAP:cl[-1][1]=max(cl[-1][1],x1);cl[-1][2].append(P)
        else:cl.append([x0,x1,[P]])
    return cl

def _seat_x(gun,old,half):
    """Lage längs (Modell x) ohne Visierschiene: bisheriges Visier als Anhalt.
    Ein Block (Reflex, Kasten, Röhre): dessen Mitte. Kimme hinten und Korn vorn: Halterung beginnt an der Kimme.
    Nur ein Korn (kein hinteres Visierteil): Mitte des Gehäuses."""
    rec=[P for P in gun if P.get('label')=='Gehäuse']
    if not old or all((P.get('label') or '')=='Korn' for P in old):
        b=_bb(rec or gun);return (b[0][0]+b[1][0])/2,'Mitte des Gehäuses (bisher nur Korn)' if old else 'Mitte des Gehäuses'
    cl=_clusters(old)
    if len(cl)==1:return (cl[0][0]+cl[0][1])/2,'Mitte des bisherigen Visiers'
    return cl[0][0]+half,'Halterung ab der bisherigen Kimme (hinteres Visierteil)'

def apply(d):
    """ersetzt die Visierteile von d['m'] durch das VS-Standardvisier des Waffentyps; d['vs'] = Lagedaten (None beim Bogen)"""
    if 'vs' in d:return d
    vid=VS_OF.get(d['name']);ov=choice_of(sheet_of(d['fid']),d['name'])
    if ov:vid=ov[0]
    if vid is None:d['vs']=None;return d
    import export_spec                                # Bezugslängen der Waffentypen (Spec-Maßstab); spät, export_spec lädt sheetmodels
    full=d['m'];gun=[P for P in full.parts if not P.get('sight') and not P.get('late')];old=[P for P in full.parts if P.get('sight')]
    gb=_bb(gun);unit=export_spec.WEAPONS[d['name']][1]/(gb[1][0]-gb[0][0])   # m je Modelleinheit (Länge ohne Visier, wie export_spec)
    k=0.001/unit                                      # Modelleinheiten je mm
    L=V.load(vid);S=L['S'];geo=L['geo']
    mb=_bb([P for P in S.m.parts if P['group']=='mount']);ml,mw=mb[1][0]-mb[0][0],mb[1][2]-mb[0][2]
    sb=_bb(S.m.parts)
    rail=[P for P in gun if P.get('label')=='Visierschiene']
    if rail:
        rb=_bb(rail[:1]);xs=(rb[0][0]+rb[1][0])/2;zs=(rb[0][2]+rb[1][2])/2;src='Mitte der Visierschiene'
    else:
        xs,src=_seat_x(gun,old,-mb[0][0]*k);ob=_bb(old) if old else gb;zs=(ob[0][2]+ob[1][2])/2
    # Visier längs innerhalb der Waffe (Länge und Maßstab des Specs bleiben die der Waffe); eine neue Schiene zählt mit
    rl_mm=min(ml+8,sb[1][0]-sb[0][0])
    ux0,ux1=(sb[0][0],sb[1][0]) if rail else (min(sb[0][0],-rl_mm/2),max(sb[1][0],rl_mm/2))
    lo,hi=gb[0][0]-ux0*k,gb[1][0]-ux1*k
    if xs<lo or xs>hi:xs=min(max(xs,lo),hi);src+=', in die Waffenlänge verschoben'
    # Höhe: höchste Stelle der Waffe unter der Halterung (Raster über die ganze Auflagefläche)
    xsamp=[xs+(mb[0][0]+(mb[1][0]-mb[0][0])*i/8)*k for i in range(9)]
    samp=[(x,zs+mw*k*j/4) for x in xsamp for j in (-2,-1,0,1,2)]
    GF=Faces(gun)
    hits=[h for h in (top_y(GF,x,z) for x,z in samp) if h is not None]
    if not hits:raise ValueError(f'{d["name"]} {d.get("fid")}: keine Waffenfläche unter dem Visier bei x={xs:.1f}, z={zs:.1f}')
    high,low=min(hits),max(hits)
    added=None
    if rail:
        RF=Faces(rail[:1])
        rh=[h for h in (top_y(RF,x,z) for x,z in samp) if h is not None]
        ys=min(rh) if rh else _bb(rail[:1])[0][1]   # Oberkante der Schiene = Socket_Sight
        GW=Faces([P for P in gun if P is not rail[0]])
    else:
        ys=high-RAIL_H_MM*k
        rl=rl_mm*k;rw=RAIL_W_MM*k
        g=Model();g.prism([(xs-rl/2,ys),(xs+rl/2,ys),(xs+rl/2,low),(xs-rl/2,low)],'#000000',zs-rw/2,zs+rw/2,r=min(1.2*k,(low-ys)/3))
        added=g.parts[0];added['label']='Visierschiene';added['vs_rail']=True
        RF=Faces([added]);GW=GF
    gun2=gun+([added] if added is not None else [])
    # Erhöhung: kein Teil des Visiers (Halterung samt Klemmbacken eingeschlossen; die Backen dürfen nur die Schiene umfassen) darf in
    # die Waffe ragen; sonst hebt ein Distanzstück unter der Halterung das Visier an (Seitenschiene am Rohr des Raketenwerfers)
    def depth(y0):
        dd=0.0
        for x,z in samp:                               # Unterseite der Halterung über die ganze Fläche
            t=top_y(GW,x,z)
            if t is not None and t<y0:dd=max(dd,(y0-t)/k)
        for P in S.m.parts:
            for f in P['F']:
                for q in f['v']:
                    t=top_y(GW,xs+q[0]*k,zs+q[2]*k)
                    if t is not None and t<y0+q[1]*k:dd=max(dd,(y0+q[1]*k-t)/k)
        return dd
    lift=depth(ys)
    lift=math.ceil(lift*2)/2+0.5 if lift>0.05 else 0.0   # auf 0,5 mm gerundet, 0,5 mm Luft
    ym=ys-lift*k                                       # Unterkante der Halterung (VS Socket_Mount)
    riser_z=None
    if lift:                                           # Erhöhung steht nur dort auf der Schiene, wo die Waffe nicht höher ist
        zz=[zs+(-mw/2+3+0.5*i)*k for i in range(int(mw-6)*2+1)]
        ok=[all(top_y(RF,x,z) is not None and (top_y(GW,x,z) is None or top_y(GW,x,z)>=ys-1e-6) for x in xsamp[1:-1]) for z in zz]
        best=(0,None);i=0
        while i<len(zz):
            if ok[i]:
                j=i
                while j+1<len(zz) and ok[j+1]:j+=1
                if j-i+1>best[0]:best=(j-i+1,(zz[i],zz[j]))
                i=j+1
            else:i+=1
        if best[1] is None:raise ValueError(f'{d["name"]} {d.get("fid")}: keine freie Auflage für die Erhöhung')
        riser_z=((best[1][0]-zs)/k+0.3,(best[1][1]-zs)/k-0.3)
    # Farben aus den Kanälen der Waffe
    # Kanalfarben wie im Spec bis claude-0.6 (Blatt mit dem bisherigen Visier, Rollen aus der Waffe): so behalten die Teile der Waffe
    # ihre Kanäle, und das neue Visier übernimmt die Farben der Kanäle, die das alte belegt hatte
    gm=Model();gm.parts=gun
    chans=channel_palettes(full,gm,d['palette'],d['pill'],CHANNELS)[0][0]['channels']
    def pick(ch):
        for c in (ch,)+FALLBACK.get(ch,()):
            if chans.get(c):return c,chans[c]
        if ch in ('MT_Energy','MT_Emission'):return ch,chans.get('MT_Accent')   # Leuchtteile bleiben auf Energie-Kanälen
        return ch,None
    if added is not None:
        ch,col=pick('MT_Metal');added['col']=col or S.groups['mount']['col'];added['channel']=ch
    T=lambda q:(xs+q[0]*k,ym+q[1]*k,zs+q[2]*k)
    new=[]
    if lift:
        R=V.Sight();R.group('riser','Erhöhung','MT_Metal','brushed',V.METAL).box('riser',mb[0][0]+2,mb[1][0]-2,0,lift,*riser_z,r=min(0.8,lift/3))
        Sparts=R.m.parts+S.m.parts;groups=dict(S.groups,riser=R.groups['riser'])
    else:Sparts=S.m.parts;groups=S.groups
    for P in Sparts:
        G=groups[P['group']]
        Q=dict(F=[dict(f,v=[T(q) for q in f['v']]) for f in P['F']],emit=P['emit'],dec=[],hull=P.get('hull',True),sight=True,
               label=P['label'],vs_group=P['group'],material=G['material'])
        if P.get('glass'):Q.update(glass=True,col=P['col'],channel=G['channel'])
        else:
            ch,col=pick(G['channel']);Q.update(col=col or P['col'],channel=ch if col else G['channel'])
        new.append(Q)
    m=Model();m.parts=gun2+new+[P for P in full.parts if P.get('late')]   # späte Teile (claude-0.15) ans Ende
    d['m']=m
    line=ym+geo['line_y']*k
    blocked=sorted({P.get('label') or 'ohne Bezeichnung' for P in gun if _blocks(P,xs+sb[1][0]*k,gb[1][0],line,zs)})
    d['vs']=dict(id=vid,   # rail_part: Index der Visierschiene in d['m'].parts
                 info=L['info'],geo=geo,unit=unit,k=k,seat=(xs,ys,zs),mount=(xs,ym,zs),seat_source=src,rail_added=added is not None,
                 rail_part=len(gun) if added is not None else gun.index(rail[0]),riser_mm=lift,line_y=line,blocked_by=blocked,
                 old_labels=sorted({P.get('label') for P in old if P.get('label')}),channels=chans)
    if ov:d['vs']['choice']=ov[1]   # nur bei Ausnahmen und Typregeln, Lagedaten der übrigen Blätter unverändert
    return d

def _blocks(P,x0,x1,line,zs):
    """Teil der Waffe ragt vor dem Visier über die Visierlinie (Strahl entlang x in Höhe line bei z = zs)"""
    b=_bb([P])
    if b[1][0]<x0 or b[0][0]>x1 or not (b[0][2]<=zs<=b[1][2]) or b[0][1]>line:return False
    n=max(2,int((min(x1,b[1][0])-max(x0,b[0][0]))/2))
    for i in range(n+1):
        x=max(x0,b[0][0])+(min(x1,b[1][0])-max(x0,b[0][0]))*i/n
        t=top_y([P],x,zs)
        if t is not None and t<line:return True
    return False
