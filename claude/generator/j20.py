"""KJ20 „Darkspear“: kompakte Raketenpistole mit keilförmigem Schlitten und tiefem Fenster-Magazin."""
from eng import rect
import jlib
from jlib import K, X

BK, IC, GM, DK = '#242B30', '#ADEBF1', '#636D73', '#10161C'


def spec():
    return [
        K([(235,301),(287,301),(271,427),(208,435)],
          DK,-20,20,b=6,bz=5,label='Griff',
          dec=[([(242,326),(272,324),(263,405),(223,411)],GM,False)]),
        K([(209,424),(272,416),(288,431),(284,468),(215,476),(201,459)],
          BK,-23,23,b=5,bz=5,label='Raketenmagazin',glow=[((0,2,3),IC,3.6)],
          dec=[([(218,438),(271,431),(274,457),(218,464)],DK,False)]+
              [([(225+12*i,457),(228+12*i,440),(234+12*i,456)],GM,False) for i in range(4)]),
        K([(225,279),(443,277),(465,293),(449,315),(252,315),(225,306)],
          BK,-19,19,b=5,bz=5,label='Rahmen',glow=[((0,2,3),IC,3.6)]),
        K([(198,247),(219,234),(411,234),(458,249),(458,282),(207,282),(198,270)],
          BK,-23,23,b=6,bz=6,label='Schlitten',glow=[((0,1,2,4),IC,3.6)],
          dec=[([(345+21*i,249),(355+21*i,252),(350+21*i,269),(340+21*i,269)],DK,False) for i in range(4)]+
              [(rect(226,250,67,12),GM,False)]),
        K(rect(239,224,145,20),DK,-10,10,b=2,bz=2,label='Visierschiene',
          dec=[(rect(250+15*i,231,6,4),GM,False) for i in range(8)]),
        X(451,535,261,22,GM,n=8,label='Lauf',
          cap=[(261,0,15,'#060B10',False),(261,0,5,IC,True)]),
        K([(496,238),(524,239),(541,248),(541,274),(524,283),(496,284)],
          DK,-22,22,b=4,bz=4,label='Lauf',glow=[((0,4),IC,3.0)],
          xdec=[('x+',541,[(251,-10),(251,10),(271,10),(271,-10)],'#060B10',False),
                ('x+',541,[(257,-4),(257,4),(265,4),(265,-4)],IC,True)]),
        K([(310,316),(320,316),(332,348),(321,355)],
          GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(279,371),(377,367),(379,377),(278,382)],DK,-8,8,b=2,bz=2),
        K([(367,314),(378,314),(379,373),(367,373)],DK,-8,8,b=2,bz=2),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='20', name='Raketenpistole', nick='DARKSPEAR', col=IC,
    pill='POLARNACHT · EISBLAU · GUNMETAL', palette=[BK,IC,GM,DK], center=(369.5,350,0),
    desc='Eine gedrungene Raketenpistole mit tief geneigtem Griff und breitem Facettenschlitten. '
         'Der kurze Achtkantlauf endet in einer kantigen Mündungsmaske mit sichtbarer Raketenspitze. '
         'Unter dem Griff sitzt das keilförmige Raketenmagazin mit Fenster, über dem Schlitten eine fest eingelassene Visierschiene.',
    form='Keilschlitten mit Abgasschlitzen · eingelassene Visierschiene · Rahmen · geneigter Griff · '
         'Fenster-Raketenmagazin unter dem Griff · kurzer weiter Achtkantlauf mit Raketenspitze · freier Abzug im Bügel',
    op=dict(
        reload_de='Raketenmagazin unten aus dem Griff ziehen, volles Magazin mit sechs Mini-Raketen einsetzen und den Schlitten zurückziehen',
        action_de='Halbautomatik: Der Schlitten lädt nach jedem Schuss die nächste Rakete; Abgase entweichen durch die schrägen Schlitze',
        fire_de='Langsame Einzelschüsse; die Rakete zündet nach der Mündung und explodiert beim Aufprall mit Flächenschaden',
        reload_en='Pull the rocket magazine from the grip bottom, insert six fresh mini rockets and rack the slide',
        action_en='Semi-automatic: the slide chambers the next rocket after each shot; exhaust escapes through the angled slots',
        fire_en='Slow single shots; the rocket ignites beyond the muzzle and explodes on impact for area damage'))
