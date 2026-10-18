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

Teil D (18.10.2026): Waffen 1–9 tragen eigenständig rekonstruierte VS01–VS09 nach den Sight-Specs;
Bögen behalten ihren rückseitig leuchtenden Pin. Bildnachweise und Grenzen stehen im Versionsbericht.
Mac-Prüfweg unter `heavy_lock`: `python codex/fluxbloom/vs_build.py`, danach `--full`.
`--capture-engine rsvg` ist ein expliziter SVG-Ersatz bei gesperrtem Chromium und bestätigt keine Browser-QA.


## 0.1.5 · Texturprofil

Die Waffen 1–9 tragen sechs Profilkacheln unter der Materialansicht: Gehäuse, Metall, Gummi,
Energie, Kantenabnutzung und Toolgen-Decals. Der Spec enthält dieselben Typvorgaben als
`texture_profile`; der Bogen bleibt unverändert ohne Profil. Die Kacheln sind eine schematische
Materiallegende für den Abnehmer, die Muster darüber zeigen weiterhin echte Modellteile.
Bildbau und Prüfwerte: `python codex/fluxbloom/texture_profile_build.py --full` unter `heavy_lock`.
Siehe [Versionsbericht](../docs/versions/0.1.md).
