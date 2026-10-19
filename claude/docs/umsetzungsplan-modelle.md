# Umsetzungsplan: Konzeptmodelle komplett nach Toolgen, danach Cube Escape

Stand 19.10.2026, Sitzung `DS Umsetzungsplan Modelle · Mac` (Branch `claude/models-toolgen-umsetzungsplan-62eedf`, ohne eigene Version).
Auftrag des Nutzers (19.10.2026): „Umsetzungsplan / Umsetzungsvorgabe der Models (KOMPLETT) in Toolgen (und später auch in CE)“ –
„Dabei sollen die bestehenden Waffen ausgetauscht werden“ – „Prüfe auch gegen, ob es mit cubeescape-reference zu Konflikten kommt oder ob
man etwas kombinieren kann“. Dieses Blatt ist die Vorgabe für die Sitzungen in cubeescape-design (DS), Toolgen (TG) und Cube Escape (CE);
hier wurde nichts gebaut. Entscheidungen des Nutzers dazu: [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md) (19.10.2026).

## Kurzfassung

- **Ziel:** Toolgen baut seine Waffenwerkzeuge aus den Konzeptmodellen dieses Repos. Die neun bestehenden Waffen werden **ersetzt**
  (gleiche Werkzeug-IDs, Anker und Clipnamen, also Vertrag 4 additiv), die 15 neuen Typen (Nr. 11–25) kommen als neue Werkzeuge dazu.
  Cube Escape übernimmt danach die ersetzten Modelle über den bestehenden Import und bindet die neuen Typen in Stufen an.
- **Weg:** kein Nachmodellieren. Das Design-Repo exportiert je Blatt einen **Geometrie-Spec** (`KXnn.geo.json`, Netz je Teil im
  Toolgen-Rahmen plus Griff-, Stützhand- und Visierdaten); Toolgen bekommt einen zweiten Bauweg (`concept_kit.py`), der diese Datei statt
  `weapon_designs.py` als Geometriequelle liest. Alles danach (Anker, Use-Clip, Ego-Hände, ADS, UV1, Karten, Roboter-Variante, Spiel-Export)
  bleibt Toolgens Pipeline.
- **Warum das trägt:** die Konzeptmodelle sind schon Polygonnetze (Prismen, Zylinder, Facetten), 8–105 Teile und 352–6 956 Dreiecke je Waffe
  (Median 2 636), also unter Toolgens LOD0-Budgets ohne Dezimierung; Toolgens Roboter-Verformung arbeitet auf Vertex-Ebene und UV1 entsteht per
  Smart-Project auf beliebigen Netzen – beides passt zu importierten Netzen ohne Umbau.
- **Visiere kommen mit:** die Waffenblätter 1–9 tragen seit claude-0.7 das Standardvisier der Serie VS01–VS09; der Modelltausch bringt Fenster,
  Rahmen und `Socket_Reticle` nach Toolgen. Die offene Visier-Aufgabe (Toolgen liest die Serie nicht, `hold.sight_kind` bei sechs von neun
  Waffen anders als das Zielbild) geht in diesem Plan auf und braucht keine eigene Sitzung.
- **Etappen:** DS-1 Geometrie-Spec → TG-A Bauweg und neun Waffen ersetzt → CE-A Übernahme → TG-B elf neue Fernwaffen → CE-B Anbindung →
  TG-C/CE-C Nahkampf, Armbrust, Bogen. Vor TG-A braucht es vier Entscheidungen des Nutzers (› 4).

## 1 Ausgangslage (geprüft 19.10.2026)

### 1.1 cubeescape-design (main 5a5615d, claude-0.12)

- 150 Waffenblätter (Varianten C, D, F, G, H, J × Typen 01–25) und die Visier-Serie VS01–VS09; alle vom Nutzer abgenommen (18./19.10.2026).
  Weapon-Spec und Sight-Spec `format_version` 2 ([weapon-spec.md](weapon-spec.md), [sight-spec.md](sight-spec.md)).
- **Modelle sind Netze:** `eng.Model` baut aus `prism` (Seitenprofil, quer extrudiert) und `cyl` (Zylinder längs); `tlib` (P/C/F/Y), `jlib`
  (Facetten), `smooth`/`ext` ergänzen Kegel, Querprismen und freie Flächen. Jedes Teil ist eine Liste ebener Polygone mit Normalen und trägt
  `label`, `channel`, `sight`, `emit` und Aufkleber (`dec`: Polygone 0,4 Modelleinheiten über der Fläche; 6 880 Aufkleber über alle 150 Modelle).
