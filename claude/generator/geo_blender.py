"""Sichtprüfung eines Geo-Specs in Blender (claude-0.13, Pilot DS-1): importiert KXnn.geo.json (ein Objekt je Teil, Farbe je Kanal aus der
Basis-Palette des Weapon-Specs, Leuchtteile emittierend, Glas durchscheinend, Aufkleber als flache Polygone 0,5 mm über der Fläche) und rendert
Seite links/rechts und zwei Isometrien (Workbench, orthografisch, fester Bildausschnitt). Nur Bildstufe auf dem Mac (heavy_lock).

   blender -b --factory-startup --python claude/generator/geo_blender.py -- claude/output/sheets/KG02.geo.json <Ausgabeordner> [--anchors]

Ausgabe: <id>_side_left.png, <id>_side_right.png, <id>_iso_left.png, <id>_iso_right.png (1280×720). --anchors: kleine Kugeln an den Ankern.
Seiten im Toolgen-Rahmen: links = +X, vorn = −Y, oben = +Z (die Blattansichten zeichnen beide Seiten mit der Mündung rechts).
"""
import json,math,os,sys
import bpy
from mathutils import Vector

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
GEO,OUTDIR=argv[0],argv[1];ANCHORS='--anchors' in argv
os.makedirs(OUTDIR,exist_ok=True)
with open(GEO,encoding='utf-8') as f:g=json.load(f)
spec_fn=os.path.join(os.path.dirname(GEO),g['source']['weapon_spec']['file'] if g['source']['weapon_spec'] else g['source']['sight_spec']['file'])
with open(spec_fn,encoding='utf-8') as f:spec=json.load(f)
palette=spec['palette'][0]['channels'] if 'palette' in spec else {}
def hexrgb(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]

for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
sc=bpy.context.scene
mats={}
def material(key,col,emit=False,glass=False):
    if key in mats:return mats[key]
    m=bpy.data.materials.new(key);r,gg,b=hexrgb(col);a=0.35 if glass else 1.0
    m.diffuse_color=(r,gg,b,a);m.use_nodes=False
    mats[key]=m;return m
def color_of(p):
    if p['glass']:return p['color']
    return palette.get(p['channel']) or p['color']

objs=[]
for p in g['parts']:
    me=bpy.data.meshes.new(p['name']);me.from_pydata([tuple(v) for v in p['mesh']['vertices']],[],[tuple(f) for f in p['mesh']['faces']])
    me.validate(clean_customdata=False);me.update()
    for poly,h in zip(me.polygons,p['mesh']['hard']):poly.use_smooth=not h
    ob=bpy.data.objects.new(p['name'],me);sc.collection.objects.link(ob)
    ob.data.materials.append(material(f"{p['channel']}_{p['emissive']}_{p['glass']}_{color_of(p)}",color_of(p),p['emissive'],p['glass']))
    objs.append(ob)
for k,dc in enumerate(g['decals']):
    n=Vector(dc['normal']);vs=[tuple(Vector(v)+n*0.0005) for v in dc['polygon_m']]
    me=bpy.data.meshes.new(f'Decal_{k:03d}');me.from_pydata(vs,[],[tuple(range(len(vs)))]);me.update()
    ob=bpy.data.objects.new(me.name,me);sc.collection.objects.link(ob);ob.data.materials.append(material('dec_'+dc['color'],dc['color']))
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
    sc.render.filepath=os.path.join(OUTDIR,f"{g['sheet']['id']}_{name}.png");bpy.ops.render.render(write_still=True)
shoot('side_left',(1,0,0));shoot('side_right',(-1,0,0))
shoot('iso_left',(1,0.9,0.75));shoot('iso_right',(-1,0.9,0.75))
print('GEO_BLENDER_OK',g['sheet']['id'],len(objs),'Teile',len(g['decals']),'Aufkleber',OUTDIR)
