"""Spec-Export der Konzeptblätter: claude/output/sheets/KXnn.spec.json (Format: claude/docs/weapon-spec.md).

   python3 claude/generator/export_spec.py            # alle 50 Specs schreiben
   python3 claude/generator/export_spec.py KC01 KD05  # nur diese
   python3 claude/generator/export_spec.py --check    # nur vergleichen; Exit 1, wenn eine Datei fehlt oder veraltet ist

Ohne Bildstufe und ohne numpy: Die Werte kommen aus denselben Python-Modellen wie die Blätter (sheetmodels.py),
damit Toolgen sie nicht aus dem Bild lesen muss.
"""
from cepaths import E3D,OUT
import json,math,os,re,sys
sys.path.insert(0,E3D)
import sheetmodels
from eng import CHANNELS,split_sight
from xlroles import VARIANTS,MATERIAL_IDS,color_roles,recolor,material_of,assign_channels

FORMAT='cubeescape-design/weapon-spec'
FORMAT_VERSION=1
CLAUDE_VERSION='0.2'

# Waffentyp -> Toolgen-Id, Bezugslänge (m), Element.
# Längen: Toolgen-Weltmodelle, Ausdehnung entlang der Mündungsachse (Blender −Y) aus qa_game.json › bounds_lod0 ›
# source_bounds_m (Toolgen 0.13, Messung 17.10.2026); Bogen: größte Ausdehnung (Wurfarm-Spannweite, Blender Z).
# Elemente: Entscheidung des Nutzers vom 17.10.2026 (Toolgen docs/ENTSCHEIDUNGEN.md, data/tools.json); Bogen ohne Element.
WEAPONS={
 'Pistole':('pistol',0.243,'solar'),
 'Sturmgewehr':('assault_rifle',0.934,'arc'),
 'Impulsgewehr':('pulse_rifle',0.862,'void'),
 'Schrotflinte':('shotgun',0.904,'solar'),
 'Scharfschützengewehr':('sniper_rifle',1.134,'energy'),
 'Maschinenpistole':('smg',0.616,'energy'),
 'Fusionsgewehr':('fusion_rifle',0.960,'void'),
 'Spurgewehr':('scout_rifle',1.044,'arc'),
 'Raketenwerfer':('rocket_launcher',0.725,'solar'),
 'Bogen':('bow',1.018,None),
}
ELEMENT_SOURCE='Nutzer 17.10.2026 (Toolgen docs/ENTSCHEIDUNGEN.md, data/tools.json)'

