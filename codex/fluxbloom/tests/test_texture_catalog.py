"""Catalogue references, physical pitch and live parameter consumption."""
from contextlib import contextmanager
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import texture_catalog as textures
from eng import prism
from raster import _finish_surface, render, shade_factor, LIGHT, texture_factor
from skins import CATALOG, FINISH, apply_skin, sample_surface


@contextmanager
def temporary_catalog(data):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/'catalog.json'
        path.write_text(json.dumps(data))
        with patch.object(textures, 'CATALOG_PATH', path):
            yield path


class TextureCatalogTests(unittest.TestCase):
    def body(self):
        part = prism([(0,0),(100,0),(100,50),(0,50)],'#D5CCB8',-8,8)
        part.label = 'Gehäuse'
        return part

    def test_used_ids_and_aliases_exist_in_catalogue(self):
        from collections_codex import load_collection
        data = textures.catalog()
        ids = {row['id'] for row in data['materials']}
        for family in ('parallax','fluxbloom'):
            for _,model in load_collection(family):
                for part in model:

                    if part.material=='glass':continue
                    self.assertIn(textures.material(part.material)['id'],ids)
        self.assertEqual({row['id'] for row in CATALOG},
                         {row['id'] for row in data['skins'] if row['origin']=='codex'})
        for row in textures.codex_skins():
            for layer in row['layers']:
                if 'finish' in layer:
                    self.assertEqual(textures.finish(layer['finish'])['id'],layer['finish'])
                if 'material' in layer:
                    self.assertIn(textures.material(layer['material'])['id'],ids)
            self.assertEqual(textures.finish(row['decor']['trim']['finish'])['id'],row['decor']['trim']['finish'])
        for identifier in ('paint','gold','chrome'):
            self.assertIn(textures.finish(identifier),data['finishes'])
        with self.assertRaises(ValueError):
            textures.material('unknown_material')

    def test_rejects_wrong_format_version_and_missing_reference(self):
        source = deepcopy(textures.catalog())
        for field,value in (('format','unrelated'),('format_version',2)):
            data = deepcopy(source); data[field] = value
            with temporary_catalog(data) as path:
                with self.assertRaisesRegex(ValueError,'format/version'):
                    textures.load_catalog(path)
        source['materials'][0]['pattern'] = 'missing_pattern'
        with temporary_catalog(source) as path:
            with self.assertRaisesRegex(ValueError,'Unknown pattern'):
                textures.load_catalog(path)

    def test_same_physical_points_have_same_pattern_at_different_model_scales(self):
        points = np.random.default_rng(7).uniform(-80,80,(200,3))
        for material in ('paint','metal','rubber','plastic','light'):
            original = texture_factor(material,points,[0,0,1],model_unit_m=.002)
            scaled = texture_factor(material,points*8,[0,0,1],model_unit_m=.002/8)
            np.testing.assert_allclose(original,scaled,atol=1e-12)
        for invalid in (0,-1,np.nan,np.inf):
            with self.assertRaises(ValueError):
                texture_factor('metal',points,model_unit_m=invalid)
        fallback = textures.catalog()['units']['model_unit_m']
        np.testing.assert_array_equal(texture_factor('rubber',points),
                                      texture_factor('rubber',points,model_unit_m=fallback))
        standalone = render([],size=(8,8),glow=False)
        self.assertEqual(standalone.model_unit_m,fallback)
        self.assertEqual(standalone.texture_scale_source,'catalog_start_value_missing_spec')
        explicit = render([],size=(8,8),glow=False,model_unit_m=.002)
        self.assertEqual(explicit.texture_scale_source,'Weapon-Spec units.model_unit_m')

    def test_file_edits_change_material_and_skin_without_reimport(self):
        data = deepcopy(textures.catalog())
        points = np.array([[20.,10.,8.],[60.,20.,8.],[80.,40.,8.]])
        with temporary_catalog(data) as path:
            before = texture_factor('metal',points,model_unit_m=.002)
            for row in data['patterns']:
                if row['id']=='brushed':
                    row['params']['amplitude'] = 0
            path.write_text(json.dumps(data))
            after = texture_factor('metal',points,model_unit_m=.002)
            self.assertFalse(np.array_equal(before,after))
            np.testing.assert_array_equal(after,np.ones(3))
            part = apply_skin([self.body()],'circuit_bloom')[0]
            sample = np.array([[68.,0.,8.]])
            before,_ = sample_surface(part,sample,[0,0,1],'circuit_bloom')
            recipe = next(s for s in data['skins'] if s['id']=='circuit_bloom')
            recipe['layers'][1]['mask']['lo'] = .90
            recipe['decor']['trim']['count'] = 1
            recipe['decor']['badge']['color'] = '#112233'
            path.write_text(json.dumps(data))
            after,_ = sample_surface(part,sample,[0,0,1],'circuit_bloom')
            self.assertFalse(np.array_equal(before,after))
            dressed = apply_skin([self.body()],'circuit_bloom')
            self.assertEqual(len(dressed),3)  # One trim on each side.
            self.assertEqual(dressed[0].decals[0].color,'#112233')

    def test_regional_materials_come_from_catalogue(self):
        part = apply_skin([self.body()],'circuit_bloom')[0]
        colors, finishes, materials = sample_surface(part,np.array([[72.5,0,8],[80.,0,8]]),
                                                    [0,0,1],'circuit_bloom',return_materials=True)
        self.assertEqual(list(materials),['brushed','painted'])
        self.assertEqual(list(finishes),[FINISH['paint'],FINISH['paint']])

    def test_tone_ladder_highlight_and_wear_read_current_catalogue(self):
        data = deepcopy(textures.catalog())
        face = self.body().faces[1]
        points = np.array([[50.,25.,8.],[.01,25.,8.]])
        colors = np.tile([210.,160.,75.],(2,1))
        finishes = np.full(2,FINISH['gold'])
        with temporary_catalog(data) as path:
            wear = data['wear']
            wear['levels']['subtle']['coverage'] = 0
            wear['streak']['width_fraction'] = 0
            gold = next(row for row in data['finishes'] if row['id']=='polished_gold')
            gold['ladder']['steps'][1] = {'amount':1,'with':'#123456'}
            path.write_text(json.dumps(data))
            def sample():
                return _finish_surface(colors.copy(),colors,finishes,points,face,1.08,
                                       body_height=50,origin=[0,0,-8])
            np.testing.assert_allclose(sample(),np.tile([18,52,86],(2,1)))
            wear['streak']['width_fraction'] = 1
            gold['ladder']['highlight'] = dict(fixed='#AABBCC')
            path.write_text(json.dumps(data))
            np.testing.assert_allclose(sample(),np.tile([170,187,204],(2,1)))
            wear['levels']['subtle']['coverage'] = 1
            wear['bare_metal'] = '#FF0000'
            path.write_text(json.dumps(data))
            worn = sample()
            self.assertGreater(worn[1,0],worn[1,1])
            np.testing.assert_allclose(worn[0],[170,187,204])
            paint = next(row for row in data['finishes'] if row['id']=='paint')
            paint['ladder']['levels'][0] = 1.31
            path.write_text(json.dumps(data))
            self.assertEqual(shade_factor(LIGHT),1.31)


if __name__=='__main__':
    unittest.main()
