#!/usr/bin/env python3
"""Validate every saved Codex spec against format 2 and shared read-only checks."""
import importlib.util
import json
from pathlib import Path
import sys
import jsonschema

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--family', choices=('parallax','fluxbloom','both'), default='both')
    parser.add_argument('--existing', action='store_true')
    args=parser.parse_args()
    official = json.loads((REPO/'claude/docs/weapon-spec.schema.json').read_text())
    local = json.loads((HERE/'weapon-spec.schema.json').read_text())
    sys.path.append(str(REPO/'claude/generator'))
    location = importlib.util.spec_from_file_location('shared_spec_checks', REPO/'claude/generator/spec_checks.py')
    checks = importlib.util.module_from_spec(location)
    # spec_checks needs only the output path. Avoid cepaths' mkdir side effect
    # so this consumer validation remains read-only in the Claude tree.
    from types import SimpleNamespace
    previous = sys.modules.get('cepaths')
    sys.modules['cepaths'] = SimpleNamespace(OUT=str(REPO/'claude/output/sheets'))
    try:
        location.loader.exec_module(checks)
    finally:
        if previous is None: sys.modules.pop('cepaths', None)
        else: sys.modules['cepaths'] = previous
    sight_validator = jsonschema.Draft202012Validator(json.loads((REPO/'claude/docs/sight-spec.schema.json').read_text()))
    for path in (REPO/'claude/output/sheets').glob('VS*.spec.json'):
        sight_validator.validate(json.loads(path.read_text()))
    schemas = [jsonschema.Draft202012Validator(s) for s in (local, official)]
    from collections_codex import load_collection
    from design_types import NEW, weapon_fields
    from weapon_spec import TOOLGEN
    from operations import operation
    count = 0
    for family in (('parallax','fluxbloom') if args.family=='both' else (args.family,)):
        expected = load_collection(family, include_new=not args.existing)
        files = sorted((HERE.parent/family/'output').glob('K*.spec.json'))
        if args.existing: files=[p for p in files if int(p.stem[2:4])<=10]
        assert len(files) == len(expected), (family, len(files), len(expected))
        for number, (path, (meta, _)) in enumerate(zip(files, expected), 1):
            spec = json.loads(path.read_text())
            for schema in schemas:
                schema.validate(spec)
            assert spec['sheet']['id'] == path.name.removesuffix('.spec.json'), path.name
            assert spec['sheet']['variant'] == meta['variant'], path.name
            assert spec['sheet']['variant_name'] == meta['variant_name'], path.name
            assert spec['sheet']['number'] == f'{number:02d}', path.name
            assert spec['weapon']['toolgen_id'] == (None if meta['slug'] in NEW else TOOLGEN[meta['slug']][0]), path.name
            assert spec['operation'] == operation(meta), path.name
            fields = weapon_fields(meta)
            assert all(spec['weapon'][k] == v for k, v in fields.items()), path.name
            issues = checks.direction_problems(spec)
            vs = spec['sight'].get('sight_spec')
            sight = json.loads((REPO/'claude/output/sheets'/vs['file']).read_text()) if vs else None
            issues += checks.vs_problems(spec, sight)
            issues += checks.sight_target_hints(spec)
            assert not issues, (path.name, issues)
            count += 1
    print(f'{count} Codex-Specs: beide Schemas Format 2; shared spec_checks 0 Befunde.')


if __name__ == '__main__':
    main()
