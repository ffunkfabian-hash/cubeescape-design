# Visier-Abgleich der Konzeptblätter mit dem Visier-Zielbild (Paket 1, 17.10.2026)

Hier wird nur gelesen und gemeldet; die Blätter, `SIGHTS` und das Vokabular sind unverändert. Entscheiden muss der Nutzer.

**Zielbild:** die beiden Visier-Blätter des Nutzers in Cube Escape: `Docs/Images/EquipmentConcepts/weapon_sights_1-9.webp` (Visier je
Waffe) und `sight_types_1-9.webp` (Visiertypen 1–9). Beide habe ich selbst gelesen. Dazu kommt `Docs/EQUIPMENT.md` › Visiere je Waffe.
**Blätter:** Feld „VISIER · SEPARAT“ aller 60 Vorschauen (Stand 0.4.1, Kontaktbogen außerhalb des Repos); dazu Kennung (`sight.kind`/
`window`) und Geometrie aus den Specs.

**Urteil je Blatt:** *passt* – Form und Kennung entsprechen dem Ziel. *Kennung* – das Blatt passt, nur `kind` weicht ab.
*Blatt* – die gezeichnete Form weicht ab. **quer** heißt: Scheibe bzw. Öffnung liegt auf der Seitenfläche, man sieht quer zur Laufachse
hindurch statt entlang −Y.

| Nr. | Ziel (Visier-Blatt) | C | D | F | G | H | J |
|---|---|---|---|---|---|---|---|
| 1 Pistole | kompaktes Reflex, offenes Fenster, ohne Kimme/Korn | Blatt: Kimme/Korn | Blatt: geschlossener Block, Seitenfenster, quer | Blatt: Kimme/Korn | Blatt: Kimme/Korn | Blatt: Reflex-Haube, quer | Blatt: Reflex-Haube, quer |
| 2 Sturmgewehr | offenes Holo | Blatt: Diopter/Korn | Blatt: geschlossener Kasten, quer | Blatt: Kimme/Korn | Blatt: Reflex-Haube, quer; Kennung reflex | Blatt: Holo-Kasten, quer | Blatt: Holo-Haube, quer |
| 3 Impulsgewehr | Präzision: runde Röhre mit Linse | Blatt: Block, Leuchtfront | Blatt: Kasten, quer | Blatt: Block, Leuchtpunkt | Blatt: Block, Leuchtfront | Blatt: offener Ring (Richtung stimmt) | Blatt: Reflex-Haube, quer |
| 4 Schrotflinte | Weitwinkel-Reflex, großes Fenster | Blatt: langer geschlossener Block | Blatt: Kasten, quer | Blatt: nur Korn | Blatt: Block mit Öffnung, quer | Blatt: Lochplatten, quer | Blatt: Kimme/Korn |
| 5 Scharfschütze | Hochpräzisions-Röhre | passt | passt | passt | passt | passt | passt |
| 6 Maschinenpistole | kompaktes, schnelles Fenster (Maschinenvisier) | Blatt: Kimme/Korn | Blatt: Kimme/Korn | Blatt: langer Block, quer | Blatt: Block, Leuchtfront | nahe: Kasten mit Scheibe vorn, Gehäuse geschlossen | Blatt: Reflex-Haube, quer |
| 7 Fusionsgewehr | Energie-Visier: breites Fenster, Energierahmen | Blatt: Block, Leuchtfront | Blatt: Block, Schlitz quer | Blatt: Block, Leuchtpunkt | Blatt: Block, Leuchtfront | nahe: Kasten mit Scheibe vorn, ohne Energierahmen; Kennung holo | Blatt: Holo-Haube, quer |
| 8 Spurgewehr | Fenster mit Markierungsrahmen, **keine Röhre** | Blatt: Röhrenblock mit Linse | Blatt: Röhre | Blatt: Röhre | Blatt: Röhre | Blatt: Röhre | Blatt: Röhre |
| 9 Raketenwerfer | Weitbereichs-Visier, breites Fenster | Blatt: Ringe, quer | Blatt: Röhre | Blatt: Block, Leuchtpunkt | Blatt: Block, Leuchtfront | Blatt: Rahmen mit Öffnung, quer | Blatt: Reflex-Haube, quer |

**Ergebnis:** 6 Blätter passen (alle Scharfschützengewehre), zwei sind nahe dran (KH06, KH07), 46 weichen als Blatt ab. Bei keinem Blatt
weicht nur die Kennung ab; bei KG02 und KH07 weicht die Kennung zusätzlich zur Form ab. Die Bögen haben kein Ziel; dort sitzen Pin und
Leuchtpunkt quer (KD10, KF10, KG10, KH10, KJ10).

