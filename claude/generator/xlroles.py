"""Farb- und Materialrollen der Konzeptblätter, ohne numpy (für xl.py und den Spec-Export export_spec.py).
Aus xl.py herausgelöst (claude-0.2); xl.py importiert alles von hier, das Verhalten der Blätter ist unverändert."""
import colorsys,copy
GRIP_LABELS={'Griff','Pistolengriff','Vordergriff','Pumpgriff','Griffstück','Wangenauflage','Schaftkappe'}
METAL_LABELS={'Lauf','Doppellauf','Oberlauf','Unterlauf','Mündung','Mündungsbremse','Laufmantel','Montageringe','Montage','Schiene','Visierschiene','Schalldämpfer','Rohr','Abschussrohr','Zinken','Kühlrippen','Laufklammer','Fokusringe','Fokusring','Bündelring','Beschleunigerring','Energiespule','Rahmen'}
VARIANTS=[
 ('CUBE ESCAPE STANDARD',['#ECE6DA','#A3A7AD','#2B2E33','#F28C28']),
 ('ARKTIS',['#F3F6F9','#AEBBCA','#3A4452','#22D3EE']),
 ('NACHT',['#4A4E57','#2C2F35','#141518','#FF5A36']),
 ('WÜSTE',['#DCC8A0','#917B57','#3B3226','#F2A93B']),
]
MATS=[('LACKIERTES METALL','lack'),('GEBÜRSTETES METALL','brushed'),('GUMMIERTER GRIFF','rubber'),('MATTER KUNSTSTOFF','plastic'),('BELEUCHTETES ELEMENT','light')]

def _rgb(c):c=c.lstrip('#');return tuple(int(c[i:i+2],16)/255 for i in (0,2,4))
def _hex(r):return '#%02X%02X%02X'%tuple(max(0,min(255,round(x*255))) for x in r)
def _lum(c):r,g,b=_rgb(c);return 0.2126*r+0.7152*g+0.0722*b
def _sat(c):r,g,b=_rgb(c);h,l,s=colorsys.rgb_to_hls(r,g,b);return s if 0.08<l<0.92 else 0
def _mix(a,b,t):A,B=_rgb(a),_rgb(b);return _hex(tuple(A[i]*(1-t)+B[i]*t for i in range(3)))

def all_colors(m):
    out={}
    for P in m.parts:
        out.setdefault(P['col'],[0,P['emit']]);out[P['col']][0]+=len(P['F'])
        for d in P['dec']:
            out.setdefault(d[3],[0,d[4]]);out[d[3]][0]+=1
            if d[4]:out[d[3]][1]=True
    return out

BODY_LABELS={'Gehäuse','Schaft','Rahmen','Handschutz','Laufverkleidung','Laufmantel','Laufhülle','Schlitten','Raketenkasten','Rohr','Abschussrohr','Abschussrohre','Mittelstück','Wurfarm','Tragegriff','Laufkasten','Ladekammer','Kondensator','Kondensatorzelle','Trommel','Schaftkappe','Trichterheck'}
DARK_LABELS={'Griff','Pistolengriff','Vordergriff','Pumpgriff','Griffstück','Magazin','Energiemagazin','Trommelmagazin','Röhrenmagazin','Abzug','Abzugbügel','Wangenauflage'}
def color_roles(m):
    """Rolle je Farbe (light/lightx/mid/dark/accd/acc) wie für die Farbvarianten des Blatts; Grundlage für recolor()
    und als Rückfall für channel_of(). Farben, die in m nicht vorkommen, werden nach Helligkeit eingeordnet."""
    cols=all_colors(m)
    votes={}
    for P in m.parts:
        lb=P.get('label') or ''
        r='light' if lb in BODY_LABELS else 'dark' if lb in DARK_LABELS else 'mid' if lb in METAL_LABELS else None
        if r and not P['emit']:votes.setdefault(P['col'],{}).setdefault(r,0);votes[P['col']][r]+=len(P['F'])
    tot=sum(n for n,e in cols.values()) or 1
    bodyc=max(cols,key=lambda c:(votes.get(c,{}).get('light',0),cols[c][0] if not cols[c][1] else -1))
    Lb=_lum(bodyc)
    def role(c,emit):
        if emit:return 'acc'
        if c in votes:return 'light' if 'light' in votes[c] else max(votes[c],key=votes[c].get)
        if c==bodyc:return 'light'
        if _sat(c)>=0.5 and cols.get(c,[0])[0]/tot<0.12 and abs(_lum(c)-Lb)>0.05:return 'accd'
        L=_lum(c)
        if abs(L-Lb)<0.07:return 'light'
        if L>Lb:return 'lightx'
        return 'mid' if L>0.24 else 'dark'
    return role

