#!/usr/bin/env python3
"""Generate the local Codex landing page without versioning rendered galleries."""
from pathlib import Path
import html
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def main(complete=False):
    cards=[]
    for family,name in (('parallax','A · Parallax'),('fluxbloom','K · Flux Bloom')):
        folder=ROOT/family
        links=[]
        for sub,label in (('output/texture-profile-probe','Texturprofil · Layoutproben'),('output/sight-probe','Teil D · Visierproben'),('output','Vollständige Serie mit VS-Visieren und Texturprofil' if complete else 'Bestehende vollständige Serie')):
            if (folder/sub/'index.html').exists():links.append(f'<p><a href="{family}/{sub}/index.html">{label}</a></p>')
        manifest=folder/'output/manifest.json'
        count=len(json.loads(manifest.read_text())['records']) if manifest.exists() else 0
        cards.append(f'<article><h2>{html.escape(name)}</h2><p>{count} lokale Konzeptblätter mit Vorschauen</p>'+''.join(links)+'</article>')
    compare=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract/index.html'
    extra=f'<p><a href="{compare.as_uri()}">Vier Proben neben Claude KF05 und KG07 · Messwerte</a></p>' if compare.exists() else ''
    status='Eigenständige Codex-Konstruktionen mit BEDIENUNG, separaten VS-Optiken und Texturprofilen. Neue Typen 11–25 sind Entwürfe ohne Toolgen- oder Spielanbindung; ihr Texturprofil ist ein abgeleiteter Vorschlag.'
    (ROOT/'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Codex · Cube Escape Designs</title><style>body{background:#0e1622;color:#ece6da;font:20px system-ui;margin:5vw;line-height:1.6}main{display:flex;flex-wrap:wrap;gap:24px}article{border:1px solid #36506b;padding:25px;border-radius:12px}a{color:#b4d8fc}</style><h1>Codex · Cube Escape Designs</h1><p>'+status+'</p>'+extra+'<main>'+''.join(cards)+'</main><p>Canonical Weapon-Spec v2 und Referenzdaten werden getrennt ohne Bildlauf erzeugt; keine bestätigte Spiel- oder Roboterpassung.</p>')
    print(ROOT/'index.html')
    if complete:
        # Full-series callers already hold heavy_lock for their Mac build.
        from spec_hashes import main as record_hashes
        record_hashes()


if __name__=='__main__':main()
