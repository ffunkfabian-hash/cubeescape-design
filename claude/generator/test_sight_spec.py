"""Schema- und Stimmigkeitstest der Sight-Specs der Visier-Serie (claude/output/sheets/VSnn.spec.json). Ohne numpy, ohne Bildstufe.
   python3 claude/generator/test_sight_spec.py
"""
from cepaths import E3D,CLAUDE,OUT
import copy,json,os,re,sys,unittest
sys.path.insert(0,E3D)
import export_sight as ES,vsmodels as V,spec_checks as SC
import test_spec as TS                      # nur validate(); als Modul, damit dessen Tests hier nicht mitlaufen
from export_spec import SIGHT_TYPES

def _read(fn):
    with open(fn,encoding='utf-8') as f:return f.read()
SCHEMA=json.loads(_read(os.path.join(CLAUDE,'docs','sight-spec.schema.json')))
def load(vid):return json.loads(_read(ES.path(vid)))
TOL=1e-4

class Files(unittest.TestCase):
    def test_present_and_current(self):
        """neun Dateien, jede gleich der Ausgabe des Exporters (sonst: python3 claude/generator/export_sight.py)"""
        self.assertEqual(V.IDS,[f'VS0{k}' for k in range(1,10)])
        stale=[v for v in V.IDS if not os.path.exists(ES.path(v)) or _read(ES.path(v))!=ES.dumps(ES.build(v))]
        self.assertEqual(stale,[],'veraltet oder fehlend – python3 claude/generator/export_sight.py')
        extra=sorted(f for f in os.listdir(OUT) if f.startswith('VS') and f.endswith('.spec.json') and f[:-10] not in V.IDS)
        self.assertEqual(extra,[])
    def test_schema(self):
        for v in V.IDS:
            with self.subTest(sight=v):self.assertEqual(TS.validate(load(v),SCHEMA,root=SCHEMA),[])
    def test_deterministic(self):
        self.assertEqual(ES.dumps(ES.build('VS05')),ES.dumps(ES.build('VS05')))

