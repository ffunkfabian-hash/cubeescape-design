"""Texturprofil je Waffentyp aus dem Textur-Blatt des Nutzers (claude-0.8, Paket 4 der Sightline-Linie).

Quelle: Cube Escape `Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp` („Cube Escape – Waffen Texturen 1–9“, Materialien · Farben ·
Oberflächen · Details; Stand der Quelle in Cube Escape `Docs/EQUIPMENT.md`). Je Waffe stehen dort sechs Kacheln mit Kurztext: Gehäuse, Metall,
Gummi, Energie/Leuchten, Kantenabnutzung, Decals. Dieses Modul überträgt sie in den Wortschatz des Texturkatalogs (docs/textures/catalog.json)
und der Toolgen-Decals (Toolgen data/decals.json): Material-IDs des Katalogs, Abnutzungsstufe (subtle/medium/strong), Toolgen-Decals.
Datenübergabe an den Spec (`texture_profile`); seit claude-0.9 zeigen die Blätter es im Feld TEXTURPROFIL (xl.profile_strip), Skins bleiben Sache der Pipeline.
Wo der Kurztext mehrdeutig ist, steht die Auslegung in `interpretation`; maßgeblich bleibt das Blatt des Nutzers.
Ohne numpy.
"""
import texcat

SOURCE=('Cube Escape Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp (Textur-Blatt des Nutzers); Übertragung in den Katalog-Wortschatz '
        'durch Claude, 18.10.2026')
# Kurztexte des Blatts: (Gehäuse, Metall, Gummi, Energie, Kantenabnutzung, Decals) – de, wie dort geschrieben
# Katalog-Material je Kachel: housing/metal aus materials[].id (painted, painted_matte, ceramic, brushed, satin, polished, rough_cast)
_P=lambda housing,hm,metal,mm,rubber,energy,ecolor,wear,wde,decals,dde,why=None:dict(
    housing=dict(material=hm,text_de=housing),metal=dict(material=mm,text_de=metal),
    rubber=dict(material='rubber',text_de=rubber),energy=dict(material='energy_glass',color=ecolor,text_de=energy),
    edge_wear=dict(level=wear,text_de=wde),decals=dict(toolgen=decals,text_de=dde),interpretation=why)
PROFILES={
 'pistol':_P('Lackiert, leicht matt','painted','Gebürstet, robust','brushed','Griffig, strukturiert','Orange, klar','orange',
             'subtle','Subtil, realistisch',['symbol_diamond','number_01'],'Symbole, Nummern'),
 'assault_rifle':_P('Lackiert, leicht matt','painted','Industrie-Finish','brushed','Struktur, Griffe','Blau, Tech-Elemente','blue',
                    'medium','Mittel, genutzt',['mil_ar2','tech_bars'],'Militärisch, Tech','Metall „Industrie-Finish“ als gebürstet gedeutet'),
 'pulse_rifle':_P('Keramik-Look','ceramic','Dunkel, satiniert','satin','Strukturiert','Violett, leuchtend','violet',
                  'subtle','Kontrolliert',['tech_ring'],'Tech-Symbole','„Kontrolliert“ als subtle gedeutet (geringste Stufe)'),
 'shotgun':_P('Strapazierfähig, matt','painted_matte','Rau, massiv','rough_cast','Griffzonen','Orange, kräftig','orange',
              'strong','Stark, abgenutzt',['hazard_stripes'],'Warnhinweise'),
 'sniper_rifle':_P('Sauber, präzise','painted','Hochwertig, fein','brushed','Minimal, griffig','Hellblau, präzise','light_blue',
                   'subtle','Leicht, dezent',['serial_s07'],'Seriennummern'),
 'smg':_P('Leicht, widerstandsfähig','painted_matte','Dunkel, genutzt','brushed','Stark strukturiert','Cyan, lebendig','cyan',
          'medium','Mittel, authentisch',['arrows_chevron','arrow_triangle'],'Taktisch, Pfeile','Metall „Dunkel, genutzt“ als gebürstet gedeutet'),
 'fusion_rifle':_P('Hochtechnologie, glatt','painted','Präzise, clean','satin','Technisch, lamellen','Violett, intensiv','violet',
                   'subtle','Gezielt, dezent',['research'],'Forschungs-Symbol','Metall „Präzise, clean“ als satiniert gedeutet'),
 'scout_rifle':_P('Glatt, sauber','painted','Premium, poliert','polished','Minimal','Blau, kontinuierlich','blue',
                  'subtle','Leicht, sauber',['tech_lines'],'Tech, Linien'),
 'rocket_launcher':_P('Schwer, robust','painted_matte','Massiv, angeraut','rough_cast','Stoßdämpfend','Orange, Hitze','orange',
                      'strong','Stark, realistisch',['hazard_stripes','warning_triangle'],'Warnzeichen','Decals: Warnzeichen plus die Warnstreifen der Schrotflinte'),
}   # Bogen: kein Eintrag im Blatt (Waffen 1–9)

# Neue Waffentypen (claude-0.10 und 0.10.1, Schlüssel wtypes.key): nicht im Textur-Blatt des Nutzers. Vorschlag von Claude im selben Wortschatz,
# abgeleitet vom verwandten Typ des Blatts (derived_from); Kurztexte von Claude. Maßgeblich bleibt eine spätere Festlegung des Nutzers.
SOURCE_NEW=('Vorschlag claude-0.10 (kein Eintrag im Textur-Blatt weapon_textures_1-9.webp): abgeleitet vom verwandten Typ (derived_from), '
            'Katalog-Wortschatz docs/textures/catalog.json, Toolgen-Decals data/decals.json')
