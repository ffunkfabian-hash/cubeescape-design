# Geometrie-Spec der Konzeptblätter (`KXnn.geo.json`, `VSnn.geo.json`, format_version 1)

Stand 19.10.2026 (claude-0.13 „Blueprint“, Etappe DS-1 aus [umsetzungsplan-modelle.md](umsetzungsplan-modelle.md) › 3 und › 5.1). Je Blatt eine Datei mit dem
**Netz jedes Teils** in Metern im Toolgen-Rahmen, dazu Primitiv-Hinweise, Aufkleber, Griff, Stützhand, Visier und Anker. Toolgen baut daraus seine Waffen
(Etappe TG-A, `concept_kit.py`); alles danach (Use-Clip, Ego-Hände, ADS, UV1, Karten, Roboter-Variante, Export) bleibt Toolgens Pipeline.

- Erzeugen: `python3 claude/generator/export_geo.py` (alle 159: 150 Waffenblätter, VS01–VS09; ~20 s) bzw. `… KG02 VS02`; prüfen: `… --check`.
- Test: `python3 claude/generator/test_geo_spec.py` (Schema, Netze, Abgleich mit Weapon-/Sight-Spec, Normalen, Aufkleber, Primitive, Koplanar-Regel mit
  Gegenbeweis, Toolgen-Budget). Golden: `claude/tests/golden.json` › `geo` (sha256 je Datei; nach Neubau `python3 claude/tests/test_golden.py --update --geo`).
- Schema: [geometry-spec.schema.json](geometry-spec.schema.json). Quelle: dieselben Modelle wie Blatt, Weapon-Spec und Sight-Spec (`sheetmodels.py`, `vsmodels.py`).
- **Nicht im Repo:** die Dateien sind gitignoriert und kommen als Release-Asset `claude-geo-claude-v<Version>.zip` (Ordner `geo/`, `release_assets.py`).
  Toolgen übernimmt die gewählten Blätter nach `data/concepts/` mit Herkunft (Release, sha256); kein Netzzugriff im Bau.
- **Vertrag:** Felder werden nur ergänzt (gleiche `format_version`); Umbenennen, Entfernen oder andere Bedeutung → `format_version` 2.
  Abnehmer prüfen `format` und `format_version` und ignorieren unbekannte Felder. Abnehmer: Toolgen ab TG-A liest Version 1.
- Weapon-Spec 2 und Sight-Spec 2 bleiben unverändert (kein Verweis `geometry_spec` in claude-0.13; der Geo-Spec verweist mit sha256 auf sie).

## Rahmen

- Meter, 5 Nachkommastellen (0,01 mm). Achsen wie der Weapon-Spec: vorn −Y, oben +Z, links +X (Blender). `p_m = model_unit_m · M · (p_model − Ursprung)`
  mit `M` = `axes.matrix_model_to_target` (Drehung, Determinante +1: der Umlaufsinn bleibt).
- Ursprung: Waffen `Socket_Hand` (wie Weapon-Spec, gleiches `model_unit_m`), Visier-Serie `Socket_Mount` (wie Sight-Spec, 1 Modelleinheit = 1 mm).
- Teile, Reihenfolge und IDs = Weapon-Spec `parts[]` (`p00` …) bzw. Sight-Spec `parts[]` (`g00` …, eine Gruppe = ein Teil).

## Felder

