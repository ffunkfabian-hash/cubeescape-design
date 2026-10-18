#!/usr/bin/env python3
"""Mac heavy_lock entry: texturprofil plates, contacts, metrics and hashes.

Default: two layout probes. --full refreshes both complete local galleries,
including the two unchanged bows. Generated evidence stays outside the repo.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import re
import xml.etree.ElementTree as ET

import numpy as np
import jsonschema
from PIL import Image, ImageDraw, ImageOps, ImageFont
import build
from measure_style_probes import measure, OWN_BOX
from texture_profile import profile
import viewer

HERE = Path(__file__).resolve().parent
CACHE = Path.home()/'Library/Caches/CubeEscapeDesign/codex-texturprofil'
BASELINE = Path.home()/'Library/Caches/CubeEscapeDesign/vs-reference/out/full'
DATA = HERE/'tests/data/texture-profile-validation.json'


def profile_text_bounds(document):
    """Check glyph extents against each tile with the bundled font metrics.

    This complements the SVG capture when Chromium is unavailable; it never
    claims a browser layout check. Coordinates are local to each tile group.
    """
    root = ET.fromstring(re.search(r'(<svg\b.*?</svg>)',document,re.S).group(1))
    ns = {'s':'http://www.w3.org/2000/svg'}
    fonts = dict(title='ChakraPetch-Regular.ttf', body='Barlow-Regular.ttf', mono='JetBrainsMono-Regular.ttf')
    checked = 0
    for tile in root.findall('.//s:g[@data-profile-tile]',ns):
        rect = tile.find('s:rect',ns)
        w,h = float(rect.attrib['width']),float(rect.attrib['height'])
        for text in tile.findall('s:text',ns):
            font = ImageFont.truetype(str(HERE/'fonts'/fonts[text.attrib['class']]),int(text.attrib['font-size']))
            l,t,r,b = font.getbbox(text.text,anchor='ls')
            x,y = float(text.attrib['x']),float(text.attrib['y'])
            assert x+l>=0 and y+t>=0 and x+r<=w and y+b<=h, (tile.attrib['data-profile-tile'],text.text,(x+l,y+t,x+r,y+b),(w,h))
            checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--capture-engine', choices=('playwright','rsvg'), default='playwright')
    parser.add_argument('--reuse-existing', action='store_true', help='Resume evidence collection from complete current galleries')
    args = parser.parse_args()
    started = time.monotonic()
    stage = 'full' if args.full else 'probe'
    profiles, material_fields, rows, summaries = [], [], [], {}
    text_bounds_checked = 0
    unchanged_regions = {}
    cached_pixel_differences = {}
    schemas = [jsonschema.Draft202012Validator(json.loads(p.read_text())) for p in
               (HERE/'weapon-spec.schema.json',HERE.parents[1]/'claude/docs/weapon-spec.schema.json')]
    for family, letter in (('parallax','A'), ('fluxbloom','K')):
        target = CACHE/stage/family
        output = HERE.parent/family/('output' if args.full else 'output/texture-profile-probe')
        options = ['--collection',family,'--output',str(output),'--screenshots',str(target),
                   '--capture-engine',args.capture_engine]
        if not args.full:
            options += ['--weapon','pistol' if family == 'parallax' else 'rocket']
        if args.reuse_existing and (output/'manifest.json').exists():
            existing = json.loads((output/'manifest.json').read_text())
            assert existing['version'] == ('0.1.5' if family=='parallax' else '0.2.5')
            assert len(existing['records']) == (10 if args.full else 1)
            expected_engine = 'librsvg' if args.capture_engine=='rsvg' else 'playwright'
            assert len(existing['browser_qa']) == len(existing['records'])
            assert all(q['metrics'].get('capture_engine','playwright')==expected_engine
                       for q in existing['browser_qa']), 'Reuse requires the same capture engine; rebuild for Chromium QA'
            assert all((target/(Path(r['filename']).stem+'.png')).exists() for r in existing['records'])
            assert all((r.get('texture_profile') is not None) == (r['number']!=10) for r in existing['records'])
            print(f'{family}: aktuelle vollständige Galerie weiterverwenden',flush=True)
        else:
            build.main(options)
        manifest = json.loads((output/'manifest.json').read_text())
        summaries[family] = dict(seconds=manifest['seconds'], sheets=len(manifest['records']))
        for record in manifest['records']:
            sid = Path(record['filename']).stem
            sp = json.loads((output/(sid+'.spec.json')).read_text())
            for schema in schemas:
                schema.validate(sp)
            previous_spec = json.loads(subprocess.check_output(['git','show',f'25f108f:codex/{family}/output/{sid}.spec.json'],cwd=HERE.parents[1]))
            unchanged = {k:v for k,v in sp.items() if k!='texture_profile'}
            unchanged['generator'] = previous_spec['generator']
            assert unchanged==previous_spec,(sid,'pre-existing Spec fields changed')
            assert sp.get('texture_profile') == record.get('texture_profile') == profile(sp['weapon']['toolgen_id']),sid
            text_bounds_checked += profile_text_bounds((output/record['filename']).read_text())
            shot = target/(sid+'.png')
            rows.append(measure(shot, OWN_BOX, sid))
            with Image.open(shot) as image:
                previous = BASELINE/family/(sid+'.png')
                if previous.exists():
                    with Image.open(previous) as old:
                        regions = {'whole_bow':(0,0,4800,4432)} if sid.endswith('10') else {
                            name:(x,y,x+w,y+h) for name,(x,y,w,h) in record['panel_viewports'].items() if name!='material'}
                        matches = []
                        changed = {}
                        for name,box in regions.items():
                            diff = np.any(np.asarray(image.crop(box).convert('RGB'))!=np.asarray(old.crop(box).convert('RGB')),axis=2)
                            if diff.any():
                                changed[name] = int(diff.sum())
                            else:
                                matches.append(name)
                        unchanged_regions[sid] = matches
                        cached_pixel_differences[sid] = changed
                if 'texture_profile_viewport' in record:
                    x,y,w,h = record['texture_profile_viewport']
                    profiles.append((sid,image.crop((x,y,x+w,y+h)).convert('RGB')))
                    x,y,w,h = record['panel_viewports']['material']
                    material_fields.append((sid,image.crop((x,y,x+w,y+h)).convert('RGB')))
        if args.full:
            subset = [r for r in rows if r['id'].startswith('K'+letter)]
            median = {key:float(np.median([r[key] for r in subset]))
                      for key in ('breite','rand_dunkel','innenlinien')}
            expected = dict(breite=.77,rand_dunkel=.53,innenlinien=.078) if letter=='A' else dict(breite=.75,rand_dunkel=.52,innenlinien=.069)
            assert all(abs(median[k]-v)<1e-9 for k,v in expected.items()), (family,median)
            summaries[family]['median'] = median
    for label, entries, cell in (('profiles',profiles,(630,345)), ('materials',material_fields,(630,930))):
        canvas = Image.new('RGB',(cell[0]*3,((len(entries)+2)//3)*cell[1]),'#0E1622')
        draw = ImageDraw.Draw(canvas)
        for i,(sid,image) in enumerate(entries):
            x,y = i%3*cell[0],i//3*cell[1]
            crop = ImageOps.contain(image,(cell[0]-20,cell[1]-36))
            canvas.paste(crop,(x+10,y+30))
            draw.text((x+12,y+8),sid,fill='#ECE6DA')
        canvas.save(CACHE/(stage+'-'+label+'.jpg'),quality=94)
    if args.full:
        assert len(profiles)==18 and len(rows)==20
        viewer.main(complete=True)
        # Invoke the official read-only checks in their own interpreter so module
        # names cannot collide with the independent Codex pipeline.
        code = '''import json,sys
from pathlib import Path
sys.path.insert(0,'claude/generator')
import spec_checks as checks
out={}
for family in ('parallax','fluxbloom'):
    for path in sorted(Path('codex',family,'output').glob('K???.spec.json')):
        sp=json.loads(path.read_text())
        out[sp['sheet']['id']]={'direction':checks.direction_problems(sp),'vs':checks.vs_problems(sp),
            'window':checks.window_problems((sp['sight'].get('window_geometry') or {}).get('elements',[]),
                {p['id']:p for p in sp['parts']},sp['decals'],hand_z=sp['anchors']['Socket_Hand']['position_m'][2])}
assert len(out)==20,len(out)
assert not any(v for row in out.values() for v in row.values()),out
print(json.dumps(out))'''
        result = subprocess.run([sys.executable,'-B','-c',code],cwd=HERE.parents[1],capture_output=True,text=True,check=True)
        spec_checks = json.loads(result.stdout)
        for family in ('parallax','fluxbloom'):
            output = HERE.parent/family/'output'
            assert len(list((output/'previews').glob('K???.jpg')))==10
            assert (output/'index.html').read_text().count('<a href=')==10
        evidence = dict(base='25f108f',capture_engine=args.capture_engine,
                        browser_layout_validated=args.capture_engine=='playwright',collections=summaries,
                        spec_checks=spec_checks,style_metrics=rows,
                        profiles=18,bows_without_profile=2,profile_text_bounds_checked=text_bounds_checked,
                        unchanged_pixel_regions=unchanged_regions,
                        cached_pixel_differences=cached_pixel_differences,
                        cached_pixel_note='Historical-session PNG differences are diagnostic; use unchanged source/Spec checks and the separately recorded same-environment baseline countercheck to distinguish capture differences from model edits.',
                        schema_validations=40,previous_spec_fields_unchanged=20,
                        seconds=round(time.monotonic()-started,2))
        countercheck = CACHE/'baseline-check/validation.json'
        if countercheck.exists():
            evidence['fresh_baseline_countercheck'] = json.loads(countercheck.read_text())
        DATA.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(summaries),flush=True)
    print(f'{stage}: {time.monotonic()-started:.2f} s; {CACHE}',flush=True)


if __name__ == '__main__':
    main()