**Korrektur zu claude-0.5:** 19 der 46 Blätter haben ein Fenster quer zur Laufachse: KD01 KH01 KJ01 KD02 KG02 KH02 KJ02 KD03 KJ03 KD04 KG04
KH04 KF06 KD07 KJ07 KJ09 KC09 KH09 und KJ06. Der Richtungstest von 0.5 hat das nicht gefunden. Er wertet Scheiben auf den Seitenflächen
als Leuchtstreifen und nicht als Fenster, und offene Ringe ohne Leuchtteil prüft er gar nicht; nur KF10 schlägt an. Der Test wird erst
nach der Entscheidung erweitert, sonst stünden 19 bekannte Befunde in der Ausnahmeliste.

**Toolgen** (`data/tools.json` › `hold.sight_kind`, c926f50) weicht ebenfalls vom Ziel ab: Pistole, Schrotflinte und Raketenwerfer
`iron`, Impulsgewehr `holo`, Spurgewehr `scope`.

## Vorschlag Vokabular (additiv, nichts umbenennen)

- **`sight.type`**: die neun Typen des Typen-Blatts: `standard`, `holo`, `precision`, `reflex`, `sniper`, `machine`, `energy` (aktiver
  Energierahmen), `trace` (Zielverfolgung und Markierung), `rocket`. Für Blätter ohne Ziel kommen `iron` und `pin` dazu. Ziel je Waffe:
  1 `reflex` (kompakt), 2 `holo`, 3 `precision`, 4 `reflex` (Weitwinkel), 5 `sniper`, 6 `machine`, 7 `energy`, 8 `trace`, 9 `rocket`.
- **`sight.frame`**: Rahmen-Varianten des Blatts: `standard`, `compact`, `open`, `closed`, `industrial`, `lightweight`.
- **`kind`** bleibt Toolgens `hold.sight_kind` und wird aus `type` abgeleitet: precision/sniper → `scope`, holo/trace/rocket → `holo`,
  reflex/standard/machine → `reflex`, energy → `energy`. `window` folgt: precision/sniper → `lens`, sonst `glass`.
- Lenswork (`window`-Form und -Maße, `glass_tint`, `reticle_anchor` / `Socket_Reticle`) kommt danach als eigener Block. Das ist der
  nächste Schritt nach der Entscheidung.

## Abgleich mit Toolgen (nur gelesen, c926f50)

- **Element**: alle neun Waffentypen stimmen mit `surface_recipes.json` › `glow.element` und `tools.json` überein (kein kinetic).
- **`textures`**: `brushed`, `knurl` und `grain` sind Toolgen-`patterns`. `grooves` und `seams` nutzt der Spec nicht; die Skin-Rippen
  verweisen auf `lamellae` (`toolgen_similar`). Alle Größen sind in mm. Toolgens Reliefgrenze `max_height_mm` 0,3 betrifft den Spec nicht,
  weil er keine Höhen enthält.
- **Material**: Die Spec-IDs `painted`, `brushed` und `rubber` haben dieselben Namen wie in Toolgen. `matte` entspricht `painted_matte`,
  `lit` entspricht `energy_glass`, die Skin-Oberflächen `polished_gold`/`polished_chrome` entsprechen `polished`. `ceramic`, `satin` und
  `rough_cast` kommen im Spec nicht vor. Vorschlag (additiv): `parts[].toolgen_material`.
- **Decals**: `decals.json` ist ein Katalog mit 14 Masken-IDs (z. B. `symbol_diamond`, `hazard_stripes`, `tech_lines`) und einer
  Strichschrift. Die Decals im Spec sind Flächen ohne ID, die Skin-Glyphen eigene Formen (Segmentziffern, Runen). Gemeinsame IDs gibt es
  nicht, und automatisch zuordnen lassen sie sich auch nicht. Eine Zuordnung (`decals[].toolgen_decal`) bräuchte eine Entscheidung je
  Waffe.

## Frage an den Nutzer

Gelten für Toolgen künftig nur die neuen Visier-Blätter (Paket 2, VS01–VS09) als Visier-Zielbild, während die Visiere auf den 60
Waffenblättern bleiben, wie sie sind (mit Verweis), oder sollen die Waffenblätter danach auf die neuen Visiere umgestellt werden?
