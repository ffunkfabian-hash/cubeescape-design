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
import sheetmodels,variants
from eng import CHANNELS,split_sight
from xlroles import MATERIAL_IDS,color_roles,material_of,assign_channels,channel_palettes
import skins as SK

FORMAT='cubeescape-design/weapon-spec'
FORMAT_VERSION=1
CLAUDE_VERSION='0.5.2'

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
 'KD01':('reflex','glass','Geometrie dmods.d01: Visierblock mit Leuchtpunkt vorn (claude-0.1.1)'),'KD02':('holo','glass','Bezeichnung Kastenvisier'),
 'KD03':('holo','glass','Geometrie dmods.d03: großer Kasten mit Leuchtfenster vorn'),'KD04':('reflex','glass','Geometrie dmods.d04: Visierblock mit Leuchtpunkt vorn (claude-0.1.1)'),
 'KD05':('scope','lens','Bezeichnung Zielfernrohr'),'KD06':('iron','none','Bezeichnung Kimme · Korn'),
 'KD07':('reflex','glass','Geometrie dmodels.d07: Visierblock mit Leuchtpunkt vorn'),'KD08':('scope','lens','Bezeichnung Zielfernrohr'),
 'KD09':('scope','lens','Geometrie dmodels.d09: Rohrvisier auf Stützen'),'KD10':('pin','open','Geometrie dmodels.d10: Pin-Visier mit Leuchtpunkt am Mittelstück (claude-0.1.1)'),
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

# Visier-Vokabular (claude-0.5.2, Entscheidung des Nutzers 17.10.2026): sight.type = Typ des Visiertypen-Blatts (Cube Escape
# Docs/Images/EquipmentConcepts/sight_types_1-9.webp) plus iron/pin für Blätter ohne Ziel; kind (Toolgen hold.sight_kind) und das
# Fenster folgen aus dem Typ. sight.frame = Rahmen-Variante des Visier-Blatts (weapon_sights_1-9.webp › Rahmen Varianten).
SIGHT_TYPES={   # type -> (kind, Fenster)
 'standard':('reflex','glass'),'holo':('holo','glass'),'precision':('scope','lens'),'reflex':('reflex','glass'),
 'sniper':('scope','lens'),'machine':('reflex','glass'),'energy':('energy','glass'),'trace':('holo','glass'),'rocket':('holo','glass'),
 'iron':('iron',None),'pin':('pin',None)}
SIGHT_FRAMES=('standard','compact','open','closed','industrial','lightweight')
def sight_type(kind,tid):
    """Typ eines bestehenden Blatts aus seiner Kennung: Zielfernrohr am Scharfschützengewehr = sniper, sonst precision."""
    if kind=='scope':return 'sniper' if tid=='sniper_rifle' else 'precision'
    return kind
def sight_frame(window):
    """Rahmen bestehender Blätter (Regel nach der Sichtprüfung 0.5.1): Scheibe im Kasten/Haube = closed, Röhre = standard,
    Ring/Lochblende = open, Kimme/Korn ohne Rahmen = null."""
    return {'glass':'closed','lens':'standard','open':'open'}.get(window)
# Material der Teile im Wortschatz von Toolgen data/surface_recipes.json › materials (claude-0.5.2)
TOOLGEN_MATERIAL={'painted':'painted','brushed':'brushed','rubber':'rubber','matte':'painted_matte','lit':'energy_glass'}

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

PROJECTILE_LABELS=('Rakete',)   # Geschoss im Rohr: gehört nicht zur Waffe (Toolgen: kein Projektil im Asset)
def _projectile(gun,tol=1.0):
    """Teile des Geschosses: bezeichnete Raketen und unbezeichnete Teile in ihrem Querschnitt, die als Kette hinten an ihr
    anschließen (Rumpf, Ringe); bezeichnete Teile und abgesetzte Teile bleiben Waffe."""
    out=set()
    for i,R in gun:
        if R.get('label') not in PROJECTILE_LABELS:continue
        rb=_bb(_verts([R]));out.add(i);rear=rb[0][0]
        while True:
            nxt=[(k,b) for k,P in gun for b in [_bb(_verts([P]))] if k not in out and P.get('label') is None
                 and all(rb[0][a]-tol<=b[0][a] and b[1][a]<=rb[1][a]+tol for a in (1,2)) and b[1][0]>=rear-tol and b[0][0]<rear-tol]
            if not nxt:break
            k,b=min(nxt,key=lambda t:t[1][0][0]);out.add(k);rear=b[0][0]
        for k,P in gun:   # Kleinteile innerhalb der Kette (Bänder, Nasenring)
            b=_bb(_verts([P]))
            if P.get('label') is None and all(rb[0][a]-tol<=b[0][a] and b[1][a]<=rb[1][a]+tol for a in (1,2)) and rear-tol<=b[0][0] and b[1][0]<=rb[1][0]+tol:out.add(k)
    return out

