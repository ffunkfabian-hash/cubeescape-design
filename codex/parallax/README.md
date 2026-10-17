# Cube Escape Design · 0.1 Parallax

Eigenständige Python-Pipeline für zehn Low-Poly-Waffen-Konzeptblätter. Keine Unity-, Blender- oder Cube-Escape-Code-Abhängigkeit.
Vorgesehenes Repository: [ffunkfabian-hash/cubeescape-design](https://github.com/ffunkfabian-hash/cubeescape-design)
(Angabe des Nutzers, 17.10.2026).

## Analyse vor dem Bau

Die Anforderung ist eine unabhängige gestalterische Referenz aus einem konsistenten 3D-Modell je Waffe.
Geometrie, CPU-Rasterizer, Modellmodule, Layout und Build sind getrennt. Farbvarianten ändern ausschließlich
Materialrollen. Die Daten werden nicht ins Spiel importiert; Spielstände, IDs, Formate und Spielmodelle bleiben unberührt.
Der [gemeinsame Masterprompt](../../docs/masterprompt.md) ist die verbindliche Gestaltungs- und Prüfreferenz;
[masterprompt.md](masterprompt.md) bewahrt die beigefügte Ausgangsreferenz.
[Versionsbericht 0.1](../docs/versions/0.1.md).

## Installation und Bau

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python build.py
```

Dann [output/index.html](output/index.html) öffnen. Jedes der zehn HTML-Blätter ist selbstständig und enthält
transparente WebP-Renderings als SVG-Bilder sowie die lokalen Schriftarten Chakra Petch, Barlow und JetBrains Mono.
Es braucht weder einen Server noch Netzwerkzugriff. OFL-Lizenzen liegen neben den Schriften in `fonts/`.

`--weapon sniper` wählt ein Modell (wiederholbar), `--output <Ordner>` bestimmt das HTML-Ziel,
`--screenshots <Ordner>` das Bildziel. `--capture-only` fotografiert vorhandene Blätter erneut.
Die vollständigen deutschen und englischen Prompts stehen auch in `output/<waffe>-prompts.txt`.

Die PNGs sind 4800 × 3400 Pixel groß. Verkleinerte Vorschauen und ein Kontaktbogen liegen daneben.
Standard-Bildziel: `~/Library/Caches/CubeEscapeDesign/concept-sheets/0.1.0/`.
Playwright und Chromium sind installiert; der im Auftrag erlaubte alternative Pillow-Blattaufbau wird nicht benötigt.

## Modell-API

Ein Modell ist eine Liste von `Part`-Objekten mit Polygonflächen, Weltnormalen, Farbe, Leuchtflag,
Material, Farbrolle, Beschriftung und Optik-Markierung. Achsen: x zur Mündung, y nach unten, z zur linken Seite.
Maße sind abstrakte Designeinheiten, keine realen Fertigungsmaße.

```python
from eng import prism, cyl, label, sight
model = [prism([(0, 0), (50, 0), (45, 20), (0, 20)], '#D5CCB8', -10, 10, r=2)]
label(model, 'Gehäuse')
model.append(cyl(40, 80, 8, 0, 4, '#858F99'))
label(model, 'Lauf')
# sight(model) marks the last part for separate optic views.
```

`decal(plane, value, points, color, emit=False)` erzeugt flache Details. Teile werden explizit an das Modell angehängt.
`models/common.py` ergänzt offene Rohrschalen, Verbindungen, offene Abzugsbügel und modulare Optiken.
Die acht Pflicht-Beschriftungen sind Gehäuse, Griff, Abzug, Magazin, Lauf, Mündung, Schaft und Visierschiene;
der Bügel ist zusätzlich vorhanden. Der Bogen nutzt eine fiktive magnetische Pfeilführung, deren Führung und
Auslass als Lauf/Mündung bezeichnet sind. Der Raketenwerfer besitzt eine links versetzte Schiene und eine freie Bohrung.

## Darstellung und Qualitätskontrolle

`raster.py` projiziert orthografisch, rotiert zuerst yaw um y, dann pitch um x in der y-nach-unten-Konvention
(positiver Pitch sieht die Oberseite). Er verwendet Polygonmasken und Ebenentiefe im Z-Buffer mit 2× Supersampling je Achse,
vier Lichtstufen und Konturen aus Flächen-IDs. Weiche Rundungsflächen teilen ihre Kontur-ID.
Leuchtteile bleiben ungeschattet; ihre weiche Aura ist auf 30 % Deckkraft begrenzt.
Die deterministischen Materialtexturen werden in Objektkoordinaten berechnet.

Die sechs Orthoansichten teilen Maßstab und Welt-Bezugspunkt (Bounding-Box-Mitte). Hauptansicht, Abzugsdetail,
getrennte Optik und Farbvarianten können zur Lesbarkeit andere Maßstäbe besitzen.
Haupt- und Orthoansichten zeigen die Waffe ohne Optik; die Schiene bleibt montiert.
Die vier Farbpaletten ändern dieselbe Geometrie nach Rollen: primär, mittel, dunkel und Akzent.

Die Unit-Tests prüfen Geometrieverträge, Achsen, Z-Verdeckung, konkave Profile, Anker, Materialtexturen und Paletten.
Der Build prüft Geometrie und Pflichtteile, nimmt jedes Blatt mit Chromium auf und prüft Seitenmaße und Textgrenzen.
`output/manifest.json` enthält die Prüfdaten, Geometrie-Hashes und gemeinsamen Ortho-Maßstäbe.
Die automatische Prüfung ersetzt nicht die Sichtprüfung aller Ansichten nach Abschnitt 12 des Masterprompts.
Die Ergebnisse sind gestalterische Referenzen, keine Fertigungs-, Kollisions- oder Belastungsfreigabe.

## Rechnerweite Abstimmung

Das Projekt selbst benötigt keine CE-Werkzeuge. Auf diesem Mac werden schwere Bildläufe optional mit der vorhandenen
rechnerweiten `heavy-run.lock` serialisiert. Diese Abstimmung ist eine Maschinenregel, keine Projektabhängigkeit.
