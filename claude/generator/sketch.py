"""Schnellskizze eines Blattmodells ohne Blatt (claude-0.11): Isometrie, Seite links, Draufsicht, Vorderansicht als PNG.
   python3 sketch.py KC11 KD14 … [--out DIR]      (Standard: ~/Library/Caches/CubeEscapeDesign/sketch/)
Lädt das Modell wie das Blatt (sheetmodels.load, also mit Visier der Visier-Serie) und rastert mit raster.rasterview, setzt mit PIL zusammen. Gedacht für die Modellprüfung vor dem Vollbau (keine Bildstufe des Blatts, kein heavy_lock nötig). Ohne Kontur-Feinheiten
des Blatts; die Bezeichnungen der Teile stehen als Liste darunter (Teile mit Bezeichnung, Visierteile ausgenommen)."""
import base64,io,os,re,sys
from PIL import Image,ImageDraw,ImageFont
import sheetmodels
from eng import svgview,extent
VIEWS=[('ISOMETRIE',-45,35.264),('SEITE LINKS',0,0),('DRAUFSICHT',0,90),('VORDERANSICHT',-90,0)]
W,H=900,520
FONT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
def sketch(sid,out):
    d=sheetmodels.load(sid);m,c=d['m'],d['center']
    labs=sorted({P['label'] for P in m.parts if P.get('label') and not P.get('sight')})
    lines,line=[],''
    for t in labs:
        if len(line)+len(t)>150:lines.append(line);line=''
        line+=t+' · '
    lines.append(line)
    lines.append(f"{sid} {d['name']} „{d['nick']}“ · {d['pill']} · Teile {len(m.parts)}")
    im=Image.new('RGB',(2*W,2*H+30+28*len(lines)),'#0B111A');dr=ImageDraw.Draw(im)
    for i,(nm,yaw,pitch) in enumerate(VIEWS):
        e1,e2=extent(m,yaw,pitch,c);sc=min((W-60)/max(e1,1),(H-80)/max(e2,1))
        x,y=(i%2)*W,(i//2)*H
        dr.rectangle([x,y,x+W-1,y+H-1],fill='#111A27',outline='#22314A')
        b64=re.search(r'base64,([^"]+)"',svgview(m,yaw,pitch,c,W,H,sc,ow=2.4)).group(1)
        v=Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGBA');im.paste(v,(x,y),v)
        dr.text((x+14,y+10),nm,font=FONT,fill='#8FA0B3')
    for k,l in enumerate(lines):dr.text((14,2*H+14+28*k),l,font=FONT,fill='#F0B060' if k==len(lines)-1 else '#C7D1DC')
    f=os.path.join(out,sid+'.png');im.save(f);print(f)
if __name__=='__main__':
    a=sys.argv[1:];out=os.path.expanduser('~/Library/Caches/CubeEscapeDesign/sketch')
    if '--out' in a:i=a.index('--out');out=a[i+1];del a[i:i+2]
    os.makedirs(out,exist_ok=True)
    for s in a:sketch(s,out)
