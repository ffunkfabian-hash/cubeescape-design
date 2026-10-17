def Lb(s,name):
    s['label']=name;return s
def apply(m,spec):
    assert len(m.parts)==len(spec),(len(m.parts),len(spec))
    for P,s in zip(m.parts,spec):
        if s.get('label'):P['label']=s['label']
    return m
