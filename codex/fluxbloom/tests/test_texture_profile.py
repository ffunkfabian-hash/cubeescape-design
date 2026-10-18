"""The user's nine-type contract and shared Spec/sheet targets."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from texture_profile import profile, TILES
from texture_catalog import catalog
from collections_codex import load_collection
from weapon_spec import make_spec, schema_path
from sheet import build_sheet


class TextureProfileTests(unittest.TestCase):
    def test_nine_type_targets_and_bow_exclusion(self):
        expected = {
            'pistol': ('painted', 'brushed', 'orange', 'subtle', ['symbol_diamond','number_01']),
            'assault_rifle': ('painted', 'brushed', 'blue', 'medium', ['mil_ar2','tech_bars']),
            'pulse_rifle': ('ceramic', 'satin', 'violet', 'subtle', ['tech_ring']),
            'shotgun': ('painted_matte', 'rough_cast', 'orange', 'strong', ['hazard_stripes']),
            'sniper_rifle': ('painted', 'brushed', 'light_blue', 'subtle', ['serial_s07']),
            'smg': ('painted_matte', 'brushed', 'cyan', 'medium', ['arrows_chevron','arrow_triangle']),
            'fusion_rifle': ('painted', 'satin', 'violet', 'subtle', ['research']),
            'scout_rifle': ('painted', 'polished', 'blue', 'subtle', ['tech_lines']),
            'rocket_launcher': ('painted_matte', 'rough_cast', 'orange', 'strong', ['hazard_stripes','warning_triangle']),
        }
        interpreted = {'assault_rifle','pulse_rifle','smg','fusion_rifle','rocket_launcher'}
        for tid, values in expected.items():
            p = profile(tid)
            self.assertEqual((p['housing']['material'], p['metal']['material'], p['energy']['color'],
                              p['edge_wear']['level'], p['decals']['toolgen']), values)
            self.assertEqual(p['rubber']['material'], 'rubber')
            self.assertEqual(p['energy']['material'], 'energy_glass')
            self.assertEqual(bool(p['interpretation']), tid in interpreted)
            self.assertEqual(p['catalog']['wear_levels'], sorted(catalog()['wear']['levels']))
            self.assertTrue(all(p[key]['text_de'] for key, _ in TILES))
        self.assertIsNone(profile('bow'))
        with self.assertRaises(KeyError):
            profile('unrecognised_type')

    def test_returned_profiles_do_not_share_mutable_data(self):
        first = profile('pistol')
        first['housing']['material'] = 'other'
        first['decals']['toolgen'].append('other')
        self.assertEqual(profile('pistol')['housing']['material'], 'painted')
        self.assertEqual(profile('pistol')['decals']['toolgen'], ['symbol_diamond','number_01'])

    def test_invalid_catalogue_wear_level_fails_at_build_time(self):
        changed = deepcopy(catalog())
        del changed['wear']['levels']['subtle']
        with patch('texture_profile.catalog', return_value=changed):
            with self.assertRaisesRegex(ValueError, 'wear level'):
                profile('pistol')

    def test_all_twenty_specs_get_the_type_profile_without_changing_existing_data(self):
        import jsonschema
        schema = json.loads(schema_path().read_text())
        for family in ('parallax', 'fluxbloom'):
            for number, (meta, model) in enumerate(load_collection(family), 1):
                sp = make_spec(meta, model, number)
                target = profile(sp['weapon']['toolgen_id'])
                if number == 10:
                    self.assertNotIn('texture_profile', sp)
                else:
                    self.assertEqual(sp['texture_profile'], target)
                jsonschema.validate(sp, schema)
                # The committed pre-task Spec is a contract/geometry countercheck.
                import subprocess
                path = f'codex/{family}/output/{sp["sheet"]["id"]}.spec.json'
                previous = json.loads(subprocess.check_output(['git','show',f'25f108f:{path}']))
                current = deepcopy(sp)
                current.pop('texture_profile', None)
                current['generator'] = previous['generator']
                self.assertEqual(current, previous)
                if number != 10:
                    invalid = deepcopy(sp)
                    invalid['texture_profile']['energy']['color'] = 'red'
                    with self.assertRaises(jsonschema.ValidationError):
                        jsonschema.validate(invalid, schema)

    def test_normal_compact_and_bow_sheet_layouts(self):
        collection = load_collection('fluxbloom')
        def fake_render(model, **kwargs):
            w,h = kwargs['size']
            return SimpleNamespace(image=SimpleNamespace(width=w,height=h),anchors={},
                                   model_bbox=(0,0,w,h),scale=kwargs.get('scale',1))
        for index in (0,8,9):
            meta,model = collection[index]
            with tempfile.TemporaryDirectory() as target, patch('sheet.render',side_effect=fake_render), patch('sheet._image',return_value=''):
                row = build_sheet(meta,model,Path(target),index+1)
                document = (Path(target)/row['filename']).read_text()
            if index == 9:
                self.assertNotIn('texture_profile',row)
                self.assertNotIn('TEXTURPROFIL',document)
                continue
            self.assertEqual(row['texture_profile'],profile(make_spec(meta,model,index+1)['weapon']['toolgen_id']))
            self.assertEqual([t['key'] for t in row['texture_profile_tiles']], [k for k,_ in TILES])
            mx,my,mw,mh = row['panel_viewports']['material']
            x,y,w,h = row['texture_profile_viewport']
            self.assertGreaterEqual(x,mx)
            self.assertGreaterEqual(y,my)
            self.assertLessEqual(x+w,mx+mw)
            self.assertLessEqual(y+h,my+mh)
            self.assertTrue(all(s['viewport'][1]+s['viewport'][3]<y for s in row['material_samples']))
            for entry in row['texture_profile_tiles']:
                tx,ty,tw,th = entry['viewport']
                self.assertLessEqual(tx+tw,x+w+1e-8)
                self.assertLessEqual(ty+th,y+h+1e-8)
            for key,_ in TILES:
                self.assertIn(row['texture_profile'][key]['text_de'], document)


if __name__ == '__main__':
    unittest.main()
