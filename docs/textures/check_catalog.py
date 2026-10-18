#!/usr/bin/env python3
"""Prüft den Texturkatalog: Schema, Verweise, Musterbilder (sha256), Abgleich mit Toolgen, wenn das Repo lokal liegt.

  python3 check_catalog.py            schnell, nur Standardbibliothek (jsonschema wird genutzt, wenn vorhanden)
  python3 check_catalog.py --deep     erzeugt die Musterbilder im Speicher neu und vergleicht die Pixel (numpy, Pillow nötig)
  python3 check_catalog.py --toolgen PFAD   anderer Ort für surface_recipes.json
Beendet mit 1 bei jedem Befund.
"""
import sys, os, json, hashlib, glob

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLGEN = os.path.expanduser('~/Claude/cubeescape-toolgen/data/surface_recipes.json')
problems = []


def bad(msg):
    problems.append(msg)


# ---------- kleiner Schema-Prüfer (Teilmenge von JSON Schema, genug für catalog.schema.json)
def _type_ok(v, t):
    if isinstance(t, list):
        return any(_type_ok(v, x) for x in t)
    return {'object': isinstance(v, dict), 'array': isinstance(v, list), 'string': isinstance(v, str), 'boolean': isinstance(v, bool),
            'null': v is None, 'number': isinstance(v, (int, float)) and not isinstance(v, bool),
            'integer': isinstance(v, int) and not isinstance(v, bool)}[t]


