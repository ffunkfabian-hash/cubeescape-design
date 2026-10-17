"""Varianten-Register der Konzeptblätter (claude-0.4): die einzige Stelle, an der Varianten eingetragen werden.

Bauskripte, Modell-Lader (sheetmodels), Skin-Auswahl (skins.pick), Spec-Export, Prompt-Sammlung (mkdoc) und Blattkopf (xl)
lesen Buchstaben und Namen von hier. Neue Variante: `python3 new_variant.py <Buchstabe> "<Name>" "<Idee>"` legt den Eintrag
und zehn Modell-Rohlinge an.

Namensregel (Nutzer, 17.10.2026): Jede neue Variante bekommt zum Kennbuchstaben einen kurzen, markanten englischen Namen
(1–3 Wörter, nur Buchstaben, Wörter groß geschrieben, nicht schon von einer Variante oder von Codex benutzt). Der Buchstabe
bleibt die ID (Blätter KJ01 …), der Name steht in Kopfzeile, Prompts, Spec (`sheet.variant_name`) und README.
C–H sind älter und bleiben ohne Namen (Entscheidung des Nutzers, 17.10.2026).

Felder: letter, name, idea, since (Claude-Version), lib ('jlib' = Modelle <buchstabe>01.py … <buchstabe>10.py mit spec() und
META wie j01.py; ohne lib: ältere Bauwege mit eigenem Kartenskript, siehe sheetmodels).
"""
import re

VARIANTS=[
 dict(letter='C',name=None,idea='Neue Formen der Originalwaffen, je eigene Palette'),
 dict(letter='D',name=None,idea='Originalformen, konstruktiv überarbeitet, Farbvarianten'),
 dict(letter='F',name=None,idea='Neue Formen, mutige Paletten'),
 dict(letter='G',name=None,idea='Neue Formen in der Cube-Escape-Farbwelt (Creme, Anthrazit, Orange, Cyan)'),
 dict(letter='H',name=None,idea='„Werkstatt-Serie“: modulare Prototypen mit Klemm-/Schraubverbindungen'),
 dict(letter='J',name='Black Ice',idea='Stealth-Serie: wenige große, scharfe Facetten wie bei Tarnkappenjets, matte dunkle Grundtöne, '
      'eisblaue Leuchtkanten',since='0.4',lib='jlib'),
]
# Namen, die schon vergeben sind (Codex-Pipeline codex/parallax), dürfen nicht noch einmal vorkommen
TAKEN={'Parallax'}
# Buchstaben, die nicht vergeben werden: I sieht in Blatt-IDs wie 1 aus (KI01), O wie 0
SKIP_LETTERS='IO'

LETTERS=''.join(v['letter'] for v in VARIANTS)
BY_LETTER={v['letter']:v for v in VARIANTS}
NAME_RE=re.compile(r'^[A-Z][a-z]+(?: [A-Z][a-z]+){0,2}$')

def name(letter):return BY_LETTER[letter]['name']
def lib(letter):return BY_LETTER[letter].get('lib')
def title(letter):
    """'J · Black Ice' bzw. 'C' (ältere Varianten ohne Namen)"""
    n=name(letter);return f'{letter} · {n}' if n else letter

def name_problems(letter,nm,variants=VARIANTS):
    """Verstöße eines (neuen) Eintrags gegen die Namensregel; leer = in Ordnung"""
    out=[]
    if not re.fullmatch(r'[A-Z]',letter or ''):out.append('Buchstabe muss ein Großbuchstabe sein')
    if letter in SKIP_LETTERS:out.append(f'Buchstabe {letter} wird nicht vergeben (Verwechslung mit Ziffern)')
    if not nm:out.append('neue Varianten brauchen einen englischen Namen');return out
    if not NAME_RE.match(nm):out.append('Name: 1–3 englische Wörter, nur Buchstaben, je Wort groß beginnend (z. B. „Black Ice“)')
    if len(nm)>16:out.append('Name höchstens 16 Zeichen (Kopfzeile des Blatts)')
    used={v['name'].lower() for v in variants if v['name'] and v['letter']!=letter}|{t.lower() for t in TAKEN}
    if nm.lower() in used:out.append(f'Name „{nm}“ ist schon vergeben')
    return out
