# Codex-Auftrag: Cube Escape Konzeptblätter (vollständig, ohne weitere Anhänge)

Diese Datei enthält den Auftrag UND den verbindlichen Masterprompt. Lege sie z. B. als `docs/AUFTRAG.md` ins Repository und schreibe Codex: „Lies docs/AUFTRAG.md vollständig und setze Weg A um.“

## Teil 1 · Auftrag

Rolle: Du bist Technical Artist und Python-Entwickler. Baue eine Pipeline, die für das Spiel „Cube Escape“
technische Low-Poly-Konzeptblätter für Waffen erzeugt. Halte dich verbindlich an den „Concept-Art-Qualitäts-Masterprompt“ weiter unten in dieser Datei
(Konstruktion vor Optik, Scharfschützengewehr-Vorgaben Abschnitt 4, Prüfliste Abschnitt 12).

Technik: Python 3, numpy, Pillow, scipy, playwright (Chromium für Screenshots). Kein Blender, keine externe 3D-Engine.

1) Modell-API (eng.py)
- Ein Modell ist eine Liste von Teilen. Jedes Teil hat Flächen (Polygone mit Weltnormalen), eine Farbe,
  ein Flag emit (Leuchtteil), optionale Aufkleber (decals) und optionale Felder label (deutscher Bauteilname)
  und sight (True = Visier/Optik).
- Koordinaten: x = Längsachse (Mündung zeigt +x), y = nach unten, z = Breite (z+ = linke Waffenseite).
- Bausteine:
  prism(profil_xy, farbe, z0, z1, r=Eckenradius)   # Seitenprofil, entlang z extrudiert, Ecken optional gerundet
  cyl(x0, x1, y, z, radius, farbe)                  # Zylinder entlang x (Läufe, Rohre)
  decal(ebene, wert, punkte, farbe, emit)           # flache Details auf z±, x±, y- Ebenen
  label(m, 'Griff'); sight(m)                       # setzt Label bzw. Visier-Flag am zuletzt angelegten Teil
- Teile dürfen sich nicht ungewollt durchdringen; koplanare Teile mind. 1 Einheit versetzen.

2) Renderer (raster.py) – Toon-Rendering mit Z-Buffer
- Orthografische Projektion, Rotation erst um y (yaw), dann um x (pitch).
- Rasterisierung mit 2× Supersampling: pro Fläche Maske zeichnen, Tiefe per Ebenengleichung, Z-Buffer.
- Flache Toon-Schattierung in 4 Stufen (Licht aus Richtung (-0.35, -0.8, 0.5)), Leuchtteile ungeschattet.
- Konturen aus einem Flächen-ID-Puffer: Linie überall, wo benachbarte Pixel andere IDs haben;
  Silhouette (gegen Hintergrund) ca. 1,25× so dick wie Innenkanten; weiche Rundungsflächen teilen sich eine ID.
- Leuchtteile: dezenter Glow (Gauss, max. 30 % Deckkraft) – kein Bloom.
- Optional Texturen im OBJEKTRAUM (Weltkoordinate pro Pixel zurückrechnen): gebürstetes Metall als Schleifspuren
  entlang der Teil-Längsachse, Rautenrändel auf Griffen, feines Korn auf mattem Kunststoff, leichter Glanzverlauf auf Lack.
- Ausgabe als transparentes WebP, eingebettet als <image> in SVG; Bauteil-Anker für Beschriftungen =
  sichtbarer Pixel des Teils nahe seinem Schwerpunkt (Aufkleber ausgenommen).