# Visier je Blatt: (Art, Fenster, Quelle). Art im Toolgen-Wortschatz hold.sight_kind (iron/reflex/holo/scope/energy) plus
# pin (Bogen-Pinvisier); Fenster: none (Kimme/Korn), open (offener Ring/Lochblende/Rahmen ohne Glas), glass (flache
# Scheibe), lens (runde Optik). Quelle: Bezeichnung im Modell, Text des Blatts oder Kommentar/Geometrie im Modell.
SIGHTS={
 'KC01':('iron','none','Bezeichnung Kimme/Korn'),'KC02':('iron','open','Bezeichnung Diopter/Korn'),
 'KC03':('reflex','glass','Bezeichnung Reflexvisier'),'KC04':('holo','glass','Bezeichnung Kastenvisier'),
 'KC05':('scope','lens','Bezeichnung Zielfernrohr'),'KC06':('iron','none','Bezeichnung Kimme/Korn'),
 'KC07':('reflex','glass','Bezeichnung Reflexvisier'),'KC08':('scope','lens','Kommentar c08.py: Zielfernrohr-Block mit Linse'),
 'KC09':('iron','open','Bezeichnung Ringvisier/Korn'),'KC10':('iron','none','Bezeichnung Kimme/Korn'),
 'KD01':(None,None,'kein separates Visier im Modell'),'KD02':('holo','glass','Bezeichnung Kastenvisier'),
 'KD03':('holo','glass','Geometrie dmods.d03: großer Kasten mit Leuchtfenster vorn'),'KD04':(None,None,'kein separates Visier im Modell'),
 'KD05':('scope','lens','Bezeichnung Zielfernrohr'),'KD06':('iron','none','Bezeichnung Kimme · Korn'),
 'KD07':('reflex','glass','Geometrie dmodels.d07: Visierblock mit Leuchtpunkt vorn'),'KD08':('scope','lens','Bezeichnung Zielfernrohr'),
 'KD09':('scope','lens','Geometrie dmodels.d09: Rohrvisier auf Stützen'),'KD10':(None,None,'kein separates Visier im Modell'),
 'KF01':('iron','none','Bezeichnung Kimme/Korn'),'KF02':('iron','none','Bezeichnung Kimme/Korn'),
 'KF03':('reflex','glass','Text des Blatts: Reflexvisier'),'KF04':('iron','none','Bezeichnung Korn'),
 'KF05':('scope','lens','Bezeichnung Zielfernrohr'),'KF06':('reflex','glass','Text des Blatts: Reflexvisier'),
 'KF07':('reflex','glass','Geometrie f07.py: Visierblock mit Leuchtpunkt vorn'),'KF08':('scope','lens','Bezeichnung Zielfernrohr'),
 'KF09':('reflex','glass','Geometrie f09.py: Visierblock mit Leuchtpunkt vorn'),'KF10':('pin','open','Geometrie f10.py: leuchtender Pin-Ring am Bogen'),
 'KG01':('iron','none','Bezeichnung Kimme/Korn'),'KG02':('reflex','glass','Bezeichnung Reflexvisier'),
 'KG03':('reflex','glass','Geometrie g03.py: Visierblock mit Leuchtfenster vorn'),'KG04':('iron','open','Text des Blatts: Lochvisier'),
 'KG05':('scope','lens','Bezeichnung Zielfernrohr'),'KG06':('reflex','glass','Text des Blatts: Reflexvisier'),
 'KG07':('reflex','glass','Geometrie g07.py: Visierkopf mit Leuchtfenster vorn'),'KG08':('scope','lens','Bezeichnung Zielfernrohr'),
 'KG09':('reflex','glass','Kommentar g09.py: Visierkopf mit Linse'),'KG10':('pin','glass','Geometrie g10.py: Visier auf Arm mit Leuchtfenster'),
 'KH01':('reflex','glass','Bezeichnung Reflexvisier'),'KH02':('holo','glass','Bezeichnung Holovisier'),
 'KH03':('iron','open','Bezeichnung Ringvisier'),'KH04':('iron','open','Bezeichnung Lochvisier'),
 'KH05':('scope','lens','Bezeichnung Zielfernrohr'),'KH06':('reflex','glass','Kommentar h06.py: Reflexvisier'),
 'KH07':('holo','glass','Kommentar h07.py: Holo-Rahmen'),'KH08':('scope','lens','Bezeichnung Zielfernrohr'),
 'KH09':('iron','open','Text des Blatts: Klappvisier'),'KH10':('pin','glass','Text des Blatts: Pin-Visier'),
}

HAND_LABELS=('Griff','Pistolengriff','Griffstück')
SUPPORT_LABELS=('Vordergriff','Pumpgriff')
GUARD_LABELS=('Handschutz','Laufverkleidung','Laufmantel','Laufhülle')
MUZZLE_LABELS={'Mündung','Mündungsbremse','Kompensator','Schalldämpfer','Feuerdämpfer','Emitter','Fächeremitter','Mündungsring',
 'Lauf','Doppellauf','Oberlauf','Unterlauf','Rohr','Abschussrohr','Abschussrohre','Raketenrohre','Laufmantel','Laufkasten',
 'Zinken','Pfeil','Bolzen','Fokusring','Fokusringe','Bündelring','Raketenkasten','Oberkiefer','Unterkiefer','Feuerkern'}
SURFACES={'z+':'left','z-':'right','x+':'front','x-':'back','y-':'top','y+':'bottom'}
VARIANT_IDS=['base','standard','arktis','nacht']
# Achsen: Modell x = Mündung (vorn), y = unten, z = links  ->  Toolgen/Blender vorn −Y, oben +Z, links +X
M2B=[[0,0,1],[-1,0,0],[0,-1,0]]
AXIS_NAMES=['Y','Z','X']   # Längsachse eines Teils: Modellachse x/y/z -> Toolgen-Achse