def _muzzle_front(gun,front,cc,tol=1.0):
    """Vorderes Ende der Mündungsachse: verlängert die Vorderkante über unbezeichnete (oder Mündungs-)Teile, die die Achse
    (Querschnittsmitte cc) schneiden und vorn anschließen – Mündungskappen, Leuchtköpfe, Pfeilspitzen. Geschosse zählen nicht."""
    proj=_projectile(gun);ext=[]
    while True:
        nxt=[(i,b) for i,P in gun for b in [_bb(_verts([P]))]
             if i not in proj and i not in ext and (P.get('label') is None or P.get('label') in MUZZLE_LABELS)
             and b[0][1]-tol<=cc[1]<=b[1][1]+tol and b[0][2]-tol<=cc[2]<=b[1][2]+tol and b[0][0]<=front+tol and b[1][0]>front+tol]
        if not nxt:return front,ext
        i,b=max(nxt,key=lambda t:t[1][1][0]);ext.append(i);front=b[1][0]

# Bewegliche Teile (Use-Clip) wie in Toolgen 0.7: docs/TECHNIK.md › Waffen 1–9 › Use-Clip und
# scripts/tool_assets/weapon_designs.py DESIGNS[…]['use_clip'] (Stand Toolgen c926f50, 17.10.2026). Die Wurzel bewegt sich nie.
# Achsen im Toolgen-Rahmen: translate = Richtung der Bewegung aus der Ruhe (zurück = +Y), rotate = Drehachse (Vorzeichen, Weg und
# Bilder legt Toolgen im Clip fest). labels: Bezeichnung des Teils im Blatt (match 'label'); similar: ähnliches Teil, Toolgen entscheidet.
MOTION_SOURCE="Toolgen docs/TECHNIK.md › Waffen 1–9 › Use-Clip; scripts/tool_assets/weapon_designs.py DESIGNS[…]['use_clip'] (Toolgen c926f50, 17.10.2026)"
MOTIONS={
 'slide':dict(node='Anim_Slide',de='Schlitten',motions=[('translate',[0,1,0])],labels=('Schlitten',),similar=('Verschluss',)),
 'bolt':dict(node='Anim_Bolt',de='Verschluss',motions=[('translate',[0,1,0])],labels=('Verschluss','Ladehebel','Spannhebel'),similar=()),
 'cell':dict(node='Anim_Cell',de='Zelle (Impulse)',motions=[('translate',[0,1,0])],labels=('Zelle','Pulszelle'),
             similar=('Kristallkern','Energiekugel','Pulswürfel')),
 'fins':dict(node='Anim_FinL/Anim_FinR',de='Flossen (links/rechts gegenläufig)',motions=[('rotate',[0,0,1])],labels=('Flossen','Finnen'),similar=()),
 'coil':dict(node='Anim_Coil',de='Spulenring',motions=[('rotate',[0,1,0])],labels=('Spulenring','Spulenringe'),similar=('Beschleunigerring',)),
 'pump':dict(node='Anim_Bolt',de='Repetierschieber',motions=[('translate',[0,1,0])],labels=('Pumpgriff','Repetierschieber'),similar=()),
 'lever':dict(node='Anim_Bolt',de='Kammerstängel (drehen, zurück, vor, drehen)',motions=[('rotate',[0,1,0]),('translate',[0,1,0])],
              labels=('Kammerstängel','Kammer'),similar=('Verschluss',)),
 'hatch':dict(node='Anim_Hatch',de='Ladeklappe',motions=[('rotate',[1,0,0])],labels=('Ladeklappe','Klappe'),similar=()),
}
WEAPON_MOTIONS={'pistol':['slide'],'assault_rifle':['bolt'],'pulse_rifle':['cell'],'shotgun':['pump'],'sniper_rifle':['lever'],
 'smg':['bolt'],'fusion_rifle':['fins','coil'],'scout_rifle':['bolt'],'rocket_launcher':['hatch'],'bow':[]}

def moving_parts(tid,allparts,ids):
    """moving_parts (claude-0.5) und je Teil die Art: Zuordnung über die Bezeichnungen des Modells, Visierteile ausgenommen."""
    items=[];per={}
    for kind in WEAPON_MOTIONS[tid]:
        M=MOTIONS[kind];e=dict(kind=kind,name_de=M['de'],toolgen_node=M['node'],motions=[dict(type=t,axis=a) for t,a in M['motions']])
        for match,labs in (('label',M['labels']),('similar',M['similar'])):
            hit=[(i,P) for i,P in allparts if not P.get('sight') and P.get('label') in labs]
            if hit:
                e.update(parts=[ids[i] for i,_ in hit],labels=sorted({P['label'] for _,P in hit}),match=match,
                         source=('Bezeichnung ' if match=='label' else f'ähnliches Teil zu „{M["de"]}“ (Toolgen entscheidet): ')
                                +', '.join(f'„{P["label"]}“ ({ids[i]})' for i,P in hit))
                for i,_ in hit:per[i]=kind
                break
        else:
            e.update(parts=None,labels=[],match=None,
                     source=f'nicht ableitbar: kein Teil mit Bezeichnung {"/".join(M["labels"]+M["similar"])} im Modell (Mechanik im Gehäuse nicht gezeichnet)')
        items.append(e)
    note=None if items else 'keine Use-Clip-Mechanik: der Bogen gehört nicht zu Toolgens Waffen 1–9'
    return dict(source=MOTION_SOURCE,root_moves=False,frame='Toolgen-Rahmen (vorn −Y, oben +Z, links +X); translate: Richtung aus der Ruhe, rotate: Drehachse',
                items=items,note=note),per

