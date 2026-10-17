# cubeescape-design

Waffen-Konzeptblätter für **Cube Escape**: Low-Poly-Sci-Fi, technisch konsistent, als Vorlage für 3D-Modellierung
(Mensch oder KI-Agent). Jede Waffe ist als kleines 3D-Modell in Python beschrieben. Alle Ansichten werden aus genau
diesem Modell gerendert und sind damit garantiert deckungsgleich.

Verbindliche Gestaltungsregeln: [`docs/masterprompt.md`](docs/masterprompt.md) (Concept-Art-Qualitäts-Masterprompt).

## Inhalt eines Konzeptblatts (4800 × 3400)

- Isometrische Hauptansicht **ohne Visier**, mit höchstens 8 deutschen Bauteil-Beschriftungen
- Sechs orthografische Ansichten (links, rechts, vorne, hinten, oben, unten) im gleichen Maßstab mit Bezugslinien
- Detail Abzugsbereich von schräg unten
- **Visier separat**: Optik ist ein modulares Anbauteil; auf der Waffe bleibt nur die Visierschiene
  (bei Raketenwerfern seitlich links am Rohr)
- Material & Texturen im Objektraum (lackiert, gebürstet, gummiert, matt, beleuchtet) mit Musterfeldern
- Vier Farbvarianten derselben Geometrie (Basis, Cube Escape Standard, Arktis, Nacht)
- Prompt auf Deutsch und Englisch

## Varianten

| Variante | Idee |
|---|---|
| C | Neue Formen der Originalwaffen, je eigene Palette |
| D | Originalformen, konstruktiv überarbeitet, Farbvarianten |
| F | Neue Formen, mutige Paletten |
| G | Neue Formen in der Cube-Escape-Farbwelt (Creme, Anthrazit, Orange, Cyan) |
| H | „Werkstatt-Serie“: modulare Prototypen mit Klemm-/Schraubverbindungen |

Waffen je Variante: Pistole, Sturmgewehr, Impulsgewehr, Schrotflinte, Scharfschützengewehr, Maschinenpistole,
Fusionsgewehr, Spurgewehr, Raketenwerfer, Bogen.

## Struktur

Die Stände sind **nach Erzeuger getrennt**: `claude/` enthält ausschließlich Claudes Pipeline und Konzepte,
`codex/` ausschließlich die von Codex. Gemeinsam ist nur `docs/` (Regeln und Aufträge). Siehe `CLAUDE.md` und `AGENTS.md`.

```
docs/                    gemeinsam: Regeln und Aufträge
  masterprompt.md        verbindliche Qualitätsregeln
  AUFTRAG.md             vollständiger Auftrag für Codex (inkl. Masterprompt)
  prompt-vorlagen.md     Vorlagen für ChatGPT-Bildgenerator und Codex
claude/                  nur Claude
  prompts/               fertige Prompts je Waffe (DE/EN)
  generator/
    eng.py raster.py     Modell-API und Z-Buffer-Toon-Renderer
    views.py xl.py       Karte (2400×1560) und Konzeptblatt XL (4800×3400)
    v01m.py c02–c10.py   Modelle Variante C
    dmods.py dmodels.py  Modelle Variante D
    f01–f10.py g01–g10.py h01–h10.py
    build_*.py           Bauskripte je Variante, build_all.py baut alles
  output/
    sheets/              Konzeptblätter XL (KC01 … KH10) als HTML
    previews/            PNG-Vorschauen
  reference/crops/       Original-Seitenansichten (Referenz für Variante D)
codex/                   nur Codex (eigene Pipeline, eigene Konzepte)
```

## Einrichten und bauen

```bash
pip install -r requirements.txt
playwright install chromium        # nur für Screenshots / Vorschauen
python claude/generator/build_all.py      # alles neu bauen (dauert, die XL-Blätter sind groß)
python claude/generator/build_all.py G H  # nur bestimmte Varianten
```

Die HTML-Dateien binden Schriften über Google Fonts ein; ohne Internet erscheinen Ersatzschriften.
`claude/output/sheets/*.dc.html` sind Canvas-Artboards; zum Ansehen im Browser die Zeile
`<script src="./support.js"></script>` ignorieren bzw. entfernen.

## Modell-API (Kurzfassung)

Koordinaten: x = Längsachse (Mündung +x), y nach unten, z = Breite (z+ = linke Waffenseite).

```python
from eng import *
m = Model()
m.prism(profil_xy, farbe, z0, z1, r=8); label(m, 'Gehäuse')   # extrudiertes Seitenprofil, gerundete Ecken
m.cyl(x0, x1, y, z, radius, farbe);     label(m, 'Lauf')      # Zylinder entlang x
m.decal('z+', z, punkte, farbe, emit=True)                     # Detail auf einer Fläche (beidseitig)
m.prism(...); sight(m)                                          # Visierteil -> wird separat gezeichnet
```

Regeln (aus dem Masterprompt): Abzug mit Bügel auch in der Isometrie sichtbar, Magazin im Schacht, sichtbarer Lauf,
keine schwebenden Teile, keine ungewollten Durchdringungen (koplanare Teile ≥ 1 Einheit versetzen), max. 8 Labels.

## Mit Codex weiterarbeiten

`docs/AUFTRAG.md` enthält den kompletten Auftrag inklusive Masterprompt. In Codex: „Lies docs/AUFTRAG.md vollständig“
– für neue Varianten eine eigene Pipeline unter `codex/` anlegen (Claudes Dateien unter `claude/` nicht verändern).

## Bekannte Grenzen

- Texturen sind prozedurale Muster für Konzeptblätter, keine UV-Texturen.
- Farbvarianten werden automatisch nach Bauteil-Rollen umgefärbt; einzelne Akzente können an ungewohnter Stelle landen.
- Gestalterische Referenz, keine bemaßte Fertigungszeichnung.

## Parallax · eigenständiger Codex-Stand

Unter [`codex/parallax/`](codex/parallax/README.md) liegt die unabhängig gebaute Pipeline 0.1 „Parallax“ mit zehn Modellen, lokal eingebetteten Schriften, selbstständigen HTML-Blättern und 22 Unit-Tests. Einstieg: [`codex/parallax/output/index.html`](codex/parallax/output/index.html). Diese Fassung besitzt ihre eigene Modell-API und ergänzt die bestehenden Varianten.

```bash
python -m unittest discover -s codex/parallax/tests -v
python codex/parallax/build.py
```

Die Stände bleiben nach Erzeuger getrennt: `generator/` enthält Claudes bestehende Pipeline; `codex/parallax/` enthält ausschließlich den Codex-Stand samt eigenen Modellen, Prompts und Konzeptblättern. Es gibt keine gemeinsam beschriebenen Generatordateien.
