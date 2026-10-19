# Codex · Cube Escape Designs

[A „Parallax“ und K „Flux Bloom“ im eigenen Viewer](index.html). Beide Modellserien bleiben eigenständig;
Raster, Materialien, Skins, Blattaufbau und Referenzdaten verwenden gemeinsame eigene Codex-Werkzeuge.

- [Parallax · codex-0.1.6](parallax/README.md): 25 eigenständige Entwürfe, Keramik/Titan/Signalorange.
- [Flux Bloom · codex-0.2.6](fluxbloom/README.md): 25 experimentelle Entwürfe mit kräftigen Farbwelten.
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

Teil D (18.10.2026): Waffen 1–9 tragen eigenständig rekonstruierte VS01–VS09 nach den Sight-Specs;
Bögen behalten ihren rückseitig leuchtenden Pin. Bildnachweise und Grenzen stehen im Versionsbericht.
Mac-Prüfweg unter `heavy_lock`: `python codex/fluxbloom/vs_build.py`, danach `--full`.
`--capture-engine rsvg` ist ein expliziter SVG-Ersatz bei gesperrtem Chromium und bestätigt keine Browser-QA.


## Texturprofil · 18.10.2026

KA01–KA09 und KK01–KK09 zeigen sechs Typvorgaben im Materialfeld und exportieren denselben
`texture_profile`-Block im Weapon-Spec v1. Die beiden Bögen bleiben ohne Profil. Die Profilfarben
stammen aus dem Textur-Blatt des Nutzers; Modelle, Variantenpaletten, Skins und Visiere bleiben erhalten.
Prüfung ohne Bildstufe: `python -m unittest discover -s codex/fluxbloom/tests -q`.
Historischer Abnahmeweg für 0.1.5/0.2.5: `texture_profile_build.py --full`; aktueller Bauweg siehe Switchcraft.
`--capture-engine rsvg` ist ein ausdrücklich ausgewiesener Ersatz bei gesperrtem Chromium.


## Switchcraft · 19.10.2026

Format 2 und BEDIENUNG auf A/K; Typen 11–25 nach der gemeinsamen Typentabelle,
mit eigenständiger Codex-Geometrie. 50 Konzepte insgesamt, 30 neue Entwürfe ohne
Toolgen-/Spielanbindung. Texturprofile der neuen Typen sind abgeleitete Vorschläge.
Mindestabnehmer für `trace_rifle`: Toolgen 0.17.0 / Cube Escape 0.98.
Älterer Codex-Spec: `git show 5a5615d:codex/parallax/output/KA08.spec.json`
(analog KK); gemeinsamer Altstand: `claude-v0.11`.

Der Mac-Bau aktualisiert Blätter, WebP-Vorschauen (Q60), Galerie und Spec-Hashes.
Aktuelle Gesamtprüfung unter `heavy_lock`: `python codex/fluxbloom/switchcraft_build.py`.
Der zusätzliche Bedienbereich verlängert das Blatt unten auf 4800×4832; die früheren
Bildfelder behalten Position, Maßstab, Konstruktion, Palette und Skin-Rezepte.