# Größe in der Roboterhand (claude-0.5.1, Entscheidung des Nutzers 17.10.2026: „in Spec 1.x mit aufnehmen“). Zahlen aus Cube Escape
# (Stand 677841ff, 17.10.2026); Längen = „Länge in der Hand“ der Tabelle, auf cm gerundet.
CE_EQ='Cube Escape Docs/EQUIPMENT.md › Größe in der Roboterhand (0.82)'
CE_S2='Cube Escape Docs/versions/0.82.md › Stufe 2 (Auftrag an Toolgen)'
ROBOT_LENGTH={'smg':0.52,'assault_rifle':0.67,'pulse_rifle':0.66,'shotgun':0.67,'fusion_rifle':0.67,'scout_rifle':0.69,
 'sniper_rifle':0.73,'rocket_launcher':0.65}
def _v(value,source):return dict(value=value,source=source)
def robot_fit(tid,anchors,parts,dims,muzzle_part):
    """robot_fit: Zielmaße einer Roboter-Variante (Toolgen Stufe 2) und das Blatt, auf die Ziellänge skaliert, daran gemessen."""
    robot=dict(height_m=_v(1.50,CE_EQ+' › Maße des Roboters'),hand_m=_v(0.09,CE_EQ+' › Maße des Roboters'),
               arm_m=_v(0.42,CE_EQ+' › Maße des Roboters'))
    base=dict(source=f'{CE_EQ}; {CE_S2} (CE 677841ff, 17.10.2026)',robot=robot,concept_sheets=False,concept_sheets_reason='keine Roboter-Konzeptblätter (Entscheidung des Nutzers 17.10.2026)')
    if tid=='pistol':
        return dict(base,applies=False,reason='Pistole von der Roboter-Variante ausgenommen: Maßstab genügt, Becher-Griff sitzt ('+CE_S2+')',
                    targets=dict(length_min_m=_v(0.24,CE_EQ+' › Begründung (1): knapp drei Handlängen')),sheet_at_target=None)
    if tid not in ROBOT_LENGTH:
        return dict(base,applies=False,reason='nicht im Waffensatz von Cube Escape (Bogen: Referenzmodell, kein Spielwerkzeug)',
                    targets=None,sheet_at_target=None)
    L=ROBOT_LENGTH[tid]
    targets=dict(length_m=_v(L,CE_EQ+' › Tabelle, Länge in der Hand (gerundet)'),
                 support_hand_max_forward_m=_v(0.10,CE_S2+': Socket_SupportHand höchstens 0,10 m vor Socket_Hand'),
                 stock_max_behind_m=_v(0.12,CE_S2+': Schaft höchstens 0,12 m hinter Socket_Hand'),
                 barrel_min_m=_v(0.03,CE_S2+': Lauf ≥ 3 cm'),receiver_min_height_m=_v(0.08,CE_S2+': Gehäuse ≥ 8 cm hoch'),
                 silhouette_factor=_v(1.5,CE_S2+': Querschnitt von Gehäuse und Lauf etwa 1,5fach (Bezug: Toolgen-Weltmodell, am Blatt nicht messbar)'))
    s=L/dims['with_sight']['length']
    sup=anchors['Socket_SupportHand']['position_m'];back=dims['with_sight']['bounds_m'][1][1]
    def ext(p):b=p['bounds_m'];return [b[1][k]-b[0][k] for k in range(3)]
    mp=[p for p in parts if p['id']==muzzle_part]
    rec=[p for p in parts if p['label']=='Gehäuse' and not p['sight']]
    m=dict(scale=r4(s),
           support_forward_m=r4(s*-sup[1]) if sup else None,
           stock_behind_m=r4(s*back),
           barrel_m=r4(s*min(ext(mp[0])[0],ext(mp[0])[2])) if mp else None,
           receiver_height_m=r4(s*max(ext(p)[2] for p in rec)) if rec else None,
           basis='Blatt auf targets.length_m skaliert (Länge entlang der Mündungsachse, Visier montiert); Lauf = kleinerer Querschnitt des '
                 'Mündungsteils, Gehäuse = größte Höhe eines Teils „Gehäuse“')
    m['ok']=dict(support_forward=None if m['support_forward_m'] is None else m['support_forward_m']<=0.10,
                 stock_behind=m['stock_behind_m']<=0.12,
                 barrel=None if m['barrel_m'] is None else m['barrel_m']>=0.03,
                 receiver_height=None if m['receiver_height_m'] is None else m['receiver_height_m']>=0.08)
    return dict(base,applies=True,reason=None,targets=targets,sheet_at_target=m)

