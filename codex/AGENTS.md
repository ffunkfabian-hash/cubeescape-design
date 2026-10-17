# Codex-Zuständigkeit

Globale Regeln und die AGENTS.md im Repository-Wurzelordner gelten. Nur unter `codex/` schreiben.
Keine Dateien aus `claude/` übernehmen, verändern oder per Symlink einbinden. Gemeinsame Vorgaben in `docs/` nur lesen.
Bildläufe auf dem Mac mit heavy_lock; Tests und Syntax sind die schnellen Prüfungen.

Aktuell codex-0.2, Variante K „Flux Bloom“, und codex-0.1, Variante A „Parallax“, Branch `codex/flux-bloom`.
Nutzerauftrag vom 17.10.2026: Auch Parallax nach dem aktuellen Claude-Maßstab überarbeiten.
Beide Modellserien bleiben getrennt, die eigenen Codex-Werkzeuge für Raster, Skins, Layout und Spec werden gemeinsam genutzt.
Der Renderer und allgemeine Bausteine stammen aus dem früheren eigenen Codex-Werkzeug; die zehn Konzepte sind neu.


## Verbindlicher Maßstab: aktueller Claude-Stand

Entscheidung des Nutzers, 17.10.2026: Bestehende und zukünftige Codex-Designs/Varianten richten sich nach Claudes
jeweils aktuellem Qualitäts- und Funktionsstand – ausdrücklich einschließlich Aufbau, Materialien und Texturen.
Vor neuen Varianten oder Überarbeitungen den aktuellen `main`-Stand, die gemeinsamen Vorgaben in `docs/` und die
relevanten Entscheidungen/Versionsberichte unter `claude/docs/` lesen. Den zugehörigen verfügbaren Bildstand getrennt
vom Stand der Spec-/Code-Daten benennen. Keine Dateien aus Claudes Pipeline übernehmen oder gemeinsam beschreiben.

- **Waffenkonstruktion:** Funktionsbereiche klar gliedern; individuelle Silhouetten, plausible Größenverhältnisse,
  erkennbare Halter, Klemmen, Gehäusenähte, Griff-/Kontaktflächen und saubere Übergänge. Griff, Schaft und Visier
  passend zur Waffenklasse ausarbeiten; die Serie nicht nur durch Farbe und Frontaufsatz unterscheiden.
- **Blattaufbau:** Claudes Informationsumfang und Lesbarkeit erreichen: große Hauptisometrie ohne montierte Optik,
  lesbare deutsche Etiketten, sechs Orthos mit gleichem Maßstab/Bezugspunkt, Abzugs-/Griffdetail (beim Bogen auch
  Pfeilauflage), getrennte Optik mit Haltern, Material-/Texturansicht, Farbvarianten, Skin-/Musterfelder und DE-/EN-Prompts.
  Freie Fläche, Konturen und Linienführung so nutzen, dass die verkleinerte Ansicht gut lesbar bleibt.
- **Materialien und Texturen:** Werkstoffe durch passende Oberflächen und funktionale Details trennen; lackiertes und
  gebürstetes Metall, Griffgummi, matter Kunststoff und funktionale Leuchtteile nachvollziehbar zuordnen. Objektfeste
  Texturen, nachvollziehbare Materialkanäle und reproduzierbare Parameter verwenden; Materialfelder müssen die tatsächlich
  verwendeten Materialien abbilden.
- **Skins und Muster:** Claudes dokumentierten Umfang als Maßstab verwenden: fünf entworfene Skins je Waffe, mit
  Farbflächen, Glyphen/Zahlen/Emblemen, Streifen/Verläufen/Ringen, Gold-/Chrombereichen samt Kantenabnutzung sowie
  Rippen/Finnen. Funktionale Lesbarkeit erhalten. Hauptskin im großen Bild und Skin-/Musterfelder im Blatt sichtbar
  machen; reine Palettenumfärbung nicht als vollständigen Skin ausgeben. Kanalzuordnung nach den dokumentierten
  sieben MT_-Kanälen und zwei Skin-Akzenten ausarbeiten, ohne eigenmächtig neue gemeinsame Verträge zu definieren.
- **Optik und Übergabedaten:** Nutzer-Zielbild und bekannte Befunde berücksichtigen, insbesondere Spurgewehr mit Fenster
  und Markierungsrahmen statt Röhre. Maßstab, Einheiten, Achsen, benannte Halte-/Mündungs-/Visierpunkte, Material-/Skin-
  Angaben und gegebenenfalls bewegliche Teile sowie `robot_fit` so explizit dokumentieren, dass nachfolgende Modellierung
  nichts erraten muss. Ungeprüfte Eignung für Toolgen oder den CE-Roboter nicht behaupten.
- **Abnahme:** Zuerst repräsentative Probeblätter mit direktem Claude-Vergleich erstellen und nach dem dort dokumentierten
  Probe-/Freigabeablauf beurteilen; anschließend die Serie ausarbeiten. Tests plus visuelle Prüfung der Konstruktion,
  Details, Texturen, Skins und des gesamten Blatts. Bildläufe nur auf dem Mac unter heavy_lock; MP4 nur auf Nutzerwunsch
  entsprechend der projektspezifischen Entscheidung. Claudes bekannte Fehler sind keine Vorlage zum Nachbauen.
- **Auslieferung:** Eigenständigen Codex-Viewer/Galerie pflegen. Claudes Vorgaben zur Größe und Auslieferung berücksichtigen
  (lokale Schriften mit Lizenz, WebP-Qualität 60, erzeugte Blätter/Vorschauen als Auslieferungsartefakte, keine automatische
  Aufnahme großer generierter Dateien in Commits). Wurzeldateien und gemeinsame Docs nur gemäß den Zuständigkeiten ändern.

Parallax 0.1.1 und Flux Bloom 0.2.1 wurden nach diesem Umfang überarbeitet und auf dem Mac geprüft.
Prüfbelege und Grenzen stehen in den Versionsberichten; eine pauschale gestalterische Gleichwertigkeit oder
Toolgen-/Roboter-Eignung wird daraus nicht abgeleitet.