- Messung 19.10.2026 (`sheetmodels.load`, Dreiecke nach Fächer-Triangulierung, ohne Fasen):

  | Blatt | Teile | davon Visier | Dreiecke | | Blatt | Teile | Dreiecke |
  |---|---|---|---|---|---|---|---|
  | KG01 Pistole | 27 | 14 | 1 880 | | KG11 Scout-Gewehr | 72 | 4 648 |
  | KG02 Sturmgewehr | 32 | 16 | 2 068 | | KG12 Handfeuerwaffe | 31 | 1 888 |
  | KG05 Scharfschützengewehr | 77 | 56 | 5 304 | | KG13 Lineares Fusionsgewehr | – | 5 504 |
  | KG08 Spurgewehr | 43 | 27 | 2 120 | | KG16 Maschinengewehr | 43 | 2 544 |
  | KG09 Raketenwerfer | 50 | 24 | 2 644 | | KG17 Schwert | 8 | 640 |
  | KG10 Bogen | 31 | 2 | 1 164 | | KG19 Schwere Armbrust | 81 | 5 020 |

  Alle 150: 352–6 956 Dreiecke (größte KH13, KH03, KC13), 8–105 Teile. Sturmgewehr je Variante: C 2 704, D 1 476, F 1 928, G 2 068, H 2 324, J 1 088.
  Die Visierteile (VS-Serie, Zylinder n = 24) stellen bei Optik-Waffen über die Hälfte der Teile.
- **Der Spec liefert schon:** `units.model_unit_m` (aus der Toolgen-Länge), Achsen, Anker (`Socket_Hand`, `Socket_SupportHand`, `Socket_Muzzle`,
  `Socket_CenterOfMass`, `Socket_Sight`) in Toolgen-Metern, `parts[]` mit Kanal, Material, Katalog-Textur, `moving`, `toolgen_material`, Hüllquader,
  `moving_parts` mit Toolgens Knotennamen, `robot_fit`, `sight` samt `sight_spec` (Fenster, Glas, Röhre, `Socket_Reticle`), `texture_profile`
  (Katalog-IDs, Abnutzung, Toolgen-Decals), `skin`, `operation`.
- **Fehlt für den Bau:** die Geometrie selbst, die Griffneigung (`grip_tilt`), der Stützhand-Querschnitt (`support_radius`), die Abzugslage,
  die Aufkleber-Polygone in Metern, `Socket_Eye`, und je Waffe eine Zahl für die Visierlinie.

### 1.2 Toolgen (origin/main 66eb855, 0.17.1 „Retrace“)

- 13 Werkzeuge in `data/tools.json`; die neun Waffen entstehen aus dem Baukasten `scripts/tool_assets/weapon_kit.py` + `weapon_designs.py`
  (Boxen, Zylinder, Platten mit Fasen 0,4–6 mm): 6 000–15 000 Quelldreiecke → LOD0 3 500–7 000 (Welt), 11 000–15 000 (Ego), 12 000 (Roboter).
- **Vertrag 4 mit Cube Escape** (additiv, `minimum_consumer` je Vertrag): Anker (`Socket_Hand/SupportHand/Muzzle/CenterOfMass/Sight/Eye`),
  `hold` (Griffneigung, Griff- und Mündungsachse, `sight_kind`, `eye_distance_m`), Use-Clip 97 Bilder nur auf Kindknoten (`Anim_Slide`, `Anim_Bolt`,
  `Anim_Cell`, `Anim_FinL/R`, `Anim_Coil`, `Anim_Hatch`), Ego-Modell mit Händen (`first_person.py`: Stützhand an `Socket_SupportHand`, Finger um
  `support_radius`), Zustandsclips, ADS-Zielpose, UV1 + Karten W0/W1/Fields/Normal (Welt 512², Ego 2048², Roboter 512²), Relief und Decals nach
  `data/surface_recipes.json`/`data/decals.json`, Roboter-Variante als Verformung des Designs (`apply_robot_fit` schreibt Vertex-Koordinaten um),
  Golden als sha256 mit Ausweichwerten, Dreiecksbudgets `data/game_budget.json`, Kollisionsboxen, Viewer-Determinismus (Koplanar-Regel ≥ 0,5 mm).
- Visiere: `hold.sight_kind` heute pistol iron, assault_rifle reflex, pulse_rifle holo, shotgun iron, sniper_rifle scope, smg reflex, fusion_rifle
  energy, trace_rifle scope, rocket_launcher iron; nach Sight-Spec (`kind` aus `type`): reflex, holo, scope, reflex, scope, reflex, energy, holo, holo –
  sechs Abweichungen. Toolgen liest `VSnn.spec.json` nirgends.
- Zu lesen vor TG-A: `docs/TECHNIK.md` › Waffen 1–9, › Visier und Zielen, › Roboter-Variante, › Cache und Worker, › Erfahrungen; `docs/UNITY_EINBAU.md`.

### 1.3 Cube Escape (main a9a6e87e, 0.98 „Recast“; 0.99 „Truehold“ in Arbeit)

- `Weapons.Def`: neun Waffen (ID, Element, Cooldown, Hinweis, zweihändig, Stützgriff, Ladezeit); der Bogen ist nicht im Waffensatz. 13
  Ausrüstungs-Definitionen mit Kanälen und Masken; `ToolgenAssets.Refresh` importiert Welt-, Ego- und Roboter-Modell samt Karten als Prefabs.
  `heldScale` je Gerät, Roboter-Variante in der Hand, ADS mit Linse (Scharfschütze, Spurgewehr), Fadenkreuz je Klasse (CE zeichnet selbst).
- Nahkampf (Schwert, Glefe) gibt es im Spiel nicht; Granatwerfer, Maschinengewehr, Armbrust usw. sind wie die neun als „Werkzeuge ohne Munition
  und Regeln“ anbindbar.

