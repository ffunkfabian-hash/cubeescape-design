"""Waffentypen-Katalog der Konzeptblätter (claude-0.10): Designtyp je Blattname, abgeglichen mit dem Destiny-2-Katalog.

Destiny 2 liefert Funktions- und Formenreferenzen (kein Nachbau). Stand des Abgleichs 18.10.2026: 17 Waffentypen im Spiel
(Granatwerfer als ein Typ, hier getrennt in Spezial- und schweren Granatwerfer), dazu die schwere Armbrust seit „The Edge of Fate“
(15.07.2025, neuer Heavy-Typ mit wiederaufnehmbarem Bolzen). Quellen und Untertypen: claude/docs/waffentypen.md.

Je Blattname (`weapon.name_de`):
  id        Designtyp (Spec `weapon.design_type`), englisch, eindeutig; Spurgewehr = trace_rifle, Scout-Gewehr = scout_rifle
  en        Destiny-Bezeichnung (englisch), de Bezeichnung auf Deutsch
  subtype   konstruktiver Untertyp (rocket_assisted, slug, breech_loaded, drum_loaded; ab 0.10.1 dynamic_heat, micro_missile, spread_shot) oder None
  ammo      Munitionsklasse in Destiny (primary, special, heavy) – nur Einordnung, keine Spielregel
  toolgen   Toolgen-Werkzeug (data/tools.json › id) oder None: neue Typen sind in Toolgen/Cube Escape nicht angebunden
  num       Typnummer = Blattnummer (KX01 … KX10 bestehend, KG11 … KG22 neu in claude-0.10, KG23 … KG25 in claude-0.10.1)
Nur für neue Typen (toolgen None):
  ref_len   Bezugslänge in m (Spec-Maßstab; Schätzung claude-0.10 aus den Toolgen-Längen verwandter Typen, siehe Bericht 0.10)
  vs        Standardvisier der Visier-Serie (VS01–VS09) oder None (Nahkampf ohne Visier)
  motions   bewegliche Teile (export_spec.MOTIONS)
Ohne numpy.
"""

SOURCE=('Destiny-2-Katalog, Stand 18.10.2026: destinytracker.com/destiny-2/db/items/weapon (17 Typen), Wikipedia „Destiny 2: The Edge of '
        'Fate“ (schwere Armbrust), Untertypen siehe claude/docs/waffentypen.md')