| Feld | Inhalt |
|---|---|
| `format`, `format_version` | `cubeescape-design/geometry-spec`, `1` |
| `generator` | Repo, Werkzeug, `claude_version` |
| `sheet` | `id`, `kind` (`weapon`/`sight`), `variant`, `variant_name`, `number`, `name_de`, `nick`, `toolgen_id`, `design_type` |
| `source` | `weapon_spec` (`file`, `format`, `format_version`, `sha256` der Datei im Repo), `sight_spec` (VSnn: `file`, `sha256`; Bogen/Nahkampf `null`), `model` |
| `units`, `axes`, `origin` | siehe Rahmen |
| `parts[]` | `id`, `name` (Blender-Name `SM_PG_<LabelAscii>_<id>`, Umlaute ae/oe/ue/ss, ohne Bezeichnung `Part`), `label`, `channel` (`MT_…`), `material`, `toolgen_material`, `texture` (Katalog-ID), `color` (Basis), `emissive`, `glass`, `sight`, `moving` (`kind`, `toolgen_node` aus `moving_parts`, sonst `null`), `bounds_m`, `primitive`, `mesh` |
| `parts[].mesh` | `vertices` (m), `faces` (Indexlisten, ebene n-Ecke, auch konkav – mit Blender/bmesh triangulieren), `hard` (je Fläche 1 = harte Kante/flach schattiert, 0 = weich) |
| `parts[].primitive` | Hinweis auf den Bauweg, nur wo er sich aus der Flächenfolge ergibt, sonst `null` (Netz allein maßgeblich): `prism` (`axis`, `profile_axes`, `profile_m`, `range_m`, `smooth_sides`), `cylinder` (`axis`, `start_m`, `end_m`, `radius_m`, `segments`, `first_vertex_m`), `cone` (wie Zylinder mit `radius_start_m`/`radius_end_m`) |
| `decals[]` | Reihenfolge = Weapon-Spec `decals[]`: `part`, `surface`, `normal`, `channel`, `color`, `emissive`, `polygon_m` (auf der Fläche, Umlauf zur Normale). Für Toolgen **Maskenregionen**, keine Geometrie (das Blatt zeichnet sie 0,4 Modelleinheiten ≈ 0,4–0,6 mm darüber, unter der 0,5-mm-Regel; Entscheidung 4 im Plan) |
| `grip` | `part` (= `Socket_Hand.part`), `grip_axis_m` (Unterkante → Oberkante), `grip_tilt_degrees`, `trigger_m`/`trigger_part` (Mitte des Abzugs, sonst `null`), `cross_section_m` (`depth_m` quer zur Achse in halber Höhe, `width_m` = X), `method` |
| `support` | `part` (= `Socket_SupportHand.part`), `radius_m` (`half_height_m` Z, `half_width_m` X: Querschnitt des Teils in der Ebene durch `Socket_SupportHand`), `section_center_m`, `anchor_m`; ohne Stützhand `part`/`radius_m` `null` mit `reason` (Pistolen, Handfeuerwaffen: Becher-Griff) |
| `sight` | Visier-Serie: `id` (VSnn), `kind`, `type`, `frame`, `window_kind`, `sight_spec` (Datei, Format, sha256), `window` (`shape`, `width_m`, `height_m`, `corner_radius_m`, `view_axis_m`), `tube` (Röhre: Länge, Linsen-, Augen-, Bohrungsradius), `socket_mount_m`, `socket_sight_rear_m`, `socket_reticle_m`, `socket_eye_m`, `eye_radius_m`, `socket_eye_source`, `line` (`start_m`, `direction`, `height_above_mount_m`, `above_body_top_m`), `parts`, `glass_parts`, `riser_m`, `rail_part`. Bogen (Pin-Visier): Art und Teile, Anker `null`; Schwert/Glefe `present` false |
| `anchors` | Weapon-Spec-Anker unverändert (`Socket_Hand`, `Socket_SupportHand`, `Socket_Muzzle`, `Socket_CenterOfMass`, `Socket_Sight`: `position_m`, `part`, `source`) plus `Socket_Reticle` und `Socket_Eye`; Visier-Serie: Sight-Spec-Anker (`Socket_Mount`, `Socket_Sight`, `Socket_Reticle`, `Socket_Eye`) |
| `string` | Bogen (KX10) und Armbrust (KX19), sonst `null` (Entscheidung des Nutzers 19.10.2026: Bogen sofort in TG-A): `kind` (`bow`/`crossbow`), `span_axis` (Z bzw. X), `limb_tips_m` (Sehnenenden an Wurfarm bzw. Umlenkrolle), `limb_tip_parts`, `nock_m` (Ruhelage) und `nock_source`, `arrow_axis` (`part`, `rear_m`, `tip_m`, `direction`, `radius_m`; ohne Pfeil `through_m` über der Auflage), `arrow_rest_m` (Oberkante Mitte von Pfeilauflage/Führungsrinne, sonst Unterkante des Bolzens) mit Quelle, `nock_behind_hand_m` (+Y; Armbrust negativ), `string_parts`, `string_segments_m`, `string_length_m`, `limb_parts`, `cam_parts`, `riser_parts` |
| `melee` | `null` in Version 1; `blocks_pending.melee` nennt DS-2 (Schwert, Glefe) |
| `checks` | `coplanar[]` (Befunde, siehe unten), `decals_outside_part` (Indizes in `decals[]`, deren Polygon im Blatt mehr als 1 mm über den Hüllquader seines Teils ragt), `coplanar_rule` |
| `counts` | `parts`, `vertices`, `faces`, `triangles` (n − 2 je Fläche), `decals`, `dropped_faces` (beim Runden entartet; immer 0), `normal_fixes` (Flächen, deren Normale im Modell nach innen zeigte und hier gedreht ist) |

## Regeln und Messwege

