"""Packt die Konzeptblätter als Release-Asset und hängt sie per gh an das Release claude-v<Version> (nur auf Wunsch des Nutzers).
   python3 claude/generator/release_assets.py            # Probelauf: packt nach dist/ (ungetrackt) und zeigt, was hochgeladen würde
   python3 claude/generator/release_assets.py --upload   # zusätzlich: gh release upload claude-v<Version> dist/*.zip --clobber
Voraussetzung: Blätter gebaut (build_all.py --nur-xl, Prüfung: python3 claude/tests/test_golden.py --full), Release existiert
(der Workflow legt es beim Push auf release/claude-<Version> an). Je Variante ein zip: Blätter, Specs, fonts/ (Pakete laufen allein offline);
dazu ein zip Vorschauen, falls vorhanden."""
import os,re,subprocess,sys,zipfile
from cepaths import ROOT,OUT,PREV
VARIANTS='CDFGH'
def version():
    with open(os.path.join(ROOT,'CHANGELOG.md'),encoding='utf-8') as f:return re.search(r'(?m)^## claude-(\d+\.\d+(?:\.\d+)?)',f.read()).group(1)
def pack(zpath,files):
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_STORED) as z:   # WebP/TTF sind schon komprimiert
        for arc,src in files:z.write(src,arc)
def main(argv):
    ver=version();tag=f'claude-v{ver}';dist=os.path.join(ROOT,'dist');os.makedirs(dist,exist_ok=True)
    fonts=[(f'fonts/{n}',os.path.join(OUT,'fonts',n)) for n in sorted(os.listdir(os.path.join(OUT,'fonts')))]
    zips=[]
    for v in VARIANTS:
        sheets=sorted(f for f in os.listdir(OUT) if re.fullmatch(rf'K{v}\d\d\.(dc\.html|spec\.json)',f))
        if sum(s.endswith('.dc.html') for s in sheets)!=10:sys.exit(f'Variante {v}: nicht 10 Blätter gebaut (build_all.py --nur-xl)')
        z=os.path.join(dist,f'claude-konzeptblaetter-{v}-{tag}.zip');pack(z,[(s,os.path.join(OUT,s)) for s in sheets]+fonts);zips.append(z)
    pv=sorted(os.listdir(PREV)) if os.path.isdir(PREV) else []
    if pv:z=os.path.join(dist,f'claude-vorschauen-{tag}.zip');pack(z,[(f'previews/{p}',os.path.join(PREV,p)) for p in pv]);zips.append(z)
    for z in zips:print(f'{os.path.getsize(z)/1e6:7.1f} MB  {os.path.relpath(z,ROOT)}')
    if '--upload' in argv:
        subprocess.run(['gh','release','upload',tag,*zips,'--clobber'],check=True,cwd=ROOT);print('hochgeladen an',tag)
    else:print(f'Probelauf: nichts hochgeladen (--upload hängt an {tag})')
if __name__=='__main__':main(sys.argv[1:])
