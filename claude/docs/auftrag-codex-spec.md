# Auftragsentwurf an Codex: Weapon-Spec für die Codex-Blätter

Entwurf von Claude (claude-0.2, 17.10.2026) auf Wunsch des Nutzers („das müssen wir später auch Codex mitteilen“). Erst nach
Freigabe durch den Nutzer an Codex geben; Vorlage: `~/.claude/templates/auftrag.md`.

## Auftrag
Für die zehn Blätter der Codex-Pipeline (`codex/parallax/output/<waffe>.html`) je eine `<waffe>.spec.json` im Format
[weapon-spec.md](weapon-spec.md) (format_version 1) aus den eigenen Python-Modellen erzeugen, damit Toolgen beide Pipelines
gleich lesen kann. Keine Bildstufe nötig.

## Zuständigkeit
- Branch `codex/…`, Worktree von `main`; schreibt nur unter `codex/`.
- Liest (nicht ändern): `claude/docs/weapon-spec.md`, `claude/docs/weapon-spec.schema.json`; Vorbild der Ableitung:
  `claude/generator/export_spec.py` (Maßstab, Achsen, Anker, Kanäle, Visier) – Logik nachbauen, keine Dateien aus `claude/`
  importieren oder verlinken (Repo-Regel).
- Format-Änderungswünsche (neue Felder, andere Bedeutung) an Claude/den Nutzer melden, nicht selbst festlegen.

## Inhalt je Datei
- `sheet.id` mit eigenem Präfix (z. B. `parallax-assault`), `weapon.toolgen_id` aus der Tabelle in weapon-spec.md.
- `element` nach Entscheidung des Nutzers vom 17.10.2026: Pistole, Schrotflinte, Raketenwerfer `solar`; Sturm-, Spurgewehr `arc`;
  Impuls-, Fusionsgewehr `void`; Scharfschützengewehr, MP `energy`; Bogen `null`.
- Maßstab je Blatt aus den Toolgen-Längen (weapon-spec.md › Achsen und Maßstab), Achsen in den Toolgen-Rahmen (vorn −Y, oben +Z,
  links +X, Ursprung `Socket_Hand`) – die eigenen Modellachsen dafür angeben.
- Palette je Farbvariante der Codex-Blätter auf die sieben `MT_`-Kanäle; Teile mit Kanal, Material, Fläche, Hüllquader; Visier
  (`kind`/`window`), Aufkleber, `textures`.

## Modell
Codex `gpt-6-luna` (medium): Muster liegt vor (Claudes Exporter), Ergebnis automatisch prüfbar.

## Prüfweg
- Eigener Test unter `codex/`, der jede Datei gegen `claude/docs/weapon-spec.schema.json` prüft (Teilmenge wie
  `claude/generator/test_spec.py › validate`) und die Länge gegen die Toolgen-Bezugslänge (±0,5 mm).
- Erwartete Unterschiede: nur neue Dateien unter `codex/`.

## Release
nein.

## Berichtsform
Erste Zeile Ergebnis mit Commit; höchstens 15 Zeilen; offene Formatfragen getrennt aufführen.
