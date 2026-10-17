"""Fast reference-data checks: no image generation or external importer required."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eng import prism, bounds
from spec import CHANNELS, M, design_spec
import skins

CATALOG = [dict(id=f'test-{i}', name=f'Test {i}', description='Fixture only',
                accent1='#B00000', accent2='#00B000') for i in range(5)]


def block(label, x0, x1, y0, y1, z0=-2, z1=2, sight=False):
    p = prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], '#D5CCB8', z0, z1)
    p.label = label; p.sight = sight
    return p


def fixture(slug='pistol'):
    meta = dict(slug=slug, variant='K', variant_name='Flux Bloom', name='Fixture', kind='Fixture',
                palette=['#D5CCB8', '#858F99', '#303844', '#F28C28'], notes=[], form='test', sight_type='reflex')
    model = [block('Gehäuse', -10, 30, -4, 4), block('Griff', -8, 0, 2, 20),
             block('Abzug', 1, 3, 4, 9), block('Mündung', 30, 40, -2, 2),
             block('Visierklemme', 0, 4, -9, -4, sight=True),
             block('Reflexrahmen', 4, 6, -16, -6, sight=True)]
    return meta, model


def export(meta, model, record=None):
    with patch.object(skins, 'CATALOG', CATALOG):
        return design_spec(meta, model, 1, record or dict(orthographic_views=[], geometry_sha256='fixture'))


class DesignSpecTests(unittest.TestCase):
    def test_coordinate_matrix_is_rotation_and_points_have_deterministic_hand_origin(self):
        meta, model = fixture()
        data = export(meta, model)
        np.testing.assert_allclose(M @ M.T, np.eye(3))
        self.assertAlmostEqual(np.linalg.det(M), 1.)
        scale = .243 / 50
        self.assertAlmostEqual(data['units']['model_unit_m'], scale)
        self.assertEqual(data['anchors']['Socket_Hand']['model'], [-4., 11., 0.])
        self.assertEqual(data['anchors']['Socket_Hand']['position_m'], [0., 0., 0.])
        muzzle = data['anchors']['Socket_Muzzle']
        np.testing.assert_allclose(muzzle['position_m'], np.array([0, -44, 11]) * scale)
        self.assertLess(muzzle['position_m'][1], 0)
        self.assertEqual(export(meta, model), data)
        json.dumps(data, allow_nan=False)

    def test_raw_faces_bbox_and_legacy_properties_are_preserved(self):
        meta, model = fixture()
        data = export(meta, model)
        lo, hi = bounds([p for p in model if not p.sight])
        self.assertEqual(data['format'], 'CodexDesignReference')
        self.assertEqual(data['version'], 1)
        self.assertEqual(data['bounding_box'], [lo.tolist(), hi.tolist()])
        self.assertEqual(data['sheet']['id'], 'KK01')
        self.assertTrue(data['reference_only'])
        for part, raw in zip(model, data['parts']):
            for face, saved in zip(part.faces, raw['faces']):
                np.testing.assert_allclose(face.vertices, saved['vertices'], atol=1e-7)
        self.assertFalse(data['compatibility']['toolgen_import_validated'])

    def test_available_anchors_inside_source_bounds_and_missing_support_explained(self):
        meta, model = fixture()
        data = export(meta, model)
        for anchor in data['anchors'].values():
            if anchor['part'] and anchor['model'] is not None:
                lo, hi = bounds([model[int(anchor['part'][1:])]])
                point = np.asarray(anchor['model'])
                self.assertTrue(np.all(point >= lo - 1e-8))
                self.assertTrue(np.all(point <= hi + 1e-8))
        support = data['anchors']['Socket_SupportHand']
        self.assertIsNone(support['model'])
        self.assertIsNone(support['position_m'])
        self.assertTrue(support['null_reason'])
        self.assertTrue(data['anchors']['Socket_CenterOfMass']['source'].startswith('approximation'))

    def test_explicit_anchor_provenance_and_forward_support(self):
        meta, model = fixture('assault')
        model.append(block('Vordergriff', 10, 15, 3, 12))
        meta['anchors'] = {'Socket_Hand': dict(model=[-5, 10, 0], part='Griff', source='author pivot')}
        data = export(meta, model)
        hand = data['anchors']['Socket_Hand']
        self.assertEqual(hand['part'], 'p001')
        self.assertIn('author pivot', hand['source'])
        self.assertEqual(hand['position_m'], [0., 0., 0.])
        self.assertLess(data['anchors']['Socket_SupportHand']['position_m'][1], 0)

    def test_bow_scales_largest_extent_not_barrel_length(self):
        meta, model = fixture('bow')
        model.append(block('Wurfarm', -4, 4, -60, 60))
        data = export(meta, model)
        self.assertAlmostEqual(data['units']['model_unit_m'], 1.018 / 120)
        self.assertAlmostEqual(data['dimensions_m']['with_sight']['height'], 1.018)
        self.assertFalse(data['robot_fit']['applies'])

    def test_palette_has_exactly_seven_channels_and_annotated_source(self):
        meta, model = fixture()
        model[0].channel = 'MT_Secondary'
        record = dict(orthographic_views=[], geometry_sha256='fixture', main_skin=CATALOG[0], palette_variants=[
            dict(name='BASIS', colors=meta['palette']),
            dict(name='NACHT', colors=['#111111', '#222222', '#333333', '#444444'])])
        data = export(meta, model, record)
        for palette in data['palette_variants']:
            self.assertEqual(set(palette['channels']), set(CHANNELS))
        self.assertEqual(data['parts'][0]['channel'], 'MT_Secondary')
        self.assertTrue(data['parts'][0]['channel_source'].startswith('explicit'))
        self.assertEqual(len(data['skin']['catalog']), 5)
        self.assertEqual(data['skin']['hero'], CATALOG[0]['id'])
        self.assertEqual(data['skin']['catalog'][0]['accent1'], '#B00000')
        self.assertNotIn('channel', vars(model[1]))

    def test_no_inferred_window_from_housing_and_no_guessed_movement(self):
        meta, model = fixture()
        data = export(meta, model)
        self.assertEqual(data['sight']['type'], 'reflex')
        self.assertIsNone(data['sight']['window_geometry'])
        self.assertTrue(data['sight']['window_geometry_note'])
        self.assertIsNone(data['moving_parts']['items'])
        self.assertTrue(data['moving_parts']['null_reason'])

    def test_optical_surface_axis_detects_transverse_window(self):
        meta, model = fixture()
        # Flat YZ pane: looks forward down the barrel.
        model.append(block('Optikglas', 4, 4.2, -14, -8, -4, 4, sight=True))
        data = export(meta, model)
        window = data['sight']['window_geometry'][0]
        self.assertEqual(window['view_axis_m'], [0., -1., 0.])
        self.assertTrue(window['forward_aligned'])
        # Flat XY pane: its actual optical axis is transverse, even if declared reflex.
        model[-1] = block('Optikglas', 4, 12, -14, -8, -.1, .1, sight=True)
        window = export(meta, model)['sight']['window_geometry'][0]
        self.assertFalse(window['forward_aligned'])
        self.assertEqual(window['model_thin_axis'], 'Z')

    def test_explicit_open_aperture_uses_functional_normal_not_solid_frame(self):
        meta, model = fixture('trace')
        meta.update(sight_type='trace', sight_frame='industrial')
        model[-1].sight_window = True
        model[-1].window_geometry = dict(center_model=[5, -11, 0], normal_model=[1, 0, 0],
                                         width_model=3, height_model=8, source='explicit test aperture')
        data = export(meta, model)
        window = data['sight']['window_geometry'][0]
        self.assertEqual(window['type'], 'open_aperture')
        self.assertEqual(data['sight']['window_geometry_kind'], 'open')
        self.assertTrue(window['forward_aligned'])
        self.assertEqual(window['view_axis_m'], [0., -1., 0.])
        self.assertAlmostEqual(window['width_m'], 3 * data['units']['model_unit_m'])

    def test_robot_fit_reports_actual_and_target_separately_without_claiming_fit(self):
        meta, model = fixture('fusion')
        data = export(meta, model)
        fit = data['robot_fit']
        self.assertAlmostEqual(fit['actual']['length_m']['value'], .960)
        self.assertEqual(fit['targets']['length_m']['value'], .67)
        self.assertAlmostEqual(fit['sheet_at_target']['scale'], .67 / .960)
        self.assertIsNone(fit['actual']['support_forward_m']['value'])
        self.assertIsNone(fit['actual']['support_forward_m']['ok'])
        self.assertFalse(fit['validated'])
        self.assertIsNone(fit['fits_robot'])
        self.assertNotIn('silhouette_factor', fit['actual'])

    def test_reject_unknown_channel_scale_and_missing_origin(self):
        meta, model = fixture()
        model[0].channel = 'MT_MadeUp'
        with self.assertRaises(ValueError):
            export(meta, model)
        del model[0].channel
        meta['slug'] = 'unregistered'
        with self.assertRaises(ValueError):
            export(meta, model)
        meta['slug'] = 'pistol'; model[1].label = 'unnamed'
        with self.assertRaisesRegex(ValueError, 'Socket_Hand'):
            export(meta, model)


if __name__ == '__main__':
    unittest.main()
