"""Two separately authored model series using the shared upgraded Codex tooling."""
import importlib
import sys
from pathlib import Path
from authoring import polish_model, upgrade_bow

PROBE_SLUGS = ('pistol','fusion','trace','bow')


def load_collection(collection='fluxbloom', include_new=False):
    if collection=='fluxbloom':
        from models import load_all
        result=load_all()
    elif collection=='parallax':
        root=str(Path(__file__).resolve().parent.parent)
        if root not in sys.path:sys.path.insert(1,root)
        result=importlib.import_module('parallax.models').load_all()
    else:raise ValueError('Unknown Codex collection')
    # Keep the original ten-design API for its frozen regression contract;
    # production builds explicitly request the extended 25-type catalogue.
    if include_new:
        root=str(Path(__file__).resolve().parent.parent)
        if root not in sys.path:sys.path.insert(1,root)
        result += importlib.import_module(collection+'.models.arsenal').load_new()
    for meta,model in result:
        meta['series']=collection
        if collection=='parallax':meta.update(variant='A',variant_name='Parallax')
        if meta['slug']=='bow':upgrade_bow(meta,model)
        polish_model(meta,model)
    return result
