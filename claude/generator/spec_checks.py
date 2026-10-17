"""Prüfungen auf den Spec-Dateien (claude-0.5), ohne numpy, ohne Bildstufe.

   python3 claude/generator/spec_checks.py            # Richtungsbefunde und Visier-Hinweise aller Blätter
   python3 claude/generator/spec_checks.py --json     # dasselbe als JSON

direction_problems: Richtung im Toolgen-Rahmen (vorn −Y, oben +Z, links +X; Cubegen docs/DEVELOPER.md 9.17: die Funktionsfläche
prüfen, nicht nur Anker oder Bounds). Fehler im Test (test_spec.py), Ausnahmen nur in KNOWN_CROSS_WINDOWS (datiert, mit Grund).
window_problems: dieselbe Fensterprüfung für jeden Spec mit window_geometry (auch die Visier-Serie VS01–VS09).
sight_target_hints: Visier je Waffentyp gegen das Zielbild von Cube Escape (Docs/EQUIPMENT.md › Visiere je Waffe). Nur Hinweise
für den Bericht, kein Fehler; ob ein Blatt geändert wird, entscheidet der Nutzer.
"""
from cepaths import OUT
import json,os,re,sys

TOL=1e-3            # m
GRIP_LABELS=('Griff','Pistolengriff','Griffstück')
PROJECTILE_LABELS=('Rakete',)

# Bekannte Querfenster (Stand 17.10.2026, claude-0.5.2): Blatt -> Schlüssel der Fensterelemente (dNN = decals[NN], pNN = Teil), deren
# Funktionsfläche quer zur Laufachse liegt. Generatorfehler der Blätter (Öffnungen und Scheiben in der Seitenansicht gezeichnet und
# durch die Breite extrudiert); wird mit der Umstellung der Waffenblätter auf die Visier-Serie VS01–VS09 behoben (Entscheidung des
# Nutzers 17.10.2026: „Test jetzt, Fix mit Umstellung“). Der Test verlangt genau diese Menge: ein neues Querfenster macht ihn rot,
# ein behobenes ebenso (dann den Eintrag entfernen).
KNOWN_CROSS_SINCE='17.10.2026'
KNOWN_CROSS_WINDOWS={}   # wird unten aus der Liste befüllt
# 19 aus der Sichtprüfung 0.5.1, dazu KC02 (Diopter-Öffnung), KH03 (hintere Lochblende), KD10 und KF10 (Bogen-Pins)
_KNOWN='''
KC02 d33 d34
KC09 p19
KD01 d36 d37
KD02 d38 d39
KD03 d40 d41
KD04 d34 d35
KD07 d20 d21
KD10 d14 d15
KF06 d20 d21
KF10 d5 d6 p34
KG02 d38 d39
KG04 d18 d19
KH01 d93 d94 d95 d96
KH02 d107 d108 d109 d110
KH03 d61 d62
KH04 d83 d84 p17 p18
KH09 d48
KJ01 d30 d31
KJ02 d32 d33
KJ03 d20 d21
KJ06 d28 d29
KJ07 d18 d19
KJ09 d6 d7
'''
def _parse_known(txt):return {l.split()[0]:sorted(l.split()[1:]) for l in txt.strip().splitlines()}
KNOWN_CROSS_WINDOWS.update(_parse_known(_KNOWN))

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

def _key(e):return f"d{e['decal']}" if e['type']=='decal' else e['part']
def window_problems(elements,parts,decals,hand_z=None):
    """Prüft Fensterelemente (sight.window_geometry.elements) an ihrer Funktionsfläche, nicht an Rotation oder Bounds allein
    (Cubegen docs/DEVELOPER.md 9.17). parts: id -> Teil, decals: Liste wie im Spec. Rahmen: vorn −Y. Wiederverwendbar für jeden Spec
    mit diesen Feldern (auch die Visier-Serie VS01–VS09). Befunde beginnen mit „Fenster quer [key]“ (Durchsicht nicht entlang Y),
    „Fensterachse [key]“ (view_axis widerspricht der Geometrie) oder „Fenster [key] unter dem Griff“."""
    pr=[]
    for e in elements:
        k=_key(e);ax=e['view_axis_m'];va=max(range(3),key=lambda a:abs(ax[a]))
        x=_ext((decals[e['decal']] if e['type']=='decal' else parts[e['part']])['bounds_m'])
        ga=min(range(3),key=lambda a:x[a])          # flache bzw. dünnste Achse = Durchsicht
        if ga!=1:pr.append(f'Fenster quer [{k}] ({e["type"]} auf {e["part"]}): Durchsicht entlang {"XYZ"[ga]} statt −Y (Ausdehnung {[round(v,4) for v in x]})')
        if va!=ga or (va==1 and not ax[1]<=-0.95):pr.append(f'Fensterachse [{k}]: view_axis_m {ax} passt nicht zur Geometrie ({"XYZ"[ga]}, Vorzeichen −Y)')
        if e['type']=='decal' and not (x[ga]<TOL/2 and all(x[a]>TOL/2 for a in range(3) if a!=ga)):
            pr.append(f'Fensterachse [{k}]: Aufkleber nicht flach (Ausdehnung {[round(v,4) for v in x]})')
        if hand_z is not None and not e['center_m'][2]>hand_z:pr.append(f'Fenster [{k}] unter dem Griff')
    return pr
