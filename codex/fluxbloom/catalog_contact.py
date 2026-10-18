#!/usr/bin/env python3
"""Compare four actual material fields with catalog swatches; Mac heavy_lock."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
OUT=Path.home()/'Library/Caches/CubeEscapeDesign/style-contract'


def main():
    font=ImageFont.truetype(str(HERE/'fonts/Barlow-Regular.ttf'),34)
    small=ImageFont.truetype(str(HERE/'fonts/Barlow-Regular.ttf'),27)
    canvas=Image.new('RGB',(2400,2920),'#0e1622');draw=ImageDraw.Draw(canvas)
    for index,sid in enumerate(('KA01','KA05','KK05','KK08')):
        family='parallax' if sid.startswith('KA') else 'fluxbloom'
        x=(index%2)*1200;y=(index//2)*900
        with Image.open(OUT/f'{family}/{sid}.png') as image:
            cropped=ImageOps.contain(image.crop((2300,2240,3620,3200)).convert('RGB'),(1180,850))
            canvas.paste(cropped,(x+(1200-cropped.width)//2,y+45))
        draw.text((x+18,y+5),sid+' · tatsächliches Materialfeld',font=font,fill='#ece6da')
    rows=(('material_painted','material_brushed','material_rubber','material_painted_matte','material_energy_glass'),
          ('finish_paint','finish_polished_gold','finish_polished_chrome','finish_neon','wear'))
    for row,ids in enumerate(rows):
        y=1810+row*550
        for col,sid in enumerate(ids):
            with Image.open(ROOT/'docs/textures/swatches'/(sid+'.png')) as swatch:
                tile=ImageOps.contain(swatch.convert('RGB'),(460,460))
                canvas.paste(tile,(col*480+10,y+50))
            draw.text((col*480+10,y+6),sid,font=small,fill='#ece6da')
    canvas.save(OUT/'catalog-materials.jpg',quality=92)
    print(OUT/'catalog-materials.jpg')


if __name__=='__main__':main()
