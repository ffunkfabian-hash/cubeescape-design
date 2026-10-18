"""VS measurements independently checked against read-only source Sight-Specs."""
from copy import deepcopy
from collections import Counter
import json
import os
from pathlib import Path
import sys
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vs_models import build_sight,DESIGNS,solid
from vs_mount import TO_NATIVE,line_blockers
from collections_codex import load_collection
from weapon_spec import make_spec,MATRIX
from sight_validation import aperture_blockers
from eng import bounds,Part,prism

REFERENCE=Path(os.environ.get('CODEX_VS_REFERENCE',Path.home()/'Library/Caches/CubeEscapeDesign/vs-reference'))

class SightSeriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs={n:json.loads((REFERENCE/f'VS{n:02d}.spec.json').read_text()) for n in range(1,10)}
        cls.rows=[(n,m,p) for fam in ('parallax','fluxbloom') for n,(m,p) in enumerate(load_collection(fam),1)]

    def test_named_parts_materials_and_envelopes_match_reference_half_mm(self):
        aliases={'paint':'painted','metal':'brushed','light':'lit'}
        for n,ref in self.refs.items():
            parts=build_sight(n)
            self.assertEqual(len(parts),len(ref['parts']))
            for p,expected in zip(parts,ref['parts']):
                with self.subTest(sight=n,part=p.label):
                    self.assertEqual(p.label,expected['label'])
                    self.assertEqual(aliases.get(p.material,p.material),expected['material'])
                    self.assertEqual(p.channel,expected['channel'])
                    np.testing.assert_allclose(np.array(bounds([p]))*.001,expected['bounds_m'],atol=.0005)
            lo,hi=bounds(parts);dim=ref['dimensions_m']
            np.testing.assert_allclose((hi-lo)*.001,[dim['width'],dim['length'],dim['height']],atol=.0005)
            window=ref['window'];d=DESIGNS[n]
            np.testing.assert_allclose(np.array(d['opening'])*.001,
                [window['width_m'],window['height_m'],window['corner_radius_m']],atol=.0005)
            self.assertEqual(d['shape'],window['shape'])
            np.testing.assert_allclose([0,d['rear']*.001,d['reticle'][2]*.001],ref['anchors']['Socket_Sight']['position_m'],atol=.0005)

    def test_all_reference_anchors_and_window_centres_half_mm(self):
        for n,m,parts in self.rows:
            if n==10:continue
            s=make_spec(m,parts,n);ref=self.refs[n];vs=s['sight']['sight_spec']
            mount=np.array(vs['socket_mount_m'])
            for key,anchor in (('socket_reticle_m','Socket_Reticle'),('socket_eye_m','Socket_Eye')):
                if ref['anchors'][anchor] is None:self.assertIsNone(vs[key]);continue
                np.testing.assert_allclose(np.array(vs[key])-mount,ref['anchors'][anchor]['position_m'],atol=.0005)
            self.assertEqual(s['sight']['type'],ref['sight']['type']);self.assertEqual(s['sight']['frame'],ref['sight']['frame'])
            rail=s['parts'][int(vs['rail']['part'][1:])]['bounds_m'];seat=s['anchors']['Socket_Sight']['position_m']
            self.assertAlmostEqual(seat[2],rail[1][2],places=6)
            self.assertAlmostEqual(seat[1],(rail[0][1]+rail[1][1])/2,places=6)
            np.testing.assert_allclose(mount,np.asarray(seat)+[0,0,vs['riser_m']],atol=1e-7)
            panes=[p for p in s['parts'] if p['material']=='glass']
            self.assertEqual(len(panes),len(ref['window_geometry']['elements']))
            self.assertEqual({e['part'] for e in s['sight']['window_geometry']['elements']},{p['id'] for p in panes})
            for p in panes:
                self.assertIsNone(p['toolgen_material'])
                self.assertEqual(p['color'],ref['glass']['srgb'].upper())
                ext=np.ptp(np.array(p['bounds_m']),axis=0);self.assertEqual(int(ext.argmin()),1)
            # Reconstructed pane centroids are the actual exported optical anchors.
            centre=np.mean(panes[0]['bounds_m'],axis=0)
            np.testing.assert_allclose(centre,vs['socket_reticle_m'],atol=.0005)

    def test_dense_aperture_clear_and_detects_off_axis_obstruction(self):
        for n in range(1,10):
            parts=build_sight(n);d=DESIGNS[n]
            rays,blocked=aperture_blockers(parts,d)
            self.assertGreater(rays,500);self.assertEqual(blocked,[],(n,blocked))
            # Off-axis 0.9 mm peg: misses centre but must fail the dense test.
            cx,cy,cz=d['reticle'];peg=Part(solid((cx+2,cy-1,cz+2,cx+2.9,cy+1,cz+2.9)), '#000000',label='counterexample')
            self.assertIn('counterexample',aperture_blockers(parts+[peg],d)[1])

    def test_objective_collar_reaches_housing_without_longitudinal_gap(self):
        for n in (3,5):
            parts=build_sight(n)
            frame=next(p for p in parts if p.label=='Rahmen')
            housing=next(p for p in parts if p.label=='Gehäuse')
            front=bounds([frame])[0][1];join=bounds([housing])[0][1]
            # At several axial slices before the housing a real annular wall
            # must exist; an overall component envelope would hide a gap.
            from sight_validation import _ray_intervals
            points=np.array([(y,DESIGNS[n]['reticle'][2]) for y in np.linspace(front+.1,join-.1,20)])
            left,right,inside=_ray_intervals(frame,points)
            self.assertTrue(np.all(inside.any(axis=1)),n)

    def test_added_rail_has_integral_pedestal_touching_weapon_roof(self):
        from vs_mount import mount_sight
        body=prism([(-50,0),(50,0),(50,15),(-50,15)],'#808080',-5,5)
        body.label='Gehäuse';body.channel='MT_Secondary'
        meta={'slug':'pistol','palette':['#eeeeee','#808080','#202020','#ff8800']}
        model=mount_sight(meta,[body]);rail=next(p for p in model if p.label=='Visierschiene')
        self.assertTrue(meta['vs_rail_added'])
        self.assertAlmostEqual(bounds([rail])[1][1],bounds([body])[0][1])
        from sight_validation import solids_overlap
        self.assertFalse(solids_overlap(rail,body,.1,.01))

    def test_mounted_dense_apertures_and_forward_line_are_clear(self):
        for n,m,model in self.rows:
            if n==10:continue
            s=make_spec(m,model,n);unit=s['units']['model_unit_m']*1000;mount=np.array(m['vs_mount_model'])
            sight=deepcopy([p for p in model if hasattr(p,'vs_part')])
            for p in sight:
                for f in p.faces:
                    f.vertices=(f.vertices-mount)@TO_NATIVE*unit;f.normal=TO_NATIVE.T@f.normal
            self.assertEqual(aperture_blockers(sight,DESIGNS[n])[1],[])
            c=np.array(DESIGNS[n]['reticle'])@TO_NATIVE.T/unit+mount
            start=mount[0]-DESIGNS[n]['rear']/unit
            self.assertEqual(line_blockers(model,c,start),[])
            # Block in front of the mounted optic; declared clear flags cannot hide it.
            p=prism([(start+20,c[1]-2),(start+22,c[1]-2),(start+22,c[1]+2),(start+20,c[1]+2)],'#000000',c[2]-2,c[2]+2)
            self.assertIn(p,line_blockers(model+[p],c,start))

    def test_bow_rear_pin_dot_aligned_with_forward_axis(self):
        for n,m,model in self.rows:
            if n!=10:continue
            pin=next(p for p in model if p.label=='Visierpin');dot=next(p for p in model if p.label=='Leuchtpunkt')
            dlo,dhi=bounds([dot]);plo,phi=bounds([pin])
            self.assertLess(dhi[0],plo[0])
            self.assertAlmostEqual((dlo[2]+dhi[2])/2,(plo[2]+phi[2])/2)
            self.assertGreaterEqual((dlo[1]+dhi[1])/2,plo[1])
            self.assertEqual(int(np.argmin(dhi-dlo)),0)

    def test_no_opaque_sight_volume_penetrates_weapon(self):
        from sight_validation import solids_overlap
        for n,m,model in self.rows:
            if n==10:continue
            # 0.5 mm ray spacing, 0.2 mm penetration threshold; no AABB-only claims.
            lo,hi=bounds([p for p in model if not p.sight])
            from spec import LENGTHS_M
            mm=LENGTHS_M[m['slug']]/(hi[0]-lo[0])*1000
            for sight in model:
                if not sight.sight or sight.material=='glass':continue
                for weapon in model:
                    if weapon.sight or weapon.label=='Visierschiene':continue
                    self.assertFalse(solids_overlap(sight,weapon,.5/mm,.2/mm),(m['variant'],n,sight.label,weapon.label))
        a=Part(solid((0,0,0,2,2,2)), '#000000')
        b=Part(solid((1,1,1,3,3,3)), '#000000')
        self.assertTrue(solids_overlap(a,b,.5,.2))

