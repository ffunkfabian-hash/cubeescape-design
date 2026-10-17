"""Baut die Blätter der Visier-Serie: claude/output/sheets/VSnn.dc.html (Bildstufe: numpy/scipy, auf dem Mac mit heavy_lock).
   python3 claude/generator/build_vs.py            # alle neun
   python3 claude/generator/build_vs.py VS01 VS05  # nur diese
Die Specs schreibt export_sight.py (ohne Bildstufe); das Blatt liest dieselben Modelle (vsmodels.py)."""
from cepaths import E3D,OUT
import os,sys,time
sys.path.insert(0,E3D)
import vsheet,vsmodels
def main(ids):
    for vid in ids or vsmodels.IDS:
        t=time.time();page=vsheet.sheet(vid)
        with open(os.path.join(OUT,f'{vid}.dc.html'),'w',encoding='utf-8') as f:f.write(page)
        with open(os.path.join(E3D,'final',f'{vid}.html'),'w',encoding='utf-8') as f:f.write(page.replace('<script src="./support.js"></script>',''))
        print(f'{vid}.dc.html',len(page)//1024,'KB',f'{time.time()-t:.1f} s',flush=True)
if __name__=='__main__':main(sys.argv[1:])
