# Entscheidungen

Dauerhafte Entscheidungen des Nutzers für Claudes Teil von cubeescape-design (`claude/`, Wurzeldateien), mit Grund. Neue Zeilen unten
anfügen; Einzelheiten stehen in der Quelle (Versionsbericht), nicht hier. Muster wie Toolgen, Cubegen und Robogen (`docs/ENTSCHEIDUNGEN.md`).
Übertragen am 17.10.2026 aus `claude/docs/versions/0.1–0.4.md` (claude-0.5).

| Datum | Entscheidung | Grund |
|---|---|---|
| 16.10.2026 | Die Konzeptblätter sind das Zielbild für Texturen, Visiere und Leuchtfarben in Toolgen und Cube Escape; der Spec `KXnn.spec.json` ist ihre maschinenlesbare Fassung | Toolgen 0.7 konnte das Konzeptbild nicht lesen und hat Werte geraten; Quelle: [0.2](versions/0.2.md), [weapon-spec.md](weapon-spec.md) |
| 17.10.2026 | Bogen im Detailfeld „Abzugsbereich“: die Pfeilauflage kommt mit in den Rahmen | Rückfrage beim Nutzer in claude-0.1.2; Quelle: [0.1 › 0.1.2](versions/0.1.md) |
| 17.10.2026 | Element je Waffentyp im Spec nach Toolgens Zuordnung (Pistole solar, Sturmgewehr arc …), Bogen ohne Element | Entscheidung des Nutzers in Toolgen `docs/ENTSCHEIDUNGEN.md`; Quelle: [weapon-spec.md](weapon-spec.md), `export_spec.WEAPONS` |
| 17.10.2026 | Skins mit allen fünf Bausteinen (Farbflächen, Glyphen/Zahlen/Embleme, Streifen/Verläufe/Ringe, Gold/Chrom mit Kantenabnutzung, Rippen/Finnen); Stimmung, kein Nachbau | Der Nutzer fand die Waffen zu glatt (Referenzbilder 17.10.2026); Quelle: [0.3](versions/0.3.md) |
| 17.10.2026 | Skin-Katalog mit fünf Skins je Waffe; Farben aus den sieben MT_-Kanälen plus zwei feste Skin-Akzente | Quelle: [0.3 › Entscheidungen des Nutzers](versions/0.3.md) |
| 17.10.2026 | Neue Gestaltung erst als Probeblatt je Familie (KC01, KD02, KF05, KG07, KH10), Freigabe an verkleinerten Bildern, dann alle Blätter | Probe nach zwei Runden freigegeben; Quelle: [0.3](versions/0.3.md) |
| 17.10.2026 | Jede neue Variante bekommt zum Kennbuchstaben einen englischen Namen (1–3 Wörter, nicht doppelt, I und O nicht als Buchstaben); C–H bleiben ohne Namen | Wunsch des Nutzers; Regel in `CLAUDE.md`, geprüft von `new_variant.py`; Quelle: [0.4](versions/0.4.md) |
| 17.10.2026 | Variante J heißt „Black Ice“ (Stealth-Serie) | Wahl des Nutzers aus drei Vorschlägen (Black Ice, Monolith, Starliner); Quelle: [0.4](versions/0.4.md) |
| 17.10.2026 | Viewer bei jeder Varianten-Sitzung ohne Nachfrage aktualisieren, beim Abschluss einmal anbieten, ihn zu öffnen | Regel des Nutzers in `CLAUDE.md` |
| 17.10.2026 | Blätter, Vorschauen und `index.html` werden lokal gebaut und als Release-Asset ausgeliefert (`release_assets.py`), nicht committet; im Repo bleiben Specs und `golden.json` (sha256) | Repo-Größe (Blätter 46 MB, Messung 17.10.2026); Quelle: [0.4 › 0.4.1](versions/0.4.md) |
| 17.10.2026 | WebP-Qualität der Blattbilder 60 statt 92; Schriften als Dateien neben den Blättern (SIL OFL 1.1, mit Lizenztexten) statt Google Fonts | Optionen Repo-Größe und Schrift, vom Nutzer entschieden; Quelle: [0.4 › 0.4.1](versions/0.4.md), `CHANGELOG.md` |
