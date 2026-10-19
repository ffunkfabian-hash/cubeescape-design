# Auftrag an Codex: Designtyp im Spec und die 15 neuen Waffentypen auf den Codex-Blättern

**Modell und Aufwand dieser Sitzung:** Codex `gpt-6.1-sol`, `high` – Grund: neue Modelle ohne Vorlage in `codex/`, Ergebnis wird am Bild beurteilt,
Spec-Vertrag wird ergänzt. Prüfungen und kleine Pakete mit `gpt-6-luna` (`medium`).
Gewünscht von: Nutzer, 19.10.2026 („design_type + neue Typen“; [ENTSCHEIDUNGEN.md](ENTSCHEIDUNGEN.md)). Auftrag geschrieben von Claude
(Sitzung `DS 0.10 „Arsenal“ · Mac`); die Codex-Blätter entscheidet Codex, `codex/` ändert Claude nicht.
**Sitzungsname und Version:** vor der ersten Änderung im Versionsregister (`ffunkfabian-hash/cubeescape-rules#12`) reservieren, z. B.
`DS codex-0.1.6/0.2.6 „<Name>“ · Codex-Mac`; Branch `codex/<version>-<name>`.

## Grundlage (nur lesen, nichts übernehmen)
- Bestand, Destiny-Katalog und Maßnahmen: [waffentypen.md](waffentypen.md); Versionsbericht [0.10](versions/0.10.md) mit Patch 0.10.1.
- Typen, Längen, Visiere, Bewegungen, Untertypen: `claude/generator/wtypes.py` (Tabelle `TYPES`); Spec-Felder: [weapon-spec.md › Designtyp, Bedienung](weapon-spec.md#designtyp),
  Schema `claude/docs/weapon-spec.schema.json`; Texturprofile der neuen Typen: `claude/generator/texprofile.py › NEW`.
- Zielbild: Claudes Blätter KG11–KG25 (abgenommen 19.10.2026), Kontaktbögen `~/Library/Caches/CubeEscapeDesign/waffentypen-0.10/` und `…/waffentypen-0.10.1/`;
  Modelle `claude/generator/g11.py` … `g25.py` als Funktionsreferenz (Bauteile, Mechanik). Form, Stil und Farben bleiben Codex' eigener Stilvertrag (Parallax, Flux Bloom).

## Paket 1 – Designtyp im Spec (klein, zuerst)
Alle 20 Specs KA01–KA10/KK01–KK10 bekommen additiv (`format_version` 1) die Felder unter `weapon` wie bei Claude: `design_type`, `design_type_de`,
`destiny_type`, `subtype`, `ammo_class`, `toolgen_status` (`tool`), `type_source`; Werte je Typ aus `wtypes.TYPES` (Pistole = `sidearm`, Sturmgewehr = `auto_rifle`,
Spurgewehr = `trace_rifle`, Bogen = `combat_bow` …). `note` nur, wo die Bauweise vom Typnamen abweicht (Hinweis: KA08 hat ein Magazin – prüfen und ggf. begründen).
Blätter bleiben bytegleich.

## Paket 2 – die 15 neuen Typen (Nummern wie bei Claude)
| Nr. | Typ (`design_type`, `subtype`) | Visier (Visier-Serie, separat wie bisher) | Pflicht-Mechanik |
|---|---|---|---|
| 11 | Scout-Gewehr (`scout_rifle`) | VS03 | halbautomatisch, langer Lauf, Kastenmagazin |
| 12 | Handfeuerwaffe (`hand_cannon`) | VS01 | Trommel, Hahn |
| 13 | Lineares Fusionsgewehr (`linear_fusion_rifle`) | VS05 | Ladekammern, offene Beschleunigerstrecke |
| 14 | Spezial-Granatwerfer (`grenade_launcher_special`, `breech_loaded`) | VS04 | Kipplauf |
| 15 | Schwerer Granatwerfer (`grenade_launcher_heavy`, `drum_loaded`) | VS09 | Drehtrommel, Ladeklappe |
| 16 | Maschinengewehr (`machine_gun`) | VS06 | Gurt, Munitionskasten, Zuführdeckel |
| 17 | Schwert (`sword`) | keines | Klinge, Parierstange, Energiezelle |
| 18 | Glefe (`glaive`) | keines | Stange mit Abzug, Klinge mit Emitter, Schild |
| 19 | Schwere Armbrust (`heavy_crossbow`) | VS03 | quer liegende Wurfarme, Sehne, Spannhebel |
| 20 | Raketenpistole (`sidearm`, `rocket_assisted`) | VS01 | Raketenrohr, Raketenmagazin |
| 21 | Raketen-Impulsgewehr (`pulse_rifle`, `rocket_assisted`) | VS03 | Raketenmagazin, Rohrlauf |
| 22 | Slug-Schrotflinte (`shotgun`, `slug`) | VS04 | gezogener Lauf, Slug-Magazin |
| 23 | Hitze-Impulsgewehr (`pulse_rifle`, `dynamic_heat`) | VS03 | kein Magazin, Hitzespeicher, Entlüftung |
| 24 | Mikroraketen-Granatwerfer (`grenade_launcher_special`, `micro_missile`) | VS04 | einschüssig, Raketenvorrat |
| 25 | Streuschuss-Handfeuerwaffe (`hand_cannon`, `spread_shot`) | VS01 | Kipprahmen-Revolver, Streumündung |

Je Blatt: eigene Silhouette und Mechanik (keine Umfärbung), Feld BEDIENUNG (Nachladen, Spannen/Aufladen, Feuern) wie Claudes `operation`, Texturprofil
nach `texprofile.NEW` (als „Vorschlag, abgeleitet“ kennzeichnen), Prompts de/en. Spec: `toolgen_id` `null`, `toolgen_status` `not_connected`, `element` `null`,
`operation`, `moving_parts` mit `proposed: true`. Bezugslängen wie `wtypes.TYPES[…]['ref_len']`.
**Achtung `scout_rifle`:** Der Nutzer hat am 19.10.2026 entschieden, dass Toolgen das Spurgewehr in `trace_rifle` umbenennt; bis das in Toolgen umgesetzt
ist, bleibt `toolgen_id` des Spurgewehrs `scout_rifle` und das Scout-Gewehr hat `toolgen_id` `null`.

## Zuständigkeit
- Dateien: nur `codex/` (Pipeline, Modelle, Tests, `codex/docs/versions/`). Nicht anfassen: `claude/`, `docs/`; Wurzeldateien (CHANGELOG-Zeilen) als Änderungswunsch im PR.
- Zwei Pakete = zwei PRs (Paket 1 klein und schnell prüfbar).

## Prüfweg
Tests der Codex-Pipeline, Claudes `spec_checks` auf allen Codex-Specs (0 Befunde), Schema `claude/docs/weapon-spec.schema.json`, Blattgröße ohne Überlauf,
Stilwerte im Soll. Bildstufe (Blätter, Kontaktbogen als verkleinerte Übersicht) nur auf dem Mac mit `heavy_lock`; Cloud setzt um und prüft ohne Bildstufe.
Überschneidungen und schwebende Teile prüfen (Lehren aus 0.10: Visierschienen auf schrägen Gehäusen, Bügel nicht in Magazin/Trommel, Bezeichnung an beiden
Gegenstücken symmetrischer Teile, offene Ringe statt Vollkörper in Strahlkanälen).

## Release
nein (PR, Merge nach `main` durch den Nutzer).

## Zeitschätzung
Schätzung 19.10.2026 (Messweg: Claudes 0.10 mit 12 Modellen ≈ 4 h Arbeit, Bildlauf 30 Blätter): Paket 1 unter 1 h; Paket 2 je Variante 4–6 h, Bildlauf 10–20 min.

## Berichtsform
Bericht in `codex/docs/versions/0.1.md`/`0.2.md` (Patch-Abschnitte); erste Zeile fertig/nicht fertig mit Teststand, höchstens 15 Zeilen; Meldungen beginnen mit
dem Sitzungsnamen; keine Wartemeldungen.
