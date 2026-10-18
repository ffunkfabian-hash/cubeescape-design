# K · Flux Bloom

Zehn neue experimentelle Low-Poly-Waffenkonzepte. Variante K trägt in Kopf, Prompts und Spec den Namen „Flux Bloom“.
Die IDs KK01–KK10 bezeichnen Pistole, Sturmgewehr, Impulsgewehr, Schrotflinte, Scharfschützengewehr,
Maschinenpistole, Fusionsgewehr, Spurgewehr, Raketenwerfer und Bogen.

## Analyse vor dem Bau

Die neuen Modelle werden eigenständig für Codex konstruiert; Claudes Dateien und die alten Parallax-Konzepte werden
nicht übernommen. Wiederverwendet werden ausschließlich der geprüfte eigene CPU-Renderer, die Geometrie-API,
das Blattlayout und allgemeine Bauteilhelfer. Jede Waffe bekommt eine neue, charakteristische Silhouette und eine
kohärente kräftige Palette. Abzug, Magazin, Lauf, Optikhalter und alle Verbindungen bleiben konstruktiv lesbar.

Verbindliche Referenz: [gemeinsamer Masterprompt](../../docs/masterprompt.md).
Keine Unity-/Blender-Abhängigkeit, keine Änderungen an Spiel- oder Importformaten.

## Bauen und prüfen

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python build.py
```

Bildläufe ausschließlich auf einem Mac mit der vorhandenen rechnerweiten `heavy_lock` ausführen.
Der Build öffnet Chromium und nimmt jedes 4800 × 4432-Blatt auf; Vorschauen und Kontaktbogen folgen aus denselben PNGs.
HTML-Galerie: `output/index.html`. PNGs liegen unter `~/Library/Caches/CubeEscapeDesign/concept-sheets/fluxbloom-upgrade-full/`.
`--weapon sniper` wählt ein Modell; `--output` und `--screenshots` ändern die Ausgabeorte.

Eigene Daten pro Blatt: HTML, DE-/EN-Prompts, Spec mit `sheet.variant_name`, Materialrollen und sämtlichen Polygonen.
Der zusätzliche Typ `CodexDesignReference` in `*.reference.json` ist eine eigene gestalterische Referenz, kein Importvertrag und keine
Fertigungszeichnung. Die Rohpolygone verwenden Designeinheiten; Referenzmaße in Metern, Achsenumrechnung und Anker sind zusätzlich dokumentiert. Sechs Orthos teilen Maßstab und Bezugspunkt;
Hauptansicht, Detail und separate Optik haben eigene Darstellungsmaßstäbe.

Die Tests prüfen Geometrie, Z-Verdeckung, Achsen, sichtbare Beschriftungsanker und Objekttexturen. Für die Abnahme
werden zusätzlich die finalen Bilder kritisch nach Abschnitt 12 des Masterprompts angesehen. Automatische
Bauteil-Verbindungsprüfungen sind Grobprüfungen, kein Beweis physikalischer Funktionsfähigkeit.

## Gemeinsame Überarbeitung 0.2.1 / Parallax 0.1.1

Große Hauptisometrie, sechs gleich skalierte Orthos, Basis-Griffdetail, separate klassenbezogene Optik,
Materialansicht aus echten Teilen, vier Paletten mit Hauptskin und fünf entworfene Skin-Layouts.
Objektfeste Farbblöcke, eigene Zahlen/Glyphen, Bänder, Gold-/Chromflächen, Kantenabnutzung und befestigte Rippen.
Lokale Schriften samt OFL-Lizenzen; WebP-Bilder mit Qualität 60. Generierte Ausgaben sind von Git ausgeschlossen.

`--collection parallax` lädt die getrennten Parallax-Modelle, `--probe` wählt vier repräsentative Klassen.
[Beide Serien](../index.html). Schnelle Prüfung ab Repo-Wurzel:
`python -m unittest discover -s codex/fluxbloom/tests -v`.

Beide Serien samt Direktvergleich in einem gemeinsamen Mac-Zeitband bauen:

```sh
python3 '/Users/ffunk/Claude/Cube Escape/Tools/heavy_lock.py' run \
  --what 'Codex Parallax und Flux Bloom' -- \
  codex/fluxbloom/.venv/bin/python codex/fluxbloom/build_both.py
```

Der Vergleich erwartet die separat heruntergeladenen Claude-v0.3-Bildbelege unter
`~/Library/Caches/CubeEscapeDesign/comparison/shots/`. Ohne diese Belege die Serien einzeln mit `build.py` bauen;
`compare.py` kopiert keine Claude-Quellen. Der Vergleich liegt anschließend unter
`~/Library/Caches/CubeEscapeDesign/comparison-upgrade/index.html`.

## Stilvertrag, Weapon-Spec v1 und gemeinsamer Katalog

Die aktuelle Überarbeitung verwendet [docs/textures/catalog.json](../../docs/textures/catalog.json) zur Bauzeit:
Material-Aliase, physische Mustergrößen in mm, Oberflächen, Abnutzung und die bestehenden fünf Skins. Kein Katalogwert
wird als zweite Rezeptdefinition im Codex-Code gepflegt. `units.model_unit_m` aus dem Spec versorgt alle Bildpanels;
der Katalog-Startwert greift nur ohne Spec und wird als solcher ausgewiesen.

Die Darstelleinheiten des Blattfits sind ausdrücklich von physischen Metern getrennt: vier Displayeinheiten je
Modelleinheit lassen den Claude-Fit mit cap6 auf den kleineren Codex-Modellen zu, ohne die Modelle zu verändern.
Lange Waffen bekommen volle Orthozeilen; bei breiteren Formen wird die rechte Spalte höher und die Zusatzfelder
links schmaler. Gemeinsamer Maßstab und Hüllquader-Mittelpunkt bleiben erhalten.

Ohne Bildstufe: `python codex/fluxbloom/build.py --spec-only`, ebenso mit `--collection parallax`.
Die Dateien `KAxx.spec.json` / `KKxx.spec.json` neben den Blättern sind das kanonische Weapon-Spec-v1-Format;
`weapon-spec.schema.json` ist das unabhängig formulierte eigene Prüfprofil, zusätzlich prüfen Tests das offizielle
Schema nur lesend. `jsonschema` ist dafür eine verpflichtende Abhängigkeit.

Freigegebener vollständiger Neubau (Mac unter heavy_lock):
`python codex/fluxbloom/alignment_build.py --full`.
Vier Katalogproben samt breitem Raketenwerfer und Kontaktbogen: derselbe Befehl ohne `--full`.
Prüfwerte erneuern: `python codex/fluxbloom/spec_hashes.py`.

Messung nur mit dem offiziellen CLI `claude/generator/style_metrics.py`, Codex-Feld `150 560 2910 2120`;
Ergebnis enthält dessen Rundung. Materialvergleich und Messdaten liegen unter
`~/Library/Caches/CubeEscapeDesign/style-contract/`. Die Musterbilder im Katalog bleiben unverändert.

Die Spec enthält konservative Use-Clip-Zuordnungen anhand der dokumentierten Bauteilnamen; unbekannte Teile stehen
mit Grund auf null. Offene Aperturen sind als solche beschrieben, es wird kein physisches Glas erfunden.
Die vollständigen Skin-Rezepte sind über Katalog-IDs erreichbar. V1 beschreibt nicht jede dynamische Ersatzfarbe,
kontinuierliche Mischung oder elliptische Ringmaske; die präzisen Grenzen stehen in den Skin-Notizen.