def _newell(pts):
    n=[0.0,0.0,0.0]
    for k in range(len(pts)):
        (x0,y0,z0),(x1,y1,z1)=pts[k],pts[(k+1)%len(pts)]
        n[0]+=(y0-y1)*(z0+z1);n[1]+=(z0-z1)*(x0+x1);n[2]+=(x0-x1)*(y0+y1)
    L=math.sqrt(sum(c*c for c in n)) or 1.0
    return [c/L for c in n]
def _view_axis(n):
    """Achse ohne Vorzeichen: größte Komponente negativ (Fenster nach vorn −Y), gerundet."""
    k=max(range(3),key=lambda a:abs(n[a]));s=-1 if n[k]>0 else 1
    return [r4(s*c)+0.0 for c in n]

PANE_MIN_FRACTION=0.075   # Seitenaufkleber ab diesem Anteil der Teilfläche gilt als Scheibe/Öffnung (Sichtprüfung 0.5.1: Punkte ≤ 0,06)
def _disc(e):
    """Scheibe/Ring/Platte: zwei Ausdehnungen ähnlich (≥ 75 %), die dritte höchstens 40 % davon; liefert die Achse oder None."""
    o=sorted(range(3),key=lambda a:e[a])
    return o[0] if e[o[0]]<=0.4*e[o[1]] and e[o[1]]>=0.75*e[o[2]] else None
def window_geometry(window,sight_parts,ids,F,decal_index):
    """Fenster des Visiers als Funktionsfläche (claude-0.5, erweitert 0.5.2; Cubegen docs/DEVELOPER.md 9.17): alle Aufkleber vorn/
    hinten auf Visierteilen (Scheibe, Linse, Leuchtpunkt), Seitenaufkleber ab PANE_MIN_FRACTION der Teilfläche (Scheibe oder Öffnung
    auf der Seite), leuchtende Visierteile und Scheiben/Ringe/Platten (type disc). Achse aus der Geometrie (Newell-Normale bzw.
    dünnste Ausdehnung), nicht aus der Flächenbezeichnung; ob sie entlang −Y liegt, prüft spec_checks."""
    if window in (None,'none'):return None,'kein Fenster (Kimme/Korn bzw. kein Visier)'
    el=[]
    for i,P in sight_parts:
        b=F.bb(_bb(_verts([P])));e=[b[1][a]-b[0][a] for a in range(3)]
        for k,(plane,val,pts,col,em) in enumerate(P['dec']):
            q=[F.p(v) for v in _decal3(plane,val,pts)];n=_newell(q);ax=max(range(3),key=lambda a:abs(n[a]))
            face=max(1e-12,e[(ax+1)%3]*e[(ax+2)%3]);frac=_area2(pts)*F.u*F.u/face
            if plane[0]!='x' and frac<PANE_MIN_FRACTION:continue
            el.append(dict(type='decal',decal=decal_index[(i,k)],part=ids[i],emissive=bool(em),view_axis_m=_view_axis(n),
                           center_m=[r4(sum(v[a] for v in q)/len(q)) for a in range(3)],face_fraction=round(frac,3)))
        c=[r4((b[0][a]+b[1][a])/2) for a in range(3)]
        if P['emit']:
            k=min(range(3),key=lambda a:e[a])
            el.append(dict(type='part',decal=None,part=ids[i],emissive=True,view_axis_m=[0.0 if a!=k else -1.0 for a in range(3)],center_m=c))
        elif window in ('open','lens') and _disc(e) is not None:   # Ring/Lochplatte bzw. Linsenring; bei Scheiben-Visieren (glass) keine Öffnung
            k=_disc(e)
            el.append(dict(type='disc',decal=None,part=ids[i],emissive=False,view_axis_m=[0.0 if a!=k else -1.0 for a in range(3)],center_m=c))
    if not el:return None,'kein Fensterelement im Modell (Fenster nur in Bezeichnung/Text)'
    return dict(elements=el,source='Aufkleber vorn/hinten, Seitenaufkleber als Scheibe/Öffnung, leuchtende Visierteile, Scheiben/Ringe; '
                'Achse aus der Geometrie'),None

