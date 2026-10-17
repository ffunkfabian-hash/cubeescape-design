"""Prüfungen auf den Spec-Dateien (claude-0.5), ohne numpy, ohne Bildstufe.

   python3 claude/generator/spec_checks.py            # Richtungsbefunde und Visier-Hinweise aller Blätter
   python3 claude/generator/spec_checks.py --json     # dasselbe als JSON

direction_problems: Richtung im Toolgen-Rahmen (vorn −Y, oben +Z, links +X; Cubegen docs/DEVELOPER.md 9.17: die Funktionsfläche
prüfen, nicht nur Anker oder Bounds). Fehler im Test (test_spec.py), Ausnahmen nur mit Grund in KNOWN_DIRECTION.
sight_target_hints: Visier je Waffentyp gegen das Zielbild von Cube Escape (Docs/EQUIPMENT.md › Visiere je Waffe). Nur Hinweise
für den Bericht, kein Fehler; ob ein Blatt geändert wird, entscheidet der Nutzer.
"""
from cepaths import OUT
import json,os,re,sys

TOL=1e-3            # m
GRIP_LABELS=('Griff','Pistolengriff','Griffstück')
PROJECTILE_LABELS=('Rakete',)

# Bekannte Richtungsbefunde: Blatt -> (Grund, Anfänge der erwarteten Befundtexte). Der Test verlangt genau diese Befunde
# (verschwindet einer oder kommt einer hinzu, schlägt er an).
KNOWN_DIRECTION={
 'KF10':('Pin-Ring (p34, leuchtend) ist in X am dünnsten: Durchsicht quer zur Pfeilachse statt entlang −Y; '
         'Blatt unverändert, Entscheidung des Nutzers offen (claude-0.5)',['Fenster part p34:','Fensterteil p34 ']),
}
def known_matches(sheet,problems):
    """True, wenn problems genau die erwarteten Befunde des bekannten Blatts sind (je Anfang genau einer)."""
    pre=KNOWN_DIRECTION[sheet][1]
    return len(problems)==len(pre) and all(sum(p.startswith(x) for p in problems)==1 for x in pre)

def _inside(p,b,tol=TOL,axes=(0,1,2)):return all(b[0][a]-tol<=p[a]<=b[1][a]+tol for a in axes)
def _ext(b):return [b[1][a]-b[0][a] for a in range(3)]
def _center(b):return [(b[0][a]+b[1][a])/2 for a in range(3)]

def projectile_ids(sp):
    """Geschoss im Rohr (Rakete) samt unbezeichneter Teile in ihrem Querschnitt, die als Kette hinten anschließen (wie der Exporter):
    zählt nicht als Waffe vor der Mündung."""
    parts=sp['parts'];out=set()
    def within(b,rb):return all(rb[0][a]-TOL<=b[0][a] and b[1][a]<=rb[1][a]+TOL for a in (0,2))
    for R in parts:
        if R['label'] not in PROJECTILE_LABELS:continue
        rb=R['bounds_m'];out.add(R['id']);rear=rb[1][1]          # hinten = größtes Y
        while True:
            nxt=[P for P in parts if P['id'] not in out and P['label'] is None and within(P['bounds_m'],rb)
                 and P['bounds_m'][0][1]<=rear+TOL and P['bounds_m'][1][1]>rear+TOL]
            if not nxt:break
            P=max(nxt,key=lambda q:q['bounds_m'][1][1]);out.add(P['id']);rear=P['bounds_m'][1][1]
        out|={P['id'] for P in parts if P['label'] is None and within(P['bounds_m'],rb) and P['bounds_m'][1][1]<=rear+TOL
              and P['bounds_m'][0][1]>=rb[0][1]-TOL}
    return out