def recolor(m,pal,role=None):
    """Gleiche Geometrie, neue Materialkombination – nach Bauteil-Rollen:
    Gehäuse/Schaft -> Primärfarbe (hell), Griffe/Magazine -> dunkel, Metallteile -> mittel, Leucht-/Signalfarben -> Akzent.
    role: Rollen einer anderen Bezugs-Waffe (Spec-Export: Visierteile mit den Rollen der Waffe ohne Visier)."""
    light,mid,dark,acc=pal
    role=role or color_roles(m)
    def mp(c,emit):
        r=role(c,emit)
        if r=='acc':return _mix(acc,'#FFFFFF',0.18) if _lum(c)>0.75 else acc
        if r=='accd':return acc
        if r=='light':return light
        if r=='lightx':return _mix(light,'#FFFFFF',0.35)
        if r=='mid':return mid
        return dark
    m2=copy.deepcopy(m)
    for P in m2.parts:
        if P.get('glass'):continue   # Glas der Visier-Serie behält seine Tönung (claude-0.7)
        P['col']=mp(P['col'],P['emit'])
        P['dec']=[(a,b,c,mp(d,e),e) for a,b,c,d,e in P['dec']]
    return m2

VS_MATERIAL={'painted':'lack','brushed':'brushed','rubber':'rubber','lit':'light','glass':'glass'}
def material_of(P):
    if P.get('material'):return VS_MATERIAL[P['material']]   # Teile der Visier-Serie tragen ihr Material (vsmodels, claude-0.7)
    if P['emit']:return 'light'
    lb=P.get('label') or ''
    if lb in GRIP_LABELS:return 'rubber'
    if lb in METAL_LABELS:return 'brushed'
    L=_lum(P['col'])
    if _sat(P['col'])>0.5:return 'lack'
    if L>0.55:return 'lack'
    if L>0.22:return 'brushed'
    return 'plastic'


# ---------- Cube-Escape-Farbkanäle (Spec-Export, claude-0.2) – das Blatt liest das nicht
MATERIAL_IDS={'lack':'painted','brushed':'brushed','rubber':'rubber','plastic':'matte','light':'lit','glass':'glass'}
ROLE_CHANNEL={'light':'MT_Primary','lightx':'MT_Secondary','accd':'MT_Accent','mid':'MT_Secondary','dark':'MT_Detail'}
def preferred_channel(P,role):
    """Bevorzugter Kanal eines Teils aus Rolle (wie die Farbvarianten des Blatts) und Material."""
    if P['emit']:return 'MT_Energy'
    r=role(P['col'],False);k=material_of(P)
    if k=='brushed' and r in ('mid','dark'):return 'MT_Metal'
    if k in ('rubber','plastic') and r in ('mid','dark'):return 'MT_Detail'
    return ROLE_CHANNEL[r]
FALLBACK={'MT_Primary':('MT_Secondary','MT_Accent','MT_Detail','MT_Metal'),
          'MT_Secondary':('MT_Accent','MT_Primary','MT_Detail','MT_Metal'),
          'MT_Accent':('MT_Secondary','MT_Detail','MT_Primary','MT_Metal'),
          'MT_Metal':('MT_Secondary','MT_Detail','MT_Accent'),
          'MT_Detail':('MT_Secondary','MT_Accent','MT_Metal')}
