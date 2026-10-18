"""Read-only adapter for the shared, versioned material/skin catalogue.

The file is checked at build time and reloaded after an on-disk edit. No recipe
parameters live here; aliases merely preserve the existing renderer vocabulary.
"""
from collections.abc import Sequence
import json
import math
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parents[2] / 'docs/textures/catalog.json'
_cache = None
_stamp = None
FINISH_ALIASES = {'gold': 'polished_gold', 'chrome': 'polished_chrome'}


def load_catalog(path=CATALOG_PATH):
    data = json.loads(Path(path).read_text())
    if data.get('format') != 'cubeescape-design/texture-catalog' or data.get('format_version') != 1:
        raise ValueError('Unsupported texture catalogue format/version')
    indexed = {}
    for section in ('materials', 'patterns', 'finishes', 'skins'):
        rows = data[section]
        indexed[section] = {row['id']: row for row in rows}
        if len(indexed[section]) != len(rows):
            raise ValueError(f'Duplicate texture catalogue ID in {section}')
    for row in data['materials']:
        for field, section in (('pattern', 'patterns'), ('finish', 'finishes')):
            if row.get(field) is not None and row[field] not in indexed[section]:
                raise ValueError(f"Unknown {field}: {row[field]}")
    for row in data['skins']:
        for accent in row['accents'].values():
            if accent['finish'] not in indexed['finishes']:
                raise ValueError(f"Unknown accent finish: {accent['finish']}")
        for layer in row['layers']:
            if layer.get('finish') and layer['finish'] not in indexed['finishes']:
                raise ValueError(f"Unknown skin finish: {layer['finish']}")
            if layer.get('material') and layer['material'] not in indexed['materials']:
                raise ValueError(f"Unknown skin material: {layer['material']}")
    return data


def catalog():
    global _cache, _stamp
    path = Path(CATALOG_PATH)
    stat = path.stat()
    stamp = (str(path), stat.st_mtime_ns, stat.st_size)
    if stamp != _stamp:
        _cache = load_catalog(path)
        _stamp = stamp
    return _cache


def _entry(section, identifier):
    for row in catalog()[section]:
        if row['id'] == identifier:
            return row
    raise ValueError(f'Unknown catalogue {section} ID: {identifier}')


def material(identifier):
    for row in catalog()['materials']:
        if identifier == row['id'] or identifier in row.get('aliases', {}).values():
            return row
    raise ValueError(f'Unknown catalogue material/alias: {identifier}')


def pattern(identifier):
    return _entry('patterns', identifier)


def finish(identifier):
    return _entry('finishes', FINISH_ALIASES.get(identifier, identifier))


def skin(identifier):
    return _entry('skins', identifier)


def codex_skins():
    return [row for row in catalog()['skins'] if row['origin'] == 'codex']


def model_unit_m(value=None):
    """Only missing Specs use the explicitly documented catalogue start value."""
    result = float(catalog()['units']['model_unit_m'] if value is None else value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError('model_unit_m must be finite and positive')
    return result


def skin_record(row):
    """Compatibility record for sheet text; parameterised recipes stay in JSON."""
    return dict(id=row['id'], name=row['name']['en'], description=row['description']['de'],
                accent1=row['accents']['SK_Accent1']['color'],
                accent2=row['accents']['SK_Accent2']['color'])


class CodexSkinRecords(Sequence):
    def __deepcopy__(self, memo):
        return [skin_record(row) for row in codex_skins()]

    def __len__(self):
        return len(codex_skins())

    def __getitem__(self, key):
        rows = codex_skins()
        if isinstance(key, slice):
            return [skin_record(row) for row in rows[key]]
        return skin_record(rows[key])
