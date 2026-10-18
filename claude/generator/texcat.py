"""Gemeinsamer Texturkatalog lesen (claude-0.8): docs/textures/catalog.json (`cubeescape-design/texture-catalog` v1).

Claudes Pipeline kopiert keine Werte in eigenen Code, sondern liest Muster, Oberflächen, Abnutzung und die neun Claude-Skins zur Bauzeit
aus dem Katalog (Regel in docs/textures/README.md). Längen stehen im Katalog in mm am echten Objekt; die Pipeline rechnet mit der
Modelleinheit des Blatts (Spec `units.model_unit_m`, Meter je Modelleinheit) in Modelleinheiten um: Modelleinheiten = mm / (model_unit_m · 1000).
Ohne numpy (export_spec.py und Tests nutzen das Modul ebenfalls).
"""
from cepaths import ROOT
import hashlib,json,math,os

PATH=os.path.join(ROOT,'docs','textures','catalog.json')
FORMAT='cubeescape-design/texture-catalog'
VERSION=1
_cache={}

def load(path=PATH):
    """Katalog laden (ein Mal je Pfad und Datei-Stand); prüft format und format_version."""
    st=os.stat(path);key=(path,st.st_mtime_ns,st.st_size)
    if key not in _cache:
        with open(path,encoding='utf-8') as f:c=json.load(f)
        if c.get('format')!=FORMAT or c.get('format_version')!=VERSION:
            raise ValueError(f'{path}: erwartet {FORMAT} v{VERSION}, gefunden {c.get("format")!r} v{c.get("format_version")!r}')
        _cache.clear();_cache[key]=c
    return _cache[key]

def _index(section):
    rows=load()[section];idx={r['id']:r for r in rows}
    if len(idx)!=len(rows):raise ValueError(f'Katalog: doppelte ID in {section}')
    return idx
def material(mid):return _index('materials')[mid]
def pattern(pid):return _index('patterns')[pid]
def finish(fid):return _index('finishes')[fid]
def skin(sid):return _index('skins')[sid]
def material_of_alias(alias,who='claude'):
    """Katalog-Material zu Claudes Namen (lack, brushed, rubber, plastic, light) oder dem Namen im Spec (painted, matte, lit)"""
    hit=[m for m in load()['materials'] if m['aliases'].get(who)==alias]
    if len(hit)!=1:raise KeyError(f'Katalog: {len(hit)} Materialien mit Alias {who}={alias!r} (erwartet: genau eines)')
    return hit[0]

def fingerprint():
    """sha256 über die Teile des Katalogs, die Claudes Blätter lesen (Muster, Materialien, Oberflächen, Abnutzung, Glyphen, Claude-Skins)"""
    c=load();part=dict(patterns=c['patterns'],materials=c['materials'],finishes=c['finishes'],wear=c['wear'],glyphs=c['glyphs'],
                       skins=[s for s in c['skins'] if s['origin']=='claude'])
    return hashlib.sha256(json.dumps(part,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode('ascii')).hexdigest()

# ---------- Muster in Modelleinheiten
def to_mu(mm,unit_m):
    """mm am Objekt -> Modelleinheiten des Blatts (unit_m: Meter je Modelleinheit, > 0 und endlich)"""
    if not (isinstance(unit_m,(int,float)) and math.isfinite(unit_m) and unit_m>0):raise ValueError(f'texcat: ungültige Modelleinheit {unit_m!r}')
    return mm/(unit_m*1000.0)

def sheet_patterns(unit_m):
    """Parameter der Material-Ansicht des Blatts (xl.make_texture) in Modelleinheiten für die Modelleinheit unit_m.
    Formeln stehen im Katalog (patterns[].params.formula); hier nur Zahlen. Fehlt unit_m (None), gilt der Startwert des Katalogs."""
    c=load();u=c['units']['model_unit_m'] if unit_m is None else unit_m
    g=pattern('gloss_gradient')['params'];b=pattern('brushed')['params'];k=pattern('knurl');n=pattern('grain')
    wave=lambda w:dict(axes=tuple(w['axes']),k=2*math.pi/to_mu(w['wavelength_mm'],u),amp=w['amplitude'])
    return dict(
        gloss=[wave(w) for w in g['waves']],
        brushed=dict(amp=b['amplitude'],waves=[(2*math.pi/to_mu(w['wavelength_mm'],u),w['phase'],w['weight']) for w in b['waves']]),
        knurl=dict(cell=to_mu(k['size_mm'],u),dark=k['params']['darkening']),
        grain=dict(cell=to_mu(n['size_mm'],u),amp=n['params']['amplitude'],hash=tuple(n['params']['hash_coefficients'])),
    )

# ---------- Oberflächen und Abnutzung
def paint_levels():
    """Helligkeitsfaktoren der Toon-Stufen (hell, mittel, schattig, dunkel) des Lacks; die erste Stufe ist auch das Glanzlicht"""
    return tuple(finish('paint')['ladder']['levels'])

def ladder(fid):
    """Tonleiter einer polierten oder leuchtenden Oberfläche: (vier Stufen, Glanzlicht), je (Anteil, Mischfarbe|None) bzw. feste Farbe"""
    L=finish(fid)['ladder']
    if L['kind']!='blends':raise ValueError(f'{fid}: keine Mischtonleiter')
    steps=[(s['amount'],s['with']) for s in L['steps']];h=L['highlight']
    return steps,(('fixed',h['fixed']) if 'fixed' in h else (h['amount'],h['with']))

def finish_ids():return tuple(f['id'] for f in load()['finishes'])
def has_streak(fid):return bool(finish(fid)['streak'])
def bare_metal():return load()['wear']['bare_metal']
def wear_cell_widths():return load()['wear']['cell_widths']
def wear_width_variation():return tuple(load()['wear']['width_variation'])
def streak():
    s=load()['wear']['streak'];return dict(direction=tuple(s['direction']),period_rel=s['period_rel_height'],width_fraction=s['width_fraction'])
def wear_levels():return load()['wear']['levels']

# ---------- Skins (Claude-Ursprung) in der Form von skins.CATALOG
_DROP_LAYER=('block','wear')
def claude_skins():
    """skins.CATALOG aus dem Katalog: Liste von dict(id, name, accents={Slot: (Farbe, Oberfläche)}, layers=[...]) wie bisher in skins.py.
    Katalog-Lagen tragen zusätzlich `block` und `wear` (Dokumentation); sie gehören nicht zur Lage der Pipeline."""
    def lay(L):
        o={k:v for k,v in L.items() if k not in _DROP_LAYER}
        for k in ('dir','at','center','along','window','poly','start','end'):
            if k in o and isinstance(o[k],list):o[k]=_tup(o[k])
        return o
    out=[]
    for s in load()['skins']:
        if s['origin']!='claude':continue
        out.append(dict(id=s['id'],name=s['name']['de'] if isinstance(s['name'],dict) else s['name'],
                        accents={k:(v['color'],v['finish']) for k,v in s['accents'].items()},layers=[lay(L) for L in s['layers']]))
    return out
def _tup(x):return tuple(_tup(y) for y in x) if isinstance(x,list) else x

def claude_skin_descriptions():
    """{id: (de, en)} der neun Claude-Skins"""
    return {s['id']:(s['description']['de'],s['description']['en']) for s in load()['skins'] if s['origin']=='claude'}

def skin_ids():return [s['id'] for s in load()['skins']]