FALLBACK['MT_Energy']=('MT_Emission',);FALLBACK['MT_Emission']=('MT_Energy',)
MIN_SHARE=0.04
def assign_channels(m,role,area,decal_area,swatches=()):
    """Kanäle für alle Teile und Aufkleber von m (Visier eingeschlossen).
    1. Ausdrücklich gesetzte Kanäle (eng.channel / 'ch') gelten immer.
    2. Bevorzugter Kanal: leuchtende Teile MT_Energy, leuchtende Aufkleber MT_Emission (auf MT_Energy-Teilen MT_Energy),
       sonst preferred_channel(); Aufkleber nehmen den Kanal, den ihre Farbe an den Teilen überwiegend hat.
    3. (Farbe, bevorzugter Kanal) bildet eine Gruppe. Getrennt für nicht leuchtende und leuchtende Gruppen behält – zuerst
       die Farben der Blatt-Palette (swatches), dann die übrigen, jeweils nach Fläche absteigend – jede Gruppe ab MIN_SHARE der Fläche ihres Pools (Palettenfarben immer) den bevorzugten Kanal, wenn er frei ist oder
       schon dieselbe Farbe trägt; sonst nimmt sie einen Kanal aus FALLBACK, der dieselbe Farbe trägt oder frei ist
       (so bleiben zweifarbige Gehäuse zweifarbig). Kleinere Gruppen und Gruppen ohne Platz bleiben beim bevorzugten
       Kanal und erscheinen in der Palette als Nebenfarbe.
    Rückgabe: (Liste (Kanal, Quelle) je Teil, Liste von Listen (Kanal, Quelle) je Aufkleber); Quelle explicit/role/distributed."""
    pch=[None]*len(m.parts);dch=[[None]*len(P['dec']) for P in m.parts]
    sw={c.upper() for c in swatches}
    groups={}
    def add(key,a,ref):g=groups.setdefault(key,[0,[],key[2]]);g[0]+=a;g[1].append(ref)
    owner={}
    for i,P in enumerate(m.parts):
        if P.get('channel'):
            pch[i]=(P['channel'],'explicit')
            if not P.get('glass'):owner.setdefault(P['channel'],P['col'])   # Glas (Tönung) belegt keine Kanalfarbe
    by_color={}
    vs_color={}
    for i,P in enumerate(m.parts):
        if pch[i]:
            if P.get('vs_group') and not P['emit'] and not P.get('glass'):
                vs_color.setdefault(P['col'],{}).setdefault(pch[i][0],0);vs_color[P['col']][pch[i][0]]+=area(P)
            continue
        pc=preferred_channel(P,role);add((P['col'],pc,bool(P['emit'])),area(P),('p',i))
        if not P['emit']:by_color.setdefault(P['col'],{}).setdefault(pc,0);by_color[P['col']][pc]+=area(P)
    # Visier-Serie (claude-0.7): Aufkleber in einer Farbe, die nur das Visier trägt, nehmen dessen Kanal (wie bis 0.6 beim alten Visier)
    for c,v in vs_color.items():by_color.setdefault(c,v)
    for i,P in enumerate(m.parts):
        host=pch[i][0] if pch[i] else preferred_channel(P,role)
        for k,d in enumerate(P['dec']):
            col,emit=d[3],d[4]
            if P.get('dec_channel'):dch[i][k]=(P['dec_channel'],'explicit');continue   # eng.copy_channels 'dch' (claude-0.15.2)
            if emit:pc='MT_Energy' if host=='MT_Energy' else 'MT_Emission'
            else:pc=max(by_color[col],key=by_color[col].get) if col in by_color else ROLE_CHANNEL[role(col,False)]
            add((col,pc,bool(emit)),decal_area(d),('d',i,k))
    for emit in (False,True):
        pool=sorted(((k,g) for k,g in groups.items() if g[2]==emit),key=lambda t:(t[0][0].upper() not in sw,-t[1][0],t[0][0],t[0][1]))
        total=sum(g[0] for _,g in pool) or 1
        for (col,pc,_),(a,refs,_e) in pool:
            ch,src=pc,'role'
            if a/total>=MIN_SHARE or col.upper() in sw:
                if owner.get(pc,col)!=col:
                    alt=[c for c in FALLBACK[pc] if owner.get(c)==col] or [c for c in FALLBACK[pc] if c not in owner]
                    if alt:ch,src=alt[0],'distributed'
                owner.setdefault(ch,col)
            for r in refs:
                if r[0]=='p':pch[r[1]]=(ch,src)
                else:dch[r[1]][r[2]]=(ch,src)
    return pch,dch