### 1.4 cubeescape-reference (origin/main 91bec09, 0.11.20) – Konflikt oder Kombination

- **Kein Konflikt:** das Repo hält Messungen und Steckbriefe (Lage im Bild, Zeiten, Abläufe), keine Modelle, keine Verträge. Es schreibt nie in
  Toolgen, Design oder CE.
- **Kombination 1 – Steckbriefe als Vorgabe für Clips und Haltung:** `docs/destiny2.md` › 3 nennt je Typ Hüftlage, ADS, Nachladen, Arme und die
  Cube-Escape-Felder; für die neuen Typen (Scout, Handfeuerwaffe, lineare Fusion, Granatwerfer, MG, Glefe) liegen Messzeilen vor. TG-B liest sie
  für Use-Clip und `hold`, CE-B für Profilklassen. Belegt dort: **Schwert wechselt in die Schulteransicht, Glefe bleibt Ego** – das bestimmt den
  CE-C-Umfang (› 5.6).
- **Kombination 2 – Typenkatalog:** `docs/destiny2.md` › 4 (Bungie-Manifest, 17 Untertypen) und [waffentypen.md](waffentypen.md) decken sich bei
  Typen und Untertypen (Hitzewaffe, Mikro-Rakete, Spread Shot, Slug). **Unstimmigkeit:** die Reference führt **keine Armbrust** (weder Untertyp noch
  Rahmen), waffentypen.md führt die schwere Armbrust (KX19) als neuen Heavy-Typ nach Wikipedia/TheGamer. Vor TG-B klären, ob sie ein Untertyp des
  Bogens ist (dann Toolgen-ID als Bogen-Variante) oder ein eigener Typ (`heavy_crossbow`); Frage an die Reference-Sitzung, Entscheidung beim Nutzer.
- **Folgearbeit dort:** `docs/cube-escape.md` vermisst die Ego-Lage der heutigen Toolgen-Modelle in CE 0.94. Nach CE-A sind diese Zeilen veraltet;
  eine REF-Sitzung misst neu (gleiche Methode, eigene Aufnahmen). Namen aus dem Register beachten: „Armory“ (REF 0.7.0) und „Arsenal“ (DS 0.10)
  sind vergeben.

## 2 Grundsatz: Geometrie übernehmen, nicht nachbauen

| Weg | Was | Bewertung |
|---|---|---|
| **A Geometrie-Spec (empfohlen)** | Design exportiert je Blatt die Netze je Teil in Metern im Toolgen-Rahmen plus Bau-Metadaten; Toolgen baut daraus Blender-Objekte und hängt alles Weitere an | deckungsgleich mit dem Blatt (eine Wahrheit), 150 Modelle sofort verfügbar, Varianten später per Datenwert tauschbar; Toolgen bleibt Pipeline für Anker, Clips, Hände, Karten, Roboter, Export |
| B Nachbau im Baukasten | je Waffe `weapon_designs.py` von Hand nach dem Blatt | 25 × Handarbeit, nie deckungsgleich, Blätter und Modell laufen auseinander – verworfen |
| C Rezept statt Netz | Design übersetzt Prismen/Zylinder in Baukasten-Aufrufe (`slab`, `cyl`) | geht nur für zwei Primitive; Facetten (jlib), Querprismen und freie Flächen fallen heraus; bringt Fasen, aber ein zweites Bausystem – nur als Zusatz (Primitiv-Hinweis im Spec) sinnvoll |

Konsequenz für Toolgen: `weapon_designs.py` behält je Waffe die **Beschlagdaten** (Asset, Clipname, Element, Clip-Schlüssel, Schussbild, Kamera),
die Geometrie kommt aus `data/concepts/<id>.geo.json`. Die Repo-Regel „`output/` nur durch die Pipeline“ bleibt; die Geo-Dateien sind Eingabedaten
wie `tools.json`, mit Herkunft (Design-Release, sha256) in `data/concepts/source.json`.

## 3 Vertrag: Geometrie-Spec v1 (`cubeescape-design/geometry-spec`)

Neues additives Format neben dem Weapon-Spec, eine Datei je Blatt `claude/output/sheets/KXnn.geo.json` (Bögen und VS-Serie eingeschlossen).
Nicht committet (wie die Blätter), sondern Release-Asset `geo/` über `release_assets.py`; im Repo bleiben Hashes in `claude/tests/golden.json`
(neue Gruppe `geo`). Toolgen übernimmt nur die gewählten Blätter (25 Dateien, geschätzt 100–300 KB je Datei bei 0,1-mm-Rundung) nach
`data/concepts/`; kein Netzzugriff im Bau.