class GlassRenderingTests(unittest.TestCase):
    def test_glass_is_two_sided_translucent_tinted_and_depth_tested(self):
        from raster import render
        from eng import Face
        pane=Part([Face([[-8,-8,0],[8,-8,0],[8,8,0],[-8,8,0]],[0,0,1])], '#3D9BEA',material='glass')
        pane.glass_alpha=.28
        view=render([pane],yaw=0,pitch=0,size=(64,64),scale=3,ow=0,glow=False,textured=True,palette={'MT_Primary':'#FF0000'})
        pixel=view.image.getpixel((32,32))
        np.testing.assert_allclose(pixel[:3],[61,155,234],atol=2)
        self.assertTrue(70<=pixel[3]<=90,pixel)
        self.assertGreater(view.image.getpixel((8,32))[3],150)
        # Face winding does not make an optical pane disappear from the back.
        rear=render([pane],yaw=180,pitch=0,size=(64,64),scale=3,ow=0,glow=False)
        self.assertGreater(rear.image.getpixel((32,32))[3],60)
        wall=prism([(-9,-9),(9,-9),(9,9),(-9,9)],'#E0C0A0',1,2)
        opaque=render([wall],yaw=0,pitch=0,size=(64,64),scale=3,ow=0,glow=False)
        hidden=render([wall,pane],yaw=0,pitch=0,size=(64,64),scale=3,ow=0,glow=False)
        self.assertEqual(hidden.image.getpixel((32,32)),opaque.image.getpixel((32,32)))
        # The alpha field is a smooth monotone gradient, never hatch bands.
        alpha=np.asarray(view.image)[32,14:50,3].astype(float)
        self.assertLessEqual(np.max(np.abs(np.diff(alpha,n=2))),2)
