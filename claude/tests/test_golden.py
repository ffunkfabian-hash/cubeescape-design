"""Golden-Hashes und Determinismus (Muster Toolgen: Hash statt Bild im Repo).
   python3 claude/tests/test_golden.py            # schnell: Spec-Hashes, Determinismus der Specs, Gegenbeweis
   python3 claude/tests/test_golden.py --full     # zusätzlich Blätter (nach build_all.py --nur-xl) und Determinismus eines Blatts (Mac, numpy/scipy)
   python3 claude/tests/test_golden.py --update [--specs|--sheets]   # golden.json aus den Dateien auf der Platte neu schreiben
Golden = sha256 je claude/output/sheets/KXnn.spec.json und KXnn.dc.html in claude/tests/golden.json; die Visier-Serie (claude-0.6)
unter vs_specs/vs_sheets (VSnn.spec.json, VSnn.dc.html). Ändert sich eine Ausgabe
absichtlich, steht die neue Hash-Liste im selben Commit wie die Änderung (nach Neubau: --update).
"""
import hashlib,json,os,subprocess,sys,tempfile,unittest
HERE=os.path.dirname(os.path.abspath(__file__))
GEN=os.path.join(HERE,'..','generator');sys.path.insert(0,GEN)
from cepaths import OUT
import sheetmodels,vsmodels
GOLDEN=os.path.join(HERE,'golden.json')
FULL='--full' in sys.argv
sha=lambda b:hashlib.sha256(b).hexdigest()
def disk(sheet,ext):
    with open(os.path.join(OUT,f'{sheet}.{ext}'),'rb') as f:return sha(f.read())
def golden():
    with open(GOLDEN,encoding='utf-8') as f:return json.load(f)

def run_hashes(cmd,seeds=('1','2')):
    """Führt cmd einmal je PYTHONHASHSEED aus; liefert die Ausgaben (Determinismus = alle gleich)."""
    outs=[]
    for sd in seeds:
        r=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONHASHSEED':sd})
        if r.returncode:raise RuntimeError(r.stderr[-1500:])
        outs.append(r.stdout)
    return outs

SPEC_CMD=lambda s:[sys.executable,'-c',f'import sys;sys.path.insert(0,{GEN!r});import export_spec;sys.stdout.write(export_spec.dumps(export_spec.build({s!r})))']
# Gegenbeweis: absichtlich nicht deterministisch (hash() von Strings ist je Prozess zufällig)
BAD_CMD=[sys.executable,'-c','print(abs(hash("zufall"))%9999)']
GOOD_CMD=[sys.executable,'-c','import zlib;print(zlib.crc32(b"zufall")%9999)']

class Golden(unittest.TestCase):
    def test_golden_covers_all_sheets(self):
        g=golden();self.assertEqual(sorted(g['specs']),sorted(sheetmodels.SHEETS));self.assertEqual(sorted(g['sheets']),sorted(sheetmodels.SHEETS))
    def test_spec_hashes(self):
        g=golden()['specs'];bad=[s for s in sheetmodels.SHEETS if disk(s,'spec.json')!=g[s]]
        self.assertEqual(bad,[],'Spec geändert – neu bauen und: python3 claude/tests/test_golden.py --update --specs')
    def test_vs_spec_hashes(self):
        g=golden()['vs_specs'];self.assertEqual(sorted(g),vsmodels.IDS)
        bad=[v for v in vsmodels.IDS if disk(v,'spec.json')!=g[v]]
        self.assertEqual(bad,[],'Sight-Spec geändert – python3 claude/generator/export_sight.py, dann test_golden.py --update --specs')
    @unittest.skipUnless(FULL,'nur mit --full (nach build_vs.py)')
    def test_vs_sheet_hashes(self):
        g=golden()['vs_sheets'];bad=[v for v in vsmodels.IDS if disk(v,'dc.html')!=g[v]]
        self.assertEqual(bad,[],'Visier-Blatt geändert – python3 claude/tests/test_golden.py --update --sheets')
    @unittest.skipUnless(FULL,'nur mit --full (nach build_all.py --nur-xl)')
    def test_sheet_hashes(self):
        g=golden()['sheets'];bad=[s for s in sheetmodels.SHEETS if disk(s,'dc.html')!=g[s]]
        self.assertEqual(bad,[],'Blatt geändert – python3 claude/tests/test_golden.py --update --sheets')

class Determinism(unittest.TestCase):
    def test_spec_build_is_deterministic(self):
        for s in ('KC01','KD05','KH10'):
            with self.subTest(sheet=s):
                a,b=run_hashes(SPEC_CMD(s));self.assertEqual(a,b)
    def test_detector_catches_nondeterminism(self):
        """Gegenbeweis: Die Prüfung schlägt bei einer absichtlich nicht deterministischen Ausgabe an."""
        a,b=run_hashes(BAD_CMD);self.assertNotEqual(a,b)
        a,b=run_hashes(GOOD_CMD);self.assertEqual(a,b)
    @unittest.skipUnless(FULL,'nur mit --full (Bildstufe, ~3 Min.)')
    def test_sheet_build_is_deterministic(self):
        a,b=run_hashes([sys.executable,os.path.join(HERE,'emit_sheet.py'),'KC01']);self.assertEqual(a,b)
        self.assertEqual(a.strip(),golden()['sheets']['KC01'])   # Bau im Speicher = Datei in golden.json

def update(which):
    g=golden() if os.path.exists(GOLDEN) else {'specs':{},'sheets':{}}
    if which in ('all','specs'):g['specs']={s:disk(s,'spec.json') for s in sheetmodels.SHEETS};g['vs_specs']={v:disk(v,'spec.json') for v in vsmodels.IDS}
    if which in ('all','sheets'):
        # Blätter nur übernehmen, wenn sie gebaut sind (Waffenblätter und Visier-Serie getrennt baubar)
        if all(os.path.exists(os.path.join(OUT,f'{s}.dc.html')) for s in sheetmodels.SHEETS):g['sheets']={s:disk(s,'dc.html') for s in sheetmodels.SHEETS}
        if all(os.path.exists(os.path.join(OUT,f'{v}.dc.html')) for v in vsmodels.IDS):g['vs_sheets']={v:disk(v,'dc.html') for v in vsmodels.IDS}
    with open(GOLDEN,'w',encoding='utf-8') as f:json.dump(g,f,indent=1,sort_keys=True);f.write('\n')
    print('golden.json:',len(g['specs']),'Specs,',len(g['sheets']),'Blätter,',len(g.get('vs_specs',{})),'Sight-Specs,',len(g.get('vs_sheets',{})),'Visier-Blätter')

if __name__=='__main__':
    if '--update' in sys.argv:update('specs' if '--specs' in sys.argv else 'sheets' if '--sheets' in sys.argv else 'all');sys.exit(0)
    unittest.main(argv=[a for a in sys.argv if a!='--full'])