- **Normalen nach außen.** Der Umlaufsinn folgt der Normale, die das Blatt zeichnet. Geschlossene Hüllen eines Modellteils (jede Kante an genau zwei Flächen)
  richtet der Exporter zusätzlich über die Kantennachbarschaft aus und dreht sie auf positives Volumen; das korrigiert alte Modelle mit nach innen gespeicherten
  Seitennormalen (claude-0.13: KC10 Wurfarme, 8 Flächen, alter `prism_y`-Weg vor der Umlaufregel aus claude-0.11). Offene Teile (Ringhälften, Mäntel, Linsen-
  scheiben) behalten die gespeicherte Normale. Glas der Visiere sind zwei Flächen am selben Ort (beidseitig).
- **Koplanar (Toolgen-Regel ≥ 0,5 mm).** `checks.coplanar[]` nennt Teilpaare mit gleichgerichteten Flächen unter 0,5 mm Abstand, die sich um mindestens
  1 mm² überdecken (Z-Fighting im Tiefenpuffer; das Blatt zeichnet Teil für Teil und kennt das Problem nicht): `parts`, kleinster `distance_m`, größte
  `overlap_m2`, `normal`, `faces` (Zahl der Flächenpaare), `same_look` (gleicher Kanal, Material, Leuchten, Glas – Flackern kaum sichtbar). Entgegengesetzte
  Flächen (ein Teil sitzt auf dem anderen) zählen nicht. Stand claude-0.13: 915 Paare auf 153 Blättern, 883 davon mit Abstand 0, 338 mit unterschiedlichem
  Aussehen. Befund, kein Fehler: die Modelle bleiben die abgenommenen; TG-A entscheidet (z. B. gleiche Teile verschmelzen, Deckflächen 0,5 mm absetzen,
  Viewer-Determinismus 16 Läufe).
- **Griffachse.** Konvexe Hülle des Griffteils in der Seitenansicht; Mitte der waagrechten Schnitte bei 25 % und 85 % der Höhe ab Oberkante, bis Unter- und
  Oberkante verlängert. `grip_tilt_degrees` positiv = oben nach vorn (Toolgen-Sinn, Pistole 14°); negativ = oben nach hinten (Variante D, bis −15°).
  Liegende Griffteile (länger als hoch: Schwert, Glefe, KF10) bekommen die Längsachse und 90°.
- **Visier.** `socket_sight_rear_m` ist der `Socket_Sight` des Sight-Specs (hinteres Visierende auf der Visierlinie) und entspricht Toolgens Regel für
  `Socket_Sight` („am hinteren Ende des Visiers“); `anchors.Socket_Sight` bleibt der Weapon-Spec-Anker (Oberkante der Visierschiene unter der Halterung =
  `socket_mount_m` − `riser_m`). `Socket_Eye`: Röhre = Mitte des Okularglases (Sight-Spec), sonst Vorschlag = hinterer Fensterrand, `eye_radius_m` = halbe
  kleinere Fensterseite. `line.above_body_top_m` = Visierlinie über der höchsten Stelle der Waffe ohne Visier und Schiene (negativ: ein Teil der Waffe
  ragt irgendwo längs höher; ob es die Linie verdeckt, sagt der Weapon-Spec `sight.sight_spec.line_clear_of_weapon`).
- **Stützhand.** Querschnitt des Stützhand-Teils in der Ebene quer zur Laufachse durch `Socket_SupportHand` (Schnittpunkte aller Flächenkanten); Toolgens
  `support_radius` wird in TG-A daraus abgeleitet (Reihenfolge dort beachten, hier benannte Felder).
- **Sehne.** Jedes Teil „Sehne“ als Strecke (die zwei entferntesten Ecken, Enden = Mitte der Ecken bis 4 mm davor); Spitzen = äußerste Enden entlang
  der Spannachse; Nockpunkt = Schnitt der Sehne mit der Ebene der Pfeilachse. Bei den Armbrüsten enden die Sehnenhälften 2 mm vor der Mitte: dort Mitte
  der inneren Enden (`nock_source` sagt es). Toolgen setzt `Socket_Nock`, Pfeil und Zugclip darauf; Sehnenlänge und Zugweg misst TG-A neu.
- **Budget.** Dreiecke je Waffe (Fächer, ohne Fasen) 352–6 956 (KJ17 … KH13), alle unter Toolgens Welt-Budget (`data/game_budget.json`; neue Typen ohne
  Werkzeug: größtes Waffen-Budget 8 000 als Annahme bis TG-B).

## Größen (claude-0.13)

| | Wert |
|---|---|
| Dateien | 159 (150 Waffen, 9 Visiere), 23–325 KB, zusammen 23 MB; zip (deflate) 3,1 MB |
| Teile | 7 423, davon 4 450 mit Primitiv-Hinweis |
| Hüllen | 5 139 geschlossen (Volumen > 0), 2 334 offen |
| Aufkleber | 6 880 (Weapon-Spec), 28 ragen im Blatt über ihr Teil |
