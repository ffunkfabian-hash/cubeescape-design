"""Canonical cubeescape-design/weapon-spec v1 exporter for Codex weapon models.

The existing CodexDesignReference remains a separate, optional record. This module
serializes its independently authored model inputs into the shared consumer schema.
"""
from __future__ import annotations
import json
from pathlib import Path

FORMAT = 'cubeescape-design/weapon-spec'
VERSION = 1
TOOLGEN = {
    'pistol': ('pistol', .243, 'solar'), 'assault': ('assault_rifle', .934, 'arc'),
    'impulse': ('pulse_rifle', .862, 'void'), 'shotgun': ('shotgun', .904, 'solar'),
    'sniper': ('sniper_rifle', 1.134, 'energy'), 'smg': ('smg', .616, 'energy'),
    'fusion': ('fusion_rifle', .960, 'void'), 'trace': ('scout_rifle', 1.044, 'arc'),
    'rocket': ('rocket_launcher', .725, 'solar'), 'bow': ('bow', 1.018, None),
}
CHANNELS = ('MT_Primary','MT_Secondary','MT_Accent','MT_Metal','MT_Energy','MT_Emission','MT_Detail')
MATRIX = [[0,0,1],[-1,0,0],[0,-1,0]]
PALETTES = (
    ('base','BASIS',None), ('standard','CUBE ESCAPE',('#ECE6DA','#A3A7AD','#2B2E33','#F28C28')),
    ('arktis','ARKTIS',('#F3F6F9','#AEBBCA','#3A4452','#22D3EE')),
    ('nacht','NACHT',('#4A4E57','#2C2F35','#141518','#FF5A36')),
)

def _hex(c): return str(c).upper()
def _null_anchor(source): return {'position_m':None,'model':None,'source':'unavailable','part':None,'null_reason':source}
def _clip_uv(constraints):
    """Intersect the weapon UV rectangle with a*x+b*y <= c half-planes."""
    import numpy as np
    poly=[np.array(p,dtype=float) for p in ((0,0),(1,0),(1,1),(0,1))]
    for a,b,c in constraints:
        result=[]
        for old,new in zip(poly,poly[1:]+poly[:1]):
            d0=a*old[0]+b*old[1]-c; d1=a*new[0]+b*new[1]-c
            if d0<=0: result.append(old)
            if (d0<0<d1) or (d1<0<d0):
                result.append(old+(new-old)*(d0/(d0-d1)))
        poly=result
        if len(poly)<3: return []
    return poly


def _linear_mask_constraints(mask):
    """Expand catalog linear/boolean/periodic masks into convex intersections.

    Each result is one polygon's half-planes in the original global u/v frame.
    Elliptic masks deliberately return None: polygonal or circular substitutes
    would silently alter the design. Unknown catalog kinds fail explicitly too.
    """
    import math
    from itertools import product
    kind=mask['kind']
    if kind in ('all','any'):
        children=[_linear_mask_constraints(child) for child in mask['of']]
        if any(child is None for child in children): return None
        if kind=='any': return [region for child in children for region in child]
        return [sum(combination,[]) for combination in product(*children)]
    if kind=='ellipse_rings': return None
    if kind not in ('u','v','diagonal','sawtooth'):
        raise ValueError(f'Unsupported catalog mask kind: {kind}')
    a,b={'u':(1,0),'v':(0,1),'diagonal':(1,mask.get('k',0)),
         'sawtooth':(mask.get('fu',0),mask.get('fv',0))}[kind]
    low,high=mask.get('lo'),mask.get('hi')
    repeats=[0]
    if kind=='sawtooth':
        values=(0,a,b,a+b)
        repeats=range(math.floor(min(values)),math.floor(max(values))+1)
    result=[]
    for repeat in repeats:
        constraints=[]
        if low is not None: constraints.append((-a,-b,-(repeat+low)))
        if high is not None: constraints.append((a,b,repeat+high))
        result.append(constraints)
    return result


