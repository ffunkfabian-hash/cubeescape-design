"""Contract and construction checks for the new experimental collection."""
import sys
from pathlib import Path
import unittest
from collections import Counter
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import validate_model, geometry_hash
from eng import bounds
from models import load_all
from spec import design_spec


class CollectionTests(unittest.TestCase):
    def test_ten_new_named_designs_share_series_but_not_geometry(self):
        models = load_all()
        self.assertEqual(len(models), 10)
        self.assertEqual(len({meta['slug'] for meta, _ in models}), 10)
        self.assertEqual(len({geometry_hash(m) for _, m in models}), 10)
        for meta, m in models:
            with self.subTest(weapon=meta['slug']):
                validate_model(meta, m)
                self.assertEqual(meta['variant'], 'K')
                self.assertEqual(meta['variant_name'], 'Flux Bloom')
                self.assertEqual(len(meta['palette']), 4)
                roles = dict(zip(('primary','medium','dark','accent'),meta['palette']))
                for p in m:
                    self.assertEqual(p.color.lower(), roles[p.role].lower())
                    self.assertIn(p.material, ('paint','metal','rubber','plastic','light'))

    def test_faces_are_planar_closed_and_assemblies_have_no_detached_parts(self):
        for meta, model in load_all():
            parts = [p for p in model if not p.sight]
            for p in model:
                edges = Counter()
                for f in p.faces:
                    with self.subTest(weapon=meta['slug'],part=p.label):
                        self.assertLess(float(np.max(np.abs((f.vertices-f.vertices[0]) @ f.normal))), 1e-6)
                    v = [tuple(np.round(x,7)) for x in f.vertices]
                    for a,b in zip(v,v[1:]+v[:1]):
                        edges[tuple(sorted((a,b)))] += 1
                self.assertEqual(set(edges.values()), {2}, (meta['slug'],p.label))
            boxes = [bounds([p]) for p in parts]
            connected = {0}
            while True:
                adjacent = {i for i in range(len(parts)) if i not in connected and any(
                    np.all(boxes[i][0] <= boxes[j][1]+1.1) and
                    np.all(boxes[j][0] <= boxes[i][1]+1.1) for j in connected)}
                if not adjacent:break
                connected |= adjacent
            self.assertEqual(len(connected),len(parts),(meta['slug'],[p.label for i,p in enumerate(parts) if i not in connected]))

    def test_pistol_cell_and_trigger_remain_visible_in_isometry(self):
        from raster import render
        model = next(m for meta,m in load_all() if meta['slug']=='pistol')
        result = render([p for p in model if not p.sight],size=(400,250))
        self.assertIn('Magazin',result.anchors)
        self.assertIn('Abzug',result.anchors)
        trigger = next(p for p in model if p.label=='Abzug')
        self.assertEqual(trigger.role,'accent')

    def test_specs_identify_variant_and_export_same_model_polygons(self):
        for n,(meta,model) in enumerate(load_all(),1):
            record={'orthographic_views': [], 'geometry_sha256':geometry_hash(model)}
            spec=design_spec(meta,model,n,record)
            self.assertEqual(spec['sheet']['id'],f'KK{n:02d}')
            self.assertEqual(spec['sheet']['variant_name'],'Flux Bloom')
            self.assertEqual(len(spec['parts']),len(model))
            self.assertEqual(spec['geometry_sha256'],geometry_hash(model))
            self.assertTrue(spec['reference_only'])
            self.assertTrue(any(p['sight'] for p in spec['parts']))
            for source, exported in zip(model,spec['parts']):
                self.assertEqual(len(source.faces),len(exported['faces']))
                for face, data in zip(source.faces,exported['faces']):
                    np.testing.assert_allclose(face.vertices,data['vertices'],atol=1e-7)

    def test_rocket_left_rail_and_bore(self):
        from raster import render
        model = next(m for meta,m in load_all() if meta['slug']=='rocket')
        rail = next(p for p in model if p.label=='Visierschiene')
        self.assertGreater(bounds([rail])[0][2],0)
        tube = next(p for p in model if p.label=='Lauf')
        lo, hi = bounds([tube]); center = (lo+hi)/2
        result = render([p for p in model if not p.sight],yaw=-90,pitch=0,size=(100,100),scale=1,center=center)
        self.assertEqual(result.image.getpixel((50,50))[3],0)


if __name__ == '__main__':
    unittest.main()
