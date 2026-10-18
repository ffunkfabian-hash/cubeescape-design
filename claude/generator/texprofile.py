"""Texturprofil je Waffentyp aus dem Textur-Blatt des Nutzers (claude-0.8, Paket 4 der Sightline-Linie).

Quelle: Cube Escape `Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp` („Cube Escape – Waffen Texturen 1–9“, Materialien · Farben ·
Oberflächen · Details; Stand der Quelle in Cube Escape `Docs/EQUIPMENT.md`). Je Waffe stehen dort sechs Kacheln mit Kurztext: Gehäuse, Metall,
Gummi, Energie/Leuchten, Kantenabnutzung, Decals. Dieses Modul überträgt sie in den Wortschatz des Texturkatalogs (docs/textures/catalog.json)
und der Toolgen-Decals (Toolgen data/decals.json): Material-IDs des Katalogs, Abnutzungsstufe (subtle/medium/strong), Toolgen-Decals.
Es ist reine Datenübergabe an den Spec (`texture_profile`); die Konzeptblätter zeichnen es nicht neu (Skins bleiben Sache der Pipeline).
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

def profile(tid):
    """Texturprofil des Waffentyps (Spec-Feld `texture_profile`) oder None (Bogen)"""
    p=PROFILES.get(tid)
    if p is None:return None
    out={k:(dict(v) if isinstance(v,dict) else v) for k,v in p.items() if k!='interpretation'}
    out['interpretation']=p['interpretation']
    out['source']=SOURCE
    out['catalog']=dict(file='docs/textures/catalog.json',wear_levels=sorted(texcat.wear_levels()))
    return out
