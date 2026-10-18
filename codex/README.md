# Codex · Cube Escape Designs

[A „Parallax“ und K „Flux Bloom“ im eigenen Viewer](index.html). Beide Modellserien bleiben eigenständig;
Raster, Materialien, Skins, Blattaufbau und Referenzdaten verwenden gemeinsame eigene Codex-Werkzeuge.

- [Parallax · codex-0.1.2](parallax/README.md): zehn bestehende Entwürfe, Keramik/Titan/Signalorange.
- [Flux Bloom · codex-0.2.2](fluxbloom/README.md): zehn experimentelle Entwürfe mit kräftigen Farbwelten.
- Versionsberichte: [0.1 Parallax](docs/versions/0.1.md), [0.2 Flux Bloom](docs/versions/0.2.md).

Nutzerauftrag vom 17.10.2026: Bestehende und zukünftige Entwürfe orientieren sich am aktuellen Claude-Stand,
ausdrücklich einschließlich Konstruktion, Blattaufbau, Materialien, Texturen und Skins; verbindlich in
[Codex-Regeln](AGENTS.md#verbindlicher-maßstab-aktueller-claude-stand).

Basis der Überarbeitung: `main` 9798f2a (Claude 0.5.2), Bildvergleich mit veröffentlichten F/H-Blättern aus Claude v0.3.
Code, Modelle und Ausgaben unter `codex/` gehören Codex; Claudes Pipeline unter `claude/generator/` bleibt getrennt.
Gemeinsam ist `docs/` mit dem [Masterprompt](../docs/masterprompt.md). Wurzeldateien pflegt Claude.
Generierte Blätter und Vorschauen entstehen lokal und sind von Git ausgeschlossen; kein Merge ohne Nutzerfreigabe.

## Angleichung A/B/C · 18.10.2026

Grundlage: main `0e62096`, [Stilvertrag und Weapon-Spec-Auftrag](../claude/docs/auftrag-codex-angleichung.md) und
[gemeinsamer Texturkatalog](../docs/textures/README.md). Die vier Stilproben wurden vom Nutzer für alle zwanzig Blätter
freigegeben; Katalogproben wurden zusätzlich mit den Musterbildern verglichen.

`*.spec.json` ist jetzt **cubeescape-design/weapon-spec v1**; die frühere eigene DesignReference wird bei Bildbauten
zusätzlich als `*.reference.json` erzeugt. Katalog-IDs stehen an Materialteilen und Skins. Das Schema wird mitgeliefert;
Tests prüfen das eigene und das offizielle Schema, physische Maße und tatsächliche Farb-/Geometriedaten.

Lokale Ausgaben und Galerien bleiben von Git ausgeschlossen. Kanonische Specs und `golden.json` mit Prüfwerten werden
versioniert. Einstieg regenerieren: `python codex/fluxbloom/viewer.py`. Die Umsetzung eines Toolgen-Imports oder einer
Roboter-Griffprüfung gehört nicht zu diesem Auftrag.
