"""Lädt die Modelle der Konzeptblätter (KC01 … KH10, ab 0.4 auch KJ01 …; Varianten aus variants.py) ohne Bildstufe.

Liefert dasselbe Wörterbuch, das views.card() nach reg/<fid>.pkl schreibt und build_xl.py für das Blatt nutzt
(m, center, num, name, sub, col, pill, desc, palette, form, fid) plus V und nick wie in build_xl.py.
Die Bauwege spiegeln die Bauskripte (build_v01, build_c25, build_c, build_d15, build_d, build_f15, build_f610,
build_g15, build_g610, build_h15, build_h610); Varianten mit lib='jlib' (ab J) haben kein Kartenskript, ihr Modell kommt direkt aus jlib; deren Konstanten (INFO, D, Aufruf von card) werden per ast gelesen,
damit die Skripte unverändert bleiben und beim Import nichts bauen.
Ab claude-0.7 ersetzt vsmount.apply() das Visier der Waffen 1–9 durch das Standardvisier der Visier-Serie VS01–VS09.
Ab claude-0.10 kommen die neuen Waffentypen dazu (wtypes.NEW_SHEETS, KG11 … KG22): Modell aus g11.py … mit model() und META (tlib),
Bedienung META['op'] als d['op']; ihr Visier setzt vsmount nach wtypes (Nahkampf ohne Visier).
"""
from cepaths import E3D
import ast,importlib,os,re,sys
sys.path.insert(0,E3D)
from eng import copy_channels
import variants,vsmount,wtypes

VARS=variants.LETTERS
NUMS=[f'{i:02d}' for i in range(1,11)]
NEW_NUMS=wtypes.NEW_SHEETS   # neue Waffentypen (claude-0.10) je Variante
SHEETS=[f'K{v}{n}' for v in VARS for n in NUMS]+[f'K{v}{n}' for v in VARS for n in NEW_NUMS.get(v,[])]

def _src(fn):
    with open(os.path.join(E3D,fn),encoding='utf-8') as f:return ast.parse(f.read())
def _const(fn,name):
    for node in _src(fn).body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(f'{name} fehlt in {fn}')
def _card_call(fn):
    """Literale Argumente des card(...)-Aufrufs (build_v01.py)."""
    for node in ast.walk(_src(fn)):
        if isinstance(node,ast.Call) and getattr(node.func,'id',None)=='card':
            return [None if isinstance(a,ast.Call) else ast.literal_eval(a) for a in node.args]
    raise KeyError(f'card() fehlt in {fn}')

def _mod(name):return importlib.import_module(name)
def _items(mod):
    """fgen-Weg (F/G/H 01–05): Modell aus ITEMS, Labels/Bias/Visier wie in build_f15/g15/h15."""
    import fgen
    m=fgen.model(mod.ITEMS)
    assert len(m.parts)==len(mod.ITEMS),(len(m.parts),len(mod.ITEMS))
    for it,Pt in zip(mod.ITEMS,m.parts):
        if it.get('L'):Pt['label']=it['L']
        if it.get('bias'):Pt['bias']=it['bias']
        if it.get('S'):Pt['sight']=True
    return copy_channels(m,mod.ITEMS)

def _c(n):
    if n=='01':
        from v01m import model
        _,center,num,name,sub,col,pill,desc,pal,form,fid=_card_call('build_v01.py')
        return dict(m=model(),center=center,num=num,name=name,sub=sub,col=col,pill=pill,desc=desc,palette=pal,form=form,fid=fid)
    if n<='05':
        c,name,nick,col,pill,pal,desc,form=_const('build_c25.py','INFO')[n]
        return dict(m=_mod('c'+n).model(),center=c,num=n,name=name,sub=f'VARIANTE C · „{nick}“ · ALLE PERSPEKTIVEN, GEZEICHNET',
                    col=col,pill=pill,desc=desc,palette=pal,form=form,fid='c'+n)
    M=_mod('c'+n);k=M.META
    return dict(m=M.model(),center=M.CENTER,num=n,name=k['name'],sub=f'VARIANTE C · „{k["var"]}“ · ALLE PERSPEKTIVEN, GEZEICHNET',
                col=k['col'],pill=k['pill'],desc=k['desc'],palette=k['pal'],form=k['form'],fid='c'+n)

