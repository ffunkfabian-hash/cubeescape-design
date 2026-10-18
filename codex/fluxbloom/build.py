#!/usr/bin/env python3
"""Build reproducible weapon concept sheets and inspect their browser layout."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / 'Library/Caches/CubeEscapeDesign/concept-sheets/fluxbloom-0.2.0'


def validate_model(meta, model):
    required = {'Gehäuse', 'Griff', 'Abzug', 'Bügel', 'Magazin', 'Lauf', 'Mündung', 'Schaft', 'Visierschiene'}
    present = {p.label for p in model if not p.sight}
    missing = required - present
    if missing:
        raise ValueError(f"{meta['slug']}: missing labels {sorted(missing)}")
    if not any(p.sight for p in model):
        raise ValueError(f"{meta['slug']}: missing separate optic")
    for part in model:
        if not part.faces:
            raise ValueError(f"{meta['slug']}: empty part {part.label}")
        for face in part.faces:
            v = np.asarray(face.vertices)
            n = np.asarray(face.normal)
            if len(v) < 3 or not np.isfinite(v).all() or not np.isfinite(n).all():
                raise ValueError(f"{meta['slug']}: invalid face")
            if np.linalg.norm(n) < 0.99:
                raise ValueError(f"{meta['slug']}: invalid normal")
    return {'part_count': len(model), 'face_count': sum(len(p.faces) for p in model),
            'labels': sorted(present), 'optic_parts': sum(p.sight for p in model)}


def geometry_hash(model):
    digest = hashlib.sha256()
    for p in model:
        digest.update(p.label.encode())
        digest.update(str(p.sight).encode())
        for f in p.faces:
            digest.update(np.asarray(f.vertices, dtype='<f8').tobytes())
    return digest.hexdigest()


def capture_record(output, path, current_hash):
    """Retain the rendered sheet's provenance; never relabel old pixels."""
    manifest=json.loads((output/'manifest.json').read_text(encoding='utf-8'))
    record=next((row for row in manifest['records'] if row.get('filename')==path.name),None)
    if record is None or not path.is_file():
        raise ValueError(f'{path.name}: existing sheet and manifest record required for --capture-only')
    if record.get('geometry_sha256')!=current_hash:
        raise ValueError(f'{path.name}: geometry changed; rebuild instead of --capture-only')
    return record


def screenshots(paths, target):
    """Use installed Chromium; fail visibly rather than silently skipping browser QA."""
    from playwright.sync_api import sync_playwright
    target.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 4800, 'height': 4432}, device_scale_factor=1)
        for path in paths:
            errors = []
            def on_error(error):
                errors.append(str(error))
            page.on('pageerror', on_error)
            page.goto(path.resolve().as_uri(), wait_until='load')
            page.evaluate('document.fonts.ready')
            page.evaluate('Promise.all([...document.images].map(i=>i.decode()))')
            metrics = page.evaluate('''() => ({width:document.documentElement.scrollWidth,
                height:document.documentElement.scrollHeight, fonts:document.fonts.status,
                svgImages:document.querySelectorAll('svg image').length,
                overflow:[...document.querySelectorAll('svg text')].filter(e=>{const b=e.getBoundingClientRect(); return b.left<0 || b.top<0 || b.right>4800 || b.bottom>4432}).map(e=>e.textContent.slice(0,100))})''')
            if errors or metrics['width'] != 4800 or metrics['height'] != 4432 or metrics['overflow']:
                raise RuntimeError(f'{path.name}: browser QA failed {errors} {metrics}')
            filename = target / f'{path.stem}.png'
            page.screenshot(path=str(filename), full_page=True, animations='disabled')
            with Image.open(filename) as image:
                image.thumbnail((1600, 1478))
                image.save(target / f'{path.stem}-preview.jpg', quality=91)
            page.remove_listener('pageerror', on_error)
            results.append({'file': path.name, 'screenshot': str(filename), 'metrics': metrics})
            print(f'Screenshot: {filename}', flush=True)
        browser.close()
    return results


