# Cube Escape – Prompt-Vorlagen, um die Konzeptblätter mit ChatGPT bzw. Codex nachzubauen

Zwei Wege:
- **A · Codex (oder ChatGPT mit Code-Ausführung):** baut dieselbe Pipeline als Programm nach. Ergebnis wie auf der Seite „Konzeptblätter“: ein 3D-Modell → alle Ansichten exakt konsistent.
- **B · ChatGPT-Bildgenerator:** malt ein Blatt als Bild. Schneller, aber Ansichten sind nie 100 % deckungsgleich.

Den „Concept-Art-Qualitäts-Masterprompt“ (liegt im Projekt) jeweils mitgeben.

---

## A · Prompt für Codex

```
Rolle: Du bist Technical Artist und Python-Entwickler. Baue eine Pipeline, die für das Spiel „Cube Escape“
technische Low-Poly-Konzeptblätter für Waffen erzeugt. Halte dich verbindlich an den beigefügten
„Concept-Art-Qualitäts-Masterprompt“ (Konstruktion vor Optik, Prüfliste Abschnitt 12).

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
```

---

## B · Prompt für den ChatGPT-Bildgenerator (pro Waffe)

Tipp: erst die Isometrie erzeugen lassen, dann im selben Chat mit diesem Bild als Referenz die Ortho-Ansichten
nachfordern („gleiche Waffe, exakt gleiche Bauteile“). Platzhalter in <…> ersetzen – oder die fertigen Prompts aus
„Waffen-Prompts.md“ nehmen.

```
Erstelle ein technisches Concept-Art-Designblatt (Querformat, 16:9) für das Low-Poly-Sci-Fi-Spiel „Cube Escape“:
<Waffe>, Variante <X> „<Name>“.

Form: <FORM-Zeile>. Pflicht-Bauteile, alle sichtbar und logisch verbunden: <Bauteilliste>.
Farbpalette: <Hex-Farben>. Materialien: lackiertes Metall, gebürstetes Metall (Läufe), gummierter Griff, matter Kunststoff,
sparsame beleuchtete Funktionselemente.

Aufbau des Blatts: links große isometrische Hauptansicht der Waffe mit deutschen Beschriftungen in Etiketten
(Gehäuse, Griff, Abzug, Magazin, Lauf, Mündung, Schaft, Visierschiene) und Hinweislinien; rechts orthografische
Seitenansicht links und rechts, Vorder-, Rück-, Drauf- und Unteransicht im gleichen Maßstab mit gestrichelten Bezugslinien;
unten: Detail Abzugsbereich von schräg unten, das Visier separat gezeichnet (nicht montiert, Vermerk „Visier · separat,
modular auf Schiene“), Materialfelder, vier Farbvarianten derselben Waffe.

Stil: Low-Poly, Hard-Surface, abgeschrägte Gehäuse, kantige Panzerplatten, klare dunkle Konturen, flache Toon-Schattierung
in wenigen Stufen, dunkelblauer Rasterhintergrund (#0E1622), saubere Typografie.
Konstruktion: Abzug mit Bügel klar sichtbar, Magazin im Schacht, Lauf sichtbar aus dem Gehäuse, auf der Waffe nur die
freie Visierschiene (bei Raketenwerfern seitlich links am Rohr), konsistente Achsen, identisches Modell in allen Ansichten.
Vermeiden: schwebende Teile, unbeabsichtigte Überschneidungen, zufällige Leuchtstreifen, Bloom, Unschärfe, Nebel,
Fotorealismus, Kopien realer Militärwaffen.
```

Hinweis: Bildgeneratoren halten Maßstab und Bauteilpositionen zwischen den Ansichten nicht zuverlässig ein und
schreiben Beschriftungen teils fehlerhaft. Für verbindliche 3D-Vorlagen ist Weg A zuverlässiger.