def _d(n):
    if n<='05':
        w,nm,pill,pal,col,desc,form=_const('build_d15.py','D')[int(n)]
        m,c=getattr(_mod('dmods'),'d'+n)(*pal)
        return dict(m=m,center=c,num=n,name=w,sub='VARIANTE D · „%s“ · ALLE PERSPEKTIVEN, GEZEICHNET'%nm.upper(),
                    col=col,pill=pill,desc=desc,palette=pal,form=form,fid='d'+n)
    name,nick,col,pill,pal,desc,form=_const('build_d.py','INFO')[n]
    m,c=getattr(_mod('dmodels'),'d'+n)()
    return dict(m=m,center=c,num=n,name=name,sub=f'VARIANTE D · „{nick}“ · ALLE PERSPEKTIVEN, GEZEICHNET',
                col=col,pill=pill,desc=desc,palette=pal,form=form,fid='d'+n)

def _fgh(v,n):
    mod=_mod(v.lower()+n)
    if n<='05':
        I=mod.INFO;sub=f'VARIANTE {v} · „{I["nick"]}“ · KONZEPTBLATT'
        return dict(m=_items(mod),center=I['center'],num=I['num'],name=I['name'],sub=sub,col=I['col'],pill=I['pill'],
                    desc=I['desc'],palette=I['pal'],form=I['form'],fid=v.lower()+n)
    import flib
    M=mod.META;sp=mod.spec();m=flib.model(sp)
    if v=='F':
        import flabel,fsight
        m=flabel.apply(m,sp);fsight.flag_parts(m,[bool(s.get('S')) for s in sp])
    elif v=='G':
        import flabel,gsight
        m=gsight.mark(flabel.apply(m,sp),sp,'sight')
    else:
        import hxlib
        m=hxlib.apply(m,sp)
    copy_channels(m,sp)
    return dict(m=m,center=M['center'],num=M['num'],name=M['name'],sub=f"VARIANTE {v} · „{M['vname'].upper()}“ · KONZEPTBLATT",
                col=M['col'],pill=M['pill'],desc=M['desc3'],palette=M['palette'],form=M['form'],fid=v.lower()+n)

def _jlib(v,n):
    """Varianten mit lib='jlib' (ab J): Modell direkt aus <v>NN.py (spec, META), kein Kartenskript"""
    import jlib
    fid=v.lower()+n;mod=_mod(fid);M=mod.META
    return dict(m=jlib.model(mod.spec()),center=M['center'],num=M['num'],name=M['name'],sub=f"VARIANTE {v} · „{M['nick']}“ · KONZEPTBLATT",
                col=M['col'],pill=M['pill'],desc=M['desc'],palette=M['palette'],form=M['form'],fid=fid,sight=tuple(M['sight']))

def _tlib(v,n):
    """neue Waffentypen (claude-0.10): Modell direkt aus <v>NN.py (model, META mit Bedienung op)"""
    fid=v.lower()+n;mod=_mod(fid);M=mod.META
    assert wtypes.TYPES[M['name']]['num']==n,(fid,M['name'])
    return dict(m=mod.model(),center=M['center'],num=M['num'],name=M['name'],sub=f"VARIANTE {v} · „{M['nick']}“ · KONZEPTBLATT",
                col=M['col'],pill=M['pill'],desc=M['desc'],palette=M['palette'],form=M['form'],fid=fid,op=M['op'])

def load(sheet):
    """sheet = 'KC01' … 'KH10' -> Wörterbuch wie reg/<fid>.pkl, ergänzt um V und nick (wie build_xl.py)."""
    v,n=sheet[1],sheet[2:]
    assert v in VARS and (n in NUMS or n in NEW_NUMS.get(v,[])),sheet
    d=_tlib(v,n) if n not in NUMS else _jlib(v,n) if variants.lib(v)=='jlib' else _c(n) if v=='C' else _d(n) if v=='D' else _fgh(v,n)
    mm=re.search(r'VARIANTE\s+([A-Z])\s*·\s*„([^“]+)“',d['sub'])
    assert mm.group(1)==v,(sheet,d['sub'])
    d['V']=v;d['nick']=mm.group(2).title();d['sheet']=sheet
    return vsmount.apply(d)   # Visier der Visier-Serie VS01–VS09 (claude-0.7), Bögen unverändert
