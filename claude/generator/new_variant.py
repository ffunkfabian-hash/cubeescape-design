"""Legt eine neue Konzeptblatt-Variante an (claude-0.4).
   python3 new_variant.py K "Glass Fang" "Kurzbeschreibung der Idee" [--vorlage J] [--version 0.5] [--probe]

Prüft Buchstabe und englischen Namen nach der Namensregel (variants.py), trägt die Variante in variants.py ein und kopiert
die zehn Modelle der Vorlage (Standard: J) als Rohlinge <k>01.py … <k>10.py (Spitzname ENTWURF, Beschreibung markiert).
Danach sind die Rohlinge zu gestalten; alle Skripte (build_all, sheetmodels, export_spec, mkdoc, skins, xl) kennen die
Variante ohne weitere Änderung. --probe zeigt nur, was passieren würde.
"""
from cepaths import E3D
import argparse,os,re,sys
sys.path.insert(0,E3D)
import variants

def main(argv):
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('letter');ap.add_argument('name');ap.add_argument('idea')
    ap.add_argument('--vorlage',default='J');ap.add_argument('--version',default=None);ap.add_argument('--probe',action='store_true')
    a=ap.parse_args(argv)
    L=a.letter.upper();src=a.vorlage.upper()
    err=variants.name_problems(L,a.name)
    if L in variants.LETTERS:err.append(f'Buchstabe {L} ist schon vergeben ({variants.LETTERS})')
    if src not in variants.LETTERS or variants.lib(src)!='jlib':err.append(f'Vorlage {src} muss eine jlib-Variante sein')
    files=[(os.path.join(E3D,f'{src.lower()}{n:02d}.py'),os.path.join(E3D,f'{L.lower()}{n:02d}.py')) for n in range(1,11)]
    err+=[f'{os.path.basename(d)} existiert schon' for _,d in files if os.path.exists(d)]
    if err:
        print('Nicht angelegt:\n- '+'\n- '.join(err));return 1
    entry=f" dict(letter={L!r},name={a.name!r},idea={a.idea!r},since={a.version or 'offen'!r},lib='jlib'),\n"
    vf=os.path.join(E3D,'variants.py');txt=open(vf,encoding='utf-8').read()
    anchor='\n]\n# Namen, die schon vergeben sind'
    assert txt.count(anchor)==1,'Ende von VARIANTS in variants.py nicht gefunden'
    print(f'Variante {L} · {a.name}: Eintrag in variants.py, Rohlinge '+', '.join(os.path.basename(d) for _,d in files))
    # erst alle Rohlinge vorbereiten, dann schreiben, zuletzt das Register (bricht etwas ab, ist die Variante nicht halb eingetragen)
    out=[]
    for s,d in files:
        t=open(s,encoding='utf-8').read()
        t,k1=re.subn(r"nick='[^']*'","nick='ENTWURF'",t,count=1)
        t,k2=re.subn(r"desc='","desc='ENTWURF (Vorlage "+src+") – ",t,count=1)
        if not(k1 and k2):print(f'Nicht angelegt: META in {os.path.basename(s)} ohne nick=\'…\' bzw. desc=\'…\'');return 1
        out.append((d,f'# Rohling aus {os.path.basename(s)} (new_variant.py) – Formen, Palette und META neu gestalten\n'+t))
    if a.probe:return 0
    done=[]
    try:
        for d,t in out:
            with open(d,'x',encoding='utf-8') as f:f.write(t)
            done.append(d)
    except Exception:
        for d in done:os.remove(d)   # nur eben angelegte Rohlinge
        raise
    open(vf,'w',encoding='utf-8').write(txt.replace(anchor,'\n'+entry.rstrip('\n')+anchor,1))
    print('Nächste Schritte: Rohlinge gestalten; Blätter: python3 build_xl.py '+' '.join(f'{L.lower()}{n:02d}' for n in range(1,11))+
          f' (Mac, heavy_lock); Vorschauen: python3 preview.py K{L}01 …; Specs: python3 export_spec.py; Test: python3 test_spec.py;'
          ' README-Tabelle und CHANGELOG ergänzen.')
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