def cross_windows(problems):
    """Schlüssel der Querfenster aus den Befunden (für KNOWN_CROSS_WINDOWS)."""
    return sorted({p.split('[')[1].split(']')[0] for p in problems if p.startswith('Fenster quer [')})
def known_ok(sheet,problems):
    """True, wenn die Befunde genau die bekannten Querfenster des Blatts sind (keine anderen Befunde)."""
    return all(p.startswith('Fenster quer [') for p in problems) and cross_windows(problems)==KNOWN_CROSS_WINDOWS.get(sheet,[])

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
    # 4. Visierfenster: Funktionsfläche (Scheibe, Öffnung, Ring) mit Durchsicht entlang −Y, über dem Griff
    pr+=window_problems((s.get('window_geometry') or {}).get('elements',[]),parts,sp['decals'],hand_z=h[2])
    return pr

# Zielbild Cube Escape, Docs/EQUIPMENT.md › „Visiere je Waffe“ (Stand CE 8ae12b15, 17.10.2026): Nr., Visier, Durchsicht.
# Erlaubt: Visierarten (Toolgen hold.sight_kind) und Fenster (Spec-Wortschatz), die zur Zeile passen. Offenes Fenster =
# Rahmen mit Scheibe oder offener Ring (glass/open), runde Röhre = lens. Zieltyp (claude-0.5.2): Typ des Visiertypen-Blatts je Waffe. CE 0.72/0.74: offene Fenster statt geschlossener Gehäuse.
CE_SIGHTS={
 'pistol':(1,'kompaktes Reflex-Visier','offenes Fenster',{'reflex'},{'glass','open'},'reflex'),
 'assault_rifle':(2,'offenes Holo-Visier','offenes Fenster',{'holo'},{'glass','open'},'holo'),
 'pulse_rifle':(3,'Präzisions-Visier (mittlere Distanz)','runde Röhre',{'scope'},{'lens'},'precision'),
 'shotgun':(4,'Weitwinkel-Reflex-Visier','großes rundes Fenster',{'reflex'},{'glass','open'},'reflex'),
 'sniper_rifle':(5,'Hochpräzisions-Visier','runde Röhre, Zoom',{'scope'},{'lens'},'sniper'),
 'smg':(6,'kompakt und schnell','offenes Fenster',{'reflex','holo'},{'glass','open'},'machine'),
 'fusion_rifle':(7,'technologisches Visier mit Energierahmen','breites Fenster',{'energy','holo'},{'glass','open'},'energy'),
 'scout_rifle':(8,'Zielverfolgungs-Visier','Fenster mit Markierung',{'holo','reflex'},{'glass','open'},'trace'),
 'rocket_launcher':(9,'Weitbereichs-Visier','breites Fenster',{'holo','reflex','energy'},{'glass','open'},'rocket'),
}
CE_SOURCE='Cube Escape Docs/EQUIPMENT.md › Visiere je Waffe (CE 8ae12b15, 17.10.2026)'

def sight_target_hints(sp):
    """Abweichungen vom CE-Zielbild als Hinweise (Liste von Texten; leer = passt oder kein Zielbild)."""
    tid=sp['weapon']['toolgen_id'];s=sp['sight']
    if tid not in CE_SIGHTS:return []
    nr,vis,durch,kinds,wins,typ=CE_SIGHTS[tid];out=[]
    if s.get('type') not in (None,typ):out.append(f'Typ {s["type"]} statt {typ}')
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
        known=known_ok(s,r['direction']) and r['direction']
        for p in r['direction']:print(f'  {s}: {p}'+('  [bekannt]' if known else ''))
    hints=[h for r in res.values() for h in r['sight_hints']]
    print(f'Visier gegen CE-Zielbild ({CE_SOURCE}): {len(hints)} Hinweise')
    for h in hints:print('  '+h)
    gaps=[s for s,r in res.items() if r['window_gap']]
    print(f'Fenster mit Glas/Linse/offen ohne Fensterelement im Modell ({len(gaps)}): {" ".join(gaps)}')
    return 0

if __name__=='__main__':sys.exit(main(sys.argv[1:]))
