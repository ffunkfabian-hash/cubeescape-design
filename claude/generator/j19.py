"""KJ19 „Winterbow“: offene Stealth-Armbrust mit breiten, rückwärts gepfeilten Querarmen."""
import math
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222B30', '#B4EDF3', '#626E73', '#10171C'
BY=252


def Q(prof,col,y0,y1,**kw):
    """jlib-Facette in der x-z-Ebene, anschließend im Modell um x gedreht."""
    p=K(prof,col,-y1,-y0,**kw)
    p['quer']=True
    return p


def string(p0,p1):
    dx,dz=p1[0]-p0[0],p1[1]-p0[1]
    length=math.hypot(dx,dz)
    nx,nz=-dz/length*1.2,dx/length*1.2
    return Q([(p0[0]+nx,p0[1]+nz),(p1[0]+nx,p1[1]+nz),
              (p1[0]-nx,p1[1]-nz),(p0[0]-nx,p0[1]-nz)],
             GM,BY-1.2,BY+1.2,b=.3,bz=.3,label='Sehne')


def spec():
    p=[
        K([(70,255),(91,246),(105,259),(105,357),(83,369),(70,357)],
          DK,-17,17,b=4,bz=4,label='Schaftkappe'),
        K([(101,257),(202,251),(250,264),(250,283),(197,271),(101,278)],
          BK,-14,14,b=4,bz=4,label='Schaft',glow=[((0,1),IC,3.6)]),
        K([(101,341),(171,322),(232,284),(251,301),(184,346),(101,362)],
          BK,-14,14,b=4,bz=4,label='Schaft',glow=[((1,3),IC,3.6)]),
        K([(121,246),(194,241),(213,249),(211,260),(122,267)],
          GM,-11,11,b=3,bz=3,label='Wangenauflage'),
        K([(246,261),(554,261),(629,269),(650,285),(638,309),
           (554,322),(246,322),(234,307),(234,277)],
          BK,-21,21,b=6,bz=6,label='Gehäuse',glow=[((0,1,4,5),IC,3.6)],
          dec=[([(271,280),(349,280),(366,288),(349,297),(271,297)],DK,False),
               ([(459,284),(526,284),(554,294),(459,298)],GM,False)]),
        K(rect(264,249,106,20),DK,-10,10,b=2,bz=2,label='Visierschiene',
          dec=[(rect(277+14*i,256,5,4),GM,False) for i in range(6)]),
        K([(384,241),(407,241),(419,250),(419,264),(384,264)],
          GM,-15,15,b=3,bz=3,label='Schloss'),
        K(rect(413,255,233,6),DK,-5,5,b=1,bz=1,label='Führungsrinne'),
        X(411,738,BY,3.5,GM,n=8,label='Bolzen'),
        T(737,769,BY,7,1,IC,n=8,label='Bolzen'),
        K([(414,247),(425,241),(441,241),(450,247),(450,251),(414,251)],
          GM,-1,1,b=1,bz=.5,label='Bolzen'),
        K([(602,261),(635,260),(655,275),(655,306),(638,322),(602,319)],
          DK,-29,29,b=5,bz=6,label='Bogenblock'),
        K([(390,285),(612,280),(624,288),(612,296),(390,297)],
          GM,21,31,b=2,bz=2,label='Spannhebel'),
        K([(605,278),(619,276),(628,285),(626,295),(613,299),(604,291)],
          DK,21,34,b=2,bz=2),
        K([(273,321),(319,321),(307,417),(256,421)],
          DK,-18,18,b=5,bz=5,label='Griff',
          dec=[([(284,343),(307,343),(298,402),(269,406)],GM,False)]),
        K([(339,323),(350,323),(361,353),(350,360)],
          GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(313,377),(397,373),(400,384),(311,389)],DK,-8,8,b=2,bz=2),
        K([(389,321),(400,321),(400,381),(389,381)],DK,-8,8,b=2,bz=2),
        K([(512,320),(547,320),(557,377),(534,391),(519,378)],
          DK,-14,14,b=4,bz=4,label='Vordergriff'),
    ]
    for side in (-1,1):
        # Manta-Grundriss: breiter Schulterknick und deutlich rückwärts gepfeilte Spitzen.
        p.append(Q([(615,24*side),(644,24*side),(671,92*side),
                    (618,179*side),(593,189*side),(580,180*side),(628,91*side)],
                   BK,BY-8,BY+10,b=3,bz=3,label='Wurfarm',glow=[((0,1,2,3,4,5,6),IC,3.6)]))
        p.append(Q([(581,173*side),(598,172*side),(606,185*side),
                    (595,198*side),(582,193*side),(576,182*side)],
                   GM,BY-10,BY+12,b=2,bz=3,label='Wurfarm'))
        p.append(string((590,181*side),(398,2*side)))
    return p


def model():
    entries=spec()
    m=jlib.model(entries)
    for part,entry in zip(m.parts,entries):
        if not entry.get('quer'):
            continue
        for face in part['F']:
            face['v']=[(x,-z,y) for x,y,z in face['v']]
            nx,ny,nz=face['n'];face['n']=(nx,-nz,ny)
        # Die obere Fläche erhält Decals; eng.render behandelt y+ nicht separat.
        part['dec']=[('y-',-value,pts,col,emit)
                     for plane,value,pts,col,emit in part['dec'] if plane=='z+']
    return m


META = dict(
    num='19', name='Schwere Armbrust', nick='WINTERBOW', col=IC,
    pill='POLARNACHT · EISWEISS · GUNMETAL', palette=[BK,IC,GM,DK], center=(419.5,331,0),
    desc='Eine schwere Armbrust mit offenem Dreieckschaft und flacher Führungsrinne. '
         'Die quer liegenden Facettenwurfarme sind breit geknickt und pfeilen zur gespannten Sehne zurück. '
         'Der wiederaufnehmbare Bolzen ruht vor dem Schloss; links am langen Gehäuse sitzt der Spannhebel, darunter der freie Griffbereich.',
    form='Offener Dreieckschaft mit Wangenauflage · Gehäuse mit Führungsrinne und Visierschiene · Schloss · '
         'Bolzen · Bogenblock mit zwei gepfeilten Querwurfarmen und zwei Sehnenhälften · Spannhebel links · Griff mit Abzug · Vordergriff',
    op=dict(
        reload_de='Spannhebel links am vorderen Gelenk nach vorn-unten schwenken, Sehne ins Schloss ziehen und Bolzen in die Führungsrinne legen',
        action_de='Ein Bolzen je Spannung; Bolzen nach dem Treffer wieder aufnehmen, um den Vorrat zu ergänzen',
        fire_de='Einzelschuss mit hoher Durchschlagskraft; je nach Ausführung Explosiv- oder Widerhakenbolzen',
        reload_en='Swing the left cocking lever forward and down on its front hinge, draw the string into the latch and lay a bolt in the groove',
        action_en='One bolt per draw; recover the bolt after impact to refill the reserve',
        fire_en='Single high-impact shot; explosive or serrated bolts depending on the build'))