def svg_captures(paths,target):
    """Explicit librsvg fallback for Mac sessions that cannot launch Chromium.

    These are sheet renders, never labelled as browser-layout validation.
    Local Fontconfig uses the same three bundled, licensed font files.
    """
    import os,re,subprocess
    target.mkdir(parents=True,exist_ok=True)
    from xml.sax.saxutils import escape
    fontconfig=target/'fonts.conf'
    fontconfig.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>'+escape(str(HERE/'fonts'))+'</dir><cachedir>'+escape(str(target/'font-cache'))+'</cachedir></fontconfig>')
    env={**os.environ,'FONTCONFIG_FILE':str(fontconfig)}
    records=[]
    for path in paths:
        document=path.read_text();svg=re.search(r'(<svg\b.*?</svg>)',document,re.S).group(1)
        css='.title{font-family:"Chakra Petch"}.body{font-family:Barlow}.mono{font-family:"JetBrains Mono"}'
        svg=svg.replace('>', '><style>'+css+'</style>',1)
        source=target/(path.stem+'.svg');source.write_text(svg)
        filename=target/(path.stem+'.png')
        subprocess.run(['rsvg-convert','--output',str(filename),str(source)],env=env,check=True)
        with Image.open(filename) as image:
            assert image.size==(4800,4432)
            image.thumbnail((1600,1478));image.save(target/(path.stem+'-preview.jpg'),quality=91)
        source.unlink()  # transient extraction generated by this call only
        records.append({'file':path.name,'screenshot':str(filename),'metrics':{'width':4800,'height':4432,
            'capture_engine':'librsvg','browser_layout_validated':False,'fonts':'bundled Fontconfig families'}})
        print(f'SVG-Aufnahme (Browser-QA offen): {filename}',flush=True)
    return records


