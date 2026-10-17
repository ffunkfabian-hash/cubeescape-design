#!/usr/bin/env python3
"""Compare own rendered sheets with separately cached Claude release evidence.

Image stage: run on macOS under heavy_lock after building both collections.
No access to Claude's source pipeline and no copying into its repository.
"""
from pathlib import Path
import html
from PIL import Image, ImageDraw, ImageOps

CACHE=Path.home()/'Library/Caches/CubeEscapeDesign'
HERE=Path(__file__).resolve().parent
NAMES=('Pistole','Sturmgewehr','Impulsgewehr','Schrotflinte','Scharfschützengewehr',
       'Maschinenpistole','Fusionsgewehr','Spurgewehr','Raketenwerfer','Bogen')


def main():
    destination=CACHE/'comparison-upgrade'
    destination.mkdir(parents=True,exist_ok=True)
    sections=[]
    manifest=[]
    for n,name in enumerate(NAMES,1):
        sources=[('Codex A · Parallax',CACHE/f'concept-sheets/parallax-upgrade-full/KA{n:02d}.png',(140,430,2920,2200)),
                 ('Codex K · Flux Bloom',CACHE/f'concept-sheets/fluxbloom-upgrade-full/KK{n:02d}.png',(140,430,2920,2200)),
                 ('Claude F · Release v0.3',CACHE/f'comparison/shots/KF{n:02d}.png',(80,290,2780,2100)),
                 ('Claude H · Release v0.3',CACHE/f'comparison/shots/KH{n:02d}.png',(80,290,2780,2100))]
        canvas=Image.new('RGB',(2400,470),'#0e1622');draw=ImageDraw.Draw(canvas)
        for column,(label,source,crop) in enumerate(sources):
            with Image.open(source) as image:
                tile=ImageOps.contain(image.crop(crop).convert('RGB'),(590,420))
                canvas.paste(tile,(column*600+(600-tile.width)//2,40+(420-tile.height)//2))
            draw.text((column*600+15,15),label,fill='#ece6da')
        filename=f'compare-{n:02d}.jpg';canvas.save(destination/filename,quality=90)
        links=[]
        for label,source,_ in sources:
            preview=source.with_name(source.stem+'-preview.jpg')
            links.append(f'<a href="{html.escape(preview.as_uri())}">{html.escape(label)} vollständig</a>')
        sections.append(f'<section><h2>{n:02d} · {name}</h2><a href="{filename}"><img src="{filename}" alt="Vergleich {name}"></a><p>'+ ' · '.join(links)+'</p></section>')
        manifest.append(canvas)
    contact=Image.new('RGB',(1600,10*314),'#0e1622')
    for row,item in enumerate(manifest):contact.paste(item.resize((1600,313)),(0,row*314))
    contact.save(destination/'contact-sheet.jpg',quality=89)
    (destination/'index.html').write_text('''<!doctype html><html lang="de"><meta charset="utf-8"><title>Parallax und Flux Bloom · Claude-Vergleich</title><style>body{background:#0e1622;color:#ece6da;font:20px system-ui;margin:35px;line-height:1.5}img{width:100%;max-width:2400px}a{color:#b4d8fc}section{margin:50px 0}</style><h1>Überarbeitung · Parallax und Flux Bloom</h1><p>Je Klasse die Hauptfelder bei gleicher Spaltenbreite: Codex A, Codex K, Claude F, Claude H. Claude-Bildstand: veröffentlichtes Paket v0.3. Neuere Anforderungen aus main 9798f2a / Claude 0.5.2 sind zusätzlich im Codex-Werkzeug umgesetzt; diese Gegenüberstellung behauptet keinen Bildvergleich mit Claude 0.5.2.</p>'''+''.join(sections),encoding='utf-8')
    print(destination/'index.html')


if __name__=='__main__':main()
