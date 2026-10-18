# Auftrag an Codex: Texturprofil (`texture_profile`) auf den Codex-Blättern

**Modell und Aufwand dieser Sitzung:** Codex `gpt-6.1-sol`, `high` – Grund: Ergebnis wird am Bild beurteilt (Blattgestaltung) und ändert einen Spec-Vertrag.
Gewünscht von: Nutzer, 18.10.2026 („Texturprofil auf den Blättern anzeigen“; für Claudes Blätter seit claude-0.9 umgesetzt). Auftrag geschrieben von Claude
(Sitzung „Offene Punkte“); die Codex-Blätter entscheidet Codex, `codex/` ändert Claude nicht.

## Auftrag
KA01–KA09 (Parallax) und KK01–KK09 (Flux Bloom) bekommen (1) das Spec-Feld `texture_profile` und (2) das Feld **TEXTURPROFIL** auf dem Blatt:
sechs Kacheln (Gehäuse, Metall, Gummi, Energie, Kantenabnutzung, Decals) unter der Materialansicht, wie bei Claude seit claude-0.9
([Bericht](versions/0.9.md), Code `claude/generator/xl.py › profile_strip`; **nur lesen, nichts übernehmen** – Layout und Stil bleiben Codex' eigener
Stilvertrag). Bögen (KA10/KK10) bekommen kein Profil (nicht im Textur-Blatt). Modelle, Paletten, Skins und Visiere bleiben unverändert.

## Daten
Quelle: Cube Escape `Docs/Images/EquipmentConcepts/weapon_textures_1-9.webp` („Waffen Texturen 1–9“) – das Blatt des Nutzers ist maßgeblich. Claude hat
es in den Katalog-Wortschatz übertragen ([weapon-spec.md › Texturprofil](weapon-spec.md#texturprofil); Daten in `claude/generator/texprofile.py`, hier als Tabelle zum
Nachbauen; die Werte gelten je Waffentyp, also für Parallax und Flux Bloom gleich). Zuordnung über den Waffentyp im Weapon-Spec (`weapon.type`), Nummern 1–9 in der
Reihenfolge der Tabelle.

| Typ | Gehäuse | Metall | Gummi | Energie | Kantenabnutzung | Decals (Toolgen-IDs) |
|---|---|---|---|---|---|---|
| `pistol` | painted (Lackiert, leicht matt) | brushed (Gebürstet, robust) | Griffig, strukturiert | orange (Orange, klar) | subtle (Subtil, realistisch) | symbol_diamond, number_01 (Symbole, Nummern) |
| `assault_rifle` | painted (Lackiert, leicht matt) | brushed (Industrie-Finish) | Struktur, Griffe | blue (Blau, Tech-Elemente) | medium (Mittel, genutzt) | mil_ar2, tech_bars (Militärisch, Tech) |
| `pulse_rifle` | ceramic (Keramik-Look) | satin (Dunkel, satiniert) | Strukturiert | violet (Violett, leuchtend) | subtle (Kontrolliert) | tech_ring (Tech-Symbole) |
| `shotgun` | painted_matte (Strapazierfähig, matt) | rough_cast (Rau, massiv) | Griffzonen | orange (Orange, kräftig) | strong (Stark, abgenutzt) | hazard_stripes (Warnhinweise) |
| `sniper_rifle` | painted (Sauber, präzise) | brushed (Hochwertig, fein) | Minimal, griffig | light_blue (Hellblau, präzise) | subtle (Leicht, dezent) | serial_s07 (Seriennummern) |
| `smg` | painted_matte (Leicht, widerstandsfähig) | brushed (Dunkel, genutzt) | Stark strukturiert | cyan (Cyan, lebendig) | medium (Mittel, authentisch) | arrows_chevron, arrow_triangle (Taktisch, Pfeile) |
| `fusion_rifle` | painted (Hochtechnologie, glatt) | satin (Präzise, clean) | Technisch, lamellen | violet (Violett, intensiv) | subtle (Gezielt, dezent) | research (Forschungs-Symbol) |
| `scout_rifle` | painted (Glatt, sauber) | polished (Premium, poliert) | Minimal | blue (Blau, kontinuierlich) | subtle (Leicht, sauber) | tech_lines (Tech, Linien) |
| `rocket_launcher` | painted_matte (Schwer, robust) | rough_cast (Massiv, angeraut) | Stoßdämpfend | orange (Orange, Hitze) | strong (Stark, realistisch) | hazard_stripes, warning_triangle (Warnzeichen) |

Spec-Form je Blatt (additiv, `format_version` 1): `texture_profile = {housing:{material,text_de}, metal:{material,text_de}, rubber:{material:"rubber",text_de},
energy:{material:"energy_glass",color,text_de}, edge_wear:{level,text_de}, decals:{toolgen:[…],text_de}, interpretation, source, catalog:{file:"docs/textures/catalog.json",wear_levels:[…]}}`;
`interpretation` nur dort, wo Claude den Kurztext deuten musste (Tabelle: assault_rifle, pulse_rifle, smg, fusion_rifle, rocket_launcher) – gleichen Text übernehmen oder eigene Deutung nennen.
Material-IDs und Stufen müssen im Katalog `docs/textures/catalog.json` stehen (`check_catalog.py`, Claudes `spec_checks`).

## Zuständigkeit
- Branch `codex/texturprofil` (neuer Worktree von `main`; erst nach dem Merge von claude-0.9 nach `main`, sonst ohne dieses Dokument). Dateien: `codex/` (Pipeline `codex/fluxbloom`, Tests, `codex/docs/versions/0.1.md`/`0.2.md`).
- Nicht anfassen: `claude/`, `docs/`; Wurzeldateien meldet Codex als Änderungswunsch (CHANGELOG-Zeilen `codex-0.1.5` / `codex-0.2.5` im PR).

## Prüfweg
Tests der Codex-Pipeline, dann Claudes `spec_checks` auf allen 20 Specs (erwartet: 0 Befunde), Blattgröße 4800×4432 ohne Überlauf, Stilwerte im Soll (Parallax 77/53/7,8 %, Flux Bloom 75/52/6,9 %).
Bildstufe (Rendern der 18 Blätter, Kontaktbogen als verkleinerte Übersicht) nur auf dem Mac mit `heavy_lock`; Cloud darf umsetzen und ohne Bildstufe prüfen (Codex Cloud nur auf freigegebenem Branch).
Zielbild lokal: `~/Library/Caches/CubeEscapeDesign/texturprofil-0.9/` (Claudes Blätter mit dem Feld; Kontaktbogen `texturprofil_54_kontaktbogen.jpg`).

## Release
nein (PR, Merge nach `main` durch den Nutzer).

## Zeitschätzung
Schätzung 18.10.2026: Bildlauf je Serie etwa 50 s (Messwert 0.1.1/0.2.1), Gesamtdauer der Sitzung 1–2 Stunden.

## Berichtsform
Bericht in `codex/docs/versions/0.1.md`/`0.2.md` (Abschnitt `0.1.5`/`0.2.5`); erste Zeile fertig/nicht fertig mit Teststand, höchstens 15 Zeilen; keine Wartemeldungen.
