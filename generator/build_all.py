"""Baut alle Karten und Konzeptblätter neu.
   python generator/build_all.py            # alles (Karten + XL-Blätter + Prompts)
   python generator/build_all.py --nur-xl   # nur die großen Konzeptblätter aus den vorhandenen reg/*.pkl
   python generator/build_all.py --varianten C G   # nur bestimmte Varianten
"""
import subprocess,sys,os,shutil
from concurrent.futures import ThreadPoolExecutor
from cepaths import E3D,ROOT,OUT
os.chdir(E3D)
args=sys.argv[1:]
nur_xl='--nur-xl' in args
V=[a for a in args if len(a)==1 and a in 'CDFGH'] or list('CDFGH')
P=lambda *c:[sys.executable,*c]
N=[f'{i:02d}' for i in range(1,11)]
jobs={
 'C':[P('build_v01.py')]+[P('build_c25.py',n) for n in N[1:5]]+[P('build_c.py',n) for n in N[5:]]+[P('make_v2d.py',*N)],
 'D':[P('build_d15.py','1','2','3','4','5'),P('build_d.py',*N[5:]),P('render_dx05.py')],
 'F':[P('build_f15.py',*N[:5],'noshot'),P('build_f610.py',*N[5:],'noshot')],
 'G':[P('build_g15.py',n,'noshot') for n in N[:5]]+[P('build_g610.py',n,'noshot') for n in N[5:]],
 'H':[P('build_h15.py',n,'noshot') for n in N[:5]]+[P('build_h610.py',n,'noshot') for n in N[5:]],
}
fid={'C':['v01']+[f'c{n}' for n in N[1:]],'D':[f'd{n}' for n in N],'F':[f'f{n}' for n in N],'G':[f'g{n}' for n in N],'H':[f'h{n}' for n in N]}
def run_seq(cmds):
    for c in cmds:
        r=subprocess.run(c,capture_output=True,text=True)
        print(('OK  ' if r.returncode==0 else 'FEHLER ')+' '.join(c[1:]),flush=True)
        if r.returncode:print(r.stderr[-2000:])
if not nur_xl:
    with ThreadPoolExecutor(len(V)) as ex:list(ex.map(run_seq,[jobs[v] for v in V]))
with ThreadPoolExecutor(len(V)) as ex:list(ex.map(run_seq,[[P('build_xl.py',*fid[v])] for v in V]))
run_seq([P('mkdoc.py')])
if os.path.exists('Waffen-Prompts.md'):shutil.copy('Waffen-Prompts.md',os.path.join(ROOT,'docs','prompts','Waffen-Prompts.md'))
print('fertig')
