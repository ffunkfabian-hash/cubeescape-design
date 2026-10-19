"""Geometrie-Spec der Konzeptblätter: claude/output/sheets/KXnn.geo.json und VSnn.geo.json (Format: claude/docs/geometry-spec.md).

   python3 claude/generator/export_geo.py             # alle 159 Geo-Specs schreiben (150 Waffen, VS01–VS09)
   python3 claude/generator/export_geo.py KG02 VS02   # nur diese
   python3 claude/generator/export_geo.py --check     # nur vergleichen; Exit 1, wenn eine Datei fehlt oder veraltet ist

Bauquelle für Toolgen (Etappe TG-A, Umsetzungsplan claude/docs/umsetzungsplan-modelle.md › 3): das Netz jedes Teils in Metern im
Toolgen-Rahmen (vorn −Y, oben +Z, links +X, Ursprung Socket_Hand bzw. bei der Visier-Serie Socket_Mount), dazu Primitiv-Hinweise,
Aufkleber als Polygone, Griff, Stützhand, Visier und Anker. Dieselben Python-Modelle wie Blatt und Weapon-Spec (sheetmodels.py,
vsmodels.py); ohne numpy, ohne Bildstufe. Die Dateien werden nicht committet (Release-Asset geo/), im Repo stehen nur ihre Hashes.
"""
from cepaths import E3D,OUT
import hashlib,json,math,os,re,sys
sys.path.insert(0,E3D)
import sheetmodels,wtypes
import vsmodels as V
import export_spec as ES
import export_sight as EX

FORMAT='cubeescape-design/geometry-spec'
FORMAT_VERSION=1
CLAUDE_VERSION='0.13'
DIGITS=5                # Meter mit 5 Nachkommastellen = 0,01 mm (feiner als die 0,5-mm-Regel, keine Kante fällt beim Runden weg)
COPLANAR_M=0.0005       # Toolgen-Regel: gleichgerichtete Flächen verschiedener Teile mindestens 0,5 mm auseinander (TECHNIK › Determinismus)
OVERLAP_MIN_M2=1e-6     # Überdeckung ab 1 mm² zählt (darunter nur Berührung an Kanten, Rundungsrauschen)
DECAL_OFFSET_UNITS=0.4  # eng.render: Aufkleber 0,4 Modelleinheiten über der Fläche (nur Zeichnung)
M2B=ES.M2B              # Modell (vorn x, unten y, links z) -> Toolgen/Blender (vorn −Y, oben +Z, links +X); Drehung, det = +1
TARGET_AXES='XYZ'
MODEL_TO_TARGET_AXIS=['Y','Z','X']   # Modellachse x/y/z -> Zielachse
PLANE_NORMAL={'z+':(0,0,1),'z-':(0,0,-1),'x+':(1,0,0),'x-':(-1,0,0),'y-':(0,-1,0),'y+':(0,1,0)}

def rd(v):return round(v,DIGITS)+0.0
def r4(v):return round(v,4)+0.0
def _dot(a,b):return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def _cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def _norm(v):
    L=math.sqrt(_dot(v,v));return [c/L for c in v] if L>1e-15 else [0.0,0.0,0.0]
def newell(pts):
    n=[0.0,0.0,0.0]
    for k in range(len(pts)):
        (x0,y0,z0),(x1,y1,z1)=pts[k],pts[(k+1)%len(pts)]
        n[0]+=(y0-y1)*(z0+z1);n[1]+=(z0-z1)*(x0+x1);n[2]+=(x0-x1)*(y0+y1)
    return n
def _bb(pts):return [[min(q[i] for q in pts) for i in range(3)],[max(q[i] for q in pts) for i in range(3)]]
def _verts(parts):return [q for P in parts for f in P['F'] for q in f['v']]

class Frame:
    """Modellpunkt -> Zielpunkt in m: p = unit · M · (q − origin); Richtungen nur gedreht"""
    def __init__(s,unit,origin):s.u=unit;s.o=list(origin)
    def raw(s,q):
        d=[q[i]-s.o[i] for i in range(3)];return [s.u*sum(M2B[r][c]*d[c] for c in range(3)) for r in range(3)]
    def p(s,q):return [rd(c) for c in s.raw(q)]
    def d(s,v):return [sum(M2B[r][c]*v[c] for c in range(3)) for r in range(3)]

# ---------------------------------------------------------------- Netz
def signed_volume(verts,faces):
    """Volumen eines Netzes (Fächer je Fläche, Divergenzsatz); > 0 bei geschlossener Hülle mit Normalen nach außen"""
    v=0.0
    for f in faces:
        a=verts[f[0]]
        for i in range(1,len(f)-1):v+=_dot(a,_cross(verts[f[i]],verts[f[i+1]]))/6
    return v
def closed_components(faces):
    """Zusammenhangskomponenten über gemeinsame Kanten; je Komponente (Flächenindizes, geschlossen ja/nein).
    Geschlossen = jede Kante gehört genau zwei Flächen."""
    edges={}
    for k,f in enumerate(faces):
        for i in range(len(f)):edges.setdefault(frozenset((f[i],f[(i+1)%len(f)])),[]).append(k)
    seen=set();out=[]
    for s0 in range(len(faces)):
        if s0 in seen:continue
        comp=[];stack=[s0];seen.add(s0)
        while stack:
            k=stack.pop();comp.append(k);f=faces[k]
            for i in range(len(f)):
                for j in edges[frozenset((f[i],f[(i+1)%len(f)]))]:
                    if j not in seen:seen.add(j);stack.append(j)
        closed=all(len(edges[frozenset((faces[k][i],faces[k][(i+1)%len(faces[k])]))])==2 for k in comp for i in range(len(faces[k])))
        out.append((sorted(comp),closed))
    return out
