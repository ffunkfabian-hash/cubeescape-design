"""KJ14 COLDWIRE: Keilschaft und kurzer achteckiger Kipplauf mit tiefer Kinnfinne."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#212A30', '#AFEFF3', '#616C73', '#10161D'


def spec():
    return [
        K([(84,243),(106,235),(125,247),(125,345),(100,362),(84,351)],
          DK,-18,18,b=4,bz=5,label='Schaftkappe'),
        K([(116,248),(210,259),(250,282),(250,309),(207,303),(116,277)],
          BK,-15,15,b=5,bz=5,label='Schaft',glow=[((0,1,3),IC,3.6)]),
        K([(116,335),(214,311),(250,296),(256,315),(211,337),(116,354)],
          BK,-15,15,b=4,bz=4,label='Schaft',glow=[((0,3),IC,3.0)]),
        K([(148,272),(217,272),(222,302),(148,307)],GM,14,23,b=3,bz=3,label='Granathalter'),
        X(154,199,289,10,DK,n=6,cz=32,label='Ersatzgranate'),
        T(199,216,289,10,4,GM,n=6,cz=32,label='Ersatzgranate'),
        K([(245,270),(339,250),(393,263),(410,288),(399,327),(245,332)],
          BK,-21,21,b=6,bz=7,label='Gehäuse',glow=[((0,1,4),IC,3.6)],
          dec=[([(265,289),(328,274),(362,281),(349,297),(265,309)],DK,False)]),
        K(rect(274,239,87,34),DK,-10,10,b=2,bz=3,label='Visierschiene',
          dec=[(rect(284+14*i,247,5,3),GM,False) for i in range(5)]),
        K([(367,257),(375,236),(394,233),(407,253),(393,263)],
          GM,-6,6,b=2,bz=2,label='Verriegelungshebel'),
        K([(390,309),(406,303),(421,311),(421,325),(405,333),(390,325)],
          GM,-25,25,b=3,bz=4,label='Scharnier'),
        # Die Barrel-Gruppe bleibt vollständig vor dem Scharnier bedienbar.
        X(405,569,289,28,BK,n=8,label='Kipplauf'),
        K([(410,258),(536,248),(564,263),(548,274),(410,274)],
          BK,-16,16,b=3,bz=4,label='Kipplauf',glow=[((0,1,3),IC,3.6)]),
        K([(411,306),(549,306),(562,319),(530,336),(411,325)],
          BK,-16,16,b=3,bz=4,label='Kipplauf',glow=[((0,2),IC,3.6)]),
        X(563,585,289,32,GM,n=8,label='Mündung',cap=[(289,0,22,'#05090C',False)]),
        K([(275,327),(319,327),(308,414),(266,421)],DK,-17,17,b=4,bz=5,label='Griff',
          dec=[([(285,350),(305,350),(297,401),(277,407)],GM,False)]),
        K([(338,327),(349,327),(361,357),(349,365)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(315,377),(388,372),(395,383),(314,389)],DK,-7,7,b=2,bz=2),
        K([(385,326),(397,326),(397,383),(385,383)],DK,-7,7,b=2,bz=2),
        K([(464,325),(499,328),(487,386),(461,379)],DK,-14,14,b=4,bz=4,label='Vordergriff'),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='14',name='Spezial-Granatwerfer',nick='COLDWIRE',col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(334.5,327,0),
    desc='Ein kurzer achteckiger Kipplauf liegt zwischen einer scharfen Rückenleiste und einer tiefen Kinnfinne. Der offene Keilschaft '
         'trägt links eine Ersatzgranate im separaten Halter. Verriegelungshebel und großes Facettenscharnier erklären das Abkippen des gesamten Vorderteils.',
    form='Offener Keilschaft · Granathalter links mit Ersatzgranate · kurzes Facettengehäuse · Verriegelungshebel · Scharnier · '
         'achteckiger Kipplauf mit Kinnfinne · breite Mündung · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Verriegelungshebel drücken, Kipplauf am Scharnier nach unten klappen, Hülse auswerfen, eine Granate einschieben und Lauf schließen',
        action_de='Ein Schuss je Ladung; die Ersatzgranate im linken Schafthalter bleibt beim Öffnen des Kipplaufs erreichbar',
        fire_de='Eine Granate fliegt im Bogen; Aufprallzünder oder Fernzündung mit erneutem Abzug',
        reload_en='press the locking lever, tip the barrel down on its hinge, eject the case, insert one grenade and close the barrel',
        action_en='one shot per load; the spare grenade in the left stock holder stays accessible while the barrel is open',
        fire_en='lob one grenade with an impact fuse, or detonate remotely with a second trigger pull'))
