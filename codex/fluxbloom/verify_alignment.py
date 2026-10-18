#!/usr/bin/env python3
"""Validate the actual delivered files, full-series metrics and catalog links."""
import json
from pathlib import Path
import jsonschema
from build import geometry_hash
from collections_codex import load_collection
from texture_catalog import catalog

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CACHE=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract'


def main():
    metrics=json.loads((CACHE/'metrics.json').read_text())
    material_ids={x['id'] for x in catalog()['materials']}
    skin_ids={x['id'] for x in catalog()['skins']}
    schemas=[jsonschema.Draft202012Validator(json.loads(p.read_text())) for p in
             (HERE/'weapon-spec.schema.json',ROOT/'claude/docs/weapon-spec.schema.json')]
    baseline=json.loads((HERE/'tests/data/style-contract-baseline.json').read_text())
    summary={}
    for family,letter in (('parallax','A'),('fluxbloom','K')):
        output=HERE.parent/family/'output'
        manifest=json.loads((output/'manifest.json').read_text())
        assert len(manifest['records'])==len(manifest['browser_qa'])==10
        rows={r['slug']:r for r in manifest['records']}
        widths=[]
        for n,(meta,model) in enumerate(load_collection(family),1):
            sid=f'K{letter}{n:02d}';record=rows[meta['slug']]
            previous=baseline['collections'][family][meta['slug']]
            assert previous['geometry_sha256']==geometry_hash(model)==record['geometry_sha256'],sid
            assert previous['palette']==meta['palette'] and previous['name']==meta['name'],sid
            data=json.loads((output/(sid+'.spec.json')).read_text())
            for schema in schemas:schema.validate(data)
            assert data['sheet']['file']==sid+'.html'
            assert all(part['texture'] in material_ids for part in data['parts']),sid
            assert data['skin']['catalog_id'] in skin_ids
            assert all(s['catalog_id'] in skin_ids for s in data['skin']['items'])
            dims=data['dimensions_m']['with_sight']
            physical=max(dims['length'],dims['height'],dims['width']) if meta['slug']=='bow' else dims['length']
            assert abs(physical-data['units']['reference_length_m'])<=.0005,(sid,physical)
            assert not record['textures']['catalog_scale_fallback'],sid
            assert abs(record['textures']['model_unit_m']-data['units']['model_unit_m'])<1e-12
            views=record['orthographic_views']
            assert len(views)==6 and len({v['scale'] for v in views})==1
            assert len({tuple(v['center']) for v in views})==1
            if record['orthographic_layout'].startswith('long_rows'):
                values=[v['width_fraction'] for v in views if v['name'] in ('links','rechts')]
                assert len(values)==2 and min(values)>=.70,(sid,values)
                widths.extend(values)
        for qa in manifest['browser_qa']:
            m=qa['metrics'];assert (m['width'],m['height'])==(4800,4432) and not m['overflow']
        group=metrics['groups']['after-'+letter]
        assert group['n']==10 and .72<=group['breite']<=.85,group
        assert group['rand_dunkel']>=.40 and group['innenlinien']>=.05,group
        summary[family]={'sheets':10,'canonical_specs':10,'metrics':group,'long_side_min_width':min(widths),
                         'schema':'official and independent profile','model_palette_name_unchanged':True,
                         'catalog_physical_scale_fallback':False}
    (CACHE/'acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
