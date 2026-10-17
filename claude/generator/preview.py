"""WebP-Vorschauen der Konzeptblätter (claude/output/previews/KXnn.webp, 1600 px breit) aus generator/final/KXnn.html.
   python3 preview.py KJ01 KJ02 …     (Playwright/Chromium; Bildstufe: auf dem Mac mit heavy_lock)
Bis 0.3 lief die Aufnahme ohne eigenes Skript; Maße wie dort: volle Blattgröße 4800×4432, verkleinert auf 1600 px."""
from cepaths import E3D,PREV
import io,os,sys
from PIL import Image
from playwright.sync_api import sync_playwright
W,H,OUTW=4800,4432,1600
def main(ids):
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':W,'height':H})
        for sid in ids:
            pg.goto('file://'+os.path.join(E3D,'final',sid+'.html'));pg.wait_for_load_state('networkidle');pg.wait_for_timeout(400)
            im=Image.open(io.BytesIO(pg.screenshot(full_page=False))).convert('RGB')
            im.resize((OUTW,round(im.height*OUTW/im.width)),Image.LANCZOS).save(os.path.join(PREV,sid+'.webp'),'WEBP',quality=88,method=6)
            print(sid,'ok')
        b.close()
if __name__=='__main__':main(sys.argv[1:])
