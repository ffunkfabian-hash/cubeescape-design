"""Schema- und Stimmigkeitstest der Spec-Dateien (claude/output/sheets/KXnn.spec.json). Ohne numpy, ohne Bildstufe.
   python3 -m unittest claude/generator/test_spec.py      (oder: python3 claude/generator/test_spec.py)
"""
from cepaths import E3D,CLAUDE,OUT
import copy,json,math,os,re,sys,unittest
sys.path.insert(0,E3D)
import export_spec,sheetmodels,variants
from eng import CHANNELS,Model,rect,channel,copy_channels,split_sight
from xlroles import recolor,VARIANTS,color_roles,assign_channels

def _read(fn):
    with open(fn,encoding='utf-8') as f:return f.read()
SCHEMA=json.loads(_read(os.path.join(CLAUDE,'docs','weapon-spec.schema.json')))
TYPES={'object':dict,'array':list,'string':str,'boolean':bool,'null':type(None)}

def validate(x,s,path='$',root=SCHEMA):
    """Kleine Teilmenge von JSON Schema (siehe description im Schema); liefert Fehlertexte."""
    if '$ref' in s:
        node=root
        for k in s['$ref'][2:].split('/'):node=node[k]
        return validate(x,node,path,root)
    err=[]
    if 'type' in s:
        ts=s['type'] if isinstance(s['type'],list) else [s['type']]
        ok=any((t=='number' and isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)) or
               (t=='integer' and isinstance(x,int) and not isinstance(x,bool)) or
               (t in TYPES and isinstance(x,TYPES[t]) and not (t!='boolean' and isinstance(x,bool))) for t in ts)
        if not ok:return [f'{path}: Typ {type(x).__name__} statt {ts}']
    if 'const' in s and x!=s['const']:err.append(f'{path}: {x!r} != {s["const"]!r}')
    if 'enum' in s and x not in s['enum']:err.append(f'{path}: {x!r} nicht in {s["enum"]}')
    if isinstance(x,str) and 'pattern' in s and not re.search(s['pattern'],x):err.append(f'{path}: {x!r} passt nicht zu {s["pattern"]}')
    if isinstance(x,(int,float)) and not isinstance(x,bool) and 'minimum' in s and x<s['minimum']:err.append(f'{path}: {x} < {s["minimum"]}')
    if isinstance(x,dict):
        for k in s.get('required',[]):
            if k not in x:err.append(f'{path}: {k} fehlt')
        props=s.get('properties',{})
        for k,v in x.items():
            if k in props:err+=validate(v,props[k],f'{path}.{k}',root)
            elif s.get('additionalProperties') is False:err.append(f'{path}: unbekanntes Feld {k}')
    if isinstance(x,list):
        if len(x)<s.get('minItems',0):err.append(f'{path}: weniger als {s["minItems"]} Einträge')
        if 'maxItems' in s and len(x)>s['maxItems']:err.append(f'{path}: mehr als {s["maxItems"]} Einträge')
        if 'items' in s:
            for i,v in enumerate(x):err+=validate(v,s['items'],f'{path}[{i}]',root)
    return err

def load(sheet):return json.loads(_read(export_spec.path(sheet)))

