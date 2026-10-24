"""Claudes Pipeline liest den gemeinsamen Texturkatalog (claude/generator/texcat.py, docs/textures/catalog.json; claude-0.8).
   python3 claude/tests/test_texcat.py        # ohne Bildstufe; Tonleiter-Test nur mit numpy
Regressionsanker: claude/tests/data/skins-legacy-0.7.json (skins.CATALOG/DESC vor der Umstellung). Ein Skin, ein Material und eine Oberfläche,
die die Pipeline benutzt, müssen im Katalog stehen (Regel in docs/textures/README.md).
"""
import json,math,os,sys,unittest
HERE=os.path.dirname(os.path.abspath(__file__))
GEN=os.path.join(HERE,'..','generator');sys.path.insert(0,GEN)
import texcat,skins,export_spec,texprofile,sheetmodels,variants
from xlroles import MATERIAL_IDS

def norm(x):
    if isinstance(x,(list,tuple)):return [norm(y) for y in x]
    if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
    return x
def _json(p):
    with open(p,encoding='utf-8') as f:return json.load(f)
LEGACY=_json(os.path.join(HERE,'data','skins-legacy-0.7.json'))

class Catalog(unittest.TestCase):
    def test_format_is_checked(self):
        import tempfile
        c=dict(texcat.load());c['format_version']=2
        with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:json.dump(c,f)
        with self.assertRaises(ValueError):texcat.load(f.name)
        os.unlink(f.name)

    def test_skins_equal_legacy(self):
        self.assertEqual(norm(skins.CATALOG),LEGACY['catalog'])
        self.assertEqual({k:list(v) for k,v in skins.DESC.items()},LEGACY['desc'])
        self.assertEqual(skins.FINISHES,('paint','polished_gold','polished_chrome','neon'))
        self.assertEqual(skins.BARE_METAL,'#9AA2AC')

    def test_everything_used_is_in_the_catalog(self):
        ids={s['id'] for s in texcat.load()['skins']};fin=set(texcat.finish_ids())
        for s in skins.CATALOG:
            self.assertIn(s['id'],ids)
            for a,(c,f) in s['accents'].items():self.assertIn(f,fin,(s['id'],a))
        for sid in MATERIAL_IDS.values():
            if sid=='glass':self.assertIsNone(export_spec.TEXTURE_ID[sid]);continue
            m=texcat.material_of_alias(sid,'spec');self.assertEqual(export_spec.TEXTURE_ID[sid],m['id'])
            self.assertEqual(export_spec.TOOLGEN_MATERIAL[sid],m['toolgen_material'])
        for k,sid in (('lack','painted'),('brushed','brushed'),('rubber','rubber'),('plastic','matte'),('light','lit')):
            self.assertEqual(texcat.material_of_alias(k,'claude')['id'],texcat.material_of_alias(sid,'spec')['id'])

    def test_fingerprint_follows_pattern_values(self):
        f0=texcat.fingerprint();c=texcat.load();old=c['patterns'][2]['size_mm']
        try:
            c['patterns'][2]['size_mm']=old+1;self.assertNotEqual(texcat.fingerprint(),f0)
        finally:c['patterns'][2]['size_mm']=old
        self.assertEqual(texcat.fingerprint(),f0)

    def test_unit_must_be_valid_and_aliases_unique(self):
        for bad in (0,-1,float('inf'),float('nan'),'x'):
            with self.assertRaises(ValueError):texcat.sheet_patterns(bad)
        for who in ('claude','spec'):
            al=[m['aliases'][who] for m in texcat.load()['materials'] if who in m['aliases']];self.assertEqual(len(al),len(set(al)),who)

    def test_catalog_content_is_part_of_the_cache_key(self):
        import sheetcache as SC
        SC._code_cache.clear();k0=SC.code_key('weapon');orig=texcat.fingerprint
        try:
            texcat.fingerprint=lambda:'geaendert';SC._code_cache.clear();self.assertNotEqual(SC.code_key('weapon'),k0)
        finally:
            texcat.fingerprint=orig;SC._code_cache.clear()
        self.assertEqual(SC.code_key('weapon'),k0)

