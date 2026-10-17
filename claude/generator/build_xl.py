from cepaths import E3D,OUT
import sys,pickle,re,glob,json,os
sys.path.insert(0,E3D+'')
import xl
PROJ=OUT+'/'
out={}
for fid in sys.argv[1:]:
    pk=f'{E3D}/reg/{fid}.pkl'
    if os.path.exists(pk):d=pickle.load(open(pk,'rb'))
    else:   # ohne Kartenlauf: Modell direkt aus dem Bauskript (sheetmodels, wie der Spec-Export)
        import sheetmodels
        d=sheetmodels.load('K'+('C' if fid[0]=='v' else fid[0].upper())+fid[1:])
    mm=re.search(r'VARIANTE\s+([A-Z])\s*·\s*„([^“]+)“',d['sub'])
    V,nick=mm.group(1),mm.group(2).title()
    d['nick']=nick
    page,de,en=xl.sheet(d,V)
    fn=f'K{V}{d["num"]}.dc.html'
    open(PROJ+fn,'w').write(page)
    open(f'{E3D}/final/{fn[:-8]}.html','w').write(page.replace('<script src="./support.js"></script>',''))
    json.dump(dict(V=V,num=d['num'],name=d['name'],nick=nick,de=de,en=en),open(f'{E3D}/reg/{fid}.prompt.json','w'),ensure_ascii=False)
    print(fn,len(page)//1024,'KB')
