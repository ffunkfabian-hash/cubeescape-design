# Auftragsentwurf an Codex: Angleichung an den Claude-Stand (Stil, Spec, Texturen)

Entwurf von Claude, 17.10.2026, auf Wunsch des Nutzers („Auftrag an Codex mit Stilvertrag (Messwerte aus deinem Renderer) und
Weapon-Spec-Export“). Am 18.10.2026 vom Nutzer an Codex gegeben (Teil A und B; Teil C erst, wenn der Katalog auf `main` liegt). Vorlage:
`~/.claude/templates/auftrag.md`. Teil B ersetzt den älteren Entwurf [auftrag-codex-spec.md](auftrag-codex-spec.md).
Grundlage: `main` 3e0751e, Rebase auf d8a4890 (Claude 0.6, Codex 0.1.1 Parallax und 0.2.1 Flux Bloom). Regeln: [AGENTS.md](../../AGENTS.md) (gleiche
Regeln wie Claude seit 17.10.2026), [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md).

## Befund

Seit codex-0.1.1/0.2.1 entspricht der Blattaufbau dem Claude-Stand (4800 × 4432, Isometrie, sechs Orthos, Detail, Optik, Material,
vier Farbvarianten, fünf Skins, Prompts). Drei Unterschiede bleiben. Gemessen wurde am 17.10.2026 mit
`claude/generator/style_metrics.py` im Feld der Hauptansicht, angegeben ist der Median über je zehn Blätter (Claude: KF01–KF10 aus
v0.3, Codex: KA und KK aus `~/Library/Caches/CubeEscapeDesign/concept-sheets/*-upgrade-full/`):

| | Breite | Höhe | Rand dunkel (Kontur) | Innenlinien | Sättigung |
|---|---|---|---|---|---|
| Claude KF01–10 | 78 % | 91 % | **58 %** | **8,9 %** | 52 |
| Codex KA01–10 | 70 % | 89 % | **1 %** | **0,1 %** | 32 |
| Codex KK01–10 | 70 % | 89 % | **1 %** | **0,1 %** | 67 |

1. **Keine Konturen.** Die Codex-Modelle haben weder Silhouette noch Kantenlinien. Das ist der sichtbarste Unterschied: Die Waffen
   wirken flach und grau und lösen sich in der verkleinerten Ansicht schlechter vom Hintergrund.
2. **Licht und Tonstufen.** Codex legt das Licht im Modellraum fest und dunkelt nur ab (RGB × 0,58/0,73/0,88/1,0). Bei Claude ist das
   Licht an die Kamera gebunden, und die hellste Stufe hellt auf (siehe Stilvertrag). Bei Codex fehlt dadurch die helle Oberseite, und
   die Orthos sind je nach Ansicht unterschiedlich hell.
3. **Orthos langer Waffen.** Codex teilt die Orthos immer 2 × 3 auf. Bei Scharfschützengewehr, Spurgewehr und Raketenwerfer werden die
   Ansichten dadurch winzig (KK05: Seitenansicht 36 % der Feldhöhe, Vorne/Hinten nur wenige Pixel). Claude stellt lange Waffen in
   volle Zeilen.
4. **Spec.** Codex gibt `CodexDesignReference` aus, nicht `cubeescape-design/weapon-spec`. Toolgen kann die Codex-Blätter deshalb nicht
   lesen.

Ursache: Die Pipelines sind nach Repo-Regel getrennt. Codex hat das Bild an veröffentlichten v0.3-Blättern nachgebaut, die Zeichenregeln
selbst standen aber nirgends als Zahlen. Dieser Auftrag liefert sie nach.

## Auftrag

- **Teil A – Stilvertrag:** Den gemeinsamen Codex-Renderer und das Blattlayout (`codex/fluxbloom/raster.py`, `sheet.py`, wirkt auch
  auf Parallax) auf die Werte unten bringen und alle 20 Blätter neu bauen.
