"""Identity migration must reject old semantics rather than reinterpret IDs."""
import json
from pathlib import Path
import sys
import unittest
import jsonschema
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from design_types import EXISTING, weapon_fields


class DesignTypeTests(unittest.TestCase):
    def test_catalogue_values_match_official_type_facts(self):
        import importlib.util
        path = HERE.parents[1]/'claude/generator/wtypes.py'
        location = importlib.util.spec_from_file_location('official_types_read_only', path)
        module = importlib.util.module_from_spec(location)
        location.loader.exec_module(module)
        by_tool = {row['toolgen']: row for row in module.TYPES.values() if row['toolgen']}
        from weapon_spec import TOOLGEN
        for slug in EXISTING:
            row = weapon_fields(dict(slug=slug))
            official = by_tool[TOOLGEN[slug][0]]
            for ours, theirs in [('design_type','id'),('design_type_de','de'),('destiny_type','en'),('ammo_class','ammo')]:
                self.assertEqual(row[ours], official[theirs])
            self.assertIsNone(row['subtype'])
            self.assertEqual(row['toolgen_status'], 'tool')

    def test_saved_v2_specs_reject_v1_and_old_trace_tool_id(self):
        validator = jsonschema.Draft202012Validator(json.loads((HERE/'weapon-spec.schema.json').read_text()))
        for family, letter in [('parallax','A'),('fluxbloom','K')]:
            spec = json.loads((HERE.parent/family/f'output/K{letter}08.spec.json').read_text())
            validator.validate(spec)
            self.assertEqual(spec['format_version'], 2)
            self.assertEqual(spec['weapon']['toolgen_id'], 'trace_rifle')
            old = dict(spec, format_version=1)
            self.assertTrue(list(validator.iter_errors(old)))
            old = dict(spec, weapon=dict(spec['weapon'], toolgen_id='invalid_old_trace_id'))
            self.assertTrue(list(validator.iter_errors(old)))

if __name__ == '__main__': unittest.main()