def r4(v):return round(v+0.0,4)
def _bb(vs):return [min(q[i] for q in vs) for i in range(3)],[max(q[i] for q in vs) for i in range(3)]
def _verts(parts):return [q for P in parts for f in P['F'] for q in f['v']]
def _center(bb):return [(bb[0][i]+bb[1][i])/2 for i in range(3)]
def _area3(v):
    nx=ny=nz=0.0
    for i in range(len(v)):
        (x0,y0,z0),(x1,y1,z1)=v[i],v[(i+1)%len(v)]
        nx+=(y0-y1)*(z0+z1);ny+=(z0-z1)*(x0+x1);nz+=(x0-x1)*(y0+y1)
    return 0.5*math.sqrt(nx*nx+ny*ny+nz*nz)
def _area2(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))/2
def _decal3(plane,val,pts):
    if plane[0]=='z':return [(x,y,val) for x,y in pts]
    if plane[0]=='x':return [(val,y,z) for y,z in pts]
    return [(x,val,z) for x,z in pts]

class Frame:
    """Modellkoordinaten -> Toolgen-Blender-Meter relativ zu Socket_Hand."""
    def __init__(s,unit,origin):s.u=unit;s.o=origin
    def p(s,q):
        d=[q[i]-s.o[i] for i in range(3)]
        return [r4(s.u*sum(M2B[r][c]*d[c] for c in range(3))) for r in range(3)]
    def bb(s,bb):
        cs=[s.p((x,y,z)) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1]) for z in (bb[0][2],bb[1][2])]
        return [[min(c[i] for c in cs) for i in range(3)],[max(c[i] for c in cs) for i in range(3)]]

def _pick_hand(parts):
    cand=[(i,P) for i,P in parts if P.get('label') in HAND_LABELS]
    trig=[P for _,P in parts if P.get('label')=='Abzug']
    if not cand:return None,None
    if trig:
        tx=_center(_bb(_verts(trig)))[0]
        behind=[c for c in cand if _center(_bb(_verts([c[1]])))[0]<=tx+1e-6]
        pool=behind or cand
        return min(pool,key=lambda c:abs(_center(_bb(_verts([c[1]])))[0]-tx))
    return max(cand,key=lambda c:_center(_bb(_verts([c[1]])))[0])

