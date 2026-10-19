"""KJ16 DEEPFREEZE: flaches Gurt-MG mit Eiskiel-Schaft und langem Schlitzmantel."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#222B30', '#B1F1F4', '#626D73', '#10171C'


def spec():
    return [
        K([(52,258),(76,248),(95,261),(95,347),(72,364),(52,350)],
          DK,-19,19,b=4,bz=5,label='Schaftkappe'),
        K([(85,261),(195,265),(248,281),(248,312),(192,307),(85,286)],
          BK,-17,17,b=5,bz=5,label='Schaft',glow=[((0,1,3),IC,3.6)]),
        K([(85,340),(194,316),(242,299),(252,319),(198,342),(85,358)],
          BK,-17,17,b=4,bz=5,label='Schaft',glow=[((0,3),IC,3.6)]),
        K([(242,270),(426,253),(528,260),(560,279),(560,324),(523,343),(242,339)],
          BK,-27,27,b=7,bz=8,label='Gehäuse',glow=[((0,1,4,5),IC,3.6)],
          dec=[([(270,290),(345,283),(365,292),(350,306),(270,310)],DK,False),
               ([(479,281),(525,284),(539,296),(480,296)],GM,False)]),
        # Über die Gehäuseflanke greifender Deckel, hinten mit Sechskantscharnier.
        K([(307,248),(444,234),(483,244),(491,265),(307,279)],
          BK,-24,24,b=4,bz=6,label='Zuführdeckel',glow=[((0,1,3),IC,3.6)]),
        X(297,312,264,7,GM,n=6,label='Deckelscharnier'),
        K(rect(326,228,118,27),DK,-11,11,b=2,bz=3,label='Visierschiene',
          dec=[(rect(336+15*i,235,5,3),GM,False) for i in range(7)]),
        K([(473,299),(501,299),(511,308),(501,318),(473,318)],
          GM,26,40,b=2,bz=3,label='Ladehebel'),
        K([(396,308),(470,302),(486,321),(482,397),(397,408),(384,389)],
          BK,27,78,b=5,bz=7,label='Munitionskasten',glow=[((0,2,3),IC,3.6)],
          dec=[([(402,344),(468,338),(467,379),(402,389)],DK,False),
               ([(403,321),(463,315),(468,328),(402,335)],GM,False)]),
        K([(394,275),(451,270),(465,311),(405,319)],GM,27,41,b=2,bz=3,label='Patronengurt',
          dec=[([(402+8*i,279),(406+8*i,279),(415+8*i,308),(411+8*i,309)],DK,False) for i in range(6)]),
        K([(551,276),(738,266),(791,281),(803,304),(777,331),(551,326)],
          BK,-20,20,b=6,bz=6,label='Laufmantel',glow=[((0,1,3,4),IC,3.6)],
          dec=[([(577+26*i,285),(590+26*i,284),(582+26*i,309),(569+26*i,309)],DK,False) for i in range(8)]),
        # Hoher offener Tragbügel statt eines aufgeklebten Vollblocks.
        K([(590,238),(601,238),(607,278),(594,278)],DK,-7,7,b=2,bz=2,label='Tragegriff'),
        K([(695,236),(706,239),(711,273),(698,273)],DK,-7,7,b=2,bz=2,label='Tragegriff'),
        K([(585,229),(607,215),(683,212),(712,226),(707,240),(591,245)],
          BK,-10,10,b=3,bz=3,label='Tragegriff',glow=[((0,1,2),IC,3.0)]),
        X(793,873,295,9,GM,n=6,label='Lauf'),
        T(867,885,295,12,17,BK,n=6,label='Feuerdämpfer'),
        X(882,920,295,17,DK,n=6,label='Feuerdämpfer',cap=[(295,0,8,'#05090C',False)]),
        K(rect(697,325,17,23),GM,-17,17,b=3,bz=3,label='Zweibeinhalter'),
        X(705,790,344,4,DK,n=6,cz=12,label='Zweibein'),
        X(705,790,344,4,DK,n=6,cz=-12,label='Zweibein'),
        K([(280,336),(326,336),(313,428),(270,436)],DK,-18,18,b=4,bz=5,label='Griff',
          dec=[([(291,359),(313,358),(303,414),(281,421)],GM,False)]),
        K([(345,337),(356,337),(368,367),(356,375)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(322,389),(387,384),(395,395),(321,401)],DK,-7,7,b=2,bz=2),
        K([(384,338),(396,338),(396,395),(384,395)],DK,-7,7,b=2,bz=2),
        K([(609,327),(645,328),(632,400),(606,391)],DK,-14,14,b=4,bz=4,label='Vordergriff'),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='16',name='Maschinengewehr',nick='DEEPFREEZE',col=IC,
    pill='SCHIEFERNACHT · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(486,324,0),
    desc='Ein flaches Gurt-MG mit langem geschlitztem Keilmantel und hohem offenem Tragbügel. Ein kantiger Munitionskasten ist '
         'links abgesetzt; ein sichtbarer Gunmetal-Patronengurt führt in den aufgelegten Zuführdeckel. Zwei getrennte Zweibeinholme liegen unter dem Vorderteil.',
    form='Offener Eiskiel-Schaft · flaches Gehäuse · Zuführdeckel mit hinterem Scharnier · Ladehebel · Munitionskasten links · '
         'Patronengurt · Schlitzlaufmantel · offener Tragegriff · Sechskantlauf · Feuerdämpfer · gefaltetes Zweibein · Vordergriff · Visierschiene',
    op=dict(
        reload_de='Zuführdeckel hinten aufklappen, neuen Munitionskasten links einhängen, Gurt einlegen, Deckel schließen und Ladehebel ziehen',
        action_de='Gurtzuführung: Der Verschluss zieht bei jedem Schuss eine weitere Patrone unter den Zuführdeckel',
        fire_de='Dauerfeuer mit steigender Feuerrate beim Halten; Tragegriff zum Laufwechsel, Zweibein für abgestützte Feuerstöße',
        reload_en='open the feed cover on its rear hinge, hang a fresh ammo box on the left, lay in the belt, close the cover and pull the charging handle',
        action_en='belt feed: the bolt draws one more cartridge under the feed cover with every shot',
        fire_en='sustained automatic fire with a rising rate; carry handle for barrel swaps and folded bipod for supported bursts'))
