"""Katalog-Muster als Blender-Material (claude-0.13, nur Sichtprüfung über geo_blender.py --textures; Toolgen bakt seine eigenen Karten).

Formeln und Größen aus docs/textures/catalog.json › patterns (mm am echten Objekt, Objektkoordinaten des Geo-Specs in m):
- gloss_gradient (painted): Helligkeit 1 + Σ amplitude · cos(2π · Σ Achsen / wavelength_mm); Achse height = Z, length+width = X − Y.
- brushed: 1 + amplitude · Σ weight · sin(2π · quer / wavelength_mm + phase); quer = Summe der beiden Achsen quer zur Längsachse des Teils.
- knurl (rubber): Zellen floor((u+v)/size) und floor((u−v)/size) beide gerade → Helligkeit −darkening; (u, v) = Flächenebene, je
  Flächenrichtung projiziert (Normale dominiert X, Y oder Z).
- grain (painted_matte): 1 + amplitude · (hash(Zelle) − 0,5), Zellen der Kantenlänge size_mm.
Kantenabnutzung (surface.wear): Bevel-Normale gegen Flächennormale (Cycles), fleckig über Zellen cell_m mit Anteil coverage; nur Lack.
Rauheit/Metall je Material sind Schätzwerte für das Bild (Katalog hat keine), Emission für Leuchtteile.
"""
import json,math,os
import bpy

HERE=os.path.dirname(os.path.abspath(__file__))
CATALOG=os.path.join(os.path.dirname(os.path.dirname(HERE)),'docs','textures','catalog.json')
with open(CATALOG,encoding='utf-8') as f:CAT=json.load(f)
PAT={p['id']:p for p in CAT['patterns']};MAT={m['id']:m for m in CAT['materials']}
LOOK={'painted':(0.38,0.0),'painted_matte':(0.75,0.0),'brushed':(0.32,0.85),'rubber':(0.85,0.0),'energy_glass':(0.2,0.0)}   # Rauheit, Metall (Schätzung)

class T:
    def __init__(s,mat):s.nt=mat.node_tree;s.n=s.nt.nodes;s.l=s.nt.links;s.x=0
    def node(s,kind,**kw):
        nd=s.n.new(kind);s.x+=60;nd.location=(s.x-1600,0)
        for k,v in kw.items():setattr(nd,k,v)
        return nd
    def math(s,op,a,b=None):
        nd=s.node('ShaderNodeMath',operation=op)
        for i,v in enumerate((a,b)[:1 if b is None else 2]):
            if hasattr(v,'bl_idname') or hasattr(v,'is_output'):s.l.new(v if hasattr(v,'is_output') else v.outputs[0],nd.inputs[i])
            else:nd.inputs[i].default_value=v
        return nd.outputs[0]
    def add(s,*xs):
        out=xs[0]
        for x in xs[1:]:out=s.math('ADD',out,x)
        return out