def _anchors(d,gun,sight_parts,allparts,ids):
    hand=_pick_hand(gun)
    an={};notes={}
    if hand[0] is not None:
        hc=_center(_bb(_verts([hand[1]])));an['Socket_Hand']=(hc,f'Mitte von {ids[hand[0]]} ({hand[1]["label"]})')
    else:
        hc=_center(_bb(_verts([P for _,P in gun])));an['Socket_Hand']=(hc,'kein Griff bezeichnet: Mitte der Waffe')
    # Stützhand
    sup=None
    c=[(i,P) for i,P in gun if P.get('label') in SUPPORT_LABELS]
    if c:
        i,P=min(c,key=lambda t:abs(_center(_bb(_verts([t[1]])))[0]-hc[0]));sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} ({P["label"]})')
    else:
        g2=[(i,P) for i,P in gun if P.get('label') in HAND_LABELS and i!=hand[0] and _center(_bb(_verts([P])))[0]>hc[0]+10]
        if g2:
            i,P=min(g2,key=lambda t:_center(_bb(_verts([t[1]])))[0]);sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} (zweiter Griff)')
        else:
            gd=[(i,P) for i,P in gun if P.get('label') in GUARD_LABELS and _center(_bb(_verts([P])))[0]>hc[0]]
            if gd:
                i,P=max(gd,key=lambda t:_area(t[1]));sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} ({P["label"]})')
    if sup:an['Socket_SupportHand']=sup
    else:notes['Socket_SupportHand']='nicht ableitbar (kein Vordergriff, zweiter Griff oder Handschutz vor dem Griff)'
    # Mündung
    mz=[(i,P) for i,P in gun if P.get('label') in MUZZLE_LABELS]
    src='vorderstes bezeichnetes Mündungs-/Laufteil'
    if not mz:mz=gun;src='vorderstes Teil (kein Lauf bezeichnet)'
    i,P=max(mz,key=lambda t:_bb(_verts([t[1]]))[1][0]);bb=_bb(_verts([P]));cc=_center(bb)
    an['Socket_Muzzle']=([bb[1][0],cc[1],cc[2]],f'{src}: Vorderkante von {ids[i]} ({P.get("label") or "ohne Bezeichnung"}), Querschnittsmitte')
    # Schwerpunkt: Näherung, Teile mit Volumen ihres Hüllquaders gewichtet (Visier montiert)
    W=0;acc=[0,0,0]
    for _,P in allparts:
        bb=_bb(_verts([P]));w=max(1e-9,(bb[1][0]-bb[0][0])*(bb[1][1]-bb[0][1])*(bb[1][2]-bb[0][2]));cc=_center(bb)
        W+=w;acc=[acc[k]+w*cc[k] for k in range(3)]
    an['Socket_CenterOfMass']=([a/W for a in acc],'Näherung: Hüllquader-Volumen je Teil gewichtet, Visier montiert')
    # Visier
    if sight_parts:
        bb=_bb(_verts([P for _,P in sight_parts]));cc=_center(bb)
        an['Socket_Sight']=([cc[0],bb[1][1],cc[2]],'Unterkante Mitte der Visierbaugruppe (montierte Lage)')
    else:
        rail=[(i,P) for i,P in gun if P.get('label')=='Visierschiene']
        if rail:
            i,P=rail[0];bb=_bb(_verts([P]));cc=_center(bb)
            an['Socket_Sight']=([cc[0],bb[0][1],cc[2]],f'Oberkante Mitte von {ids[i]} (Visierschiene, kein Visier im Modell)')
        else:notes['Socket_Sight']='kein Visier und keine Visierschiene im Modell'
    return an,notes

def _area(P):return sum(_area3(f['v']) for f in P['F'])

def _hex(c):return c.upper() if c.startswith('#') else c