def _anchors(d,gun,sight_parts,allparts,ids):
    hand=_pick_hand(gun)
    an={};notes={}
    if hand[0] is not None:
        hc=_center(_bb(_verts([hand[1]])));an['Socket_Hand']=(hc,f'Mitte von {ids[hand[0]]} ({hand[1]["label"]})',hand[0])
    else:
        hc=_center(_bb(_verts([P for _,P in gun])));an['Socket_Hand']=(hc,'kein Griff bezeichnet: Mitte der Waffe')
    # Stützhand
    sup=None
    c=[(i,P) for i,P in gun if P.get('label') in SUPPORT_LABELS]
    if c:
        i,P=min(c,key=lambda t:abs(_center(_bb(_verts([t[1]])))[0]-hc[0]));sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} ({P["label"]})',i)
    else:
        g2=[(i,P) for i,P in gun if P.get('label') in HAND_LABELS and i!=hand[0] and _center(_bb(_verts([P])))[0]>hc[0]+10]
        if g2:
            i,P=min(g2,key=lambda t:_center(_bb(_verts([t[1]])))[0]);sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} (zweiter Griff)',i)
        else:
            gd=[(i,P) for i,P in gun if P.get('label') in GUARD_LABELS and _center(_bb(_verts([P])))[0]>hc[0]]
            if gd:
                i,P=max(gd,key=lambda t:_area(t[1]));sup=(_center(_bb(_verts([P]))),f'Mitte von {ids[i]} ({P["label"]})',i)
    if sup:an['Socket_SupportHand']=sup
    else:notes['Socket_SupportHand']='nicht ableitbar (kein Vordergriff, zweiter Griff oder Handschutz vor dem Griff)'
    # Mündung
    mz=[(i,P) for i,P in gun if P.get('label') in MUZZLE_LABELS]
    src='vorderstes bezeichnetes Mündungs-/Laufteil'
    if not mz:mz=gun;src='vorderstes Teil (kein Lauf bezeichnet)'
    i,P=max(mz,key=lambda t:_bb(_verts([t[1]]))[1][0]);bb=_bb(_verts([P]));cc=_center(bb)
    front,ext=_muzzle_front(gun,bb[1][0],cc)
    tail=f', verlängert über {", ".join(ids[k] for k in ext)} (ohne Bezeichnung, auf der Mündungsachse)' if ext else ''
    an['Socket_Muzzle']=([front,cc[1],cc[2]],f'{src}: Vorderkante von {ids[i]} ({P.get("label") or "ohne Bezeichnung"}){tail}, Querschnittsmitte',i)
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
            an['Socket_Sight']=([cc[0],bb[0][1],cc[2]],f'Oberkante Mitte von {ids[i]} (Visierschiene, kein Visier im Modell)',i)
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
    # Kanäle und Paletten je Variante (xlroles.channel_palettes, auch für die Skins)
    palette,pch=channel_palettes(full,gun_m,d['palette'],d['pill'],CHANNELS)
    dch=[[c for c,_ in row] for row in assign_channels(full,color_roles(gun_m),_area,lambda dd:_area2(dd[2]),d['palette'])[1]]
    moving,moving_of=moving_parts(tid,allparts,ids)
    # Teile
    parts=[]
    for i,P in allparts:
        bb=_bb(_verts([P]));ext=[bb[1][k]-bb[0][k] for k in range(3)]
        parts.append(dict(id=ids[i],label=P.get('label'),channel=pch[i][0],channel_source=pch[i][1],
                          material=MATERIAL_IDS[material_of(P)],toolgen_material=TOOLGEN_MATERIAL[MATERIAL_IDS[material_of(P)]],emissive=bool(P['emit']),sight=bool(P.get('sight')),
                          color=_hex(P['col']),area_m2=round(_area(P)*unit*unit,6),long_axis=AXIS_NAMES[ext.index(max(ext))],
                          bounds_m=F.bb(bb),moving=moving_of.get(i)))
    decals=[];decal_index={}
    for i,P in allparts:
        for k,(plane,val,pts,col,em) in enumerate(P['dec']):
            v3=_decal3(plane,val,pts);decal_index[(i,k)]=len(decals)
            decals.append(dict(part=ids[i],channel=dch[i][k],surface=SURFACES[plane],emissive=bool(em),color=_hex(col),
                               area_m2=round(_area2(pts)*unit*unit,7),bounds_m=F.bb(_bb(v3))))
    # Visier
    # ab J (jlib): Visierart steht im Modell (META['sight'] in <v>NN.py)
    kind,window,ssrc=SIGHTS[sheet] if sheet in SIGHTS else (*d['sight'],f"META sight in {d['fid']}.py")
    if sight_parts:
        sb=_bb(_verts([P for _,P in sight_parts]));gb=_bb(_verts([P for _,P in gun]))
        gz=_center(gb)[2];side='left' if sb[0][2]>gz+5 else 'right' if sb[1][2]<gz-5 else 'top'
        st=sight_type(kind,tid);assert SIGHT_TYPES[st][0]==kind,(sheet,st,kind)
        sight=dict(present=True,kind=kind,window=window,source=ssrc,modular=True,mount_side=side,
                   type=st,type_source='aus kind abgeleitet (bestehendes Blatt; Zielfernrohr am Scharfschützengewehr = sniper)',
                   frame=sight_frame(window),frame_source='Regel aus window nach Sichtprüfung 0.5.1 (glass closed, lens standard, open open, none null)',
                   labels=sorted({P.get('label') for _,P in sight_parts if P.get('label')}),parts=[ids[i] for i,_ in sight_parts],
                   bounds_m=F.bb(sb),anchor='Socket_Sight')
        sight['window_geometry'],sight['window_geometry_note']=window_geometry(window,sight_parts,ids,F,decal_index)
    else:
        sight=dict(present=False,kind=None,window=None,source=ssrc,modular=True,mount_side=None,labels=[],parts=[],bounds_m=None,
                   type=None,type_source='kein Visier',frame=None,frame_source='kein Visier',
                   anchor='Socket_Sight' if 'Socket_Sight' in an else None,window_geometry=None,window_geometry_note='kein Visier')
    def dims(parts_):
        bb=F.bb(_bb(_verts(parts_)));e=[r4(bb[1][k]-bb[0][k]) for k in range(3)]
        return dict(length=e[1],height=e[2],width=e[0],bounds_m=bb)
    anchors={k:dict(position_m=F.p(v[0]),model=[round(x,2) for x in v[0]],source=v[1],part=ids[v[2]] if len(v)>2 and v[2] is not None else None)
             for k,v in an.items()}
    for k in ('Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight'):
        if k not in anchors:anchors[k]=dict(position_m=None,model=None,source=notes.get(k,'nicht ableitbar'),part=None)
    anchors={k:anchors[k] for k in ('Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight')}
    used=[ch for ch in CHANNELS if palette[0]['channels'][ch]]
    dims_=dict(weapon=dims([P for _,P in gun]),with_sight=dims(full.parts))
    return dict(
        format=FORMAT,format_version=FORMAT_VERSION,
        generator=dict(repo='cubeescape-design',tool='claude/generator/export_spec.py',claude_version=CLAUDE_VERSION),
        sheet=dict(id=sheet,file=f'{sheet}.dc.html',variant=d['V'],variant_name=variants.name(d['V']),number=d['num'],nick=d['nick'],fid=d['fid']),
        weapon=dict(name_de=d['name'],toolgen_id=tid),
        element=element,element_source=ELEMENT_SOURCE if element else 'nicht festgelegt (Toolgen-Bogen ohne Element)',
        units=dict(model_unit_m=round(unit,8),model_length_units=round(model_len,2),reference_length_m=ref_len,rule=rule,
                   reference='Toolgen 0.13 Weltmodell '+tid+', qa_game.json bounds_lod0.source_bounds_m (Messung 17.10.2026)'),
        axes=dict(model=dict(x='vorn (Mündung)',y='unten',z='links'),target=dict(system='Toolgen/Blender',forward='-Y',up='+Z',left='+X',unit='m'),
                  matrix_model_to_target=M2B,origin='Socket_Hand',
                  formula='p_m = model_unit_m * M · (p_model − Socket_Hand.model)'),
        dimensions_m=dims_,
        anchors=anchors,
        palette=palette,
        channels_used=used,
        parts=parts,
        moving_parts=moving,
        robot_fit=robot_fit(tid,anchors,parts,dims_,anchors['Socket_Muzzle']['part']),
        sight=sight,
        decals=decals,
        textures=textures(unit),
        skin=skin_spec(sheet,full,d,palette,F,ids,unit),
        summary=dict(skins=5,parts=len(parts),parts_explicit_channel=sum(1 for c in pch if c[1]=='explicit'),decals=len(decals),
                     channels_with_other_colors={p['id']:sorted(p['other_colors']) for p in palette if p['other_colors']}),
    )

