"""Codex type identities, aligned with the read-only shared type catalogue.

Design identities are distinct from Toolgen IDs. Source facts: wtypes.TYPES;
no Claude model, operation text or pipeline implementation is imported.
"""
SOURCE = 'claude/generator/wtypes.py TYPES; Destiny-2-Katalog, Stand 18.10.2026; claude/docs/waffentypen.md'
# slug: design_type, German designation, Destiny type, ammunition class
EXISTING = {
    'pistol': ('sidearm', 'Pistole (Sidearm)', 'Sidearm', 'primary'),
    'assault': ('auto_rifle', 'Sturmgewehr (Automatikgewehr)', 'Auto Rifle', 'primary'),
    'impulse': ('pulse_rifle', 'Impulsgewehr', 'Pulse Rifle', 'primary'),
    'shotgun': ('shotgun', 'Schrotflinte (Streuschrot)', 'Shotgun', 'special'),
    'sniper': ('sniper_rifle', 'Scharfschützengewehr', 'Sniper Rifle', 'special'),
    'smg': ('submachine_gun', 'Maschinenpistole', 'Submachine Gun', 'primary'),
    'fusion': ('fusion_rifle', 'Fusionsgewehr', 'Fusion Rifle', 'special'),
    'trace': ('trace_rifle', 'Spurgewehr', 'Trace Rifle', 'special'),
    'rocket': ('rocket_launcher', 'Raketenwerfer', 'Rocket Launcher', 'heavy'),
    'bow': ('combat_bow', 'Bogen', 'Combat Bow', 'primary'),
}


def weapon_fields(meta):
    if meta['slug'] in NEW:
        identity, german, destiny, subtype, ammo, _, _ = NEW[meta['slug']]
        return dict(design_type=identity, design_type_de=german, destiny_type=destiny,
                    subtype=subtype, ammo_class=ammo, toolgen_status='not_connected', type_source=SOURCE)
    identity, german, destiny, ammo = EXISTING[meta['slug']]
    result = dict(design_type=identity, design_type_de=german,
                  destiny_type=destiny, subtype=None, ammo_class=ammo,
                  toolgen_status='tool', type_source=SOURCE)
    if meta['slug'] == 'trace':
        result['note'] = ('Strahlwaffe: Das Magazin versorgt den Emitter; es bezeichnet keine Patronenzufuhr. '
                          'Die getrennten Beschleunigerschienen (Parallax) bzw. der Fokusaufbau (Flux Bloom) '
                          'führen den Dauerstrahl. Das neue Scout-Gewehr trägt Blattnummer 11 und bleibt ohne Toolgen-Anbindung.')
    return result

# Factual type identities and estimated lengths from wtypes.TYPES. Geometry and
# operation texts are independently authored in the two Codex model series.
# slug: identity, German designation, Destiny designation, subtype, ammo, metres, VS
NEW = {
 'scout': ('scout_rifle','Scout-Gewehr','Scout Rifle',None,'primary',1.00,3),
 'handcannon': ('hand_cannon','Handfeuerwaffe (Hand Cannon)','Hand Cannon',None,'primary',.32,1),
 'linear': ('linear_fusion_rifle','Lineares Fusionsgewehr','Linear Fusion Rifle',None,'heavy',1.30,5),
 'breech': ('grenade_launcher_special','Spezial-Granatwerfer (Kipplauf)','Grenade Launcher (Special, breech-loaded)','breech_loaded','special',.78,4),
 'drum': ('grenade_launcher_heavy','Schwerer Granatwerfer (Trommel)','Grenade Launcher (Heavy, drum-loaded)','drum_loaded','heavy',.95,9),
 'machine': ('machine_gun','Maschinengewehr','Machine Gun',None,'heavy',1.15,6),
 'sword': ('sword','Schwert','Sword',None,'heavy',1.10,None),
 'glaive': ('glaive','Glefe','Glaive',None,'special',1.40,None),
 'crossbow': ('heavy_crossbow','Schwere Armbrust','Crossbow (Heavy)',None,'heavy',.95,3),
 'rocketside': ('sidearm','Raketenpistole (Sidearm mit Raketenmunition)','Rocket-Assisted Sidearm','rocket_assisted','special',.27,1),
 'rocketpulse': ('pulse_rifle','Raketen-Impulsgewehr','Rocket-Assisted Pulse Rifle','rocket_assisted','special',.88,3),
 'slug': ('shotgun','Slug-Schrotflinte (Einzelgeschoss)','Slug Shotgun','slug','special',.94,4),
 'heat': ('pulse_rifle','Hitze-Blaster (Impulsgewehr, Rahmen Dynamic Heat)','Pulse Rifle (Dynamic Heat Frame, blaster)','dynamic_heat','primary',.86,3),
 'micro': ('grenade_launcher_special','Mikroraketen-Granatwerfer (Micro-Missile-Rahmen)','Grenade Launcher (Micro-Missile Frame)','micro_missile','special',.84,4),
 'spread': ('hand_cannon','Streuschuss-Handfeuerwaffe (Spread-Shot-Rahmen, Schrotladung)','Hand Cannon (Spread Shot Frame)','spread_shot','primary',.30,1),
}


def type_key(slug):
    if slug not in NEW:
        from weapon_spec import TOOLGEN
        return TOOLGEN[slug][0]
    row = NEW[slug]
    suffix = ':' + row[3] if row[3] in ('rocket_assisted','slug','dynamic_heat','micro_missile','spread_shot') else ''
    return '+' + row[0] + suffix
