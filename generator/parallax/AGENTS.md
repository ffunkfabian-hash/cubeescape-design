# Cube Escape Design

Die globalen Regeln des Nutzers in `~/.codex/AGENTS.md` gelten. Antworten und Dokumentation auf Deutsch;
Code, Bezeichner und Kommentare auf Englisch.

- Eigenständiges Design-Werkzeug. Keine Unity-, Blender- oder CE-Laufzeit-Abhängigkeit hinzufügen.
- Ziel-Repository: https://github.com/ffunkfabian-hash/cubeescape-design (Nutzer, 17.10.2026).
- Masterprompt: `masterprompt.md`; Konstruktion vor Optik, Prüfliste Abschnitt 12 verbindlich.
- Modell-API `eng.py`, CPU-Renderer `raster.py`, Modelle `models/`, Blattlayout `sheet.py`, Build `build.py`.
- Prüfen: `python -m unittest discover -s tests -v`, dann Build und alle PNGs ansehen. Kein Unity-Lauf erforderlich.
- Schwere Bildläufe auf dem Mac und rechnerweit über die vorhandene heavy-run.lock serialisieren.
- Nur eigene Dateien ändern; Commit, Tag, Push oder Veröffentlichung nur auf Wunsch.
- Versionen dieses Projekts zählen unabhängig vom Spiel. Aktuell 0.1.0 „Parallax“.
