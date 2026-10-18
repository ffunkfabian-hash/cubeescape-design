# A · Parallax

Zehn eigenständige Codex-Entwürfe aus dem früheren Parallax-Stand, nun auf Wunsch des Nutzers mit dem aktuellen
Blatt-, Material-, Skin- und Referenzdatenumfang überarbeitet. Die Formen stammen ausschließlich aus der eigenen
Codex-Historie (`f5a7fde`); keine Übernahme aus Claudes Generator.

[Galerie](output/index.html) · [Probeblätter](probe/index.html) · [Versionsbericht](../docs/versions/0.1.md)

Die Modelle bleiben unter `models/`; gemeinsame eigene Codex-Werkzeuge liegen unter `../fluxbloom/`.
Auf dem Mac unter heavy_lock: `python ../fluxbloom/build.py --collection parallax`.
Mit `--probe` entstehen zunächst Pistole, Fusionsgewehr, Spurgewehr und Bogen. Abhängigkeiten und Prüfbefehle:
[gemeinsame Pipeline](../fluxbloom/README.md).

Die Specs sind eigenständige gestalterische Referenzen, kein bestätigter Toolgen-Importvertrag. Maße und Anker
sind nachvollziehbar ausgewiesen; CE-Roboterpassung ist ohne Modelltest unbekannt.

## 0.1.2 · Stilvertrag und Texturkatalog

Gleiche zeichnerische Regeln und gemeinsamer Katalog wie Flux Bloom, ohne Änderung der ursprünglichen Modelle,
Paletten oder Namen. Kanonische Übergabe: `output/KAxx.spec.json` im Weapon-Spec-v1-Format plus `golden.json`.
Befehle und Grenzen: [gemeinsame Pipeline](../fluxbloom/README.md#stilvertrag-weapon-spec-v1-und-gemeinsamer-katalog).
