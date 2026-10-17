# Weapon-Spec der Konzeptblätter (`KXnn.spec.json`, format_version 1)

Stand 17.10.2026 (claude-0.2). Neben jedem Konzeptblatt `claude/output/sheets/KXnn.dc.html` liegt `KXnn.spec.json` mit den
Werten des Blatts als Daten, damit Toolgen (und Cube Escape) sie nicht aus dem Bild lesen müssen. Die Blätter bleiben das
Zielbild (Entscheidung des Nutzers, 16.10.2026); der Spec ist ihre maschinenlesbare Fassung.

- Erzeugen: `python3 claude/generator/export_spec.py` (alle 50) bzw. `… KC01 KD05`; prüfen: `… --check` (Exit 1 bei veraltet).
- Test: `python3 claude/generator/test_spec.py` (Schema, Stimmigkeit, Aktualität; ohne numpy, ohne Bildstufe, ~2 s).
- Schema: [weapon-spec.schema.json](weapon-spec.schema.json). Quelle der Werte: dieselben Python-Modelle wie das Blatt
  (`sheetmodels.py` lädt sie wie die Bauskripte, ohne zu rendern).
- **Vertrag:** Felder werden nur ergänzt (gleiche `format_version`); Umbenennen, Entfernen oder andere Bedeutung → `format_version` 2.
  Abnehmer prüfen `format` und `format_version` und ignorieren unbekannte Felder.

## Felder

| Feld | Inhalt |
|---|---|
| `format`, `format_version` | `cubeescape-design/weapon-spec`, `1` |
| `sheet` | `id` (KC01 …), `file`, `variant` (C/D/F/G/H), `number`, `nick`, `fid` |
| `weapon` | `name_de`, `toolgen_id` (pistol, assault_rifle, pulse_rifle, shotgun, sniper_rifle, smg, fusion_rifle, scout_rifle, rocket_launcher, bow) |
| `element` | `solar`/`arc`/`void`/`energy` je Waffentyp nach Entscheidung des Nutzers (17.10.2026, Toolgen `docs/ENTSCHEIDUNGEN.md`); Bogen `null` (nicht festgelegt) |
| `units` | `model_unit_m` (Faktor Modelleinheit → m), `model_length_units`, `reference_length_m`, `rule`, `reference` |
| `axes` | Modellachsen, Ziel Toolgen/Blender, Matrix, Ursprung `Socket_Hand` |
| `dimensions_m` | `weapon` (ohne Visier) und `with_sight`: `length` (−Y), `height` (Z), `width` (X), `bounds_m` |
| `anchors` | `Socket_Hand`, `Socket_SupportHand`, `Socket_Muzzle`, `Socket_CenterOfMass`, `Socket_Sight`: `position_m` (Toolgen-Rahmen), `model` (Modelleinheiten), `source`; nicht ableitbar → `null` mit Grund |
| `palette` | vier Farbvarianten des Blatts (`base`, `standard`, `arktis`, `nacht`): `swatches` (Blatt), `channels` (7 MT-Slots → sRGB-Hex oder `null`), `other_colors` (weitere Farben im Kanal mit Flächenanteil) |
| `channels_used` | Kanäle, die Teile oder Aufkleber belegen |
| `parts[]` | `id` (p00 …, Reihenfolge des Modells), `label` (deutsche Bauteilbezeichnung oder `null`), `channel`, `channel_source`, `material`, `emissive`, `sight`, `color` (Basis), `area_m2`, `long_axis`, `bounds_m` |
| `sight` | `present`, `kind`, `window`, `source`, `modular` (immer separat), `mount_side`, `labels`, `parts`, `bounds_m`, `anchor` |
| `decals[]` | `part`, `channel`, `surface` (left/right/front/back/top), `emissive`, `color`, `area_m2`, `bounds_m` |
| `textures` | Muster der Materialansicht des Blatts in mm, im Wortschatz von Toolgen `data/surface_recipes.json › patterns` |
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
- `Socket_Muzzle`: Vorderkante des vordersten Lauf-/Mündungsteils, Querschnittsmitte; Bogen: Pfeilspitze.
- `Socket_CenterOfMass`: Näherung, Hüllquader-Volumen je Teil gewichtet, Visier montiert.
- `Socket_Sight`: Unterkante Mitte der Visierbaugruppe in montierter Lage; ohne Visier Oberkante der Visierschiene.
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

Stand 17.10.2026: alle Zuordnungen heuristisch (0 ausdrücklich); 36 Kanäle in der Basis-Palette haben Nebenfarben über 10 %
(meist zwei Metalltöne in `MT_Metal` oder dunkle Aufkleber in `MT_Detail`). Feinjustage je Blatt über `channel`/`ch`.

## Material, Visier, Aufkleber, Texturen

- `material`: `painted` (lackiert), `brushed` (gebürstet), `rubber` (gummiert), `matte` (matter Kunststoff), `lit` (beleuchtet) –
  dieselbe Zuordnung wie die Materialansicht des Blatts (`material_of`).
- `sight.kind` im Toolgen-Wortschatz `hold.sight_kind` (`iron`, `reflex`, `holo`, `scope`, `energy`) plus `pin` (Bogen-Pinvisier);
  `window`: `none` (Kimme/Korn), `open` (Ring, Lochblende, Klappvisier ohne Glas), `glass` (flache Scheibe), `lens` (runde Optik).
  Festgelegt je Blatt in `export_spec.SIGHTS` mit Quelle (Bezeichnung, Text des Blatts, Kommentar/Geometrie im Modell).
  `mount_side`: `left` bei den Raketenwerfern (Schiene links am Rohr), sonst `top`. KD01, KD04, KD10 haben auf diesem Stand kein
  separates Visier (claude-0.1.1 ergänzt es; danach neu exportieren).
- `decals`: jeder Aufkleber des Modells (beidseitige als zwei Einträge), Fläche nach Ebene: `left` (+X), `right` (−X), `front` (−Y),
  `back` (+Y), `top` (+Z).
- `textures`: Muster der Materialansicht des Blatts (`xl.make_texture`) in mm: gebürstet → `brushed` entlang `long_axis` des Teils,
  gummiert → `knurl` (Rautenteilung), matt → `grain`, lackiert → Glanzverlauf ohne Relief, leuchtend → ohne Muster.
  Gestaltete Muster (Farbflächen, Glyphen, Streifen über mehrere Teile) gibt es in Version 1 nicht; sie kämen als neues Feld dazu.

## Für Codex (`codex/`)

Das Format ist nicht an Claudes Pipeline gebunden. Codex kann für seine Blätter dieselben Dateien erzeugen (eigener Exporter unter
`codex/`, Ablage neben den eigenen Blättern, `sheet.id` mit eigenem Präfix) und mit dem Schema prüfen. Auftragsentwurf:
[auftrag-codex-spec.md](auftrag-codex-spec.md).
