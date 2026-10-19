"""KJ24 FROSTSPIKE: schlanker Mikroraketenwerfer mit gabelförmigem Schaft."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#252E30', '#BCEEF4', '#606B6E', '#11171C'
AX = 278


def spec():
    return [
        K([(78,262),(94,253),(107,267),(107,364),(91,374),(78,362)],
          DK,-17,17,b=4,bz=5,label='Schaftkappe'),
        K([(101,262),(167,245),(240,257),(240,279),(168,267),(101,286)],
          BK,-14,14,b=4,bz=5,label='Schaft',glow=[((0,1),IC,3.2)]),
        K([(101,348),(167,327),(237,286),(248,307),(178,348),(101,370)],
          BK,-14,14,b=4,bz=5,label='Schaft',glow=[((3,4),IC,3.2)]),
        K([(232,258),(328,245),(405,253),(439,272),(439,311),(408,337),
           (232,337),(220,318),(220,277)],BK,-23,23,b=7,bz=8,label='Gehäuse',
          glow=[((0,1,4),IC,3.6)]),
        K(rect(244,230,80,34),DK,-9,9,b=2,bz=3,label='Visierschiene',
          dec=[(rect(253+13*i,237,5,4),GM,False) for i in range(5)]),
        K([(340,243),(415,238),(432,248),(432,264),(340,265)],
          BK,-16,16,b=3,bz=4,label='Ladeklappe',glow=[((0,1),IC,3.1)],
          dec=[([(352+17*i,249),(361+17*i,248),(362+17*i,255),(353+17*i,256)],GM,False)
               for i in range(4)]),
        K(rect(331,249,12,18),GM,-19,19,b=2,bz=3,label='Klappenscharnier'),
        # Die Reserve liegt ausschließlich links; vier volle Raketenprofile im Fenster.
        K([(271,278),(394,266),(425,279),(425,322),(399,336),(271,336)],
          BK,23,56,b=5,bz=6,label='Raketenvorrat',glow=[((0,3,4),IC,3.6)],
          dec=[([(283,286),(394,276),(414,284),(414,316),(395,327),(283,327)],DK,False)]+
              [(rect(290,286+9*i,84,5),GM,False) for i in range(4)]+
              [([(374,286+9*i),(391,286+9*i),(403,288.5+9*i),(391,291+9*i),(374,291+9*i)],IC,False)
               for i in range(4)]),
        K([(269,337),(317,337),(305,418),(265,430),(254,414)],
          DK,-16,16,b=5,bz=5,label='Griff',
          dec=[([(278,353),(303,349),(292,401),(268,409)],GM,False)]),
        K([(337,336),(349,336),(361,368),(349,375)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(312,385),(388,377),(395,388),(312,396)],DK,-7,7,b=2,bz=2),
        K([(385,337),(395,337),(395,388),(385,388)],DK,-7,7,b=2,bz=2),
        # Langes flaches Achteckprofil mit durchlaufenden oberen/unteren Eiskanten.
        K([(429,263),(722,263),(737,271),(737,285),(722,293),(429,293)],
          BK,-15,15,b=4,bz=5,label='Abschussrohr',glow=[((0,3,4),IC,3.2)],
          dec=[(rect(447+12*i,274,5,8),DK,False) for i in range(3)]),
        X(483,495,AX,21,GM,n=8,label='Leitring'),
        X(582,594,AX,21,GM,n=8,label='Leitring'),
        X(687,699,AX,21,GM,n=8,label='Leitring'),
        K([(625,292),(659,292),(651,356),(630,368),(618,356)],
          DK,-13,13,b=4,bz=4,label='Vordergriff',glow=[((1,2),IC,3.0)]),
        T(731,755,AX,16,23,BK,n=8,label='Mündung'),
        X(753,763,AX,23,DK,n=8,label='Mündung',
          cap=[(AX,0,15,'#05090C',False),(AX,0,6,IC,False)]),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='24',name='Mikroraketen-Granatwerfer',nick='FROSTSPIKE',col=IC,
    pill='NACHTSCHIEFER · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(420.5, 330.0, 0),
    desc='Ein langer eisgeränderter Abschussstachel setzt die Linie des flachen Facettengehäuses fort. '
         'Drei achteckige Leitringe, ein Vordergriff weit vorn und der offene Gabelschaft machen den Werfer unverwechselbar. '
         'Links sitzen vier Ersatz-Mikroraketen im Reservekasten, geladen wird einzeln durch die obere Ladeklappe.',
    form='Offener Gabelschaft · flaches Facettengehäuse · fest verbundene Visierschiene · obere Ladeklappe mit hinterem Scharnier · '
         'Raketenvorrat links mit vier Mikroraketen · langes Abschussrohr · drei Achteck-Leitringe · Mündung · Vordergriff',
    op=dict(
        reload_de='Obere Ladeklappe nach hinten öffnen, eine Mikrorakete aus dem linken Vorrat ins Patronenlager legen, Klappe schließen',
        action_de='Einschüssig: Nach jedem Schuss neu laden; der Raketenmotor zündet erst vor der Mündung',
        fire_de='Eine schnelle Mikrorakete fliegt gerade statt im Bogen; Aufprallzünder, Spezialmunition',
        reload_en='open the top gate to the rear, put one micro-missile from the left reserve into the chamber, close the gate',
        action_en='single shot: reload after each shot; the missile motor ignites just past the muzzle',
        fire_en='one fast micro-missile flies straight instead of arcing; impact fuse, special ammunition'))
