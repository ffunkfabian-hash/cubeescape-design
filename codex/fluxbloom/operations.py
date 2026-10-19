"""Independently written operation concepts for the actual Codex constructions.

Static concept intent; no rig, animation, ammunition simulation or gameplay is
validated. The shared ops.py is a functional reference, not a text source.
"""
from design_types import weapon_fields

# Each tuple is reload, action, fire in German then English. These describe the
# visible assembly and never invent a visible bolt/slide on a sealed receiver.
OPS = {
 'parallax': {
 'pistol': (
  'Die Energiezelle nach unten aus dem Griff ziehen und am Zellensockel durch eine volle Zelle ersetzen.',
  'Die Ladeanzeige prüfen; die Energiezufuhr im Keilgehäuse wird mit jedem Abzugsdruck freigegeben.',
  'Einzelne Energieimpulse durch die offene Laufhülse abgeben; den Abzug zwischen den Impulsen lösen.',
  'Pull the energy cell down from the grip and seat a charged cell against the heel socket.',
  'Check the charge indicator; each trigger pull enables the energy feed inside the wedge housing.',
  'Send single energy pulses through the open barrel sleeve; release the trigger between pulses.'),
 'assault': (
  'Das Kastenmagazin vor dem Bügel nach unten herausnehmen und im verstärkten Schacht ersetzen.',
  'Schulterpolster anlegen und den Handschutz auf der Griffauflage stützen; die Zuführung arbeitet im Gehäuse.',
  'Für Dauerfeuer den Abzug halten; kurze Feuerstöße durch Loslassen begrenzen.',
  'Remove the box magazine ahead of the guard and replace it in the reinforced well.',
  'Shoulder the pad and support the handguard at its grip rest; the feed mechanism operates inside the receiver.',
  'Hold the trigger for automatic fire; release it to limit each burst.'),
 'impulse': (
  'Das Zellenmagazin unter dem Gehäuse wechseln; die vier Pulsspulen bleiben fest auf ihrem Träger.',
  'Vor jeder Salve die Ladeanzeige prüfen; die Spulen takten die Energie entlang der Laufachse.',
  'Ein Abzugsdruck löst eine Impulsfolge aus; erst nach Ende der Folge erneut betätigen.',
  'Swap the cell magazine below the housing; the four pulse coils remain fixed to their carrier.',
  'Check the charge indicator before each burst; the coils time energy along the barrel axis.',
  'One trigger pull starts a pulse sequence; pull again only after that sequence ends.'),
 'shotgun': (
  'Die kompakte Munitionskassette vor dem Bügel aus dem Schacht nehmen und ersetzen.',
  'Den Pumpgriff am unteren Rohr zurück- und vorschieben; die Laufbrücke bleibt fest mit beiden Rohren verbunden.',
  'Ein Abzugsdruck gibt eine Schrotladung frei; vor dem nächsten Schuss erneut pumpen.',
  'Remove and replace the compact ammunition cassette ahead of the guard.',
  'Cycle the pump grip along the lower tube; the barrel bridge remains fixed to both tubes.',
  'Each trigger pull releases a pellet load; cycle the pump before firing again.'),
 'sniper': (
  'Das Magazin vor dem Griff wechseln; die verstellbare Schulterplatte bleibt an den beiden Schaftstegen.',
  'Wange auflegen und die nächste Patrone über die innenliegende Zuführung bereitstellen; außen ist kein Kammerhebel modelliert.',
  'Gezielte Einzelschüsse durch den langen freien Lauf; nach jedem Schuss neu ausrichten.',
  'Swap the magazine ahead of the grip; the adjustable shoulder plate stays on the two stock struts.',
  'Set the cheek rest and feed the next round internally; no external bolt handle is modelled.',
  'Fire aimed single shots through the long exposed barrel; reacquire the target after each shot.'),
 'smg': (
  'Das hinter dem Griff sitzende Magazin nach unten aus dem Bullpup-Schacht ziehen und ersetzen.',
  'Den gefalteten Schaftsteg anlegen; den vorderen Handstopp unter dem kurzen Lauf als Stützgrenze nutzen.',
  'Automatische kurze Feuerstöße abgeben; der Abzug stoppt die Folge beim Loslassen.',
  'Pull the magazine down from the bullpup well behind the grip and insert a replacement.',
  'Shoulder the folded stock strut; use the forward hand stop below the short barrel as the support limit.',
  'Fire short automatic bursts; releasing the trigger stops the sequence.'),
 'fusion': (
  'Die untere Energiezelle im Schacht tauschen; Reaktorkammer, Kammerringe und Zugstangen bleiben montiert.',
  'Abzug zum Laden der gefassten Reaktorkammer halten; die Kammerfenster zeigen den Energiezustand.',
  'Nach dem Aufbau der Ladung eine Bolzensalve durch den offenen Düsenring freigeben.',
  'Replace the lower energy cell; the reactor chamber, chamber rings and tie rods remain assembled.',
  'Hold the trigger to charge the supported reactor chamber; its windows indicate energy state.',
  'Once charged, release an energy-bolt volley through the open nozzle ring.'),
 'trace': (
  'Das Magazin vor dem Griff als Energiezelle wechseln; die beiden freien Beschleunigerschienen nicht entnehmen.',
  'Abzug halten, um den durch Querbrücken gestützten Schienenkanal zu speisen.',
  'Ein Dauerstrahl verlässt den offenen Mündungsrahmen; beim Loslassen endet die Energiezufuhr.',
  'Swap the magazine ahead of the grip as an energy cell; leave both exposed accelerator rails installed.',
  'Hold the trigger to power the rail channel supported by its cross bridges.',
  'A continuous beam leaves the open muzzle frame; releasing the trigger cuts its energy supply.'),
 'rocket': (
  'Die Rakete durch die offene Rohrmündung einsetzen; die untere Steuerenergiezelle wird separat gewechselt.',
  'Rohr auf der Schulter ausrichten und das linke Visier nutzen; der hintere Öffnungsring bleibt frei.',
  'Eine Rakete je Beladung starten; der freie Rohrkanal führt den Start entlang der Längsachse.',
  'Insert a rocket through the open tube muzzle; replace the lower control cell separately.',
  'Align the shoulder tube using the left sight; keep the rear opening ring clear.',
  'Launch one rocket per loading; the clear tube guides launch along the longitudinal axis.'),
 'bow': (
  'Einen Pfeil in die seitlich freie Pfeilauflage legen; die Zelle bei Bedarf unter dem Griff austauschen.',
  'Die Sehne bis zur Auslösung spannen; Riser und Rekurvearme lassen den Pfeilkorridor offen.',
  'Mit dem Auslöser die Sehne freigeben; ein Pfeil folgt der offenen Magnetführung.',
  'Place an arrow on the unobstructed side rest; replace the cell below the grip as needed.',
  'Draw the string to the release; the riser and recurve limbs leave the arrow corridor open.',
  'Use the release to let the string go; one arrow follows the open magnetic guide.'),
 },
 'fluxbloom': {
 'pistol': (
  'Das Griffmagazin unter dem offenen Fersenrahmen herausziehen und bis an die sichtbare Bodenplatte ersetzen.',
  'Die versetzten Keilschalen am Griff ruhig führen; die Auslösung arbeitet im geschlossenen Hammerkopf.',
  'Pro Abzugsdruck einen Einzelschuss durch die offene Mündung abgeben; anschließend den Abzug freigeben.',
  'Pull the grip magazine out beneath the open heel loop and seat a replacement against the visible base plate.',
  'Steady the offset wedge shells through the grip; the firing mechanism works inside the closed hammerhead.',
  'Fire one shot per trigger pull through the open muzzle, then release the trigger.'),
 'assault': (
  'Das Magazin unter dem offenen Lastträger wechseln; es sitzt im eigenen Schacht vor dem Abzug.',
  'Den dreieckigen Schaft anlegen und die untere Schale stützen; das Verschlussfenster bleibt frei.',
  'Abzug für automatische Feuerfolgen halten und zum Ende jedes Stoßes lösen.',
  'Swap the magazine beneath the open load carrier; its well sits ahead of the trigger.',
  'Shoulder the triangular stock and support the lower shell; leave the receiver window clear.',
  'Hold the trigger for automatic fire and release it at the end of each burst.'),
 'impulse': (
  'Das verriegelte Zellenmagazin unter der Kammer abziehen und eine geladene Zelle einsetzen.',
  'Die drei Impulsstufen über den Abzug speisen; Kühlkrone und Lastträger bleiben fest am Gehäuse.',
  'Getaktete Energiesalven durch die dünne Laufseele; zwischen den Salven den Abzug lösen.',
  'Remove the locked cell magazine below the chamber and insert a charged cell.',
  'Power the three pulse stages through the trigger; the cooling crown and carriers remain fixed to the housing.',
  'Send timed energy bursts through the thin barrel core; release the trigger between bursts.'),
 'shotgun': (
  'Das Magazin unter dem Gehäuse entnehmen und ersetzen; beide seitlich versetzten Rohre bleiben zusammen montiert.',
  'Die breite Pumpmanschette auf ihrer Führung zurückziehen und wieder vorschieben.',
  'Eine Schrotladung durch die gestaffelte Mündungsgruppe abgeben; danach die Manschette erneut bewegen.',
  'Replace the magazine beneath the receiver; both offset tubes stay assembled together.',
  'Pull the broad pump sleeve back along its guide and push it forward again.',
  'Fire a pellet load through the staggered muzzle group, then cycle the sleeve again.'),
 'sniper': (
  'Das Kastenmagazin an der kurzen Rautenkammer wechseln; die Wangenauflage bleibt links der Achse.',
  'Schaftdreieck anlegen und die Kammer innen bereitstellen; kein äußerer Kammerhebel ist im Modell vorhanden.',
  'Präzise Einzelschüsse durch den freien langen Lauf; zwischen Schüssen bewusst neu zielen.',
  'Swap the box magazine at the short diamond chamber; the cheek rest remains left of the axis.',
  'Shoulder the stock triangle and ready the internal chamber; no exterior bolt handle is modelled.',
  'Fire precise single shots through the long exposed barrel; deliberately reacquire aim between shots.'),
 'smg': (
  'Das Bullpup-Magazin hinter dem Griff austauschen; die linke Einspeisekassette bleibt am Heck.',
  'Das offene Schulterdreieck anlegen und den kurzen Keilsockel unterhalb des Laufes stützen.',
  'Automatikfolgen auf kurze Entfernung; den Abzug lösen, um jede Folge zu beenden.',
  'Replace the bullpup magazine behind the grip; the left feed cassette stays at the rear.',
  'Shoulder the open triangle and support the short wedge socket beneath the barrel.',
  'Use automatic sequences at short range; release the trigger to end each sequence.'),
 'fusion': (
  'Die Energiezelle im unteren Schacht wechseln; Induktionsringe und Speichen bleiben am Kernsattel.',
  'Abzug halten und die Ladung über die offenen Induktionsringe aufbauen; der Feldstatus zeigt die Versorgung.',
  'Nach dem Laden eine Energiebolzen-Salve durch den Kernlauf und die offene Mündung freigeben.',
  'Swap the cell in the lower well; the induction rings and spokes remain on the core saddle.',
  'Hold the trigger to charge through the open induction rings; the field indicator shows supply state.',
  'Once charged, release an energy-bolt volley through the core barrel and open muzzle.'),
 'trace': (
  'Das Zellenmagazin vor dem Griff nach unten wechseln; die beiden Gabelzinken bleiben fest in den Feldklammern.',
  'Abzug halten, um den zurückgesetzten Emitter zwischen den Beschleunigern zu speisen.',
  'Den Dauerstrahl auf dem Ziel halten; beim Lösen des Abzugs erlischt der schmale Strahl.',
  'Swap the cell magazine ahead of the grip downward; both fork prongs stay fixed in their field clamps.',
  'Hold the trigger to power the recessed emitter between the accelerators.',
  'Keep the continuous beam on target; release the trigger to stop the thin beam.'),
 'rocket': (
  'Das durchgehend offene Hauptrohr von vorn mit einer Rakete beladen; das untere Steuermagazin separat prüfen.',
  'Am Griff und Vordergriff führen, Schulterpolster anlegen und über das linke Visier ausrichten.',
  'Eine Rakete starten; der Heckring und der freie Rohrdurchlass gehören zur gleichen Startachse.',
  'Load a rocket through the front of the continuously open main tube; check the lower control magazine separately.',
  'Use the main and forward grips, shoulder the pad and aim through the left sight.',
  'Launch one rocket; the rear ring and clear tube share the same launch axis.'),
 'bow': (
  'Pfeil in die Auflage neben dem Riser legen; die seitliche Energiezelle bei Bedarf austauschen.',
  'Sehne bis zur Sehnenkerbe spannen; Unterarmstütze und Riserbrücke stabilisieren den Kontaktgriff.',
  'Auslöser betätigen und den Pfeil durch die freie Magnetführung freigeben.',
  'Place an arrow on the rest beside the riser; replace the side energy cell as needed.',
  'Draw the string to its notch; the forearm brace and riser bridge steady the contact grip.',
  'Operate the release to send the arrow through the unobstructed magnetic guide.'),
 }}


def operation(meta):
    values = OPS[meta['series']][meta['slug']]
    return {**{key:dict(de=values[i], en=values[i+3]) for i,key in enumerate(('reload','action','fire'))},
            'ammo_class':weapon_fields(meta)['ammo_class'],
            'source':'Eigenständiger Codex-Bedienentwurf zur sichtbaren Bauweise; statische Funktionsabsicht, keine geprüfte Animation oder Spielfunktion.'}
