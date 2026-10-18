#!/usr/bin/env python3
"""Run Claude's read-only CLI metric and assemble requested probe evidence.

Execute on macOS under heavy_lock. No Claude source is imported or copied.
The CLI rounds its output: results retain that fact rather than invent precision.
"""
import json
from pathlib import Path
import re
import subprocess
import sys
from PIL import Image, ImageDraw, ImageOps
from build import screenshots

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CACHE=Path.home()/'Library/Caches/CubeEscapeDesign'
OUT=CACHE/'style-contract'
TOOL=ROOT/'claude/generator/style_metrics.py'
OWN_BOX=(150,560,2910,2120)
REF_BOX=(100,330,2760,2080)
IDS=('KA01','KA05','KK05','KK08')


def measure(path,box,label):
    result=subprocess.run([sys.executable,str(TOOL),str(path),*(str(v) for v in box),label],check=True,text=True,capture_output=True)
    text=result.stdout.strip()
    found=re.search(r'Breite (\d+)% Höhe (\d+)% \| Rand dunkel (\d+)% \| Innenlinien ([\d.]+)% \| Sättigung (\d+)',text)
    if not found:raise ValueError(text)
    values=list(map(float,found.groups()))
    print(text,flush=True)
    return {'id':label,'file':str(path),'box':box,'breite':values[0]/100,'hoehe':values[1]/100,
            'rand_dunkel':values[2]/100,'innenlinien':values[3]/100,'saettigung':values[4],
            'raw_cli':text,'cli_rounding':'Width/height/border/saturation rounded to integer; interior lines to 0.1%. No extra precision claimed.'}


def main():
    import numpy as np
    OUT.mkdir(parents=True,exist_ok=True)
    reference_dir=CACHE/'comparison/claude-v0.3/sheets'
    reference_html=[reference_dir/f'{sid}.dc.html' for sid in ('KF05','KG07')]
    reference_shots=OUT/'references'
    screenshots(reference_html,reference_shots)
    records=[]
    for family,letter in (('parallax','A'),('fluxbloom','K')):
        for number in range(1,11):
            sid=f'K{letter}{number:02d}'
            records.append({'stage':'before',**measure(CACHE/f'concept-sheets/{family}-upgrade-full/{sid}.png',OWN_BOX,sid)})
    for sid in IDS:
        family='parallax' if sid.startswith('KA') else 'fluxbloom'
        records.append({'stage':'probe',**measure(OUT/f'{family}/{sid}.png',OWN_BOX,sid)})
    if '--full' in sys.argv:
        for family,letter in (('parallax','A'),('fluxbloom','K')):
            for number in range(1,11):
                sid=f'K{letter}{number:02d}'
                records.append({'stage':'after',**measure(OUT/f'full/{family}/{sid}.png',OWN_BOX,sid)})
    for sid in ('KF05','KG07'):
        records.append({'stage':'reference',**measure(reference_shots/f'{sid}.dc.png',REF_BOX,sid)})
    groups={}
    for stage in (('before','probe','after') if '--full' in sys.argv else ('before','probe')):
        for letter in ('A','K'):
            subset=[r for r in records if r['stage']==stage and r['id'].startswith('K'+letter)]
            groups[f'{stage}-{letter}']={'n':len(subset),**{key:float(np.median([r[key] for r in subset])) for key in ('breite','hoehe','rand_dunkel','innenlinien','saettigung')}}
    (OUT/'metrics.json').write_text(json.dumps({'tool':'claude/generator/style_metrics.py','base':'7f88136','groups':groups,'records':records},ensure_ascii=False,indent=2)+'\n')
    # Six current hero crops: four Codex probes and the two requested Claude refs.
    canvas=Image.new('RGB',(2400,1260),'#0e1622');draw=ImageDraw.Draw(canvas)
    chosen=[r for r in records if r['stage'] in ('probe','reference')]
    links=[]
    for index,row in enumerate(chosen):
        x=(index%3)*800;y=(index//3)*630
        with Image.open(row['file']) as im:
            display_box=(140,530,2920,2200) if row['stage']=='probe' else row['box']
            crop=ImageOps.contain(im.crop(display_box).convert('RGB'),(780,570))
            canvas.paste(crop,(x+(800-crop.width)//2,y+45+(570-crop.height)//2))
        draw.text((x+15,y+15),row['id']+' / '+row['stage'],fill='#ece6da')
        links.append(f'<a href="{Path(row["file"]).as_uri()}">{row["id"]} vollständig</a>')
    canvas.save(OUT/'contact-heroes.jpg',quality=92)
    (OUT/'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><title>Stilvertrag · Freigabeprobe</title><style>body{background:#0e1622;color:#ece6da;font:20px system-ui;margin:30px;line-height:1.5}img{max-width:100%;width:2400px}a{color:#b4d8fc}</style><h1>Stilvertrag · vier Probeblätter</h1><p>KA01, KA05, KK05, KK08 · darunter/ daneben Claude KF05 und KG07 aus Release v0.3. Modelle, Paletten und Skin-Arten unverändert. Die Stilproben wurden vom Nutzer freigegeben; aktuelle Katalogproben werden hier neben den Referenzen geprüft.</p><a href="contact-heroes.jpg"><img src="contact-heroes.jpg" alt="Vier Proben und zwei Claude-Referenzen"></a><p>'+' · '.join(links)+'</p><p><a href="metrics.json">Messwerte und verwendete Felder</a> · <a href="catalog-materials.jpg">Materialfelder neben Katalog-Musterbildern</a></p>')
    print(json.dumps(groups,ensure_ascii=False),flush=True)
    print(OUT/'index.html',flush=True)


if __name__=='__main__':main()
