#!/usr/bin/env python3
"""Four user-approved style probe targets; run on the Mac under heavy_lock.

No series rollout. Canonical specs are exported separately without image work.
"""
import json
from pathlib import Path
import time
import sys
from build import geometry_hash, validate_model, screenshots, contact_sheet
from collections_codex import load_collection
from sheet import build_sheet

HERE=Path(__file__).resolve().parent
CACHE=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract'
TARGETS={'parallax':('pistol','sniper'),'fluxbloom':('sniper','trace')}


def main():
    started=time.monotonic()
    for family,slugs in TARGETS.items():
        output=HERE.parent/family/'style-probe'
        shot_dir=CACHE/family
        paths=[];records=[]
        for n,(meta,model) in enumerate(load_collection(family),1):
            if meta['slug'] not in slugs:continue
            validate_model(meta,model)
            record=build_sheet(meta,model,output,n)
            record.update(slug=meta['slug'],geometry_sha256=geometry_hash(model))
            records.append(record);paths.append(output/record['filename'])
        qa=screenshots(paths,shot_dir)
        contact_sheet(paths,shot_dir)
        (output/'manifest.json').write_text(json.dumps({'stage':'style-probe','records':records,'browser_qa':qa},ensure_ascii=False,indent=2)+'\n')
        cards=[]
        for record in records:
            stem=Path(record['filename']).stem
            preview=shot_dir/f'{stem}-preview.jpg'
            cards.append(f'<a href="{record["filename"]}"><img src="{preview.as_uri()}" alt="{stem}"><p>{stem}</p></a>')
        (output/'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><title>Stilvertrag · Probe</title><style>body{background:#0e1622;color:#eee;font:20px sans-serif;margin:35px}main{display:grid;grid-template-columns:1fr 1fr;gap:25px}img{width:100%}a{color:#b4d8fc}</style><h1>Stilvertrag · '+family+'</h1><p>Vier Proben vor der Freigabe zur Serienausarbeitung.</p><main>'+''.join(cards)+'</main>')
    print(f'Vier Probeblätter: {time.monotonic()-started:.2f} s; {CACHE}',flush=True)


if __name__=='__main__':
    main()
    if '--measure' in sys.argv:
        from measure_style_probes import main as measure
        measure()