class SpecFiles(unittest.TestCase):
    def test_all_present_and_current(self):
        """10 Dateien je Variante, jede gleich der Ausgabe des Exporters (sonst: python3 claude/generator/export_spec.py)."""
        self.assertEqual(len(sheetmodels.SHEETS),10*len(variants.LETTERS))
        stale=[s for s in sheetmodels.SHEETS if not os.path.exists(export_spec.path(s)) or
               _read(export_spec.path(s))!=export_spec.dumps(export_spec.build(s))]
        self.assertEqual(stale,[],'veraltet oder fehlend – python3 claude/generator/export_spec.py')
        extra=sorted(f for f in os.listdir(OUT) if f.endswith('.spec.json') and f[:-10] not in sheetmodels.SHEETS)
        self.assertEqual(extra,[])

    def test_schema(self):
        for s in sheetmodels.SHEETS:
            with self.subTest(sheet=s):self.assertEqual(validate(load(s),SCHEMA),[])

    def test_consistency(self):
        for s in sheetmodels.SHEETS:
            sp=load(s)
            with self.subTest(sheet=s):
                self.assertEqual(sp['sheet']['id'],s)
                tid,ref,el=export_spec.WEAPONS[sp['weapon']['name_de']]
                self.assertEqual((sp['weapon']['toolgen_id'],sp['element']),(tid,el))
                # Maßstab: Bezugslänge auf 0,5 mm
                d=sp['dimensions_m']['with_sight']
                got=max(d['length'],d['height'],d['width']) if tid=='bow' else d['length']
                self.assertAlmostEqual(got,ref,delta=5e-4)
                self.assertAlmostEqual(sp['units']['model_unit_m']*sp['units']['model_length_units'],ref,delta=5e-4)
                # Anker: Griff ist Ursprung, alle Werte endlich, Mündung vor dem Griff (−Y)
                a=sp['anchors']
                self.assertEqual(a['Socket_Hand']['position_m'],[0.0,0.0,0.0])
                self.assertIsNotNone(a['Socket_Muzzle']['position_m'])
                self.assertLess(a['Socket_Muzzle']['position_m'][1],0)
                for k,v in a.items():
                    if v['position_m'] is None:self.assertIsNone(v['model'])
                # Teile/Aufkleber/Visier verweisen richtig
                ids=[p['id'] for p in sp['parts']]
                self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue({dd['part'] for dd in sp['decals']}<=set(ids))
                self.assertEqual(sorted(sp['sight']['parts']),sorted(p['id'] for p in sp['parts'] if p['sight']))
                self.assertEqual(sp['sight']['present'],bool(sp['sight']['parts']))
                self.assertEqual(sp['sight']['kind'] is None,not sp['sight']['present'])
                # jeder benutzte Kanal hat in jeder Variante eine Farbe, unbenutzte keine
                used={p['channel'] for p in sp['parts']}|{dd['channel'] for dd in sp['decals']}
                self.assertEqual(sorted(used,key=CHANNELS.index),sp['channels_used'])
                for v in sp['palette']:
                    self.assertEqual(list(v['channels']),list(CHANNELS),v['id'])
                    self.assertEqual({c for c,h in v['channels'].items() if h},used,v['id'])
                    self.assertEqual(list(a),['Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight'])
                self.assertEqual([v['id'] for v in sp['palette']],export_spec.VARIANT_IDS)
                self.assertEqual([v['swatches'] for v in sp['palette'][1:]],[[c.upper() for c in p] for _,p in VARIANTS[:3]])
                # leuchtende Teile liegen auf Energie-/Leuchtkanälen, wenn nicht ausdrücklich anders gesetzt
                for p in sp['parts']:
                    if p['emissive'] and p['channel_source']!='explicit':self.assertIn(p['channel'],('MT_Energy','MT_Emission'))