- **Teil B – Weapon-Spec:** Je Blatt eine `KAnn.spec.json` bzw. `KKnn.spec.json` im Format
  [weapon-spec.md](weapon-spec.md) (`format_version` 1) samt Schema ausgeben.
- **Teil C – Texturen:** Materialmuster, Oberflächen und Skins aus dem gemeinsamen Katalog `docs/textures/` lesen statt eigener Werte.
  Den Katalog legt Claude vorher an; der Aufbau ist unten vorgeschlagen. Codex beginnt Teil C erst, wenn der Katalog auf `main` liegt.

Eigen bleiben bei Codex: Modelle, Silhouetten, Paletten, Skin-Entwürfe und Namen. Der Vertrag legt fest, *wie* gezeichnet wird,
nicht *was*.

## Stilvertrag (Teil A)

Die Werte stammen aus `claude/generator/` (Stand ebb8f1d, claude-0.7). Quellen sind als Funktion und Abschnitt angegeben, weil sich
Zeilennummern mit jeder Version verschieben. Codex baut die Logik nach der Beschreibung nach und kopiert keine Dateien
(Repo-Regel). Pixelangaben beziehen sich auf das ausgegebene Blatt (4800 px breit).

| Merkmal | Claude-Wert | Quelle |
|---|---|---|
| Kantenglättung | 2× Supersampling, verkleinert mit Lanczos | `raster.py` `SS`, Ende von `rasterview` |
| Konturfarbe | `#0A0A0D` | `eng.py` `OL` |
| Konturbreite `ow` | Hauptansicht 4,6 · Orthos und Material 3,0 · Optik und Skin-Karten 2,6 · Farbvarianten 2,4 | `xl.py` `ow=` in `sheet`, `obox`, `_sight_view`, `skin_row` |
| Konturarten | Innenkanten (Grenze zwischen Flächen-IDs) ≈ `ow`·0,8 px; Silhouette ≈ `ow`·1,25 px, halb außen, halb innen; Flächen einer glatten Gruppe (Zylindermantel, gerundetes Profil) ohne Linie dazwischen | `raster.rasterview` › „Konturen“ |
| Licht | **kameragebunden**: Richtung (−0,35, −0,8, 0,5), normiert, im Bildraum, für jede Ansicht gleich (oben links vorn) | `eng.py` `LV`, `shadef` |
| Tonstufen | Skalarprodukt d: > 0,75 → ×1,28 · > 0,45 → ×1,08 · > 0,1 → ×0,88 · sonst ×0,62. Wirkt auf die HLS-Helligkeit: f < 1 ergibt l·f, f > 1 ergibt l + (1−l)·(f−1)·0,9. Farbton und Sättigung bleiben | `eng.py` `lum`, `shadef` |
| Leuchtteile | ohne Schattierung; Schein dahinter: Gauß σ = 4 px (bei 2× SS: 8), Deckkraft höchstens 0,3 | `raster.rasterview` › „Glow“ |
| Bodenschatten | Ellipse unter dem Modell: rx = 0,45 · Modellbreite, ry = max(8, 14 · Maßstab), Schwarz mit Deckkraft 0,32, 14 px unter der Unterkante. In Hauptansicht, Orthos, Material, Farbvarianten und Skins; nicht in Detail und Optik | `raster.rasterview` › `sh_y`, `shd` |
| Rundung | Profilecken mit r = 8 Modelleinheiten in 4 Segmenten (`roundpoly`); bei facettierten Serien Fase b = 4 | `eng.py`, `jlib.py` |
| Hauptansicht | Feld 2700 × 1800; Maßstab = min((2700−200)/Breite, (1800−420)/Höhe, 6), höchstens 6 | `xl.sheet` › `MW,MH`, `sm` |
| Orthos | gemeinsamer Maßstab und Bezugspunkt (Mitte des Hüllquaders). Ist die halbe Breite der linken Seitenansicht größer als die doppelte halbe Höhe (lange Waffe), stehen Links, Rechts, Oben und Unten in **vollen Zeilen** und Vorne/Hinten nebeneinander; sonst Raster 2 × 3. Bezugslinien `#4A6080` 1,4 px gestrichelt 8/8, Mittellinie `#2E405A` 1,2 px 2/8 | `xl.sheet` › `obox` und folgende Aufteilung |
| Glas (seit claude-0.7) | Glasscheiben werden **nach** Kontur und Schattierung als getönte, durchscheinende Fläche aufgelegt, nur wo sie vor undurchsichtigen Teilen liegen. Deckkraft je Tönung (Standard 0,34) plus weicher Glanzverlauf von oben links bis +0,07, **keine Schraffur** (Wunsch des Nutzers, 18.10.2026); helle Kante 1 px aus 35 % Tönung und 65 % Weiß, Deckkraft ≥ 235/255 | `raster._glass_pass`, `xl._sight_view` |
| Feld „Visier · separat“ (seit claude-0.7) | Isometrie und Seite nebeneinander, Konturbreite 2,6, ohne Bodenschatten. Ein Visier der Visier-Serie füllt das Feld (keine Maßstabsgrenze), sonst höchstens Maßstab 6. Beim Bogen Rückansicht statt Seite (Leuchtpunkt, wie ihn der Schütze sieht) | `xl.sight_panel` |
| Etiketten | Pille 46 px hoch, rx 23, Breite = 13,5 px · Zeichen + 40, Fläche `#0E1622`, Rand 1,8 px in Variantenfarbe, Chakra Petch 19 px Gewicht 600. Hinweislinie mit Knick bei 35 %, `#E6ECF2` 1,8 px, Deckkraft 0,9, Ankerpunkt r 6 mit Rand `#0A0A0D` 2 px | `xl.py` `_callouts` |
| Felder | rx 18, Rand 1 px `#22314A`, Fläche `#111A27`, Raster 40 px `#1A2636`; Feldtitel Chakra Petch 19 px, Sperrung 3 px, `#8FA0B3` | `xl.py` `panel`, `DEFS` |
| Blatt | 4800 × 4432, Rand 80, Abstand 32, Grund `#0E1622`; Kopf: Nummer Chakra Petch 140 px/700 in Variantenfarbe, Titel 74 px/700 mit Sperrung 6 px, Palette als Pille rechts | `xl.sheet` › HTML-Kopf |
| Auslieferung | WebP-Qualität 60; Schriften als Dateien mit OFL-Lizenz | `raster.py` `WEBP_QUALITY`, ENTSCHEIDUNGEN |

