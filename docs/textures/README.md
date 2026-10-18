# Texturkatalog

Gemeinsamer Katalog für Claude und Codex (Entscheidung des Nutzers, 18.10.2026): Materialmuster, Oberflächen und Skins an **einer**
Stelle, mit Parametern und Musterbildern. Angelegt mit claude-0.6.1 (Bericht: [claude/docs/versions/0.6.md](../../claude/docs/versions/0.6.md)).
Aufbau und Reihenfolge: [claude/docs/auftrag-codex-angleichung.md](../../claude/docs/auftrag-codex-angleichung.md) › Texturen (Teil C).

| Datei | Inhalt |
|---|---|
| `catalog.json` | alle Parameter, `format` `cubeescape-design/texture-catalog`, `format_version` 1 |
| `catalog.schema.json` | JSON-Schema dazu |
| `swatches/` | Musterbilder 512 × 512 PNG (24 Stück) und `manifest.json` (sha256) |
| `make_swatches.py` | erzeugt `swatches/` nur aus `catalog.json` (numpy, Pillow). Referenz, keine Pipeline-Logik |
| `check_catalog.py` | Schema, Verweise, Musterbilder (sha256), Abgleich mit Toolgen `data/surface_recipes.json`, wenn lokal vorhanden |

## Abschnitte von `catalog.json`
- **`units`**: Längen in **mm am echten Objekt**. Die Pipelines rechnen mit `units.model_unit_m` des Specs (Meter je Modelleinheit) in
  Modelleinheiten um: `Modelleinheiten = mm / (model_unit_m · 1000)`. Der Wert im Katalog (0,00139823) ist nur der **Startwert**
  (Median der 60 Claude-Specs, Spanne 0,386–3,096 mm je Einheit). Dieselbe Rändelung ist damit auf jeder Waffe gleich fein.
  Helligkeiten sind Faktoren auf die Grundfarbe, Skin-Lagen Anteile (0..1) der Waffenausdehnung.
- **`materials`**: neun Toolgen-Materialien (`painted`, `brushed`, `rubber`, `painted_matte`, `energy_glass` mit Blattmuster;
  `ceramic`, `satin`, `polished`, `rough_cast` nur als Eintrag). `aliases` verbinden Claudes (`lack`, `plastic`, `light`) und Codex'
  Namen (`paint`, `metal`) mit der Katalog-ID; `aliases.spec` ist die ID im Weapon-Spec (`matte`, `lit`).
- **`patterns`**: die sechs Toolgen-Muster (`knurl`, `grooves`, `lamellae`, `seams`, `brushed`, `grain`) mit gleicher Bedeutung
  (`size_mm`, `direction`, `height_mm`) und `contrast` für das Blatt, dazu die reinen Blattmuster `gloss_gradient` und `none`.
  `used_by_sheets: false` = Toolgen-Relief ohne Blattwert (Maße je Waffe im Toolgen-Relief). `height_mm` ist `null`: Das Blattmuster
  ist nur Helligkeit, die Reliefhöhe (≤ 0,3 mm) legt Toolgen fest.
- **`finishes`**: `paint`, `polished_gold`, `polished_chrome`, `neon` mit Tonleiter (vier Stufen plus Glanzlicht); Glanzstreifen und
  Kantenabnutzung stehen in **`wear`** (zusätzlicher Abschnitt): drei Stufen `subtle`/`medium`/`strong` mit den Toolgen-Werten
  0,2/0,5/0,8, dazu Breite und Deckung der Zeichnung.
- **`skins`**: 14 Skins, 9 `origin: claude` (aus `skins.CATALOG`), 5 `origin: codex` (aus `codex/fluxbloom/skins.py`, nur gelesen).
  Claudes Lagen (`side_block`, `bands`, `gradient`, `rings`, `glyphs`, `finish`, `trim`, `edge_wear`) sind in [weapon-spec.md](../../claude/docs/weapon-spec.md)
  beschrieben. Codex' Muster sind als `region` (Maske aus `diagonal`, `u`, `v`, `sawtooth`, `ellipse_rings`, `all`/`any`) und `blend`
  festgehalten, Emblem, Nummer und Rippen als `decor`. Beide Pipelines dürfen jede Art verwenden; die Auswahl je Blatt bleibt Sache der Pipeline.
- **`glyphs`**: Segmentziffern, Runen, Embleme (Claudes Zeichensatz), für die Musterbilder und als Vorlage.
- **`channels`**: die sieben `MT_`-Kanäle und `SK_Accent1/2`; Bedeutung wie [weapon-spec.md](../../claude/docs/weapon-spec.md) › Kanäle
  (Verweis, keine zweite Definition), `material` = Standard laut Toolgen.
- **`swatch_setup`**: Konstanten der Musterbilder (Palette, Beleuchtung, Muster-Gehäuse).

## Musterbilder
Eines je Material, Oberfläche, Wear-Stufe (`wear.png`: drei Blöcke) und Skin. Materialbilder zeigen eine Ebene mit u = Länge,
v = Höhe, der Balken unten links ist ein Viertel der Bildbreite (`swatch_view_mm / 4`). Skinbilder sind **Schemabilder** auf einem
Muster-Gehäuse mit Lauf (grobe Wiedergabe der Lagen, z. B. Querstreifen nur als Randstreifen oben); maßgeblich sind die Parameter.
Nur `make_swatches.py` erzeugt sie. Weicht ein Bild oder `catalog.json` vom Manifest ab, schlägt `check_catalog.py` an.

```bash
python3 docs/textures/check_catalog.py            # schnell, nur Standardbibliothek
~/Library/Caches/CubeEscape/concept-sheets-venv/bin/python docs/textures/check_catalog.py --deep   # Pixel neu erzeugen
~/Library/Caches/CubeEscape/concept-sheets-venv/bin/python docs/textures/make_swatches.py          # Musterbilder neu
```

## Regeln für Änderungen
- `docs/` ist gemeinsam: Änderungen am Katalog nur auf Wunsch des Nutzers. Neue Einträge schlägt die jeweilige Pipeline im PR oder Bericht vor.
- Wie beim Weapon-Spec: Felder dürfen hinzukommen; Umbenennen, Entfernen oder eine andere Bedeutung erhöhen `format_version`. Die
  Pipelines prüfen `format` und `format_version`.
- Beide Pipelines lesen `catalog.json` zur Bauzeit und kopieren keine Werte in eigenen Code. Ein Test je Pipeline stellt sicher, dass
  jedes verwendete Material, jede Oberfläche und jeder Skin im Katalog steht.
- Nach jeder Änderung: `make_swatches.py`, dann `check_catalog.py` (beide Ergebnisse committen).

## Stand und Grenzen
- Claudes Pipeline (`xl.py`, `skinraster.py`, `skins.py`) liest den Katalog **noch nicht**; die Werte sind heutige Claude-Werte, in mm
  umgerechnet. Die Umstellung ist ein eigener Schritt mit Bildstufe (Blätter ändern sich leicht: Musterfeinheit je Waffe).
- Codex' Muster (`raster.texture_factor`, `_finish_surface`) weichen von Claudes ab (Modelleinheiten, Reflexionskeulen); in Teil C
  gleicht Codex an den Katalog an. Seine fünf Skins stehen als `origin: codex` im Katalog, so wie der Code sie heute beschreibt.
- Die Zuordnung `parts[].texture` und `skin.catalog_id` im Weapon-Spec (additiv) und das optionale Lesen durch Toolgen sind eigene Aufträge.