class Patterns(unittest.TestCase):
    """Bei der Modelleinheit des Katalog-Startwerts ergeben die Katalogwerte die Muster von claude-0.7 (Rundung der mm-Werte auf 3 Stellen)."""
    P=texcat.sheet_patterns(texcat.load()['units']['model_unit_m'])
    def near(self,a,b,tol=2e-3):self.assertLess(abs(a-b)/abs(b),tol,(a,b))
    def test_legacy_values(self):
        P=self.P
        self.near(P['gloss'][0]['k'],1/26);self.assertEqual(P['gloss'][0]['axes'],('height',));self.assertEqual(P['gloss'][0]['amp'],0.09)
        self.near(P['gloss'][1]['k'],1/55);self.assertEqual(P['gloss'][1]['axes'],('length','width'));self.assertEqual(P['gloss'][1]['amp'],0.04)
        self.assertEqual(P['brushed']['amp'],0.13)
        for (k,ph,wt),(k0,ph0,wt0) in zip(P['brushed']['waves'],((3.1,0.0,0.5),(7.3,1.7,0.3),(13.1,0.4,0.2))):
            self.near(k,0.9*k0);self.assertEqual((ph,wt),(ph0,wt0))
        self.near(P['knurl']['cell'],4.0);self.assertEqual(P['knurl']['dark'],0.34)
        self.near(P['grain']['cell'],1/1.3);self.assertEqual(P['grain']['amp'],0.09);self.assertEqual(P['grain']['hash'],(0.37,1.91,3.7))
    def test_physical_size_is_constant(self):
        """dieselbe Rändelung ist auf jeder Waffe gleich fein: doppelte Modelleinheit -> halbe Zelle in Modelleinheiten"""
        a=texcat.sheet_patterns(0.001);b=texcat.sheet_patterns(0.002)
        self.assertAlmostEqual(a['knurl']['cell']/b['knurl']['cell'],2.0)
        self.assertAlmostEqual(a['grain']['cell']/b['grain']['cell'],2.0)
        self.assertAlmostEqual(b['gloss'][0]['k']/a['gloss'][0]['k'],2.0)
        self.assertAlmostEqual(a['knurl']['cell']*0.001*1000,texcat.pattern('knurl')['size_mm'])

class Ladders(unittest.TestCase):
    def test_tones_equal_legacy(self):
        try:
            import numpy  # noqa: F401
        except ImportError:
            self.skipTest('numpy fehlt (Bildstufe)')
        from skinraster import tones,LEVELS
        from xlroles import _mix
        from eng import lum
        self.assertEqual(LEVELS,(1.28,1.08,0.88,0.62))
        def legacy(c,fin):
            if fin=='polished_gold':return [_mix(c,'#FFF4D0',0.35),c,_mix(c,'#5A3A08',0.45),_mix(c,'#2A1A04',0.72),_mix(c,'#FFFFFF',0.8)]
            if fin=='polished_chrome':return [_mix(c,'#FFFFFF',0.5),c,_mix(c,'#1C2128',0.5),_mix(c,'#1C2128',0.8),'#FFFFFF']
            if fin=='neon':return [_mix(c,'#FFFFFF',0.25)]*4+[_mix(c,'#FFFFFF',0.25)]
            return [lum(c,f) for f in LEVELS]+[lum(c,LEVELS[0])]
        for c in ('#E2B04A','#C9D2DC','#123456','#FFFFFF','#000000','#6CF2FF'):
            for f in skins.FINISHES+('unbekannt',):self.assertEqual(tones(c,f),legacy(c,f),(c,f))
    def test_wear_and_streak(self):
        self.assertEqual(texcat.wear_cell_widths(),6.0);self.assertEqual(texcat.wear_width_variation(),(0.6,1.0))
        s=texcat.streak();self.assertEqual((s['direction'],s['period_rel'],s['width_fraction']),((0.55,-1.0,0.35),0.42,0.13))
        lv=texcat.wear_levels()
        for s_ in skins.CATALOG:
            for L in s_['layers']:
                if L['type']=='edge_wear':
                    self.assertTrue(any(abs(L['coverage']-v['coverage'])<0.12 for v in lv.values()),(s_['id'],L))