| Block | Inhalt |
|---|---|
| `format`, `format_version` | `cubeescape-design/geometry-spec`, `1`; Regel wie Weapon-Spec: nur ergänzen, Umbenennen/Bedeutungswechsel → 2 |
| `sheet`, `source` | Blatt-ID, Variante, Name; Weapon-Spec-Datei und sha256, Sight-Spec-Datei (VSnn), Design-Version |
| `units`, `axes`, `origin` | Meter; vorn −Y, oben +Z, links +X; Ursprung `Socket_Hand` (wie Weapon-Spec) |
| `parts[]` | `id` (= Weapon-Spec `parts[].id`), `name` (Blender-Name `SM_PG_<LabelAscii>_<id>`), `label`, `channel` (`MT_…`), `material`, `emissive`, `glass`, `sight` (Teil der Visier-Serie), `moving` (Art, Toolgen-Knoten), `texture` (Katalog-ID), `bounds_m`, `mesh` (`vertices` in m, `faces` als Indexlisten, `hard` je Fläche), optional `primitive` (`prism`: Profil y/z + x-Bereich; `cylinder`: Achse, Mitte, Radius, Länge, Segmente; `cone`) |
| `decals[]` | Aufkleber des Blatts: Teil, Ebene, Polygon in m, Farbe/Kanal, leuchtend – für Toolgen als Maskenregion, nicht als Geometrie |
| `grip` | `part`, `grip_axis_m` (Unterkante → Oberkante des Griffs), `grip_tilt_degrees` (gemessen), `trigger_m` (Abzugsmitte), `cross_section_m` |
| `support` | `part`, `radius_m` (halbe Höhe/Breite des Querschnitts an `Socket_SupportHand`) oder `null` (Pistolen: Becher-Griff) |
| `sight` | aus VSnn: `kind`, `type`, Fenster (Form, Maße), Glas, Röhre, `Socket_Mount`, `Socket_Sight` (hinterer Fensterrand), `Socket_Reticle` (Glasmitte), Vorschlag `Socket_Eye` (Röhre: Okularlinse, sonst = `Socket_Sight`), `eye_radius_m`, Visierlinie (`line_above_m` über der Gehäuseoberkante) |
| `anchors` | Kopie der Weapon-Spec-Anker in m plus `Socket_Sight`, `Socket_Eye`, `Socket_Reticle` |
| `string` | Bogen/Armbrust (seit Entscheidung 19.10.2026 schon in DS-1): Sehnen-Ansatzpunkte an beiden Wurfarmspitzen, Nockpunkt auf der Sehnenlinie in Ruhe, Pfeilauflage/Bolzenrinne, Pfeilachse; Toolgen setzt seine Sehne, den Pfeil und den Zugclip darauf |
| `melee` | nur Schwert/Glefe (Klingenachse, Griffzone) – erst DS-2 |
| `counts` | Teile, Dreiecke, Aufkleber |

Prüfung im Design-Repo: Schema, Teilezahl und Hüllquader je Teil gleich dem Weapon-Spec (±0,5 mm), Anker identisch, Normalen nach außen,
keine Fläche unter 0,5 mm Abstand zu einer koplanaren Nachbarfläche (sonst Befund), Dreieckszahl unter Toolgens Welt-Budget.

## 4 Entscheidungen des Nutzers vor TG-A

| Nr. | Frage | Empfehlung | Alternativen |
|---|---|---|---|
| 1 | **Welche Variante** wird das Toolgen-Modell je Waffentyp? – **entschieden 19.10.2026: G** ([ENTSCHEIDUNGEN](ENTSCHEIDUNGEN.md)) | **G** (Cube-Escape-Farbwelt, Heimat der neuen Typen, zuerst abgenommen); je Waffe tauschbar über die Datentabelle `design_pick` in Toolgen (`pistol: KG01` …) | je Waffe im Viewer wählen (Tabelle sofort anders belegen); alle Varianten als Toolgen-Varianten (150 Modelle, sechsfache Bake-Zeit – später, nicht jetzt); Codex-Blätter A/K sind ebenso wählbar, sobald Codex einen Geo-Spec liefert |
| 2 | **Bogen** tauschen? – **entschieden 19.10.2026: sofort in TG-A**, Toolgen-Sehne, Pfeil und Zugclip auf den Konzept-Wurfarmen; DS-1 liefert den `string`-Block ([ENTSCHEIDUNGEN](ENTSCHEIDUNGEN.md)) | ~~noch nicht:~~ Toolgens Bogen hat Sehne, Pfeil, Zugclip und eigene Anker (`Socket_Nock`, `Socket_ArrowTip`); die Blätter KX10 modellieren keine Sehne. Tausch in TG-C mit `string`-Block (DS-2) | sofort mit Toolgen-Sehne auf Konzept-Wurfarmen (Mischform, nicht deckungsgleich) |
| 3 | **Kanten:** hart wie das Blatt oder Fasen wie heute? | **hart** (Low-Poly-Look des Konzepts, Budgets ohne Dezimierung, Normalkarte trägt das Relief); Fase nur als globaler Datenwert `bevel_mm` für eine Sichtprobe | Fasen 0,5–2 mm auf allen Teilen (Look der vier Werkzeuge, ~1,5–3× Dreiecke) |
| 4 | **Aufkleber des Blatts** (Glyphen, Streifen, Embleme) | **als Maskenregionen** über Toolgens Decal-System (W0/W1, `data/decals.json`), nicht als Geometrie (0,4 mm Abstand verletzt die Koplanar-Regel und flackert) – Umfang TG-A Stufe B | zuerst ohne Aufkleber (nur Texturprofil), Aufkleber später |
| 5 | Roboter-Variante der neuen Typen: **Ziel-Längen** | CE legt sie nach der 0.82-Regel fest: pistolenartig ≥ 0,24 m, Gewehre 0,65–0,69 m, MG/lineare Fusion/Armbrust ≤ 0,75 m; Schwert und Glefe eigene Regel (Nahkampf) | – |
| 6 | **Elemente** der neuen Typen (`element` ist im Spec `null`) | Vorschlag nach verwandtem Typ: Scout arc, Handfeuerwaffe solar, lineare Fusion void, Granatwerfer (beide) solar, MG arc, Schwert energy, Glefe void, Armbrust energy, Raketenpistole solar, Raketen-Impuls void, Slug solar, Hitze-Blaster solar, Mikroraketen solar, Streuschuss solar | – (Entscheidung des Nutzers wie am 17.10.2026 für 1–9) |
| 7 | **CE-Umfang** der neuen Typen | Fernwaffen als `Weapons.Def` wie die neun (CE-B); Nahkampf als eigene Entscheidung (CE-C) | nur Modelle und Spender ohne Regeln |

