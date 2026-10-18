# CHANGELOG

Einträge je Erzeuger: `claude-…` (Ordner `claude/`), `codex-…` (Ordner `codex/`).

## claude-0.8
- Pipeline liest den gemeinsamen Texturkatalog `docs/textures/catalog.json` (`texcat.py`): Muster der Materialansicht in mm am Objekt (mit der Modelleinheit
  des Blatts umgerechnet, gleiche Rändelung auf jeder Waffe gleich fein), Skins, Tonleitern und Kantenabnutzung aus dem Katalog; Katalog-Inhalt im Cache-Schlüssel.
- Spec (additiv, format_version 1): `parts[].texture`, `skin.catalog_id`/`items[].catalog_id`, `textures.catalog`; `texture_profile` je Waffentyp (Textur-Blatt:
  Material-IDs, Abnutzungsstufe, Toolgen-Decals; Waffen 1–9) – damit ist die Decal-Zuordnung zu Toolgen erledigt.
- Black Ice (J) bevorzugt bei Gleichstand dunkle Hauptskins; andere Varianten unverändert.
- Inhalts-Cache für Blätter (`claude/generator/sheetcache.py`): `build_all.py`/`build_xl.py`/`build_vs.py` bauen nur Blätter neu, deren Schlüssel
  (Modell, Palette/Skin, Quelltext der schreibenden Funktionen `CODE_PARTS`) sich geändert hat; Cache außerhalb des Repos. `--force` (alles neu, Einträge
  erneuert) und `CE_NO_CACHE=1` (Cache ganz aus) umgehen den Cache; `full`-Check (`test_golden --full`) und Release immer ohne Cache. Test `claude/tests/test_sheetcache.py`.
- Alle 60 Waffenblätter und Specs neu (Musterfeinheit; KJ: Skin-Auswahl), Visier-Serie unverändert. Bericht [claude/docs/versions/0.8.md](claude/docs/versions/0.8.md).

## codex-0.1.3 / codex-0.2.3 (PR #4, gemerged)
- Parallax (0.1.3) und Flux Bloom (0.2.3): KA01–KA09 und KK01–KK09 tragen das Standardvisier VS01–VS09 (nachgebaut nach `VSnn.spec.json`, ±0,5 mm,
  Montage auf der Schiene, Glas, Strahlprüfung über die ganze Öffnung; KK03 mit Erhöhung 33 mm); Bögen behalten den Pin (Pin/Leuchtpunkt entlang −Y,
  `Socket_Sight` Unterkante-Mitte). Das Visier sitzt auf den Blättern nicht auf der Waffe (Hauptansicht „ohne Optik“, Feld „Visier · separat“; Entscheidung 18.10.2026).
- Claudes `spec_checks` auf allen 20 Specs: 58 → 0 Befunde; Berichte [Parallax](codex/docs/versions/0.1.md), [Flux Bloom](codex/docs/versions/0.2.md).

## codex-0.1.2 / codex-0.2.2 (PR #3, gemerged)
- Stilvertrag (Konturen, kameragebundenes Licht, große Orthos langer Waffen), Weapon-Spec v1 (`KAnn.spec.json`/`KKnn.spec.json`) und gemeinsamer Texturkatalog
  `docs/textures/` (physische Mustergrößen, Katalog-IDs); 20 Blätter neu gebaut, Modelle und Paletten unverändert.

## claude-0.7
- Waffenblätter 1–9 (C, D, F, G, H, J) tragen das Standardvisier ihres Typs aus der Visier-Serie VS01–VS09 (`vsmount.py`, Modell aus
  `vsmodels.py`, Farben über die MT_-Kanäle der Waffe, Sitz auf der Visierschiene; 15 Blätter mit neuer Schiene, 5 mit Erhöhung).
- Spec (additiv, format_version 1): `sight.sight_spec` (Verweis `VSnn.spec.json`, Lage, Erhöhung, Anker), `material: glass`; Typ/Rahmen aus der Serie.
- Die 23 Querfenster sind behoben (`KNOWN_CROSS_WINDOWS` leer), Bogen-Pins fluchten entlang −Y, Visier-Hinweise 0; Test `VisierSerie`.
- Glas ohne Schraffur (Wunsch des Nutzers): getönte Fläche mit weichem Glanz; VS01–VS09 neu gebaut.
- Bericht [claude/docs/versions/0.7.md](claude/docs/versions/0.7.md).

## claude-0.6.1
- Gemeinsamer Texturkatalog [docs/textures/](docs/textures/README.md) (`cubeescape-design/texture-catalog` v1): Materialien nach Toolgen-Namen, Muster in mm
  (Median-Maßstab der 60 Specs als Startwert), Oberflächen mit Tonleitern und Kantenabnutzung, 14 Skins (9 Claude, 5 Codex), Kanäle; 24 Musterbilder.
