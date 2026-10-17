"""Model contracts for downstream design-sheet consumers."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import validate_model, geometry_hash
from eng import bounds
from models import load_all
import numpy as np


class ModelContractTests(unittest.TestCase):
    def test_ten_distinct_designs_have_required_functional_parts(self):
        models = load_all()
        self.assertEqual(len(models), 10)
        self.assertEqual(len({meta['slug'] for meta, _ in models}), 10)
        self.assertEqual(len({geometry_hash(model) for _, model in models}), 10)
        for meta, model in models:
            with self.subTest(weapon=meta['slug']):
                checks = validate_model(meta, model)
                self.assertGreater(checks['optic_parts'], 1)
                self.assertTrue(all(p.role in ('primary','medium','dark','accent') for p in model))
                self.assertTrue(all(p.material in ('paint','metal','rubber','plastic','light') for p in model))

    def test_every_solid_has_planar_faces_and_outward_unit_normals(self):
        for meta, model in load_all():
            for part in model:
                for face in part.faces:
                    with self.subTest(weapon=meta['slug'], part=part.label):
                        distances = (face.vertices - face.vertices[0]) @ face.normal
                        self.assertLess(float(np.max(np.abs(distances))), 1e-6)
                        self.assertAlmostEqual(float(np.linalg.norm(face.normal)), 1., places=6)
                        # Outward normal follows polygon winding, even for nonconvex profiles.
                        n = np.sum(np.cross(face.vertices,np.roll(face.vertices,-1,axis=0)),axis=0)
                        self.assertGreater(float(n @ face.normal), 0.)

    def test_rocket_rail_is_on_left_and_barrel_axis_is_forward(self):
        model = next(m for meta, m in load_all() if meta['slug']=='rocket')
        rail = next(p for p in model if p.label=='Visierschiene')
        lo, hi = bounds([rail])
        self.assertGreater(lo[2], 0.)
        barrel = next(p for p in model if p.label=='Lauf')
        lo, hi = bounds([barrel])
        # A launcher sleeve may be shorter than its diameter; ring centers still share the x axis.
        ends = [barrel.vertices[np.isclose(barrel.vertices[:,0], x)] for x in (lo[0], hi[0])]
        np.testing.assert_allclose(ends[0][:,1:].mean(axis=0), ends[1][:,1:].mean(axis=0), atol=1e-8)

    def test_solid_surfaces_are_closed_and_parts_form_a_connected_assembly(self):
        from collections import Counter
        for meta, model in load_all():
            parts = [p for p in model if not p.sight]
            for part in parts:
                edges = Counter()
                for face in part.faces:
                    v = [tuple(np.round(x, 7)) for x in face.vertices]
                    for a, b in zip(v, v[1:] + v[:1]):
                        edges[tuple(sorted((a, b)))] += 1
                with self.subTest(weapon=meta['slug'], part=part.label):
                    self.assertEqual(set(edges.values()), {2})
            boxes = [bounds([p]) for p in parts]
            connected = {0}
            while True:
                neighbors = {i for i in range(len(parts)) if i not in connected and any(
                    np.all(boxes[i][0] <= boxes[j][1] + 1.1) and
                    np.all(boxes[j][0] <= boxes[i][1] + 1.1) for j in connected)}
                if not neighbors:
                    break
                connected |= neighbors
            # Broad-phase check only; visual inspection still checks the actual joints.
            self.assertEqual(len(connected), len(parts), meta['slug'])

    def test_rocket_has_an_unobstructed_axial_bore(self):
        from raster import render
        model = next(m for meta, m in load_all() if meta['slug'] == 'rocket')
        model = [p for p in model if not p.sight]
        front = render(model, yaw=-90, pitch=0, size=(100,100), scale=1,
                       center=np.array((0., -24., 0.)))
        self.assertEqual(front.image.getpixel((50,50))[3], 0)
        self.assertGreater(np.count_nonzero(np.asarray(front.image)[:,:,3]), 100)

    def test_sniper_exposed_barrel_is_slim_and_stock_has_shaped_profile(self):
        model = next(m for meta,m in load_all() if meta['slug']=='sniper')
        barrel = next(p for p in model if p.label=='Lauf')
        lo, hi = bounds([barrel])
        self.assertGreater((hi-lo)[0], 5 * max((hi-lo)[1:]))
        stock = next(p for p in model if p.label=='Schaft')
        self.assertGreater(len(stock.faces[0].vertices), 4)


if __name__ == '__main__':
    unittest.main()
