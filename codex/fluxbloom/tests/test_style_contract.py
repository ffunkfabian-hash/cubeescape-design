"""Numerical style regressions, using tiny pixels and projected model bounds."""
import colorsys
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import tempfile

import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eng import Face, Part, bounds, prism
from raster import LIGHT, OUTLINE, render, rotation_matrix, shade_factor, shade_hls
from sheet import (_callout, _hero_frame, _orthographic_frame, _panel_layout, _project, _vertices, build_sheet,
                   DISPLAY_UNITS_PER_MODEL_UNIT, HERO_FIELD, OUTLINE_WIDTHS)


class StyleContractTests(unittest.TestCase):
    def box(self, color='#b06030', emit=False):
        result = prism([(-10,-10), (10,-10), (10,10), (-10,10)], color, -2, 2)
        result.emit = emit
        result.label = 'Gehäuse'
        return result

    def test_four_band_thresholds_are_strict(self):
        # Unit vectors with an exactly controlled scalar product to the light.
        tangent = np.cross(LIGHT, [0,0,1]); tangent /= np.linalg.norm(tangent)
        for d, expected in ((.8,1.28),(.7,1.08),(.4,.88),(0,.62)):
            self.assertEqual(shade_factor(d*LIGHT+np.sqrt(1-d*d)*tangent), expected)

    def test_hls_lightness_preserves_hue_and_saturation(self):
        colors = np.array([[180.,75.,40.], [50.,130.,170.], [80.,80.,80.]])
        for factor in (.62,.88,1.08,1.28):
            shaded = shade_hls(colors, factor)
            for before, after in zip(colors/255, shaded/255):
                h,l,s = colorsys.rgb_to_hls(*before)
                ah,al,ass = colorsys.rgb_to_hls(*after)
                self.assertAlmostEqual(h,ah)
                self.assertAlmostEqual(s,ass)
                expected = l*factor if factor<1 else l+(1-l)*(factor-1)*.9
                self.assertAlmostEqual(al,expected)

    def test_lighting_is_fixed_in_camera_space_in_all_views(self):
        vertices = np.array([[-10,-10,0], [10,-10,0], [10,10,0], [-10,10,0.]])
        normal = np.array([0,0,1.])
        samples = []
        for yaw,pitch in ((0,0),(-45,35.264),(90,-22),(180,90)):
            rotation = rotation_matrix(yaw,pitch)
            # Rotate the same screen-facing face back into each model frame.
            part = Part([Face(vertices@rotation, normal@rotation)], '#b06030')
            result = render([part], yaw=yaw, pitch=pitch, size=(96,96), scale=3, center=[0,0,0], glow=False)
            samples.append(result.image.getpixel((48,48)))
        self.assertEqual(len(set(samples)),1)
        np.testing.assert_array_equal(samples[0][:3],shade_hls([176,96,48],1.08).astype(np.uint8))

    def test_silhouette_is_dark_centred_and_uses_sheet_pixel_width(self):
        part = self.box('#ffffff')
        narrow = render([part], yaw=0, pitch=0, size=(96,96), scale=3, center=[0,0,0], ow=2.4, glow=False)
        wide = render([part], yaw=0, pitch=0, size=(96,96), scale=3, center=[0,0,0], ow=4.6, glow=False)
        self.assertEqual(narrow.model_bbox,wide.model_bbox)
        np.testing.assert_array_equal(narrow.part_ids,wide.part_ids)
        # Projected left boundary is x18; the stroke must reach both sides.
        image = np.asarray(wide.image)
        np.testing.assert_allclose(image[48,18,:3],OUTLINE,atol=2)
        self.assertGreater(image[48,16,3],200)
        self.assertLess(image[48,20,:3].max(),90)
        dark_narrow = (np.asarray(narrow.image)[48,:,:3].max(axis=1)<40)&(np.asarray(narrow.image)[48,:,3]>200)
        dark_wide = (image[48,:,:3].max(axis=1)<40)&(image[48,:,3]>200)
        self.assertGreater(dark_wide.sum(),dark_narrow.sum())

    def test_emitters_are_unlit_glow_is_restrained_and_hidden_lights_do_not_glow(self):
        emitter = self.box('#ff8020',emit=True)
        lit = render([emitter], yaw=0, pitch=0, size=(96,96), scale=2, ow=0, glow=True)
        flat = render([emitter], yaw=0, pitch=0, size=(96,96), scale=2, ow=0, glow=False)
        self.assertEqual(lit.image.getpixel((48,48))[:3],(255,128,32))
        pixels = np.asarray(lit.image)
        outside = (lit.part_ids<0)&(np.asarray(flat.image)[:,:,3]==0)
        self.assertGreater(pixels[:,:,3][outside].max(),0)
        self.assertLessEqual(pixels[:,:,3][outside].max(),77)
        cover = self.box('#ffffff'); cover.faces = [Face(f.vertices+[0,0,8],f.normal,f.smooth_group) for f in cover.faces]
        hidden = render([emitter,cover],yaw=0,pitch=0,size=(96,96),scale=2,ow=0,glow=True)
        no_glow = render([emitter,cover],yaw=0,pitch=0,size=(96,96),scale=2,ow=0,glow=False)
        np.testing.assert_array_equal(np.asarray(hidden.image),np.asarray(no_glow.image))

    def test_hidden_nearly_edge_on_faces_cannot_punch_ink_through_front_surface(self):
        front = Part([Face(np.array([[-10,-10,5], [10,-10,5], [10,10,5], [-10,10,5]]),
                                [0,0,1])], '#ffffff')
        for cosine, half_depth in ((.00000589,5.), (.0005,.1)):
            with self.subTest(cosine=cosine):
                normal = np.array([.5,np.sqrt(.75),cosine]); normal /= np.linalg.norm(normal)
                along = np.cross(normal,[0,0,1]); along /= np.linalg.norm(along)
                across = np.cross(normal,along)
                center = np.array([0,0,-10.])
                vertices = np.array([center-along*10-across*half_depth,
                                     center+along*10-across*half_depth,
                                     center+along*10+across*half_depth,
                                     center-along*10+across*half_depth])
                sliver = Part([Face(vertices,normal)], '#ff0000')
                for model in ([front,sliver],[sliver,front]):
                    result = render(model,yaw=0,pitch=0,size=(96,96),scale=3,
                                    center=[0,0,0],ow=4.6,glow=False)
                    # Before the fix, the first hidden face leaked 21 pixels.
                    self.assertFalse(np.any(result.part_ids==model.index(sliver)))
                    reference = render([front],yaw=0,pitch=0,size=(96,96),scale=3,
                                       center=[0,0,0],ow=4.6,glow=False)
                    np.testing.assert_array_equal(np.asarray(result.image),np.asarray(reference.image))

    def test_shadow_only_changes_composition_and_preserves_geometry_ids(self):
        part = self.box()
        plain = render([part],yaw=0,pitch=0,size=(96,96),scale=1,ow=0,shadow=False)
        shaded = render([part],yaw=0,pitch=0,size=(96,96),scale=1,ow=0,shadow=True)
        np.testing.assert_array_equal(plain.part_ids,shaded.part_ids)
        self.assertEqual(plain.anchors,shaded.anchors)
        self.assertEqual(shaded.image.getpixel((48,72)),(0,0,0,82))
        self.assertEqual(plain.image.getpixel((48,72))[3],0)

    def test_all_twenty_orthos_use_adaptive_rows_one_scale_and_fill_seventy_percent(self):
        from collections_codex import load_collection
        from skins import apply_skin, CATALOG
        for family in ('parallax','fluxbloom'):
            collection = load_collection(family)
            for index,(meta, model) in enumerate(collection):
                weapon = [p for p in model if not p.sight]
                dressed = apply_skin(weapon,CATALOG[0]['id'])
                lo,hi = bounds(weapon); center = (lo+hi)/2
                before = _vertices(dressed).copy()
                views,scale,layout = _orthographic_frame(dressed,center,(hi-lo)[1]>(hi-lo)[0])
                with self.subTest(family=family,slug=meta['slug']):
                    if layout not in ("long_rows","long_rows_extended"):
                        self.assertIn(meta["slug"],("pistol","bow"))
                        continue
                    if index in (4,7):
                        self.assertEqual(layout,"long_rows")
                    panels = _panel_layout(layout=="long_rows_extended")
                    self.assertEqual([v[0] for v in views],['LINKS','RECHTS','OBEN','UNTEN','VORNE','HINTEN'])
                    self.assertTrue(all(v[3][0]==1610 for v in views[:4]))
                    self.assertEqual(views[4][4][1],views[5][4][1])
                    self.assertLess(views[2][3][1],views[0][3][1])
                    for _,yaw,pitch,(w,h),(x,y) in views:
                        px,py,pw,ph = panels["orthographic"]
                        self.assertGreaterEqual(x,px)
                        self.assertGreaterEqual(y-17,py)
                        self.assertLessEqual(x+w,px+pw)
                        self.assertLessEqual(y+h,py+ph)
                        projected = _project(before-center,yaw,pitch)
                        half = np.abs(projected[:,:2]).max(axis=0)*scale
                        self.assertLess(half[0],w/2)
                        self.assertLess(half[1],h/2)
                    side_span = np.ptp(_project(before-center,0,0)[:,0])*scale
                    self.assertGreaterEqual(side_span/views[0][3][0],.70)
                    np.testing.assert_array_equal(_vertices(dressed),before)

    def test_extended_support_panels_do_not_overlap_or_move_hero_skins_and_prompts(self):
        normal,extended = _panel_layout(False),_panel_layout(True)
        for key in ("hero","skins","prompts"):
            self.assertEqual(normal[key],extended[key])
        self.assertEqual(extended['orthographic'],[2960,430,1700,2770])
        for key,viewport in extended.items():
            x,y,w,h = viewport
            self.assertGreaterEqual(x,0); self.assertGreaterEqual(y,0)
            self.assertLessEqual(x+w,4800); self.assertLessEqual(y+h,4432)
            for other,second in extended.items():
                if key>=other:continue
                sx,sy,sw,sh = second
                overlap = x<sx+sw and sx<x+w and y<sy+sh and sy<y+h
                self.assertFalse(overlap,(key,other))

    def test_sheet_reflow_keeps_native_render_aspect_and_catalog_spec_unit(self):
        from collections_codex import load_collection
        from spec import design_spec
        collection = load_collection('fluxbloom')
        for index in (0,8):
            meta,model = collection[index]
            physical = design_spec(meta,model,index+1,dict(orthographic_views=[],geometry_sha256=''))['units']['model_unit_m']
            calls = []
            def fake_render(model, **kwargs):
                calls.append(kwargs)
                w,h = kwargs['size']
                return SimpleNamespace(image=SimpleNamespace(width=w,height=h),anchors={},
                                       model_bbox=(0,0,w,h),scale=kwargs.get('scale',1),center=kwargs.get('center'))
            with tempfile.TemporaryDirectory() as output, patch('sheet.render',side_effect=fake_render), patch('sheet._image',return_value='') as images:
                record = build_sheet(meta,model,Path(output),index+1)
            with self.subTest(weapon=meta['slug']):
                self.assertTrue(all(call['model_unit_m']==physical for call in calls))
                # Every embedded model image uses its native dimensions.
                self.assertTrue(all(len(call.args)==3 and not call.kwargs for call in images.call_args_list))
                self.assertEqual(record['textures']['model_unit_m'],physical)
                self.assertEqual(record['panel_viewports']['orthographic'][3],1770 if index==0 else 2770)
                if index==8:
                    self.assertEqual(record['material_viewport'],[1586,2370,591,300])
                    self.assertEqual(record['detail']['viewport'],[180,2390,591,630])
                    self.assertTrue(all(sample['viewport'][2:]==[110,75] for sample in record['material_samples']))
                    self.assertTrue(all(p['viewport'][2:]==[280,270] for p in record['palette_variants']))
                    for section in ('detail','optic','material','palette'):
                        self.assertEqual(record['panel_viewports'][section][1:],[2240,671,960])

    def test_hero_fitting_uses_documented_display_units_and_contract_reserves(self):
        part = self.box()
        center,scale = _hero_frame([part])
        projected = _project(_vertices([part])-center,-45,35.264)
        span = np.ptp(projected,axis=0)
        self.assertLessEqual(scale,6*DISPLAY_UNITS_PER_MODEL_UNIT)
        self.assertLessEqual(span[0]*scale,HERO_FIELD[0]-200+1e-9)
        self.assertLessEqual(span[1]*scale,HERO_FIELD[1]-420+1e-9)
        self.assertEqual(OUTLINE_WIDTHS,dict(hero=4.6,orthographic=3.,material=3.,optic=2.6,skin=2.6,palette=2.4,detail=3.))
        pill = _callout('Gehäuse',(100,200),(300,50),'#ff8020')
        for token in ('height="46"','rx="23"','stroke-width="1.8"','font-size="19"','font-weight="600"','r="6"','stroke="#0A0A0D"'):
            self.assertIn(token,pill)


if __name__ == '__main__':
    unittest.main()
