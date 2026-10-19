"""Sichtprüfung eines Geo-Specs in Blender (claude-0.13, Pilot DS-1): importiert KXnn.geo.json (ein Objekt je Teil, Farbe je Kanal aus der
Basis-Palette des Weapon-Specs, Leuchtteile emittierend, Glas durchscheinend, Aufkleber als flache Polygone 0,5 mm über der Fläche) und rendert
Seite links/rechts und zwei Isometrien (Workbench, orthografisch, fester Bildausschnitt). Nur Bildstufe auf dem Mac (heavy_lock).

   blender -b --factory-startup --python claude/generator/geo_blender.py -- claude/output/sheets/KG02.geo.json <Ausgabeordner> [--anchors]

--palette standard|arktis|nacht: Farbvariante wie auf dem Blatt (xlroles.recolor nach Rollen, ohne Skin; Dateien mit Endung _<variante>).
--textures: Katalog-Muster je Teil und Kantenabnutzung des Waffenprofils (Cycles), zusätzlich Nahansichten Griff/Mündung.
Ausgabe: <id>_side_left.png, <id>_side_right.png, <id>_iso_left.png, <id>_iso_right.png (1280×720). --anchors: kleine Kugeln an den Ankern.
Seiten im Toolgen-Rahmen: links = +X, vorn = −Y, oben = +Z (die Blattansichten zeichnen beide Seiten mit der Mündung rechts).
"""
import json,math,os,sys
import bpy
from mathutils import Vector

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
GEO,OUTDIR=argv[0],argv[1];ANCHORS='--anchors' in argv
PAL=argv[argv.index('--palette')+1] if '--palette' in argv else 'base'
TEX='--textures' in argv   # Katalog-Muster und Kantenabnutzung (geo_textures.py, Cycles), Dateien mit Endung _tex   # Farbvariante des Weapon-Specs: base, standard, arktis, nacht
os.makedirs(OUTDIR,exist_ok=True)
with open(GEO,encoding='utf-8') as f:g=json.load(f)
spec_fn=os.path.join(os.path.dirname(GEO),g['source']['weapon_spec']['file'] if g['source']['weapon_spec'] else g['source']['sight_spec']['file'])
with open(spec_fn,encoding='utf-8') as f:spec=json.load(f)
palette=next((p['channels'] for p in spec.get('palette',[]) if p['id']==PAL),{})
SUFFIX=('' if PAL=='base' else '_'+PAL)+('_tex' if TEX else '')
SHEET_COLORS=None   # Farbvarianten wie das Blatt: xlroles.recolor nach Bauteil-Rollen (xl.sheet › Farbvarianten), ohne Skin
if PAL!='base' and g['sheet']['kind']=='weapon':
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    import sheetmodels,xlroles
    from eng import split_sight
    _d=sheetmodels.load(g['sheet']['id']);_full=_d['m'];_gun,_=split_sight(_full)
    _pal=dict(xlroles.VARIANTS)[{'standard':'CUBE ESCAPE STANDARD','arktis':'ARKTIS','nacht':'NACHT'}[PAL]]
    _m2=xlroles.recolor(_full,_pal,role=xlroles.color_roles(_gun))
    SHEET_COLORS=dict(parts={f'p{i:02d}':P['col'] for i,P in enumerate(_m2.parts)},decals=[dc[3] for P in _m2.parts for dc in P['dec']])
def hexrgb(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]

for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
sc=bpy.context.scene
mats={}
if TEX:
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    import geo_textures
    WEAR=(g.get('surface') or {}).get('wear')
def material_tex(p,col):
    b=p['bounds_m'];ext=[b[1][i]-b[0][i] for i in range(3)];la='XYZ'[ext.index(max(ext))]
    key=f"tex_{p['id']}"
    return geo_textures.build(key,hexrgb(col),p['texture'],long_axis=la,emissive=p['emissive'],glass=p['glass'],wear=WEAR,
                              bare_lin=hexrgb(WEAR['bare_metal']) if WEAR else None)
