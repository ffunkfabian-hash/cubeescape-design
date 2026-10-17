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
CACHE = Path.home() / 'Library/Caches/CubeEscapeDesign/concept-sheets/0.1.0'


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


def screenshots(paths, target):
    """Use installed Chromium; fail visibly rather than silently skipping browser QA."""
    from playwright.sync_api import sync_playwright
    target.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 4800, 'height': 3400}, device_scale_factor=1)
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
                overflow:[...document.querySelectorAll('svg text')].filter(e=>{const b=e.getBoundingClientRect(); return b.left<0 || b.top<0 || b.right>4800 || b.bottom>3400}).map(e=>e.textContent.slice(0,100))})''')
            if errors or metrics['width'] != 4800 or metrics['height'] != 3400 or metrics['overflow']:
                raise RuntimeError(f'{path.name}: browser QA failed {errors} {metrics}')
            filename = target / f'{path.stem}.png'
            page.screenshot(path=str(filename), full_page=True, animations='disabled')
            with Image.open(filename) as image:
                image.thumbnail((1600, 1134))
                image.save(target / f'{path.stem}-preview.jpg', quality=91)
            page.remove_listener('pageerror', on_error)
            results.append({'file': path.name, 'screenshot': str(filename), 'metrics': metrics})
            print(f'Screenshot: {filename}', flush=True)
        browser.close()
    return results


def contact_sheet(paths, target):
    canvas = Image.new('RGB', (1600, 5 * 605), '#0e1622')
    draw = ImageDraw.Draw(canvas)
    for i, path in enumerate(paths):
        with Image.open(target / f'{path.stem}.png') as image:
            image.thumbnail((790, 560))
            x, y = (i % 2) * 800, (i // 2) * 605
            canvas.paste(image, (x, y + 30))
            draw.text((x + 16, y + 8), path.stem, fill='#ECE6DA')
    canvas.crop((0, 0, 1600, ((len(paths) + 1) // 2) * 605)).save(target / 'contact-sheet.jpg', quality=92)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'output')
    parser.add_argument('--screenshots', type=Path, default=CACHE)
    parser.add_argument('--weapon', action='append', help='Slug; repeat to select multiple weapons')
    parser.add_argument('--capture-only', action='store_true', help='Inspect existing HTML without rerendering geometry')
    args = parser.parse_args(argv)
    from models import load_all
    from sheet import build_sheet
    started = time.monotonic()
    models = load_all()
    selected = [(n, meta, model) for n, (meta, model) in enumerate(models, 1)
                if not args.weapon or meta['slug'] in args.weapon]
    if not selected or (args.weapon and set(args.weapon) - {m['slug'] for _, m, _ in selected}):
        parser.error('Unknown or empty weapon selection')
    args.output.mkdir(parents=True, exist_ok=True)
    records, paths = [], []
    for number, meta, model in selected:
        checks = validate_model(meta, model)
        path = args.output / (meta['slug'] + '.html')
        if not args.capture_only:
            print(f"Baue {meta['name']} ({len(model)} Teile)", flush=True)
            record = build_sheet(meta, model, args.output, number)
        else:
            record = {'filename': path.name}
        if not args.capture_only:
            (args.output / (meta['slug'] + '-prompts.txt')).write_text('DEUTSCH\n' + record['prompts']['de'] + '\n\nENGLISH\n' + record['prompts']['en'] + '\n', encoding='utf-8')
        records.append({**record, 'slug': meta['slug'], 'geometry_sha256': geometry_hash(model), 'geometry_checks': checks})
        paths.append(path)
    captures = screenshots(paths, args.screenshots)
    contact_sheet(paths, args.screenshots)
    links = ''.join(f'<li><a href="{html.escape(p.name)}">{html.escape(p.stem)}</a></li>' for p in paths)
    (args.output / 'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><title>Cube Escape · Parallax</title><style>body{background:#0e1622;color:#ece6da;font:24px sans-serif;padding:60px}a{color:#f28c28}li{margin:18px}</style><h1>Cube Escape · Konzeptblätter</h1><p>10 Modelle · gleiche Geometrie je Ansicht und Farbvariante · gestalterische Referenzen</p><ul>'+links+'</ul></html>', encoding='utf-8')
    manifest = {'version': '0.1.0', 'name': 'Parallax', 'canvas': [4800, 3400],
                'records': records, 'browser_qa': captures, 'seconds': round(time.monotonic()-started, 2),
                'visual_review': 'Manuelle Sichtprüfung der Screenshots erforderlich; automatische Prüfungen ersetzen sie nicht.'}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"Fertig: {len(paths)} Blätter, {manifest['seconds']} s; {args.output / 'index.html'}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
