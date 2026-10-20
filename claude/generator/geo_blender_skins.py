"""Ein Blatt in allen Farbvarianten und Skins als Blender-Szene (claude-0.13 Nachtrag, Wunsch des Nutzers 20.10.2026: „KG02 in alle
Farbvarianten in Blender, mit allen Texturen, wie auf dem Bild“). Nur Sichtprüfung; Toolgen baut seine Waffen selbst aus dem Geo-Spec.

Wie das Blatt: obere Reihe die vier Farbvarianten (Basis, Cube Escape Standard, Arktis, Nacht) mit dem Hauptskin, untere Reihe die übrigen
Skins des Blatts (Skin 2/5 … 5/5) in der Basis-Farbe. Je Modell: Netze und Aufkleber des Geo-Specs, Teilfarben wie die Farbvarianten des
Blatts (xlroles.recolor), Katalog-Muster und Kantenabnutzung (geo_textures.py) und die Skin-Lagen des Weapon-Specs (`skin.items[].layers`,
Objektraum in m, gleiche Formeln wie skinraster.py): finish, side_block, bands, gradient, rings je Bildpunkt im Shader, glyphs als
Aufkleber, trim als Prismen, edge_wear als Kantenabnutzung. Finishes: paint, polished_chrome, polished_gold (metallisch), neon (leuchtend).

1. Farben vorbereiten (System-Python, braucht die Blatt-Modelle):
   python3 claude/generator/geo_blender_skins.py prepare KG02 <Ordner>        -> <Ordner>/KG02.variants.json
2. Szene bauen (Blender-MCP: Datei mit exec laden und build(...) aufrufen; oder Kommandozeile) und rendern (Bildstufe, heavy_lock):
   blender -b --factory-startup --python claude/generator/geo_blender_skins.py -- claude/output/sheets/KG02.geo.json <Ordner> [--render]
   Ausgabe: <Ordner>/KG02_varianten.blend, mit --render KG02_varianten.png (Übersicht) und KG02_<variante>_<skin>_iso.png je Modell.
   Speichern nur über die Kommandozeile (wm.save_as_mainfile): bpy.data.libraries.write mit einer neuen Szene ließ die Blender-Oberfläche
   (5.2.2, über MCP) am 20.10.2026 abstürzen (BKE_view_layer_copy_data).
"""
import json,math,os,sys

HERE=os.path.dirname(os.path.abspath(__file__))
VARIANTS=(('base','Basis'),('standard','Cube Escape Standard'),('arktis','Arktis'),('nacht','Nacht'))
SHEET_NAMES={'standard':'CUBE ESCAPE STANDARD','arktis':'ARKTIS','nacht':'NACHT'}

def prepare(sid,outdir):
    """Teil- und Aufkleberfarben je Farbvariante wie das Blatt (System-Python)"""
    sys.path.insert(0,HERE)
    import sheetmodels,xlroles
    from eng import split_sight
    full=sheetmodels.load(sid)['m'];gun,_=split_sight(full)
    out={}
    for vk,_ in VARIANTS:
        m2=full if vk=='base' else xlroles.recolor(full,dict(xlroles.VARIANTS)[SHEET_NAMES[vk]],role=xlroles.color_roles(gun))
        out[vk]=dict(parts={f'p{i:02d}':P['col'] for i,P in enumerate(m2.parts)},decals=[dc[3] for P in m2.parts for dc in P['dec']])
    os.makedirs(outdir,exist_ok=True);fn=os.path.join(outdir,f'{sid}.variants.json')
    with open(fn,'w',encoding='utf-8') as f:json.dump(out,f,indent=1)
    return fn

# ---------------------------------------------------------------- Blender
FINISH={'paint':(0.0,None,0.0),'polished_chrome':(1.0,0.12,0.0),'polished_gold':(1.0,0.2,0.0),'neon':(0.0,0.3,5.0)}   # Metall, Rauheit, Leuchten (Schätzung)
# Raster der Modelle: Spalten entlang +Y (von links gesehen nach rechts, wie das Blatt), Reihen nach unten; Abstände aus der Hülle der Waffe