def direction_problems(sp):
    """Liste der Richtungsbefunde eines Specs (leer = in Ordnung)."""
    pr=[];a=sp['anchors'];parts={p['id']:p for p in sp['parts']}
    m=a['Socket_Muzzle']['position_m']
    if m is None:return ['Socket_Muzzle fehlt']
    # 1. Mündung: vor dem Griff (−Y) und am vorderen Ende der Mündungsachse – kein Teil (außer Geschoss) ragt auf der Achse weiter vor
    if not m[1]<-0.01:pr.append(f'Socket_Muzzle nicht vor dem Griff (y={m[1]}, vorn ist −Y)')
    proj=projectile_ids(sp)
    ahead=[p['id'] for p in sp['parts'] if not p['sight'] and p['id'] not in proj and _inside(m,p['bounds_m'],axes=(0,2))
           and p['bounds_m'][0][1]<m[1]-TOL]
    if ahead:pr.append(f'Socket_Muzzle nicht am vorderen Ende der Mündungsachse: {", ".join(ahead)} ragen weiter nach −Y')
    face=[p['id'] for p in sp['parts'] if not p['sight'] and p['id'] not in proj and _inside(m,p['bounds_m'],axes=(0,2))
          and abs(p['bounds_m'][0][1]-m[1])<=TOL]
    if not face:pr.append('Socket_Muzzle liegt auf keiner Vorderkante eines Teils auf der Mündungsachse (zu weit vorn oder seitlich)')
    mp=parts.get(a['Socket_Muzzle'].get('part'))
    if mp is None or not _inside(m,mp['bounds_m'],axes=(0,2)):pr.append('Socket_Muzzle liegt nicht im Querschnitt seines Mündungsteils')
    # 2. Griff: Socket_Hand (Ursprung) im Griffteil, der Griff hängt unter der Mündungsachse
    h=a['Socket_Hand']['position_m'];hp=parts.get(a['Socket_Hand'].get('part'))
    if hp is None or hp['label'] not in GRIP_LABELS:pr.append('Socket_Hand ohne Griffteil')
    else:
        if not _inside(h,hp['bounds_m']):pr.append(f'Socket_Hand liegt nicht im Griffteil {hp["id"]}')
        if not hp['bounds_m'][0][2]<m[2]-TOL:pr.append(f'Griffteil {hp["id"]} reicht nicht unter die Mündungsachse (+Z oben)')
    # 3. Visier oben (bzw. links bei mount_side left), Socket_Sight an der Unterkante der Baugruppe
    s=sp['sight']
    if s['present']:
        sa=a['Socket_Sight']['position_m'];sb=s['bounds_m'];c=_center(sb)
        if sa is None:pr.append('Socket_Sight fehlt')
        else:
            if not sa[2]>h[2]:pr.append(f'Socket_Sight nicht über dem Griff (z={sa[2]})')
            if sb[0][2]<sa[2]-TOL:pr.append('Visierbaugruppe reicht unter Socket_Sight')
        if not c[2]>m[2]:pr.append(f'Visier nicht über der Mündungsachse (Mitte z={round(c[2],4)}, Mündung z={m[2]})')
        if s['mount_side']=='left' and not c[0]>m[0]+TOL:pr.append('Visier mount_side left, liegt aber nicht links (+X)')
        if s['mount_side']=='right' and not c[0]<m[0]-TOL:pr.append('Visier mount_side right, liegt aber nicht rechts (−X)')
    # 4. Visierfenster: Durchsicht entlang der Laufachse (Fensterfläche quer zu Y), über dem Griff
    wg=s.get('window_geometry')
    for e in (wg or {}).get('elements',[]):
        ax=e['view_axis_m']
        if not ax[1]<=-0.95:pr.append(f'Fenster {e["type"]} {e["decal"] if e["type"]=="decal" else e["part"]}: Durchsicht {ax} nicht entlang der Laufachse (erwartet −Y)')
        if e['type']=='decal':
            x=_ext(sp['decals'][e['decal']]['bounds_m'])
            if not (x[1]<TOL/2 and x[0]>TOL/2 and x[2]>TOL/2):pr.append(f'Fenster-Aufkleber {e["decal"]} liegt nicht quer zur Laufachse (Ausdehnung {[round(v,4) for v in x]})')
        else:
            x=_ext(parts[e['part']]['bounds_m'])
            if min(range(3),key=lambda k:x[k])!=1:pr.append(f'Fensterteil {e["part"]} ist nicht in Y am dünnsten (Ausdehnung {[round(v,4) for v in x]})')
        if not e['center_m'][2]>h[2]:pr.append(f'Fenster {e["part"]} nicht über dem Griff')
    return pr