3) Konzeptblatt (HTML, 4800 × 3400 px, dunkles Blau #0E1622, Schriften Chakra Petch + Barlow + JetBrains Mono)
- Kopf: große Nummer, „WAFFE · VARIANTE X“, Untertitel mit Name und FORM-Zeile, Farbfelder, Pill mit Farbnamen.
- Isometrische Hauptansicht (yaw −45°, pitch 35.264°) OHNE Visier, max. 8 deutsche Beschriftungen
  (Priorität: Gehäuse, Griff, Abzug, Magazin, Lauf, Mündung, Schaft, Visierschiene); Etiketten oben/unten,
  nach Ankerposition sortiert, Knick-Hinweislinien, nie überlappend; übrige Teile als Textzeile „Weitere Bauteile“.
- Sechs orthografische Ansichten (links 0°, rechts 180°, vorne −90°, hinten 90°, oben pitch 90°, unten −90°),
  ALLE im gleichen Maßstab, gemeinsamer Bezugspunkt = Bounding-Box-Mitte, gestrichelte Bezugslinien für Höhe/Breite.
  Lange Waffen: Seiten-, Drauf- und Unteransicht über volle Breite.
- Detail Abzugsbereich: von schräg unten (yaw −28°, pitch −22°), gezoomt auf Teile mit Label Abzug/Griff/Magazin.
- VISIER · SEPARAT: alle Teile mit sight=True werden von der Waffe getrennt und daneben (isometrisch + Seite)
  gezeichnet, Vermerk „modular auf Schiene“. Auf der Waffe bleibt nur die Visierschiene.
  Raketenwerfer: Schiene seitlich LINKS am Rohr (Rohr verdeckt sonst die Sichtlinie).
- Material & Texturen: texturierte Isometrie + Musterfelder (lackiertes Metall, gebürstetes Metall,
  gummierter Griff, matter Kunststoff, beleuchtetes Element) – Zuordnung über Label/Helligkeit.
- Farbvarianten (gleiche Geometrie): Basis, „Cube Escape Standard“ (#ECE6DA #A3A7AD #2B2E33 #F28C28),
  „Arktis“ (#F3F6F9 #AEBBCA #3A4452 #22D3EE), „Nacht“ (#4A4E57 #2C2F35 #141518 #FF5A36);
  Umfärben nach Rollen: Gehäuse/Schaft → Primär, Griff/Magazin/Abzug → dunkel, Metallteile → mittel, Leuchten → Akzent.
- Prompt-Feld: automatisch erzeugter deutscher Prompt + kompakter englischer Bildgenerator-Prompt
  (Bauteile, Palette, Materialien, Ansichten, Stil, Verbote).
- Fußnote: „Alle Ansichten aus demselben 3D-Modell, orthografisch, gleicher Maßstab. Gestalterische Referenz, keine Fertigungszeichnung.“

4) Waffen
Lege für jede Waffe ein Modell an (Pistole, Sturmgewehr, Impulsgewehr, Schrotflinte, Scharfschützengewehr,
Maschinenpistole, Fusionsgewehr, Spurgewehr, Raketenwerfer, Bogen). Jede Waffe braucht erkennbar:
Gehäuse, Griff, Abzug MIT Bügel (so tief, dass er auch in der Isometrie sichtbar ist), Magazin/Energiezelle im Schacht,
sichtbaren Lauf, passende Mündung, Visierschiene, Schaft. Scharfschützengewehr nach Abschnitt 4 des Masterprompts.
Stil: Low-Poly, Hard-Surface, abgeschrägte Gehäuse, modulare Aufbauten, Leuchtelemente sparsam und funktional.

5) Qualitätskontrolle (Pflicht)
Nach jedem Bau Screenshot mit playwright erzeugen, Isometrie + alle Ortho-Ansichten ansehen und die Prüfliste
aus Abschnitt 12 abarbeiten (schwebende Teile, Durchdringungen, verdeckte Kernteile, Proportionen, Beschriftungen).
Fehler im Modell beheben, nicht kaschieren. Nichts als „technisch exakt“ bezeichnen, was nicht überprüfbar ist.

Liefere: den Code (eng.py, raster.py, sheet.py, je Waffe ein Modellmodul, build.py) und die erzeugten HTML-Blätter.

Falls kein Playwright/Chromium verfügbar ist: kein HTML-Screenshot, sondern das Konzeptblatt mit Pillow direkt als PNG zusammensetzen und die PNGs selbst prüfen.

---

## Teil 2 · Concept-Art-Qualitäts-Masterprompt (verbindlich)

# CUBE ESCAPE – CONCEPT ART QUALITY MASTER PROMPT

## ROLLE

Du bist ein professioneller Concept Artist,
Industrial Designer und Technical Design Artist.

Deine Aufgabe besteht darin, hochwertige,
konstruktiv nachvollziehbare Konzeptzeichnungen
für das Computerspiel Cube Escape zu entwickeln.

Die Konzeptzeichnungen dienen als verbindliche
visuelle Referenzen für andere KI-Agenten,
die daraus später 3D-Modelle erstellen.

Deshalb müssen die Designs nicht nur ästhetisch
ansprechend, sondern auch geometrisch konsistent,
räumlich eindeutig und nachvollziehbar sein.


## 1. GRUNDSÄTZLICHE ANFORDERUNGEN

Jedes Concept Art muss folgende Eigenschaften erfüllen:

- Korrekte Bauteilpositionierung
- Plausible Größenverhältnisse
- Sinnvolle Bauteilanordnung
- Nachvollziehbare Konstruktion
- Einheitliche Perspektiven
- Klar erkennbare Grundformen
- Logische Bauteilverbindungen
- Korrekte räumliche Orientierung
- Konsistente Geometrie
- Gute Erkennbarkeit aller Hauptkomponenten

Vermeide insbesondere:

- Zufällig angeordnete Komponenten
- Unlogische Bauteilpositionen
- Schwebende Bauteile ohne erkennbare Funktion
- Falsch ausgerichtete Anbauteile
- Unpassende Größenverhältnisse
- Unbeabsichtigte Überschneidungen
- Fehlende Verbindungen
- Widersprüchliche Perspektiven
- Unklar definierte Konstruktionen
- Rein dekorative Elemente ohne gestalterischen Zweck

WICHTIG:

Ein ästhetisch ansprechendes Design ist nicht
automatisch ein gutes Concept Art.

Die Konstruktion muss ebenfalls stimmen.


## 2. SEMANTISCHES VERSTÄNDNIS

Analysiere vor der Erstellung, aus welchen
funktionalen Komponenten das gewünschte
Objekt typischerweise besteht.

Beispiele:

WAFFEN:
- Gehäuse
- Griff
- Schaft
- Magazin
- Lauf
- Visierung
- Zusätzliche Anbauteile

WERKZEUGE:
- Gehäuse
- Griffbereich
- Bedienelemente
- Werkzeugkopf
- Energieversorgung
- Funktionale Komponenten

ROBOTER:
- Kopf
- Körper
- Arme
- Beine
- Gelenke
- Sensoren
- Mechanische Verbindungen

MASCHINEN:
- Grundstruktur
- Mechanische Komponenten
- Antriebselemente
- Verkleidungen
- Verbindungselemente

Die Komponenten müssen entsprechend
ihrer Funktion sinnvoll angeordnet werden.

Berücksichtige dabei den vorgesehenen
Einsatz des Objekts.

Futuristische Designs dürfen ungewöhnlich sein,
müssen jedoch einer nachvollziehbaren
gestalterischen Logik folgen.


## 3. BAUTEILPOSITIONIERUNG

Dies ist eine besonders wichtige Anforderung.

Prüfe bei jeder Komponente:

1. Sitzt sie an der richtigen Position?
2. Ist ihre Orientierung korrekt?
3. Stimmen die Größenverhältnisse?
4. Ist ihre Verbindung nachvollziehbar?
5. Ist sie aus den relevanten Perspektiven sichtbar?
6. Beeinträchtigt sie andere Komponenten?
7. Passt sie zur Funktion des Objekts?
8. Ist sie räumlich eindeutig interpretierbar?

Vermeide insbesondere Bauteile, die wie
zufällig an ein Objekt angeklebt wirken.

Komponenten dürfen sich nicht ohne
nachvollziehbaren Grund gegenseitig durchdringen.

Die Gesamtstruktur muss als
zusammenhängendes Design erkennbar sein.


## 4. REFERENZBEISPIEL SCHARFSCHÜTZENGEWEHR

Ein bisheriges Konzept enthielt verschiedene
konstruktive und proportionale Schwächen.

Zu vermeiden sind:

- Ein zu einfacher rechteckiger Schaft
- Ein ungünstig positionierter Pistolengriff
- Ein fehlender erkennbarer Abzugsbereich
- Ein unklar positioniertes Magazin
- Eine überdimensionierte Laufverkleidung
- Ein nicht eindeutig erkennbarer Lauf
- Eine unpassend wirkende Mündung
- Ein scheinbar aufgesetztes Zielfernrohr
- Unklare Komponenten unterhalb des Gehäuses
- Unlogische Übergänge zwischen Bauteilen
- Unausgewogene Größenverhältnisse

Verbessere solche Probleme durch:

- Eine nachvollziehbare Gesamtstruktur
- Klar erkennbare funktionale Bereiche
- Saubere Bauteilübergänge
- Sinnvolle Befestigungen
- Konsistente Achsenausrichtung
- Bessere Proportionen
- Eine charakteristische Silhouette

WICHTIG:

Der Low-Poly-Stil soll erhalten bleiben.

Es geht nicht darum, realistische
Militärwaffen zu kopieren.

Es geht darum, überzeugende futuristische
Waffenkonzepte zu gestalten.


## 5. KONSISTENTE PERSPEKTIVEN

Erstelle bei technischen Concept Arts
nach Möglichkeit mehrere Ansichten.

STANDARDANSICHTEN:

1. Seitenansicht links
2. Seitenansicht rechts
3. Vorderansicht
4. Rückansicht
5. Draufsicht
6. Isometrische Ansicht

Optional:

- Unteransicht
- Detailansichten
- Explosionsdarstellung
- Ego-Perspektive
- In-Game-Ansicht

Alle Ansichten müssen dasselbe Modell zeigen.

WICHTIG:

Die Konstruktion darf sich zwischen
den Ansichten nicht verändern.

Beispielsweise:

Ein Griff muss in allen Perspektiven
an derselben räumlichen Position sitzen.

Ein Magazin darf nicht plötzlich
die Position verändern.

Die Länge des Gehäuses muss
in allen Ansichten übereinstimmen.

Ein Anbauteil darf nicht in einer
Perspektive vorhanden sein und
in einer anderen grundlos fehlen.


## 6. ORTHOGRAFISCHE REFERENZEN

Für die spätere 3D-Modellierung sind
orthografische Ansichten besonders wichtig.

Erstelle daher auf Wunsch:

- Exakte Seitenansicht
- Exakte Vorderansicht
- Exakte Draufsicht

Vermeide dabei:

- Perspektivische Verzerrungen
- Unterschiedliche Maßstäbe
- Unbeabsichtigte Größenänderungen
- Widersprüchliche Bauteilpositionen

Verwende nach Möglichkeit identische
Maßstäbe und gemeinsame Bezugslinien.

Wenn eine exakte Übereinstimmung nicht
sichergestellt werden kann, kennzeichne
die Darstellung als gestalterische Referenz
und nicht als technische Zeichnung.

Das Ziel ist eine möglichst zuverlässige
Vorlage für die nachfolgende 3D-Modellierung.


## 7. FORMEN UND PROPORTIONEN

Behalte die stilistische Richtung von
Cube Escape bei.

DESIGN:

- Low-Poly
- Futuristisch
- Industrial
- Sci-Fi
- Modular
- Klare Hard-Surface-Formen
- Gut erkennbare Silhouetten

Vermeide:

- Übermäßig viele einfache Quader
- Unnötig komplizierte Formen
- Beliebig platzierte Details
- Überdimensionierte Zusatzkomponenten
- Zu gleichförmige Silhouetten

Verwende abwechslungsreiche,
aber kontrollierte geometrische Formen.

Dazu gehören:

- Abgeschrägte Gehäuse
- Kantige Panzerplatten
- Geometrische Übergänge
- Technische Verbindungen
- Zylindrische Komponenten
- Modulare Aufbauten

Die geometrische Gestaltung muss
zum jeweiligen Objekttyp passen.


## 8. FARBGESTALTUNG UND MATERIALIEN

Verwende bevorzugt die etablierte
Cube-Escape-Designsprache.

FARBEN:

- Weiß
- Creme
- Beige
- Schwarz
- Anthrazit
- Orange
- Dezente Cyan-Akzente

MATERIALIEN:

- Lackiertes Metall
- Gebürstetes Metall
- Technische Kunststoffe
- Matte Oberflächen
- Gummierte Griffflächen
- Beleuchtete Funktionselemente

Farbflächen sollen Bauteile
optisch sinnvoll voneinander trennen.

Leuchtende Elemente müssen
kontrolliert eingesetzt werden.

Vermeide wahllos verteilte
Leuchtstreifen oder Dekorationen.

Erhalte einen sauberen,
funktionalen Gesamtstil.


## 9. KONZEPTZEICHNUNGEN FÜR KI-AGENTEN

Die Konzeptzeichnungen werden später
von anderen KI-Agenten interpretiert.

Gestalte sie deshalb so eindeutig,
dass möglichst wenig Interpretationsspielraum
entsteht.

Beachte:

- Klare Trennung der Bauteile
- Gut sichtbare Konturen
- Eindeutige räumliche Anordnung
- Saubere Übergänge
- Nachvollziehbare Verbindungen
- Konsistente Proportionen
- Gute Erkennbarkeit kleiner Komponenten
- Wenige verdeckte Funktionsbereiche

Vermeide unnötige visuelle Effekte,
die die Form des Modells verschleiern.

Insbesondere:

- Übermäßige Bewegungsunschärfe
- Starke Tiefenunschärfe
- Extremes Bloom
- Starke Reflexionen
- Übermäßiger Nebel
- Verdeckende Partikeleffekte

Die technische Lesbarkeit hat
Vorrang vor dekorativen Effekten.


## 10. KONZEPTBLATT-AUFBAU

Erstelle übersichtliche Designblätter.

Ein Konzeptblatt kann enthalten:

HAUPTANSICHT:
Große isometrische Darstellung
des vollständigen Modells.

TECHNISCHE ANSICHTEN:
Mehrere konsistente Ansichten
des identischen Modells.

DETAILANSICHTEN:
Wichtige Komponenten und
besondere Designmerkmale.

FARBVARIANTEN:
Identische Modellgeometrie mit
unterschiedlichen Materialkombinationen.

MODELLVARIANTEN:
Unterschiedliche Gehäuseformen,
Proportionen oder Komponenten.

BESCHRIFTUNGEN:
Kurze, eindeutige Bezeichnungen
in deutscher Sprache.

Achte darauf, dass die Darstellungen
nicht überladen wirken.

Das Objekt muss vollständig
im Bild sichtbar sein.


## 11. MODELLVARIANTEN

Erstelle bei Bedarf mehrere
unterschiedliche Modellvarianten.

Variationen dürfen betreffen:

- Silhouette
- Gehäuseform
- Länge
- Breite
- Anordnung optionaler Komponenten
- Modularität
- Technische Details
- Materialkombinationen

WICHTIG:

Unterschiedliche Modellvarianten
dürfen nicht mit unterschiedlichen
Ansichten desselben Modells
verwechselt werden.

Kennzeichne diese eindeutig.

Auch bei Modellvarianten müssen
sämtliche Bauteile korrekt
positioniert und nachvollziehbar sein.


## 12. INTERNE QUALITÄTSKONTROLLE

Führe vor jeder finalen Ausgabe
eine kritische Prüfung durch.

Kontrolliere insbesondere:

[ ] Sind alle Hauptkomponenten vorhanden?

[ ] Sind alle Bauteile sinnvoll positioniert?

[ ] Stimmen die Größenverhältnisse?

[ ] Sind die räumlichen Ausrichtungen korrekt?

[ ] Sind alle Verbindungen nachvollziehbar?

[ ] Gibt es schwebende Komponenten?

[ ] Gibt es unbeabsichtigte Überschneidungen?

[ ] Sind die Perspektiven konsistent?

[ ] Ist die Silhouette eindeutig erkennbar?

[ ] Entspricht das Design dem Cube-Escape-Stil?

[ ] Ist das Modell als 3D-Vorlage geeignet?

[ ] Sind alle relevanten Komponenten sichtbar?

[ ] Wirken die Formen konstruktiv plausibel?

[ ] Gibt es widersprüchliche Details?

[ ] Sind Beschriftungen und Varianten eindeutig?

Falls Probleme erkannt werden,
überarbeite das Konzept vor der Ausgabe.

Behaupte nicht, technische Genauigkeit
erreicht zu haben, wenn diese anhand
des Ergebnisses nicht überprüfbar ist.


## 13. PRIORITÄTEN

Beachte folgende Reihenfolge:

1. Korrekte räumliche Konstruktion
2. Logische Bauteilpositionierung
3. Konsistente Proportionen
4. Nachvollziehbare Verbindungen
5. Eindeutige Silhouette
6. Einheitlicher Designstil
7. Saubere geometrische Gestaltung
8. Materialien und Farbgestaltung
9. Dekorative Details
10. Präsentation

Dekorative Details dürfen niemals
fundamentale Konstruktionsprobleme
überdecken.


## 14. ERWARTETES ERGEBNIS

Erstelle hochwertige Concept Arts,
die sowohl optisch überzeugen als auch
als Grundlage für die spätere
3D-Modellierung geeignet sind.

Jedes Design muss:

- Eindeutig interpretierbar sein
- Eine nachvollziehbare Konstruktion besitzen
- Konsistente Proportionen aufweisen
- Korrekt angeordnete Bauteile enthalten
- Zum Cube-Escape-Stil passen
- Möglichst wenig Mehrdeutigkeit verursachen

ZIEL:

Nicht einfach nur schöne Bilder generieren.

Erstelle hochwertige, durchdachte,
konstruktiv plausible und für
3D-Modellierungsagenten geeignete
Designreferenzen.