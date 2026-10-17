# Codex-Konzepte

Dieser Ordner enthält ausschließlich Codex-eigene Konzepte und ihre Erzeugungspipeline.

- [Parallax 0.1](parallax/README.md): Code, zehn Modelle, vollständige Prompts, lokale Fonts, Tests und erzeugte Konzeptblätter.
- [Konzeptblätter](parallax/output/index.html).

Claudes bestehende Fassung liegt getrennt unter `claude/generator/` und den zugehörigen bisherigen Dokumentations- und Ausgabewegen.
Keine Code-, Modell-, Prompt- oder Ausgabedateien zwischen den Fassungen gemeinsam beschreiben oder per Symlink koppeln.
Weitere Codex-Fassungen bekommen ihren eigenen Unterordner hier; eine Zusammenführung ist ein gesonderter Auftrag.

## Parallax · eigenständiger Codex-Stand

Die Pipeline 0.1 „Parallax“ besitzt ihre eigene Modell-API, zehn Modelle, lokal eingebettete Schriften,
selbstständige HTML-Blätter und 22 Unit-Tests. Einstieg: [Konzeptblätter](parallax/output/index.html),
[Anleitung](parallax/README.md), [Versionsbericht](docs/versions/0.1.md).

Vom Repository-Wurzelordner aus:

```bash
python -m unittest discover -s codex/parallax/tests -v
python codex/parallax/build.py
```

Code, Modelle, Prompts und Ausgaben der beiden Erzeuger werden getrennt gepflegt. Gemeinsam sind ausschließlich
die ausdrücklich freigegebenen Grundlagen in `docs/`; der verbindliche Masterprompt ist `docs/masterprompt.md`.
Wurzeldateien pflegt Claude. Codex meldet CHANGELOG-Wünsche in der Pull-Request-Beschreibung.
