# Waffentypen: Abgleich mit Destiny 2 (claude-0.10)

Stand 18.10.2026. Auftrag des Nutzers: das vollständige Destiny-2-Waffentypen-Sortiment für Cube Escape abgleichen und gestalterisch
vervollständigen (Granatwerfer bewusst als zwei Designpositionen). Destiny liefert Funktions- und Formenreferenzen, kein Nachbau.
Maschinenlesbar: `claude/generator/wtypes.py` (Designtyp je Blattname), im Spec `weapon.design_type` …
Umsetzung und Prüfung: [versions/0.10.md](versions/0.10.md) (Lücken KG23–KG25: Patch 0.10.1 dort).

## Katalog (Quelle und Stand)

- **17 Waffentypen** im Spiel (Datenbank destinytracker.com › Destiny 2 › Weapons, abgerufen 18.10.2026): Automatikgewehr, Handfeuerwaffe,
  Impulsgewehr, Scout-Gewehr, Fusionsgewehr, Scharfschützengewehr, Schrotflinte, Maschinengewehr, Raketenwerfer, Pistole (Sidearm), Schwert,
  Granatwerfer, lineares Fusionsgewehr, Spurgewehr, Bogen, Glefe, Maschinenpistole. Der Granatwerfer ist im Spiel ein Typ mit zwei Bauweisen
  (Kipplauf/Spezialmunition, Trommel/schwere Munition) – hier zwei Positionen, wie beauftragt.
- **Hinzugekommen:** schwere **Armbrust** als neuer Heavy-Typ mit wiederaufnehmbarem Bolzen in „The Edge of Fate“ (15.07.2025; Wikipedia
  „Destiny 2: The Edge of Fate“, TheGamer „Edge of Fate adds heavy-ammo crossbows“). Mit „Renegades“ (02.12.2025) kamen **Hitzewaffen/Blaster**
  (Rahmen „Dynamic Heat“: kein Magazin, Abwärme und Entlüften statt Nachladen; Gizmodo, Dot Esports) und das Laserschwert „Praxic Blade“ (Schwert).
  „Monument of Triumph“ (09.06.2026, letztes Inhalts-Update) brachte keinen neuen Typ.
- **Untertypen mit anderer Mechanik:** Raketen-Sidearm (Rocket-Assisted Frame, Spezialmunition) und Raketen-Impulsgewehr (seit Edge of Fate,
  z. B. „Mint Retrograde“); Slug-Schrotflinte (Einzelgeschoss) gegenüber Streuschrot; Granatwerfer mit Kipplauf, Trommel, „Wave Frame“
  (Bodenwelle), „Double Fire“ und „Micro-Missile Frame“ (Mini-Raketen, Edge of Fate); Handfeuerwaffe „Spread Shot“ (Schrotladung, Edge of Fate);
  Bogen „High-Impact Longbow“; Schwerer Scharfschütze („Refurbished A499“, Renegades); schwere Schrotflinte „Tractor Cannon“; Schwert „Caster Frame“.
- **Nachtrag 19.10.2026 (claude-0.10.1):** Der Hitze-Rahmen ist kein eigener Typ, sondern ein Rahmen bestehender Typen: „Dynamic Heat“ gibt es als
  Handfeuerwaffe, Impulsgewehr, Pistole und Scharfschützengewehr (light.gg „Dynamic Heat Weapon“, Sportskeeda und Boosting-Ground zu den
  Renegades-Heat-Waffen) – kein Maschinengewehr; Munition kommt direkt aus der Reserve, Nachladen = Entlüften. Der Micro-Missile-Rahmen ist ein
  **einschüssiger Spezial-Granatwerfer** mit gerade fliegender Mikrorakete (Destinypedia „Theodolite“: Spezialmunition, Magazin 1; light.gg
  „Micro-Missile Frame“). „Spread Shot“ ist ein Handfeuerwaffen-Rahmen mit kurzem Schrotkegel (light.gg „Spread Shot“), Primärmunition
  (WowVendor zu „Phoneutria Fera“).

## Bestand und Maßnahmen