class Content(unittest.TestCase):
    def test_target_per_weapon(self):
        """Typ je Waffe = Zielbild (spec_checks.CE_SIGHTS, Vokabular 0.5.2); kind/Fenster folgen aus dem Typ; Röhre nur bei precision/sniper
        (Spurgewehr ohne Röhre: Entscheidung des Nutzers)"""
        for v in V.IDS:
            sp=load(v);tid=sp['weapon']['toolgen_id'];s=sp['sight']
            with self.subTest(sight=v):
                nr,_,_,kinds,wins,typ=SC.CE_SIGHTS[tid]
                self.assertEqual(sp['weapon']['number'],nr);self.assertEqual(s['type'],typ)
                self.assertEqual((s['kind'],s['window_kind']),SIGHT_TYPES[typ]);self.assertIn(s['kind'],kinds);self.assertIn(s['window_kind'],wins)
                self.assertEqual(sp['tube'] is not None,typ in ('precision','sniper'))
                self.assertEqual(sp['anchors']['Socket_Eye'] is not None,sp['tube'] is not None)
                self.assertEqual(SC.sight_target_hints(dict(sp,sheet=dict(id=v),sight=dict(s,window=s['window_kind']))),[])
        self.assertIsNone(load('VS08')['tube'])
    def test_reticles_match_ce_table(self):
        """Fadenkreuz-Varianten je Waffe wie in Cube Escape Docs/EQUIPMENT.md › Visiere je Waffe (Spalte 4)"""
        p=SC.ce_equipment_path()
        if not os.path.exists(p):self.skipTest('Cube Escape nicht ausgecheckt: '+p)
        sec=_read(p).split('### Visiere je Waffe',1)[1].split('\n#',1)[0]
        rows={int(m.group(1)):[x.strip() for x in m.group(2).split(',')] for m in re.finditer(r'^\|\s*(\d+)\s+[^|]+\|[^|]+\|[^|]+\|([^|]+)\|',sec,re.M)}
        for v in V.IDS:
            sp=load(v)
            with self.subTest(sight=v):self.assertEqual([r['name_de'] for r in sp['reticle_variants']],rows[sp['weapon']['number']])
    def test_window_function_surface(self):
        """Funktionsfläche (Cubegen docs/DEVELOPER.md 9.17): Glas mit Durchsicht entlang −Y, kein Querfenster; ganze Öffnung frei"""
        for v in V.IDS:
            sp=load(v);parts={p['id']:p for p in sp['parts']}
            with self.subTest(sight=v):
                self.assertEqual(SC.window_problems(sp['window_geometry']['elements'],parts,[]),[])
                self.assertTrue(sp['sight_line']['clear']);self.assertEqual(sp['sight_line']['blocked_by'],[])
                self.assertEqual(sp['window']['aperture']['blocked_by'],[]);self.assertGreater(sp['window']['aperture']['rays'],1000)
                self.assertTrue(all(parts[g]['glass'] for g in sp['sight_line']['glass_crossed']))
    def test_anchors(self):
        """Socket_Sight am hinteren Fensterrand auf der Visierlinie, Socket_Reticle in der Glasmitte, Socket_Eye hinter dem Objektiv"""
        for v in V.IDS:
            sp=load(v);a={k:(x['position_m'] if x else None) for k,x in sp['anchors'].items()};h=sp['dimensions_m']['line_height_m']
            with self.subTest(sight=v):
                self.assertEqual(a['Socket_Mount'],[0.0,0.0,0.0])
                for k in ('Socket_Sight','Socket_Reticle'):self.assertAlmostEqual(a[k][0],0.0,delta=TOL);self.assertAlmostEqual(a[k][2],h,delta=TOL)
                self.assertGreater(a['Socket_Sight'][1],a['Socket_Reticle'][1])                  # hinten = +Y
                self.assertAlmostEqual(a['Socket_Sight'][1],sp['window']['rear_edge_y_m'],delta=TOL)
                self.assertEqual(a['Socket_Reticle'],sp['window']['center_m'])
                # Socket_Reticle liegt auf einer Glasfläche: Glastreffer der Visierlinie an seiner Stelle
                d=V.load(v);gx=[x for g,x,gl in ES.line_hits(d['S'].m.parts,d['geo']['line_y']) if gl]
                self.assertTrue(any(abs(ES.P((x,d['geo']['line_y'],0))[1]-a['Socket_Reticle'][1])<TOL for x in gx),(gx,a['Socket_Reticle']))
                # Socket_Mount mittig unter der Halterung
                mb=next(p for p in sp['parts'] if p['label']=='Halterung')['bounds_m']
                self.assertAlmostEqual((mb[0][1]+mb[1][1])/2,0.0,delta=TOL);self.assertAlmostEqual((mb[0][0]+mb[1][0])/2,0.0,delta=TOL)
                if a['Socket_Eye']:
                    self.assertGreaterEqual(a['Socket_Sight'][1],a['Socket_Eye'][1]);self.assertGreater(a['Socket_Eye'][1],a['Socket_Reticle'][1])
                    self.assertAlmostEqual(a['Socket_Eye'][2],h,delta=TOL)
                lo,hi=sp['dimensions_m']['bounds_m']
                for k,p in a.items():
                    if p:self.assertTrue(all(lo[i]-TOL<=p[i]<=hi[i]+TOL for i in range(3)),(k,p))
    def test_channels(self):
        """Gehäuse Secondary, Rahmen Accent, Glas Detail, Leuchtrahmen Energy (Auftrag Paket 2)"""
        want={'Gehäuse':'MT_Secondary','Rahmen':'MT_Accent','Glas':'MT_Detail','Leuchtrahmen':'MT_Energy','Markierungsrahmen':'MT_Energy'}
        for v in V.IDS:
            for p in load(v)['parts']:
                with self.subTest(sight=v,part=p['label']):
                    if p['label'] in want:self.assertEqual(p['channel'],want[p['label']])
                    self.assertEqual(p['glass'],p['label'] in ('Glas','Okularglas'))
                    if p['glass']:self.assertEqual((p['material'],p['toolgen_material'],p['emissive']),('glass',None,False))
        self.assertTrue(any(p['label']=='Leuchtrahmen' for p in load('VS07')['parts']))
        self.assertTrue(any(p['label']=='Markierungsrahmen' for p in load('VS08')['parts']))
    def test_tint_and_vocabulary(self):
        for v in V.IDS:
            sp=load(v);g=sp['glass']
            with self.subTest(sight=v):
                self.assertEqual(sp['glass_tint'],ES.tint_rgba(g['id']));self.assertEqual(sp['glass_tint'][3],V.TINTS[g['id']][2])
                self.assertIn(sp['sight']['frame'],V.FRAMES);self.assertEqual(sp['frame']['type'],sp['sight']['frame'])
                self.assertTrue(set(r['id'] for r in sp['reticle_variants'])<=set(V.RETICLES))
                self.assertEqual(sum(r['default'] for r in sp['reticle_variants']),1)
                for va in sp['variants']:self.assertIn(va['glass_tint'],V.TINTS)
        self.assertEqual(ES.tint_rgba('clear')[:3],[round(ES.srgb_to_linear(c),4) for c in (0xE4,0xEE,0xF5)])
    def test_weapon_spec_reference(self):
        for v in V.IDS:
            sp=load(v);ws=sp['weapon']['weapon_spec']['sheets']
            with self.subTest(sight=v):
                self.assertEqual(len(ws),6)
                for s in ws:self.assertEqual(TS.load(s)['weapon']['toolgen_id'],sp['weapon']['toolgen_id'])

