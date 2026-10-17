"""Small object-space and attachment regressions, without sheet generation."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eng import bounds, prism
from raster import render, project, rotation_matrix
from skins import (CATALOG, CHANNELS, FINISH, apply_skin, channel_for,
                   channel_palette, sample_surface, _inside)


class SkinTests(unittest.TestCase):
    def body(self):
        part = prism([(0,0),(100,0),(100,50),(0,50)], '#D5CCB8', -8, 8)
        part.label = 'Gehäuse'
        return part

    def test_catalog_contains_five_substantial_recipes(self):
        self.assertEqual(len(CATALOG),5)
        self.assertEqual(len({s['id'] for s in CATALOG}),5)
        part = self.body()
        xx,yy = np.meshgrid(np.linspace(0,100,37),np.linspace(0,50,23))
        points = np.column_stack((xx.ravel(),yy.ravel(),np.full(xx.size,8)))
        fingerprints = []
        for entry in CATALOG:
            self.assertEqual(set(entry),{'id','name','description','accent1','accent2'})
            model = apply_skin([part],entry['id'])
            colors,finishes = sample_surface(model[0],points,[0,0,1],entry['id'])
            self.assertGreater(np.ptp(colors,axis=0).max(),40)
            self.assertGreater(len(model),1)
            self.assertTrue(model[0].decals)
            fingerprints.append(colors.tobytes())
            if entry['id']=='gilt_vector':
                self.assertIn(FINISH['gold'],finishes)
                self.assertIn(FINISH['chrome'],finishes)
        self.assertEqual(len(set(fingerprints)),5)

    def test_base_is_deep_copied_and_reapplication_has_no_duplicate_trim(self):
        part = self.body()
        before = part.vertices.copy()
        result = apply_skin([part],CATALOG[0]['id'])
        self.assertFalse(hasattr(part,'skin_id'))
        self.assertEqual(part.decals,[])
        result[0].faces[0].vertices[0,0] += 1
        np.testing.assert_array_equal(part.vertices,before)
        first = apply_skin([part],CATALOG[0]['id'])
        again = apply_skin(first,CATALOG[0]['id'])
        self.assertEqual(len(first),len(again))
        self.assertEqual(len(first[0].decals),len(again[0].decals))
        np.testing.assert_allclose(bounds(first),bounds(again))

    def test_patterns_stay_in_model_coordinates_through_camera_transforms(self):
        part = apply_skin([self.body()],'tidal_pulse')[0]
        points = np.array([[21,12,8],[62,31,8],[90,40,8]],dtype=float)
        expected = sample_surface(part,points,[0,0,1],'tidal_pulse')
        for yaw,pitch in ((0,0),(-45,35.264),(90,-22),(180,90)):
            rotation = rotation_matrix(yaw,pitch)
            center = [32,11,0]
            projected = project(points,yaw,pitch,7,center,(96,96))
            view = projected.copy()
            view[:,:2] = (view[:,:2]-[48,48])/7
            reconstructed = view@rotation+center
            actual = sample_surface(part,reconstructed,[0,0,1],'tidal_pulse')
            np.testing.assert_allclose(actual[0],expected[0],atol=1e-10)
            np.testing.assert_array_equal(actual[1],expected[1])

    def test_all_seven_channels_accept_independent_palette_values(self):
        palette = {channel:f'#{20+i*25:02x}{40+i*15:02x}{55+i*11:02x}' for i,channel in enumerate(CHANNELS)}
        for channel in CHANNELS:
            part = self.body()
            part.channel = channel
            self.assertEqual(channel_for(part),channel)
            colors,_ = sample_surface(part,np.array([[3.,4.,8.]]),[0,0,1],None,palette)
            from PIL import ImageColor
            np.testing.assert_array_equal(colors[0],ImageColor.getrgb(palette[channel]))
        self.assertEqual(set(channel_palette([],{})),set(CHANNELS))
        legacy = channel_palette([],dict(primary='#112233',medium='#445566',dark='#778899',accent='#AABBCC'))
        self.assertEqual(legacy['MT_Metal'],'#445566')
        self.assertEqual(legacy['MT_Emission'],'#AABBCC')

    def test_palette_changes_channels_but_preserves_fixed_skin_accents(self):
        part = apply_skin([self.body()],'circuit_bloom')[0]
        # y=0: u=.05 uses secondary; u=.68 uses fixed warm accent.
        points = np.array([[5,0,8],[68,0,8],[80,0,8]],dtype=float)
        a,_ = sample_surface(part,points,[0,0,1],'circuit_bloom',{'primary':'#E0D0B0','medium':'#485868'})
        b,_ = sample_surface(part,points,[0,0,1],'circuit_bloom',{'primary':'#887060','medium':'#A0B0C0'})
        np.testing.assert_array_equal(a[1],b[1])
        self.assertFalse(np.array_equal(a[0],b[0]))
        self.assertFalse(np.array_equal(a[2],b[2]))
        trim = part.decals[0]
        ca,_ = sample_surface(trim,points,[0,0,1],'circuit_bloom',{'MT_Detail':'#ffffff'})
        cb,_ = sample_surface(trim,points,[0,0,1],'circuit_bloom',{'MT_Detail':'#000000'})
        np.testing.assert_array_equal(ca,cb)

    def test_trim_attaches_to_host_and_stays_within_small_surface_envelope(self):
        body = self.body()
        model = apply_skin([body],'chrome_crest')
        lo,hi = bounds([body])
        for part in model[1:]:
            self.assertTrue(part.skin_trim)
            self.assertEqual(part.skin_host,0)
            self.assertFalse(part.label)
            pl,ph = bounds([part])
            self.assertTrue(np.all(pl>=lo-[0,0,1]))
            self.assertTrue(np.all(ph<=hi+[0,0,1]))
            self.assertTrue(pl[2]<=hi[2] and ph[2]>=lo[2])
            self.assertLess(min(abs(pl[2]-hi[2]),abs(ph[2]-lo[2])),.03)
        for item in model[0].decals:
            self.assertTrue(_inside(item.vertices[:,:2],body.faces[1].vertices[:,:2]).all())
            self.assertLess(np.min(abs(abs(item.vertices[:,2])-8)),.06)
        result = render(model,yaw=0,pitch=0,size=(140,90),skin='chrome_crest',textured=True)
        self.assertEqual(set(result.anchors),{'Gehäuse'})

    def test_fully_covered_front_gets_no_floating_badge_or_ribs(self):
        body = self.body()
        blocker = prism([(-5,-5),(105,-5),(105,55),(-5,55)],'#303844',8,12)
        blocker.material = 'rubber'
        blocker.label = 'Kontaktfläche'
        model = apply_skin([body,blocker],'gilt_vector')
        self.assertTrue(model[0].decals)
        self.assertTrue(all(np.max(d.vertices[:,2])<0 for d in model[0].decals))
        self.assertEqual(model[1].decals,[])
        self.assertTrue(all(np.max(p.vertices[:,2])<0 for p in model[2:]))

    def test_optics_lights_trigger_and_rubber_remain_functional(self):
        for attr,value in (('sight',True),('emit',True),('material','rubber'),('label','Abzug'),('label','Pfeilauflage')):
            part = self.body()
            setattr(part,attr,value)
            model = apply_skin([part],'circuit_bloom')
            self.assertEqual(len(model),1)
            self.assertEqual(model[0].decals,[])
            point = np.array([[60.,20.,8.]])
            base,_ = sample_surface(model[0],point,[0,0,1])
            skin,_ = sample_surface(model[0],point,[0,0,1],'circuit_bloom')
            np.testing.assert_array_equal(base,skin)

    def test_opposite_badges_reflect_world_x_for_readable_numbers(self):
        model = apply_skin([self.body()],'circuit_bloom')
        plus = [d for d in model[0].decals if d.vertices[:,2].mean()>0]
        minus = [d for d in model[0].decals if d.vertices[:,2].mean()<0]
        self.assertEqual(len(plus),len(minus))
        # Different fits may be positioned independently; compare centred shapes.
        for a,b in zip(plus,minus):
            va = a.vertices[:,:2]-a.vertices[:,:2].mean(axis=0)
            vb = b.vertices[:,:2]-b.vertices[:,:2].mean(axis=0)
            self.assertAlmostEqual(np.ptp(va[:,0]),np.ptp(vb[:,0]))
            # Compare point sets because outward face winding also reverses.
            expected = sorted(map(tuple,np.round(va*[-1,1],7)))
            actual = sorted(map(tuple,np.round(vb,7)))
            self.assertEqual(expected,actual)

    def test_no_bloom_pixels_outside_geometry(self):
        part = self.body()
        part.emit=True
        result = render([part],yaw=0,pitch=0,size=(80,60),scale=.5,center=[50,25,0])
        self.assertEqual(result.image.getpixel((5,5))[3],0)
        self.assertEqual(result.image.getpixel((40,30))[3],255)


if __name__=='__main__':
    unittest.main()
