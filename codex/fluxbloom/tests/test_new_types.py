"""New concepts: identities, mandatory mechanisms, conservative handover data."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys
import unittest
import numpy as np
import jsonschema
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from collections_codex import load_collection
from design_types import NEW, weapon_fields, type_key
from texture_profile import profile
from build import validate_model, geometry_hash
from eng import bounds
from weapon_spec import make_spec

REQUIRED = dict(scout={'Magazin','Verschluss'}, handcannon={'Trommel','Hahn'},
 linear={'Ladekammer','Beschleunigerschiene'}, breech={'Kipplauf'}, drum={'Granattrommel','Ladeklappe'},
 machine={'Munitionskasten','Patronengurt','Zuführdeckel'}, sword={'Klinge','Parierstange','Energiezelle'},
 glaive={'Klinge','Emitter','Schildflügel'}, crossbow={'Wurfarm','Sehne','Spannhebel'},
 rocketside={'Raketenmagazin'},rocketpulse={'Raketenmagazin'},slug={'Slug-Magazin'},
 heat={'Hitzespeicher','Entlüftungsklappe'},micro={'Raketenvorrat','Ladeklappe'},spread={'Kipprahmen','Trommel'})


class NewTypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [(n,m,w) for family in ('parallax','fluxbloom')
                    for n,(m,w) in enumerate(load_collection(family,include_new=True),1) if n>10]

    def test_30_independent_constructions_and_class_specific_labels(self):
        self.assertEqual(len(self.rows),30)
        self.assertEqual(len({geometry_hash(w) for _,_,w in self.rows}),30)
        for n,m,w in self.rows:
            validate_model(m,w)
            labels={p.label for p in w if not p.sight}
            self.assertTrue(REQUIRED[m['slug']] <= labels,(m['variant'],n,REQUIRED[m['slug']]-labels))
            if m['slug'] in ('sword','glaive'):
                self.assertFalse(any(p.sight for p in w))
                self.assertNotIn('Visierschiene',labels)
            if m['slug']=='sword': self.assertFalse({'Abzug','Bügel'} & labels)
            if m['slug']=='heat': self.assertFalse(any('magazin' in str(p.label).lower() for p in w))
            for key in ('reload','action','fire'):
                self.assertTrue(all(0<len(m['operation_intent'][key][lang])<=180 for lang in ('de','en')))

    def test_new_parts_closed_planar_and_connected(self):
        for n,m,w in self.rows:
            weapon=[p for p in w if not p.sight]
            for part in weapon:
                edges=Counter()
                for f in part.faces:
                    self.assertLess(float(np.max(np.abs((f.vertices-f.vertices[0])@f.normal))),1e-6,(m['variant'],n,part.label))
                    points=[tuple(np.round(v,6)) for v in f.vertices]
                    for a,b in zip(points,points[1:]+points[:1]): edges[tuple(sorted((a,b)))]+=1
                self.assertEqual(set(edges.values()),{2},(m['variant'],n,part.label))
            boxes=[bounds([p]) for p in weapon]; connected={0}
            while True:
                adjacent={i for i in range(len(weapon)) if i not in connected and any(
                    np.all(boxes[i][0]<=boxes[j][1]+1.1) and np.all(boxes[j][0]<=boxes[i][1]+1.1) for j in connected)}
                if not adjacent: break
                connected |= adjacent
            self.assertEqual(len(connected),len(weapon),(m['variant'],n,[p.label for i,p in enumerate(weapon) if i not in connected]))
            # A seated magazine may overlap the grip/socket, never the guard.
            guards=[p for p in weapon if p.label=='Bügel']
            magazines=[p for p in weapon if p.label in ('Magazin','Raketenmagazin','Slug-Magazin','Trommel','Granattrommel')]
            for guard in guards:
                for magazine in magazines:
                    a,b=bounds([guard]),bounds([magazine])
                    overlap=np.minimum(a[1],b[1])-np.maximum(a[0],b[0])
                    self.assertFalse(np.all(overlap>1e-7),(m['variant'],n,'Bügel in '+magazine.label))

    def test_new_type_and_profile_facts_match_read_only_shared_catalogue(self):
        loc=importlib.util.spec_from_file_location('type_facts_read_only',HERE.parents[1]/'claude/generator/wtypes.py')
        facts=importlib.util.module_from_spec(loc);loc.loader.exec_module(facts)
        sys.path.append(str(HERE.parents[1]/'claude/generator'))
        loc=importlib.util.spec_from_file_location('profile_facts_read_only',HERE.parents[1]/'claude/generator/texprofile.py')
        profiles=importlib.util.module_from_spec(loc);loc.loader.exec_module(profiles)
        for n,m,w in self.rows:
            ours=weapon_fields(m); shared=facts.TYPES[m['kind']]
            for a,b in [('design_type','id'),('design_type_de','de'),('destiny_type','en'),('subtype','subtype'),('ammo_class','ammo')]:
                self.assertEqual(ours[a],shared[b],(m['variant'],n,a))
            self.assertEqual(NEW[m['slug']][5],shared['ref_len'])
            self.assertEqual(None if NEW[m['slug']][6] is None else f'VS{NEW[m["slug"]][6]:02d}', shared['vs'])
            self.assertEqual(ours['toolgen_status'],'not_connected')
            proposed=profile(type_key(m['slug']))
            reference=profiles.profile(type_key(m['slug']))
            self.assertIn('Vorschlag',proposed['source'])
            self.assertEqual(proposed['derived_from'],reference['derived_from'])
            for key,field in [('housing','material'),('metal','material'),('rubber','material'),('energy','color'),('edge_wear','level'),('decals','toolgen')]:
                self.assertEqual(proposed[key][field],reference[key][field],(m['variant'],n,key))

    def test_handover_does_not_claim_connected_tools_elements_or_robot_fit(self):
        schemas=[jsonschema.Draft202012Validator(json.loads(p.read_text())) for p in
                 [HERE/'weapon-spec.schema.json',HERE.parents[1]/'claude/docs/weapon-spec.schema.json']]
        for n,m,w in self.rows:
            sp=make_spec(m,w,n)
            for schema in schemas: schema.validate(sp)
            self.assertIsNone(sp['weapon']['toolgen_id'])
            self.assertIsNone(sp['element'])
            self.assertFalse(sp['robot_fit']['applies'])
            self.assertIsNone(sp['robot_fit']['sheet_at_target'])
            self.assertTrue(sp['moving_parts']['proposed'])
            for motion in sp['moving_parts']['items']:
                self.assertTrue(motion['proposed'])
                self.assertTrue(motion['parts'],(m['variant'],n,motion['kind']))
            for key in ('reload','action','fire'):
                self.assertEqual(sp['operation'][key],m['operation_intent'][key])

if __name__=='__main__':unittest.main()
