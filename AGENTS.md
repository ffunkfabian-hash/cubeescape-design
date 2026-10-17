# Regeln für Codex in diesem Repository

Zuerst gelten die globalen Regeln aus `ffunkfabian-hash/cubeescape-rules` (lokal `~/.claude/CLAUDE.md` bzw.
`~/.codex/AGENTS.md`). Ergänzend für dieses Repo:

- Codex schreibt ausschließlich unter `codex/` (eigene Pipeline, Modelle, Konzeptblätter, Prompts).
- `claude/` gehört Claude: nicht ändern, nicht verschieben, keine Dateien daraus übernehmen oder per Symlink koppeln.
- `docs/` ist gemeinsam (Masterprompt `docs/masterprompt.md`, Auftrag `docs/AUFTRAG.md`): nur nach ausdrücklichem Wunsch des Nutzers ändern.
- Verbindliche Gestaltungsregeln: `docs/masterprompt.md`.
- Wurzeldateien (`README.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, `.ce-repo.json`, `.github/`) pflegt Claude; Codex meldet
  Änderungswünsche (z. B. eigene CHANGELOG-Zeilen `codex-…`) im PR oder an den Nutzer.
- Codex arbeitet auf Branches `codex/…`; der Merge nach `main` erfolgt per Pull Request durch den Nutzer bzw. nach seiner Freigabe.
  Claude committet seine eigenen Ordner direkt auf `main`.
- Bildstufen (Rendern der Konzeptblätter) laut globaler Regel auf dem Mac mit `heavy_lock`; Cloud-Sitzungen nur schnelle Prüfungen.
