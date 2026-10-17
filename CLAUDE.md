# Regeln für Claude in diesem Repository

Zuerst gelten die globalen Regeln aus `ffunkfabian-hash/cubeescape-rules` (lokal `~/.claude/CLAUDE.md` bzw.
`~/.codex/AGENTS.md`). Ergänzend für dieses Repo:

- Claude schreibt ausschließlich unter `claude/` (Pipeline, Modelle, Konzeptblätter, Prompts).
- `codex/` gehört Codex: nicht ändern, nicht verschieben, keine Dateien daraus übernehmen oder per Symlink koppeln.
- `docs/` ist gemeinsam (Masterprompt, Aufträge, Vorlagen): nur nach ausdrücklichem Wunsch des Nutzers ändern.
- Releases von Claude: Branch `release/claude-<version>` pushen; der Workflow legt Tag `claude-v<version>` und Release an.
- Wurzeldateien (`README.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, `.ce-repo.json`, `.github/`) pflegt Claude; Codex meldet
  Änderungswünsche (z. B. eigene CHANGELOG-Zeilen `codex-…`) im PR oder an den Nutzer.
- Codex arbeitet auf Branches `codex/…`; der Merge nach `main` erfolgt per Pull Request durch den Nutzer bzw. nach seiner Freigabe.
  Claude committet seine eigenen Ordner direkt auf `main`.
- Bildstufen (Rendern der Konzeptblätter) laut globaler Regel auf dem Mac mit `heavy_lock`; Cloud-Sitzungen nur schnelle Prüfungen.
- **Erfahrungen** (Lehren aus Modell-, Raster- und Render-Pipeline, Prompts und Konzeptblättern) stehen in `docs/masterprompt.md` und
  `docs/prompt-vorlagen.md` (gemeinsam, Änderungen nur auf Wunsch des Nutzers), Claudes zusätzlich in `claude/docs/versions/`; vor dem
  Bauen, das ein Schwesterprojekt berührt (Toolgen, Cube Escape, Robogen, Cubegen), dessen Stelle lesen: `~/.claude/CLAUDE.md` ›
  Erfahrungen festhalten und querlesen.