Entwürfe: Claude C, D, F, G, H, J (`KXnn`, je 10 Typen) und Codex A „Parallax“, K „Flux Bloom“ (`codex/`, je 10). Visierblätter VS01–VS09
zählen nicht als Waffenkonzept. Bewertet wurden Modell, Bauteile und Hauptansicht, nicht der Dateiname.

| Destiny-Typ | vorhandene Entwürfe/IDs | Varianten | Befund | Maßnahme | konkrete Maßnahme und Begründung |
|---|---|---|---|---|---|
| 1 Automatikgewehr / Sturmgewehr | KC02 KD02 KF02 KG02 KH02 KJ02 · KA02 KK02 (`assault_rifle`) | 8 | Magazin, Schaft, Handschutz, Vollautomatik-Aufbau; klar | behalten | `design_type` auto_rifle im Spec |
| 2 Impulsgewehr | KC03 … KJ03 · KA03 KK03 (`pulse_rifle`) | 8 | Energiezelle/Pulskern, Salvenaufbau | behalten | Untertyp Raketen-Impuls neu: KG21 |
| 3 Scout-Gewehr | keiner (`scout_rifle` ist bei Toolgen das **Spurgewehr**) | 0 | fehlt; die KX08 sind Strahlwaffen | **neu erstellen** | **KG11 „Fernlicht“**: halbautomatisch, langer gezogener Lauf, Kastenmagazin, Lochschaft, Präzisionsvisier VS03 |
| 4 Handfeuerwaffe / Hand Cannon | keiner als Typ; KF01 hat eine Trommel | 0 (KF01 konstruktiv) | KF01 ist konstruktiv ein Revolver unter `pistol` | **neu erstellen**, KF01 behalten | **KG12 „Schwerlast“**: Revolver mit Trommel, Hahn, Oberbrücke, Laufmantel; KF01 bleibt Pistole (ID nicht umgedeutet), Hinweis im Spec (`weapon.note`) |
| 5 Pistole / Sidearm | KC01 KD01 KF01 KG01 KH01 KJ01 · KA01 KK01 (`pistol`) | 8 | G/H/J Schlittenpistolen, C/D Energiepistolen – passen zum Sidearm | behalten | `design_type` sidearm; Untertyp Raketen-Sidearm neu: KG20 |
| 6 Maschinenpistole | KC06 … KJ06 · KA06 KK06 (`smg`) | 8 | klar | behalten | – |
| 7 Bogen | KD10 KF10 KG10 KH10 KJ10 · KA10 KK10 (`bow`); KC10 ist eine Armbrust | 8 | Bögen klar; KC10 konstruktiv Armbrust | behalten | KC10 bleibt Bogen (Hinweis im Spec); schwere Armbrust als eigener Typ KG19 |
| 8 Schrotflinte (Streuschrot) | KC04 … KJ04 · KA04 KK04 (`shotgun`) | 8 | Pump-, Trommel-, Doppellauf-, Kastenmagazin-Flinten; alle Streuschrot | behalten | Untertyp Slug neu: KG22 |
| 9 Scharfschützengewehr | KC05 … KJ05 · KA05 KK05 (`sniper_rifle`) | 8 | klar | behalten | schwerer Scharfschütze: gleiche Bauweise, kein eigenes Blatt |
| 10 Fusionsgewehr | KC07 … KJ07 · KA07 KK07 (`fusion_rifle`) | 8 | Kondensatoren, Emitter, Kühlrippen | behalten | – |
| 11 Lineares Fusionsgewehr | keiner | 0 | fehlt | **neu erstellen** | **KG13 „Lichtlinie“**: Kondensatorkammern, zwei Beschleunigerschienen mit Linearkern, Spulenringe, Zielfernrohr VS05 – Unterschied zu KX07: einzelner Linearstrahl über offene Schienen |
| 12 Spurgewehr | KC08 KD08 KF08 KG08 · KH08 KJ08 · KA08 KK08 (`scout_rifle`) | 8 | C/D/F/G klare Strahlwaffen (Spule, Fokus, Fächer); H/J mit Magazin und Laufmantel lesen sich teils wie Scout-Gewehre, Strahl nur über Emitter | behalten, Hinweis | `design_type` trace_rifle für alle; KH08/KJ08 Hinweis im Spec; kein Neubau, weil abgenommen (18.10.2026) und Emitter vorhanden |
| 13 Spezial-Granatwerfer | keiner | 0 | fehlt | **neu erstellen** | **KG14 „Kipper“**: einschüssig, Kipplauf am Scharnier, Verriegelungshebel, Ersatzgranate am Schaft |
| 14 Schwerer Granatwerfer | keiner | 0 | fehlt | **neu erstellen** | **KG15 „Trommelfeuer“**: Drehtrommel mit sechs Kammern, Ladeklappe, Lauf auf Höhe der oberen Kammer |
| 15 Raketenwerfer | KC09 … KJ09 · KA09 KK09 (`rocket_launcher`) | 8 | klar | behalten | – |
| 16 Maschinengewehr | keiner | 0 | fehlt | **neu erstellen** | **KG16 „Dauerläufer“**: Munitionskasten links, Patronengurt in den Zuführdeckel, Tragegriff, Zweibein |
| 17 Schwert | keiner | 0 | fehlt | **neu erstellen** | **KG17 „Kantenlicht“**: Klinge mit leuchtender Schneide, Parierblock mit Energiezelle, Parierstange, kein Visier |
| 18 Glefe | keiner | 0 | fehlt | **neu erstellen** | **KG18 „Wellenbrecher“**: Stange mit Abzug, Klinge mit Emitter, Schildflügel, kein Visier |
| 19 Schwere Armbrust (neu seit 2025) | KC10 (unter Bogen) | 0 als Typ | fehlt als Heavy-Typ | **neu erstellen** | **KG19 „Bolzenwerk“**: quer liegende Recurve-Wurfarme, Sehne zum Schloss, Spannhebel, Bolzen in der Führungsrinne |
| Raketen-Sidearm | keiner | 0 | Mechanik anders (Raketenmunition) | **neu erstellen** | **KG20 „Funkenflug“**: weite Rohrbohrung mit Rakete, Raketenmagazin mit Fenster, Abgasschlitze |
| Raketen-Impulsgewehr | keiner | 0 | Mechanik anders (Raketensalven) | **neu erstellen** | **KG21 „Salvenwerk“**: querliegendes Raketenmagazin (5), Rohrlauf mit Abgasring |
| Slug-Schrotflinte | keiner | 0 | alle Flinten Streuschrot | **neu erstellen** | **KG22 „Treffpunkt“**: ein gezogener Lauf, Mündungsbremse mit Zügen, Kastenmagazin mit Slugs, Ladehebel |
| Granatwerfer Micro-Missile | keiner | 0 | einschüssig, Spezialmunition, Rakete fliegt gerade | **neu erstellt** (0.10.1) | **KG24 „Zielstrich“**: schlankes Abschussrohr mit Leitringen, Ladeklappe oben, Raketenvorrat mit vier Mikroraketen links; `grenade_launcher_special`, `micro_missile` |
| Granatwerfer Wave/Double Fire | – | – | Bauweise wie KG14 (Kipplauf) | offen | kein eigenes Blatt nötig (Mechanik wie KG14) |
| Hitzewaffen/Blaster (Renegades) | keiner | 0 | Rahmen über mehrere Typen (kein MG), ohne Magazin, Entlüftung | **neu erstellt** (0.10.1) | **KG23 „Hitzestau“**: Impulsgewehr ohne Magazin, Hitzespeicher mit Rippenpaket, zwei Entlüftungsklappen, Hitzeanzeige; `pulse_rifle`, `dynamic_heat` |
| Spread-Shot-Handfeuerwaffe | keiner (KG12 Patronen-Revolver) | 0 | Schrotladung, kurzer Streukegel | **neu erstellt** (0.10.1) | **KG25 „Breitseite“**: Kipprahmen-Revolver, Trommel mit fünf Schrotkammern, gefächerte Streumündung; `hand_cannon`, `spread_shot` |
| Tractor Cannon, Caster-Schwert, Longbow | – | – | Sonderformen bestehender Typen | offen | als Varianten von KX04/KG17/KX10 denkbar |

