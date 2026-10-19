#!/usr/bin/env python3
"""Switchcraft image evidence. Run on the Mac through heavy_lock.

Existing sheets retain their original 4432px image region. BEDIENUNG is appended;
baseline comparison names every actual changed pixel instead of assuming parity.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import build
from measure_style_probes import measure, OWN_BOX
from texture_profile_build import assert_style_median, profile_text_bounds

HERE = Path(__file__).resolve().parent
CACHE = Path.home()/'Library/Caches/CubeEscapeDesign/switchcraft'
BASELINE = Path.home()/'Library/Caches/CubeEscapeDesign/codex-texturprofil/full'
OLD = ('pistol','assault','impulse','shotgun','sniper','smg','fusion','trace','rocket','bow')


def gallery_qa(count, families=('parallax','fluxbloom')):
    """Decode actual gallery previews and follow its local sheet links."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1600,'height':1000})
        for family in families:
            folder=HERE.parent/family/'output'
            page.goto((folder/'index.html').as_uri(),wait_until='load')
            page.evaluate('Promise.all([...document.images].map(i=>i.decode()))')
            result=page.evaluate('''() => ({images:[...document.images].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth})),
                links:[...document.querySelectorAll('main a')].map(a=>a.getAttribute('href'))})''')
            assert len(result['images'])==len(result['links'])==count,(family,result)
            assert all(r['width']>0 and (folder/r['src']).is_file() for r in result['images'])
            assert all((folder/path).is_file() for path in result['links'])
        page.goto((HERE.parent/'index.html').as_uri(),wait_until='load')
        actual=page.locator('article > p:first-of-type').all_text_contents()
        expected=[]
        for family in ('parallax','fluxbloom'):
            path=HERE.parent/family/'output/manifest.json'
            total=len(json.loads(path.read_text())['records']) if path.exists() else 0
            expected.append(f'{total} lokale Konzeptblätter mit Vorschauen')
        assert actual==expected,(actual,expected)
        browser.close()
    print(f'Galerie-QA: {len(families)} × {count} Vorschauen dekodiert und Blattlinks vorhanden.',flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('parallax','fluxbloom','both'), default='both')
    parser.add_argument('--existing', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    style_failures = []
    for family in (('parallax','fluxbloom') if args.family == 'both' else (args.family,)):
        family_started = time.monotonic()
        target = CACHE/('existing' if args.existing else 'full')/family
        command = ['--collection', family, '--screenshots', str(target)]
        if args.existing:
            command += ['--existing-only']
            for slug in OLD: command += ['--weapon', slug]
        build.main(command)
        manifest = json.loads((HERE.parent/family/'output/manifest.json').read_text())
        # Three readable construction contact sheets, five new concepts each.
        new_records = [r for r in manifest['records'] if r['number'] > 10]
        for start in range(0,len(new_records),5):
            group = new_records[start:start+5]
            canvas = Image.new('RGB',(2400,1120),'#0e1622')
            draw = ImageDraw.Draw(canvas)
            for i,record in enumerate(group):
                sid = Path(record['filename']).stem
                with Image.open(target/(sid+'.png')) as image:
                    tile=ImageOps.contain(image.crop((140,430,2920,2200)).convert('RGB'),(780,520))
                x,y=(i%3)*800,(i//3)*560
                canvas.paste(tile,(x+(800-tile.width)//2,y+32))
                draw.text((x+15,y+8),sid+' / '+record['slug'],fill='#ECE6DA')
            canvas.save(target/f'heroes-{start+11:02d}-{start+10+len(group):02d}.jpg',quality=92)
        rows, unchanged, tiles = [], {}, 0
        for record in manifest['records']:
            sid = Path(record['filename']).stem
            shot = target/(sid+'.png')
            rows.append(measure(shot, OWN_BOX, sid))
            tiles += profile_text_bounds((HERE.parent/family/'output'/record['filename']).read_text())
            if record['number'] <= 10:
                with Image.open(shot) as current, Image.open(BASELINE/family/(sid+'.png')) as old:
                    a = np.asarray(current.crop((0,0,4800,4432)).convert('RGB'))
                    b = np.asarray(old.convert('RGB'))
                    count = int(np.any(a != b, axis=2).sum())
                    unchanged[sid] = dict(changed_pixels=count, baseline=str(BASELINE/family/(sid+'.png')))
                    assert count == 0, (sid, 'Bestehende Bildfläche verändert', count)
            deltas = record.get('operation')
            assert deltas and all(deltas[k]['de'] and deltas[k]['en'] for k in ('reload','action','fire'))
        median = {k:float(np.median([r[k] for r in rows])) for k in ('breite','rand_dunkel','innenlinien')}
        expected = dict(breite=.77,rand_dunkel=.53,innenlinien=.078) if family=='parallax' else dict(breite=.75,rand_dunkel=.52,innenlinien=.069)
        # The historic numeric median is defined over the unchanged original ten.
        old_rows = [r for r in rows if int(r['id'][2:]) <= 10]
        old_median = {k:float(np.median([r[k] for r in old_rows])) for k in expected}
        assert_style_median(family, old_median, expected)
        result = dict(family=family,rows=rows,median_all=median,median_existing=old_median,
                      expected_existing=expected,unchanged_original_canvas=unchanged,
                      profile_glyphs_checked=tiles,seconds=round(time.monotonic()-family_started,2),
                      total_seconds=round(time.monotonic()-started,2))
        if not args.existing:
            try:
                assert_style_median(family, median, expected)
                result['style_pass'] = True
            except AssertionError as error:
                result['style_pass'] = False
                style_failures.append(str(error))
        (target/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','unchanged_original_canvas')}),flush=True)
    if style_failures:
        raise AssertionError('Stilgrenzen verletzt: ' + '; '.join(style_failures))
    from viewer import main as viewer
    viewer(complete=False)
    from spec_hashes import main as hashes
    hashes(include_new=not args.existing)
    count=10 if args.existing else 25
    families=('parallax','fluxbloom') if args.family=='both' else (args.family,)
    gallery_qa(count,families)


if __name__ == '__main__': main()