def orient(faces,verts):
    """Geschlossene Komponenten: Umlaufsinn über die Kantennachbarschaft angleichen, dann Volumen positiv (Normalen nach außen) –
    unabhängig von der gespeicherten Normale. Offene Teile (Ringhälften, Mäntel, Scheiben) behalten die gespeicherte Normale.
    Liefert die Zahl der Flächen, die gegen die gespeicherte Normale gedreht wurden."""
    fixed=0
    for comp,closed in closed_components(faces):
        if not closed:continue
        cs=set(comp);start=comp[0];want={start:faces[start]};stack=[start]
        de={}
        for k in comp:
            f=faces[k]
            for i in range(len(f)):de.setdefault(frozenset((f[i],f[(i+1)%len(f)])),[]).append(k)
        ok=True
        while stack:
            k=stack.pop();f=want[k]
            for i in range(len(f)):
                a,b=f[i],f[(i+1)%len(f)]
                for j in de[frozenset((a,b))]:
                    if j==k or j not in cs:continue
                    g=faces[j];has=any(g[t]==a and g[(t+1)%len(g)]==b for t in range(len(g)))   # gleiche Richtung -> umdrehen
                    gg=g[::-1] if has else g
                    if j in want:
                        if want[j]!=gg:ok=False
                    else:want[j]=gg;stack.append(j)
        if not ok:continue   # nicht orientierbar: gespeicherte Normale bleibt
        vol=signed_volume(verts,[want[k] for k in comp])
        if abs(vol)<1e-15:continue   # flach (Scheibe beidseitig)
        for k in comp:
            g=want[k][::-1] if vol<0 else want[k]
            if g!=faces[k]:faces[k]=g;fixed+=1
    return fixed
def mesh(parts,F):
    """Netz aus Modellteilen (eine oder mehrere eng-Teile): gemeinsame Ecken (auf DIGITS gerundet), Flächen als Indexlisten.
    Umlaufsinn: zuerst nach der im Modell gespeicherten Normale (die das Blatt zeichnet), dann je eng-Teil geschlossene Hüllen
    nach Kantennachbarschaft und positivem Volumen (orient); normal_fixes = Flächen, deren gespeicherte Normale nach innen zeigte."""
    verts=[];idx={};faces=[];hard=[];stat=dict(dropped=0,normal_fixes=0)
    for P in parts:
        pf=[];ph=[]
        for f in P['F']:
            ids=[]
            for q in f['v']:
                p=tuple(F.p(q));i=idx.get(p)
                if i is None:i=idx[p]=len(verts);verts.append(list(p))
                if not ids or ids[-1]!=i:ids.append(i)
            while len(ids)>1 and ids[0]==ids[-1]:ids.pop()
            if len(set(ids))<3:stat['dropped']+=1;continue
            n=newell([verts[i] for i in ids])
            if _dot(n,F.d(f['n']))<0:ids=ids[::-1]
            pf.append(ids);ph.append(1 if f['hard'] else 0)
        stat['normal_fixes']+=orient(pf,verts)
        faces+=pf;hard+=ph
    return dict(vertices=verts,faces=faces,hard=hard),stat

def triangles(m):return sum(len(f)-2 for f in m['faces'])

# ---------------------------------------------------------------- Primitiv-Hinweis
def _axis(n):
    """Index der Modellachse, wenn die Normale achsparallel ist"""
    for a in range(3):
        if abs(abs(n[a])-1)<1e-9 and all(abs(n[b])<1e-9 for b in range(3) if b!=a):return a
    return None
def _regular(pp):
    """Mitte und Radius, wenn die Punkte (2D) auf einem Kreis liegen (gleiche Abstände)"""
    c=(sum(p[0] for p in pp)/len(pp),sum(p[1] for p in pp)/len(pp));r=[math.hypot(p[0]-c[0],p[1]-c[1]) for p in pp]
    R=sum(r)/len(r)
    if R<=1e-9 or max(abs(x-R) for x in r)>1e-6*max(1.0,R):return None,None
    n=len(pp);step=2*math.pi/n   # gleichmäßige Winkel (regelmäßiges Vieleck), sonst kein Zylinder
    for i in range(n):
        a0=math.atan2(pp[i][1]-c[1],pp[i][0]-c[0]);a1=math.atan2(pp[(i+1)%n][1]-c[1],pp[(i+1)%n][0]-c[0])
        if abs(abs(math.remainder(a1-a0,2*math.pi))-step)>1e-6:return None,None
    return c,R
def primitive(P,F):
    """Bauweg eines eng-Teils, wo er sich aus der Flächenfolge ergibt: Prisma (eng.prism, ext.prism_y, Kästen der Visier-Serie),
    Zylinder (eng.cyl, tlib C, gerade Vieleck-Läufe), Kegelstumpf (ext.frustum). Sonst None (Netz allein maßgeblich)."""
    Fs=P['F']
    if len(Fs)<5:return None
    a,b=Fs[0],Fs[1];n=len(a['v'])
    if n<3 or len(Fs)!=n+2 or len(b['v'])!=n or any(len(f['v'])!=4 for f in Fs[2:]):return None
    ax=_axis(a['n'])
    if ax is None or _axis(b['n'])!=ax or a['n'][ax]*b['n'][ax]>=0:return None
    ca=[q[ax] for q in a['v']];cb=[q[ax] for q in b['v']]
    if max(ca)-min(ca)>1e-6 or max(cb)-min(cb)>1e-6 or abs(ca[0]-cb[0])<1e-9:return None
    o=[k for k in range(3) if k!=ax]
    pa=[(q[o[0]],q[o[1]]) for q in a['v']];pb=[(q[o[0]],q[o[1]]) for q in b['v']]
    key=lambda pp:sorted((round(x,6),round(y,6)) for x,y in pp)
    smooth=not any(f['hard'] for f in Fs[2:])
    tax=MODEL_TO_TARGET_AXIS[ax];others=[i for i,c in enumerate(TARGET_AXES) if c!=tax]
    def end(c,coord):
        q=[0.0,0.0,0.0];q[ax]=coord;q[o[0]],q[o[1]]=c;return F.p(q)
    (c0,R0),(c1,R1)=_regular(pa),_regular(pb)
    if smooth and n>=6 and c0 and c1 and math.hypot(c0[0]-c1[0],c0[1]-c1[1])<1e-6:
        e0,e1=end(c1,cb[0]),end(c0,ca[0])   # Start = Fläche F[1], Ende = F[0] (eng.cyl: F[0] vorn bei x1)
        if abs(R0-R1)<=1e-6*max(1.0,R0):
            return dict(type='cylinder',axis=tax,start_m=e0,end_m=e1,radius_m=rd(R0*F.u),segments=n,first_vertex_m=F.p(a['v'][0]))
        return dict(type='cone',axis=tax,start_m=e0,end_m=e1,radius_start_m=rd(R1*F.u),radius_end_m=rd(R0*F.u),segments=n,
                    first_vertex_m=F.p(a['v'][0]))
    if key(pa)!=key(pb):return None
    prof=[F.p(q) for q in a['v']];rng=sorted([F.p(a['v'][0])[TARGET_AXES.index(tax)],F.p(b['v'][0])[TARGET_AXES.index(tax)]])
    return dict(type='prism',axis=tax,profile_axes=''.join(TARGET_AXES[i] for i in others),
                profile_m=[[p[i] for i in others] for p in prof],range_m=rng,smooth_sides=smooth)

