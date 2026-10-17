"""Sight-Spec der Visier-Serie: claude/output/sheets/VSnn.spec.json (Format: claude/docs/sight-spec.md, Schema sight-spec.schema.json).

   python3 claude/generator/export_sight.py            # alle neun Specs schreiben
   python3 claude/generator/export_sight.py VS01 VS05  # nur diese
   python3 claude/generator/export_sight.py --check    # nur vergleichen; Exit 1, wenn eine Datei fehlt oder veraltet ist

Ohne numpy und ohne Bildstufe: dieselben Modelle wie die Blätter (vsmodels.py), damit Ansichten und Daten deckungsgleich sind.
"""
from cepaths import E3D,OUT
import glob,json,math,os,sys
sys.path.insert(0,E3D)
import vsmodels as V
from export_spec import SIGHT_TYPES,TOOLGEN_MATERIAL,FORMAT as WEAPON_FORMAT,CLAUDE_VERSION as _WEAPON_VERSION,dumps,r4,_area3,_newell

FORMAT='cubeescape-design/sight-spec'
FORMAT_VERSION=1
CLAUDE_VERSION='0.6'
M2B=[[0,0,1],[-1,0,0],[0,-1,0]]   # Modell (vorn x, unten y, links z) -> Blender (vorn −Y, oben +Z, links +X), wie export_spec
UNIT=0.001                          # Modelleinheit = 1 mm
# Toolgen-Material je Spec-Material; Klarglas hat in Toolgen (data/surface_recipes.json › materials) noch kein Material
MATERIALS=dict(TOOLGEN_MATERIAL,glass=None,painted_matte='painted_matte')
TARGET_SOURCE=dict(
 images=['Cube Escape Docs/Images/EquipmentConcepts/weapon_sights_1-9.webp (Visier je Waffe)',
         'Cube Escape Docs/Images/EquipmentConcepts/sight_types_1-9.webp (Visiertypen)'],
 table='Cube Escape Docs/EQUIPMENT.md › Visiere je Waffe',
 decisions='claude/docs/ENTSCHEIDUNGEN.md (17.10.2026: Visier-Serie VS01–VS09 ist das Zielbild; Vokabular sight.type/sight.frame; '
           'Spurgewehr ohne Röhre; Lenswork-Daten im Sight-Spec)')
# Achsen des Ankers: Cube Escape `Socket_Sight` „Blick +Z, +Y oben“ (FIRST_PERSON_EQUIPMENT.md › 4.2) als Blender-Drehung (XYZ):
# Rx(90°) dreht lokal +Z auf Welt −Y (Blick nach vorn) und lokal +Y auf Welt +Z (oben)
ANCHOR_AXES=dict(local_forward='+Z',local_up='+Y',forward=[0.0,-1.0,0.0],up=[0.0,0.0,1.0],rotation_euler_deg=[90.0,0.0,0.0],
                 rotation_space='Blender (lokale Achsen des Empties vor dem Export)',
                 note='Verbindlich sind forward/up im Weltrahmen (Blender). Die Drehung gilt nur in Blender: der glTF-Export dreht die Achsen, '
                      'in Unity entspricht „Blick +Z, +Y oben“ (Cube Escape Socket_Sight) dann der Identität. Toolgen: Anker-Drehung ist kein Vertrag, die Position schon')

def srgb_to_linear(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def tint_rgba(tid):
    nm,hx,a=V.TINTS[tid];h=hx.lstrip('#')
    return [round(srgb_to_linear(int(h[i:i+2],16)),4) for i in (0,2,4)]+[a]

def P(q):
    """Modellpunkt (mm, Ursprung Socket_Mount) -> Blender-Meter"""
    return [r4(UNIT*sum(M2B[r][c]*q[c] for c in range(3))) for r in range(3)]
def _verts(parts):return [q for Pt in parts for f in Pt['F'] for q in f['v']]
def _bb(vs):return [min(q[i] for q in vs) for i in range(3)],[max(q[i] for q in vs) for i in range(3)]
def BB(bb):
    cs=[P((x,y,z)) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1]) for z in (bb[0][2],bb[1][2])]
    return [[min(c[i] for c in cs) for i in range(3)],[max(c[i] for c in cs) for i in range(3)]]

def _in_poly(y,z,pts):
    """gerade-ungerade-Regel in der Ebene (y, z)"""
    ins=False;n=len(pts)
    for i in range(n):
        (y0,z0),(y1,z1)=pts[i],pts[(i+1)%n]
        if (z0>z) != (z1>z):
            yc=y0+(z-z0)*(y1-y0)/(z1-z0)
            if y<yc:ins=not ins
    return ins