Keine Ersetzung (KH03: nur der englische Prompt übersetzt jetzt „Spulenringe“): Alle 60 Claude-Blätter sind am 18.10.2026 abgenommen; Typzuordnung und Konstruktion tragen. Grenzfälle (KF01, KC10, KH08, KJ08)
bekommen einen Hinweis im Spec, die fehlenden Typen ein eigenes Blatt.

## Zustände

| Blätter | Design vorhanden | visuell geprüft | in Toolgen/Spiel angebunden |
|---|---|---|---|
| KX01–KX09 (Claude C–J) | ja | ja, vom Nutzer abgenommen (18.10.2026) | ja: Toolgen-Werkzeuge 1–9, Cube Escape Waffen 1–9 |
| KX10 Bogen (Claude) | ja | ja, abgenommen | Toolgen-Werkzeug `bow` (Referenzmodell), nicht im Waffensatz von Cube Escape |
| KA/KK (Codex) | ja | Codex-Pipeline (Prüfung dort) | wie oben je Typ |
| KG11–KG22 (neu) | ja | von Claude geprüft (Skizze, Blatt, Kontaktbogen); Abnahme durch den Nutzer offen | **nein** – `toolgen_id` null, `toolgen_status` not_connected |
| KG23–KG25 (neu, 0.10.1) | ja | von Claude geprüft (Skizze, Blatt, Kontaktbogen); Abnahme durch den Nutzer offen | **nein** – wie KG11–KG22 |