## 5 Etappen

Je Etappe: Ziel, Zuständigkeit (eine Sitzung, eine Schreiberin je Datei), Modell nach der Modellregel mit Grund, Codex-Anteil, Prüfweg, Abnahme,
Vertrag, Zeitschätzung. **Zeitschätzungen** sind Schätzungen vom 19.10.2026 aus den Sitzungszahlen vergleichbarer Versionen (Toolgen 0.13–0.17: je
ein bis zwei Sitzungen; claude-0.10/0.11: je eine bis zwei Sitzungen), keine Messung; Rechenzeit schwerer Läufe liest jede Sitzung aus dem Zeitband
in `logs/toolgen_report.json` des letzten `standard`-Laufs. Versionsnummern und Namen vergibt jede Sitzung selbst und reserviert sie im
Versionsregister (cubeescape-rules); die Namen unten sind Vorschläge und im Register noch frei (Stand 19.10.2026, geprüft gegen CHANGELOGs).

### 5.1 DS-1 „Blueprint“ – Geometrie-Spec (cubeescape-design)

- **Ziel:** `claude/generator/export_geo.py` schreibt `KXnn.geo.json` für alle 159 Blätter (Bögen mit `string`-Block); Doku `claude/docs/geometry-spec.md` + Schema;
  Test `claude/generator/test_geo_spec.py` (› 3 Prüfung); Golden-Gruppe `geo`; `release_assets.py` liefert `geo/` mit aus; `vsmount` liefert
  `Socket_Eye`/`Socket_Reticle` in Waffenlage; Messung von `grip`/`support`; Aufkleber-Export. Weapon-Spec unverändert (nur Verweis
  `geometry_spec` additiv).
- **Pilot am Bild:** KG02 in Blender importieren (Skript im Repo, Mac, `heavy_lock`), Seite/Iso neben `claude/output/previews/KG02.webp` als
  Kontaktbogen – Freigabe des Nutzers, dann alle Blätter.
- **Modell:** Opus `high` – Entwurf ohne Vorlage im Repo und Vertrag zwischen Repos. **Codex:** `gpt-6-luna` (`medium`, `-s read-only`) prüft den
  Diff vor Merge; ab 300 Zeilen einmal `gpt-6.1-sol` (`high`) nach der Misstrauensregel.
- **Prüfweg:** `.ce-repo.json` › quick (plus neuer Test), `test_golden`; Bildstufe nur für den Pilot. Cloud möglich bis auf den Blender-Pilot.
- **Vertrag:** geometry-spec 1; Abnehmer Toolgen ≥ TG-A.
- **Zeit:** eine Sitzung, 3–6 h; Wartezeit auf die Pilot-Freigabe.

### 5.2 TG-A „Reforge“ – Bauweg und neun Waffen ersetzt (Toolgen)

- **Ziel (neun Waffen und der Bogen):** `scripts/tool_assets/concept_kit.py` lädt einen Geo-Spec, baut je Teil ein Mesh-Objekt (Name, `MT_`-Material über `game_palette`,
  Glas als Visierglas, leuchtende Teile mit dem Glühmaterial des Elements), hängt bewegliche Teile unter die `Anim_`-Knoten aus `moving_parts`,
  setzt die Anker aus dem Spec und übergibt an den bestehenden Weg (`weapon_kit.world` → FPS-Kopie → Clips → Export). `weapon_designs.py`:
  je Waffe `concept: 'KG02'` (Tabelle `design_pick`), Use-Clip-Wege aus den Teilmaßen neu, `grip_tilt_degrees` aus dem Spec, `sight` aus dem Spec
  (ersetzt `sight.py` für Konzeptwaffen), `hold.sight_kind` nach VS-`kind` (sechs Werte ändern sich). `data/viewmodels.json`: `support_radius`,
  `hand_rotation_degrees`, Kopfprüfungsgrenzen neu messen; `data/ego_clips.json`: AimIdle-Visierlinie je Waffe neu. `ROBOT` je Gewehr neu
  (Stützpunkte, Querschnitt) auf der neuen Geometrie. Katalog-Textur-IDs → `surface_recipes.json`-Muster (Abbildungstabelle). Golden der
  Oberflächenkarten als `stale` markieren, bis der Mac bakt; `version.py` vor dem ersten großen Lauf heben (Cache). **Bogen (KG10):** Wurfarme, Mittelstück und Pin-Visier aus dem Geo-Spec; Toolgens Sehne, Pfeil, Zugclip, `Socket_Nock`/`Socket_ArrowTip` und die Zughand-Pose (`bow_geometry.py`, `animate_standard_bow.py`) werden auf die `string`-Punkte des Spec gesetzt; Sehnenlänge und Zugweg neu gemessen.