- `make_swatches.py` (nur aus `catalog.json`), `check_catalog.py` (Schema, sha256, Abgleich mit Toolgen `surface_recipes.json`); Teil von `./check`.
  Claudes Pipeline liest den Katalog noch nicht (eigener Schritt mit Bildstufe); Bericht [claude/docs/versions/0.6.md](claude/docs/versions/0.6.md).

## claude-0.6
- Visier-Serie VS01–VS09: je Waffe 1–9 ein Blatt im XL-Stil aus einem Modell (`vsmodels.py`, `vsheet.py`, `build_vs.py`): Isometrie,
  Seite/Oben/Rück mit Visierlinie und Ankern, Durchsicht im Spiel, vier Varianten, Fadenkreuze (nur Bild), Bausteine.
- Neues Format `cubeescape-design/sight-spec` v1 (`VSnn.spec.json`, [claude/docs/sight-spec.md](claude/docs/sight-spec.md), Schema, Test):
  Fenster, Rahmen, Glas-Tönung (RGBA linear), Röhre, Modul, Anker `Socket_Mount`/`Socket_Sight`/`Socket_Reticle`/`Socket_Eye`, Verweis
  auf die Waffen-Specs. Freie Durchsicht an der Geometrie geprüft (Visierlinie, ganze Öffnung, Funktionsfläche); 60 Waffenblätter unverändert.
- Raster: Glas durchscheinend (nur mit `glass=`, Waffenblätter bytegleich); Viewer-Gruppe „VS“; Bericht [claude/docs/versions/0.6.md](claude/docs/versions/0.6.md).

## claude-0.5.2
- Spec (additiv, format_version 1): `sight.type` (neun Typen des Visiertypen-Blatts plus `iron`/`pin`, `kind` folgt daraus),
  `sight.frame` (Rahmen-Variante), `parts[].toolgen_material` (Toolgen-Materialien); Visier-Hinweise vergleichen jetzt den Zieltyp.
- Richtungstest an der Funktionsfläche (`spec_checks.window_problems`, wiederverwendbar für VS01–VS09): Seitenscheiben, Öffnungen
  und Ringe zählen als Fenster; 23 bekannte Querfenster datiert im Test (Fix mit der Umstellung auf VS01–VS09), Gegenbeweis je Fall.
- Entscheidungen: Visier-Serie VS01–VS09 wird Zielbild, Waffenblätter werden danach umgestellt; Vokabular wie vorgeschlagen; Querfenster
  „Test jetzt, Fix mit Umstellung“.

## claude-0.5.1
- Spec (additiv, format_version 1): `robot_fit` – Größe in der Roboterhand (CE 0.82): Zielzahlen mit Quelle, Blatt auf Ziellänge
  gemessen; Pistole und Bogen ausgenommen; keine Roboter-Konzeptblätter.
- Visier-Abgleich aller 60 Blätter gegen die Visier-Blätter des Nutzers ([claude/docs/visier-abgleich.md](claude/docs/visier-abgleich.md)):
  6 passen, 46 weichen als Blatt ab, 19 mit Fenster quer zur Laufachse; Vorschlag `sight.type`/`frame`; Abgleich mit Toolgen-Mustern/Decals.
- ENTSCHEIDUNGEN.md: MP4 nur auf Anfrage, keine Roboter-Blätter, `robot_fit`, Visier-Zielbild.

## claude-0.5
- Spec (additiv, format_version 1): `moving_parts` und `parts[].moving` (bewegliche Teile wie Toolgens Use-Clip, Wurzel fest, Zuordnung
  über Bezeichnungen, sonst `null` mit Grund), `sight.window_geometry` (Fenster mit Durchsichtachse aus der Geometrie), `anchors.*.part`.
- `Socket_Muzzle` am vorderen Ende der Mündungsachse (17 Blätter: Mündungskappe/Pfeilspitze mitgezählt, Rakete im Rohr nicht).
- Richtungstest mit Gegenbeweis (gespiegelte Achsen), Visier gegen CE-Zielbild als Hinweisliste (`spec_checks.py`); `claude/docs/ENTSCHEIDUNGEN.md`.
- Bericht: [claude/docs/versions/0.5.md](claude/docs/versions/0.5.md), Format: [claude/docs/weapon-spec.md](claude/docs/weapon-spec.md)

## claude-0.4.1
- Golden nur als sha256 (`claude/tests/golden.json`, Blätter und Specs), Test `claude/tests/test_golden.py` (quick: Specs, Determinismus,
  Gegenbeweis; `--full`: Blätter, Determinismus eines Blatts). Blätter waren nicht reproduzierbar: `hash()` in `xl.swatch_svg` (je Prozess
  anderes IDs) → `zlib.crc32`; alle 60 Blätter neu gebaut, nur diese IDs ändern sich.
- `shot.py`: PNG ohne date/time-Chunks, 8 Bit (ImageMagick 6 und 7); `report.md` ungetrackt.
- Repo-Größe: Blätter (`*.dc.html`) und Vorschauen nicht mehr im Repo, sondern Release-Asset (je Variante ein zip, dazu Vorschauen;
  `claude/generator/release_assets.py`, Upload per `gh release upload` vom Mac, `release.yml` legt nur Release an); WebP-Qualität 92 → 60. Historie unverändert.
