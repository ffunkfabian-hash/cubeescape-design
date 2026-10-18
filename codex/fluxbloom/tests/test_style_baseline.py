"""The style contract must not change authored models, palettes or names."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collections_codex import load_collection
from build import geometry_hash


class StyleBaselineTests(unittest.TestCase):
    def test_all_twenty_models_palettes_and_names_remain_unchanged(self):
        data=json.loads((Path(__file__).parent/'data/style-contract-baseline.json').read_text())
        for family,expected in data['collections'].items():
            actual=load_collection(family)
            self.assertEqual(len(actual),len(expected))
            for meta,model in actual:
                with self.subTest(family=family,weapon=meta['slug']):
                    previous=expected[meta['slug']]
                    self.assertEqual(geometry_hash(model),previous['geometry_sha256'])
                    self.assertEqual(meta['palette'],previous['palette'])
                    self.assertEqual(meta['name'],previous['name'])
