from cepaths import E3D,OUT,PROMPTS
import json,glob,os,re
import variants
items=[json.load(open(f)) for f in glob.glob(E3D+'/reg/*.prompt.json')]
items.sort(key=lambda d:(variants.LETTERS.index(d['V']),d['num']))
# Varianten ohne frische Prompts (reg/ fehlt, z. B. Teilbau `build_all.py J`): Abschnitt aus der bisherigen Sammlung übernehmen
old={}
fn=os.path.join(PROMPTS,'Waffen-Prompts.md')
if os.path.exists(fn):
    for m in re.finditer(r'^## Variante ([A-Z])\b[^\n]*\n(.*?)(?=^## Variante |\Z)',open(fn,encoding='utf-8').read(),re.S|re.M):old[m.group(1)]=m.group(2)
have={d['V'] for d in items}
out=['# Cube Escape – Waffen-Prompts (Varianten '+', '.join(variants.title(v) for v in variants.LETTERS)+')','',
'Je Waffe ein deutscher Prompt (für Concept-Art- bzw. 3D-Agenten, nach dem Qualitäts-Masterprompt) und ein kompakter englischer Prompt für Bildgeneratoren. Die zugehörigen Konzeptblätter liegen im Canvas auf der Seite „Konzeptblätter“.','']
for v in variants.LETTERS:
    if v not in have:
        if v in old:out+=[f'## Variante {variants.title(v)}',old[v].rstrip('\n'),'']
        continue
    out+=[f'## Variante {variants.title(v)}','']
    for d in items:
        if d['V']!=v:continue
        out+=[f"### {d['num']} · {d['name']} – „{d['nick']}“",'','**Deutsch**','',d['de'],'','**Englisch (Bildgenerator)**','',d['en'],'']
open(E3D+'/Waffen-Prompts.md','w').write('\n'.join(out))
print(len(items),'neu,',len([v for v in variants.LETTERS if v not in have and v in old]),'Varianten übernommen')