def line_hits(parts,line_y,lz=0.0):
    """Schnittpunkte der Visierlinie (entlang x bei y=line_y, z=lz) mit den Flächen der Teile: Liste (Gruppe, x in mm, Glas ja/nein).
    Fläche = ebenes Polygon; Normale nach Newell aus den Punkten (nicht aus der gespeicherten Normale)."""
    out=[]
    for Pt in parts:
        for f in Pt['F']:
            v=f['v'];n=_newell(v)
            if abs(n[0])<1e-6:continue          # parallel zur Linie (Mantel, Wand)
            x=v[0][0]-(n[1]*(line_y-v[0][1])+n[2]*(lz-v[0][2]))/n[0]
            if _in_poly(line_y,lz,[(q[1],q[2]) for q in v]):out.append((Pt.get('group'),round(x,3),bool(Pt.get('glass'))))
    return out

APERTURE_STEP=0.5     # mm, Rasterweite der Strahlen
APERTURE_MARGIN=0.3   # mm Abstand zum Rand der Öffnung
def aperture_check(S,geo,step=APERTURE_STEP,margin=APERTURE_MARGIN):
    """Ganze Öffnung frei: Strahlen parallel zur Visierlinie auf einem Raster mit Weite step (mm) in der freien Öffnung
    (vsmodels.aperture_loop, Rand margin); Ergebnis (Zahl der Strahlen, Gruppen undurchsichtiger Teile, die einen Strahl schneiden)."""
    lp=V.aperture_loop(geo,margin);ys=[p[0] for p in lp];zs=[p[1] for p in lp]
    # nur Flächen quer zur Linie, mit Hüllrechteck (y, z) für den schnellen Ausschluss
    F=[]
    for Pt in S.m.parts:
        if Pt.get('glass'):continue
        for f in Pt['F']:
            v=f['v'];n=_newell(v)
            if abs(n[0])<1e-6:continue
            yz=[(q[1],q[2]) for q in v]
            F.append((Pt.get('group'),yz,min(p[0] for p in yz),max(p[0] for p in yz),min(p[1] for p in yz),max(p[1] for p in yz)))
    ny=int((max(ys)-min(ys))/step)+1;nz=int((max(zs)-min(zs))/step)+1;rays=0;bad=set()
    for i in range(ny):
        y=min(ys)+(max(ys)-min(ys))*(i+0.5)/ny
        for j in range(nz):
            z=min(zs)+(max(zs)-min(zs))*(j+0.5)/nz
            if not _in_poly(y,z,lp):continue
            rays+=1
            for g,yz,y0,y1,z0,z1 in F:
                if g not in bad and y0<=y<=y1 and z0<=z<=z1 and _in_poly(y,z,yz):bad.add(g)
    return rays,sorted(bad)

def weapon_sheets(tid):
    """Waffen-Specs (KXnn.spec.json) desselben Waffentyps"""
    out=[]
    for fn in sorted(glob.glob(os.path.join(OUT,'K*.spec.json'))):
        with open(fn,encoding='utf-8') as f:d=json.load(f)
        if d.get('weapon',{}).get('toolgen_id')==tid:out.append(d['sheet']['id'])
    return out

def variants(info,S):
    """vier Varianten des Blatts: Kanalfarben und Glas; Basis = Farben des Modells"""
    from xlroles import VARIANTS as XV
    base={G['channel']:G['col'] for G in S.groups.values() if not G['glass'] and not G['emit'] and G['label']!='Augenmuschel'}
    out=[dict(id='base',name_de='Basis · Cube Escape',channels=dict(sorted(base.items())),glass_tint=info['tint'])]
    for (nm,pal),gt in zip(XV[1:4],VARIANT_TINTS[info['num']]):
        light,mid,dark,acc=pal
        ch={'MT_Primary':light,'MT_Secondary':dark,'MT_Accent':acc,'MT_Metal':mid}
        out.append(dict(id=nm.lower().replace('ü','ue'),name_de=nm.title(),channels={k:ch[k] for k in sorted(base)},glass_tint=gt))
    return out
# Glas der drei Farbvarianten (Arktis, Nacht, Wüste) je Visier; Tönungen aus dem Visier-Blatt
VARIANT_TINTS={'01':('clear','red','orange'),'02':('clear','green','orange'),'03':('light','red','orange'),'04':('clear','red','orange'),
 '05':('mirror','green','orange'),'06':('clear','red','orange'),'07':('blue','red','orange'),'08':('light','green','orange'),'09':('clear','red','orange')}