- **Stufe B (gleiche Version oder Patch):** Aufkleber als Decal-Regionen aus `decals[]`; Texturprofil-Abnutzung je Waffe aus `texture_profile`.
- **Pilot:** Sturmgewehr (KG02) zuerst – Viewer-Bilder Welt/Ego/Roboter, `scripts/ego_video.py` (Use-Clip als MP4), `robot_preview.py`,
  `surface_preview.py` – Freigabe des Nutzers, dann die übrigen acht.
- **Modell:** Opus `high` – Ergebnis wird am Bild beurteilt (Haltung, Ego, ADS), Eingriff in Kernsysteme (Ego-Hände, Roboter-Variante).
  **Codex:** nach dem Pilot portiert `gpt-6.1-sol` (`high`) die Beschlagdaten der übrigen acht Waffen (Clip-Schlüssel, `ROBOT`, `viewmodels`,
  `ego_clips`) in einem eigenen Worktree (Claude prüft Diff und Bild); Prüfung vor Merge `sol` (großer Diff, Vertragsänderung).
- **Prüfweg:** `./check`, `--tier quick` (Cloud erlaubt), `--tier standard` auf dem Mac unter `heavy_lock` (Bake, Reimport, Bilder),
  `verify_output.py`, `viewer/test_determinism.py --runs 16` je Modell, `scripts/compare_models.py` (erwartet: die neun Waffen und der Bogen anders, die drei
  Werkzeuge bytegleich), Viewer-Build und -Tests.
- **Vertrag:** 4 additiv (Namen, Anker, Knoten bleiben); `hold.sight_kind`, `grip_tilt_degrees`, Maße und Karten ändern ihre Werte →
  `minimum_consumer` = die CE-Version von CE-A; ältere Fassung `v0.17.1`.
- **Zeit:** zwei bis drei Sitzungen (Pilot, acht Waffen, Stufe B), je Mac-`standard`-Lauf nach Zeitband; Wartezeit auf die Pilot-Freigabe.

### 5.3 CE-A „Refit“ – Übernahme der neun Modelle (Cube Escape)

- **Ziel:** Import des TG-A-Pakets (`ToolgenAssets.Refresh`), Prefabs, Maskenmaterialien, Roboter-Variante in der Hand; Tests nachziehen:
  `ToolgenModelTests` (Anker), `HeldWeaponReelTests` (Passung), `FrameBudgetEnvelopeTests`, Kanaltests gegen `channel_map`; ADS je Waffe prüfen
  (Bildmitte frei, 25-%-Grenze); Fadenkreuz je `sight_kind` (sechs Waffen wechseln die Art; **Impulsgewehr wird Röhren-Optik VS03** → Linse
  wie bei Scharfschütze/Spurgewehr, Entscheidung 6 vom 17.10.2026 erweitern); `heldScale` bleibt 1,0 (Roboter-Variante) bzw. Pistole prüfen.
- **Reihenfolge:** erst nach 0.99 „Truehold“ und laufenden Toolgen-Patches, damit sich nichts überlagert (Dateien `ToolgenAssets`,
  `HeldToolModels`, `ToolViewModels`, `CrosshairUI`).
- **Modell:** Opus `high` – Spielgefühl am Bild, Kernsysteme (Ego, ToolBelt-nahe Klassen). **Codex:** Prüfung vor Merge `luna`; Unity-Regression
  nur Mac.
- **Prüfweg:** Unity-Regression (EditMode/PlayMode), Iso- und Ego-Screenshots je Waffe, MP4 Feuern/Nachladen (CE-Aufnahmeweg), Roboterhand-Passung.
- **Vertrag:** liest Toolgen ≥ TG-A; Spielstände unverändert (IDs gleich).
- **Zeit:** ein bis zwei Sitzungen; Unity-Läufe unter `heavy_lock`.

### 5.4 TG-B „Longlist“ – elf neue Fernwaffen (Toolgen)