class Counterproof(unittest.TestCase):
    """Gegenbeweis: die Prüfungen schlagen bei absichtlich falschen Modellen an."""
    def test_blocking_part_is_found(self):
        d=V.load('VS01');S=d['S'];ly=d['geo']['line_y']
        S.group('bad','Steg','MT_Secondary','painted',V.DARK).box('bad',-4,-2,ly-3,ly+3,-3,3)
        self.assertIn('bad',[g for g,_,gl in ES.line_hits(S.m.parts,ly) if not gl])
        rays,bad=ES.aperture_check(S,d['geo']);self.assertIn('bad',bad)
    def test_edge_block_found_only_by_aperture(self):
        """ein Teil am Rand der Öffnung verfehlt die Visierlinie, die Prüfung der ganzen Öffnung findet es"""
        d=V.load('VS06');S=d['S'];g=d['geo'];ly=g['line_y'];hh=g['window']['h']/2
        S.group('edge','Kante','MT_Secondary','painted',V.DARK).box('edge',-20,-16,ly+hh-3,ly+hh+2,-4,4)
        self.assertNotIn('edge',[x for x,_,gl in ES.line_hits(S.m.parts,ly)])
        self.assertIn('edge',ES.aperture_check(S,g)[1])
    def test_thin_and_shallow_blocks_found(self):
        """Gegenbeweise aus der Opus-Prüfung 0.6: ein 1,7 mm schmaler Steg neben der Linie und eine 0,9 mm tiefe Nase am Rand (Raster 0,5 mm
        plus Rand 0,3 mm: ab 0,8 mm Tiefe sicher gefunden)"""
        d=V.load('VS09');S=d['S'];g=d['geo'];ly=g['line_y'];hh=g['window']['h']/2
        S.group('rib','Steg','MT_Secondary','painted',V.DARK).box('rib',-20,-18,ly-hh,ly+hh,0.6,2.3)
        self.assertNotIn('rib',[x for x,_,gl in ES.line_hits(S.m.parts,ly)]);self.assertIn('rib',ES.aperture_check(S,g)[1])
        d=V.load('VS06');S=d['S'];g=d['geo'];ly=g['line_y'];hh=g['window']['h']/2
        S.group('nose','Nase','MT_Secondary','painted',V.DARK).box('nose',-20,-16,ly+hh-0.9,ly+hh+2,-4,4)
        self.assertIn('nose',ES.aperture_check(S,g)[1])
    def test_cross_window_is_found(self):
        sp=load('VS02');parts={p['id']:copy.deepcopy(p) for p in sp['parts']}
        gid=sp['window_geometry']['elements'][0]['part'];b=parts[gid]['bounds_m']
        # Scheibe um 90° gedreht: dünn entlang X statt Y (Querfenster)
        parts[gid]['bounds_m']=[[0.0,b[0][1]-0.01,b[0][2]],[0.0002,b[1][1]+0.01,b[1][2]]]
        pr=SC.window_problems(sp['window_geometry']['elements'],parts,[])
        self.assertTrue(any(p.startswith('Fenster quer [') for p in pr),pr)

if __name__=='__main__':unittest.main()
