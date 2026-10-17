import shutil,subprocess,sys
from playwright.sync_api import sync_playwright

def im():
    """ImageMagick-Aufruf: 7 kennt `magick`, 6 nur `convert` – nie fest `magick` aufrufen."""
    return [shutil.which('magick') or shutil.which('convert') or sys.exit('ImageMagick fehlt (magick/convert)')]

def png_clean(path):
    """PNG reproduzierbar: ohne date/time-Chunks, 8 Bit je Kanal (gleiche Pixel -> gleiche Bytes)."""
    subprocess.run(im()+[path,'-define','png:exclude-chunks=date,time','-depth','8',path],check=True)

if __name__=='__main__':
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':int(sys.argv[3]),'height':int(sys.argv[4])})
        pg.goto('file://'+sys.argv[1]);pg.wait_for_timeout(300);pg.screenshot(path=sys.argv[2]);b.close()
    png_clean(sys.argv[2])
