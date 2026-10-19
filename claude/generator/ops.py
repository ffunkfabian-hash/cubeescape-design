"""Bedienung der bestehenden Waffenblätter KX01–KX10 (claude-0.11): Blattfeld BEDIENUNG und Spec `operation`.

Die neuen Typen (Nr. 11–25) tragen ihre Bedienung im Modell (META['op'], seit claude-0.10). Die 60 Blätter C, D, F, G, H, J 01–10 haben
kein eigenes META-Feld in allen Bauwegen (Kartenskripte, fgen, flib, jlib); ihre Texte stehen deshalb hier, je Blatt passend zur
Bauweise (Pumpgriff, Trommelmagazin, Revolver KF01, Armbrust KC10 …), nicht nur je Typ. Entscheidung des Nutzers 19.10.2026
(„Ja, nachrüsten“, claude/docs/ENTSCHEIDUNGEN.md).

Je Blatt: moving (Kopfzeile des Felds: bewegliche Teile auf Deutsch, Bezeichnungen wie im Modell), reload/action/fire je _de/_en
(höchstens 160 Zeichen, sonst schneidet die Kachel ab). Munitionsklasse: wtypes (nur Einordnung).
"""
OPS={
}
MAXLEN=160

def attach(d,sheet):
    """d['op'] aus OPS setzen, wenn das Modell keine eigene Bedienung mitbringt (neue Typen: META['op'])"""
    if d.get('op') or sheet not in OPS:return d
    d['op']=dict(OPS[sheet],src='ops');return d
