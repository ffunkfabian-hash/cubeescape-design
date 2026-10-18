# Weapon-Spec der Konzeptblätter (`KXnn.spec.json`, format_version 1)

Stand 18.10.2026 (claude-0.2, Feld `skin` seit claude-0.3, `moving_parts`, Fenstergeometrie und Richtungstest seit claude-0.5, `robot_fit` seit claude-0.5.1, `sight.type`/`frame` und `parts[].toolgen_material` seit claude-0.5.2, Visier der Visier-Serie mit `sight.sight_spec` seit claude-0.7). Neben jedem Konzeptblatt `claude/output/sheets/KXnn.dc.html` liegt `KXnn.spec.json` mit den
Werten des Blatts als Daten, damit Toolgen (und Cube Escape) sie nicht aus dem Bild lesen müssen. Die Blätter bleiben das
Zielbild (Entscheidung des Nutzers, 16.10.2026); der Spec ist ihre maschinenlesbare Fassung.

- Erzeugen: `python3 claude/generator/export_spec.py` (alle 60) bzw. `… KC01 KD05`; prüfen: `… --check` (Exit 1 bei veraltet).
- Test: `python3 claude/generator/test_spec.py` (Schema, Stimmigkeit, Aktualität, Richtung mit Gegenbeweis; ohne numpy, ohne Bildstufe, ~25 s).
- Befunde und Hinweise lesen: `python3 claude/generator/spec_checks.py` (Richtung, Visier gegen das CE-Zielbild, Fenster ohne Geometrie).
- Schema: [weapon-spec.schema.json](weapon-spec.schema.json). Quelle der Werte: dieselben Python-Modelle wie das Blatt
  (`sheetmodels.py` lädt sie wie die Bauskripte, ohne zu rendern).
- **Vertrag:** Felder werden nur ergänzt (gleiche `format_version`); Umbenennen, Entfernen oder andere Bedeutung → `format_version` 2.
  Abnehmer prüfen `format` und `format_version` und ignorieren unbekannte Felder.

## Felder