def textures(unit):
    """Muster der Material-Ansicht des Blatts (xl.make_texture) als Zielbild für Toolgens Bake, im Wortschatz von
    Toolgen data/surface_recipes.json › patterns (knurl/brushed/grain; Größen in mm, Werkzeugrahmen Socket_Hand).
    brightness = Helligkeitsfaktor auf die Kanalfarbe im Blatt; Längen sind Weltlängen am Modell (keine UV).
    Wellenachsen im Zielrahmen: Blatt-y -> Z, Blatt-(x+z) -> X−Y (Richtung, Vorzeichen egal: Kosinus)."""
    mm=lambda v:round(v*unit*1000,3)
    return dict(
        source='xl.make_texture (Materialansicht des Blatts), Modelleinheiten mal model_unit_m',
        vocabulary='Toolgen data/surface_recipes.json › patterns',
        painted=dict(toolgen_pattern=None,look='weicher Glanzverlauf, kein Relief',brightness=[0.87,1.13],
                     waves=[dict(axis='Z',wavelength_mm=mm(2*math.pi*26),amplitude=0.09),
                            dict(axis='X-Y',wavelength_mm=mm(2*math.pi*55),amplitude=0.04)]),
        brushed=dict(toolgen_pattern='brushed',direction='long_axis',size_mm=mm(2*math.pi/(7.3*0.9)),brightness=[0.87,1.13],
                     cross_wavelengths_mm=[mm(2*math.pi/(3.1*0.9)),mm(2*math.pi/(7.3*0.9)),mm(2*math.pi/(13.1*0.9))],weights=[0.5,0.3,0.2]),
        rubber=dict(toolgen_pattern='knurl',direction='Flächenebene, ±45°',size_mm=mm(4.0),brightness=[0.66,1.0]),
        matte=dict(toolgen_pattern='grain',size_mm=mm(1/1.3),brightness=[0.955,1.045]),
        lit=dict(toolgen_pattern=None,look='leuchtend, Kanalfarbe als Emission, kein Muster'),
    )

