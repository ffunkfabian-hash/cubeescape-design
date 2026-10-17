# CHANGELOG

Einträge je Erzeuger: `claude-…` (Ordner `claude/`), `codex-…` (Ordner `codex/`).

## claude-0.2
- Weapon-Spec je Konzeptblatt (`claude/output/sheets/KXnn.spec.json`, 50 Dateien): Element, Kanal-Paletten der vier
  Farbvarianten, Bauteile, Visier, Aufkleber, Maße, Anker, Texturmuster – für Toolgen ohne Bildlesen.
- Exporter, Schema und Test ohne numpy (quick-Check); ausdrückliche Kanalzuordnung `channel()`/`ch`.
- Bericht: [claude/docs/versions/0.2.md](claude/docs/versions/0.2.md), Format: [claude/docs/weapon-spec.md](claude/docs/weapon-spec.md)

## claude-0.1.2
- Detailfeld „Abzugsbereich“: Griff, Abzug und Bügel mittig unter der Feldüberschrift (Rahmen aus der sichtbaren Box, Magazin im
  Griff zählt mit); alle 50 Blätter neu aufgenommen, nur das Detailbild geändert.
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
