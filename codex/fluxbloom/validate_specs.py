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
    official = json.loads((REPO/'claude/docs/weapon-spec.schema.json').read_text())
    local = json.loads((HERE/'weapon-spec.schema.json').read_text())
    sys.path.append(str(REPO/'claude/generator'))
    location = importlib.util.spec_from_file_location('shared_spec_checks', REPO/'claude/generator/spec_checks.py')
    checks = importlib.util.module_from_spec(location)
    location.loader.exec_module(checks)
    schemas = [jsonschema.Draft202012Validator(s) for s in (local, official)]
    from collections_codex import load_collection
    from design_types import weapon_fields
    count = 0
    for family in ('parallax', 'fluxbloom'):
        expected = load_collection(family)
        files = sorted((HERE.parent/family/'output').glob('K*.spec.json'))
        assert len(files) == len(expected), (family, len(files), len(expected))
        for path, (meta, _) in zip(files, expected):
            spec = json.loads(path.read_text())
            for schema in schemas:
                schema.validate(spec)
            fields = weapon_fields(meta)
            assert all(spec['weapon'][k] == v for k, v in fields.items()), path.name
            issues = checks.direction_problems(spec)
            vs = spec['sight'].get('sight_spec')
            sight = json.loads((REPO/'claude/output/sheets'/vs['file']).read_text()) if vs else None
            issues += checks.vs_problems(spec, sight)
            assert not issues, (path.name, issues)
            count += 1
    print(f'{count} Codex-Specs: beide Schemas Format 2; shared spec_checks 0 Befunde.')


if __name__ == '__main__':
    main()
