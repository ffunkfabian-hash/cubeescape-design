"""Construction regressions for both upgraded Codex families."""
from collections import Counter
from pathlib import Path
import sys
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from collections_codex import load_collection
from build import validate_model, geometry_hash
from authoring import _inside
from eng import bounds
from spec import design_spec


def x_hits(part, y, z):
    hits=[]
    for f in part.faces:
        if abs(f.normal[0])<1e-9:continue
        if _inside((y,z), f.vertices[:,1:]):
            x=float(f.vertices[0,0]-(f.normal[1]*(y-f.vertices[0,1])+f.normal[2]*(z-f.vertices[0,2]))/f.normal[0])
            hits.append(x)
    return hits


class UpgradedTests(unittest.TestCase):
    def test_both_families_are_reproducible_closed_and_exportable(self):
        for family in ('fluxbloom','parallax'):
            first=load_collection(family);second=load_collection(family)
            self.assertEqual(len(first),10)
            for (meta,model),(_,again) in zip(first,second):
                with self.subTest(family=family,weapon=meta['slug']):
                    validate_model(meta,model)
                    self.assertEqual(geometry_hash(model),geometry_hash(again))
                    boxes=[bounds([p]) for p in model]
                    connected={0}
                    while True:
                        adjacent={i for i in range(len(model)) if i not in connected and any(
                            np.all(boxes[i][0]<=boxes[j][1]+1.1) and np.all(boxes[j][0]<=boxes[i][1]+1.1) for j in connected)}
                        if not adjacent:break
                        connected|=adjacent
                    self.assertEqual(len(connected),len(model),(family,meta['slug'],[p.label for i,p in enumerate(model) if i not in connected]))
                    self.assertEqual(len(meta['notes']),len(next(m for m,_ in second if m['slug']==meta['slug'])['notes']))
                    for p in model:
                        edges=Counter()
                        for f in p.faces:
                            self.assertLess(np.max(np.abs((f.vertices-f.vertices[0])@f.normal)),1e-6)
                            v=[tuple(np.round(x,7)) for x in f.vertices]
                            for a,b in zip(v,v[1:]+v[:1]):edges[tuple(sorted((a,b)))]+=1
                        self.assertEqual(set(edges.values()),{2},(family,meta['slug'],p.label))

    def test_reference_data_matches_each_upgraded_collection(self):
        for family in ('fluxbloom','parallax'):
            for number,(meta,model) in enumerate(load_collection(family),1):
                record={'orthographic_views':[], 'geometry_sha256':geometry_hash(model)}
                data=design_spec(meta,model,number,record)
                self.assertEqual(data['sheet']['id'],f"K{meta['variant']}{number:02d}")
                self.assertEqual(data['sight']['type'],meta['sight_type'])
                self.assertEqual(len(data['parts']),len(model))
                self.assertTrue(data['sight']['window_geometry'])
                self.assertFalse(data['compatibility']['toolgen_import_validated'])
                self.assertEqual(len(data['skin']['catalog']),5)
                if meta['slug']=='bow':self.assertTrue(data['moving_parts']['items'])

    def test_functional_optic_apertures_are_clear_along_barrel(self):
        for family in ('fluxbloom','parallax'):
            for meta,model in load_collection(family):
                optics=[p for p in model if p.sight]
                window=next(p.window_geometry for p in optics if getattr(p,'sight_window',False))
                c=window['center_model'];w=window['width_model'];h=window['height_model']
                for fy,fz in ((0,0),(-.3,-.3),(.3,.3),(-.3,.3),(.3,-.3)):
                    blocked=[p.label for p in model if x_hits(p,c[1]+fy*h,c[2]+fz*w)]
                    self.assertEqual(blocked,[],(family,meta['slug'],blocked))
                self.assertEqual(window['normal_model'],[1,0,0])
                if meta['slug']=='trace':
                    self.assertFalse(any(p.label=='Optikröhre' for p in optics))
                    self.assertTrue(any(p.label=='Markierungsrahmen' for p in optics))

    def test_bow_arrow_corridor_is_clear_of_riser_and_guides(self):
        for family in ('fluxbloom','parallax'):
            meta,model=next((m,p) for m,p in load_collection(family) if m['slug']=='bow')
            arrow=next(p for p in model if p.label=='Pfeilschaft')
            lo,hi=bounds([arrow]);y,z=((lo+hi)/2)[1:]
            self.assertAlmostEqual(lo[0],-120 if family=='parallax' else -50)
            blocked=[]
            for p in model:
                if p.sight or getattr(p,'projectile',False) or 'Sehne' in p.label:continue
                if any(lo[0]+2<x<hi[0] for x in x_hits(p,y,z)):blocked.append(p.label)
            self.assertEqual(blocked,[],(family,blocked))
