"""Baut ein Konzeptblatt im Speicher und gibt sein sha256 aus (ohne Dateien zu schreiben). Gebraucht vom Determinismustest.
   python3 claude/tests/emit_sheet.py KC01      # braucht numpy/scipy (Bildstufe)
"""
import os,re,sys,hashlib
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','generator'))
import sheetmodels,xl
d=sheetmodels.load(sys.argv[1])
mm=re.search(r'VARIANTE\s+([A-Z])\s*·\s*„([^“]+)“',d['sub'])   # wie build_xl.py
d['nick']=mm.group(2).title()
page,_,_=xl.sheet(d,mm.group(1))
print(hashlib.sha256(page.encode('utf-8')).hexdigest())