def validate(v, s, root, path='$'):
    import re
    if '$ref' in s:
        node = root
        for k in s['$ref'][2:].split('/'):
            node = node[k]
        return validate(v, node, root, path)
    if 'const' in s and v != s['const']:
        bad(f'{path}: erwartet {s["const"]!r}')
    if 'enum' in s and v not in s['enum']:
        bad(f'{path}: {v!r} nicht in {s["enum"]}')
    if 'type' in s and not _type_ok(v, s['type']):
        bad(f'{path}: falscher Typ ({type(v).__name__})'); return
    if isinstance(v, str) and 'pattern' in s and not re.search(s['pattern'], v):
        bad(f'{path}: {v!r} passt nicht zu {s["pattern"]}')
    if _type_ok(v, 'number') and not isinstance(v, bool):
        if 'minimum' in s and v < s['minimum']: bad(f'{path}: {v} < {s["minimum"]}')
        if 'maximum' in s and v > s['maximum']: bad(f'{path}: {v} > {s["maximum"]}')
        if 'exclusiveMinimum' in s and v <= s['exclusiveMinimum']: bad(f'{path}: {v} <= {s["exclusiveMinimum"]}')
    if isinstance(v, dict):
        for k in s.get('required', []):
            if k not in v: bad(f'{path}: Feld {k} fehlt')
        props = s.get('properties', {})
        for k, sub in props.items():
            if k in v: validate(v[k], sub, root, f'{path}.{k}')
        ap = s.get('additionalProperties')
        if isinstance(ap, dict):
            for k, x in v.items():
                if k not in props: validate(x, ap, root, f'{path}.{k}')
    if isinstance(v, list):
        if 'minItems' in s and len(v) < s['minItems']: bad(f'{path}: weniger als {s["minItems"]} Einträge')
        if 'maxItems' in s and len(v) > s['maxItems']: bad(f'{path}: mehr als {s["maxItems"]} Einträge')
        if 'items' in s:
            for i, x in enumerate(v): validate(x, s['items'], root, f'{path}[{i}]')


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    deep = '--deep' in sys.argv
    tg = TOOLGEN
    if '--toolgen' in sys.argv:
        tg = sys.argv[sys.argv.index('--toolgen') + 1]
    cpath = os.path.join(HERE, 'catalog.json')
    cat = json.load(open(cpath, encoding='utf-8'))
    schema = json.load(open(os.path.join(HERE, 'catalog.schema.json'), encoding='utf-8'))

    # 1 Schema
    try:
        import jsonschema
        for e in jsonschema.Draft202012Validator(schema).iter_errors(cat):
            bad('Schema ' + '/'.join(str(p) for p in e.absolute_path) + ': ' + e.message)
    except ImportError:
        validate(cat, schema, schema)

    # 2 Verweise
    def ids(sec, key='id'): return [x[key] for x in cat[sec]]
    for sec in ('materials', 'patterns', 'finishes', 'skins'):
        d = [i for i in ids(sec) if ids(sec).count(i) > 1]
        if d: bad(f'{sec}: doppelte IDs {sorted(set(d))}')
    pat, fin = set(ids('patterns')), set(ids('finishes'))
    mats = set(ids('materials'))
    for m in cat['materials']:
        if m['pattern'] is not None and m['pattern'] not in pat: bad(f'Material {m["id"]}: Muster {m["pattern"]} fehlt')
        if m['finish'] is not None and m['finish'] not in fin: bad(f'Material {m["id"]}: Oberfläche {m["finish"]} fehlt')
        if m['sheet_pattern'] and not m['swatch']: bad(f'Material {m["id"]}: Musterbild fehlt')
    for c in cat['channels']['items']:
        if c['material'] is not None and c['material'] not in mats: bad(f'Kanal {c["id"]}: Material {c["material"]} fehlt')
    for p in cat['patterns']:
        if p['used_by_sheets'] and p['id'] != 'none' and not p['params']: bad(f'Muster {p["id"]}: params leer')
    for s in cat['skins']:
        for k, a in s['accents'].items():
            if a['finish'] not in fin: bad(f'Skin {s["id"]}: {k} Oberfläche {a["finish"]} fehlt')
        used = []
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ('slot', 'color', 'from', 'to') and isinstance(v, str) and v[:3] in ('MT_', 'SK_'): used.append(v)
                    if k == 'slots': used.extend(v)
                    if k == 'finish' and isinstance(v, str) and v not in fin: bad(f'Skin {s["id"]}: Oberfläche {v} fehlt')
                    walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(s['layers']); walk(s.get('decor', {}))
        slots = {c['id'] for c in cat['channels']['items']}
        for u in used:
            if u not in slots: bad(f'Skin {s["id"]}: unbekannter Slot {u}')
    if sorted(set(s['origin'] for s in cat['skins'])) != ['claude', 'codex']: bad('Skins: origin claude und codex erwartet')

    # 3 Musterbilder
    sd = os.path.join(HERE, 'swatches'); mp = os.path.join(sd, 'manifest.json')
    refs = [m['swatch'] for m in cat['materials'] if m['swatch']] + [f['swatch'] for f in cat['finishes']] + [cat['wear']['swatch']] + [s['swatch'] for s in cat['skins']]
    if not os.path.exists(mp):
        bad('swatches/manifest.json fehlt (make_swatches.py ausführen)')
    else:
        man = json.load(open(mp))
        if man['catalog_sha256'] != sha(cpath): bad('Musterbilder veraltet: catalog.json hat sich seit make_swatches.py geändert')
        have = {os.path.basename(p) for p in glob.glob(os.path.join(sd, '*.png'))}
        want = {os.path.basename(r) for r in refs}
        for n in sorted(want - have): bad(f'Musterbild fehlt: {n}')
        for n in sorted(have - want): bad(f'Musterbild ohne Katalogeintrag: {n}')
        for n in sorted(want & have):
            if n not in man['files']: bad(f'{n}: nicht im Manifest')
            elif sha(os.path.join(sd, n)) != man['files'][n]['sha256']: bad(f'{n}: sha256 weicht vom Manifest ab')
        if deep:
            sys.path.insert(0, HERE)
            import make_swatches as ms
            for n, im in ms.build(cat).items():
                if n in man['files'] and ms.sha_pixels(im) != man['files'][n]['pixels_sha256']:
                    bad(f'{n}: neu erzeugte Pixel weichen vom Manifest ab')

    # 4 Toolgen
    if os.path.exists(tg):
        t = json.load(open(tg))
        for m in t['materials']:
            if m not in mats: bad(f'Toolgen-Material {m} fehlt im Katalog')
        for m in cat['materials']:
            if m['toolgen_material'] not in t['materials']: bad(f'Material {m["id"]}: toolgen_material {m["toolgen_material"]} unbekannt')
        tp = {p['toolgen_pattern'] for p in cat['patterns'] if p['toolgen_pattern']}
        if tp != set(t['patterns']): bad(f'Toolgen-Muster {sorted(set(t["patterns"]) ^ tp)} stimmen nicht überein')
        for k, v in t['limits']['wear_levels'].items():
            if cat['wear']['levels'][k]['toolgen'] != v: bad(f'wear {k}: Katalog {cat["wear"]["levels"][k]["toolgen"]} ≠ Toolgen {v}')
        for p in cat['patterns']:
            if p['height_mm'] is not None and p['height_mm'] > t['limits']['max_height_mm']: bad(f'Muster {p["id"]}: height_mm über Toolgen-Grenze')
        seen = {}
        for w in t['weapons'].values():
            for ch, x in w['channels'].items(): seen.setdefault('MT_' + ch, set()).add(x['material'])
        for c in cat['channels']['items']:
            if c['material'] and c['id'] in seen and c['material'] not in seen[c['id']]:
                bad(f'Kanal {c["id"]}: Standardmaterial {c["material"]} kommt in Toolgen nicht vor ({sorted(seen[c["id"]])})')
        print(f'Toolgen-Abgleich: {tg}')
    else:
        print('Toolgen-Abgleich übersprungen (surface_recipes.json nicht gefunden)')

    if problems:
        print(f'{len(problems)} Befunde:'); [print(' -', p) for p in problems]; sys.exit(1)
    print(f'check_catalog: grün ({len(cat["materials"])} Materialien, {len(cat["patterns"])} Muster, {len(cat["finishes"])} Oberflächen, '
          f'{len(cat["skins"])} Skins, {len(refs)} Musterbilder{", Pixel neu erzeugt" if deep else ""})')


if __name__ == '__main__':
    main()