class Channels(unittest.TestCase):
    def _model(self):
        m=Model()
        m.prism(rect(0,0,100,40),'#DDDDDD',-10,10);m.parts[-1]['label']='Gehäuse'
        m.prism(rect(60,40,20,50),'#222222',-8,8);m.parts[-1]['label']='Griff'
        m.prism(rect(100,10,60,10),'#888888',-4,4);m.parts[-1]['label']='Lauf'
        m.prism(rect(10,4,30,6),'#FF8800',-11,11,emit=True)
        return m
    def test_explicit_wins(self):
        m=self._model();channel(m,'MT_Accent')
        role=color_roles(m);pch,_=assign_channels(m,role,lambda P:1.0,lambda d:1.0)
        self.assertEqual(pch[-1],('MT_Accent','explicit'))
        self.assertEqual(pch[0][0],'MT_Primary');self.assertEqual(pch[1][0],'MT_Detail');self.assertEqual(pch[2][0],'MT_Metal')
    def test_explicit_rejects_unknown(self):
        m=self._model()
        with self.assertRaises(AssertionError):channel(m,'MT_Glow')
    def test_copy_channels(self):
        m=self._model();copy_channels(m,[{},{'ch':'MT_Secondary'},{},{}])
        self.assertEqual(m.parts[1]['channel'],'MT_Secondary');self.assertNotIn('channel',m.parts[0])
    def test_channel_does_not_change_sheet_colors(self):
        """Ein gesetzter Kanal ändert die Farbvarianten des Blatts nicht (recolor liest ihn nicht)."""
        for s in sheetmodels.SHEETS:
            g,_=split_sight(sheetmodels.load(s)['m'])
            g2=copy.deepcopy(g)
            for P in g2.parts:P['channel']='MT_Detail'
            strip=lambda m:[{k:v for k,v in P.items() if k!='channel'} for P in m.parts]
            for _,pal in VARIANTS:
                self.assertEqual(strip(recolor(g,pal)),strip(recolor(g2,pal)),s)

class SkinSpec(unittest.TestCase):
    """Feld skin (claude-0.3): fünf Skins je Blatt, Verweise, Farben je Variante, Geometrie der Aufkleber/Schmuckteile."""
    def test_skins(self):
        import skins
        heroes={}
        for s in sheetmodels.SHEETS:
            sp=load(s);sk=sp['skin']
            with self.subTest(sheet=s):
                ids=[it['id'] for it in sk['items']]
                self.assertEqual(len(set(ids)),5);self.assertTrue(set(ids)<=set(sk['catalog']))
                self.assertEqual(sk['hero'],ids[0]);self.assertEqual([it['hero'] for it in sk['items']],[True]+[False]*4)
                heroes[ids[0]]=heroes.get(ids[0],0)+1
                parts={p['id']:p for p in sp['parts']}
                lo,hi=sp['dimensions_m']['weapon']['bounds_m'];ext=max(hi[k]-lo[k] for k in range(3))
                for it in sk['items']:
                    used=set(it['slots_used'])
                    for v in sp['palette']:
                        cv=it['colors'][v['id']]
                        self.assertEqual(set(cv),used)
                        for sl,c in cv.items():
                            if sl.startswith('MT_'):
                                self.assertEqual(c['color'],v['channels'][sl] or v['swatches'][skins.SWATCH_FALLBACK[sl]],(it['id'],v['id'],sl))
                                self.assertEqual(c['source'],'channel' if v['channels'][sl] else 'swatch')
                            else:self.assertEqual(c['color'],it['accents'][sl]['color'])
                    for L in it['layers']:
                        ref=([L['slot']] if 'slot' in L else [])+L.get('slots',[])+[dd['slot'] for dd in L.get('decals',[])]
                        self.assertTrue(set(ref)<=used,(it['id'],L['type']))
                        if L['type'] in ('side_block','bands','gradient','rings','finish','edge_wear'):
                            self.assertTrue(L['parts']);self.assertTrue(set(L['parts'])<=set(parts))
                            self.assertFalse(any(parts[q]['sight'] or parts[q]['emissive'] for q in L['parts']))
                        if L['type']=='bands':self.assertGreaterEqual(L['period_m']+1e-9,L['width_m']);self.assertGreater(L['width_m'],0)
                        if L['type']=='glyphs':
                            self.assertIn(L['part'],parts)
                            for dd in L['decals']:   # flach auf der Seitenfläche (X konstant), im Hüllquader der Waffe
                                xs=[q[0] for q in dd['points_m']];self.assertLess(max(xs)-min(xs),1e-3)
                                for q in dd['points_m']:
                                    for k in range(3):self.assertTrue(lo[k]-0.02*ext<=q[k]<=hi[k]+0.02*ext,(it['id'],q))
                        if L['type']=='trim':
                            self.assertIn(L['attach'],parts);self.assertTrue(L['parts'])
                            for tp in L['parts']:
                                b=tp['bounds_m']
                                for k in range(3):self.assertTrue(lo[k]-0.12*ext<=b[0][k] and b[1][k]<=hi[k]+0.12*ext,(it['id'],b))
        # jeder Katalog-Skin ist auf mindestens drei Blättern Hauptskin
        self.assertEqual(set(heroes),{c['id'] for c in skins.CATALOG});self.assertGreaterEqual(min(heroes.values()),3)