def contact_sheet(paths, target):
    canvas = Image.new('RGB', (1600, 5 * 790), '#0e1622')
    draw = ImageDraw.Draw(canvas)
    for i, path in enumerate(paths):
        with Image.open(target / f'{path.stem}.png') as image:
            image.thumbnail((790, 745))
            x, y = (i % 2) * 800, (i // 2) * 790
            canvas.paste(image, (x, y + 30))
            draw.text((x + 16, y + 8), path.stem, fill='#ECE6DA')
    canvas.crop((0, 0, 1600, ((len(paths) + 1) // 2) * 790)).save(target / 'contact-sheet.jpg', quality=92)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--collection', choices=('fluxbloom','parallax'), default='fluxbloom')
    parser.add_argument('--probe', action='store_true', help='Build representative sheets for visual approval before rollout')
    parser.add_argument('--screenshots', type=Path)
    parser.add_argument('--weapon', action='append', help='Slug; repeat to select multiple weapons')
    parser.add_argument('--capture-only', action='store_true', help='Inspect existing HTML without rerendering geometry')
    parser.add_argument('--capture-engine',choices=('playwright','rsvg'),default='playwright')
    parser.add_argument('--spec-only', action='store_true', help='Export canonical weapon specs without rendering sheets')
    args = parser.parse_args(argv)
    from collections_codex import load_collection, PROBE_SLUGS
    from sheet import build_sheet
    started = time.monotonic()
    models = load_collection(args.collection)
    collection_root=HERE if args.collection=='fluxbloom' else HERE.parent/'parallax'
    args.output=args.output or (collection_root/'output' if args.spec_only else collection_root/('probe' if args.probe else 'output'))
    args.screenshots=args.screenshots or Path.home()/f'Library/Caches/CubeEscapeDesign/concept-sheets/{args.collection}-upgrade-{"probe" if args.probe else "full"}'
    if args.probe and not args.weapon:args.weapon=list(PROBE_SLUGS)
    selected = [(n, meta, model) for n, (meta, model) in enumerate(models, 1)
                if not args.weapon or meta['slug'] in args.weapon]
    if not selected or (args.weapon and set(args.weapon) - {m['slug'] for _, m, _ in selected}):
        parser.error('Unknown or empty weapon selection')
    args.output.mkdir(parents=True, exist_ok=True)
    if args.spec_only:
        from weapon_spec import make_spec, dump
        for number, meta, model in selected:
            sheet_id=f"K{meta['variant']}{number:02d}"
            record={'geometry_sha256':geometry_hash(model),'orthographic_views':[]}
            canonical=make_spec(meta,model,number,record)
            target=args.output/f'{sheet_id}.spec.json'
            target.write_text(dump(canonical),encoding='utf-8')
        print(f"Fertig: {len(selected)} kanonische Specs unter {args.output}; keine Bilder erzeugt.",flush=True)
        return 0
    records, paths = [], []
    for number, meta, model in selected:
        checks = validate_model(meta, model)
        sheet_id = f"K{meta['variant']}{number:02d}"
        path = args.output / (sheet_id + '.html')
        if not args.capture_only:
            print(f"Baue {meta['name']} ({len(model)} Teile)", flush=True)
            record = build_sheet(meta, model, args.output, number)
        else:
            record = capture_record(args.output, path, geometry_hash(model))
        record['geometry_sha256'] = geometry_hash(model)
        if not args.capture_only:
            (args.output / (sheet_id + '-prompts.txt')).write_text('DEUTSCH\n' + record['prompts']['de'] + '\n\nENGLISH\n' + record['prompts']['en'] + '\n', encoding='utf-8')
        if not args.capture_only:
            from spec import design_spec
            from weapon_spec import make_spec, dump
            (args.output / (sheet_id + '.reference.json')).write_text(json.dumps(design_spec(meta, model, number, record), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
            (args.output / (sheet_id + '.spec.json')).write_text(dump(make_spec(meta, model, number, record)), encoding='utf-8')
        records.append({**record, 'slug': meta['slug'], 'geometry_sha256': geometry_hash(model), 'geometry_checks': checks})
        paths.append(path)
    captures = (screenshots if args.capture_engine=='playwright' else svg_captures)(paths, args.screenshots)
    contact_sheet(paths, args.screenshots)
    if args.capture_only:
        qa={'browser_qa':captures,'seconds':round(time.monotonic()-started,2),
            'source':'Existing HTML and manifest; no rebuild or provenance update.'}
        (args.output/'capture-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'Fertig: {len(paths)} vorhandene Blätter erneut aufgenommen; Manifest unverändert.',flush=True)
        return 0
    previews = args.output / 'previews'
    previews.mkdir(exist_ok=True)
    cards = []
    for (_, meta, _), path in zip(selected, paths):
        with Image.open(args.screenshots / (path.stem + '-preview.jpg')) as preview:
            preview.save(previews / (path.stem + '.jpg'), quality=88)
        cards.append(f'<a href="{html.escape(path.name)}"><img src="previews/{path.stem}.jpg" alt="{html.escape(meta["kind"])}"><span>{path.stem} · {html.escape(meta["name"])} / {html.escape(meta["kind"])}</span></a>')
    gallery_title=f"Codex · {models[0][0]['variant_name']} · {'Probeblätter' if args.probe else 'Konzeptblätter'}"
    (args.output / 'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><title>'+html.escape(gallery_title)+'</title><style>body{background:#0e1622;color:#ece6da;font:20px sans-serif;padding:40px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}a{color:#e1d2ff;text-decoration:none}img{width:100%;display:block;border-radius:8px}span{display:block;padding:16px}p{max-width:900px;line-height:1.5}</style><h1>'+html.escape(gallery_title)+'</h1><p>Überarbeitete Waffenformen · kräftige Farbwelten · ein 3D-Modell je Blatt · sechs orthografische Ansichten im selben Maßstab. Gestalterische Referenzen.</p><main>'+''.join(cards)+'</main></html>', encoding='utf-8')
    manifest = {'version': '0.2.3' if args.collection=='fluxbloom' else '0.1.3', 'name': models[0][0]['variant_name'], 'stage': 'probe' if args.probe else 'full', 'canvas': [4800, 4432],
                'records': records, 'browser_qa': captures, 'seconds': round(time.monotonic()-started, 2),
                'visual_review': 'Manuelle Sichtprüfung der Screenshots erforderlich; automatische Prüfungen ersetzen sie nicht.'}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"Fertig: {len(paths)} Blätter, {manifest['seconds']} s; {args.output / 'index.html'}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