TYPES={
 # bestehende Typen 01–10 (Toolgen-Werkzeuge): Designtyp macht die Bedeutung ausdrücklich, toolgen_id bleibt unverändert
 'Pistole':dict(id='sidearm',en='Sidearm',de='Pistole (Sidearm)',subtype=None,ammo='primary',toolgen='pistol',num='01'),
 'Sturmgewehr':dict(id='auto_rifle',en='Auto Rifle',de='Sturmgewehr (Automatikgewehr)',subtype=None,ammo='primary',toolgen='assault_rifle',num='02'),
 'Impulsgewehr':dict(id='pulse_rifle',en='Pulse Rifle',de='Impulsgewehr',subtype=None,ammo='primary',toolgen='pulse_rifle',num='03'),
 'Schrotflinte':dict(id='shotgun',en='Shotgun',de='Schrotflinte (Streuschrot)',subtype=None,ammo='special',toolgen='shotgun',num='04'),
 'Scharfschützengewehr':dict(id='sniper_rifle',en='Sniper Rifle',de='Scharfschützengewehr',subtype=None,ammo='special',toolgen='sniper_rifle',num='05'),
 'Maschinenpistole':dict(id='submachine_gun',en='Submachine Gun',de='Maschinenpistole',subtype=None,ammo='primary',toolgen='smg',num='06'),
 'Fusionsgewehr':dict(id='fusion_rifle',en='Fusion Rifle',de='Fusionsgewehr',subtype=None,ammo='special',toolgen='fusion_rifle',num='07'),
 'Spurgewehr':dict(id='trace_rifle',en='Trace Rifle',de='Spurgewehr',subtype=None,ammo='special',toolgen='scout_rifle',num='08',
                   note='Toolgen-ID „scout_rifle“ bezeichnet hier das Spurgewehr (Toolgen data/tools.json: label „Spurgewehr“); das echte Scout-Gewehr ist KG11'),
 'Raketenwerfer':dict(id='rocket_launcher',en='Rocket Launcher',de='Raketenwerfer',subtype=None,ammo='heavy',toolgen='rocket_launcher',num='09'),
 'Bogen':dict(id='combat_bow',en='Combat Bow',de='Bogen',subtype=None,ammo='primary',toolgen='bow',num='10'),
 # neue Typen (claude-0.10), Variante G; ohne Toolgen-Werkzeug
 'Scout-Gewehr':dict(id='scout_rifle',en='Scout Rifle',de='Scout-Gewehr',subtype=None,ammo='primary',toolgen=None,num='11',
                     ref_len=1.00,vs='VS03',motions=['bolt']),
 'Handfeuerwaffe':dict(id='hand_cannon',en='Hand Cannon',de='Handfeuerwaffe (Hand Cannon)',subtype=None,ammo='primary',toolgen=None,num='12',
                       ref_len=0.32,vs='VS01',motions=['cylinder','hammer']),
 'Lineares Fusionsgewehr':dict(id='linear_fusion_rifle',en='Linear Fusion Rifle',de='Lineares Fusionsgewehr',subtype=None,ammo='heavy',toolgen=None,num='13',
                               ref_len=1.30,vs='VS05',motions=['rails']),
 'Spezial-Granatwerfer':dict(id='grenade_launcher_special',en='Grenade Launcher (Special, breech-loaded)',de='Spezial-Granatwerfer (Kipplauf)',subtype='breech_loaded',
                             ammo='special',toolgen=None,num='14',ref_len=0.78,vs='VS04',motions=['breech']),
 'Schwerer Granatwerfer':dict(id='grenade_launcher_heavy',en='Grenade Launcher (Heavy, drum-loaded)',de='Schwerer Granatwerfer (Trommel)',subtype='drum_loaded',
                              ammo='heavy',toolgen=None,num='15',ref_len=0.95,vs='VS09',motions=['drum']),
 'Maschinengewehr':dict(id='machine_gun',en='Machine Gun',de='Maschinengewehr',subtype=None,ammo='heavy',toolgen=None,num='16',
                        ref_len=1.15,vs='VS06',motions=['bolt','feed_cover']),
 'Schwert':dict(id='sword',en='Sword',de='Schwert',subtype=None,ammo='heavy',toolgen=None,num='17',ref_len=1.10,vs=None,motions=[]),
 'Glefe':dict(id='glaive',en='Glaive',de='Glefe',subtype=None,ammo='special',toolgen=None,num='18',ref_len=1.40,vs=None,motions=['shield']),
 'Schwere Armbrust':dict(id='heavy_crossbow',en='Crossbow (Heavy)',de='Schwere Armbrust',subtype=None,ammo='heavy',toolgen=None,num='19',
                         ref_len=0.95,vs='VS03',motions=['cocking','string']),
 'Raketenpistole':dict(id='sidearm',en='Rocket-Assisted Sidearm',de='Raketenpistole (Sidearm mit Raketenmunition)',subtype='rocket_assisted',ammo='special',
                       toolgen=None,num='20',ref_len=0.27,vs='VS01',motions=['slide']),
 'Raketen-Impulsgewehr':dict(id='pulse_rifle',en='Rocket-Assisted Pulse Rifle',de='Raketen-Impulsgewehr',subtype='rocket_assisted',ammo='special',
                             toolgen=None,num='21',ref_len=0.88,vs='VS03',motions=['bolt']),
 'Slug-Schrotflinte':dict(id='shotgun',en='Slug Shotgun',de='Slug-Schrotflinte (Einzelgeschoss)',subtype='slug',ammo='special',toolgen=None,num='22',
                          ref_len=0.94,vs='VS04',motions=['bolt']),
 # Lücken aus 0.10, gebaut in claude-0.10.1 (Variante G). Munitionsklasse nach Destiny-Quellen (Bericht 0.10.1 › Quellen): Dynamic-Heat-
 # Waffen gibt es als Handfeuerwaffe, Impulsgewehr, Pistole und Scharfschütze (kein MG) – hier als Impulsgewehr; der Micro-Missile-Rahmen ist ein
 # einschüssiger Spezial-Granatwerfer (Theodolite, Mountaintop); Spread Shot ist ein Handfeuerwaffen-Rahmen mit Primärmunition (Phoneutria Fera)
 'Hitze-Blaster':dict(id='pulse_rifle',en='Pulse Rifle (Dynamic Heat Frame, blaster)',de='Hitze-Blaster (Impulsgewehr, Rahmen Dynamic Heat)',subtype='dynamic_heat',
                      ammo='primary',toolgen=None,num='23',ref_len=0.86,vs='VS03',motions=['vent']),
 'Mikroraketen-Granatwerfer':dict(id='grenade_launcher_special',en='Grenade Launcher (Micro-Missile Frame)',de='Mikroraketen-Granatwerfer (Micro-Missile-Rahmen)',
                                  subtype='micro_missile',ammo='special',toolgen=None,num='24',ref_len=0.84,vs='VS04',motions=['hatch']),
 'Streuschuss-Handfeuerwaffe':dict(id='hand_cannon',en='Hand Cannon (Spread Shot Frame)',de='Streuschuss-Handfeuerwaffe (Spread-Shot-Rahmen, Schrotladung)',
                                   subtype='spread_shot',ammo='primary',toolgen=None,num='25',ref_len=0.30,vs='VS01',motions=['top_break']),
}
NEW={k:v for k,v in TYPES.items() if v['toolgen'] is None}
# Blätter der neuen Typen je Variante: G seit claude-0.10 (Modelle g11.py … g25.py), C, D, F, H, J seit claude-0.11 (c11.py … j25.py,
# Modelle gebaut von Codex als Unteragent, je Variante im eigenen Stil; gleiche Mechanik und Bauteile je Typ wie G, eigene Silhouette)
NEW_NUMS=sorted(v['num'] for v in NEW.values())
NEW_SHEETS={'G':NEW_NUMS,'C':['12'],'D':['13'],'F':['19'],'H':['16'],'J':['11']}
REF_SOURCE='Schätzung claude-0.10: Proportion zu den Toolgen-0.13-Längen verwandter Typen (Bericht claude/docs/versions/0.10.md › Maße), kein Toolgen-Modell'
# Sätze für Abnehmer, die toolgen_id als Pflichtwert lesen
TOOLGEN_NONE='nicht in Toolgen/Cube Escape angebunden (neuer Designtyp claude-0.10); toolgen_id null, Anbindung siehe claude/docs/waffentypen.md › Offene Anbindungen'