- **Ziel:** neue Werkzeuge mit dauerhaften IDs (Vorschlag = `design_type`, Untertypen als eigene Werkzeuge, weil andere Geometrie):
  `scout_rifle` (KG11; `renamed_from` am Spurgewehr entfällt), `hand_cannon` (KG12), `linear_fusion_rifle` (KG13), `grenade_launcher_special` (KG14),
  `grenade_launcher_heavy` (KG15), `machine_gun` (KG16), `rocket_sidearm` (KG20), `rocket_pulse_rifle` (KG21), `slug_shotgun` (KG22),
  `heat_pulse_rifle` (KG23), `micro_missile_launcher` (KG24), `spread_hand_cannon` (KG25) – zwölf; Armbrust (KG19) nach Klärung › 1.4.
  Je Werkzeug: Eintrag `tools.json`, `DESIGNS`, `viewmodels.json`, `ego_clips.json`, `game_budget.json`, Ordner mit Startern; **Use-Clip je
  Mechanik** (Trommel, Hahn, Beschleunigerschienen, Kipplauf, Granattrommel, Zuführdeckel, Entlüftungsklappen, Kipprahmen – neue `Anim_`-Knoten aus
  `moving_parts`, `proposed` wird verbindlich); Haltung nach den Steckbriefen der Reference (Handfeuerwaffe Becher-Griff, MG und Granatwerfer
  Unterhand); Roboter-Variante mit Ziel-Längen aus › 4 Nr. 5; Elemente aus › 4 Nr. 6.
- **Modell:** Opus `high` – Clips und Haltung werden am Bild beurteilt. **Codex:** `sol` baut nach zwei Pilot-Werkzeugen (Handfeuerwaffe,
  Maschinengewehr) die übrigen Einträge und Clips paketweise in eigenen Worktrees; Claude prüft je Paket am Bild; Prüfung vor Merge `sol`.
- **Prüfweg:** wie TG-A; zusätzlich `tests/test_weapons.py` für jede neue ID; Golden neu (nur neue Karten).
- **Vertrag:** 4 additiv (neue Werkzeuge); `minimum_consumer` = CE-B; Abnehmer ohne neue Typen filtern auf bekannte IDs.
- **Zeit:** drei bis fünf Sitzungen (zwölf Werkzeuge, je Paket ein `standard`-Lauf).

### 5.5 CE-B „Enlist“ – neue Fernwaffen im Spiel (Cube Escape)

- **Ziel:** `Weapons.Def` je neue ID (Element, Cooldown, Hinweis, zweihändig, Stützgriff; Ladezeit bei linearer Fusion), Ausrüstungs-Definitionen
  (Kanäle, `heldScale`/Roboter-Variante), Profilklassen für ADS (`eye_distance` je Klasse, Steckbriefe der Reference), Fadenkreuz je `sight_kind`,
  Spender/HUD-Einträge nach dem Muster der neun; keine Munition, keine Regeln darüber hinaus.
- **Modell:** Sonnet `medium` für die Datenpflege nach Muster (Def-Zeilen, Definitionen), Opus `high` für Haltung/ADS und Abnahme am Bild.
  **Codex:** `luna` schreibt Def-Zeilen und Definitionen nach Muster; Prüfung vor Merge `luna`.
- **Prüfweg:** Unity-Regression, `EquipmentCatalogTests` (Längenregel), Screenshots Iso/Ego je Waffe, ADS je Klasse.
- **Zeit:** zwei bis drei Sitzungen.

### 5.6 TG-C / CE-C „Edgework“ – Nahkampf, Armbrust, Bogen

- **Schwert (KX17), Glefe (KX18):** kein Visier, Griff ohne Abzug (Schwert), Stangenhaltung (Glefe). Toolgen braucht eine neue Haltungsart
  `melee` (Ego-Profil, Hände am Griff bzw. Schaft, Use-Clip = Hieb/Stoß) – Entwurf ohne Vorlage, Opus `high`. Cube Escape hat kein Nahkampfsystem;
  die Reference belegt: Schwert in Destiny in der Schulteransicht, Glefe im Ego. **Entscheidung des Nutzers nötig**, ob CE Nahkampf baut (Trefferlogik,
  Kamera) oder Schwert/Glefe zunächst nur als Modelle/Spender erscheinen.
- **Armbrust (KX19):** `string`-Block wie beim Bogen (DS-1); Toolgen überträgt Sehne, Bolzen, Spannhebel-Clip nach dem Bogen-Muster aus TG-A. Erst nach Klärung › 1.4. Der Bogen selbst ist seit der Entscheidung vom 19.10.2026 Teil von TG-A.
- **Zeit:** je zwei bis drei Sitzungen; nach TG-B/CE-B.

### 5.7 DS-2 (parallel zu TG-A, optional)

`melee`-Block im Geo-Spec; Geo-Spec der Codex-Blätter als Änderungswunsch an Codex (eigener Exporter unter `codex/`, keine Dateien aus
`claude/`); Verweis `geometry_spec` in den Weapon-Specs. Sonnet `medium` (Muster liegt nach DS-1 vor).

## 6 Reihenfolge, Parallelität, Zuständigkeit

```
DS-1 Blueprint ──► TG-A Reforge (Pilot KG02 → 8 Waffen → Stufe B) ──► CE-A Refit (nach Truehold)
                   │                                                  │
DS-2 (optional) ───┘                 TG-B Longlist (nach TG-A) ──────► CE-B Enlist ──► TG-C/CE-C Edgework
                                                                       REF: Ego-Lage neu messen (nach CE-A)
```

