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
    identity, german, destiny, ammo = EXISTING[meta['slug']]
    result = dict(design_type=identity, design_type_de=german,
                  destiny_type=destiny, subtype=None, ammo_class=ammo,
                  toolgen_status='tool', type_source=SOURCE)
    if meta['slug'] == 'trace':
        result['note'] = ('Strahlwaffe: Das Magazin versorgt den Emitter; es bezeichnet keine Patronenzufuhr. '
                          'Die getrennten Beschleunigerschienen (Parallax) bzw. der Fokusaufbau (Flux Bloom) '
                          'führen den Dauerstrahl. Das neue Scout-Gewehr trägt Blattnummer 11 und bleibt ohne Toolgen-Anbindung.')
    return result