def _canonical_skins(meta, model, ref):
    """Export exact v1 polygons and decorations, naming narrower contract gaps.

    The shader's u/v frame is the *whole weapon* bbox, not each part's bbox.
    Contrast fallbacks are exported only if a single existing slot matches on all
    four palettes. Unsupported colours/finishes stay explicit in notes; they must
    never silently acquire another palette slot or an invented v1 layer type.
    """
    import numpy as np
    from PIL import ImageColor
    from skins import CATALOG, apply_skin, channel_palette, channel_for, _contrast
    from texture_catalog import skin as catalog_skin
    hand=np.asarray(ref['anchors']['Socket_Hand']['model'],dtype=float)
    unit=float(ref['units']['model_unit_m']); matrix=np.asarray(MATRIX,dtype=float)
    convert=lambda points: ((np.asarray(points,dtype=float)-hand) @ matrix.T * unit).round(9).tolist()
    rgb=lambda color: np.asarray(ImageColor.getrgb(color)[:3],dtype=float)
    as_hex=lambda color: '#'+''.join(f'{int(c):02X}' for c in color)
    count_base=len(model); slots=list(CHANNELS)+['SK_Accent1','SK_Accent2']; items=[]
    roles=('primary','medium','dark','accent')
    for skin in CATALOG:
        sid=skin['id']; dressed=apply_skin(model,sid)
        recipe=catalog_skin(sid)
        a1,a2=(recipe['accents'][slot]['color'] for slot in ('SK_Accent1','SK_Accent2'))
        accent_finish={slot:recipe['accents'][slot]['finish'] for slot in ('SK_Accent1','SK_Accent2')}
        # v1 has a single finish per slot. Preserve the principal polished fields;
        # document the paint decals which reuse that colour below.
        for layer in recipe['layers']:
            if layer.get('color') in accent_finish and layer.get('finish') in ('polished_gold','polished_chrome'):
                accent_finish[layer['color']]=layer['finish']
        f1,f2=(accent_finish[slot] for slot in ('SK_Accent1','SK_Accent2'))
        layers=[]; notes=[]; colors={}; palettes={}
        for pid,_,swatches in PALETTES:
            # base describes the main view and skin cards (no palette override).
            palette=None if swatches is None else dict(zip(roles,swatches))
            resolved=channel_palette(dressed,palette)
            if palette is not None: palette.update(resolved)
            palettes[pid]=(palette,resolved)
            values={c:{'color':_hex(resolved[c]),'finish':'paint',
                'source':f'skins.channel_palette; {pid}; {c}'} for c in CHANNELS}
            values['SK_Accent1']={'color':a1,'finish':f1,'source':f'fixed recipe accent: {sid}'}
            values['SK_Accent2']={'color':a2,'finish':f2,'source':f'fixed recipe accent: {sid}'}
            colors[pid]=values
        def matching_slot(by_palette):
            return next((slot for slot in slots if all(np.array_equal(rgb(colors[pid][slot]['color']),value)
                for pid,value in by_palette.items())),None)
        def fixed_slot(color):
            # Prefer the declared accents even if a base palette happens to match.
            if _hex(color)==a1: return 'SK_Accent1'
            if _hex(color)==a2: return 'SK_Accent2'
            return matching_slot({pid:rgb(color) for pid in palettes})
        def contrast_slot(part,requested):
            actual={}
            for pid,(palette,resolved) in palettes.items():
                base=rgb(part.color if palette is None else palette.get(channel_for(part),palette.get(part.role,part.color)))
                actual[pid]=_contrast(requested,base,resolved)
            return matching_slot(actual),actual
        eligible=[(i,p) for i,p in enumerate(dressed[:count_base]) if p.skin_declarations['eligible']]
        # All declarations share the bbox authored by apply_skin, including optics exclusion.
        declaration=dressed[0].skin_declarations
        origin=np.asarray(declaration['origin']); extent=np.maximum(declaration['extent'],1e-12)
        notes.append('Masken: globale apply_skin-Waffenbbox ohne Optik, Katalogkoordinaten u/v analytisch '
            'in handrelative Meter transformiert. Polygonränder entsprechen offenen Shader-Schwellen bis auf '
            'die maßlose Randlinie. Vollständige Quellrezepte über catalog_id in docs/textures/catalog.json.')
        for layer_index,source_layer in enumerate(recipe['layers']):
            name=f"catalog.layers[{layer_index}]"
            if source_layer['type']=='blend':
                notes.append(f'Nicht exportiert ({name}): kontinuierlicher Katalogverlauf '
                    +json.dumps(source_layer,ensure_ascii=False,separators=(',',':'))
                    +'; v1 gradient.steps ist gestuft und besitzt keine Teil-Basisfarbe als Slot. '
                    'Formatfrage: Wie werden kontinuierliche Teil-Basisfarbverläufe mit begrenzter Mischung angegeben?')
                continue
            if source_layer['type']!='region':
                raise ValueError(f"Unsupported Codex catalog layer: {source_layer['type']}")
            regions=_linear_mask_constraints(source_layer['mask'])
            if regions is None:
                notes.append(f'Nicht exportiert ({name}): elliptische Katalogringe '
                    +json.dumps(source_layer['mask'],separators=(',',':'))
                    +'; v1 rings sind Kreisringe. Formatfrage: Wie werden metrische Ellipsenradien/-achsen angegeben?')
                continue
            requested=source_layer['color']; groups={}; missing={}
            for index,part in eligible:
                if requested.startswith('SK_'): slot=requested
                else:
                    slot,actual=contrast_slot(part,requested)
                    if slot is None:
                        key=tuple((pid,as_hex(value)) for pid,value in actual.items())
                        missing.setdefault(key,[]).append(f'p{index:03d}')
                        continue
                groups.setdefault(slot,[]).append(f'p{index:03d}')
            for constraints in regions:
                poly=_clip_uv(constraints)
                if not poly: continue
                source_points=[[origin[0]+p[0]*extent[0],origin[1]+p[1]*extent[1],origin[2]] for p in poly]
                poly_yz=np.asarray(convert(source_points))[:,1:].tolist()
                for slot,part_ids in groups.items():
                    layers.append({'type':'side_block','block':source_layer['block'],
                        'parts':part_ids,'slot':slot,'poly_yz_m':poly_yz})
            for actual,part_ids in missing.items():
                notes.append(f'Nicht exportierte Kontrastfarbe ({name}; {requested}), Teile {",".join(part_ids)}: '
                    +', '.join(f'{pid}={color}' for pid,color in actual)
                    +'. Kein einzelner der neun Slots trifft alle vier Paletten; diese Maske fehlt nur auf diesen Teilen. '
                    'Formatfrage: Wie sollen part- und palettenabhängige Ersatzfarben ohne zusätzliche Slots angegeben werden?')
            if source_layer.get('material')=='brushed':
                notes.append(f'Material-Lücke ({name}): Katalog material=brushed ist eine regionale Material-ID; '
                    'v1 side_block besitzt keine Materialzuordnung je Teilfläche. Farbe, paint-Finish und Geometrie '
                    'sind exakt; brushed bleibt über catalog_id auflösbar. '
                    'Formatfrage: Wie wird gebürstetes Material auf einer maskierten Teilfläche ausgedrückt?')
        for host_i,host in enumerate(dressed[:count_base]):
            decals=[]
            for part in host.decals:
                if not getattr(part,'skin_trim',False): continue
                slot=fixed_slot(part.color)
                if slot is None:
                    notes.append(f'Nicht exportierte feste Badge-Farbe {_hex(part.color)} auf p{host_i:03d}; '
                        'kein palettenunabhängiger vorhandener Slot. Originalpolygon points_m='
                        +json.dumps(convert(part.faces[0].vertices),separators=(',',':'))
                        +'. Formatfrage: Wie wird eine dritte feste Skinfarbe angegeben?')
                    continue
                target_normal=matrix @ np.asarray(part.faces[0].normal)
                surface='left' if target_normal[0]>0 else 'right'
                decals.append({'surface':surface,'slot':slot,'points_m':convert(part.faces[0].vertices)})
            if decals:
                layers.append({'type':'glyphs','block':'glyphen','part':f'p{host_i:03d}',
                    'slots':sorted({d['slot'] for d in decals}),'decals':decals})
        trims={}
        for part in dressed[count_base:]:
            if not getattr(part,'skin_trim',False) or part.skin_kind not in ('rib','fin'): continue
            host=f'p{int(part.skin_host):03d}'; kind='fins' if part.skin_kind=='fin' else 'ribs'
            cap=max(part.faces,key=lambda face:len(face.vertices)); target=np.asarray(convert(part.vertices))
            trims.setdefault((host,kind),[]).append({'profile_yz_m':np.asarray(convert(cap.vertices))[:,1:].tolist(),
                'x_m':[float(target[:,0].min()),float(target[:,0].max())],
                'bounds_m':[target.min(axis=0).tolist(),target.max(axis=0).tolist()]})
        for (host,kind),trim_parts in trims.items():
            layers.append({'type':'trim','block':'schmuck','kind':kind,'slot':'SK_Accent1',
                'attach':host,'count':len(trim_parts),'parts':trim_parts})
        if any(value!='paint' for value in accent_finish.values()):
            notes.append('Finish-Lücke Glyphen: apply_skin setzt Ziffer-/Emblem-Decals auf paint, während '
                'dieselben SK-Akzente für maskierte Flächen und Rippen poliertes Metall tragen. '
                'v1 besitzt keinen Finish-Override je Decal; Geometrie und Farben sind exportiert. '
                'Formatfrage: Wie kann ein Slot mehrere Finishwerte je Lage tragen?')
        if any(layer.get('finish') in ('polished_gold','polished_chrome') for layer in recipe['layers']):
            notes.append('Zeichnungskonvention: raster._finish_surface verwendet die katalogbasierten Glanz-/Wearwerte '
                'nur auf polierten Texeln, mit echten Polygonkantendistanzen und deterministischem Objektraum-Hash. '
                'v1 edge_wear mit ganzen parts und einem coverage/color transportiert diese maskierte, '
                'abgestufte Zeichnungsfunktion nicht exakt; kein falscher Ganzteil-Verschleiß exportiert. '
                'Formatfrage: Wie wird Kantenverschleiß an die polierte Teilflächenmaske gekoppelt?')
        trim_finish=recipe['decor']['trim']['finish']
        if trim_finish!=f1:
            notes.append(f'Finish-Lücke Rippen: Katalogfinish {trim_finish}, SK_Accent1-Finish {f1}; '
                'v1 besitzt keinen Finish-Override je Trim-Lage; Geometrie/Farbe sind exakt.')
        notes.append('base beschreibt Hauptansicht/Skin-Karten ohne Palettenoverride. Das BASIS-Palettenfeld auf dem Blatt '
            'remappt zusätzlich die vier Rollen und kann bei einzelnen Basisfarben abweichen; v1 hat dafür keine zweite base-Variante.')
        if not layers: raise ValueError(f'{meta["slug"]}/{sid}: no representable skin geometry')
        items.append({'id':sid,'catalog_id':sid,'name':skin['name'],'hero':sid=='circuit_bloom',
            'blocks':list(dict.fromkeys(layer['block'] for layer in layers)),
            'description_de':recipe['description']['de'],'description_en':recipe['description']['en'],
            'accents':{'SK_Accent1':colors['base']['SK_Accent1'],'SK_Accent2':colors['base']['SK_Accent2']},
            'slots_used':slots,'colors':colors,'layers':layers,'notes':notes})
    return {'source':'docs/textures/catalog.json; codex/fluxbloom/skins.py sample_surface and apply_skin','catalog_id':'circuit_bloom',
        'hero':'circuit_bloom','catalog':[s['id'] for s in CATALOG],
        'slots':{'channels':list(CHANNELS),'accents':['SK_Accent1','SK_Accent2'],
            'rule':'Seven MT channels use skins.channel_palette; two accents remain fixed. Exact unresolved source colours/finishes are named in item notes.'},
        'finishes':['paint','polished_gold','polished_chrome'],
        'space':'Toolgen frame, metres, Socket_Hand origin; side polygons extruded through X; global weapon bbox UV frame converted analytically.',
        'vocabulary':'cubeescape-design/weapon-spec v1 layer vocabulary',
        'new_pattern_types':{},'items':items}

