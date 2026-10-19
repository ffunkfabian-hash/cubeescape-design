"""Weapon-type targets transcribed from the user's Waffen Texturen 1–9 table.

These targets describe the consumer's material recipe, not a replacement for the
authored palette, skin or model materials. No Claude pipeline code is imported.
"""
from copy import deepcopy
from texture_catalog import catalog, material

SOURCE = ('Cube Escape Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp '
          '(Textur-Blatt des Nutzers); Codex-Übertragung nach Auftrag vom 18.10.2026')
TILES = (('housing', 'GEHÄUSE'), ('metal', 'METALL'), ('rubber', 'GUMMI'),
         ('energy', 'ENERGIE'), ('edge_wear', 'KANTENABNUTZUNG'), ('decals', 'DECALS'))
ENERGY_COLORS = dict(orange='#FF8A2A', blue='#3D8BFF', violet='#A15CFF',
                     light_blue='#7FD4FF', cyan='#22E3E8')
WEAR_NAMES = dict(subtle='dezent', medium='mittel', strong='stark')

# housing ID/text, metal ID/text, rubber text, energy color/text, wear/text,
# Toolgen decal IDs/text, and the interpretation explicitly required by the brief.
ROWS = {
    'pistol': ('painted', 'Lackiert, leicht matt', 'brushed', 'Gebürstet, robust',
               'Griffig, strukturiert', 'orange', 'Orange, klar', 'subtle', 'Subtil, realistisch',
               ['symbol_diamond', 'number_01'], 'Symbole, Nummern', None),
    'assault_rifle': ('painted', 'Lackiert, leicht matt', 'brushed', 'Industrie-Finish',
                      'Struktur, Griffe', 'blue', 'Blau, Tech-Elemente', 'medium', 'Mittel, genutzt',
                      ['mil_ar2', 'tech_bars'], 'Militärisch, Tech', 'Metall „Industrie-Finish“ als gebürstet gedeutet'),
    'pulse_rifle': ('ceramic', 'Keramik-Look', 'satin', 'Dunkel, satiniert', 'Strukturiert',
                    'violet', 'Violett, leuchtend', 'subtle', 'Kontrolliert', ['tech_ring'],
                    'Tech-Symbole', '„Kontrolliert“ als subtle gedeutet (geringste Stufe)'),
    'shotgun': ('painted_matte', 'Strapazierfähig, matt', 'rough_cast', 'Rau, massiv', 'Griffzonen',
                'orange', 'Orange, kräftig', 'strong', 'Stark, abgenutzt', ['hazard_stripes'], 'Warnhinweise', None),
    'sniper_rifle': ('painted', 'Sauber, präzise', 'brushed', 'Hochwertig, fein', 'Minimal, griffig',
                     'light_blue', 'Hellblau, präzise', 'subtle', 'Leicht, dezent', ['serial_s07'], 'Seriennummern', None),
    'smg': ('painted_matte', 'Leicht, widerstandsfähig', 'brushed', 'Dunkel, genutzt', 'Stark strukturiert',
            'cyan', 'Cyan, lebendig', 'medium', 'Mittel, authentisch', ['arrows_chevron', 'arrow_triangle'],
            'Taktisch, Pfeile', 'Metall „Dunkel, genutzt“ als gebürstet gedeutet'),
    'fusion_rifle': ('painted', 'Hochtechnologie, glatt', 'satin', 'Präzise, clean', 'Technisch, lamellen',
                     'violet', 'Violett, intensiv', 'subtle', 'Gezielt, dezent', ['research'],
                     'Forschungs-Symbol', 'Metall „Präzise, clean“ als satiniert gedeutet'),
    'trace_rifle': ('painted', 'Glatt, sauber', 'polished', 'Premium, poliert', 'Minimal', 'blue',
                    'Blau, kontinuierlich', 'subtle', 'Leicht, sauber', ['tech_lines'], 'Tech, Linien', None),
    'rocket_launcher': ('painted_matte', 'Schwer, robust', 'rough_cast', 'Massiv, angeraut', 'Stoßdämpfend',
                        'orange', 'Orange, Hitze', 'strong', 'Stark, realistisch', ['hazard_stripes', 'warning_triangle'],
                        'Warnzeichen', 'Decals: Warnzeichen plus die Warnstreifen der Schrotflinte'),
}