- Schriften als Dateien mit echten Gewichten (Chakra Petch 400–700, Barlow 400–600, JetBrains Mono variabel, SIL OFL 1.1) in `claude/output/sheets/fonts/`, relative `@font-face` statt Google Fonts.

## claude-0.4
- Neue Variante **J „Black Ice“**: zehn Stealth-Waffen (KJ01–KJ10) aus Facettenkörpern (`jlib.py`: abgeschrägte Prismen,
  Sechs-/Achtkant-Läufe, eisige Leuchtkanten), Blätter, Vorschauen, Specs und Prompts.
- Regel: neue Varianten bekommen einen englischen Namen; Register `variants.py`, Anlage mit `new_variant.py` (prüft die Regel).
- Spec: `sheet.variant_name` (additiv); `preview.py` nimmt die WebP-Vorschauen auf; `mkdoc.py` behält Abschnitte bei Teilbau.
- Bericht: [claude/docs/versions/0.4.md](claude/docs/versions/0.4.md)

## claude-0.3
- Skins: Katalog mit 9 gestalteten Skins (Farbflächen, eigene Glyphen/Zahlen/Embleme, Streifen/Verläufe/Ringe, Gold/Chrom mit
  Kantenabnutzung, Rippen/Finnen), je Waffe fünf; Farben aus den MT_-Kanälen plus zwei feste Skin-Akzente, Kontrastregel.
- Konzeptblätter: Hauptskin in Isometrie, Orthos und Farbvarianten, neue Reihe SKIN/MUSTER (Blatt 4800×4432), Prompts nennen den Skin.
- Spec: Feld `skin` (additiv, format_version 1) mit Lagen im Toolgen-Rahmen und neuen Mustertypen; Test 12 Fälle.
- Bericht: [claude/docs/versions/0.3.md](claude/docs/versions/0.3.md), Format: [claude/docs/weapon-spec.md › Skins](claude/docs/weapon-spec.md#skins)

## claude-0.2
- Weapon-Spec je Konzeptblatt (`claude/output/sheets/KXnn.spec.json`, 50 Dateien): Element, Kanal-Paletten der vier
  Farbvarianten, Bauteile, Visier, Aufkleber, Maße, Anker, Texturmuster – für Toolgen ohne Bildlesen.
- Exporter, Schema und Test ohne numpy (quick-Check); ausdrückliche Kanalzuordnung `channel()`/`ch`.
- Bericht: [claude/docs/versions/0.2.md](claude/docs/versions/0.2.md), Format: [claude/docs/weapon-spec.md](claude/docs/weapon-spec.md)

## claude-0.1.2
- Detailfeld „Abzugsbereich“: Griff, Abzug und Bügel mittig unter der Feldüberschrift (Rahmen aus der sichtbaren Box, Magazin im
  Griff zählt mit, beim Bogen die Pfeilauflage); alle 50 Blätter neu aufgenommen, nur das Detailbild geändert.
- `build_all.py` überspringt Schritte, deren gitignorierte Vorlagen fehlen (`render_dx05.py`, `make_v2d.py`).
- Bericht: [claude/docs/versions/0.1.md](claude/docs/versions/0.1.md) (Abschnitt 0.1.2)

## claude-0.1.1
- Mac-Prüfung aller 50 Konzeptblätter (4800×3400, Vorschauen unter `claude/output/previews/`); Vorprüfung in der Cloud.
- KD01, KD04, KD10 mit Visierschiene bzw. -aufnahme und separatem Visier; Abzug von KD01/KD07 sichtbar gemacht.
- Visier-Ansicht: getrennte Kimme/Korn rücken zusammen (11 Blätter); Prompts KD01/04/10 und `.gitignore` korrigiert.
- Bericht: [claude/docs/versions/0.1.md](claude/docs/versions/0.1.md) (Abschnitt 0.1.1)

## claude-0.1
- Pipeline, 50 Waffenmodelle (Varianten C, D, F, G, H) und Konzeptblätter XL mit separatem Visier, Material- und Farbvarianten.
- Trennung `claude/` · `codex/` · gemeinsames `docs/`; Release-Workflow für Tags `claude-v*`.
- Bericht: [claude/docs/versions/0.1.md](claude/docs/versions/0.1.md)

## codex-0.1
- Parallax: eigenständige Pipeline unter `codex/parallax/` mit zehn Waffenmodellen und konsistenten Konzeptblättern.
- CPU-Toon-Renderer, getrennte Optiken, Materialmuster, vier Farbpaletten und deutsche/englische Referenzprompts.
- 22 Unit-Tests und zehn auf dem Mac visuell geprüfte Blätter; [Versionsbericht](codex/docs/versions/0.1.md).