class SkinGeometry(unittest.TestCase):
    def test_glyph_layout_and_mirror(self):
        import skins
        polys,w=skins.layout([('digit','0'),('digit','7')],20)
        self.assertEqual(len(polys),6+3);self.assertGreater(w,20)
        for poly,_ in polys:self.assertTrue(all(-1<=y<=21 for _,y in poly))
        d=sheetmodels.load('KD02');rs=skins.resolve(d['m'],'rennstreifen','KD02',d['num'],d['palette'])
        g=[L for L in rs['layers'] if L['type']=='glyphs'][0]
        x0,y0,x1,y1=g['rect'];lft=[dd for dd in g['decals'] if dd[0]=='z+'];rgt=[dd for dd in g['decals'] if dd[0]=='z-']
        self.assertEqual(len(lft),len(rgt))
        for a,b in zip(lft,rgt):   # rechte Seite = linke an der Rechteckmitte gespiegelt
            for (xa,ya),(xb,yb) in zip(a[2],b[2]):self.assertAlmostEqual(xa+xb,x0+x1,6);self.assertAlmostEqual(ya,yb,6)
        P=d['m'].parts[g['part']];poly=skins.side_face(P)[0]
        for x,y in ((x0,y0),(x1,y0),(x0,y1),(x1,y1)):self.assertTrue(skins.inside(poly,x,y))
    def test_pick_is_stable_and_distinct(self):
        import skins
        for s in ('KC01','KH10'):
            d=sheetmodels.load(s);a=skins.pick(s,d['m'],d['num'],d['palette']);b=skins.pick(s,d['m'],d['num'],d['palette'])
            self.assertEqual(a,b);self.assertEqual(len(set(a)),5)

LAYER_FIELDS={'side_block':['parts','slot','poly_yz_m'],'bands':['parts','dir','t0_m','width_m','period_m','count','slots','window_yz_m'],
 'gradient':['parts','dir','t0_m','t1_m','steps','slots'],'rings':['parts','axis','center_yz_m','r0_m','width_m','gap_m','count','slots'],
 'finish':['parts','slot','target'],'edge_wear':['parts','width_mm','coverage','color'],
 'glyphs':['part','items','content','height_m','bounds_m','decals'],'trim':['kind','attach','slot','count','parts']}