NEW_PATTERNS={
 'side_block':'Farbfläche: Polygon in der Seitenprojektion (Punkte [Y, Z] in m), durch die ganze Breite (X) extrudiert; Teile im Polygon tragen den Slot',
 'bands':'Streifen: t = p · dir (m, Ursprung Socket_Hand); Band k (0 ≤ k < count) bei t0_m + k·period_m ≤ t < … + width_m, Slot slots[k mod n]; optional nur im Fenster window (wie side_block)',
 'gradient':'Verlauf: s = (p · dir − t0_m) / (t1_m − t0_m), auf 0..1 begrenzt, in steps Stufen; Farbe gemischt von slots[0] nach slots[1] (Toon-Stufen, keine Kanal-Maske)',
 'rings':'konzentrische Ringe um die Achse X durch center [Y, Z]: Abstand r in der Seitenprojektion; Ring k bei r0_m + k·(width_m+gap_m) ≤ r < … + width_m, Slot slots[k mod n]',
 'finish':'ganzes Teil im Slot; Oberfläche des Slots (polished_gold/polished_chrome: hochglänzend metallisch, Glanzstreifen im Blatt nur Zeichnung)',
 'edge_wear':'Kantenabnutzung: blankes Metall (color) entlang harter Kanten bis width_mm, fleckig mit Anteil coverage (Blender: Pointiness/AO-Maske)',
 'glyph_decals':'Glyphen/Zahlen/Embleme als flache Aufkleber: Polygone mit Punkten [X, Y, Z] in m auf der Seitenfläche (left +X, right −X, rechte Seite gespiegelt lesbar)',
 'trim':'Schmuckteile als zusätzliche Prismen: Profil [Y, Z] in m, extrudiert über x_m [X0, X1]; ribs (Rippen an der Seite), fins (Finnen oben)',
}
def skin_spec(sheet,full,d,palette,F,ids,unit):
    """Skins des Blatts (skins.py) im Toolgen-Rahmen: fünf je Waffe, der erste ist der Hauptskin des Blatts."""
    o=F.o
    def dvec(v):return [r4(sum(M2B[r][c]*v[c] for c in range(3))) for r in range(3)]
    def tm(t,dv):return r4(unit*(t-sum(o[k]*dv[k] for k in range(3))))
    def yz(x,y):p=F.p((x,y,o[2]));return [p[1],p[2]]
    def xm(z):return r4(unit*(z-o[2]))
    def L_(v):return r4(v*unit)
    sids=SK.pick(sheet,full,d['num'],d['palette'])
    items=[]
    for sid in sids:
        rs=SK.resolve(full,sid,sheet,d['num'],d['palette']);used=SK.slots_used(rs)
        cols={}
        for p in palette:
            cs=SK.slot_colors(rs,p['channels'],p['swatches'])
            cols[p['id']]={s_:dict(color=cs[s_][0],finish=cs[s_][1],source=cs[s_][2]) for s_ in used}
        layers=[]
        for L in rs['layers']:
            t=L['type'];e=dict(type=t,block=SK.LAYER_BLOCK[t])
            if t=='finish':e.update(parts=[ids[i] for i in L['parts']],slot=L['slot'],target=L['target'])
            elif t=='side_block':e.update(pattern='side_block',parts=[ids[i] for i in L['parts']],slot=L['slot'],poly_yz_m=[yz(*q) for q in L['poly']])
            elif t=='bands':
                e.update(pattern='bands',parts=[ids[i] for i in L['parts']],dir=dvec(L['dir']),t0_m=tm(L['t0'],L['dir']),width_m=L_(L['width']),
                         period_m=L_(L['period']),count=L['count'],slots=L['slots'],window_yz_m=[yz(*q) for q in L['window']] if L.get('window') else None)
            elif t=='gradient':
                e.update(pattern='gradient',parts=[ids[i] for i in L['parts']],dir=dvec(L['dir']),t0_m=tm(L['t0'],L['dir']),t1_m=tm(L['t1'],L['dir']),
                         steps=L['steps'],slots=L['slots'])
            elif t=='rings':
                e.update(pattern='rings',parts=[ids[i] for i in L['parts']],axis='X',center_yz_m=yz(*L['center']),r0_m=L_(L['r0']),width_m=L_(L['width']),
                         gap_m=L_(L['gap']),count=L['count'],slots=L['slots'])
            elif t=='edge_wear':
                e.update(pattern='edge_wear',parts=[ids[i] for i in L['parts']],width_mm=r4(L['width']*unit*1000),coverage=L['coverage'],color=L['color'])
            elif t=='glyphs':
                x0,y0,x1,y1=L['rect']
                e.update(pattern='glyph_decals',part=ids[L['part']],items=L['items'],content=L['content'],height_m=L_(L['height']),
                         bounds_m=F.bb(([x0,y0,full.parts[L['part']]['F'][1]['v'][0][2]],[x1,y1,full.parts[L['part']]['F'][0]['v'][0][2]])),
                         decals=[dict(surface=SURFACES[pl],slot=sl,points_m=[F.p(q) for q in _decal3(pl,val,pts)]) for pl,val,pts,sl in L['decals']])
            elif t=='trim':
                e.update(pattern='trim',kind=L['kind'],slot=L['slot'],attach=ids[L['attach']],count=L['count'],toolgen_similar='lamellae' if L['kind']=='ribs' else None,
                         parts=[dict(profile_yz_m=[yz(*q) for q in tp['prof']],x_m=sorted([xm(tp['z0']),xm(tp['z1'])]),
                                     bounds_m=F.bb(([min(q[0] for q in tp['prof']),min(q[1] for q in tp['prof']),tp['z0']],
                                                    [max(q[0] for q in tp['prof']),max(q[1] for q in tp['prof']),tp['z1']]))) for tp in L['parts']])
            rq=L.get('requested');got=L.get('slots',[L.get('slot')])
            if rq is not None and list(rq if isinstance(rq,list) else [rq])!=list(got):
                e['requested']=rq;e['requested_reason']=f'Kontrastregel: Abstand zur Körperfarbe {rs["body_color"]} unter {SK.MIN_CONTRAST} (RGB 0..1)'
            if t=='glyphs':e['slots']=L['slots']
            layers.append(e)
        items.append(dict(id=sid,name=rs['name'],hero=sid==sids[0],blocks=SK.summary(rs),
                          description_de=SK.DESC[sid][0],description_en=SK.DESC[sid][1],
                          accents={a:dict(color=c,finish=f) for a,(c,f) in rs['accents'].items()},
                          slots_used=used,colors=cols,layers=layers,notes=rs['notes']))
    return dict(source='claude/generator/skins.py (Katalog, Auflösung), Zeichnung xl.py/skinraster.py (Feld SKIN/MUSTER, Hauptskin in Isometrie, Orthos, Farbvarianten)',
                hero=sids[0],catalog=[s_['id'] for s_ in SK.CATALOG],
                slots=dict(channels=list(CHANNELS),accents=list(SK.ACCENTS),
                           rule='MT_-Kanäle färben mit der Variante um (unbelegter Kanal: Farbfeld der Blatt-Palette, source swatch); SK_Accent1/2 fest je Skin'),
                finishes=list(SK.FINISHES),space='Objektraum (Toolgen-Rahmen, m), keine UV; Sichtteile ohne Skin',
                vocabulary='Toolgen data/surface_recipes.json › patterns kennt nur Relief (knurl, grooves, lamellae, seams, brushed, grain); Skin-Muster sind neue Typen (new_pattern_types)',
                new_pattern_types=NEW_PATTERNS,items=items)

_NUMS=re.compile(r'\[\s*((?:-?[\d.eE+-]+|null)(?:,\s*(?:-?[\d.eE+-]+|null))*)\s*\]')
_PTS=re.compile(r'\[\s*\[[^\[\]]*\](?:,\s*\[[^\[\]]*\])+\s*\]')
def dumps(spec):
    """JSON mit Einzug; Zahlenlisten (Koordinaten, Matrixzeilen) bleiben in einer Zeile."""
    txt=json.dumps(spec,ensure_ascii=False,indent=1)
    txt=_NUMS.sub(lambda mm:'['+', '.join(x.strip() for x in mm.group(1).split(','))+']',txt)
    # Punktlisten (Polygone der Skins, ab drei Punkten) ebenfalls in einer Zeile
    return _PTS.sub(lambda mm:'['+', '.join(re.findall(r'\[[^\[\]]*\]',mm.group(0)))+']' if mm.group(0).count('[')>=4 else mm.group(0),txt)+'\n'
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