def build(name,color_lin,material_id,long_axis=None,emissive=False,glass=False,wear=None,bare_lin=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;t=T(m)
    for nd in list(t.n):
        if nd.bl_idname!='ShaderNodeOutputMaterial':t.n.remove(nd)
    out=next(nd for nd in t.n if nd.bl_idname=='ShaderNodeOutputMaterial')
    bsdf=t.node('ShaderNodeBsdfPrincipled');rough,metal=LOOK.get(material_id,(0.5,0.0))
    bsdf.inputs['Roughness'].default_value=rough;bsdf.inputs['Metallic'].default_value=metal
    t.l.new(bsdf.outputs[0],out.inputs[0])
    base=(*color_lin,1.0)
    if emissive:
        bsdf.inputs['Base Color'].default_value=base;bsdf.inputs['Emission Color'].default_value=base;bsdf.inputs['Emission Strength'].default_value=4.0
        return m
    if glass:
        bsdf.inputs['Base Color'].default_value=base;bsdf.inputs['Alpha'].default_value=0.35
        try:m.surface_render_method='BLENDED'
        except Exception:pass
        return m
    tc=t.node('ShaderNodeTexCoord');sep=t.node('ShaderNodeSeparateXYZ');t.l.new(tc.outputs['Object'],sep.inputs[0])
    X,Y,Z=[t.math('MULTIPLY',sep.outputs[i],1000.0) for i in range(3)]   # mm
    pid=(MAT.get(material_id) or {}).get('pattern')
    b=None;tau=2*math.pi
    if pid=='gloss_gradient':
        w=PAT[pid]['params']['waves'];terms=[]
        for wv in w:
            ax=Z if wv['axes']==['height'] else t.math('SUBTRACT',X,Y)
            terms.append(t.math('MULTIPLY',t.math('COSINE',t.math('MULTIPLY',ax,tau/wv['wavelength_mm'])),wv['amplitude']))
        b=t.add(1.0,*terms)
    elif pid=='brushed':
        p=PAT[pid]['params'];axes=[X,Y,Z];la='XYZ'.index(long_axis or 'Y')
        q=t.add(*[axes[i] for i in range(3) if i!=la]);terms=[]
        for wv in p['waves']:
            terms.append(t.math('MULTIPLY',t.math('SINE',t.math('ADD',t.math('MULTIPLY',q,tau/wv['wavelength_mm']),wv['phase'])),p['amplitude']*wv['weight']))
        b=t.add(1.0,*terms)
    elif pid=='knurl':
        size=PAT[pid]['size_mm'];dk=PAT[pid]['params']['darkening']
        gn=t.node('ShaderNodeNewGeometry');sn=t.node('ShaderNodeSeparateXYZ');t.l.new(gn.outputs['Normal'],sn.inputs[0])
        ab=[t.math('ABSOLUTE',sn.outputs[i]) for i in range(3)]
        def even(v):return t.math('SUBTRACT',1.0,t.math('FLOORED_MODULO',t.math('FLOOR',t.math('DIVIDE',v,size)),2.0))
        def cell(u,v):return t.math('MULTIPLY',even(t.math('ADD',u,v)),even(t.math('SUBTRACT',u,v)))
        # Gewicht je Projektion: Normale dominiert diese Achse (Gleichstand: erste)
        wx=t.math('MULTIPLY',t.math('GREATER_THAN',ab[0],t.math('SUBTRACT',ab[1],1e-6)),t.math('GREATER_THAN',ab[0],t.math('SUBTRACT',ab[2],1e-6)))
        wy=t.math('MULTIPLY',t.math('SUBTRACT',1.0,wx),t.math('GREATER_THAN',ab[1],t.math('SUBTRACT',ab[2],1e-6)))
        wz=t.math('SUBTRACT',t.math('SUBTRACT',1.0,wx),wy)
        c=t.add(t.math('MULTIPLY',wx,cell(Y,Z)),t.math('MULTIPLY',wy,cell(X,Z)),t.math('MULTIPLY',wz,cell(X,Y)))
        b=t.math('SUBTRACT',1.0,t.math('MULTIPLY',c,dk))
    elif pid=='grain':
        size=PAT[pid]['size_mm'];amp=PAT[pid]['params']['amplitude']
        cmb=t.node('ShaderNodeCombineXYZ')
        for i,v in enumerate((X,Y,Z)):t.l.new(t.math('FLOOR',t.math('DIVIDE',v,size)),cmb.inputs[i])
        wn=t.node('ShaderNodeTexWhiteNoise',noise_dimensions='3D');t.l.new(cmb.outputs[0],wn.inputs['Vector'])
        b=t.math('ADD',1.0,t.math('MULTIPLY',t.math('SUBTRACT',wn.outputs['Value'],0.5),amp))
    if b is None:b=1.0
    sc=t.node('ShaderNodeVectorMath',operation='SCALE');sc.inputs[0].default_value=color_lin
    if isinstance(b,float):sc.inputs['Scale'].default_value=b
    else:t.l.new(b,sc.inputs['Scale'])
    col=sc.outputs[0]
    if wear and material_id in ('painted','painted_matte'):
        # Kantenabnutzung (Katalog wear, Geo-Spec surface.wear): Bevel-Normale weicht an harten Kanten ab; Zellen mit Anteil coverage tragen sie
        bv=t.node('ShaderNodeBevel');bv.inputs['Radius'].default_value=2.5*wear['width_m'];bv.samples=16   # Bevel-Normale weicht nur nahe der Kante merklich ab: 2,5 × Breite ≈ sichtbare Breite width_m
        gn=t.node('ShaderNodeNewGeometry');dt=t.node('ShaderNodeVectorMath',operation='DOT_PRODUCT')
        t.l.new(bv.outputs[0],dt.inputs[0]);t.l.new(gn.outputs['Normal'],dt.inputs[1])
        edge=t.math('GREATER_THAN',t.math('SUBTRACT',1.0,dt.outputs['Value']),0.0005)   # schon kleine Abweichung = innerhalb width_m an der Kante
        cmb=t.node('ShaderNodeCombineXYZ')
        for i,v in enumerate((X,Y,Z)):t.l.new(t.math('FLOOR',t.math('DIVIDE',v,wear['cell_m']*1000)),cmb.inputs[i])
        wn=t.node('ShaderNodeTexWhiteNoise',noise_dimensions='3D');t.l.new(cmb.outputs[0],wn.inputs['Vector'])
        w=t.math('MULTIPLY',edge,t.math('LESS_THAN',wn.outputs['Value'],wear['coverage']))
        mx=t.node('ShaderNodeMix',data_type='RGBA');t.l.new(w,mx.inputs['Factor']);t.l.new(col,mx.inputs[6]);mx.inputs[7].default_value=(*bare_lin,1.0)
        t.l.new(mx.outputs[2],bsdf.inputs['Base Color'])
        mm=t.node('ShaderNodeMapRange');t.l.new(w,mm.inputs['Value']);mm.inputs['To Min'].default_value=metal;mm.inputs['To Max'].default_value=0.9
        t.l.new(mm.outputs[0],bsdf.inputs['Metallic'])
        return m
    t.l.new(col,bsdf.inputs['Base Color'])
    return m
