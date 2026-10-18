"""Stilmaße eines gerenderten Konzeptblatts (PNG in voller Größe) für den Abgleich Claude/Codex.

Misst im angegebenen Feld das größte Objekt vor dem Feldhintergrund:
  Breite/Höhe  Ausdehnung des Objekts relativ zum Feld (Füllgrad)
  Rand dunkel  Anteil des 3-px-Objektrands mit Kontur (max(R,G,B) < 30)
  Innenlinien  Anteil dunkler Konturpixel im Inneren (Kanten zwischen Flächen)
  Sättigung    mittleres max−min der Kanäle im Inneren
Grundlage des Stilvertrags in claude/docs/auftrag-codex-angleichung.md (Messung 17.10.2026).

  python3 style_metrics.py BLATT.png x0 y0 x1 y1 [Bezeichnung]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

def measure(path,box):
    im=np.asarray(Image.open(path).convert('RGB')).astype(np.int16)
    x0,y0,x1,y1=box;r=im[y0:y1,x0:x1]
    bg=np.median(r.reshape(-1,3),0)
    fg=np.abs(r-bg).sum(2)>40
    lab,n=ndimage.label(ndimage.binary_closing(fg,iterations=3))
    if n==0:return None
    k=int(np.argmax(ndimage.sum(fg,lab,range(1,n+1))))+1
    obj=ndimage.binary_fill_holes(lab==k)
    ys,xs=np.nonzero(obj)
    rim=obj&~ndimage.binary_erosion(obj,iterations=3)
    inner=ndimage.binary_erosion(obj,iterations=4)
    dark=r.max(2)<30
    px=r[inner]
    return dict(breite=(xs.max()-xs.min())/(x1-x0),hoehe=(ys.max()-ys.min())/(y1-y0),
                rand_dunkel=(dark&rim).sum()/max(1,rim.sum()),innenlinien=(dark&inner).sum()/max(1,inner.sum()),
                saettigung=float((px.max(1)-px.min(1)).mean()))

if __name__=='__main__':
    a=sys.argv[1:]
    if len(a)<5:sys.exit(__doc__)
    m=measure(a[0],tuple(int(v) for v in a[1:5]))
    if m is None:sys.exit('kein Objekt im Feld')
    print(f"{a[5] if len(a)>5 else a[0]}: Breite {m['breite']:.0%} Höhe {m['hoehe']:.0%} | Rand dunkel {m['rand_dunkel']:.0%} | "
          f"Innenlinien {m['innenlinien']:.1%} | Sättigung {m['saettigung']:.0f}")
