"""Schriften als Dateien neben den Blättern (claude/output/sheets/fonts/, SIL OFL 1.1, Lizenztexte liegen dabei) statt Google Fonts.
Echte Gewichte aus github.com/google/fonts (ofl/): Chakra Petch 400–700, Barlow 400–600, JetBrains Mono als variable Datei (wght 100–800)."""
_F=[('Chakra Petch','ChakraPetch-Regular.ttf',400),('Chakra Petch','ChakraPetch-Medium.ttf',500),('Chakra Petch','ChakraPetch-SemiBold.ttf',600),
    ('Chakra Petch','ChakraPetch-Bold.ttf',700),('Barlow','Barlow-Regular.ttf',400),('Barlow','Barlow-Medium.ttf',500),
    ('Barlow','Barlow-SemiBold.ttf',600),('JetBrains Mono','JetBrainsMono-Variable.ttf','400 500')]
FONT_CSS='<style>'+''.join(f"@font-face{{font-family:'{n}';src:url('fonts/{f}') format('truetype');font-weight:{w};font-style:normal}}" for n,f,w in _F)+'</style>'
