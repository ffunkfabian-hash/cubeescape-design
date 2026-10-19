"""KJ18 „Shiver“: dunkle Stangenwaffe mit langem Keilblatt und quer liegenden Schildflügeln."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#242C30', '#ACEDF2', '#606B72', '#10161C'


def Q(prof,col,y0,y1,**kw):
    """jlib-Facette in der x-z-Ebene, anschließend im Modell um x gedreht."""
    p=K(prof,col,-y1,-y0,**kw)
    p['quer']=True
    return p


def spec():
    p=[
        X(53,84,302,16,DK,n=8,label='Knauf'),
        X(80,656,302,9,GM,n=6,label='Stange'),
        K([(100,284),(190,284),(208,293),(208,314),(190,322),(100,322)],
          DK,-15,15,b=4,bz=4,label='Griff',
          dec=[(rect(114+17*i,291,7,23),GM,False) for i in range(5)]),
        K([(204,277),(266,277),(294,290),(294,326),(206,326),(196,314),(196,289)],
          BK,-18,18,b=5,bz=5,label='Gehäuse',glow=[((0,1,3),IC,3.6)]),
        K([(203,322),(232,322),(226,389),(198,389)],
          DK,-14,14,b=4,bz=4,label='Griff'),
        K([(246,327),(256,327),(267,351),(258,357)],
          GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(227,371),(295,371),(295,381),(227,381)],DK,-7,7,b=2,bz=2),
        K(rect(285,325,10,48),DK,-7,7,b=2,bz=2),
        K([(405,284),(477,284),(494,293),(494,314),(477,322),(405,322)],
          DK,-14,14,b=4,bz=4,label='Vordergriff',
          dec=[(rect(419+16*i,291,7,23),GM,False) for i in range(4)]),
        K([(556,277),(617,274),(638,287),(638,318),(617,330),(556,327)],
          BK,-19,19,b=5,bz=5,label='Energiezelle',glow=[((0,1,3,4),IC,3.6)],
          dec=[(rect(569+15*i,291,7,20),GM,False) for i in range(4)]),
        K([(635,263),(662,260),(678,278),(678,327),(662,343),(635,338)],
          DK,-26,26,b=5,bz=6,label='Klingenfassung'),
    ]
    # Beide beweglichen Flügel sind echte Querprofile; keine seitlichen Attrappen.
    for side in (-1,1):
        p.append(Q([(641,22*side),(670,22*side),(684,68*side),
                    (668,112*side),(649,112*side),(637,66*side)],
                   BK,279,324,b=3,bz=5,label='Schildflügel',glow=[((1,2,3,4),IC,3.6)]))
    p += [
        K([(674,272),(763,238),(842,250),(929,292),(929,308),
           (851,327),(718,349),(674,330)],
          BK,-6,6,b=4,bz=3,label='Klinge',glow=[((0,1,2,4,5,6),IC,3.6)],
          dec=[([(706,284),(774,260),(820,265),(766,280)],GM,False)]),
        X(674,911,302,4,DK,n=8,label='Emitter'),
        T(908,936,302,6,2,IC,n=8,emit=True,label='Emitter'),
    ]
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
    num='18', name='Glefe', nick='SHIVER', col=IC,
    pill='POLARNACHT · EISBLAU · GUNMETAL', palette=[BK,IC,GM,DK], center=(494.5,313.5,0),
    desc='Ein langes asymmetrisches Keilblatt krönt die zweihändige Sechskantstange. '
         'Zwei breite, quer liegende Facettenflügel klappen am Klingenkopf zum Schild aus. '
         'Der Emitter verläuft durch die Klinge bis zur hellen Spitze; Energiezelle, Vordergriff und freier Abzugbereich gliedern die Stange.',
    form='Sechskantstange mit Achtkantknauf · hinterer Griff und Abzug im Bügel · Vordergriff · Energiezelle · '
         'Klingenfassung mit zwei Schildflügeln · geknickte Keilklinge · Emitter bis zur Spitze · kein Visier',
    op=dict(
        reload_de='Energiezelle vor dem Klingenkopf durch Nahkampftreffer laden; zum Nachladen Zelle drehen und einrasten (4 Schuss)',
        action_de='Abzug verschießt ein Energiegeschoss; beim Blocken klappen beide Schildflügel quer zur Stange aus und spannen den Schild',
        fire_de='Klingenhiebe und Energiegeschosse aus der Hüfte ohne Visier; der ausgeklappte Schild hält Treffer ab',
        reload_en='Melee hits charge the cell ahead of the blade mount; twist and lock the cell to reload (four shots)',
        action_en='The trigger fires an energy bolt; guarding unfolds both transverse shield wings and raises the shield',
        fire_en='Blade swings and hip-fired energy shots without a sight; the deployed shield absorbs hits'))