# ---------- Flächen und Kanal-Paletten je Farbvariante (Spec-Export und Skins, claude-0.3; ohne numpy)
import math as _m
def area3(v):
    nx=ny=nz=0.0
    for i in range(len(v)):
        (x0,y0,z0),(x1,y1,z1)=v[i],v[(i+1)%len(v)]
        nx+=(y0-y1)*(z0+z1);ny+=(z0-z1)*(x0+x1);nz+=(x0-x1)*(y0+y1)
    return 0.5*_m.sqrt(nx*nx+ny*ny+nz*nz)
def area2(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))/2
def part_area(P):return sum(area3(f['v']) for f in P['F'])
VARIANT_IDS=['base','standard','arktis','nacht']
def _hexu(c):return c.upper() if c.startswith('#') else c
def channel_palettes(full,gun_m,palette,pill,channels):
    """Kanalfarben der vier Farbvarianten des Blatts (Basis + 3) wie im Spec (`palette`): je Kanal die Farbe mit der
    größten Fläche (Teile + Aufkleber); Rollen aus der Waffe ohne Visier. Rückgabe: (Liste je Variante, Kanal je Teil)."""
    role=color_roles(gun_m)
    pch,dsrc=assign_channels(full,role,part_area,lambda dd:area2(dd[2]),palette)
    dch=[[c for c,_ in row] for row in dsrc]
    names=['BASIS · '+pill]+[n for n,_ in VARIANTS[:3]]
    pals=[palette]+[p for _,p in VARIANTS[:3]]
    out=[]
    for vid,vn,pal in zip(VARIANT_IDS,names,pals):
        mm=full if vid=='base' else recolor(full,pal,role=role)
        acc={ch:{} for ch in channels}
        gacc={}
        for i,P in enumerate(mm.parts):
            if P.get('glass'):   # Glas: Tönung des Visiers, Kanalfarbe nur, wenn sonst nichts auf dem Kanal liegt
                gacc.setdefault(pch[i][0],{});gacc[pch[i][0]][P['col']]=gacc[pch[i][0]].get(P['col'],0)+part_area(P);continue
            a=part_area(P);acc[pch[i][0]][P['col']]=acc[pch[i][0]].get(P['col'],0)+a
            for k,dd in enumerate(P['dec']):
                da=area2(dd[2]);acc[dch[i][k]][dd[3]]=acc[dch[i][k]].get(dd[3],0)+da
        for ch,g in gacc.items():
            if not acc[ch]:acc[ch]=g
        chans={};dev={}
        for ch in channels:
            if not acc[ch]:chans[ch]=None;continue
            tot=sum(acc[ch].values());order=sorted(acc[ch].items(),key=lambda t:(-t[1],t[0]))
            chans[ch]=_hexu(order[0][0])
            if len(order)>1:dev[ch]=[dict(color=_hexu(c),share=round(a/tot,3)) for c,a in order[1:]]
        out.append(dict(id=vid,name=vn,swatches=[_hexu(c) for c in pal],channels=chans,other_colors=dev,
                        on_sheet=True,sight_colors='extrapoliert' if vid!='base' else 'wie Modell'))
    return out,pch