def hexlin(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]

def _inpoly(t,Y,Z,poly):
    """gerade/ungerade Regel wie skinraster._inpoly, Punkte [Y, Z] in m, Y/Z-Ausgänge in mm"""
    cnt=0.0
    for i in range(len(poly)):
        (y0,z0),(y1,z1)=[(a*1000,b*1000) for a,b in (poly[i],poly[i-1])]
        if z0==z1:continue
        neq=t.math('ABSOLUTE',t.math('SUBTRACT',t.math('LESS_THAN',Z,z0),t.math('LESS_THAN',Z,z1)))
        xi=t.math('ADD',t.math('MULTIPLY',t.math('SUBTRACT',Z,z0),(y1-y0)/(z1-z0)),y0)
        cnt=t.math('ADD',cnt,t.math('MULTIPLY',neq,t.math('LESS_THAN',Y,xi)))
    return t.math('FLOORED_MODULO',cnt,2.0)

def _eq(t,a,j):return t.math('LESS_THAN',t.math('ABSOLUTE',t.math('SUBTRACT',a,float(j))),0.5)

def skin_hook(layers,slotcol):
    """Shader-Haken für geo_textures.build: Skin-Lagen eines Teils (Reihenfolge des Specs, spätere überdecken frühere)"""
    def hook(t,X,Y,Z,color_lin,rough,metal):
        st=dict(col=None,met=metal,rgh=rough,emi=0.0)
        def lerp(a,b,m):return t.math('ADD',a,t.math('MULTIPLY',m,t.math('SUBTRACT',b,a)))
        def blend(mask,slot):
            c,fin=slotcol(slot);fm,fr,fe=FINISH.get(fin,FINISH['paint'])
            mx=t.node('ShaderNodeMix',data_type='RGBA');t.l.new(mask,mx.inputs[0])
            if st['col'] is None:mx.inputs[6].default_value=(*color_lin,1.0)
            else:t.l.new(st['col'],mx.inputs[6])
            mx.inputs[7].default_value=(*hexlin(c),1.0);st['col']=mx.outputs[2]
            st['met']=lerp(st['met'],fm,mask);st['rgh']=lerp(st['rgh'],rough if fr is None else fr,mask);st['emi']=lerp(st['emi'],fe,mask)
        def dot(d):return t.add(t.math('MULTIPLY',X,d[0]),t.math('MULTIPLY',Y,d[1]),t.math('MULTIPLY',Z,d[2]))
        for L in layers:
            ty=L['type']
            if ty=='finish':blend(t.math('ADD',0.0,1.0),L['slot'])   # ganzes Teil (Maske als Ausgang, weil Mix verbunden wird)
            elif ty=='side_block':blend(_inpoly(t,Y,Z,L['poly_yz_m']),L['slot'])
            elif ty=='bands':
                tt=t.math('SUBTRACT',dot(L['dir']),L['t0_m']*1000);per=(L['period_m'] or L['width_m'])*1000
                k=t.math('FLOOR',t.math('DIVIDE',tt,per))
                inb=t.math('MULTIPLY',t.math('GREATER_THAN',tt,-1e-6),t.math('LESS_THAN',t.math('SUBTRACT',tt,t.math('MULTIPLY',k,per)),L['width_m']*1000))
                inb=t.math('MULTIPLY',inb,t.math('LESS_THAN',k,L['count']-0.5))
                if L.get('window_yz_m'):inb=t.math('MULTIPLY',inb,_inpoly(t,Y,Z,L['window_yz_m']))
                ns=len(L['slots'])
                for j,sl in enumerate(L['slots']):blend(inb if ns==1 else t.math('MULTIPLY',inb,_eq(t,t.math('FLOORED_MODULO',k,ns),j)),sl)
            elif ty=='gradient':
                s_=t.math('MINIMUM',t.math('MAXIMUM',t.math('DIVIDE',t.math('SUBTRACT',dot(L['dir']),L['t0_m']*1000),(L['t1_m']-L['t0_m'])*1000),0.0),0.9999)
                stp=t.math('FLOOR',t.math('MULTIPLY',s_,L['steps']));ca,_=slotcol(L['slots'][0]);cb,_=slotcol(L['slots'][1])
                for j in range(L['steps']):
                    f=j/max(1,L['steps']-1);c=[a+(b-a)*f for a,b in zip(hexlin(ca),hexlin(cb))]
                    mx=t.node('ShaderNodeMix',data_type='RGBA');t.l.new(_eq(t,stp,j),mx.inputs[0])
                    if st['col'] is None:mx.inputs[6].default_value=(*color_lin,1.0)
                    else:t.l.new(st['col'],mx.inputs[6])
                    mx.inputs[7].default_value=(*c,1.0);st['col']=mx.outputs[2]
            elif ty=='rings':
                cy,cz=[v*1000 for v in L['center_yz_m']]
                r=t.math('SUBTRACT',t.math('SQRT',t.add(t.math('POWER',t.math('SUBTRACT',Y,cy),2.0),t.math('POWER',t.math('SUBTRACT',Z,cz),2.0))),L['r0_m']*1000)
                per=(L['width_m']+L['gap_m'])*1000;k=t.math('FLOOR',t.math('DIVIDE',r,per))
                inr=t.math('MULTIPLY',t.math('GREATER_THAN',r,-1e-6),t.math('LESS_THAN',t.math('SUBTRACT',r,t.math('MULTIPLY',k,per)),L['width_m']*1000))
                inr=t.math('MULTIPLY',inr,t.math('LESS_THAN',k,L['count']-0.5));ns=len(L['slots'])
                for j,sl in enumerate(L['slots']):blend(t.math('MULTIPLY',inr,_eq(t,t.math('FLOORED_MODULO',k,ns),j)),sl)
        if st['col'] is None:return None
        return dict(color=st['col'],metallic=st['met'],roughness=st['rgh'],emission=st['emi'])
    return hook