class SkinFrame(unittest.TestCase):
    """Pflichtfelder je Lagentyp (das Schema prüft nur type/block) und Umrechnung Modell -> Toolgen-Rahmen."""
    def test_layer_fields(self):
        for s in sheetmodels.SHEETS:
            for it in load(s)['skin']['items']:
                for L in it['layers']:
                    with self.subTest(sheet=s,skin=it['id'],type=L['type']):
                        self.assertEqual([k for k in LAYER_FIELDS[L['type']] if k not in L],[])
                        if L['type']=='trim':
                            for tp in L['parts']:self.assertEqual(sorted(tp),['bounds_m','profile_yz_m','x_m'])
    def test_frame(self):
        import skins
        s='KD02';sp=load(s);d=sheetmodels.load(s)
        u=sp['units']['model_unit_m'];o=sp['anchors']['Socket_Hand']['model']
        M=sp['axes']['matrix_model_to_target']
        P=lambda q:[u*sum(M[r][c]*(q[c]-o[c]) for c in range(3)) for r in range(3)]
        it=[i for i in sp['skin']['items'] if i['id']=='rennstreifen'][0]
        rs=skins.resolve(d['m'],'rennstreifen',s,d['num'],d['palette'])
        gm=[L for L in rs['layers'] if L['type']=='glyphs'][0];gs=[L for L in it['layers'] if L['type']=='glyphs'][0]
        pl,val,pts,_=gm['decals'][0];exp=P((pts[0][0],pts[0][1],val))
        for k in range(3):self.assertAlmostEqual(gs['decals'][0]['points_m'][0][k],exp[k],delta=2e-4)
        self.assertEqual(gs['decals'][0]['surface'],'left');self.assertGreater(gs['decals'][0]['points_m'][0][0],0)  # links = +X
        # Seitenband: Modell y (unten) -> Toolgen −Z; t0 im Zielrahmen = u·(t_model − Socket_Hand·dir)
        bm=[L for L in rs['layers'] if L['type']=='bands' and L['dir']==(0.0,1.0,0.0)][0]
        bs=[L for L in it['layers'] if L['type']=='bands' and L['dir']==[0.0,0.0,-1.0]][0]
        self.assertAlmostEqual(bs['t0_m'],u*(bm['t0']-o[1]),delta=2e-4)
        # ein Punkt im Band liegt im Zielrahmen ebenfalls im Band
        q=(o[0],bm['t0']+bm['width']/2,o[2]);pm=P(q);t=sum(pm[k]*bs['dir'][k] for k in range(3))
        self.assertTrue(bs['t0_m']<=t<=bs['t0_m']+bs['width_m'],(t,bs['t0_m']))

class Variants(unittest.TestCase):
    """Varianten-Register (claude-0.4): Namensregel für neue Varianten, Name im Spec, Facettenkörper der Variante J."""
    def test_naming_rule(self):
        self.assertEqual(len(set(variants.LETTERS)),len(variants.LETTERS))
        for v in variants.VARIANTS:
            if v['letter'] in 'CDFGH':self.assertIsNone(v['name']);continue   # älter als die Regel
            with self.subTest(variant=v['letter']):self.assertEqual(variants.name_problems(v['letter'],v['name']),[])
        self.assertTrue(variants.name_problems('K','Black Ice'))        # vergeben
        self.assertTrue(variants.name_problems('K','Parallax'))         # Codex
        self.assertTrue(variants.name_problems('K','schwarzes eis'))    # Schreibweise
        self.assertTrue(variants.name_problems('K',None))
        self.assertTrue(variants.name_problems('I','Glass Fang'))       # I wird nicht vergeben
        self.assertEqual(variants.name_problems('K','Glass Fang'),[])
    def test_spec_name(self):
        for s in sheetmodels.SHEETS:
            with self.subTest(sheet=s):self.assertEqual(load(s)['sheet']['variant_name'],variants.name(s[1]))
    def test_facet_faces(self):
        import jlib
        m=jlib.model([jlib.K([(0,0),(80,0),(100,20),(80,40),(0,40)],'#222222',-10,10,b=4,bz=4)])
        F=m.parts[0]['F']
        self.assertEqual(tuple(F[0]['n']),(0,0,1));self.assertEqual(tuple(F[1]['n']),(0,0,-1))
        self.assertEqual({v[2] for v in F[0]['v']},{10});self.assertEqual({v[2] for v in F[1]['v']},{-10})
        # Seitenfläche eingerückt, Normalen Einheitslänge, je Kante Band + zwei Facetten
        xs=[v[0] for v in F[0]['v']];self.assertAlmostEqual(min(xs),4,places=6)
        self.assertEqual(len(F),2+3*5)
        for f in F:self.assertAlmostEqual(sum(c*c for c in f['n']),1,places=9)
        import skins
        self.assertIsNotNone(skins.side_face(m.parts[0]))
        with self.assertRaises(ValueError):jlib.inset([(0,0),(10,0),(10,4),(0,4)],3)   # Fase breiter als das Teil

if __name__=='__main__':unittest.main()