## Offene Anbindungen

- **Toolgen:** neue Werkzeug-IDs nötig (Vorschlag = `design_type`): `hand_cannon`, `linear_fusion_rifle`, `grenade_launcher_special`,
  `grenade_launcher_heavy`, `machine_gun`, `sword`, `glaive`, `heavy_crossbow`; Untertypen als eigene Werkzeuge oder als Variante des Eltern-Werkzeugs.
  **Namenskonflikt:** Toolgens `scout_rifle` ist das Spurgewehr; ein echtes Scout-Gewehr braucht eine neue ID (Vorschlag `scout_rifle_semi`)
  oder Toolgen benennt das Spurgewehr in `trace_rifle` um (Vertragsänderung in Toolgen/Cube Escape, Entscheidung des Nutzers).
- **Use-Clips:** neue Bewegungsarten im Spec (`proposed: true`): Trommel, Hahn, Beschleunigerschienen, Kipplauf, Granattrommel, Zuführdeckel,
  Spannhebel, Sehne, Schildflügel, seit 0.10.1 Entlüftungsklappen (`vent`) und Kipprahmen (`top_break`); Knotennamen (`Anim_Cylinder` …) sind Vorschläge.
- **Cube Escape:** Haltungen für Nahkampf (Schwert, Glefe: kein Visier, Griff ohne Abzug beim Schwert), Roboter-Maße (`robot_fit` fehlt, Zielmaße
  legt Cube Escape fest), Elemente (`element` null), Visier-Ziele (Tabelle „Visiere je Waffe“ kennt nur 1–9).
- **Texturprofile** der neuen Typen sind Vorschläge (`derived_from`), nicht im Textur-Blatt des Nutzers.
- **Codex:** keine Blätter der neuen Typen in A/K; Spec-Feld `weapon.design_type` fehlt dort (Änderungswunsch an Codex).

## Verbleibende Lücken

- Hitzewaffe, Micro-Missile-Granatwerfer und Spread-Shot-Handfeuerwaffe: seit claude-0.10.1 gebaut (KG23–KG25). Der Hitze-Rahmen nur als
  Impulsgewehr; Hitze-Handfeuerwaffe, -Pistole und -Scharfschütze wären Varianten derselben Mechanik.
- Neue Typen nur in Variante G; die übrigen Claude-Varianten und Codex haben sie nicht.
- Das Blattfeld BEDIENUNG gibt es nur auf den neuen Blättern; die 60 bestehenden Blätter haben es nicht (eigener Schritt mit Neubau).
