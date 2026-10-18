"""Canonical v1 contract and semantic checks against both schemas and source models."""
import json
from pathlib import Path
import sys
import unittest
import numpy as np
HERE=Path(__file__).resolve().parents[1]
REPO=HERE.parents[1]
sys.path.insert(0,str(HERE))
from collections_codex import load_collection
from weapon_spec import make_spec, dump, TOOLGEN, CHANNELS, MATRIX, PALETTES
from texture_catalog import catalog, skin as catalog_skin
from PIL import ImageColor
from skins import CATALOG, apply_skin, sample_surface, channel_palette, channel_for, _contrast, FINISH

def _rgb(color):
    return np.asarray(ImageColor.getrgb(color)[:3],dtype=float)


def _inside_yz(points,poly):
    # Independent ray crossing evaluation of the exported canonical polygons.
    x,y=np.asarray(points).T
    poly=np.asarray(poly); result=np.zeros(len(x),dtype=bool)
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        if abs(b[1]-a[1])>1e-15:
            result^=((a[1]>y)!=(b[1]>y)) & (x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])
    return result


def _source_mask(mask,u,v):
    kind=mask['kind']
    if kind in ('all','any'):
        masks=[_source_mask(child,u,v) for child in mask['of']]
        return np.logical_and.reduce(masks) if kind=='all' else np.logical_or.reduce(masks)
    if kind=='ellipse_rings':
        radius=np.hypot((u-mask['center'][0])*mask['scale'][0],(v-mask['center'][1])*mask['scale'][1])
        return np.logical_or.reduce([(radius>low)&(radius<high) for low,high in mask['ranges']])
    value={'u':u,'v':v,'diagonal':u+mask.get('k',0)*v,
           'sawtooth':np.mod(mask.get('fu',0)*u+mask.get('fv',0)*v,1)}[kind]
    result=np.ones(len(u),dtype=bool)
    if mask.get('lo') is not None: result &= value>mask['lo']
    if mask.get('hi') is not None: result &= value<mask['hi']
    return result


def _linear_mask(mask):
    return mask['kind']!='ellipse_rings' and all(_linear_mask(child) for child in mask.get('of',[]))


class CanonicalWeaponSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=[(i,m,w) for series in ('fluxbloom','parallax')
                  for i,(m,w) in enumerate(load_collection(series),1)]
        cls.specs={(m['variant'],m['slug']):make_spec(m,w,i) for i,m,w in cls.rows}
    def spec_for(self,index,meta,model):
        return self.specs[(meta['variant'],meta['slug'])]
    def test_all_twenty_specs_validate_own_and_official_read_only_schemas(self):
        try:
            import jsonschema
        except ImportError as exc:
            raise RuntimeError('Install the declared test dependency: python -m pip install -r requirements.txt') from exc
        local=json.loads((HERE/'weapon-spec.schema.json').read_text())
        official=json.loads((REPO/'claude/docs/weapon-spec.schema.json').read_text())
        self.assertEqual(len(self.rows),20)
        for number,meta,model in self.rows:
            with self.subTest(variant=meta['variant'],weapon=meta['slug']):
                spec=self.spec_for(number,meta,model)
                jsonschema.Draft202012Validator(local).validate(spec)
                jsonschema.Draft202012Validator(official).validate(spec)
                tid,length,_=TOOLGEN[meta['slug']]
                self.assertEqual(spec['weapon']['toolgen_id'],tid)
                self.assertLessEqual(abs(spec['units']['model_unit_m']*spec['units']['model_length_units']-length),.0005)
                self.assertEqual(spec['format'],'cubeescape-design/weapon-spec')
                self.assertIsNone(spec['generator']['claude_version'])
                expected_version = ('0.2.3' if meta['variant']=='K' else '0.1.3') if meta['slug']=='bow' else ('0.2.5' if meta['variant']=='K' else '0.1.5')
                self.assertEqual(spec['generator']['codex_version'],expected_version)
                self.assertEqual(spec['sheet']['file'],f"K{meta['variant']}{number:02d}.html")
                self.assertEqual(spec['sheet']['id'],f"K{meta['variant']}{number:02d}")
                self.assertEqual(len(spec['palette']),4)
                baseline=json.loads((HERE/'tests/data/style-contract-baseline.json').read_text())
                family='parallax' if meta['variant']=='A' else 'fluxbloom'
                self.assertEqual(spec['palette'][0]['channels'],baseline['collections'][family][meta['slug']]['base_channels'])
                self.assertEqual(len(spec['skin']['items']),5)
                self.assertEqual(set(spec['anchors']),{'Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight'})
                ids={part['id'] for part in spec['parts']}
                for anchor in spec['anchors'].values():
                    if anchor['part'] is not None: self.assertIn(anchor['part'],ids)
                    if anchor['model'] is not None:
                        hand=np.asarray(spec['anchors']['Socket_Hand']['model'])
                        expected=(np.asarray(anchor['model'])-hand) @ np.asarray(MATRIX).T * spec['units']['model_unit_m']
                        np.testing.assert_allclose(anchor['position_m'],expected,atol=1e-7)
                for raw,part in zip(model,spec['parts']):
                    vertices=np.concatenate([face.vertices for face in raw.faces])
                    extents=np.ptp(vertices,axis=0)
                    self.assertEqual(part['long_axis'],('Y','Z','X')[int(np.argmax(extents))])
                    target=(vertices-np.asarray(spec['anchors']['Socket_Hand']['model'])) @ np.asarray(MATRIX).T * spec['units']['model_unit_m']
                    np.testing.assert_allclose(part['bounds_m'][0],target.min(axis=0),atol=1e-6)
                    np.testing.assert_allclose(part['bounds_m'][1],target.max(axis=0),atol=1e-6)
                self.assertTrue(spec['sight']['window_geometry']['elements'])
                self.assertEqual(spec['sight']['window'], 'lens' if meta['slug'] in ('impulse','sniper') else 'open' if meta['slug']=='bow' else 'glass')
                aperture=next(p for p in model if getattr(p,'sight_window',False))
                source_index=model.index(aperture)
                element=next(e for e in spec['sight']['window_geometry']['elements'] if e['part']==f'p{source_index:03d}')
                vertices=aperture.vertices
                center=(vertices.min(axis=0)+vertices.max(axis=0))/2
                hand=np.asarray(spec['anchors']['Socket_Hand']['model'])
                expected_center=(center-hand) @ np.asarray(MATRIX).T * spec['units']['model_unit_m']
                np.testing.assert_allclose(element['center_m'],expected_center,atol=1e-7)
                np.testing.assert_allclose(element['view_axis_m'],[0,-1,0],atol=1e-7)
                self.assertEqual(element['type'],'part')
                for skin in spec['skin']['items']:
                    self.assertEqual(set(skin['slots_used']),set(CHANNELS)|{'SK_Accent1','SK_Accent2'})
                    for variant in ('base','standard','arktis','nacht'):
                        self.assertEqual(set(skin['colors'][variant]),set(CHANNELS)|{'SK_Accent1','SK_Accent2'})
                        for slot in skin['colors'][variant]:
                            self.assertEqual(set(skin['colors'][variant][slot]),{'color','finish','source'})
                    glyph_layers=[layer for layer in skin['layers'] if layer['type']=='glyphs']
                    self.assertTrue(glyph_layers)
                    self.assertTrue(all(layer['decals'] for layer in glyph_layers))
                    model_skin=apply_skin(model,skin['id'])
                    expected_glyphs=[d for host in model_skin[:len(model)] for d in host.decals if getattr(d,'skin_trim',False)]
                    self.assertEqual(sum(len(layer['decals']) for layer in glyph_layers),sum(d.color in (s['accent1'],s['accent2']) for d in expected_glyphs for s in CATALOG if s['id']==skin['id']))
                glyphs={skin['id']:next(layer for layer in skin['layers'] if layer['type']=='glyphs') for skin in spec['skin']['items']}
                self.assertGreater(len(glyphs['gilt_vector']['decals']),0)
                self.assertEqual(next(s for s in spec['skin']['items'] if s['id']=='gilt_vector')['accents']['SK_Accent1']['finish'],'polished_gold')
                self.assertEqual(next(s for s in spec['skin']['items'] if s['id']=='gilt_vector')['accents']['SK_Accent2']['finish'],'polished_chrome')
                self.assertEqual(next(s for s in spec['skin']['items'] if s['id']=='chrome_crest')['accents']['SK_Accent1']['finish'],'polished_chrome')
                json.loads(dump(spec),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    def test_canonical_masks_match_source_samples_on_all_weapons_skins_and_palettes(self):
        # An asymmetric dense grid catches axis signs, mm/m, local-vs-global
        # frames, thin bands and overwrite order without a render or a golden.
        uu,vv=np.meshgrid(np.linspace(.00137,.99811,91),np.linspace(.00371,.99691,67))
        u,v=uu.ravel(),vv.ravel()
        compared=0; compared_finishes=0; resolved_gaps=0
        for number,meta,model in self.rows:
            spec=self.spec_for(number,meta,model)
            hand=np.asarray(spec['anchors']['Socket_Hand']['model']); unit=spec['units']['model_unit_m']
            for item in spec['skin']['items']:
                sid=item['id']; recipe=catalog_skin(sid); dressed=apply_skin(model,sid)
                declared=dressed[0].skin_declarations
                origin=np.asarray(declared['origin']); extent=np.maximum(declared['extent'],1e-12)
                world=origin+np.column_stack((u,v,np.full(len(u),.371)))*extent
                target=(world-hand) @ np.asarray(MATRIX).T * unit
                canonical=[(layer,_inside_yz(target[:,1:],layer['poly_yz_m']))
                           for layer in item['layers'] if layer['type']=='side_block']
                eligible={f'p{i:03d}' for i,p in enumerate(dressed[:len(model)]) if p.skin_declarations['eligible']}
                self.assertTrue(canonical, (meta['slug'],sid))
                for layer,_ in canonical:
                    self.assertTrue(set(layer['parts'])<=eligible)
                for index,part in enumerate(dressed[:len(model)]):
                    if not part.skin_declarations['eligible']: continue
                    pid=f'p{index:03d}'
                    palette_context={}
                    for vid,_,swatches in PALETTES:
                        palette=None if swatches is None else dict(zip(('primary','medium','dark','accent'),swatches))
                        resolved=channel_palette(dressed,palette)
                        if palette is not None: palette.update(resolved)
                        base=_rgb(part.color if palette is None else palette.get(channel_for(part),palette.get(part.role,part.color)))
                        palette_context[vid]=(base,dict(resolved,_base_color=base))
                    # Determine exact support independently from canonical geometry.
                    # An unsupported lower layer can be overwritten by a later
                    # representable layer and must then be checked again.
                    supported=np.ones(len(u),dtype=bool); authored=np.zeros(len(u),dtype=bool)
                    expected_slot=np.full(len(u),'',dtype=object)
                    source_finish=np.full(len(u),'',dtype=object)
                    for source_index,source in enumerate(recipe['layers']):
                        if source['type']=='blend':
                            affected=u>source['lo']
                            supported[affected]=False
                            continue
                        mask=_source_mask(source['mask'],u,v)
                        authored[mask]=True
                        key=source['color']
                        if key.startswith('SK_'):
                            candidate=key
                        else:
                            actual={vid:_contrast(key,base,context) for vid,(base,context) in palette_context.items()}
                            candidate=next((slot for slot in item['slots_used'] if all(
                                np.array_equal(_rgb(item['colors'][vid][slot]['color']),color)
                                for vid,color in actual.items())),None)
                            if candidate is None:
                                self.assertTrue(any(f'catalog.layers[{source_index}]; {key}' in note and pid in note
                                    for note in item['notes']), (meta['slug'],sid,pid,source_index))
                                resolved_gaps+=1
                        exact=_linear_mask(source['mask']) and candidate is not None
                        supported[mask]=exact
                        expected_slot[mask]=candidate or ''
                        source_finish[mask]=source.get('finish','paint')
                    for vid,(base,context) in palette_context.items():
                        expected,_=sample_surface(part,world,np.array([0,0,1]),sid,context)
                        actual=np.broadcast_to(base,expected.shape).copy(); hit=np.zeros(len(u),dtype=bool)
                        actual_finish=np.full(len(u),'',dtype=object)
                        for layer,mask in canonical:
                            if pid in layer['parts']:
                                actual[mask]=_rgb(item['colors'][vid][layer['slot']]['color'])
                                actual_finish[mask]=item['colors'][vid][layer['slot']]['finish']
                                hit[mask]=True
                        with self.subTest(weapon=meta['slug'],series=meta['variant'],skin=sid,part=pid,palette=vid):
                            self.assertTrue(hit[supported & authored].all())
                            np.testing.assert_allclose(actual[supported],expected[supported],atol=1e-8)
                            np.testing.assert_array_equal(actual_finish[supported & authored],source_finish[supported & authored])
                        compared+=int(supported.sum()); compared_finishes+=int((supported&authored).sum())
        self.assertGreater(compared,1000000)
        self.assertGreater(compared_finishes,100000)
        self.assertGreater(resolved_gaps,0)

    def test_decals_and_trim_preserve_real_host_geometry_and_fixed_colours(self):
        for number,meta,model in self.rows:
            spec=self.spec_for(number,meta,model)
            unit=spec['units']['model_unit_m']; hand=np.asarray(spec['anchors']['Socket_Hand']['model'])
            transform=lambda p:(np.asarray(p)-hand) @ np.asarray(MATRIX).T * unit
            for item in spec['skin']['items']:
                dressed=apply_skin(model,item['id'])
                by_host={layer['part']:layer for layer in item['layers'] if layer['type']=='glyphs'}
                for host_i,host in enumerate(dressed[:len(model)]):
                    source=[d for d in host.decals if getattr(d,'skin_trim',False)]
                    if not source: continue
                    host_id=f'p{host_i:03d}'; actual=by_host[host_id]['decals']
                    expected=[d for d in source if d.skin_kind!='badge']
                    self.assertEqual(len(actual),len(expected))
                    for decal,raw in zip(actual,expected):
                        np.testing.assert_allclose(decal['points_m'],transform(raw.faces[0].vertices),atol=1e-9)
                        self.assertEqual(decal['surface'],'left' if raw.faces[0].normal[2]>0 else 'right')
                        for vid in item['colors']:
                            self.assertEqual(item['colors'][vid][decal['slot']]['color'],raw.color.upper())
                    for badge in [d for d in source if d.skin_kind=='badge']:
                        notes=[note for note in item['notes'] if f'Badge-Farbe {badge.color.upper()} auf {host_id}' in note]
                        points=[json.loads(note.split('points_m=',1)[1].split('. Formatfrage:',1)[0]) for note in notes]
                        self.assertTrue(any(np.allclose(candidate,transform(badge.faces[0].vertices),atol=1e-9) for candidate in points))
                expected_trim={}
                for part in dressed[len(model):]:
                    if getattr(part,'skin_kind',None) in ('rib','fin'):
                        expected_trim.setdefault(f'p{part.skin_host:03d}',[]).append(part)
                trim_layers={layer['attach']:layer for layer in item['layers'] if layer['type']=='trim'}
                self.assertEqual(set(trim_layers),set(expected_trim))
                for host,raw_parts in expected_trim.items():
                    layer=trim_layers[host]
                    self.assertEqual(layer['count'],len(raw_parts))
                    for encoded,raw in zip(layer['parts'],raw_parts):
                        vertices=transform(raw.vertices)
                        np.testing.assert_allclose(encoded['bounds_m'],[vertices.min(axis=0),vertices.max(axis=0)],atol=1e-9)
                        np.testing.assert_allclose(encoded['x_m'],[vertices[:,0].min(),vertices[:,0].max()],atol=1e-9)
                        cap=max(raw.faces,key=lambda face:len(face.vertices))
                        np.testing.assert_allclose(encoded['profile_yz_m'],transform(cap.vertices)[:,1:],atol=1e-9)

    def test_texture_and_skin_catalog_ids_resolve_without_local_recipe_copies(self):
        materials={row['id'] for row in catalog()['materials']}; skins={row['id'] for row in catalog()['skins']}
        for number,meta,model in self.rows:
            spec=self.spec_for(number,meta,model)
            self.assertTrue(all(part['texture'] in materials or (part['material']=='glass' and part['texture'] is None) for part in spec['parts']))
            self.assertEqual(spec['skin']['catalog_id'],spec['skin']['hero'])
            for item in spec['skin']['items']:
                self.assertEqual(item['catalog_id'],item['id']); self.assertIn(item['catalog_id'],skins)
                self.assertEqual(item['description_en'],catalog_skin(item['id'])['description']['en'])
                self.assertFalse(any(layer['type'] in ('gradient','rings') for layer in item['layers']))
                if item['id']=='tidal_pulse':
                    self.assertTrue(any('kontinuierlicher Katalogverlauf' in note for note in item['notes']))
                    self.assertTrue(any('elliptische Katalogringe' in note for note in item['notes']))
                self.assertFalse(any('nicht vollständig übertragbar' in note for note in item['notes']))
            for motion in spec['moving_parts']['items']:
                for pid in motion['parts'] or []:
                    self.assertEqual(next(p['moving'] for p in spec['parts'] if p['id']==pid),motion['kind'])

    def test_mask_geometry_reads_catalogue_parameters_at_export_time(self):
        from copy import deepcopy
        from unittest.mock import patch
        number,meta,model=self.rows[0]
        before=self.spec_for(number,meta,model)
        original=catalog_skin
        def altered(identifier):
            row=deepcopy(original(identifier))
            if identifier=='circuit_bloom':
                region=next(layer for layer in row['layers'] if layer.get('color')=='SK_Accent1')
                region['mask']['k'] += .137
            return row
        with patch('texture_catalog.skin',side_effect=altered):
            after=make_spec(meta,model,number)
        polygons=lambda spec:[layer['poly_yz_m'] for layer in spec['skin']['items'][0]['layers']
            if layer['type']=='side_block' and layer['slot']=='SK_Accent1']
        self.assertNotEqual(polygons(before),polygons(after))
        # Catalogue edits affect no authored model data.
        for raw,part in zip(model,after['parts']):
            self.assertEqual(raw.color.upper(),part['color'])

    def test_bow_element_and_robot_fit_are_not_overclaimed(self):
        _,meta,model=next(row for row in self.rows if row[1]['slug']=='bow')
        spec=self.spec_for(10,meta,model)
        self.assertIsNone(spec['element'])
        self.assertFalse(spec['robot_fit']['applies'])
        self.assertTrue(spec['robot_fit']['reason'])
        self.assertIsNone(spec['robot_fit']['sheet_at_target'])
    def test_channels_are_in_documented_vocabulary(self):
        for number,meta,model in self.rows:
            spec=self.spec_for(number,meta,model)
            self.assertTrue(set(spec['channels_used'])<=set(CHANNELS))

if __name__=='__main__': unittest.main()