# Zielbild Cube Escape, Docs/EQUIPMENT.md › „Visiere je Waffe“ (Stand CE 8ae12b15, 17.10.2026): Nr., Visier, Durchsicht.
# Erlaubt: Visierarten (Toolgen hold.sight_kind) und Fenster (Spec-Wortschatz), die zur Zeile passen. Offenes Fenster =
# Rahmen mit Scheibe oder offener Ring (glass/open), runde Röhre = lens. CE 0.72/0.74: offene Fenster statt geschlossener Gehäuse.
CE_SIGHTS={
 'pistol':(1,'kompaktes Reflex-Visier','offenes Fenster',{'reflex'},{'glass','open'}),
 'assault_rifle':(2,'offenes Holo-Visier','offenes Fenster',{'holo'},{'glass','open'}),
 'pulse_rifle':(3,'Präzisions-Visier (mittlere Distanz)','runde Röhre',{'scope'},{'lens'}),
 'shotgun':(4,'Weitwinkel-Reflex-Visier','großes rundes Fenster',{'reflex'},{'glass','open'}),
 'sniper_rifle':(5,'Hochpräzisions-Visier','runde Röhre, Zoom',{'scope'},{'lens'}),
 'smg':(6,'kompakt und schnell','offenes Fenster',{'reflex','holo'},{'glass','open'}),
 'fusion_rifle':(7,'technologisches Visier mit Energierahmen','breites Fenster',{'energy','holo'},{'glass','open'}),
 'scout_rifle':(8,'Zielverfolgungs-Visier','Fenster mit Markierung',{'holo','reflex'},{'glass','open'}),
 'rocket_launcher':(9,'Weitbereichs-Visier','breites Fenster',{'holo','reflex','energy'},{'glass','open'}),
}
CE_SOURCE='Cube Escape Docs/EQUIPMENT.md › Visiere je Waffe (CE 8ae12b15, 17.10.2026)'

def sight_target_hints(sp):
    """Abweichungen vom CE-Zielbild als Hinweise (Liste von Texten; leer = passt oder kein Zielbild)."""
    tid=sp['weapon']['toolgen_id'];s=sp['sight']
    if tid not in CE_SIGHTS:return []
    nr,vis,durch,kinds,wins=CE_SIGHTS[tid];out=[]
    if s['kind'] not in kinds:out.append(f'Art {s["kind"]} statt {"/".join(sorted(kinds))}')
    if s['window'] not in wins:out.append(f'Fenster {s["window"]} statt {"/".join(sorted(wins))}')
    if not out:return []
    return [f'{sp["sheet"]["id"]} {sp["weapon"]["name_de"]}: {s["kind"]}/{s["window"]} – Zielbild CE {nr}: {vis}, Durchsicht „{durch}“ ({"; ".join(out)})']

def ce_table(path):
    """Zeilen der CE-Tabelle „Visiere je Waffe“: Nr. -> (Visier, Durchsicht)."""
    with open(path,encoding='utf-8') as f:txt=f.read()
    sec=txt.split('### Visiere je Waffe',1)[1].split('\n#',1)[0]
    return {int(mm.group(1)):(mm.group(2).strip(),mm.group(3).strip()) for mm in re.finditer(r'^\|\s*(\d+)\s+[^|]+\|([^|]+)\|([^|]+)\|',sec,re.M)}
def ce_equipment_path():
    return os.environ.get('CE_EQUIPMENT') or os.path.expanduser('~/Claude/Cube Escape/Docs/EQUIPMENT.md')

def main(argv):
    import sheetmodels
    res={}
    for s in sheetmodels.SHEETS:
        with open(os.path.join(OUT,f'{s}.spec.json'),encoding='utf-8') as f:sp=json.load(f)
        res[s]=dict(direction=direction_problems(sp),sight_hints=sight_target_hints(sp),
                    window_gap=sp['sight']['window_geometry_note'] if sp['sight']['window'] not in (None,'none') and not sp['sight']['window_geometry'] else None)
    if '--json' in argv:print(json.dumps(res,ensure_ascii=False,indent=1));return 0
    print('Richtung (Fehler, außer bekannte):')
    for s,r in res.items():
        for p in r['direction']:print(f'  {s}: {p}'+('  [bekannt]' if s in KNOWN_DIRECTION and known_matches(s,r['direction']) else ''))
    hints=[h for r in res.values() for h in r['sight_hints']]
    print(f'Visier gegen CE-Zielbild ({CE_SOURCE}): {len(hints)} Hinweise')
    for h in hints:print('  '+h)
    gaps=[s for s,r in res.items() if r['window_gap']]
    print(f'Fenster mit Glas/Linse/offen ohne Fensterelement im Modell ({len(gaps)}): {" ".join(gaps)}')
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