def cleanup(scene_name,prefix):
    """eigene Szene samt Objekten, Netzen, Kurven, Sammlungen und Materialien (Präfix) entfernen; andere Szenen bleiben unberührt"""
    import bpy
    sc=bpy.data.scenes.get(scene_name);n=0
    if sc:
        colls=[c for c in sc.collection.children_recursive]
        obs=set(sc.collection.all_objects)
        datas=[(o.type,o.data.name) for o in obs if o.data is not None]
        for o in obs:bpy.data.objects.remove(o,do_unlink=True);n+=1
        by_type={'MESH':bpy.data.meshes,'FONT':bpy.data.curves,'CAMERA':bpy.data.cameras,'LIGHT':bpy.data.lights}
        for ty,nm in datas:
            coll=by_type.get(ty)
            if coll is not None and nm in coll and coll[nm].users==0:coll.remove(coll[nm])
        for c in colls:bpy.data.collections.remove(c)
        bpy.data.scenes.remove(sc)
    for coll in (bpy.data.materials,bpy.data.worlds):
        for nm in [x.name for x in coll if x.name.startswith(prefix) and x.users==0]:coll.remove(coll[nm])
    return n

def build(geo_fn,variants_fn,scene_name=None):
    import bpy
    sys.path.insert(0,HERE)
    import geo_textures,texcat
    with open(geo_fn,encoding='utf-8') as f:g=json.load(f)
    with open(os.path.join(os.path.dirname(geo_fn),g['source']['weapon_spec']['file']),encoding='utf-8') as f:spec=json.load(f)
    with open(variants_fn,encoding='utf-8') as f:vcols=json.load(f)
    sid=g['sheet']['id'];scene_name=scene_name or f'{sid}_Varianten'
    if scene_name in bpy.data.scenes:raise RuntimeError(f'Szene {scene_name} gibt es schon')
    sc=bpy.data.scenes.new(scene_name)
    items=spec['skin']['items'];hero=next(i for i in items if i.get('hero'))
    # Modelle wie das Blatt: Farbvarianten mit Hauptskin, dann die übrigen Skins in Basis
    models=[(vk,vn,hero) for vk,vn in VARIANTS]+[('base','Basis',it) for it in items if not it.get('hero')]
    cellw=texcat.wear_cell_widths()
    mats={}
    def simple(key,hexc,fin='paint',emit=False):
        k=f'{sid}_{key}_{hexc}_{fin}_{emit}'
        if k in mats:return mats[k]
        m=bpy.data.materials.new(k);m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF'];lin=hexlin(hexc)
        fm,fr,fe=FINISH.get(fin,FINISH['paint']);b.inputs['Base Color'].default_value=(*lin,1);b.inputs['Metallic'].default_value=fm
        b.inputs['Roughness'].default_value=0.45 if fr is None else fr
        if emit or fe:b.inputs['Emission Color'].default_value=(*lin,1);b.inputs['Emission Strength'].default_value=fe or 4.0
        m.diffuse_color=(*lin,1);mats[k]=m;return m
    def mesh_obj(name,verts,faces,coll,root,mat,hard=None):
        me=bpy.data.meshes.new(name);me.from_pydata([tuple(v) for v in verts],[],[tuple(f) for f in faces]);me.validate(clean_customdata=False);me.update()
        for i,poly in enumerate(me.polygons):poly.use_smooth=not (hard[i] if hard else 1)
        ob=bpy.data.objects.new(name,me);coll.objects.link(ob);ob.parent=root;ob.data.materials.append(mat);return ob
    pts=[v for p in g['parts'] for v in p['mesh']['vertices']]
    lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
    L,H=hi[1]-lo[1],hi[2]-lo[2];size=max(L,H);lab=0.04*max(0.6,size/0.95)   # Schriftgröße mit der Waffe
    gap_y=L+max(0.15,0.17*size);gap_z=H+3.5*lab+0.06
    placed=[]
    for n,(vk,vn,it) in enumerate(models):
        row,colm=divmod(n,4);tag=f'{vk}_{it["id"]}'
        coll=bpy.data.collections.new(f'{sid}_{vn.replace(" ","")}_{it["name"].replace(" ","")}');sc.collection.children.link(coll)
        root=bpy.data.objects.new(f'{sid}_{tag}',None);root.location=(0,colm*gap_y,-row*gap_z);coll.objects.link(root)
        root['variant']=vk;root['skin']=it['id'];root['bounds_lo']=lo;root['bounds_hi']=hi
        pc=vcols[vk]['parts'];skc=it['colors'][vk]
        def slotcol(slot,pc=pc,skc=skc):
            if slot in skc:return skc[slot]['color'],skc[slot]['finish']
            if slot in it['accents']:return it['accents'][slot]['color'],it['accents'][slot]['finish']
            ch=next(p for p in spec['palette'] if p['id']==vk)['channels'].get(slot)
            return ch or '#FF00FF','paint'
        wear={};lay={}
        for L in it['layers']:
            for pid in (L.get('parts') if isinstance(L.get('parts'),list) and L['parts'] and isinstance(L['parts'][0],str) else []):
                if L['type']=='edge_wear':
                    w=L['width_mm']/1000;wear[pid]=(dict(width_m=w,cell_m=w*cellw,coverage=L['coverage']),hexlin(L['color']))
                elif L['type'] in ('finish','side_block','bands','gradient','rings'):lay.setdefault(pid,[]).append(L)
        for p in g['parts']:
            col=p['color'] if p['glass'] else pc[p['id']]
            b=p['bounds_m'];ext=[b[1][i]-b[0][i] for i in range(3)]
            wr,bare=wear.get(p['id'],(None,None))
            m=geo_textures.build(f'{sid}_{tag}_{p["id"]}',hexlin(col),p['texture'],long_axis='XYZ'[ext.index(max(ext))],emissive=p['emissive'],
                                 glass=p['glass'],wear=wr,bare_lin=bare,skin=skin_hook(lay[p['id']],slotcol) if p['id'] in lay else None)
            mesh_obj(f"{p['name']}_{tag}",p['mesh']['vertices'],p['mesh']['faces'],coll,root,m,p['mesh']['hard'])
        for k,dc in enumerate(g['decals']):
            nn=dc['normal'];vs=[[v[i]+nn[i]*0.0005 for i in range(3)] for v in dc['polygon_m']]
            mesh_obj(f'Decal_{k:03d}_{tag}',vs,[range(len(vs))],coll,root,simple('dec',vcols[vk]['decals'][k],emit=dc['emissive']))
        for L in it['layers']:
            if L['type']=='glyphs':
                for k,dc in enumerate(L['decals']):
                    s=1 if dc['surface']=='left' else -1;vs=[[v[0]+s*0.0008,v[1],v[2]] for v in dc['points_m']]
                    c,fin=slotcol(dc['slot']);mesh_obj(f'Glyph_{k:03d}_{tag}',vs,[range(len(vs))],coll,root,simple('glyph',c,fin))
            elif L['type']=='trim':
                c,fin=slotcol(L['slot'])
                for k,tp in enumerate(L['parts']):
                    pr=tp['profile_yz_m'];x0,x1=tp['x_m'];n_=len(pr)
                    vs=[[x0,y,z] for y,z in pr]+[[x1,y,z] for y,z in pr]
                    fs=[list(range(n_))[::-1],list(range(n_,2*n_))]+[[i,(i+1)%n_,(i+1)%n_+n_,i+n_] for i in range(n_)]
                    mesh_obj(f'Trim_{L["kind"]}_{k:02d}_{tag}',vs,fs,coll,root,simple('trim',c,fin))
        cu=bpy.data.curves.new(f'{sid}_Label_{tag}','FONT');cu.body=f'{vn} · {it["name"]}';cu.size=lab;cu.align_x='CENTER'
        lb=bpy.data.objects.new(cu.name,cu);coll.objects.link(lb);lb.parent=root;lb.location=(hi[0]+0.01,(lo[1]+hi[1])/2,lo[2]-2.0*lab);lb.rotation_euler=(math.radians(90),0,math.radians(90))
        lb.data.materials.append(simple('label','#E6EAF0',emit=True))
        placed.append((root,tag))
    # Licht: Kamera sieht dunklen Grund, Spiegelungen sehen hellen Himmel (Chrom/Gold)
    w=bpy.data.worlds.new(f'{sid}_World');w.use_nodes=True;nt=w.node_tree
    for nd in list(nt.nodes):nt.nodes.remove(nd)
    o=nt.nodes.new('ShaderNodeOutputWorld');lp=nt.nodes.new('ShaderNodeLightPath');mx=nt.nodes.new('ShaderNodeMixShader')
    b1=nt.nodes.new('ShaderNodeBackground');b1.inputs[0].default_value=(0.55,0.6,0.68,1);b1.inputs[1].default_value=0.8
    b2=nt.nodes.new('ShaderNodeBackground');b2.inputs[0].default_value=(0.05,0.065,0.09,1)
    nt.links.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);nt.links.new(b1.outputs[0],mx.inputs[1]);nt.links.new(b2.outputs[0],mx.inputs[2]);nt.links.new(mx.outputs[0],o.inputs[0])
    sc.world=w
    for nm,rot,en,sz in (('key',(math.radians(55),0,math.radians(35)),3.5,2.0),('fill',(math.radians(70),0,math.radians(-140)),1.2,3.0),('top',(0,0,0),1.0,3.0)):
        ld=bpy.data.lights.new(f'{sid}_{nm}','SUN');ld.energy=en;ld.angle=math.radians(sz);lo=bpy.data.objects.new(ld.name,ld);lo.rotation_euler=rot;sc.collection.objects.link(lo)
    cd=bpy.data.cameras.new(f'{sid}_Cam');cd.type='ORTHO';cam=bpy.data.objects.new(cd.name,cd);sc.collection.objects.link(cam);sc.camera=cam
    sc.render.engine='CYCLES';sc.cycles.samples=64;sc.cycles.use_denoising=True;sc.view_settings.view_transform='Standard'
    sc['models']=[t for _,t in placed]
    return sc

