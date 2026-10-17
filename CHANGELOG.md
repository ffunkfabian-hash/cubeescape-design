# CHANGELOG

Einträge je Erzeuger: `claude-…` (Ordner `claude/`), `codex-…` (Ordner `codex/`).

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
