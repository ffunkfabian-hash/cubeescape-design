"""KJ22 RIMELOCK: Slug-Flinte mit tiefem Keilschaft und langem Sechskantlauf."""
from eng import rect
import jlib
from jlib import K, X, T

BK, IC, GM, DK = '#252D30', '#B7EDF3', '#606A6E', '#10161B'


def spec():
    return [
        K([(75,274),(92,266),(105,275),(105,368),(88,379),(75,367)],
          DK,-17,17,b=4,bz=5,label='Schaftkappe'),
        K([(100,278),(156,269),(242,286),(248,315),(176,345),(100,366)],
          BK,-15,15,b=6,bz=6,label='Schaft',glow=[((0,3),IC,3.6)],
          dec=[([(120,295),(154,289),(210,298),(169,319),(120,334)],DK,False)]),
        K([(230,255),(410,230),(454,238),(504,270),(497,307),(454,326),
           (230,326),(217,309),(217,273)],BK,-23,23,b=7,bz=8,label='Gehäuse',
          glow=[((0,1,4),IC,3.6)],
          dec=[([(265,273),(344,262),(360,274),(341,288),(265,294)],DK,False),
               ([(386,265),(433,261),(465,280),(397,288)],GM,False)]),
        K(rect(273,219,139,38),DK,-9,9,b=2,bz=3,label='Visierschiene',
          dec=[(rect(283+14*i,226,5,4),GM,False) for i in range(8)]),
        K([(307,277),(334,274),(346,283),(334,295),(309,295)],
          GM,22,36,b=2,bz=3,label='Ladehebel'),
        K([(260,326),(309,326),(294,419),(250,429),(241,414)],
          DK,-16,16,b=5,bz=5,label='Griff',
          dec=[([(268,345),(294,343),(281,400),(255,407)],GM,False)]),
        K([(326,325),(338,325),(350,359),(338,365)],GM,-5,5,b=1.5,bz=1.5,label='Abzug'),
        K([(301,375),(374,369),(382,379),(301,386)],DK,-7,7,b=2,bz=2),
        K([(373,326),(383,326),(383,379),(373,379)],DK,-7,7,b=2,bz=2),
        K([(413,326),(463,324),(479,395),(431,411)],BK,-15,15,b=5,bz=5,
          label='Magazin',glow=[((1,2),IC,3.6)],
          dec=[([(426,341),(452,337),(465,385),(440,394)],DK,False)]+
              [([(433+3*i,350+13*i),(452+3*i,345+13*i),(454+3*i,351+13*i),(435+3*i,356+13*i)],GM,False)
               for i in range(3)]),
        K([(428,406),(479,390),(486,401),(432,420)],GM,-16,16,b=2,bz=3,label='Magazinboden'),
        K([(493,268),(556,257),(607,269),(628,288),(604,307),(494,312)],
          BK,-18,18,b=5,bz=6,label='Laufmantel',glow=[((0,1,3),IC,3.6)],
          dec=[([(512+24*i,277),(526+24*i,274),(522+24*i,294),(508+24*i,297)],DK,False)
               for i in range(4)]),
        K([(535,311),(573,309),(565,375),(543,387),(530,374)],
          DK,-13,13,b=4,bz=4,label='Vordergriff',glow=[((1,2),IC,3.0)]),
        X(620,770,286,10,GM,n=6,label='Lauf'),
        X(624,640,286,13,DK,n=8,label='Laufbund'),
        T(764,782,286,12,18,BK,n=6,label='Mündungsbremse'),
        K([(778,268),(814,268),(829,278),(829,294),(814,304),(778,304)],
          DK,-18,18,b=3,bz=4,label='Mündungsbremse',glow=[((0,4),IC,3.0)],
          dec=[(rect(787+9*i,279,4,14),GM,False) for i in range(3)],
          xdec=[('x+',829,[(280,-6),(280,6),(292,6),(292,-6)],'#06090C',False)]),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='22',name='Slug-Schrotflinte',nick='RIMELOCK',col=IC,
    pill='NACHTSCHIEFER · RAUFEIS · GUNMETAL',palette=[BK,IC,GM,DK],center=(452.0, 324.0, 0),
    desc='Ein tief angesetzter Keilschaft und ein nach vorn abfallender Facettenrücken geben der Black-Ice-Slugflinte ihre Silhouette; '
         'Der kurze Laufmantel lässt viel vom schweren Sechskantlauf frei. Das geneigte Kastenmagazin zeigt drei Slug-Köpfe; '
         'Vordergriff und Mündungsbremse bleiben klar vom freien Abzugbügel getrennt.',
    form='Tiefer Keilschaft · Facettengehäuse mit Eis-Leuchtkanten · Ladehebel links · verbundene Visierschiene · '
         'Kastenmagazin mit Slug-Fenster · kurzer Laufmantel · langer Sechskantlauf · Mündungsbremse · Vordergriff',
    op=dict(
        reload_de='Fünf-Schuss-Kastenmagazin vor dem Abzug nach unten wechseln und den linken Ladehebel zurückziehen',
        action_de='Halbautomatik: Der Verschluss lädt nach jedem Schuss selbsttätig einen einzelnen Slug nach',
        fire_de='Ein schweres Einzelgeschoss je Abzug, präzise auf mittlere Distanz; kein Streukegel',
        reload_en='swap the five-round box magazine ahead of the trigger and pull the left charging handle',
        action_en='semi-automatic: the bolt chambers a single slug after each shot',
        fire_en='one heavy slug per pull, precise at medium range with no spread cone'))