def render(sc,outdir):
    """Übersicht (Seite links, leicht von oben) und je Modell eine Isometrie von links vorn"""
    import bpy
    from mathutils import Vector
    cam=sc.camera;cd=cam.data;sid=sc.name.split('_')[0]
    def aim(center,direction,scale,rx,ry,fn):
        d=Vector(direction).normalized();cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.location=Vector(center)+d*4
        cd.ortho_scale=scale;sc.render.resolution_x=rx;sc.render.resolution_y=ry
        sc.render.filepath=os.path.join(outdir,fn);bpy.ops.render.render(write_still=True,scene=sc.name)
    roots=[o for o in sc.objects if o.type=='EMPTY' and 'variant' in o]
    def frame(points,direction,rx,ry,fn,margin=1.08):
        """Kamera aus Richtung direction; Ausschnitt aus der Projektion aller Punkte auf die Bildachsen (wie geo_blender.shoot)"""
        d=Vector(direction).normalized();rot=(-d).to_track_quat('-Z','Y');R=rot.to_matrix();right,up=R.col[0],R.col[1]
        xs=[Vector(p).dot(right) for p in points];ys=[Vector(p).dot(up) for p in points]
        cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2;w,h=max(xs)-min(xs),max(ys)-min(ys)
        c=sum((Vector(p) for p in points),Vector())/len(points)
        aim(right*cx+up*cy+d*d.dot(c),direction,max(w,h*rx/ry)*margin if rx>=ry else max(h,w*ry/rx)*margin,rx,ry,fn)
    def corners(r,label=False):
        lo,hi=list(r['bounds_lo']),list(r['bounds_hi'])
        if label:lab=[o for o in r.children if '_Label_' in o.name][0];lo[2]=min(lo[2],lab.location[2]-lab.data.size)   # Ortsangaben relativ zum Wurzelobjekt
        return [r.location+Vector((x,y,z)) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]
    allc=[p for r in roots for p in corners(r,True)]
    d0=Vector((1,0,0.18)).normalized();R=(-d0).to_track_quat('-Z','Y').to_matrix()
    W=max(p.dot(R.col[0]) for p in allc)-min(p.dot(R.col[0]) for p in allc);Hh=max(p.dot(R.col[1]) for p in allc)-min(p.dot(R.col[1]) for p in allc)
    ry=int(min(4000,max(600,3200*Hh/W*1.04)))
    frame(allc,(1,0,0.18),3200,ry,f'{sid}_varianten.png',1.06)
    colls={r.name:r.users_collection[0] for r in roots}
    for r in roots:   # Einzelbild: nur dieses Modell, ohne Beschriftung
        for nm,c in colls.items():c.hide_render=nm!=r.name
        for o in colls[r.name].objects:o.hide_render='_Label_' in o.name
        frame(corners(r),(1,0.9,0.75),1280,720,f"{sid}_{r['variant']}_{r['skin']}_iso.png")
    for c in colls.values():
        c.hide_render=False
        for o in c.objects:o.hide_render=False

if __name__=='__main__':
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    if argv and argv[0]=='prepare':print(prepare(argv[1],argv[2]));sys.exit(0)
    geo,out=argv[0],argv[1];sid=os.path.basename(geo).split('.')[0]
    import bpy
    old=list(bpy.data.scenes)
    sc=build(geo,os.path.join(out,f'{sid}.variants.json'))
    for s in old:
        for o in list(s.collection.all_objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.scenes.remove(s)
    for w in bpy.context.window_manager.windows:w.scene=sc
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,f'{sid}_varianten.blend'),compress=True)
    if '--render' in argv:render(sc,out)
    print('GEO_SKINS_OK',sid,len(sc['models']),'Modelle',out)