# ---------------------------------------------------------------- Koplanar-Prüfung
def _basis(n):
    e=[1.0,0.0,0.0] if abs(n[0])<0.9 else [0.0,1.0,0.0]
    u=_norm(_cross(n,e));return u,_cross(n,u)
def _area2(p):return sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2
def _ears(p):
    """Dreiecke eines einfachen Polygons (2D, gegen den Uhrzeigersinn) durch Ohrenschneiden; Fächer als Rückfall"""
    pts=list(p)
    if _area2(pts)<0:pts=pts[::-1]
    tri=[];idx=list(range(len(pts)));guard=0
    cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    while len(idx)>3 and guard<10000:
        guard+=1;found=False
        for k in range(len(idx)):
            i0,i1,i2=idx[k-1],idx[k],idx[(k+1)%len(idx)];a,b,c=pts[i0],pts[i1],pts[i2]
            if cr(a,b,c)<=1e-18:continue
            if any(cr(a,b,pts[j])>=0 and cr(b,c,pts[j])>=0 and cr(c,a,pts[j])>=0 for j in idx if j not in (i0,i1,i2)):continue
            tri.append((a,b,c));idx.pop(k);found=True;break
        if not found:break
    if len(idx)==3:tri.append(tuple(pts[i] for i in idx))
    elif len(idx)>3:tri+=[(pts[idx[0]],pts[idx[i]],pts[idx[i+1]]) for i in range(1,len(idx)-1)]
    return [t for t in tri if abs(_area2(t))>1e-18]
