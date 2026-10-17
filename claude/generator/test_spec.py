"""Schema- und Stimmigkeitstest der Spec-Dateien (claude/output/sheets/KXnn.spec.json). Ohne numpy, ohne Bildstufe.
   python3 -m unittest claude/generator/test_spec.py      (oder: python3 claude/generator/test_spec.py)
"""
from cepaths import E3D,CLAUDE,OUT
import copy,json,math,os,re,sys,unittest
sys.path.insert(0,E3D)
import export_spec,sheetmodels
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
        """50 Dateien, jede gleich der Ausgabe des Exporters (sonst: python3 claude/generator/export_spec.py)."""
        self.assertEqual(len(sheetmodels.SHEETS),50)
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
                    self.assertEqual({c for c,h in v['channels'].items() if h},used,v['id'])
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
        for s in ('KC01','KF09','KH05'):
            g,_=split_sight(sheetmodels.load(s)['m'])
            g2=copy.deepcopy(g)
            for P in g2.parts:P['channel']='MT_Detail'
            for _,pal in VARIANTS:
                self.assertEqual([(P['col'],P['dec']) for P in recolor(g,pal).parts],[(P['col'],P['dec']) for P in recolor(g2,pal).parts])

if __name__=='__main__':unittest.main()
