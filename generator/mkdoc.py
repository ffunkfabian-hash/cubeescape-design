from cepaths import E3D,OUT
import json,glob
items=[json.load(open(f)) for f in glob.glob(E3D+'/reg/*.prompt.json')]
items.sort(key=lambda d:(d['V'],d['num']))
out=['# Cube Escape – Waffen-Prompts (Varianten C, D, F, G)','',
'Je Waffe ein deutscher Prompt (für Concept-Art- bzw. 3D-Agenten, nach dem Qualitäts-Masterprompt) und ein kompakter englischer Prompt für Bildgeneratoren. Die zugehörigen Konzeptblätter liegen im Canvas auf der Seite „Konzeptblätter“.','']
cur=None
for d in items:
    if d['V']!=cur:
        cur=d['V'];out+=[f'## Variante {cur}','']
    out+=[f"### {d['num']} · {d['name']} – „{d['nick']}“",'','**Deutsch**','',d['de'],'','**Englisch (Bildgenerator)**','',d['en'],'']
open(E3D+'/Waffen-Prompts.md','w').write('\n'.join(out))
print(len(items))