def profile(weapon_type):
    """Return a fresh validated v1 block, or no profile for the unlisted bow."""
    if weapon_type in NEW_PROPOSALS:
        return _proposed_profile(weapon_type)
    if weapon_type == 'bow':
        return None
    hm, ht, mm, mt, rt, ec, et, wl, wt, ids, dt, why = ROWS[weapon_type]
    for identifier in (hm, mm, 'rubber', 'energy_glass'):
        material(identifier)
    levels = catalog()['wear']['levels']
    if wl not in levels:
        raise ValueError(f'Unknown catalogue wear level: {wl}')
    return dict(housing=dict(material=hm, text_de=ht), metal=dict(material=mm, text_de=mt),
                rubber=dict(material='rubber', text_de=rt), energy=dict(material='energy_glass', color=ec, text_de=et),
                edge_wear=dict(level=wl, text_de=wt), decals=dict(toolgen=deepcopy(ids), text_de=dt),
                interpretation=why, source=SOURCE,
                catalog=dict(file='docs/textures/catalog.json', wear_levels=sorted(levels)))

# Material/decal facts aligned to texprofile.NEW. The names are proposals,
# not additions to the user's original nine-type texture specification.
NEW_PROPOSALS = {
 '+scout_rifle': ('sniper_rifle','painted','brushed','light_blue','subtle',['serial_s07','tech_lines']),
 '+hand_cannon': ('pistol','painted','polished','orange','medium',['number_01','symbol_diamond']),
 '+linear_fusion_rifle': ('fusion_rifle','painted','satin','violet','subtle',['research','fusion_px7']),
 '+grenade_launcher_special': ('shotgun','painted_matte','rough_cast','orange','medium',['warning_triangle','number_01']),
 '+grenade_launcher_heavy': ('rocket_launcher','painted_matte','rough_cast','orange','strong',['hazard_stripes','warning_triangle']),
 '+machine_gun': ('assault_rifle','painted_matte','brushed','blue','strong',['mil_ar2','hazard_stripes']),
 '+sword': ('pulse_rifle','ceramic','polished','cyan','medium',['symbol_diamond','tech_lines']),
 '+glaive': ('pulse_rifle','ceramic','satin','cyan','subtle',['tech_ring']),
 '+heavy_crossbow': ('sniper_rifle','painted_matte','brushed','orange','medium',['arrow_triangle','serial_s07']),
 '+sidearm:rocket_assisted': ('pistol','painted','brushed','orange','medium',['warning_triangle','number_01']),
 '+pulse_rifle:rocket_assisted': ('pulse_rifle','ceramic','satin','orange','medium',['tech_ring','warning_triangle']),
 '+shotgun:slug': ('shotgun','painted_matte','rough_cast','orange','medium',['serial_s07','hazard_stripes']),
 '+pulse_rifle:dynamic_heat': ('pulse_rifle','ceramic','satin','orange','medium',['tech_ring','warning_triangle']),
 '+grenade_launcher_special:micro_missile': ('rocket_launcher','painted_matte','rough_cast','orange','medium',['hazard_stripes','arrow_triangle']),
 '+hand_cannon:spread_shot': ('shotgun','painted','polished','orange','strong',['hazard_stripes','number_01']),
}

def _proposed_profile(weapon_type):
    parent, housing, metal, energy, wear, decals = NEW_PROPOSALS[weapon_type]
    for identifier in (housing, metal, 'rubber', 'energy_glass'):
        material(identifier)
    levels = sorted(catalog()['wear']['levels'])
    names = dict(painted='Lackiert, glatt',painted_matte='Lackiert, matt',ceramic='Keramik, glatt',
                 brushed='Gebürstetes Metall',satin='Satiniertes Metall',polished='Poliertes Metall',rough_cast='Rauer Metallguss')
    color_names = dict(orange='Orange',blue='Blau',light_blue='Hellblau',violet='Violett',cyan='Cyan')
    return dict(housing=dict(material=housing,text_de=names[housing]),
                metal=dict(material=metal,text_de=names[metal]),
                rubber=dict(material='rubber',text_de='Strukturierte Kontaktzonen'),
                energy=dict(material='energy_glass',color=energy,text_de=color_names[energy]+', Funktionslicht'),
                edge_wear=dict(level=wear,text_de=dict(subtle='Leicht, kontrolliert',medium='Mittel, genutzt',strong='Stark, beansprucht')[wear]),
                decals=dict(toolgen=deepcopy(decals),text_de='Kennungen nach verwandtem Typ'),
                interpretation='Vorschlag, abgeleitet; keine neue Nutzerfestlegung. Farbwert im Profil ist Funktionsziel, die Codex-Palette bleibt eigener Stil.',
                source='Vorschlag, abgeleitet aus claude/generator/texprofile.py NEW; Materialien/Skins aus docs/textures/catalog.json',
                derived_from=parent, catalog=dict(file='docs/textures/catalog.json',wear_levels=levels))