def build(vid):
    d=V.load(vid);S=d['S'];info=d['info'];geo=d['geo'];ly=geo['line_y'];win=geo['window']
    kind,window_kind=SIGHT_TYPES[info['type']]
    ids={g:f'g{k:02d}' for k,g in enumerate(S.order)}
    # Teile = Gruppen (Ringe bestehen im Modell aus mehreren Flächenteilen)
    parts=[]
    for g in S.order:
        G=S.groups[g];ps=[Pt for Pt in S.m.parts if Pt['group']==g]
        mat=G['material']
        parts.append(dict(id=ids[g],key=g,label=G['label'],channel=G['channel'],material=mat,toolgen_material=MATERIALS[mat],
                          emissive=bool(G['emit']),glass=bool(G['glass']),color=G['col'].upper(),
                          area_m2=round(sum(_area3(f['v']) for Pt in ps for f in Pt['F'])*UNIT*UNIT,6),bounds_m=BB(_bb(_verts(ps))),
                          module=g.startswith('module')))
    # Visierlinie
    xs=[q[0] for q in _verts(S.m.parts)];x0,x1=min(xs)-1,max(xs)+1
    hits=line_hits(S.m.parts,ly)
    blocked=sorted({ids[g] for g,_,gl in hits if not gl})
    glass_on=sorted({ids[g] for g,_,gl in hits if gl})
    rays,ap_bad=aperture_check(S,geo);ap_bad=sorted(ids[g] for g in ap_bad)
    # Anker
    tube=geo.get('tube')
    an=dict(
     Socket_Mount=dict(position_m=P((0,0,0)),source='Unterkante der Halterung, Mitte in Länge und Breite = Ursprung; liegt auf Socket_Sight des Waffen-Specs (Oberkante der Visierschiene)'),
     Socket_Sight=dict(position_m=P((win['x0'],ly,0)),source='hinterer Fensterrand auf der Visierlinie'+(' (Augenende der Röhre)' if tube else ' (Hinterkante des Rahmens)')),
     Socket_Reticle=dict(position_m=P((win['glass_x'],ly,0)),source='Glasmitte'+(' des Objektivs' if tube else '')+' auf der Visierlinie; Cube Escape zeichnet hier das Fadenkreuz'),
     Socket_Eye=dict(position_m=P((tube['eye_x'],ly,0)),source='Mitte des Okularglases (Augenlinse); Cube Escape legt das Scope-Bild 2 mm davor') if tube else None,
    )
    anchors={k:(dict(v,**ANCHOR_AXES) if v else None) for k,v in an.items()}
    mod=None
    if S.module:
        mp=[p for p in parts if p['module']];bb=[[min(p['bounds_m'][0][i] for p in mp) for i in range(3)],[max(p['bounds_m'][1][i] for p in mp) for i in range(3)]]
        cx=(bb[0][0]+bb[1][0])/2
        mod=dict(id=S.module,name_de=V.MODULES[S.module],side='left' if cx>0.002 else 'right' if cx<-0.002 else 'top',
                 parts=[p['id'] for p in mp],bounds_m=bb)
    fr=[p for p in parts if p['label']=='Rahmen']
    fb=[[min(p['bounds_m'][0][i] for p in fr) for i in range(3)],[max(p['bounds_m'][1][i] for p in fr) for i in range(3)]]
    gl=[p for p in parts if p['glass']]
    full=BB(_bb(_verts(S.m.parts)))
    sheets=weapon_sheets(info['tid'])
    spec=dict(
        format=FORMAT,format_version=FORMAT_VERSION,
        generator=dict(repo='cubeescape-design',tool='claude/generator/export_sight.py',claude_version=CLAUDE_VERSION,model='claude/generator/vsmodels.py'),
        sheet=dict(id=vid,file=f'{vid}.dc.html',series='VS',series_name_de='Visier-Serie',number=info['num']),
        weapon=dict(number=int(info['num']),name_de=info['weapon'],toolgen_id=info['tid'],
                    weapon_spec=dict(format=WEAPON_FORMAT,match='weapon.toolgen_id',sheets=sheets,
                                     mount='Socket_Mount dieses Specs liegt auf Socket_Sight des Waffen-Specs')),
        sight=dict(type=info['type'],type_de=V.TYPES_DE[info['type']],kind=kind,kind_source='aus type abgeleitet (export_spec.SIGHT_TYPES, claude-0.5.2)',
                   window_kind=window_kind,frame=info['frame'],title_de=info['title'],description_de=info['desc'],modular=True),
        axes=dict(model=dict(x='vorn (Blick)',y='unten',z='links',unit='mm'),target=dict(system='Blender',forward='-Y',up='+Z',left='+X',unit='m'),
                  matrix_model_to_target=M2B,model_unit_m=UNIT,origin='Socket_Mount',formula='p_m = model_unit_m * M · (p_model − Socket_Mount.model)'),
        dimensions_m=dict(length=r4(full[1][1]-full[0][1]),height=r4(full[1][2]-full[0][2]),width=r4(full[1][0]-full[0][0]),bounds_m=full,
                          line_height_m=r4(-ly*UNIT)),
        window=dict(shape=win['shape'],width_m=r4(win['w']*UNIT),height_m=r4(win['h']*UNIT),corner_radius_m=r4(win['r']*UNIT),
                    center_m=P((win['glass_x'],ly,0)),rear_edge_y_m=P((win['x0'],0,0))[1],front_edge_y_m=P((win['x1'],0,0))[1],
                    view_axis_m=[0.0,-1.0,0.0],free=not blocked and not ap_bad,
                    aperture=dict(rays=rays,blocked_by=ap_bad,step_m=APERTURE_STEP*UNIT,margin_m=APERTURE_MARGIN*UNIT,
                                  rule='Strahlen parallel zur Visierlinie im Raster 0,5 mm in der freien Öffnung (Röhre: Bohrung), Rand 0,3 mm; '
                                       'kein undurchsichtiges Teil darf einen schneiden'),
                    note='Maße = freie Öffnung (Innenkante Rahmen bzw. Leuchtrahmen); Röhre: Objektiv-Öffnung, die engste Stelle ist tube.bore_radius_m'),
        frame=dict(type=info['frame'],name_de=V.FRAMES[info['frame']],parts=[p['id'] for p in fr],
                   outer_width_m=r4(fb[1][0]-fb[0][0]),outer_height_m=r4(fb[1][2]-fb[0][2]),depth_m=r4(fb[1][1]-fb[0][1])),
        glass_tint=tint_rgba(info['tint']),
        glass=dict(id=info['tint'],name_de=V.TINTS[info['tint']][0],srgb=V.TINTS[info['tint']][1],alpha=V.TINTS[info['tint']][2],
                   space='glass_tint: RGB linear (aus sRGB), A = Deckkraft im Spiel',parts=[p['id'] for p in gl],
                   catalog={k:dict(name_de=v[0],srgb=v[1],rgba_linear=tint_rgba(k)) for k,v in V.TINTS.items()}),
        tube=dict(length_m=r4((tube['x1']-tube['x0'])*UNIT),lens_radius_m=r4(tube['lens_r']*UNIT),eye_radius_m=r4(tube['eye_r']*UNIT),
                  bore_radius_m=r4(tube['bore_r']*UNIT),
                  eye_anchor='Socket_Eye') if tube else None,
        module=mod,
        anchors=anchors,
        sight_line=dict(start_m=P((x0,ly,0)),end_m=P((x1,ly,0)),clear=not blocked,blocked_by=blocked,glass_crossed=glass_on,
                        rule='Visierlinie entlang −Y durch Socket_Sight und Socket_Reticle; keine Fläche außer Glas schneidet sie (alle Flächen geprüft, Newell-Normale)'),
        window_geometry=dict(elements=[dict(type='part',decal=None,part=p['id'],emissive=False,view_axis_m=[0.0,-1.0,0.0],
                                            center_m=[r4((p['bounds_m'][0][a]+p['bounds_m'][1][a])/2) for a in range(3)]) for p in gl],
                             source='Glasscheiben als Funktionsfläche (spec_checks.window_problems, Cubegen docs/DEVELOPER.md 9.17)'),
        parts=[{k:v for k,v in p.items() if k not in ('key','module')} for p in parts],
        reticle_variants=[dict(id=r,name_de=V.RETICLES[r],default=i==0) for i,r in enumerate(info['reticles'])],
        reticle_color=info['hud'],
        reticle_note='nur Bild auf dem Blatt; das Fadenkreuz zeichnet Cube Escape zur Laufzeit an Socket_Reticle',
        variants=variants(info,S),
        source=TARGET_SOURCE,
        summary=dict(parts=len(parts),channels=sorted({p['channel'] for p in parts}),glass_parts=len(gl),weapon_sheets=len(sheets)),
    )
    return spec

def path(vid):return os.path.join(OUT,f'{vid}.spec.json')
def main(argv):
    check='--check' in argv
    ids=[a for a in argv if not a.startswith('--')] or V.IDS
    bad=[]
    for vid in ids:
        txt=dumps(build(vid));fn=path(vid)
        if check:
            old=None
            if os.path.exists(fn):
                with open(fn,encoding='utf-8') as f:old=f.read()
            if old!=txt:bad.append(vid)
        else:
            with open(fn,'w',encoding='utf-8') as f:f.write(txt)
    if check:
        print('Sight-Specs aktuell' if not bad else 'veraltet oder fehlend: '+' '.join(bad)+'  (python3 claude/generator/export_sight.py)')
        return 1 if bad else 0
    print(len(ids),'Sight-Specs geschrieben nach',os.path.relpath(OUT))
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
