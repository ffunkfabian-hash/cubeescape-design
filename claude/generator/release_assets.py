"""Packt die Konzeptblätter als Release-Asset und hängt sie per gh an das Release claude-v<Version> (nur auf Wunsch des Nutzers).
   python3 claude/generator/release_assets.py            # Probelauf: packt nach dist/ (ungetrackt) und zeigt, was hochgeladen würde
   python3 claude/generator/release_assets.py --upload   # zusätzlich: gh release upload claude-v<Version> dist/*.zip --clobber
Voraussetzung: Blätter gebaut (build_all.py --nur-xl --force: vor einem Release immer ohne Inhalts-Cache, sheetcache.py, Prüfung: python3 claude/tests/test_golden.py --full), Release existiert
(der Workflow legt es beim Push auf release/claude-<Version> an). Je Variante ein zip: Blätter, Specs, fonts/ (Pakete laufen allein offline), dazu eins für die Visier-Serie VS01–VS09;
dazu ein zip Vorschauen samt Viewer index.html (make_viewer.py), falls vorhanden. Entpackt man alle zips in einen Ordner, öffnet index.html den Viewer."""
import os,re,subprocess,sys,zipfile
from cepaths import ROOT,OUT,PREV,CLAUDE
from variants import LETTERS as VARIANTS
from sheetmodels import SHEETS
def version():
    with open(os.path.join(ROOT,'CHANGELOG.md'),encoding='utf-8') as f:return re.search(r'(?m)^## claude-(\d+\.\d+(?:\.\d+)?)',f.read()).group(1)
def pack(zpath,files):
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_STORED) as z:   # WebP/TTF sind schon komprimiert
        for arc,src in files:z.write(src,arc)
def main(argv):
    ver=version();tag=f'claude-v{ver}';dist=os.path.join(ROOT,'dist');os.makedirs(dist,exist_ok=True)
    fonts=[(f'sheets/fonts/{n}',os.path.join(OUT,'fonts',n)) for n in sorted(os.listdir(os.path.join(OUT,'fonts')))]
    zips=[]
    for v in VARIANTS:
        sheets=sorted(f for f in os.listdir(OUT) if re.fullmatch(rf'K{v}\d\d\.(dc\.html|spec\.json)',f))
        want=sum(i.startswith(f'K{v}') for i in SHEETS)   # Blattzahl je Variante aus sheetmodels (G hat seit 0.10 KG01–KG25)
        if sum(s.endswith('.dc.html') for s in sheets)!=want:sys.exit(f'Variante {v}: nicht {want} Blätter gebaut (build_all.py --nur-xl)')
        z=os.path.join(dist,f'claude-konzeptblaetter-{v}-{tag}.zip');pack(z,[(f'sheets/{s}',os.path.join(OUT,s)) for s in sheets]+fonts);zips.append(z)
    import vsmodels   # Visier-Serie (claude-0.6): ein zip mit VS01–VS09 und den Sight-Specs
    vsf=[f for v in vsmodels.IDS for f in (f'{v}.dc.html',f'{v}.spec.json')]
    miss=[f for f in vsf if not os.path.exists(os.path.join(OUT,f))]
    if miss:sys.exit('Visier-Serie nicht vollständig gebaut (build_vs.py, export_sight.py): '+' '.join(miss[:4]))
    z=os.path.join(dist,f'claude-visier-serie-{tag}.zip');pack(z,[(f'sheets/{f}',os.path.join(OUT,f)) for f in vsf]+fonts);zips.append(z)
    pv=sorted(os.listdir(PREV)) if os.path.isdir(PREV) else []
    if pv:z=os.path.join(dist,f'claude-vorschauen-{tag}.zip');pack(z,[(f'previews/{p}',os.path.join(PREV,p)) for p in pv]+[('index.html',os.path.join(CLAUDE,'output','index.html'))]);zips.append(z)
    for z in zips:print(f'{os.path.getsize(z)/1e6:7.1f} MB  {os.path.relpath(z,ROOT)}')
    if '--upload' in argv:
        subprocess.run(['gh','release','upload',tag,*zips,'--clobber'],check=True,cwd=ROOT);print('hochgeladen an',tag)
    else:print(f'Probelauf: nichts hochgeladen (--upload hängt an {tag})')
if __name__=='__main__':main(sys.argv[1:])