class Profile(unittest.TestCase):
    def test_profiles_use_catalog_ids(self):
        mats={m['id'] for m in texcat.load()['materials']};lv=set(texcat.wear_levels())
        import wtypes   # bestehende Typen nach Toolgen-ID, neue Typen (claude-0.10) nach wtypes.key, alle mit derived_from
        tids={wtypes.key(n) for n in wtypes.TYPES}-{'bow'}
        self.assertEqual(set(texprofile.PROFILES),tids)
        self.assertEqual(set(texprofile.DERIVED_FROM),{wtypes.key(n) for n in wtypes.NEW})
        self.assertTrue(set(texprofile.DERIVED_FROM.values())<=tids)
        for tid,p in texprofile.PROFILES.items():
            for k in ('housing','metal','rubber','energy'):self.assertIn(p[k]['material'],mats,(tid,k))
            self.assertIn(p['edge_wear']['level'],lv,tid);self.assertTrue(p['decals']['toolgen'],tid)
        self.assertIsNone(texprofile.profile('bow'))
    def test_decals_exist_in_toolgen_when_local(self):
        p=os.path.expanduser('~/Claude/cubeescape-toolgen/data/decals.json')
        if not os.path.exists(p):self.skipTest('Toolgen nicht lokal')
        d=_json(p)['decals'];ids=set(d)
        for tid,pr in texprofile.PROFILES.items():
            for x in pr['decals']['toolgen']:self.assertIn(x,ids,(tid,x))

class SpecFields(unittest.TestCase):
    def test_spec_references_catalog(self):
        ids={m['id'] for m in texcat.load()['materials']};sk={s['id'] for s in texcat.load()['skins']}
        for sh in sheetmodels.SHEETS:
            sp=_json(export_spec.path(sh))
            for p in sp['parts']:self.assertTrue(p['texture'] is None or p['texture'] in ids,(sh,p['id']))
            self.assertEqual({p['texture'] is None for p in sp['parts'] if p['material']=='glass'} or {True},{True})
            self.assertIn(sp['skin']['catalog_id'],sk);self.assertEqual(sp['skin']['catalog_id'],sp['skin']['hero'])
            for it in sp['skin']['items']:self.assertEqual(it['catalog_id'],it['id'])
            self.assertEqual(sp['textures']['catalog']['sha256_claude_parts'],texcat.fingerprint(),sh)
            self.assertEqual('texture_profile' in sp,sp['weapon']['toolgen_id']!='bow',sh)
            # Katalogwerte in mm sind für jede Waffe gleich
            self.assertEqual(sp['textures']['rubber']['size_mm'],texcat.pattern('knurl')['size_mm'])

class BlackIce(unittest.TestCase):
    def test_pick_prefers_dark_skins_only_for_j(self):
        heroes=[]
        for sh in sheetmodels.SHEETS:
            d=sheetmodels.load(sh)
            order=skins.pick(sh,d['m'],d['num'],d['palette'])
            self.assertEqual(len(set(order)),5)
            miss={sid:sum(1 for t in skins.resolve(d['m'],sid,sh,d['num'],d['palette'])['notes'] if not t.startswith(('finish','Kontrast'))) for sid in [s_['id'] for s_ in skins.CATALOG]}
            if sh[1]=='J':
                heroes.append(order[0] in skins.DARK_SKINS)
                self.assertEqual(miss[order[0]],min(miss.values()),sh)   # Lücken gehen vor
            else:
                legacy=sorted([skins.CATALOG[(((variants.LETTERS.index(sh[1]))*5+int(sh[2:]))%9+2*j)%9]['id'] for j in range(9)],key=lambda s:miss[s])[:5]
                self.assertEqual(order,legacy,sh)   # andere Varianten unverändert
        self.assertGreaterEqual(sum(heroes),7,heroes)   # Black Ice: Hauptskin überwiegend dunkel

if __name__=='__main__':unittest.main(verbosity=1)