**Abnahmemaße** (Claude misst mit `claude/generator/style_metrics.py`, Median über zehn Blätter je Serie, Feld der Hauptansicht;
Feld in Pixeln des 4800er-Blatts: Codex-Layout `150 560 2910 2120`, Claude `100 330 2760 2080`):
Rand dunkel ≥ 40 %, Innenlinien ≥ 5 %, Breite 72–85 %. Bei langen Waffen müssen die Seitenansichten mindestens 70 % der Feldbreite
füllen. Die Sättigung bleibt Sache der Palette und ist kein Abnahmemaß.

## Weapon-Spec (Teil B)

Inhalt wie [auftrag-codex-spec.md](auftrag-codex-spec.md) › Inhalt je Datei, ergänzt um den Stand 0.5.2:

- Dateien `KA01.spec.json` … `KK10.spec.json` neben den Blättern, `sheet.id` = Blatt-ID, `sheet.variant_name` = „Parallax“ bzw.
  „Flux Bloom“, `generator` mit Codex-Version.
- Pflicht nach [weapon-spec.md](weapon-spec.md): Maßstab und Achsen im Toolgen-Rahmen (vorn −Y, oben +Z, links +X, Ursprung
  `Socket_Hand`), Anker samt `part`, Teile mit Kanal (sieben `MT_`), Material, `toolgen_material`, Hüllquader, Farbvarianten, Skin
  ([Skins](weapon-spec.md#skins)), Visier mit `type`/`frame`/`window` und `window_geometry` ([Visier-Vokabular](weapon-spec.md#visier-vokabular)),
  `moving_parts` ([Bewegliche Teile](weapon-spec.md#bewegliche-teile)), `robot_fit`.
- Was sich nicht ableiten lässt, steht als `null` mit Grund im Spec, wie bei Claude. Nichts raten.
- Seit claude-0.7 (additiv, `format_version` 1): `parts[].material` kennt `glass` (Glasscheiben, `toolgen_material: null`); Glas zählt
  als Fenster in `window_geometry`. `Socket_Sight` ist bei Claude jetzt die Oberkante der Visierschiene unter der Mitte der Halterung.
  `sight.sight_spec` verweist auf ein Visier der Visier-Serie (`VSnn.spec.json`); Codex lässt das Feld weg, solange es keine VS-Visiere
  verwendet ([Visier der Visier-Serie](weapon-spec.md#visier-der-visier-serie)).
- **Offen (Nutzer):** Sollen auch die Codex-Blätter das Standardvisier der Visier-Serie VS01–VS09 tragen? Bei Claude gilt das seit
  claude-0.7 nach der Entscheidung vom 17.10.2026 für die Waffen 1–9. Bis zur Entscheidung behält Codex seine eigenen Optiken.
- `CodexDesignReference` darf als zusätzliche Datei bleiben, ist aber nicht die Übergabe an Toolgen.
- Format-Änderungswünsche (neue Felder, andere Bedeutung) meldet Codex an Claude oder den Nutzer und legt sie nicht selbst fest.

## Texturen (Teil C) – gemeinsamer Katalog `docs/textures/`

Entscheidung des Nutzers vom 18.10.2026: Es gibt einen gemeinsamen Texturkatalog in `docs/` dieses Repos mit Parametern und
Musterbildern, den Claude und Codex lesen. Der Aufbau unten ist ein **Vorschlag**, angelegt ist noch nichts.

### Ausgangslage

Heute gibt es drei Fassungen derselben Idee:

| | Claude | Codex | Toolgen `data/surface_recipes.json` |
|---|---|---|---|
| Materialien | `lack`, `brushed`, `rubber`, `plastic`, `light` (`xlroles.material_of`) | `paint`, `metal`, `rubber`, `plastic`, `light` (`raster.texture_factor`) | 9: `painted`, `painted_matte`, `ceramic`, `brushed`, `satin`, `polished`, `rough_cast`, `rubber`, `energy_glass` |
| Muster | Glanzverlauf, Schleifspur (3 Sinus 3,1/7,3/13,1, ±13 %), Rautenrändel (Teilung 4, −34 %), Korn (Zelle 1/1,3, ±9 %) in Modelleinheiten (`xl.make_texture`) | eigene Sinus-Muster (Metall ±6,5 %, Rändel Frequenz 1,2, Korn ±4,5 %) in Modelleinheiten | `knurl`, `grooves`, `lamellae`, `seams`, `brushed`, `grain` in mm, Höhe ≤ 0,3 mm |
| Oberflächen | `paint`, `polished_gold`, `polished_chrome`, `neon` mit Tonleitern und Kantenabnutzung (`skinraster.py`) | `gold`, `chrome` (`_finish_surface`) | `smoothness`, `wear` (subtle 0,2 · medium 0,5 · strong 0,8) |
| Skins | 9 Arten, fünf je Blatt (`skins.CATALOG`) | 5 Arten, für alle Blätter gleich (`skins.py`) | – |

Die Werte stimmen nicht überein, und die Muster hängen an Modelleinheiten. Dieselbe Rändelung ist deshalb auf jeder Waffe anders groß.

### Vorgeschlagener Aufbau

```
docs/textures/
  README.md            Zweck, Einheiten, Regeln für Änderungen, Zuordnung zu Toolgen
  catalog.json         alle Parameter (format "cubeescape-design/texture-catalog", format_version 1)
  catalog.schema.json  JSON-Schema
  swatches/            Musterbilder, 512 × 512 PNG, eines je Material, Oberfläche und Skin
  make_swatches.py     erzeugt swatches/ nur aus catalog.json (numpy, Pillow); Referenz, keine Pipeline-Logik
  check_catalog.py     Schema, Musterbilder aktuell (sha256), Abgleich mit Toolgen, wenn das Repo lokal liegt
```

`catalog.json` hat sechs Abschnitte:

- **`units`**: Musterlängen in **mm am echten Objekt**. Die Pipelines rechnen mit dem Maßstab aus dem Spec (`units.model_unit_m`)
  um. Damit ist eine Rändelung auf Pistole und Raketenwerfer gleich fein, und Toolgen kann die Werte direkt backen. Helligkeitswerte
  sind Faktoren auf die Grundfarbe.
- **`materials`**: je Eintrag `id`, `name` (de/en), `toolgen_material` (eine der neun Toolgen-IDs), `pattern` mit Parametern,
  `finish`, typische `MT_`-Kanäle, Zuordnungsregel (z. B. Griff → `rubber`) und `swatch`. Start mit den fünf Blattmaterialien,
  benannt nach Toolgen: `painted` (lackiert), `brushed`, `rubber`, `painted_matte` (matter Kunststoff), `energy_glass` (Leuchtteil).
  Die übrigen vier Toolgen-Materialien kommen als Einträge ohne Blattmuster hinzu.
- **`patterns`**: die sechs Toolgen-Muster mit gleicher Bedeutung (`size_mm`, `direction`, `height_mm`, dazu `contrast` für das Blatt)
  sowie zwei reine Blattmuster: `gloss_gradient` (Glanzverlauf über die Bauteilhöhe) und `none`.
- **`finishes`**: `paint`, `polished_gold`, `polished_chrome`, `neon`. Je Eintrag eine Tonleiter (fünf Stufen wie in `skinraster.py`),
  Glanzstreifen und Kantenabnutzung mit den drei Toolgen-Stufen (`wear_levels`).
- **`skins`**: alle Skin-Arten beider Pipelines in einem Katalog, die 9 von Claude und die 5 von Codex. Je Eintrag `id`, `name`,
  `origin` (claude/codex), die fünf Bausteine (Farbflächen, Glyphen/Zahlen/Embleme, Streifen/Verläufe/Ringe, Gold/Chrom mit Abnutzung,
  Rippen/Finnen) samt Parametern, Akzente `SK_Accent1/2` mit Oberfläche sowie Regeln für Kontrast und Platz. Beide Pipelines dürfen
  jede Art verwenden. Die Auswahl je Blatt bleibt Sache der Pipeline, der Name im Blatt kommt aus dem Katalog.
- **`channels`**: die sieben `MT_`-Kanäle und zwei Skin-Akzente mit Bedeutung, wie in [weapon-spec.md](weapon-spec.md) (Verweis,
  keine zweite Definition).

### Regeln

- `docs/` ist gemeinsam: Änderungen am Katalog nur auf Wunsch des Nutzers. Neue Einträge schlägt die jeweilige Pipeline im PR oder
  Bericht vor.
- Der Vertrag funktioniert wie beim Weapon-Spec: Felder dürfen hinzukommen. Umbenennen, Entfernen oder eine andere Bedeutung erhöhen
  `format_version`. Die Pipelines prüfen `format` und `format_version`.
- Beide Pipelines lesen `catalog.json` zur Bauzeit und kopieren keine Werte in eigenen Code. Ein Test je Pipeline stellt sicher, dass
  jedes verwendete Material, jede Oberfläche und jeder Skin im Katalog steht.
- Das Weapon-Spec verweist mit `parts[].texture` und `skin.catalog_id` auf Katalog-IDs (additiv, `format_version` 1). Toolgen muss dann
  nichts mehr aus dem Bild ableiten.
- Musterbilder werden nur von `make_swatches.py` erzeugt. Weichen sie von `catalog.json` ab, schlägt `check_catalog.py` an.

### Reihenfolge

1. **Claude** legt den Katalog an (nächste freie Claude-Version): Werte aus Claudes heutigen Mustern, Codex' fünf Skins und die Toolgen-Zuordnung,
   dazu Musterbilder und Prüfskript. Die Werte werden von Modelleinheiten in mm umgerechnet, mit dem Median-Maßstab der 60 Blätter als
   Startwert. Danach liest Claudes Pipeline den Katalog. Bildstufe auf dem Mac, `golden.json` neu, die Blätter ändern sich leicht
   (Musterfeinheit je Waffe).
2. **Codex** (Teil C): `texture_factor`, `_finish_surface` und die Skin-Liste lesen aus dem Katalog; die eigenen fünf Skins stehen dann
   unter `origin: codex` im Katalog. Neubau zusammen mit Teil A.
3. **Toolgen** liest den Katalog optional mit (eigener Auftrag in Toolgen, nicht Teil dieses Auftrags).

## Zuständigkeit
- Codex: Branch `codex/…` von `main`, schreibt nur unter `codex/`. Liest `claude/docs/` (diese Datei, weapon-spec.md, Schema,
  ENTSCHEIDUNGEN.md) und darf `claude/generator/style_metrics.py` zum Selbsttest aufrufen. Nichts aus `claude/` kopieren oder
  importieren.
- Claude: Texturkatalog `docs/textures/` anlegen (Teil C, Schritt 1), Abnahmemessung, Richtungstest der Specs, Eintrag in
  `variants.CODEX` und CHANGELOG-Zeilen (Wurzeldateien).

## Modell
- Teil A: `gpt-6.1-sol` (`high`), weil Licht, Kontur und Wirkung erst am Bild beurteilt werden.
- Teil C: `gpt-6-luna` (`medium`), weil Katalog und Prüfskript vorliegen und das Ergebnis automatisch prüfbar ist.
- Teil B: `gpt-6-luna` (`medium`), weil das Muster vorliegt (Claudes Exporter, Schema) und das Ergebnis automatisch prüfbar ist.
- Kontingent am 17.10.2026 um 23:2x: 5-h-Fenster 33 % übrig (Reset 03:41 am 18.10.), Woche 90 % übrig. Nach der Regel heißt das:
  Teil A erst nach dem Reset starten, Teil B ginge sofort.

## Prüfweg
1. Probe: KA01, KA05, KK05 und KK08 (kurz und lang) bauen, Kontaktbogen neben Claude KF05/KG07, Messung mit `style_metrics.py`.
   Freigabe durch den Nutzer an verkleinerten Bildern, wie bei Claude 0.3 (Probeblatt je Familie).
2. Danach alle 20 Blätter. Codex-Tests grün, Bildlauf auf dem Mac unter `heavy_lock`.
3. Specs: Schemaprüfung wie `claude/generator/test_spec.py` › `validate` in einem eigenen Codex-Test, Länge gegen die Toolgen-
   Bezugslänge (±0,5 mm). Claude prüft anschließend Richtung und Anker mit `spec_checks.py`.
4. Texturen: `python3 docs/textures/check_catalog.py` grün; Codex-Test, dass jede verwendete Material-, Oberflächen- und Skin-ID
   im Katalog steht; Musterfeld im Blatt gegen `swatches/` am Kontaktbogen.
5. Erwartete Unterschiede: nur Dateien unter `codex/` ändern sich. Die Blätter bekommen Konturen, eine hellere Oberseite und bei langen
   Waffen größere Orthos; Modelle und Paletten bleiben gleich.

## Release
nein.

## Berichtsform
Bericht in `report.md` im Worktree, erste Zeile Ergebnis mit Commit und Teststand, höchstens 15 Zeilen. Vorher/Nachher-Messwerte je
Serie und die Pfade der Kontaktbögen nennen; offene Formatfragen getrennt aufführen. CHANGELOG-Wunsch in die PR-Beschreibung.
