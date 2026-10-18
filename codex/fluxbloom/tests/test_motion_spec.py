"""Contract motion axes and conservative label matching, independent of images."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collections_codex import load_collection
from motion_spec import make_moving_parts


class MotionSpecTests(unittest.TestCase):
    def test_pump_matches_actual_front_grip_in_both_families(self):
        for family in ('parallax','fluxbloom'):
            meta,model=next((m,p) for m,p in load_collection(family) if m['slug']=='shotgun')
            row=make_moving_parts(meta,model)['items'][0]
            self.assertEqual(row['kind'],'pump')
            self.assertEqual(row['motions'],[{'type':'translate','axis':[0,1,0]}])
            self.assertTrue(row['parts'])
            for pid in row['parts']:self.assertIn(model[int(pid[1:])].label,('Pumpgriff','Pumpmanschette'))

    def test_no_magazine_guess_and_bow_has_no_use_clip(self):
        for family in ('parallax','fluxbloom'):
            for meta,model in load_collection(family):
                data=make_moving_parts(meta,model)
                self.assertFalse(data['root_moves'])
                if meta['slug']=='bow':self.assertEqual(data['items'],[])
                for row in data['items']:
                    if row['parts'] is None:
                        self.assertIsNone(row['match'])
                        self.assertIn('no named',row['source'])
                    else:
                        self.assertTrue(all(not model[int(pid[1:])].sight for pid in row['parts']))
                        self.assertFalse(any('Magazin' in model[int(pid[1:])].label for pid in row['parts']))
