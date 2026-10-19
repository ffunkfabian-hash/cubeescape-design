# A · Parallax

25 eigenständige Codex-Entwürfe mit aktuellem Blatt-, Material-, Skin- und Referenzdatenumfang.
Die zehn Bestandsformen stammen aus der eigenen Codex-Historie (`f5a7fde`),
Typen 11–25 wurden neu konstruiert; keine Übernahme aus Claudes Generator.

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
Historischer Abnahmeweg für 0.1.5: `texture_profile_build.py --full`; aktuelle Gesamtprüfung siehe 0.1.6 unten.
Siehe [Versionsbericht](../docs/versions/0.1.md).


## 0.1.6 „Switchcraft“ · 19.10.2026

25 Konzepte je Variante: der bisherige Bestand 01–10 und 15 neue Typen 11–25.
Alle Blätter tragen BEDIENUNG; Weapon-Spec ist Format 2. Das Spurgewehr 08 verwendet
`trace_rifle`; Scout-Gewehr 11 bleibt ohne Toolgen-Anbindung. Die neuen Typen haben
`toolgen_id: null`, `toolgen_status: not_connected`, `element: null` und vorgeschlagene
Bewegungen; ihre Texturprofile sind ausdrücklich „Vorschlag, abgeleitet“.

Reproduzieren (Mac, unter `heavy_lock`):
`python codex/fluxbloom/switchcraft_build.py --family parallax`.
Nur Specs: `python codex/fluxbloom/build.py --collection parallax --spec-only`.
Gemeinsame Schema-/Richtungsprüfung: `python codex/fluxbloom/validate_specs.py`.
Historische Zehner-Regression: `load_collection(..., include_new=False)`; Bildbau und
Spec-Export verwenden ausdrücklich `include_new=True`.
Belege, Abnahmestand und Grenzen stehen im [Versionsbericht](../docs/versions/0.1.md).
