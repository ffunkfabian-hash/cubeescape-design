Claude-Konzeptblätter für Cube Escape (Ordner `claude/`): Waffenblätter XL je Claude-Variante (Liste in
`claude/generator/variants.py`, Stand claude-0.7: C, D, F, G, H, J) und die Visier-Serie VS01–VS09. Jedes Blatt kommt mit einem
maschinenlesbaren Steckbrief (`*.spec.json`) aus demselben Modell. Was sich geändert hat, steht in `CHANGELOG.md`.

- `claude-konzeptblaetter-<Variante>-<Version>.zip`: Waffenblätter (`sheets/*.dc.html`), Steckbriefe (`*.spec.json`) und Schriften (`fonts/`, SIL OFL)
- `claude-visier-serie-<Version>.zip`: Visier-Blätter VS01–VS09 mit Sight-Specs (`VSnn.spec.json`) und Schriften
- `claude-vorschauen-<Version>.zip`: WebP-Vorschauen (`previews/`) und der Viewer `index.html`
- `claude-prompts-<Version>.zip`: gemeinsame Regeln und Aufträge (`docs/`, mit Texturkatalog) und Waffen-Prompts (`claude/prompts/`)

Alle zips in einen Ordner entpacken und `index.html` öffnen; die Blätter laufen offline. Blätter und Vorschauen werden auf dem Mac gebaut
und mit `claude/generator/release_assets.py --upload` angehängt; im Repo liegen nur Generator, Steckbriefe und Hashes (`golden.json`).