def make_spec(meta, model, number, record=None):
    """Return a canonical weapon-spec. Uses the independent model-reference geometry routines."""
    # Reuse only the local geometry calculations; output is rebuilt field-by-field in
    # the canonical contract, never mislabeled as an importer-ready design reference.
    from spec import design_spec
    from texture_catalog import material as catalog_material
    from motion_spec import make_moving_parts
    record = dict(record or {})
    record.setdefault('orthographic_views', [])
    record.setdefault('geometry_sha256', 'model-only')
    palette_rows=[]
    for pid,name,colors in PALETTES:
        actual=list(meta['palette'] if colors is None else colors)
        palette_rows.append({'name':name,'colors':actual})
    record['palette_variants']=palette_rows
    ref=design_spec(meta,model,number,record)
    tid,reference_length,element=TOOLGEN[meta['slug']]
    legacy=ref['anchors']; anchors={}
    for key,a in legacy.items():
        anchors[key]={k:a.get(k) for k in ('position_m','model','source','part')}
        if a.get('model') is None: anchors[key]['null_reason']=a.get('null_reason') or 'Model geometry does not define this anchor.'
    parts=[]; byid={}
    for p in ref['parts']:
        chan=p['channel']; data={'id':p['id'],'label':p['label'],'channel':chan,
          'channel_source':'explicit' if str(p['channel_source']).startswith('explicit') else 'role',
          'material':{'paint':'painted','metal':'brushed','rubber':'rubber','plastic':'matte','light':'lit'}.get(p['material'],'matte'),
          'texture':catalog_material(p['material'])['id'],
          'toolgen_material':{'paint':'painted','metal':'brushed','rubber':'rubber','plastic':'painted_matte','light':'energy_glass'}.get(p['material'],'painted_matte'),
          'emissive':bool(p['emit']),'sight':bool(p['sight']),'color':_hex(p['color']),'area_m2':max(0,p['area_m2']),
          'long_axis':('Y','Z','X')[max(range(3),key=lambda axis: max(float(v[axis]) for f in model[len(parts)].faces for v in f.vertices)-min(float(v[axis]) for f in model[len(parts)].faces for v in f.vertices))],
          'bounds_m':p['bounds_m'],'moving':None}
        parts.append(data);byid[data['id']]=data
    palettes=[]
    for row,(pid,name,_) in zip(ref['palette_variants'],PALETTES):
        ch={}
        for c in CHANNELS:
            ent=row['channels'][c]; ch[c]=_hex(ent['color']) if ent['color'] else None
        palettes.append({'id':pid,'name':name,'swatches':[_hex(c) for c in row['swatches']], 'channels':ch,
          'other_colors':{c:[{'color':_hex(x['color']),'area_m2':x['area_m2']} for x in row['channels'][c]['other_colors']] for c in CHANNELS if row['channels'][c]['other_colors']},
          'on_sheet':True,'sight_colors':'extrapoliert'})
    sight=ref['sight']
    win_elements=[]
    for aperture_element in (sight.get('window_geometry') or []):
        if aperture_element.get('type')=='open_aperture':
            # This is the explicit clear frame aperture from optics.py, not a glass pane.
            win_elements.append({'type':'part','decal':None,'part':aperture_element['part'],
              'emissive':bool(model[int(aperture_element['part'][1:])].emit),
              'view_axis_m':aperture_element['view_axis_m'],'center_m':aperture_element['center_m']})
        elif aperture_element.get('type') in ('part','disc') and aperture_element.get('view_axis_m'):
            center=aperture_element.get('center_m')
            if center is None:
                bounds_=aperture_element.get('bounds_m')
                if bounds_: center=[(bounds_[0][i]+bounds_[1][i])/2 for i in range(3)]
            if center is not None:
                win_elements.append({'type':aperture_element['type'],'decal':None,'part':aperture_element['part'],
                  'emissive':bool(model[int(aperture_element['part'][1:])].emit),
                  'view_axis_m':aperture_element['view_axis_m'],'center_m':center})
    # Codex optic models use open frame clearances/tubes; none supplies a physical glass surface.
    window_kind='open' if win_elements else sight['window']
    wg={'elements':win_elements,'source':'Explicit open clear apertures from codex/fluxbloom/optics.py; no physical glass surface.'} if win_elements else None
    wg_note=None if wg else 'No functional aperture is declared by this model.'
    sight_out={'present':sight['present'],'kind':sight['kind'],'type':sight['type'],'type_source':sight['type_source'],
      'frame':sight['frame'],'frame_source':sight['frame_source'],'window':window_kind,
      'source':'explicit: optics.py sight frame/aperture geometry','modular':True,'mount_side':sight['mount_side'],
      'labels':sight['labels'],'parts':sight['parts'],'bounds_m':sight['bounds_m'],'anchor':anchors['Socket_Sight'],
      'window_geometry':wg,'window_geometry_note':wg_note}
    robot=ref['robot_fit']; reason=robot['reason'] or 'Konzeptblatt geprüft keine reale Roboterhand, Gelenke, Kollision oder Griffpose.'
    target=robot.get('targets')
    old_at=robot.get('sheet_at_target')
    at_target=None
    if old_at:
        measured=old_at.get('measurements',{})
        at_target={'scale':old_at['scale'],
          'support_forward_m':measured.get('support_forward_m',{}).get('value'),
          'stock_behind_m':measured.get('stock_behind_m',{}).get('value',0.0),
          'barrel_m':measured.get('barrel_m',{}).get('value'),
          'receiver_height_m':measured.get('receiver_height_m',{}).get('value'),
          'basis':'Codex-Modell auf CE-Ziellänge skaliert; Hüllmaße, keine Hand-, Gelenk- oder Kollisionsprüfung.',
          'ok':{key:measured.get(key,{}).get('ok') for key in ('support_forward_m','stock_behind_m','barrel_m','receiver_height_m')}}
    rfit={'source':robot['source'],'robot':robot['robot'],'concept_sheets':False,'applies':robot['applies'],'reason':reason,
      'targets':target,'sheet_at_target':at_target,'actual':robot.get('actual'),
      'validation_note':'Maßwerte stammen aus Modell-Hüllmaßen; Eignung für Toolgen/CE-Roboter ist nicht geprüft.'}
    moving=make_moving_parts(meta,model)
    for item in moving['items']:
        for part_id in item['parts'] or []:
            byid[part_id]['moving']=item['kind']
    return {'format':FORMAT,'format_version':VERSION,
      'generator':{'repo':'cubeescape-design','tool':'codex/fluxbloom/weapon_spec.py','claude_version':None,'codex_version':'0.2.2' if meta['variant']=='K' else '0.1.2'},
      'sheet':{'id':f"K{meta['variant']}{number:02d}",'file':f"K{meta['variant']}{number:02d}.html",'variant':meta['variant'],'variant_name':meta['variant_name'],'number':f'{number:02d}','nick':meta['name'],'fid':meta['slug']},
      'weapon':{'name_de':meta['kind'],'toolgen_id':tid},'element':element,
      'element_source':'Nutzerentscheidung 17.10.2026; Elementzuordnung aus cubeescape-design/weapon-spec.md' if element else 'Bogen: Element nicht festgelegt.',
      'units':{'model_unit_m':ref['units']['model_unit_m'],'model_length_units':reference_length/ref['units']['model_unit_m'],'reference_length_m':reference_length,
        'rule':ref['units']['rule'],'reference':ref['units']['source']},
      'axes':{'model':{'x':'vorn (Mündung)','y':'unten','z':'links'},'target':{'system':'Toolgen/Blender','forward':'-Y','up':'+Z','left':'+X','unit':'m'},'matrix_model_to_target':MATRIX,'origin':'Socket_Hand','formula':'p_m = model_unit_m · M · (p_model − Socket_Hand.model)'},
      'dimensions_m':ref['dimensions_m'],'anchors':anchors,'palette':palettes,
      'channels_used':sorted({p['channel'] for p in parts}),'parts':parts,'moving_parts':moving,'robot_fit':rfit,
      'sight':sight_out,'decals':[],'textures':{'source':'docs/textures/catalog.json via texture_catalog.py; raster.py preview appearance, not UV/PBR bake','vocabulary':'Shared texture-catalog v1 material/pattern IDs; parts[].texture resolves the full parameter record',
        'painted':{'toolgen_pattern':None,'look':'subtle object-space color variation'},'brushed':{'toolgen_pattern':'brushed','direction':'long_axis'},'rubber':{'toolgen_pattern':'knurl','direction':'surface plane'},'matte':{'toolgen_pattern':'grain'},'lit':{'toolgen_pattern':None,'look':'emissive light'}},
      'skin':_canonical_skins(meta,model,ref),'summary':{'parts':len(parts),'parts_explicit_channel':sum(p['channel_source']=='explicit' for p in parts),'decals':0,'channels_with_other_colors':{p['id']:list(p['other_colors']) for p in palettes if p['other_colors']}}}

def dump(spec): return json.dumps(spec,ensure_ascii=False,indent=2,allow_nan=False)+'\n'

def schema_path(): return Path(__file__).with_name('weapon-spec.schema.json')
