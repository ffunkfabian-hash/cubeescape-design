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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('parallax','fluxbloom','both'), default='both')
    parser.add_argument('--existing', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    for family in (('parallax','fluxbloom') if args.family == 'both' else (args.family,)):
        target = CACHE/('existing' if args.existing else 'full')/family
        command = ['--collection', family, '--screenshots', str(target)]
        if args.existing:
            for slug in OLD: command += ['--weapon', slug]
        build.main(command)
        manifest = json.loads((HERE.parent/family/'output/manifest.json').read_text())
        rows, unchanged, tiles = [], {}, 0
        for record in manifest['records']:
            sid = Path(record['filename']).stem
            shot = target/(sid+'.png')
            rows.append(measure(shot, OWN_BOX, sid))
            tiles += profile_text_bounds((HERE.parent/family/'output'/record['filename']).read_text())
            if args.existing:
                with Image.open(shot) as current, Image.open(BASELINE/family/(sid+'.png')) as old:
                    a = np.asarray(current.crop((0,0,4800,4432)).convert('RGB'))
                    b = np.asarray(old.convert('RGB'))
                    count = int(np.any(a != b, axis=2).sum())
                    unchanged[sid] = dict(changed_pixels=count, baseline=str(BASELINE/family/(sid+'.png')))
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
                      profile_glyphs_checked=tiles,seconds=round(time.monotonic()-started,2))
        (target/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','unchanged_original_canvas')}),flush=True)
    from viewer import main as viewer
    viewer(complete=True)


if __name__ == '__main__': main()