- Schwere Läufe (`standard`/`full`, Bake, Unity) nacheinander über `heavy_lock`; Cloud-Sitzungen nur `./check`, `--tier quick`, Spec-Tests;
  jede Bildstufe auf dem Mac. Eine Schreiberin je System: DS-1 besitzt `claude/generator/export_geo*`, `test_geo_spec.py`, `geometry-spec.*`;
  TG-A besitzt `concept_kit.py`, `weapon_designs.py`, `data/*.json`; Codex-Pakete in eigenen Worktrees, nie dort, wo Claude schreibt.
- **Codex-Stand** 19.10.2026: Wochenfenster 49 % übrig → Codex wie geplant (Prüfungen `luna`, große Umsetzungen `sol`); vor jedem Paket neu lesen
  (`python3 ~/.claude/templates/codex_quota.py`).
- Register: DS-1 reserviert die nächste DS-Nummer, TG-A `TG 0.18`, CE-A die Nummer nach Truehold; gleiche Themen (Visiere, Roboter-Variante)
  vorher im Register prüfen.

## 7 Abnahme und Belege

| Etappe | Beleg |
|---|---|
| DS-1 | Kontaktbogen: KG02 aus dem Geo-Spec in Blender (Seite, Iso) neben `claude/output/previews/KG02.webp`; Testprotokoll (159 Specs, 0 Befunde) |
| TG-A | je Waffe und Bogen: Viewer Welt/Ego/Roboter neben der Blattvorschau als Kontaktbogen (`magick montage`), Use-/Zugclip-MP4 (`ego_video.py`), `robot_preview.png`, `surface_preview.png`; `verify_output` grün; Determinismus 16 Läufe; `compare_models`: die drei Werkzeuge bytegleich |
| CE-A | Iso- und Ego-Screenshots je Waffe, ADS je Waffe (Bildmitte frei, Linse beim Impulsgewehr), Roboterhand-Passung, Unity-Regression grün |
| TG-B/CE-B | wie TG-A/CE-A je neues Werkzeug; Haltung gegen die Steckbriefe der Reference |

## 8 Risiken und Fallen

- **Koplanare Flächen:** Aufkleber des Blatts liegen 0,4 Modelleinheiten (≈ 0,4 mm) über der Fläche – unter Toolgens 0,5-mm-Regel. Deshalb Aufkleber
  als Maske (› 4 Nr. 4); der Geo-Test meldet jede Fläche unter 0,5 mm Abstand.
- **Bewegliche Teile ohne eigenes Teil:** `moving_parts.items[].parts` ist bei einigen Blättern `null` (Verschluss nicht modelliert). Dann bewegt der
  Use-Clip nichts Sichtbares; TG-A wählt ein ähnliches Teil (`similar`) oder DS ergänzt das Teil im Modell (Neubau des Blatts, erneute Abnahme).
- **Griffneigung und Stützhand ändern sich** je Blatt (andere Handschutz-Höhe, Griffwinkel): `hold.grip_tilt_degrees` und `support_radius` sind
  Vertragswerte; CE-Handpose und Roboter-Passung müssen neu gemessen werden (`HeldWeaponReelTests`).
- **Roboter-Variante neu abstimmen:** `ROBOT`-Stützpunkte sind auf die alte Geometrie geschnitten; Knickstellen dürfen nicht unter feinen
  Dekoren liegen (Erfahrung 17.10.2026); Determinismus 16 Läufe je Modell.
- **Visier als Röhre beim Impulsgewehr** (VS03, 128 mm): neue Linse in CE, `Socket_Eye` im Okular; Kopfprüfung (`head.limits`) bei schlanken Läufen.
- **Glas:** Toolgens Visiere haben bisher keine durchsichtigen Scheiben (Linse als Glühmaterial/Detail); die VS-Fenster sind frei und getönt →
  Materialentscheidung in TG-A (Palette hat kein Glas; Vorschlag: Fenster offen lassen, Rahmen als Geometrie, Tönung über CE-Overlay).
- **Dreiecke im Ego-Modell:** Hände und Unterarme kommen dazu; die Konzeptnetze sind klein, Budget kein Problem; harte Kanten erzeugen im
  Normal-Bake keine Fasenkanten (Look wie Blatt).
- **Cache und Golden:** Version vor dem ersten großen Lauf heben; Golden-Hashes nicht raten (`stale`), Ausweichwerte nur belegt eintragen.
- **Namen und Register:** „Armory“/„Arsenal“ vergeben; jede Sitzung prüft Register und Briefkasten vor Arbeitsbeginn.
- **Codex-Blätter (A/K):** nicht Teil dieses Plans; wählbar über `design_pick`, sobald Codex einen Geo-Spec nach demselben Format liefert.

## 9 Offen

- Entscheidungen › 4 Nr. 3–4 vor TG-A (Nr. 1 entschieden: G; Nr. 2: Bogen sofort), Nr. 5–7 vor TG-B/CE-B; Armbrust-Einordnung (› 1.4) vor TG-B.
- Vier Fadenkreuz-Varianten je Visier (Sight-Spec) sind in CE nicht als Vorgabe verankert – gehört zu CE-A (Daten je `sight_kind`/Visier).
- Dieses Blatt ändert keine Specs; der Verweis `geometry_spec` kommt mit DS-1.
