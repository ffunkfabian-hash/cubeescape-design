#!/usr/bin/env python3
"""Record source geometry and canonical spec hashes without rendering images."""
import hashlib
import json
from pathlib import Path
from collections_codex import load_collection
from build import geometry_hash

HERE=Path(__file__).resolve().parent


def main(include_new=True):
    for family in ('parallax','fluxbloom'):
        output=HERE.parent/family/'output'
        records={}
        for n,(meta,model) in enumerate(load_collection(family, include_new=include_new),1):
            sid=f"K{meta['variant']}{n:02d}"
            data=(output/(sid+'.spec.json')).read_bytes()
            parsed=json.loads(data)
            if parsed['format']!='cubeescape-design/weapon-spec':raise ValueError(f'{sid}: canonical spec required')
            records[sid]={'spec_sha256':hashlib.sha256(data).hexdigest(),'geometry_sha256':geometry_hash(model)}
        (output/'golden.json').write_text(json.dumps({'scope':'canonical spec and source geometry only; no claim of full-series style render approval','records':records},indent=2)+'\n')
        print(family,len(records),'spec hashes')


if __name__=='__main__':main()
