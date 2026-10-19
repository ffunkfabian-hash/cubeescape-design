# Sight-Spec der Visier-Serie (`cubeescape-design/sight-spec`, format_version 2)

Stand claude-0.6 (17.10.2026). Je Visier der Waffen 1–9 gibt es ein Blatt `VSnn.dc.html` und einen Steckbrief `VSnn.spec.json` in
`claude/output/sheets/`. Beide entstehen aus **einem** Modell je Visier (`claude/generator/vsmodels.py`), Ansichten und Daten sind
deshalb deckungsgleich. Die Serie ist das Visier-Zielbild (Entscheidung des Nutzers 17.10.2026, [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md)).
Seit claude-0.7 tragen die Waffenblätter 1–9 das Standardvisier ihres Typs aus dieser Serie (dasselbe Modell, Farben der Waffe); der
Weapon-Spec verweist mit `sight.sight_spec` auf `VSnn.spec.json` ([weapon-spec.md › Visier der Visier-Serie](weapon-spec.md#visier-der-visier-serie)).
Der Sight-Spec selbst ist unverändert (claude-0.6).

- Schema: [sight-spec.schema.json](sight-spec.schema.json). Test: `python3 claude/generator/test_sight_spec.py` (ohne numpy).
- Erzeugen: `python3 claude/generator/export_sight.py` (`--check` vergleicht nur). Blätter (Bildstufe, Mac, `heavy_lock`):
  `python3 claude/generator/build_vs.py`. Vorschauen: `preview.py VS01 …`. Viewer: Gruppe „VS · Visier-Serie“.
- Zielbild: Cube Escape `Docs/Images/EquipmentConcepts/weapon_sights_1-9.webp` und `sight_types_1-9.webp`, Tabelle `Docs/EQUIPMENT.md` ›
  Visiere je Waffe. Typen und Rahmen im Vokabular von claude-0.5.2 ([weapon-spec.md › Visier-Vokabular](weapon-spec.md#visier-vokabular)).

## Serie

| Blatt | Waffe | `type` | `kind` | Rahmen | Fenster (frei; Röhre: Objektiv) | Glas | Röhre | Modul | Fadenkreuze (erstes = Standard) |
|---|---|---|---|---|---|---|---|---|---|
| VS01 | Pistole | reflex | reflex | compact | rect 20 × 18 mm | Blau | – | – | Punkt, Kreis, Kreuz, T-Dot |
| VS02 | Sturmgewehr | holo | holo | open | rect 34 × 29 mm | Leicht getönt | – | – | Kreis, Kreis-Kreuz, Chevron, Punkt |
| VS03 | Impulsgewehr | precision | scope | standard | round Ø 34,4 mm | Blau | 128 mm | Entfernungsanzeige | Kreis, Punkt, Kreis-Kreuz, Zielfeld |
| VS04 | Schrotflinte | reflex | reflex | standard | round Ø 41 mm | Blau | – | – | Fein, Mil-Dot, Ballistik, Digital |
| VS05 | Scharfschützengewehr | sniper | scope | standard | round Ø 45,4 mm | Blau | 208 mm | Windkompensation | Fein, Mil-Dot, Ballistik, Digital |
| VS06 | Maschinenpistole | machine | reflex | closed | rect 35 × 30 mm | Blau | – | – | Punkt, Kreis, Chevron, Dynamisch |
| VS07 | Fusionsgewehr | energy | energy | closed | octagon 36,8 × 28,8 mm | Lila | – | – | Digital, Kreis, Energie, Fokus |
| VS08 | Spurgewehr | trace | holo | lightweight | rect 36,4 × 28,4 mm, Markierungsecken | Blau | keine (Nutzer) | Zielmarkierung | Tracking, Quad, Kreis, Box |
| VS09 | Raketenwerfer | rocket | holo | industrial | rect 64 × 32 mm | Blau | – | Entfernungsanzeige | Zielfeld, Kreis, Lock-On, Raster |

Die Maße stehen im Spec. Die Tabelle wiederholt nur den Stand claude-0.6.

## Rahmen, Achsen, Anker

- **Rahmen:** Blender, vorn −Y, oben +Z, links +X, Meter, wie der Weapon-Spec. Modell: x = vorn, y = unten, z = links, 1 Einheit = 1 mm;
  `p_m = 0,001 · M · (p_model − Socket_Mount)` mit `M = [[0,0,1],[−1,0,0],[0,−1,0]]`.
- **Ursprung `Socket_Mount`:** Unterkante der Halterung, mittig in Länge und Breite. Er liegt auf `Socket_Sight` des Waffen-Specs (Oberkante der Visierschiene).
  Die Klemmbacken reichen 3 mm darunter.
- **`Socket_Sight`:** hinterer Fensterrand auf der Visierlinie: Hinterkante des Rahmens, bei Röhren das Augenende. Im Waffen-Spec heißt
  `Socket_Sight` die Aufnahme auf der Schiene; dort setzt dieser Spec mit `Socket_Mount` an.
- **`Socket_Reticle`:** Glasmitte auf der Visierlinie, bei Röhren die Objektivlinse. Dort zeichnet Cube Escape das Fadenkreuz.
- **`Socket_Eye`** (nur Röhren, sonst `null`): Mitte des Okularglases; `tube.eye_radius_m` ist sein freier Radius. Cube Escape legt das
  Scope-Bild 2 mm davor (`FIRST_PERSON.md` › Scope).
- **Achsen der Anker:** Verbindlich sind `forward` [0, −1, 0] und `up` [0, 0, 1] im Weltrahmen. „Blick +Z, +Y oben“ wie Cube Escape
  `Socket_Sight` (`FIRST_PERSON_EQUIPMENT.md` › 4.2) ist als Blender-Drehung des Empties `rotation_euler_deg` [90, 0, 0] (XYZ,
  `rotation_space` Blender) angegeben. Sie gilt nur in Blender: Der glTF-Export dreht die Achsen, in Unity ist dieselbe Ausrichtung die
  Identität. Toolgen: Die Anker-Drehung ist kein Vertrag, die Position schon.

## Felder

| Feld | Inhalt |
|---|---|
| `sheet` | `id` VS01…VS09, `file`, `series` „VS“, `number` |
| `weapon` | `number` 1–9, `name_de`, `toolgen_id`; `weapon_spec`: `format`, `match` (`weapon.toolgen_id`), `sheets` (alle KXnn desselben Waffentyps) |
| `sight` | `type` (Vokabular 0.5.2), `kind` (Toolgen `hold.sight_kind`, aus `type` abgeleitet), `window_kind` (glass/lens), `frame`, `title_de`, `description_de`, `modular` |
| `window` | `shape` (rect/round/octagon), `width_m`, `height_m` (freie Öffnung), `corner_radius_m`, `center_m` (= Socket_Reticle), `rear_edge_y_m`, `front_edge_y_m`, `view_axis_m` [0,−1,0], `free`, `aperture` (Strahlenprüfung) |
| `frame` | `type`, `name_de`, `parts`, `outer_width_m`, `outer_height_m`, `depth_m` |
| `glass_tint` | RGBA: RGB linear (aus sRGB umgerechnet), A = Deckkraft im Spiel |
| `glass` | `id`, `name_de`, `srgb`, `alpha`, `parts`, `catalog` (alle acht Tönungen des Visier-Blatts mit `rgba_linear`) |
| `tube` | `length_m`, `lens_radius_m` (Objektiv frei), `eye_radius_m`, `bore_radius_m` (engste freie Stelle, Röhre innen), `eye_anchor` „Socket_Eye“; `null` ohne Röhre |
| `module` | `id` (night_vision, rangefinder, target_marker, wind_compensation), `name_de`, `side` (left/right/top), `parts`, `bounds_m`; `null` ohne Modul |
| `anchors` | `Socket_Mount`, `Socket_Sight`, `Socket_Reticle`, `Socket_Eye` (siehe oben), je `position_m`, Achsen, `source` |
| `sight_line` | `start_m`, `end_m`, `clear`, `blocked_by` (Teile außer Glas, die die Linie schneiden: leer), `glass_crossed` |
| `window_geometry` | Glasscheiben als Funktionsfläche für `spec_checks.window_problems` (wie im Weapon-Spec) |
| `parts[]` | `id` (gNN), `label`, `channel`, `material`, `toolgen_material`, `emissive`, `glass`, `color`, `area_m2`, `bounds_m` |
| `reticle_variants[]` | `id`, `name_de`, `default` (vier je Visier, Reihenfolge wie im Visier-Blatt); `reticle_color`, `reticle_note` |
| `variants[]` | vier Farbvarianten des Blatts: `channels` (MT_-Farben), `glass_tint` (Tönungs-Id) |
| `dimensions_m` | `length` (Y), `height` (Z), `width` (X), `bounds_m`, `line_height_m` (Visierlinie über `Socket_Mount`) |
| `source` | Zielbilder, Tabelle, Entscheidungen |

**Kanäle** (Auftrag Paket 2): Gehäuse `MT_Secondary`, Rahmen und Akzente `MT_Accent`, Glas `MT_Detail`, Leuchtrahmen und
Markierungsecken `MT_Energy`. Zusätzlich gibt es Abdeckungen `MT_Primary`, Halterung, Montageringe und Schrauben `MT_Metal` sowie die
Linsen der Tech-Module `MT_Emission`. Klarglas hat in Toolgen (`surface_recipes.json` › `materials`) noch kein Material: `toolgen_material:
null`, `material: glass`.

**Fadenkreuze** sind nur Bild. Cube Escape zeichnet sie zur Laufzeit an `Socket_Reticle`. Die Namen folgen der Spalte
„Fadenkreuz-Varianten“ in `Docs/EQUIPMENT.md`; der Test vergleicht sie, wenn Cube Escape lokal liegt.

## Freie Durchsicht

„Alle Fenster sind frei durchsichtig: keine Fläche in der Visierlinie.“ Geprüft wird an der Geometrie (alle Flächen, Newell-Normale):

1. **Visierlinie:** Keine Fläche außer Glas schneidet die Linie durch `Socket_Sight` und `Socket_Reticle` (`sight_line.blocked_by` leer).
2. **Ganze Öffnung:** Strahlen parallel zur Linie im Raster 0,5 mm in der freien Öffnung, 0,3 mm vom Rand (Röhre: Bohrung). Kein
   undurchsichtiges Teil darf einen Strahl schneiden (`window.aperture`). Diese Prüfung fand beim Bau Emitter, Knöpfe, Zellen und
   Markierungsecken, die ins Sichtfeld ragten.
3. **Funktionsfläche** (Cubegen `docs/DEVELOPER.md` 9.17, `spec_checks.window_problems`): Jede Glasscheibe ist entlang Y am dünnsten, mit
   Durchsicht −Y. Kein Querfenster.

Gegenbeweise im Test: ein Steg auf der Linie, ein Teil am Rand der Öffnung (das nur die Strahlenprüfung findet), ein 1,7 mm schmaler Steg
neben der Linie, eine 0,9 mm tiefe Nase am Rand (Raster plus Rand: ab 0,8 mm Tiefe sicher gefunden) und eine um 90° gedrehte Scheibe.

## Blatt (4800 × 4432 px, Stil der XL-Blätter)

Isometrie mit Beschriftungen · Seite (Visierlinie gestrichelt, Anker), Oben, Rück (Durchsicht −Y) im gleichen Maßstab · Daten aus dem
Spec · Durchsicht im Spiel (Rückansicht vor einer Würfelwelt, Glas durchscheinend, Standard-Fadenkreuz) · vier Fadenkreuz-Varianten ·
vier Farbvarianten · Bausteine: acht Glas-Tönungen, sechs Rahmen-Varianten in der Fensterform des Visiers, vier Tech-Module (verbautes
markiert). Das Glas zeichnet das Blatt deckender als im Spiel (`vsheet.DRAW_ALPHA`), damit man es sieht. Der Spec trägt die Deckkraft im
Spiel.
