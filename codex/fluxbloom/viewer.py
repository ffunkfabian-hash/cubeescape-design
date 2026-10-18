#!/usr/bin/env python3
"""Generate the local Codex landing page without versioning rendered galleries."""
from pathlib import Path
import html

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def main(complete=False):
    cards=[]
    for family,name in (('parallax','A · Parallax'),('fluxbloom','K · Flux Bloom')):
        folder=ROOT/family
        links=[]
        for sub,label in (('style-probe','Neue Stilvertrag-Proben'),('output','Vollständige Serie nach Stilvertrag' if complete else 'Bestehende vollständige Serie')):
            if (folder/sub/'index.html').exists():links.append(f'<p><a href="{family}/{sub}/index.html">{label}</a></p>')
        cards.append(f'<article><h2>{html.escape(name)}</h2>'+''.join(links)+'</article>')
    compare=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract/index.html'
    extra=f'<p><a href="{compare.as_uri()}">Vier Proben neben Claude KF05 und KG07 · Messwerte</a></p>' if compare.exists() else ''
    status='Beide vollständigen Serien wurden nach dem Stilvertrag und mit dem gemeinsamen Texturkatalog neu gebaut.' if complete else 'Vier Katalogproben vor dem vollständigen Serienlauf; die Stilfreigabe des Nutzers liegt vor.'
    (ROOT/'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Codex · Cube Escape Designs</title><style>body{background:#0e1622;color:#ece6da;font:20px system-ui;margin:5vw;line-height:1.6}main{display:flex;flex-wrap:wrap;gap:24px}article{border:1px solid #36506b;padding:25px;border-radius:12px}a{color:#b4d8fc}</style><h1>Codex · Cube Escape Designs</h1><p>'+status+'</p>'+extra+'<main>'+''.join(cards)+'</main><p>Canonical Weapon-Spec v1 und Referenzdaten werden getrennt ohne Bildlauf erzeugt; keine bestätigte Spiel- oder Roboterpassung.</p>')
    print(ROOT/'index.html')


if __name__=='__main__':main()