def build(sheet):
    d=sheetmodels.load(sheet)
    full=d['m'];gun_m,sight_m=split_sight(full)
    tid,ref_len,element=WEAPONS[d['name']]
    allparts=list(enumerate(full.parts))
    ids=[f'p{i:02d}' for i in range(len(full.parts))]
    gun=[(i,P) for i,P in allparts if not P.get('sight')];sight_parts=[(i,P) for i,P in allparts if P.get('sight')]
    # Maßstab
    bbf=_bb(_verts(full.parts));ext=[bbf[1][k]-bbf[0][k] for k in range(3)]
    if tid=='bow':model_len=max(ext);rule='größte Ausdehnung des Modells (Visier montiert) = Toolgen-Bogen, größte Ausdehnung'
    else:model_len=ext[0];rule='Länge entlang der Mündungsachse (Modell x, Visier montiert) = Toolgen-Länge des Waffentyps'
    unit=ref_len/model_len
    an,notes=_anchors(d,gun,sight_parts,allparts,ids)
    F=Frame(unit,an['Socket_Hand'][0])
    # Kanäle (Rollen wie die Farbvarianten des Blatts: aus der Waffe ohne Visier)
    role=color_roles(gun_m)
    pch,dsrc=assign_channels(full,role,_area,lambda dd:_area2(dd[2]),d['palette'])
    dch=[[c for c,_ in row] for row in dsrc]
    # Paletten je Variante: Flächenanteil je Kanal (Teile + Aufkleber)
    names=['BASIS · '+d['pill']]+[n for n,_ in VARIANTS[:3]]
    pals=[d['palette']]+[p for _,p in VARIANTS[:3]]
    palette=[]
    for vid,vn,pal in zip(VARIANT_IDS,names,pals):
        mm=full if vid=='base' else recolor(full,pal,role=role)
        acc={ch:{} for ch in CHANNELS}
        for i,P in enumerate(mm.parts):
            a=_area(P);acc[pch[i][0]][P['col']]=acc[pch[i][0]].get(P['col'],0)+a
            for k,dd in enumerate(P['dec']):
                da=_area2(dd[2]);acc[dch[i][k]][dd[3]]=acc[dch[i][k]].get(dd[3],0)+da
        chans={};dev={}
        for ch in CHANNELS:
            if not acc[ch]:chans[ch]=None;continue
            tot=sum(acc[ch].values());order=sorted(acc[ch].items(),key=lambda t:(-t[1],t[0]))
            chans[ch]=_hex(order[0][0])
            if len(order)>1:dev[ch]=[dict(color=_hex(c),share=round(a/tot,3)) for c,a in order[1:]]
        palette.append(dict(id=vid,name=vn,swatches=[_hex(c) for c in pal],channels=chans,other_colors=dev,
                            on_sheet=True,sight_colors='extrapoliert' if vid!='base' else 'wie Modell'))
    # Teile
    parts=[]
    for i,P in allparts:
        bb=_bb(_verts([P]));ext=[bb[1][k]-bb[0][k] for k in range(3)]
        parts.append(dict(id=ids[i],label=P.get('label'),channel=pch[i][0],channel_source=pch[i][1],
                          material=MATERIAL_IDS[material_of(P)],emissive=bool(P['emit']),sight=bool(P.get('sight')),
                          color=_hex(P['col']),area_m2=round(_area(P)*unit*unit,6),long_axis=AXIS_NAMES[ext.index(max(ext))],
                          bounds_m=F.bb(bb)))
    decals=[]
    for i,P in allparts:
        for k,(plane,val,pts,col,em) in enumerate(P['dec']):
            v3=_decal3(plane,val,pts)
            decals.append(dict(part=ids[i],channel=dch[i][k],surface=SURFACES[plane],emissive=bool(em),color=_hex(col),
                               area_m2=round(_area2(pts)*unit*unit,7),bounds_m=F.bb(_bb(v3))))
    # Visier
    kind,window,ssrc=SIGHTS[sheet]
    if sight_parts:
        sb=_bb(_verts([P for _,P in sight_parts]));gb=_bb(_verts([P for _,P in gun]))
        gz=_center(gb)[2];side='left' if sb[0][2]>gz+5 else 'right' if sb[1][2]<gz-5 else 'top'
        sight=dict(present=True,kind=kind,window=window,source=ssrc,modular=True,mount_side=side,
                   labels=sorted({P.get('label') for _,P in sight_parts if P.get('label')}),parts=[ids[i] for i,_ in sight_parts],
                   bounds_m=F.bb(sb),anchor='Socket_Sight')
    else:
        sight=dict(present=False,kind=None,window=None,source=ssrc,modular=True,mount_side=None,labels=[],parts=[],bounds_m=None,
                   anchor='Socket_Sight' if 'Socket_Sight' in an else None)
    def dims(parts_):
        bb=F.bb(_bb(_verts(parts_)));e=[r4(bb[1][k]-bb[0][k]) for k in range(3)]
        return dict(length=e[1],height=e[2],width=e[0],bounds_m=bb)
    anchors={k:dict(position_m=F.p(p),model=[round(x,2) for x in p],source=s) for k,(p,s) in an.items()}
    for k in ('Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight'):
        if k not in anchors:anchors[k]=dict(position_m=None,model=None,source=notes.get(k,'nicht ableitbar'))
    anchors={k:anchors[k] for k in ('Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight')}
    used=[ch for ch in CHANNELS if palette[0]['channels'][ch]]
    return dict(
        format=FORMAT,format_version=FORMAT_VERSION,
        generator=dict(repo='cubeescape-design',tool='claude/generator/export_spec.py',claude_version=CLAUDE_VERSION),
        sheet=dict(id=sheet,file=f'{sheet}.dc.html',variant=d['V'],number=d['num'],nick=d['nick'],fid=d['fid']),
        weapon=dict(name_de=d['name'],toolgen_id=tid),
        element=element,element_source=ELEMENT_SOURCE if element else 'nicht festgelegt (Toolgen-Bogen ohne Element)',
        units=dict(model_unit_m=round(unit,8),model_length_units=round(model_len,2),reference_length_m=ref_len,rule=rule,
                   reference='Toolgen 0.13 Weltmodell '+tid+', qa_game.json bounds_lod0.source_bounds_m (Messung 17.10.2026)'),
        axes=dict(model=dict(x='vorn (Mündung)',y='unten',z='links'),target=dict(system='Toolgen/Blender',forward='-Y',up='+Z',left='+X',unit='m'),
                  matrix_model_to_target=M2B,origin='Socket_Hand',
                  formula='p_m = model_unit_m * M · (p_model − Socket_Hand.model)'),
        dimensions_m=dict(weapon=dims([P for _,P in gun]),with_sight=dims(full.parts)),
        anchors=anchors,
        palette=palette,
        channels_used=used,
        parts=parts,
        sight=sight,
        decals=decals,
        textures=textures(unit),
        summary=dict(parts=len(parts),parts_explicit_channel=sum(1 for c in pch if c[1]=='explicit'),decals=len(decals),
                     channels_with_other_colors={p['id']:sorted(p['other_colors']) for p in palette if p['other_colors']}),
    )