def _clip(subj,clip):
    """Sutherland-Hodgman: konvexes Polygon subj an konvexem clip (beide gegen den Uhrzeigersinn)"""
    out=list(subj)
    for i in range(len(clip)):
        a,b=clip[i],clip[(i+1)%len(clip)];inp=out;out=[]
        if not inp:break
        side=lambda p:(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        for j in range(len(inp)):
            p,q=inp[j],inp[(j+1)%len(inp)];sp,sq=side(p),side(q)
            if sp>=0:out.append(p)
            if (sp>=0)!=(sq>=0):
                t=sp/(sp-sq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return out
def _ccw(t):return t if _area2(t)>0 else t[::-1]
def overlap(A,B):
    """Fläche der Überdeckung zweier ebener Polygone (2D, beliebig einfach)"""
    s=0.0
    for ta in _ears(A):
        for tb in _ears(B):
            c=_clip(_ccw(ta),_ccw(tb))
            if len(c)>=3:s+=abs(_area2(c))
    return s
NORMAL_CELLS=100                      # Zellen der Normalen-Rundung (0,01); Nachbarzellen werden mitgeprüft
PARALLEL_COS=math.cos(math.radians(1.0))   # gleichgerichtet = Normalen höchstens 1° auseinander
_NEIGH=[(a,b,c) for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1)]
def coplanar(parts_mesh,look=None,limit=COPLANAR_M):
    """Gleichgerichtete Flächen verschiedener Teile mit Abstand unter limit, die sich (projiziert) um mindestens 1 mm² überdecken:
    Z-Fighting-Gefahr nach Toolgens Koplanar-Regel. Entgegengesetzte Flächen (Teil sitzt auf Teil) zählen nicht.
    look: Teil-ID -> (Kanal, Material, leuchtend, Glas); same_look = beide gleich (Flackern dann kaum sichtbar, Toolgen-Präzedenz
    Impulsgewehr Zellschacht/Energiezelle). parts_mesh: Liste (Teil-ID, Netz). Liefert Befunde, sortiert, je Teilpaar der kleinste Abstand und die größte Überdeckung."""
    groups={}
    for pid,m in parts_mesh:
        V_=m['vertices']
        for fi,f in enumerate(m['faces']):
            pts=[V_[i] for i in f];n=_norm(newell(pts))
            if n==[0.0,0.0,0.0]:continue
            groups.setdefault(tuple(round(c*NORMAL_CELLS) for c in n),[]).append((pid,fi,pts,n))
    found={};seen=set()
    Rmax=max((math.sqrt(_dot(v,v)) for _,m in parts_mesh for v in m['vertices']),default=0.0)
    window=limit+2*math.sin(math.radians(2.0))*Rmax   # Zellnormale gegen Flächennormale: bis ~2° Neigung über die Modellgröße
    for key in sorted(groups):
        # Flächen dieser Zelle und der Nachbarzellen (Rundungsgrenzen); Abstand entlang der gemeinsamen Normale der Zelle
        L=[t for dk in _NEIGH for t in groups.get(tuple(key[i]+dk[i] for i in range(3)),())]
        nk=_norm([sum(t[3][i] for t in groups[key]) for i in range(3)])
        L=sorted(((_dot(nk,t[2][0]),)+t for t in L),key=lambda t:t[0])
        own={(t[0],t[1]) for t in groups[key]}
        for i in range(len(L)):
            di,pa,fa,A,na=L[i]
            for j in range(i+1,len(L)):
                dj,pb,fb,B,nb=L[j]
                if dj-di>=window:break          # grobes Fenster; exakter Abstand unten
                if pa==pb or ((pa,fa) not in own and (pb,fb) not in own):continue
                pair=tuple(sorted(((pa,fa),(pb,fb))))
                if pair in seen or _dot(na,nb)<PARALLEL_COS:continue
                dist=max(abs(_dot(na,[B[0][k]-A[0][k] for k in range(3)])),abs(_dot(nb,[B[0][k]-A[0][k] for k in range(3)])))
                if dist>=limit:continue
                u,v=_basis(na);a2=[(_dot(p,u),_dot(p,v)) for p in A];b2=[(_dot(p,u),_dot(p,v)) for p in B]
                if (max(p[0] for p in a2)<=min(p[0] for p in b2) or max(p[0] for p in b2)<=min(p[0] for p in a2) or
                    max(p[1] for p in a2)<=min(p[1] for p in b2) or max(p[1] for p in b2)<=min(p[1] for p in a2)):continue
                ov=overlap(a2,b2)
                if ov<OVERLAP_MIN_M2:continue
                seen.add(pair)
                k=tuple(sorted((pa,pb)))
                e=found.get(k)
                if e is None:found[k]=e=dict(parts=list(k),distance_m=dist,overlap_m2=ov,normal=[r4(c) for c in na],faces=0,
                                             same_look=bool(look) and look[k[0]]==look[k[1]])
                e['faces']+=1
                if dist<e['distance_m']:e.update(distance_m=dist,normal=[r4(c) for c in na])   # kleinster Abstand und
                e['overlap_m2']=max(e['overlap_m2'],ov)                                       # größte Überdeckung, unabhängig
    out=[dict(e,distance_m=rd(e['distance_m']),overlap_m2=round(e['overlap_m2'],8)) for _,e in sorted(found.items())]
    return out

# ---------------------------------------------------------------- Griff, Stützhand
def _hull2(pts):
    pts=sorted(set(pts))
    if len(pts)<3:return pts
    cr=lambda o,a,b:(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0:up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def _chord_x(poly,y):
    """x-Bereich der Schnittlinie y = konst. mit einem Polygon (x, y)"""
    xs=[]
    for i in range(len(poly)):
        (x0,y0),(x1,y1)=poly[i],poly[(i+1)%len(poly)]
        if (y0-y)*(y1-y)<=0 and y0!=y1:xs.append(x0+(y-y0)*(x1-x0)/(y1-y0))
    return (min(xs),max(xs)) if xs else None

def _chord_dir(poly,p,d):
    """Länge der Sehne eines konvexen Polygons auf der Geraden durch p in Richtung d (Einheitsvektor)"""
    ts=[]
    for i in range(len(poly)):
        a,b=poly[i],poly[(i+1)%len(poly)];e=(b[0]-a[0],b[1]-a[1]);den=d[0]*e[1]-d[1]*e[0]
        if abs(den)<1e-15:continue
        w=(a[0]-p[0],a[1]-p[1]);t=(w[0]*e[1]-w[1]*e[0])/den;u=(w[0]*d[1]-w[1]*d[0])/den
        if -1e-9<=u<=1+1e-9:ts.append(t)
    return max(ts)-min(ts) if ts else 0.0
GRIP_SLICES=(0.25,0.85)   # Schnitte ab Oberkante (Anteil der Höhe): oben unter dem Gehäuseansatz, unten über der Griffkappe
def grip(P,pid,F,trigger):
    """Griffachse aus dem Seitenumriss des Griffteils (konvexe Hülle in Modell x/y): Mitte zweier waagrechter Schnitte,
    verlängert bis Unter- und Oberkante; Neigung positiv = oben nach vorn (Toolgen grip_tilt_degrees)."""
    vs=_verts([P]);b=_bb(vs);H=_hull2([(q[0],q[1]) for q in vs]);zc=(b[0][2]+b[1][2])/2
    ytop,ybot=b[0][1],b[1][1];h=ybot-ytop;wx=b[1][0]-b[0][0]
    if h>=wx:
        mids=[]
        for t in GRIP_SLICES:
            y=ytop+t*h;c=_chord_x(H,y);mids.append(((c[0]+c[1])/2,y))
        (xt,yt),(xb,yb)=mids;dx,dy=xt-xb,yt-yb
        at=lambda y:(xb+(y-yb)*dx/dy,y,zc)
        bottom,top=at(ybot),at(ytop);tilt=math.degrees(math.atan2(dx,-dy))
        L_=math.hypot(dx,dy);m0=at(ytop+0.5*h);depth=_chord_dir(H,(m0[0],m0[1]),(-dy/L_,dx/L_))   # quer zur Griffachse
        method='Seitenumriss (konvexe Hülle in Modell x/y): Mitte der Schnitte bei %d %% und %d %% der Höhe ab Oberkante, bis Unter-/Oberkante verlängert'%tuple(round(100*t) for t in GRIP_SLICES)
    else:   # liegender Griff (Schwert, Glefe, Stangen): Achse längs, Neigung 90°
        bottom,top=(b[0][0],(ytop+ybot)/2,zc),(b[1][0],(ytop+ybot)/2,zc);tilt=90.0;depth=h
        method='liegendes Griffteil (länger als hoch): Achse entlang Modell x durch die Mitte, hinten -> vorn; Neigung 90°'
    return dict(part=pid,grip_axis_m=[F.p(bottom),F.p(top)],grip_tilt_degrees=round(tilt,2),
                trigger_m=trigger[1] if trigger else None,trigger_part=trigger[0] if trigger else None,
                cross_section_m=dict(depth_m=rd(depth*F.u),width_m=rd((b[1][2]-b[0][2])*F.u),
                                     note='depth = Sehne quer zur Griffachse in halber Höhe, width = Breite (X)'),
                method=method)

def section_x(P,x):
    """Schnitt eines Teils mit der Ebene Modell x = konst.: (y-Bereich, z-Bereich) der Schnittpunkte aller Flächenkanten"""
    pts=[]
    for f in P['F']:
        v=f['v']
        for i in range(len(v)):
            a,b=v[i],v[(i+1)%len(v)]
            if (a[0]-x)*(b[0]-x)<=0 and a[0]!=b[0]:
                t=(x-a[0])/(b[0]-a[0]);pts.append((a[1]+t*(b[1]-a[1]),a[2]+t*(b[2]-a[2])))
            elif a[0]==x:pts.append((a[1],a[2]))
    if not pts:return None
    return (min(p[0] for p in pts),max(p[0] for p in pts)),(min(p[1] for p in pts),max(p[1] for p in pts))

def support(P,pid,pos_model,F,anchor):
    s=section_x(P,pos_model[0])
    if s is None:return dict(part=pid,radius_m=None,reason='Ebene durch Socket_SupportHand schneidet das Teil nicht')
    (y0,y1),(z0,z1)=s
    return dict(part=pid,radius_m=dict(half_height_m=rd((y1-y0)/2*F.u),half_width_m=rd((z1-z0)/2*F.u)),
                section_center_m=F.p(((pos_model[0]),(y0+y1)/2,(z0+z1)/2)),anchor_m=anchor,
                method='Querschnitt des Teils in der Ebene quer zur Laufachse durch Socket_SupportHand (Höhe Z, Breite X)',reason=None)

# ---------------------------------------------------------------- Visier
def sight_block(geo,info,at,scale_m,vid,sight_sha,mount_m,weapon_top_z=None):
    """Visierblock aus der Visier-Serie; at(x_mm, y_mm) -> Zielpunkt, scale_m = Meter je mm des Visiers in diesem Rahmen"""
    win=geo['window'];tube=geo.get('tube');ly=geo['line_y']
    kind,window_kind=ES.SIGHT_TYPES[info['type']]
    rear=at(win['x0'],ly);ret=at(win['glass_x'],ly);eye=at(tube['eye_x'],ly) if tube else rear
    eye_r=(tube['eye_r'] if tube else min(win['w'],win['h'])/2)*scale_m
    out=dict(present=True,id=vid,kind=kind,type=info['type'],frame=info['frame'],window_kind=window_kind,
             sight_spec=dict(file=f'{vid}.spec.json',format=EX.FORMAT,format_version=EX.FORMAT_VERSION,sha256=sight_sha),
             window=dict(shape=win['shape'],width_m=rd(win['w']*scale_m),height_m=rd(win['h']*scale_m),corner_radius_m=rd(win['r']*scale_m),
                         view_axis_m=[0.0,-1.0,0.0]),
             tube=dict(length_m=rd((tube['x1']-tube['x0'])*scale_m),lens_radius_m=rd(tube['lens_r']*scale_m),eye_radius_m=rd(tube['eye_r']*scale_m),
                       bore_radius_m=rd(tube['bore_r']*scale_m)) if tube else None,
             socket_mount_m=mount_m,socket_sight_rear_m=rear,socket_reticle_m=ret,socket_eye_m=eye,eye_radius_m=rd(eye_r),
             socket_eye_source=('Mitte des Okularglases (Röhre, Sight-Spec Socket_Eye)' if tube else
                                'Vorschlag: hinterer Fensterrand auf der Visierlinie (Sight-Spec Socket_Sight), Radius = halbe kleinere Fensterseite'),
             line=dict(start_m=rear,direction=[0.0,-1.0,0.0],height_above_mount_m=rd(ret[2]-mount_m[2]),
                       above_body_top_m=rd(ret[2]-weapon_top_z) if weapon_top_z is not None else None),
             note='socket_sight_rear_m = Socket_Sight des Sight-Specs (hinteres Visierende auf der Visierlinie, Toolgens Socket_Sight-Regel); '
                  'anchors.Socket_Sight dieses Specs = Weapon-Spec (Oberkante der Visierschiene unter der Halterung)')
    return out

DECAL_SLACK_M=0.001
def decal_on_part(dc,pb):
    """Aufkleber liegt im Hüllquader seines Teils (1 mm Spiel)"""
    return all(pb[0][k]-DECAL_SLACK_M<=v[k]<=pb[1][k]+DECAL_SLACK_M for v in dc['polygon_m'] for k in range(3))

def ascii_label(label):
    if not label:return 'Part'
    t=label.translate(str.maketrans({'ä':'ae','ö':'oe','ü':'ue','Ä':'Ae','Ö':'Oe','Ü':'Ue','ß':'ss'}))
    return ''.join(w[:1].upper()+w[1:] for w in re.findall(r'[A-Za-z0-9]+',t)) or 'Part'

def sha(txt):return hashlib.sha256(txt.encode('utf-8')).hexdigest()
def read_spec(sid):
    """Weapon- bzw. Sight-Spec von der Platte (Text, Daten): der Geo-Spec verweist mit sha256 auf genau diese Datei; aktuell halten
    test_spec.py und export_sight.py --check (sonst zuerst export_spec.py / export_sight.py)"""
    fn=os.path.join(OUT,f'{sid}.spec.json')
    if not os.path.exists(fn):sys.exit(f'{sid}.spec.json fehlt – zuerst python3 claude/generator/export_spec.py bzw. export_sight.py')
    with open(fn,encoding='utf-8') as f:txt=f.read()
    return txt,json.loads(txt)
def _decal3(plane,val,pts):return ES._decal3(plane,val,pts)

AXES=dict(model=dict(x='vorn (Mündung)',y='unten',z='links'),target=dict(system='Toolgen/Blender',forward='-Y',up='+Z',left='+X',unit='m'),
          matrix_model_to_target=M2B)

# ---------------------------------------------------------------- Sehne (Bogen, Armbrust)
STRING_TYPES=('Bogen','Schwere Armbrust')
LIMB_LABELS=('Wurfarm','Wurfarmkappe');CAM_LABELS=('Umlenkrolle','Rollenachse');RISER_LABELS=('Mittelstück','Griff','Bogenblock')
ARROW_LABELS=('Pfeil','Bolzen');REST_LABELS=('Pfeilauflage','Führungsrinne')
def _segment(m):
    """Sehnenteil als Strecke: die zwei am weitesten entfernten Ecken, Enden = Mitte der Ecken nahe diesen (Querschnitt der Sehne)"""
    V=m['vertices'];a,b=max(((p,q) for i,p in enumerate(V) for q in V[i+1:]),key=lambda t:math.dist(*t))
    d=[b[k]-a[k] for k in range(3)];L=math.sqrt(_dot(d,d));u=[c/L for c in d]
    t=[_dot([v[k]-a[k] for k in range(3)],u) for v in V];w=min(L*0.25,0.004)   # Ecken bis 4 mm vom Ende = Endquerschnitt
    end=lambda sel:[sum(v[k] for v in sel)/len(sel) for k in range(3)]
    return end([v for v,x in zip(V,t) if x<=w]),end([v for v,x in zip(V,t) if x>=L-w])
def string_block(parts,name):
    """Sehne aus dem Modell (Teile „Sehne“) für Toolgens Sehne, Pfeil und Zugclip (Entscheidung des Nutzers 19.10.2026: Bogen sofort in TG-A):
    Strecken der Sehnenteile, Spitzen = äußere Enden entlang der Spannachse, Nockpunkt = Schnitt der Sehne mit der Pfeilachse (Ruhe),
    Pfeilachse aus Pfeil/Bolzen (sonst durch die Pfeilauflage), Pfeilauflage/Führungsrinne = Oberkante Mitte."""
    if name not in STRING_TYPES:return None
    by=lambda labs:[p for p in parts if p['label'] in labs and not p['sight']]
    strings=by(('Sehne',))
    if not strings:return dict(present=False,reason='keine Sehne im Modell')
    segs=[_segment(p['mesh']) for p in strings];ends=[e for sg in segs for e in sg]
    ext=[max(e[k] for e in ends)-min(e[k] for e in ends) for k in range(3)];ax=ext.index(max(ext))
    tips=[min(ends,key=lambda e:e[ax]),max(ends,key=lambda e:e[ax])]
    arrow=by(ARROW_LABELS);rest=by(REST_LABELS)
    if arrow:
        A=max(arrow,key=lambda p:p['bounds_m'][1][1]-p['bounds_m'][0][1]);b=A['bounds_m'];cx,cz=(b[0][0]+b[1][0])/2,(b[0][2]+b[1][2])/2
        axis=dict(part=A['id'],label=A['label'],rear_m=[rd(cx),b[1][1],rd(cz)],tip_m=[rd(cx),b[0][1],rd(cz)],direction=[0.0,-1.0,0.0],
                  radius_m=rd(min(b[1][0]-b[0][0],b[1][2]-b[0][2])/2),source=f'Mittellinie von {A["id"]} ({A["label"]}), Hüllquader')
    elif rest:
        b=rest[0]['bounds_m'];cx=(b[0][0]+b[1][0])/2
        axis=dict(part=None,label=None,rear_m=None,tip_m=None,direction=[0.0,-1.0,0.0],radius_m=None,
                  through_m=[rd(cx),rd((b[0][1]+b[1][1])/2),b[1][2]],source=f'kein Pfeil im Modell: Linie entlang −Y über der Oberkante von {rest[0]["id"]} ({rest[0]["label"]})')
    else:return dict(present=False,reason='weder Pfeil/Bolzen noch Pfeilauflage im Modell')
    ref=axis['rear_m'] or axis['through_m']
    hits=[]
    for a,b in segs:
        lo,hi=min(a[ax],b[ax]),max(a[ax],b[ax])
        if lo-1e-6<=ref[ax]<=hi+1e-6:
            t=0.0 if abs(b[ax]-a[ax])<1e-12 else (ref[ax]-a[ax])/(b[ax]-a[ax]);hits.append([a[k]+t*(b[k]-a[k]) for k in range(3)])
    nock=max(hits,key=lambda p:p[1]) if hits else None
    nsrc='Schnitt der Sehne (Strecken der Sehnenteile) mit der Ebene der Pfeilachse quer zur Spannachse, Ruhelage'
    if nock is None:   # Sehnenhälften enden kurz vor der Mitte (Armbrust): Mitte ihrer inneren Enden
        inner=[min(sg,key=lambda e:abs(e[ax]-ref[ax])) for sg in segs];nock=[sum(e[k] for e in inner)/len(inner) for k in range(3)]
        nsrc='Sehnenhälften treffen sich nicht in der Ebene der Pfeilachse: Mitte ihrer inneren Enden, Ruhelage'
    if rest:
        R=rest[0];b=R['bounds_m'];rp=[rd((b[0][0]+b[1][0])/2),rd((b[0][1]+b[1][1])/2),b[1][2]];rsrc=f'Oberkante Mitte von {R["id"]} ({R["label"]})'
    else:
        b=next(p for p in parts if p['id']==axis['part'])['bounds_m']
        rp=[axis['rear_m'][0],rd((b[0][1]+b[1][1])/2),b[0][2]];rsrc=f'keine Auflage im Modell: Unterkante Mitte von {axis["part"]} ({axis["label"]})'
    near=lambda tip:min(by(LIMB_LABELS+CAM_LABELS),key=lambda p:math.dist(tip,[(p['bounds_m'][0][k]+p['bounds_m'][1][k])/2 for k in range(3)]))['id'] if by(LIMB_LABELS+CAM_LABELS) else None
    return dict(present=True,kind='crossbow' if TARGET_AXES[ax]=='X' else 'bow',span_axis=TARGET_AXES[ax],
                limb_tips_m=[[rd(c) for c in t] for t in tips],limb_tip_parts=[near(t) for t in tips],
                nock_m=[rd(c) for c in nock],
                nock_source=nsrc,
                arrow_axis=axis,arrow_rest_m=rp,arrow_rest_source=rsrc,
                nock_behind_hand_m=rd(nock[1]),
                string_parts=[p['id'] for p in strings],string_segments_m=[[[rd(c) for c in a],[rd(c) for c in b]] for a,b in segs],
                string_length_m=rd(sum(math.dist(a,b) for a,b in segs)),
                limb_parts=[p['id'] for p in by(LIMB_LABELS)],cam_parts=[p['id'] for p in by(CAM_LABELS)],
                riser_parts=[p['id'] for p in by(RISER_LABELS)],
                note='Bogen: Spannachse Z (Wurfarme oben/unten), Armbrust: X (Wurfarme links/rechts). nock_behind_hand_m = Nockpunkt hinter Socket_Hand entlang +Y (Bogen: Spannhöhe am Griff; Armbrust negativ, Schloss vor dem Griff). '
                     'Toolgen setzt Socket_Nock auf nock_m, den Pfeil entlang arrow_axis und die Sehne zwischen limb_tips_m und nock_m (Zugclip zieht nock_m nach +Y)')

# ---------------------------------------------------------------- Waffenblatt
def build_weapon(sheet):
    d=sheetmodels.load(sheet);full=d['m'];spec_txt,spec=read_spec(sheet)
    allparts=list(enumerate(full.parts));ids=[f'p{i:02d}' for i in range(len(full.parts))]
    gun=[(i,P) for i,P in allparts if not P.get('sight')];sight_parts=[(i,P) for i,P in allparts if P.get('sight')]
    unit=ES._scale(d['name'],full)[0]
    an,_=ES._anchors(d,gun,sight_parts,allparts,ids)
    F=Frame(unit,an['Socket_Hand'][0])
    sp={p['id']:p for p in spec['parts']}
    node={}
    for it in spec['moving_parts']['items']:
        for pid in it['parts'] or []:node[pid]=it['toolgen_node']
    parts=[];meshes=[];stats=dict(dropped=0,normal_fixes=0)
    for i,P in allparts:
        pid=ids[i];s=sp[pid];m,st=mesh([P],F)
        for k in stats:stats[k]+=st[k]
        meshes.append((pid,m))
        parts.append(dict(id=pid,name=f'SM_PG_{ascii_label(s["label"])}_{pid}',label=s['label'],channel=s['channel'],material=s['material'],
                          toolgen_material=s['toolgen_material'],texture=s['texture'],color=s['color'],emissive=s['emissive'],glass=bool(P.get('glass')),
                          sight=s['sight'],moving=dict(kind=s['moving'],toolgen_node=node.get(pid)) if s['moving'] else None,
                          bounds_m=_bb(m['vertices']),primitive=primitive(P,F),mesh=m))
    # Aufkleber (Reihenfolge wie Weapon-Spec decals[])
    decals=[];k=0
    for i,P in allparts:
        for plane,val,pts,col,em in P['dec']:
            sd=spec['decals'][k];k+=1
            n=F.d(PLANE_NORMAL[plane]);poly=[F.p(q) for q in _decal3(plane,val,pts)]
            if _dot(newell(poly),n)<0:poly=poly[::-1]
            decals.append(dict(part=ids[i],surface=sd['surface'],normal=[float(c) for c in n],channel=sd['channel'],color=sd['color'],
                               emissive=sd['emissive'],polygon_m=poly))
    assert k==len(spec['decals']),(sheet,k,len(spec['decals']))
    # Griff, Abzug, Stützhand
    hp=spec['anchors']['Socket_Hand']['part']
    trig=None
    tr=[(i,P) for i,P in gun if P.get('label')=='Abzug']
    if tr and hp:
        hx=an['Socket_Hand'][0][0]
        i,P=min(tr,key=lambda t:abs(ES._center(ES._bb(ES._verts([t[1]])))[0]-hx))
        trig=(ids[i],F.p(ES._center(ES._bb(ES._verts([P])))))
    g=grip(full.parts[ids.index(hp)],hp,F,trig) if hp else None
    sa=spec['anchors']['Socket_SupportHand']
    if sa['part']:
        su=support(full.parts[ids.index(sa['part'])],sa['part'],an['Socket_SupportHand'][0],F,sa['position_m'])
    else:
        su=dict(part=None,radius_m=None,reason=('Becher-Griff: die Stützhand umfasst die Griffhand (keine Stützhand am Modell)'
                                                if spec['weapon'].get('design_type') in ('sidearm','hand_cannon','rocket_sidearm','spread_hand_cannon')
                                                else sa['source']))
    # Visier
    weapon_top=max(p['bounds_m'][1][2] for p in parts if not p['sight'] and p['label']!='Visierschiene')   # Waffe ohne Visier und Schiene
    if d.get('vs'):
        v=d['vs'];kk=v['k'];mx,my,mz=v['mount'];info=v['info']
        at=lambda x,y:F.p((mx+x*kk,my+y*kk,mz))
        vid=v['id'];st=read_spec(vid)[0]
        sight=sight_block(v['geo'],info,at,kk*unit,vid,sha(st),at(0,0),weapon_top)
        sight['parts']=[ids[i] for i,_ in sight_parts];sight['glass_parts']=[ids[i] for i,P in sight_parts if P.get('glass')]
        sight['riser_m']=rd(v['riser_mm']/1000);sight['rail_part']=ids[v['rail_part']]
        sight_src=dict(file=f'{vid}.spec.json',sha256=sha(st))
    else:
        ss=spec['sight']
        sight=dict(present=ss['present'],id=None,kind=ss['kind'],type=ss['type'],frame=ss['frame'],window_kind=ss['window'],sight_spec=None,
                   window=None,tube=None,socket_mount_m=None,socket_sight_rear_m=None,socket_reticle_m=None,socket_eye_m=None,eye_radius_m=None,
                   socket_eye_source=None,line=None,parts=ss['parts'],glass_parts=[],riser_m=None,rail_part=None,
                   note=('Visier des Blatts ohne Visier-Serie (Bogen: Pin-Visier); Anker Socket_Eye/Socket_Reticle nicht abgeleitet' if ss['present']
                         else ss['source']))
        sight_src=None
    anchors={k:dict(position_m=v['position_m'],part=v['part'],source=v['source']) for k,v in spec['anchors'].items()}
    anchors['Socket_Reticle']=dict(position_m=sight['socket_reticle_m'],part=None,
                                   source='Glasmitte auf der Visierlinie (Sight-Spec Socket_Reticle in Waffenlage)' if sight['socket_reticle_m'] else 'kein Visier der Visier-Serie')
    anchors['Socket_Eye']=dict(position_m=sight['socket_eye_m'],part=None,source=sight['socket_eye_source'] or 'kein Visier der Visier-Serie')
    melee=d['name'] in wtypes.MELEE
    return dict(
        format=FORMAT,format_version=FORMAT_VERSION,
        generator=dict(repo='cubeescape-design',tool='claude/generator/export_geo.py',claude_version=CLAUDE_VERSION),
        sheet=dict(id=sheet,kind='weapon',variant=d['V'],variant_name=spec['sheet']['variant_name'],number=d['num'],name_de=d['name'],
                   nick=d['nick'],toolgen_id=spec['weapon']['toolgen_id'],design_type=spec['weapon'].get('design_type')),
        source=dict(weapon_spec=dict(file=f'{sheet}.spec.json',format=ES.FORMAT,format_version=ES.FORMAT_VERSION,sha256=sha(spec_txt)),
                    sight_spec=sight_src,model='claude/generator/sheetmodels.py (dieselben Modelle wie Blatt und Weapon-Spec)'),
        units=dict(length='m',digits=DIGITS,model_unit_m=round(unit,8)),
        axes=AXES,origin='Socket_Hand',
        parts=parts,decals=decals,decal_note=f'Aufkleber des Blatts als Polygone auf ihrer Fläche (Blatt zeichnet sie {DECAL_OFFSET_UNITS:g} Modelleinheiten '
                                             f'= {rd(DECAL_OFFSET_UNITS*unit)*1000:g} mm darüber); für Toolgen Maskenregionen, keine Geometrie',
        grip=g,support=su,sight=sight,anchors=anchors,
        melee=None,string=string_block(parts,d['name']),
        blocks_pending=dict(melee='DS-2' if melee else None,string=None),
        checks=dict(coplanar=coplanar(meshes,{p['id']:(p['channel'],p['material'],p['emissive'],p['glass']) for p in parts}),
                    decals_outside_part=[k for k,dc in enumerate(decals) if not decal_on_part(dc,next(p['bounds_m'] for p in parts if p['id']==dc['part']))],coplanar_rule=f'gleichgerichtete Flächen verschiedener Teile unter {COPLANAR_M*1000:g} mm Abstand, '
                    f'Überdeckung ab {OVERLAP_MIN_M2*1e6:g} mm²'),
        counts=dict(parts=len(parts),vertices=sum(len(m['vertices']) for _,m in meshes),faces=sum(len(m['faces']) for _,m in meshes),
                    triangles=sum(triangles(m) for _,m in meshes),decals=len(decals),dropped_faces=stats['dropped'],normal_fixes=stats['normal_fixes']),
    )

# ---------------------------------------------------------------- Visier-Serie
def build_sight(vid):
    L=V.load(vid);S=L['S'];info=L['info'];geo=L['geo'];st,ss=read_spec(vid)
    F=Frame(EX.UNIT,(0.0,0.0,0.0))
    sp={p['id']:p for p in ss['parts']}
    parts=[];meshes=[];stats=dict(dropped=0,normal_fixes=0)
    for k,g in enumerate(S.order):
        pid=f'g{k:02d}';s=sp[pid];ps=[P for P in S.m.parts if P['group']==g];m,stt=mesh(ps,F)
        for kk in stats:stats[kk]+=stt[kk]
        meshes.append((pid,m))
        parts.append(dict(id=pid,name=f'SM_PG_{ascii_label(s["label"])}_{pid}',label=s['label'],channel=s['channel'],material=s['material'],
                          toolgen_material=s['toolgen_material'],texture=None,color=s['color'],emissive=s['emissive'],glass=s['glass'],sight=True,
                          moving=None,bounds_m=_bb(m['vertices']),primitive=primitive(ps[0],F) if len(ps)==1 else None,mesh=m))
    at=lambda x,y:F.p((x,y,0.0))
    sight=sight_block(geo,info,at,EX.UNIT,vid,sha(st),at(0,0))
    sight['parts']=[p['id'] for p in parts];sight['glass_parts']=[p['id'] for p in parts if p['glass']];sight['riser_m']=0.0;sight['rail_part']=None
    anchors={k:(dict(position_m=v['position_m'],part=None,source=v['source']) if v else dict(position_m=None,part=None,source='keine Röhre'))
             for k,v in ss['anchors'].items()}
    anchors['Socket_Eye']=dict(position_m=sight['socket_eye_m'],part=None,source=sight['socket_eye_source'])
    return dict(
        format=FORMAT,format_version=FORMAT_VERSION,
        generator=dict(repo='cubeescape-design',tool='claude/generator/export_geo.py',claude_version=CLAUDE_VERSION),
        sheet=dict(id=vid,kind='sight',variant=None,variant_name=None,number=info['num'],name_de=info['title'],nick=None,
                   toolgen_id=info['tid'],design_type=None),
        source=dict(weapon_spec=None,sight_spec=dict(file=f'{vid}.spec.json',format=EX.FORMAT,format_version=EX.FORMAT_VERSION,sha256=sha(st)),
                    model='claude/generator/vsmodels.py (dasselbe Modell wie Blatt und Sight-Spec)'),
        units=dict(length='m',digits=DIGITS,model_unit_m=EX.UNIT),
        axes=AXES,origin='Socket_Mount',
        parts=parts,decals=[],decal_note='keine Aufkleber',
        grip=None,support=None,sight=sight,anchors=anchors,melee=None,string=None,blocks_pending=dict(melee=None,string=None),
        checks=dict(coplanar=coplanar(meshes,{p['id']:(p['channel'],p['material'],p['emissive'],p['glass']) for p in parts}),
                    decals_outside_part=[],coplanar_rule=f'gleichgerichtete Flächen verschiedener Teile unter {COPLANAR_M*1000:g} mm Abstand, '
                    f'Überdeckung ab {OVERLAP_MIN_M2*1e6:g} mm²'),
        counts=dict(parts=len(parts),vertices=sum(len(m['vertices']) for _,m in meshes),faces=sum(len(m['faces']) for _,m in meshes),
                    triangles=sum(triangles(m) for _,m in meshes),decals=0,dropped_faces=stats['dropped'],normal_fixes=stats['normal_fixes']),
    )

SHEETS=list(sheetmodels.SHEETS)+list(V.IDS)
def build(sid):return build_sight(sid) if sid.startswith('VS') else build_weapon(sid)
def dumps(geo):return ES.dumps(geo)
def path(sid):return os.path.join(OUT,f'{sid}.geo.json')

def main(argv):
    check='--check' in argv
    ids=[a for a in argv if not a.startswith('--')] or SHEETS
    bad=[]
    for sid in ids:
        txt=dumps(build(sid));fn=path(sid)
        if check:
            old=None
            if os.path.exists(fn):
                with open(fn,encoding='utf-8') as f:old=f.read()
            if old!=txt:bad.append(sid)
        else:
            with open(fn,'w',encoding='utf-8') as f:f.write(txt)
    if check:
        print('Geo-Specs aktuell' if not bad else 'veraltet oder fehlend: '+' '.join(bad)+'  (python3 claude/generator/export_geo.py)')
        return 1 if bad else 0
    print(len(ids),'Geo-Specs geschrieben nach',os.path.relpath(OUT))
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