| Feld | Inhalt |
|---|---|
| `format`, `format_version` | `cubeescape-design/weapon-spec`, `1` |
| `sheet` | `id` (KC01 …), `file`, `variant` (Kennbuchstabe C/D/F/G/H/J …), `variant_name` (englischer Name der Variante, z. B. „Black Ice“; `null` bei C–H; ab claude-0.4, additiv), `number`, `nick`, `fid` |
| `weapon` | `name_de`, `toolgen_id` (pistol, assault_rifle, pulse_rifle, shotgun, sniper_rifle, smg, fusion_rifle, scout_rifle, rocket_launcher, bow) |
| `element` | `solar`/`arc`/`void`/`energy` je Waffentyp nach Entscheidung des Nutzers (17.10.2026, Toolgen `docs/ENTSCHEIDUNGEN.md`); Bogen `null` (nicht festgelegt) |
| `units` | `model_unit_m` (Faktor Modelleinheit → m), `model_length_units`, `reference_length_m`, `rule`, `reference` |
| `axes` | Modellachsen, Ziel Toolgen/Blender, Matrix, Ursprung `Socket_Hand` |
| `dimensions_m` | `weapon` (ohne Visier) und `with_sight`: `length` (−Y), `height` (Z), `width` (X), `bounds_m` |
| `anchors` | `Socket_Hand`, `Socket_SupportHand`, `Socket_Muzzle`, `Socket_CenterOfMass`, `Socket_Sight`: `position_m` (Toolgen-Rahmen), `model` (Modelleinheiten), `source`, `part` (Teil, aus dem der Anker stammt; claude-0.5); nicht ableitbar → `null` mit Grund |
| `palette` | vier Farbvarianten des Blatts (`base`, `standard`, `arktis`, `nacht`): `swatches` (Blatt), `channels` (7 MT-Slots → sRGB-Hex oder `null`), `other_colors` (weitere Farben im Kanal mit Flächenanteil) |
| `channels_used` | Kanäle, die Teile oder Aufkleber belegen |
| `parts[]` | `id` (p00 …, Reihenfolge des Modells), `label` (deutsche Bauteilbezeichnung oder `null`), `channel`, `channel_source`, `material`, `emissive`, `sight`, `color` (Basis), `area_m2`, `long_axis`, `bounds_m`, `moving` (Art aus `moving_parts` oder `null`; claude-0.5), `toolgen_material` (claude-0.5.2), `texture` (claude-0.8: Material-ID im Texturkatalog `docs/textures/catalog.json`, `null` bei Glas) |
| `moving_parts` | (claude-0.5, optional) bewegliche Teile wie Toolgens Use-Clip – siehe [Bewegliche Teile](#bewegliche-teile) |
| `robot_fit` | (claude-0.5.1, optional) Größe in der Roboterhand: Zielzahlen mit Quelle und das Blatt daran gemessen – siehe [Größe in der Roboterhand](#größe-in-der-roboterhand) |
| `sight` | `present`, `kind`, `window`, `source`, `modular` (immer separat), `mount_side`, `labels`, `parts`, `bounds_m`, `anchor`, `window_geometry` (Fensterelemente mit Durchsichtachse oder `null`), `window_geometry_note` (Grund bei `null`; beide claude-0.5), `type`, `frame` mit `type_source`/`frame_source` (claude-0.5.2, siehe [Visier-Vokabular](#visier-vokabular)), `sight_spec` (claude-0.7, Waffen 1–9: [Visier der Visier-Serie](#visier-der-visier-serie)) |
| `decals[]` | `part`, `channel`, `surface` (left/right/front/back/top), `emissive`, `color`, `area_m2`, `bounds_m` |
| `textures` | Muster der Materialansicht des Blatts in mm, im Wortschatz von Toolgen `data/surface_recipes.json › patterns`; seit claude-0.8 aus dem Texturkatalog (`catalog`: Datei, Version, sha256 der gelesenen Teile, Katalog-IDs), für jede Waffe gleich |
| `texture_profile` | (claude-0.8, optional, nicht beim Bogen) Texturprofil des Waffentyps aus dem Textur-Blatt des Nutzers – siehe [Texturprofil](#texturprofil) |
| `skin` | (claude-0.3, optional) fünf Skins je Waffe aus einem Katalog von neun, der erste ist der Hauptskin des Blatts – siehe [Skins](#skins) |
| `summary` | Anzahlen, Kanäle mit Nebenfarben je Variante |

Farben sind sRGB-Hex `#RRGGBB` wie im Cube-Escape-Design (`Docs/EQUIPMENT.md` › Farbkanäle).

## Achsen und Maßstab

- **Modell:** x = vorn (Mündung), y = unten, z = links (Einheit: Modelleinheit). **Ziel:** Toolgen/Blender, vorn −Y, oben +Z,
  links +X, Meter, Ursprung `Socket_Hand`. `p_m = model_unit_m · M · (p_model − Socket_Hand.model)` mit
  `M = [[0,0,1],[−1,0,0],[0,−1,0]]` (Drehung, det +1).
- **Maßstab je Blatt:** Die Blätter sind jeweils formatfüllend gezeichnet (Pistolen 438–629, Gewehre 570–1030 Einheiten lang),
  einen gemeinsamen Maßstab gibt es nicht. Deshalb gilt je Blatt `model_unit_m = Toolgen-Länge des Waffentyps / Modelllänge`
  (Länge entlang der Mündungsachse, Visier montiert); die Proportionen des Blatts bleiben erhalten. Bezug: Toolgen-0.13-Weltmodelle,
  `qa_game.json › bounds_lod0.source_bounds_m`, Messung 17.10.2026: Pistole 0,243 · Sturmgewehr 0,934 · Impulsgewehr 0,862 ·
  Schrotflinte 0,904 · Scharfschützengewehr 1,134 · MP 0,616 · Fusionsgewehr 0,960 · Spurgewehr 1,044 · Raketenwerfer 0,725 m.
  Bogen: größte Ausdehnung = 1,018 m (Toolgen-Bogen, Wurfarm-Spannweite); bei der Armbrust KC10 ist das die Länge.
- Ändern sich die Toolgen-Längen, ändert sich nur die Tabelle `WEAPONS` in `export_spec.py`; neu exportieren.

## Anker (Ableitung)

- `Socket_Hand`: Mitte des Teils „Griff“/„Pistolengriff“/„Griffstück“, bei mehreren das dem Abzug nächste dahinter (Toolgen: Mitte des Pistolengriffs).
- `Socket_SupportHand`: Mitte von „Vordergriff“/„Pumpgriff“, sonst eines zweiten Griffs davor, sonst des größten Handschutzes
  (Handschutz/Laufverkleidung/Laufmantel/Laufhülle) vor dem Griff; sonst `null` (meist Pistolen; Toolgen nutzt dort „cup“ am Rahmen).
- `Socket_Muzzle`: Vorderkante des vordersten Lauf-/Mündungsteils, Querschnittsmitte; Bogen: Pfeilspitze. Seit claude-0.5 verlängert
  über unbezeichnete Teile, die die Mündungsachse schneiden und vorn anschließen (Mündungskappe, Leuchtkopf, Pfeilspitze); eine Rakete
  im Rohr samt Teilen in ihrem Querschnitt ist Geschoss und zählt nicht. Betroffen: 17 Blätter, bis 7,2 cm weiter vorn (KD10).
- `Socket_CenterOfMass`: Näherung, Hüllquader-Volumen je Teil gewichtet, Visier montiert.
- `Socket_Sight`: Waffen 1–9 (seit claude-0.7) Oberkante der Visierschiene unter der Mitte der Halterung = `Socket_Mount` des
  Sight-Specs (bei einer Erhöhung darunter); Bögen: Unterkante Mitte der Visierbaugruppe in montierter Lage.
- Toolgen prüft Anker gegen sein eigenes Netz; die Werte hier sind das Zielbild, kein Ersatz für diese Prüfung.

## Kanäle

Sieben Slots wie in Cube Escape: `MT_Primary`, `MT_Secondary`, `MT_Accent`, `MT_Metal`, `MT_Energy` (Energieglas),
`MT_Emission` (Leuchtanzeige), `MT_Detail` (Gummi/Kleinteile).

1. **Ausdrücklich:** `eng.channel(m,'MT_…')` nach dem Teil (Modelle C/D), `ch='MT_…'` im Bau-Eintrag (fgen-ITEMS, flib-Spec).
   Gilt nur für den Export; das Blatt (Zeichnung, Farbvarianten) liest es nicht. `channel_source: explicit`.
2. **Rückfall (Heuristik, `xlroles.assign_channels`):** bevorzugter Kanal aus der Farbrolle des Blatts (`color_roles`, wie für
   die Farbvarianten) und dem Material: hell/Gehäuse → Primary, heller als Gehäuse → Secondary, gesättigte Kleinfläche → Accent,
   gebürstet → Metal, gummiert/matt dunkel → Detail, sonst mittel → Secondary; leuchtende Teile → Energy, leuchtende Aufkleber →
   Emission (auf Energy-Teilen Energy). Danach Verteilung: Je (Farbe, Kanal)-Gruppe – zuerst die Palettenfarben des Blatts, dann
   nach Fläche – bekommt eine Gruppe ab 4 % Flächenanteil ihren Kanal, wenn er frei ist oder schon dieselbe Farbe trägt, sonst einen
   freien Ausweichkanal (`channel_source: distributed`); so bleiben zweifarbige Gehäuse zweifarbig. Was keinen Platz findet, bleibt
   im bevorzugten Kanal und steht in `other_colors`.
3. **Palette je Variante:** Kanalfarbe = Farbe mit der größten Fläche (Teile + Aufkleber) im Kanal. Die Varianten `standard`,
   `arktis`, `nacht` entstehen wie im Blatt mit `recolor` (Rollen der Waffe ohne Visier); Visierteile sind im Blatt nicht
   umgefärbt gezeigt, ihre Farben sind mit derselben Regel ergänzt (`sight_colors: extrapoliert`).

Stand 17.10.2026: alle Zuordnungen heuristisch (0 ausdrücklich); 34 Kanäle in der Basis-Palette haben Nebenfarben über 10 %
(meist zwei Metalltöne in `MT_Metal` oder dunkle Aufkleber in `MT_Detail`). Feinjustage je Blatt über `channel`/`ch`.

## Material, Visier, Aufkleber, Texturen

- `material`: `painted` (lackiert), `brushed` (gebürstet), `rubber` (gummiert), `matte` (matter Kunststoff), `lit` (beleuchtet) –
  dieselbe Zuordnung wie die Materialansicht des Blatts (`material_of`); seit claude-0.7 `glass` (Glasscheiben der Visier-Serie,
  `toolgen_material: null`). Teile der Visier-Serie tragen das Material ihres Sight-Specs.
- `sight.kind` im Toolgen-Wortschatz `hold.sight_kind` (`iron`, `reflex`, `holo`, `scope`, `energy`) plus `pin` (Bogen-Pinvisier);
  `window`: `none` (Kimme/Korn), `open` (Ring, Lochblende, Klappvisier ohne Glas), `glass` (flache Scheibe), `lens` (runde Optik).
  Waffen 1–9: aus dem Typ der Visier-Serie (unten); Bögen: je Blatt in `export_spec.SIGHTS` (ab J `META['sight']`) mit Quelle.
  `mount_side`: `left` bei den Raketenwerfern (Schiene links am Rohr), sonst `top`. Alle 60 Blätter haben ein separates Visier.
- `decals`: jeder Aufkleber des Modells (beidseitige als zwei Einträge), Fläche nach Ebene: `left` (+X), `right` (−X), `front` (−Y),
  `back` (+Y), `top` (+Z).
- `textures`: Muster der Materialansicht des Blatts (`xl.make_texture`) in mm: gebürstet → `brushed` entlang `long_axis` des Teils,
  gummiert → `knurl` (Rautenteilung), matt → `grain`, lackiert → Glanzverlauf ohne Relief, leuchtend → ohne Muster.
  Gestaltete Muster (Farbflächen, Glyphen, Streifen über mehrere Teile) stehen im Feld `skin` (claude-0.3).

## Texturprofil

claude-0.8 (Paket 4 der Sightline-Linie): Cube Escape `Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp` („Waffen Texturen 1–9“) legt je Waffe
sechs Kacheln fest. `texture_profile` überträgt sie in den Wortschatz des Texturkatalogs und der Toolgen-Decals (nicht beim Bogen; Waffen 1–9):
`housing`, `metal`, `rubber`, `energy` (je `material` = Katalog-ID, `text_de` = Kurztext des Blatts, `energy.color`), `edge_wear.level`
(`subtle`/`medium`/`strong`, Stufen des Katalogs `wear.levels`), `decals.toolgen` (IDs aus Toolgen `data/decals.json`), `interpretation`
(Auslegung, wo der Kurztext mehrdeutig war), `source`, `catalog`. Die Konzeptblätter zeichnen das Profil nicht neu (Skins bleiben Sache der
Pipeline); es ist die Zuordnung für Toolgen. Quelle der Daten: `claude/generator/texprofile.py`, geprüft von `test_texcat.py`.

## Skins

Wunsch des Nutzers (17.10.2026): Die Waffen bekommen über Material und Kanalfarbe eine Gestaltungsebene mit fünf Bausteinen –
**Farbflächen** über Bauteilgrenzen (zweifarbige Blöcke, diagonale/gestufte Teilungen), **Glyphen/Zahlen/Embleme** als
Aufkleber-Gruppen, **Streifen, Verläufe, konzentrische Ringe**, **poliertes Gold/Chrom** gegen dunkles Metall mit
**Kantenabnutzung**, **Schmuckteile** (Rippen, Finnen). Stimmung, kein Nachbau: Ziffern, Runen und Embleme sind eigene
Formen (`skins.py`, Segmentziffern, acht Runen, Würfel/Winkel/Ring). Entscheidungen des Nutzers: Katalog mit fünf Skins je
Waffe; Farben aus den MT_-Kanälen plus zwei feste Skin-Akzente; erst je Familie ein Probeblatt (KC01, KD02, KF05, KG07, KH10).

- **Katalog** (seit claude-0.8 aus `docs/textures/catalog.json` gelesen, `skins.CATALOG`, 9; `skin.catalog_id` und `skin.items[].catalog_id` = ID im Katalog): `rennstreifen`, `goldglyphe`, `warnblock`, `zweiton`, `stufenblock`, `zielringe`,
  `glutverlauf`, `chromrippe`, `glyphenband`. Je Blatt fünf (`skins.pick`: Drehung des Katalogs je Blatt, Skins, deren Lagen alle
  Platz finden, zuerst; Black Ice bevorzugt bei Gleichstand dunkle Skins, seit claude-0.8); `skin.hero` = erster = Hauptskin, im Blatt in Isometrie, Orthos und Farbvarianten, alle fünf im Feld
  **SKIN/MUSTER** (neue untere Reihe, Blatt 4800×4432).
- **Slots:** die sieben MT_-Kanäle färben mit der Variante um; an der Waffe unbelegte Kanäle nehmen das Farbfeld der Blatt-Palette
  (`source: swatch`: Primary hell, Secondary/Metal mittel, Detail dunkel, Accent/Energy/Emission Akzent). `SK_Accent1`/`SK_Accent2`
  sind feste Farben je Skin mit Oberfläche (`finish`): `paint`, `polished_gold`, `polished_chrome`, `neon` (leuchtend).
  `items[].colors` nennt je Variante (`base`, `standard`, `arktis`, `nacht`) Farbe, Oberfläche und Quelle jedes benutzten Slots.
- **Raum:** alle Muster im Objektraum (Toolgen-Rahmen, m, Ursprung `Socket_Hand`), keine UV – Blender: Objekt-Koordinaten.
  Sichtteile und leuchtende Teile tragen keinen Skin.
- **Lagen** (`items[].layers[]`, in Reihenfolge; spätere überdecken frühere), `block` = Baustein, `pattern` = Mustertyp:

| `type` | Werte | Bedeutung |
|---|---|---|
| `side_block` | `parts`, `slot`, `poly_yz_m` | Polygon in der Seitenprojektion ([Y, Z]), durch die Breite (X) extrudiert |
| `bands` | `parts`, `dir`, `t0_m`, `width_m`, `period_m`, `count`, `slots`, `window_yz_m` | Streifen quer zu `dir` (t = p·dir); Rennstreifen `dir` X, Seitenband Z, Warnstreifen schräg mit Fenster |
| `gradient` | `parts`, `dir`, `t0_m`, `t1_m`, `steps`, `slots` | gestufter Farbverlauf zwischen zwei Slots (Mischfarbe, keine Kanal-Maske) |
| `rings` | `parts`, `axis` (X), `center_yz_m`, `r0_m`, `width_m`, `gap_m`, `count`, `slots` | konzentrische Ringe in der Seitenprojektion |
| `finish` | `parts`, `slot`, `target` | ganze Teile im Slot (meist Metallteile → Gold/Chrom) |
| `edge_wear` | `parts`, `width_mm`, `coverage`, `color` | blankes Metall an harten Kanten, fleckig (Blender: Pointiness/AO) |
| `glyphs` | `part`, `items`, `content`, `height_m`, `bounds_m`, `decals[]` (`surface`, `slot`, `points_m`) | Aufkleber auf beiden Seitenflächen, rechte Seite gespiegelt (lesbar) |
| `trim` | `kind` (`ribs`/`fins`), `attach`, `slot`, `parts[]` (`profile_yz_m`, `x_m`, `bounds_m`) | zusätzliche Prismen auf der Fläche bzw. oben; `toolgen_similar` `lamellae` bei Rippen |

- **Toolgen-Wortschatz:** `data/surface_recipes.json › patterns` kennt nur Relief (`knurl`, `grooves`, `lamellae`, `seams`,
  `brushed`, `grain`). Die Skin-Muster sind neue Typen, je Spec in `skin.new_pattern_types` beschrieben; Toolgen entscheidet,
  welche es als Kanal-Masken backt (MT_-Slots je Texel) und welche als feste Farben.
- **Platz:** Glyphen und Rippen suchen ein freies Rechteck auf einer flachen Seitenfläche (nicht verdeckt, frei von Aufklebern,
  beide Seiten), Finnen einen freien Platz oben ohne Visierschiene; ohne Platz entfällt die Lage mit Eintrag in `notes`
  (Finnen weichen auf Rippen aus). Stand claude-0.3: zwei Lagen ohne Platz (KC09 Raketenwerfer, Rohrkörper).
- **Zeichnung:** `skinraster.py` liest die Toon-Stufe jedes Bildpunkts aus seiner Helligkeit und schattiert die Skinfarbe gleich;
  Gold/Chrom mit eigener Tonleiter und Glanzstreifen (nur Zeichnung), Kantenabnutzung über Kantenabstand und Zellrauschen.

## Bewegliche Teile

`moving_parts` (claude-0.5) beschreibt je Waffe die Teile, die Toolgens Use-Clip bewegt (Toolgen `docs/TECHNIK.md` › Waffen 1–9 ›
Use-Clip, `weapon_designs.py` `DESIGNS[…]['use_clip']`, Stand c926f50). Die Wurzel bewegt sich nie (`root_moves: false`). Weg, Bilder und
Vorzeichen legt Toolgen im Clip fest; hier stehen Art, Achse und die Teile des Blatts.

| `kind` | Waffe | Toolgen-Knoten | Bewegung (Toolgen-Rahmen) | Bezeichnungen (`label`) / ähnlich (`similar`) |
|---|---|---|---|---|
| `slide` | Pistole | `Anim_Slide` | translate +Y (zurück) | Schlitten / Verschluss |
| `bolt` | Sturmgewehr, MP, Spurgewehr | `Anim_Bolt` | translate +Y | Verschluss, Ladehebel, Spannhebel |
| `cell` | Impulsgewehr | `Anim_Cell` | translate +Y (drei Impulse) | Zelle, Pulszelle / Kristallkern, Energiekugel, Pulswürfel |
| `pump` | Schrotflinte | `Anim_Bolt` | translate +Y | Pumpgriff, Repetierschieber |
| `lever` | Scharfschützengewehr | `Anim_Bolt` | rotate um Y, dann translate +Y | Kammerstängel, Kammer / Verschluss |
| `fins` | Fusionsgewehr | `Anim_FinL/R` | rotate um Z (gegenläufig) | Flossen, Finnen |
| `coil` | Fusionsgewehr | `Anim_Coil` | rotate um Y | Spulenring(e) / Beschleunigerring |
| `hatch` | Raketenwerfer | `Anim_Hatch` | rotate um X | Ladeklappe, Klappe |

- `items[]`: `kind`, `name_de`, `toolgen_node`, `motions[]` (`type` translate/rotate, `axis` Einheitsvektor), `parts` (Teil-IDs ohne
  Visierteile) oder `null`, `labels`, `match` (`label` = Bezeichnung wie in Toolgen, `similar` = ähnliches Teil, Toolgen entscheidet;
  `null` = nicht ableitbar), `source` (bei `null` der Grund). Der Bogen hat keine Einträge (`note`).
- Zuordnung nur über Bezeichnungen der Modelle. Die `Energiezelle` der Impulsgewehre ist das Magazin (Toolgen `Anim_EnergyCell`, nicht
  im Use-Clip) und zählt nicht als `cell`; `Kühlrippen` sind Ringe um den Lauf, keine Flossen.
- Stand claude-0.5: 11 von 60 Einträgen haben Teile (Schlitten 3, Verschluss als ähnliches Teil 1, Pumpgriff 3, ähnliche Zelle 3 von 6,
  Beschleunigerring 1 von 6); Verschluss der Gewehre, Kammerstängel, Ladeklappe und Flossen sind in keinem Blatt bezeichnet.

## Visier-Vokabular

Entscheidung des Nutzers (17.10.2026, claude-0.5.2), additiv: `kind` bleibt Toolgens `hold.sight_kind` und folgt aus `type`.

| `type` | Visiertypen-Blatt | `kind` | Fenster | Ziel für |
|---|---|---|---|---|
| `standard` | Standard-Visier | reflex | glass | – |
| `holo` | Holo-Visier | holo | glass | 2 Sturmgewehr |
| `precision` | Präzisions-Visier | scope | lens | 3 Impulsgewehr |
| `reflex` | Reflex-Visier | reflex | glass | 1 Pistole, 4 Schrotflinte |
| `sniper` | Sniper-Visier | scope | lens | 5 Scharfschützengewehr |
| `machine` | Maschinenvisier | reflex | glass | 6 Maschinenpistole |
| `energy` | Energie-Visier (aktiver Energierahmen) | energy | glass | 7 Fusionsgewehr |
| `trace` | Spur-Visier (Zielverfolgung, Markierung) | holo | glass | 8 Spurgewehr |
| `rocket` | Raketen-Visier | holo | glass | 9 Raketenwerfer |
| `iron`, `pin` | Kimme/Korn, Bogen-Pin (Blätter ohne Ziel) | iron, pin | – | – |

- `frame`: Rahmen-Variante des Visier-Blatts: `standard`, `compact`, `open`, `closed`, `industrial`, `lightweight`; `null` ohne Rahmen
  (Kimme/Korn). Bestehende Blätter: Regel aus `window` nach der Sichtprüfung 0.5.1 (Scheibe im Kasten `closed`, Röhre `standard`,
  Ring/Lochblende `open`); die Visier-Serie VS01–VS09 setzt Typ und Rahmen ausdrücklich.
- Bis claude-0.6 kam `type` aus `kind` (Zielfernrohr am Scharfschützengewehr `sniper`, sonst `precision`); Abweichungen vom Ziel
  (`spec_checks.CE_SIGHTS`) standen als Hinweise im Bericht (0.5.2: 41). Seit claude-0.7 tragen die Waffen 1–9 das Visier der Serie,
  der Hinweis „Visier weicht vom Zielbild ab“ entfällt (0 Hinweise); die Prüfung bleibt.
- `parts[].toolgen_material`: Toolgen `surface_recipes.json` › `materials`: painted → painted, brushed → brushed, rubber → rubber,
  matte → painted_matte, lit → energy_glass, glass → `null` (claude-0.7). Die Decal-Zuordnung zu Toolgens Katalog (`decals.json`) steht seit claude-0.8 je Waffentyp im [Texturprofil](#texturprofil) (`texture_profile.decals.toolgen`); die Aufkleber des Modells (Fenster, Leuchtflächen, Markierungen) haben keine Entsprechung im Toolgen-Katalog und tragen kein Feld.

## Visier der Visier-Serie

Seit claude-0.7 (Entscheidung des Nutzers „Danach Waffenblätter umstellen“, 17.10.2026) trägt jedes Blatt der Waffen 1–9 das
Standardvisier seines Typs aus der Visier-Serie VS01–VS09 ([sight-spec.md](sight-spec.md)); die bisherigen Visierteile (Kimme/Korn,
Kästen, Röhren) sind entfallen. Bögen haben kein VS-Ziel und behalten ihr Pin-Visier; Pin und Leuchtpunkt fluchten seit claude-0.7 entlang −Y (Leuchtpunkt auf der
Rückseite, zum Schützen; KF10 als Ring quer zur Laufachse).

- **Eine Wahrheit:** `vsmount.py` lädt das Modell aus `vsmodels.py` (mm), rechnet es mit `model_unit_m` in Modelleinheiten um und setzt
  `Socket_Mount` auf die Oberkante der Visierschiene unter der Mitte der Halterung (Raketenwerfer: Seitenschiene links am Rohr).
  Die Halterung sitzt längs auf der Mitte der Schiene. Blätter ohne Schiene bekommen eine (`rail.added`, 6 mm über der höchsten Stelle
  der Waffe unter der Halterung, 14 mm breit); längs sitzt das Visier dann wie das bisherige (ein Block: dessen Mitte; Kimme und Korn:
  Halterung ab der Kimme; nur Korn: Mitte des Gehäuses), immer innerhalb der Waffenlänge, damit Länge und Maßstab gleich bleiben.
- **Erhöhung:** Kein Teil des Visiers darf in die Waffe ragen; die Klemmbacken der Halterung (3 mm unter `Socket_Mount`) dürfen nur die
  Schiene umfassen. Sonst steht das Visier auf einem Distanzstück „Erhöhung“ (Teil des Visiers, MT_Metal, auf 0,5 mm gerundet plus
  0,5 mm Luft): `riser_m`. Die Erhöhung steht nur auf dem Teil der Schiene, über den die Waffe nicht hinausragt (Seitenschiene am Rohr).
- **Farben:** je Teil die Kanalfarbe der Waffe in der Basis-Palette (wie bis claude-0.6 gerechnet, damit die Kanäle der Waffe bleiben);
  nutzt die Waffe den Kanal nicht, gilt der erste belegte aus `xlroles.FALLBACK`, und das Teil bekommt diesen Kanal. Leuchtteile bleiben
  auf MT_Energy/MT_Emission; hat die Waffe keinen Leuchtkanal, leuchten sie in ihrer MT_Accent-Farbe. Aufkleber in einer Farbe, die nur
  das Visier trägt, nehmen dessen Kanal. Glas behält die Tönung des Sight-Specs (`material: glass`, zählt nur dann zur Kanalfarbe, wenn sonst nichts auf dem Kanal liegt).
- **`window_geometry`:** die Glasscheiben (`type: part`), Achse aus der Geometrie, wie im Sight-Spec.
- **`sight.sight_spec`:** `id`, `file` (`VSnn.spec.json`), `format`, `mount`, `riser_m`, `socket_mount_m`, `socket_reticle_m`,
  `socket_eye_m` (Röhren, sonst `null`), `line_height_m` (Visierlinie über `Socket_Sight`), `rail` (`part`, `added`, `seat` = Herleitung der
  Lage), `line_clear_of_weapon` / `blocked_by` (kein Teil der Waffe vor dem Visier über der Visierlinie), `replaced` (Bezeichnungen des
  bisherigen Visiers). Achsen wie im Sight-Spec (vorn −Y, oben +Z); `p_waffe = socket_mount_m + (p_sight − Socket_Mount_sight)`.
- **Prüfung:** `spec_checks.vs_problems` (VS-Nummer = Waffennummer, Typ/Rahmen, Anker gegen den Sight-Spec, Glas als Fenster, freie
  Visierlinie, Länge) und `test_spec.VisierSerie` (dazu: kein Visierteil steckt in der Waffe, Farben aus den Kanälen, Gegenbeweise).

## Größe in der Roboterhand

`robot_fit` (claude-0.5.1, Entscheidung des Nutzers 17.10.2026) gibt die Zielmaße einer Roboter-Variante der Weltmodelle (Toolgen,
Cube Escape 0.82 › Stufe 2) als Daten. Roboter-Konzeptblätter gibt es nicht (`concept_sheets: false`, Entscheidung des Nutzers).

- `robot`: Höhe 1,50 m, Hand 0,09 m, Arm 0,42 m (CE `Docs/EQUIPMENT.md` › Maße des Roboters). Jeder Wert als `{value, source}`.
- `targets` (je `{value, source}`): `length_m` (Länge in der Hand, CE-Tabelle auf cm gerundet: MP 0,52 · Sturm 0,67 · Impuls 0,66 ·
  Schrot 0,67 · Fusion 0,67 · Spur 0,69 · Scharfschütze 0,73 · Raketenwerfer 0,65 m), `support_hand_max_forward_m` 0,10,
  `stock_max_behind_m` 0,12, `barrel_min_m` 0,03, `receiver_min_height_m` 0,08, `silhouette_factor` 1,5 (Bezug Toolgen-Weltmodell,
  am Blatt nicht messbar). Pistole: `applies: false` (Maßstab genügt, Becher-Griff), nur `length_min_m` 0,24; Bogen: `applies: false`.
- `sheet_at_target`: das Blatt auf `length_m` skaliert (`scale`) und gemessen: Stützhand vor dem Griff, Schaft hinter dem Griff
  (hinterste Kante, Visier montiert), Lauf (kleinerer Querschnitt des Mündungsteils), Gehäuse (größte Höhe eines Teils „Gehäuse“);
  `ok` je Wert, `null` wenn am Blatt nicht ableitbar. Stand 0.5.1: kein Blatt hält Stützhand (0,12–0,31 m) und Schaft (0,17–0,34 m) ein –
  die Blätter sind Menschenwaffen; die Roboter-Variante muss Toolgen umbauen, nicht skalieren (Befund CE 0.82). Lauf ≥ 3 cm halten
  27 von 48, Gehäuse ≥ 8 cm 28 von 38 messbaren Blättern.

## Richtung und Visier-Zielbild

- **Richtungstest** (`spec_checks.direction_problems`, Lehre Cubegen `docs/DEVELOPER.md` 9.17: die Funktionsfläche prüfen, nicht nur
  Anker oder Bounds): `Socket_Muzzle` vor dem Griff (−Y) und am vorderen Ende der Mündungsachse, im Querschnitt seines Teils;
  `Socket_Hand` im Griffteil, der unter die Mündungsachse reicht; Visier über der Mündungsachse, `Socket_Sight` über dem Griff an der
  Unterkante der Baugruppe (links bei `mount_side: left`); jedes Fensterelement mit Durchsicht entlang Y, Aufkleber flach quer zur
  Laufachse (Achse −Y), Mündung auf einer Vorderkante. Gegenbeweis im Test: Exporter mit gespiegelter Y- bzw. Z-Achse oder vertauschtem
  X/Y schlägt bei jedem Waffentyp an, jeweils mit der zuständigen Prüfung (Mündung, Visier oben, Fenster).
- **Fenster an der Funktionsfläche** (`spec_checks.window_problems`, seit claude-0.5.2; wiederverwendbar für jeden Spec mit
  `window_geometry`, auch die Visier-Serie VS01–VS09): Die Durchsicht ist die flache bzw. dünnste Achse der Scheibe, Öffnung oder des
  Rings selbst, nicht die Rotation oder der Hüllquader des Visiers; sie muss Y sein, `view_axis_m` muss dazu passen (−Y).
  Befundtexte: „Fenster quer [key]“, „Fensterachse [key]“, „Fenster [key] unter dem Griff“; `key` = `dNN` (decals[NN]) oder Teil-ID.
  **Bekannte Querfenster** (`KNOWN_CROSS_WINDOWS`): Stand 17.10.2026 23 Blätter – die 19 aus der Sichtprüfung, dazu KC02, KH03 und die
  Bogen-Pins KD10, KF10 (Generatorfehler: Öffnungen und Scheiben in der Seitenansicht gezeichnet und durch die Breite extrudiert).
  Behoben in claude-0.7 (18.10.2026) mit der Umstellung auf VS01–VS09 und den entlang −Y fluchtenden Bogen-Pins; die Liste
  ist leer. Der Test bleibt und verlangt genau diese Menge; ein neues Querfenster macht ihn rot.
  Gegenbeweis je Fall im Test (Seitenscheibe, Ring/Platte, Leuchtteil oben, falsche Achse, neues Querfenster auf sauberem Blatt).
- **`window_geometry`**: Aufkleber vorn/hinten auf Visierteilen, Seitenaufkleber ab `PANE_MIN_FRACTION` (7,5 %) der Teilfläche als
  Scheibe oder Öffnung (`face_fraction`), leuchtende Visierteile (`type: part`) und Scheiben/Ringe/Platten (`type: disc`: zwei ähnliche
  Ausdehnungen, die dritte höchstens 40 %; nur bei `window` open/lens, wo der Ring die Öffnung ist – das Modell kennt keine Löcher); `view_axis_m` aus der Geometrie. Ohne solches Element `null` mit Grund (Stand 0.5.2: KJ04,
  KJ10; seit claude-0.7 keins). Waffen 1–9: Glasscheiben der Visier-Serie.
- **Visier-Zielbild:** `spec_checks.CE_SIGHTS` gibt die Tabelle aus Cube Escape `Docs/EQUIPMENT.md` › Visiere je Waffe wieder
  (Art und Fenster, die dazu passen). Abweichungen sind **Hinweise**, kein Fehler; ob ein Blatt geändert wird, entscheidet der Nutzer.
  Der Test vergleicht die Tabelle mit der CE-Datei, wenn das Repo lokal liegt (`CE_EQUIPMENT` setzt den Pfad).

## Für Codex (`codex/`)

Das Format ist nicht an Claudes Pipeline gebunden. Codex kann für seine Blätter dieselben Dateien erzeugen (eigener Exporter unter
`codex/`, Ablage neben den eigenen Blättern, `sheet.id` mit eigenem Präfix) und mit dem Schema prüfen. Auftragsentwurf:
[auftrag-codex-spec.md](auftrag-codex-spec.md).