def textures(unit):
    """Muster der Material-Ansicht des Blatts (xl.make_texture) als Zielbild für Toolgens Bake, im Wortschatz von
    Toolgen data/surface_recipes.json › patterns (knurl/brushed/grain; Größen in mm, Werkzeugrahmen Socket_Hand).
    brightness = Helligkeitsfaktor auf die Kanalfarbe im Blatt; Längen sind Weltlängen am Modell (keine UV)."""
    mm=lambda v:round(v*unit*1000,3)
    return dict(
        source='xl.make_texture (Materialansicht des Blatts), Modelleinheiten mal model_unit_m',
        vocabulary='Toolgen data/surface_recipes.json › patterns',
        painted=dict(toolgen_pattern=None,look='weicher Glanzverlauf, kein Relief',brightness=[0.87,1.13],
                     waves=[dict(axis='Z',wavelength_mm=mm(2*math.pi*26),amplitude=0.09),
                            dict(axis='X+Y',wavelength_mm=mm(2*math.pi*55),amplitude=0.04)]),
        brushed=dict(toolgen_pattern='brushed',direction='long_axis',size_mm=mm(2*math.pi/(7.3*0.9)),brightness=[0.87,1.13],
                     cross_wavelengths_mm=[mm(2*math.pi/(3.1*0.9)),mm(2*math.pi/(7.3*0.9)),mm(2*math.pi/(13.1*0.9))],weights=[0.5,0.3,0.2]),
        rubber=dict(toolgen_pattern='knurl',direction='Flächenebene, ±45°',size_mm=mm(4.0),brightness=[0.66,1.0]),
        matte=dict(toolgen_pattern='grain',size_mm=mm(1/1.3),brightness=[0.955,1.045]),
        lit=dict(toolgen_pattern=None,look='leuchtend, Kanalfarbe als Emission, kein Muster'),
    )

_NUMS=re.compile(r'\[\s*((?:-?[\d.eE+-]+|null)(?:,\s*(?:-?[\d.eE+-]+|null))*)\s*\]')
def dumps(spec):
    """JSON mit Einzug; Zahlenlisten (Koordinaten, Matrixzeilen) bleiben in einer Zeile."""
    txt=json.dumps(spec,ensure_ascii=False,indent=1)
    return _NUMS.sub(lambda mm:'['+', '.join(x.strip() for x in mm.group(1).split(','))+']',txt)+'\n'
def path(sheet):return os.path.join(OUT,f'{sheet}.spec.json')

def main(argv):
    check='--check' in argv
    sheets=[a for a in argv if not a.startswith('--')] or sheetmodels.SHEETS
    bad=[]
    for s in sheets:
        txt=dumps(build(s));fn=path(s)
        if check:
            old=None
            if os.path.exists(fn):
                with open(fn,encoding='utf-8') as f:old=f.read()
            if old!=txt:bad.append(s)
        else:
            with open(fn,'w',encoding='utf-8') as f:f.write(txt)
    if check:
        print('Specs aktuell' if not bad else 'veraltet oder fehlend: '+' '.join(bad)+'  (python3 claude/generator/export_spec.py)')
        return 1 if bad else 0
    print(len(sheets),'Specs geschrieben nach',os.path.relpath(OUT))
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