def of(name):return TYPES[name]
def is_new(name):return TYPES[name]['toolgen'] is None
def key(name):
    """Schlüssel für typabhängige Tabellen (Bewegung, Visier, Texturprofil, Roboter-Maße): Toolgen-ID bei bestehenden Typen,
    sonst „+“ und Designtyp, bei Untertypen mit „:Untertyp“ (+scout_rifle, +sidearm:rocket_assisted). Das „+“ trennt das neue
    Scout-Gewehr vom Toolgen-Schlüssel scout_rifle (= Spurgewehr)."""
    t=TYPES[name]
    if t['toolgen']:return t['toolgen']
    return '+'+t['id']+(':'+t['subtype'] if t['subtype'] in KEY_SUBTYPES else '')
# Untertypen mit eigenem Schlüssel (eigene Bewegung, eigenes Texturprofil); Kipplauf/Trommel des Granatwerfers sind eigene Designtypen
KEY_SUBTYPES=('rocket_assisted','slug','dynamic_heat','micro_missile','spread_shot')
# Kurzname der beweglichen Teile für das Blattfeld BEDIENUNG (Arten wie export_spec.MOTIONS)
MOTION_SHORT_DE={'slide':'Schlitten','bolt':'Verschluss/Ladehebel','cell':'Zelle','fins':'Flossen','coil':'Spulenring','pump':'Pumpgriff',
 'lever':'Kammerstängel','hatch':'Ladeklappe','cylinder':'Trommel','hammer':'Hahn','rails':'Beschleunigerschienen','breech':'Kipplauf',
 'drum':'Granattrommel','feed_cover':'Zuführdeckel','cocking':'Spannhebel','string':'Sehne','shield':'Schildflügel',
 'vent':'Entlüftungsklappen','top_break':'Kipprahmen'}
MELEE=('Schwert','Glefe')   # ohne Visier und Visierschiene; Detailfeld zeigt den Griffbereich
def spec(name,sheet=None):
    """Spec-Block weapon (ohne name_de/toolgen_id): Designtyp, Destiny-Bezeichnung, Untertyp, Munitionsklasse, Anbindung"""
    t=TYPES[name]
    out=dict(design_type=t['id'],design_type_de=t['de'],destiny_type=t['en'],subtype=t['subtype'],ammo_class=t['ammo'],
             toolgen_status='tool' if t['toolgen'] else 'not_connected',type_source=SOURCE)
    note=SHEET_NOTES.get(sheet) or t.get('note')
    if note:out['note']=note
    return out

# Blätter, deren Bauweise vom Typnamen abweicht (Befund der Bestandsübersicht claude-0.10); ID und Typ bleiben, der Hinweis steht im Spec
SHEET_NOTES={
 'KF01':'Trommel mit sechs Kammern: konstruktiv eine Handfeuerwaffe (Revolver); Blatt bleibt Pistole/Sidearm (ID nicht umgedeutet), eigener Typ Handfeuerwaffe: KG12',
 'KC10':'Armbrust statt Bogen: Typ bleibt Bogen (ID nicht umgedeutet); die schwere Armbrust (Destiny-Heavy-Typ seit 2025) ist KG19',
 'KH08':'Spurgewehr mit Gabel-Emitter, aber Magazin hinter dem Griff und Bullpup-Gehäuse: liest sich teils wie ein Scout-Gewehr; Strahlwaffe über den Emitter, echtes Scout-Gewehr: KG11',
 'KJ08':'Spurgewehr mit Magazin im Schacht und Sechskant-Lauf: liest sich teils wie ein Scout-Gewehr; Strahlwaffe über die facettierte Emitter-Mündung, echtes Scout-Gewehr: KG11',
}
