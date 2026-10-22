# Formgen-Werkzeuge 0.11 „Wayfinder“

Status: abgenommen (Werkzeug-Rollout).

Fortsetzung des repoübergreifenden Agent-Tools-0.11-Rollouts: `tools/ce_tools/` wird ausschließlich durch `ce_sync.py` aus der dauerhaft integrierten Quelle aktualisiert. Die eingebettete Suche enthält damit die FTS-Korrektur und akzeptiert öffentliche Formgen-/Motiongen-Namen; Validatoren, Richter, Ressourcen-Sperren und API-Werkzeuge stammen aus demselben geprüften Stand.

Die ausdrückliche Nutzerfreigabe umfasst Wurzeldateien und gemeinsame Werkzeugordner. Die Claude-/Codex-Modellpipelines, exportierten Weapon-/Sight-/Geometry-Specs, Golden-Daten und Konzeptblätter bleiben unverändert. Modellversion claude-0.15 und Codex-Varianten behalten ihre Nummern; `tools-0.11.0` bezeichnet die gemeinsame Werkzeugquelle.

Die **eingebetteten gemeinsamen Prüfschemas** `unity_contract.v4.json` und `unity_contract_arms.v5.json` werden dagegen ausdrücklich auf den bereits freigegebenen Quellenstand angehoben. Sie prüfen Toolgen-/Unity-Pakete, nicht Formgens Weapon-/Sight-/Geometry-Specs. Das ist die Übernahme der bestehenden Pactguard-/Wayfinder-Validatoren ([Quellabnahme](https://github.com/ffunkfabian-hash/ce-agent-tools/pull/8)), keine neue Vertragsversion oder Änderung der erzeugten Formgen-Daten; deshalb keine neue Formgen-Migration oder Abnehmer-Mindestversion. Quellgleichheit wird einschließlich beider JSON-Schemas geprüft.

Die offenen Änderungen an `claude/prompts/Waffen-Prompts.md` bleiben im Haupt-Checkout. Vorheriger Datei-Hash und vollständiger Diff sind außerhalb des Repos gesichert und werden nach Integration verglichen. Kein Stash, kein Commit dieser Promptänderung, keine Sitzung kontaktieren oder neu laden. Lockstep bleibt unangetastet.

Abnahme: Quell-/Hash-Abgleich einschließlich Schemas grün; repo-eigener `./ce check` besteht alle elf Befehle (123 s), darunter Spec-/Golden-/Cache-/Texturkatalog-Prüfungen. Zusätzliche eingebettete Suchprobe (Ersetzen, Löschen, Alias und SQLite-/FTS-Inhaltsintegrität), Doku-Prüfung und Diff-Prüfung grün; unabhängiger `gpt-6.1-sol high` mit Freigabe nach Klarstellung der übernommenen Prüfschemas. Die erste Luna-Prüfung war wegen dieser unklaren Formulierung und des damals noch laufenden Quick nicht freigegeben; kein Schema entfernt oder Test abgeschwächt. Reines Werkzeug-Update ohne neue Bilder; Bild-/Blender-Stufen sind dafür nicht erforderlich. Belege: `~/Library/Caches/Nexogen/formgen-wayfinder-20261022/`.