NEW={
 '+scout_rifle':('sniper_rifle',_P('Glatt, präzise','painted','Fein gebürstet','brushed','Minimal, griffig','Hellblau, ruhig','light_blue',
                 'subtle','Leicht, sauber',['serial_s07','tech_lines'],'Seriennummer, Linien')),
 '+hand_cannon':('pistol',_P('Lackiert, schwer','painted','Poliert, massiv','polished','Griffschalen, strukturiert','Orange, Hitze','orange',
                 'medium','Mittel, Holster-Spuren',['number_01','symbol_diamond'],'Nummer, Symbol')),
 '+linear_fusion_rifle':('fusion_rifle',_P('Hochtechnologie, glatt','painted','Präzise, clean','satin','Technisch, lamellen','Violett, gebündelt','violet',
                         'subtle','Gezielt, dezent',['research','fusion_px7'],'Forschung, Typkennung','Kennung fusion_px7 aus Toolgens Fusionsgewehr übernommen')),
 '+grenade_launcher_special':('shotgun',_P('Robust, matt','painted_matte','Massiv, angeraut','rough_cast','Griffzonen','Orange, Zünder','orange',
                              'medium','Mittel, Einsatz',['warning_triangle','number_01'],'Warnzeichen, Nummer')),
 '+grenade_launcher_heavy':('rocket_launcher',_P('Schwer, robust','painted_matte','Massiv, angeraut','rough_cast','Stoßdämpfend','Orange, Hitze','orange',
                            'strong','Stark, realistisch',['hazard_stripes','warning_triangle'],'Warnstreifen, Warnzeichen')),
 '+machine_gun':('assault_rifle',_P('Feldausrüstung, matt','painted_matte','Industrie-Finish','brushed','Griffzonen, Gurtführung','Blau, Tech-Elemente','blue',
                 'strong','Stark, Dauereinsatz',['mil_ar2','hazard_stripes'],'Militärisch, Warnstreifen','Metall „Industrie-Finish“ wie Sturmgewehr als gebürstet gedeutet')),
 '+sword':('pulse_rifle',_P('Keramik, glatt','ceramic','Klinge poliert','polished','Gewickelter Griff','Cyan, Schneide','cyan',
           'medium','Mittel, Klingenkante',['symbol_diamond','tech_lines'],'Symbol, Linien','Klinge als poliertes Metall, Parierblock als Keramik')),
 '+glaive':('pulse_rifle',_P('Keramik-Look','ceramic','Dunkel, satiniert','satin','Griffzonen','Cyan, Klinge','cyan',
            'subtle','Kontrolliert',['tech_ring'],'Tech-Symbole')),
 '+heavy_crossbow':('sniper_rifle',_P('Robust, matt','painted_matte','Gebürstet, Spannteile','brushed','Griffig','Orange, Bolzen','orange',
                    'medium','Mittel, Spannspuren',['arrow_triangle','serial_s07'],'Pfeil, Seriennummer')),
 '+sidearm:rocket_assisted':('pistol',_P('Lackiert, leicht matt','painted','Gebürstet, Abgasspuren','brushed','Griffig, strukturiert','Orange, Raketen','orange',
                             'medium','Mittel, Abgasspuren',['warning_triangle','number_01'],'Warnzeichen, Nummer')),
 '+pulse_rifle:rocket_assisted':('pulse_rifle',_P('Keramik-Look','ceramic','Dunkel, satiniert','satin','Strukturiert','Orange, Raketen','orange',
                                 'medium','Mittel, Abgasspuren',['tech_ring','warning_triangle'],'Tech-Symbol, Warnzeichen')),
 '+shotgun:slug':('shotgun',_P('Strapazierfähig, matt','painted_matte','Rau, massiv','rough_cast','Griffzonen','Orange, kräftig','orange',
                  'medium','Mittel, abgenutzt',['serial_s07','hazard_stripes'],'Seriennummer, Warnstreifen')),
 # claude-0.10.1
 '+pulse_rifle:dynamic_heat':('pulse_rifle',_P('Keramik, hitzefest','ceramic','Angelaufen, satiniert','satin','Strukturiert','Orange, Hitze','orange',
                               'medium','Mittel, Hitzespuren',['tech_ring','warning_triangle'],'Tech-Symbol, Warnzeichen',
                               'Angelaufenes Metall der Kühlrippen als satiniert gedeutet')),
 '+grenade_launcher_special:micro_missile':('rocket_launcher',_P('Schwer, robust','painted_matte','Massiv, angeraut','rough_cast','Stoßdämpfend','Orange, Raketen','orange',
                                            'medium','Mittel, Abgasspuren',['hazard_stripes','arrow_triangle'],'Warnstreifen, Pfeil')),
 '+hand_cannon:spread_shot':('shotgun',_P('Lackiert, schwer','painted','Poliert, massiv','polished','Griffschalen, strukturiert','Orange, kräftig','orange',
                              'strong','Stark, Schrotspuren',['hazard_stripes','number_01'],'Warnstreifen, Nummer')),
}
DERIVED_FROM={k:v[0] for k,v in NEW.items()}
PROFILES.update({k:v[1] for k,v in NEW.items()})

def profile(tid):
    """Texturprofil des Waffentyps (Spec-Feld `texture_profile`) oder None (Bogen); tid = wtypes.key (Toolgen-ID bzw. +Designtyp)"""
    p=PROFILES.get(tid)
    if p is None:return None
    out={k:(dict(v) if isinstance(v,dict) else v) for k,v in p.items() if k!='interpretation'}
    out['interpretation']=p['interpretation']
    out['source']=SOURCE_NEW if tid in NEW else SOURCE
    if tid in NEW:out['derived_from']=DERIVED_FROM[tid]
    out['catalog']=dict(file='docs/textures/catalog.json',wear_levels=sorted(texcat.wear_levels()))
    return out
