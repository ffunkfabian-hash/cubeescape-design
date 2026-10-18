#!/usr/bin/env python3
"""Mac heavy_lock entry: catalog probes or the authorized full style rollout."""
from pathlib import Path
import sys
import build
import style_probe
import measure_style_probes
import viewer

HERE=Path(__file__).resolve().parent
CACHE=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract'


def main():
    full='--full' in sys.argv
    if full:
        for family in ('parallax','fluxbloom'):
            build.main(['--collection',family,'--screenshots',str(CACHE/'full'/family)])
    else:
        style_probe.main()
        # Broad rocket checks the additional responsive long-weapon layout.
        build.main(['--collection','fluxbloom','--probe','--weapon','rocket',
                    '--output',str(HERE/'layout-probe'),'--screenshots',str(CACHE/'layout')])
    measure_style_probes.main()
    if not full:
        from catalog_contact import main as contact
        contact()
    viewer.main(complete=full)


if __name__=='__main__':main()
