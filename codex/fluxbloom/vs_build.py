#!/usr/bin/env python3
"""Mac heavy_lock entry point for Part D probes, series and evidence."""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from PIL import Image,ImageDraw,ImageOps
import build
from measure_style_probes import measure,OWN_BOX

HERE=Path(__file__).resolve().parent
CACHE=Path.home()/'Library/Caches/CubeEscapeDesign/vs-reference/out'
BASELINE=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract/full'
PROBES={'parallax':('pistol','sniper','rocket'),'fluxbloom':('sniper','trace')}


def metric_selftest():
    """Exercise the read-only metric CLI with positive and negative pixels."""
    records=[]
    for valid in (True,False):
        im=Image.new('RGB',(1000,600),'#0e1622');draw=ImageDraw.Draw(im)
        draw.rectangle((100,180,899,419),fill='#d5ccB8',outline='#000000' if valid else '#d5ccb8',width=5)
        if valid:
            for x in (300,500,700):draw.rectangle((x,185,x+17,414),fill='#000000')
        path=CACHE/f'metric-selftest-{valid}.png';im.save(path)
        row=measure(path,(0,0,1000,600),f'selftest-{valid}')
        accepted=.72<=row['breite']<=.85 and row['rand_dunkel']>=.4 and row['innenlinien']>=.05
        assert accepted==valid,row
        records.append(dict(expected_pass=valid,**row))
    (CACHE/'metric-selftest.json').write_text(json.dumps(records,indent=2)+'\n')


def contacts(stage):
    entries=[];full=[]
    for family,letter in (('parallax','A'),('fluxbloom','K')):
        output=HERE.parent/family/('output' if stage=='full' else 'output/sight-probe')
        manifest=json.loads((output/'manifest.json').read_text())
        for row in manifest['records']:
            sid=Path(row['filename']).stem
            shot=CACHE/stage/family/(sid+'.png')
            full.append((sid,shot))
            if not sid.endswith('10'):
                x,y,w,h=row['panel_viewports']['optic']
                entries.append((sid,shot,(x,y,x+w,y+h)))
    canvas=Image.new('RGB',(1800,((len(entries)+2)//3)*520),'#0e1622');draw=ImageDraw.Draw(canvas)
    for i,(sid,path,box) in enumerate(entries):
        x=i%3*600;y=i//3*520
        with Image.open(path) as im:crop=ImageOps.contain(im.crop(box).convert('RGB'),(580,475))
        canvas.paste(crop,(x+(600-crop.width)//2,y+35));draw.text((x+15,y+10),sid,fill='#ECE6DA')
    canvas.save(CACHE/f'{stage}-sight-fields.jpg',quality=92)
    if stage=='probe':
        canvas=Image.new('RGB',(2400,1480),'#0e1622');draw=ImageDraw.Draw(canvas)
        for i,(sid,path) in enumerate(full):
            x=i%3*800;y=i//3*740
            with Image.open(path) as im:crop=ImageOps.contain(im.convert('RGB'),(780,700))
            canvas.paste(crop,(x+(800-crop.width)//2,y+30));draw.text((x+15,y+8),sid,fill='#ECE6DA')
        canvas.save(CACHE/'probe-sheets.jpg',quality=90)


def metrics(stage):
    rows=[]
    for family,letter in (('parallax','A'),('fluxbloom','K')):
        output=HERE.parent/family/('output' if stage=='full' else 'output/sight-probe')
        manifest=json.loads((output/'manifest.json').read_text())
        for row in manifest['records']:
            sid=Path(row['filename']).stem
            for phase,path in (('before',BASELINE/family/(sid+'.png')),('after',CACHE/stage/family/(sid+'.png'))):
                rows.append(dict(stage=phase,**measure(path,OWN_BOX,sid)))
    groups={}
    for phase in ('before','after'):
        for letter in ('A','K'):
            selected=[r for r in rows if r['stage']==phase and r['id'].startswith('K'+letter)]
            groups[f'{phase}-{letter}']={'n':len(selected),**{key:float(np.median([r[key] for r in selected])) for key in ('breite','rand_dunkel','innenlinien')}}
    for letter in ('A','K'):
        group=groups['after-'+letter]
        assert .72<=group['breite']<=.85,group
        assert group['rand_dunkel']>=.40,group
        assert group['innenlinien']>=.05,group
    (CACHE/f'{stage}-metrics.json').write_text(json.dumps({'groups':groups,'records':rows},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(groups),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true')
    parser.add_argument('--capture-engine',choices=('playwright','rsvg'),default='playwright');args=parser.parse_args()
    start=time.monotonic();stage='full' if args.full else 'probe'
    CACHE.mkdir(parents=True,exist_ok=True)
    metric_selftest()
    for family in ('parallax','fluxbloom'):
        command=['--collection',family,'--screenshots',str(CACHE/stage/family),'--capture-engine',args.capture_engine]
        if not args.full:
            command+=['--output',str(HERE.parent/family/'output/sight-probe')]
            for slug in PROBES[family]:command+=['--weapon',slug]
        build.main(command)
    contacts(stage);metrics(stage)
    if args.full:
        import viewer
        viewer.main(complete=True)
    (CACHE/f'{stage}-timing.json').write_text(json.dumps({'seconds':time.monotonic()-start,'stage':stage})+'\n')
    print(f'{stage}: {time.monotonic()-start:.2f} seconds; {CACHE}',flush=True)

if __name__=='__main__':main()