def material(key,col,emit=False,glass=False):
    if key in mats:return mats[key]
    m=bpy.data.materials.new(key);r,gg,b=hexrgb(col);a=0.35 if glass else 1.0
    m.diffuse_color=(r,gg,b,a);m.use_nodes=bool(TEX)
    if TEX:m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(r,gg,b,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=0.5
    mats[key]=m;return m
def color_of(p):
    if p['glass']:return p['color']
    if SHEET_COLORS:return SHEET_COLORS['parts'][p['id']]
    return palette.get(p['channel']) or p['color']

objs=[]
for p in g['parts']:
    me=bpy.data.meshes.new(p['name']);me.from_pydata([tuple(v) for v in p['mesh']['vertices']],[],[tuple(f) for f in p['mesh']['faces']])
    me.validate(clean_customdata=False);me.update()
    for poly,h in zip(me.polygons,p['mesh']['hard']):poly.use_smooth=not h
    ob=bpy.data.objects.new(p['name'],me);sc.collection.objects.link(ob)
    ob.data.materials.append(material_tex(p,color_of(p)) if TEX else material(f"{p['channel']}_{p['emissive']}_{p['glass']}_{color_of(p)}",color_of(p),p['emissive'],p['glass']))
    objs.append(ob)
for k,dc in enumerate(g['decals']):
    n=Vector(dc['normal']);vs=[tuple(Vector(v)+n*0.0005) for v in dc['polygon_m']]
    me=bpy.data.meshes.new(f'Decal_{k:03d}');me.from_pydata(vs,[],[tuple(range(len(vs)))]);me.update()
    col=SHEET_COLORS['decals'][k] if SHEET_COLORS else dc['color'] if PAL=='base' else (palette.get(dc['channel']) or dc['color'])
    ob=bpy.data.objects.new(me.name,me);sc.collection.objects.link(ob);ob.data.materials.append(material('dec_'+col,col))
if ANCHORS:
    for name,a in g['anchors'].items():
        if not a['position_m']:continue
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.006,location=a['position_m']);s=bpy.context.object;s.name='Anchor_'+name
        s.data.materials.append(material('anchor','#FF00FF'))

# Bildausschnitt aus der Hülle aller Teile
pts=[Vector(v) for p in g['parts'] for v in p['mesh']['vertices']]
lo=Vector([min(v[i] for v in pts) for i in range(3)]);hi=Vector([max(v[i] for v in pts) for i in range(3)]);c=(lo+hi)/2;size=(hi-lo).length
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.film_transparent=False
sh=sc.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_object_outline=True;sh.show_cavity=True;sh.cavity_type='WORLD'
sh.show_specular_highlight=False;sh.background_type='VIEWPORT';sh.background_color=(0.06,0.08,0.11)
sc.display.render_aa='16'
sh.show_xray=False
for m in mats.values():m.blend_method='BLEND' if m.diffuse_color[3]<1 else 'OPAQUE'
if TEX:   # Cycles mit Studiolicht: Muster und Kantenabnutzung (Bevel-Knoten nur in Cycles)
    sc.render.engine='CYCLES';sc.cycles.samples=48;sc.cycles.use_denoising=True;sc.view_settings.view_transform='Standard'
    w=bpy.data.worlds.new('w');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(0.05,0.065,0.09,1);w.node_tree.nodes['Background'].inputs[1].default_value=1.0
    sc.world=w
    for nm,rot,en,sz in (('key',(math.radians(55),0,math.radians(35)),3.5,2.0),('fill',(math.radians(70),0,math.radians(-140)),1.2,3.0),('top',(0,0,0),1.0,3.0)):
        ld=bpy.data.lights.new(nm,'SUN');ld.energy=en;ld.angle=math.radians(sz);lo=bpy.data.objects.new(nm,ld);lo.rotation_euler=rot;sc.collection.objects.link(lo)
cam_data=bpy.data.cameras.new('cam');cam_data.type='ORTHO';cam_data.ortho_scale=size*1.05
cam=bpy.data.objects.new('cam',cam_data);sc.collection.objects.link(cam);sc.camera=cam
ASPECT=sc.render.resolution_x/sc.render.resolution_y
def shoot(name,direction):
    """Kamera aus Richtung direction auf die Mitte; Ausschnitt aus der Projektion aller Ecken auf die Bildachsen, Seitenverhältnis beachtet"""
    d=Vector(direction).normalized();rot=(-d).to_track_quat('-Z','Y');R=rot.to_matrix()
    right,up=R.col[0],R.col[1]
    xs=[p.dot(right) for p in pts];ys=[p.dot(up) for p in pts]
    cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2;w,h=max(xs)-min(xs),max(ys)-min(ys)
    cam_data.ortho_scale=max(w,h*ASPECT)*1.08
    cam.rotation_euler=rot.to_euler();cam.location=right*cx+up*cy+d*(d.dot(c)+size*3)
    sc.render.filepath=os.path.join(OUTDIR,f"{g['sheet']['id']}_{name}{SUFFIX}.png");bpy.ops.render.render(write_still=True)
def detail(name,direction,center,scale):
    d=Vector(direction).normalized();rot=(-d).to_track_quat('-Z','Y');cam.rotation_euler=rot.to_euler();cam_data.ortho_scale=scale
    cam.location=Vector(center)+d*size*3
    sc.render.filepath=os.path.join(OUTDIR,f"{g['sheet']['id']}_{name}{SUFFIX}.png");bpy.ops.render.render(write_still=True)
if TEX:
    for nm,a in (('detail_grip','Socket_Hand'),('detail_muzzle','Socket_Muzzle')):
        if g['anchors'].get(a,{}).get('position_m'):detail(nm,(1,0.9,0.75),g['anchors'][a]['position_m'],0.24)
shoot('side_left',(1,0,0));shoot('side_right',(-1,0,0))
shoot('iso_left',(1,0.9,0.75));shoot('iso_right',(-1,0.9,0.75))
print('GEO_BLENDER_OK',g['sheet']['id'],len(objs),'Teile',len(g['decals']),'Aufkleber',OUTDIR)
