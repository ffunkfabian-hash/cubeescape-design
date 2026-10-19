"""KJ17 „Snowblind“: facettiertes Langschwert mit breiter, geknickter Eisschneide."""
from eng import rect
import jlib
from jlib import K, X

BK, IC, GM, DK = '#232C30', '#B9F1F3', '#606C72', '#10171C'


def spec():
    return [
        X(106,145,300,19,DK,n=8,label='Knauf'),
        K([(140,285),(266,285),(284,292),(284,308),(266,315),(140,315)],
          DK,-13,13,b=4,bz=4,label='Griff',
          dec=[(rect(155+19*i,291,8,18),GM,False) for i in range(6)]),
        # Breiter Querholm, dahinter der schlanke zweihändige Griff.
        K([(269,278),(292,268),(318,281),(318,319),(292,332),(269,322)],
          BK,-63,63,b=4,bz=7,label='Parierstange',glow=[((0,1,3,4),IC,3.6)]),
        K([(283,269),(325,273),(337,285),(337,315),(325,327),(283,331)],
          BK,-25,25,b=5,bz=5,label='Parierblock',glow=[((0,4),IC,3.6)]),
        K([(314,285),(329,283),(337,290),(337,310),(329,317),(314,315)],
          GM,-29,29,b=3,bz=3,label='Energiezelle',glow=[((0,2,4),IC,3.2)]),
        # Lange geknickte Schneide und abgestumpfte Meißelspitze statt G-Blattform.
        K([(329,274),(636,254),(796,260),(898,289),(898,305),
           (791,342),(624,334),(329,326)],
          BK,-6,6,b=4,bz=3,label='Klinge',glow=[((0,1,2,4,5,6),IC,3.6)],
          dec=[([(374,289),(610,274),(614,281),(374,296)],DK,False)]),
        K([(331,289),(690,286),(793,297),(793,304),(690,315),(331,311)],
          GM,-10,10,b=3,bz=3,label='Mittelrippe'),
        K([(332,279),(367,278),(378,288),(378,312),(366,323),(332,322)],
          DK,-12,12,b=3,bz=3,label='Klingenwurzel'),
    ]


def model():
    return jlib.model(spec())


META = dict(
    num='17', name='Schwert', nick='SNOWBLIND', col=IC,
    pill='POLARNACHT · EISWEISS · GUNMETAL', palette=[BK,IC,GM,DK], center=(502,298,0),
    desc='Ein langes Stealth-Schwert mit geknickter, breiter Klinge und kurzer Meißelspitze. '
         'Eine Gunmetal-Mittelrippe versteift die dunkle Klinge; eisweiße Leuchtkanten zeichnen ihre beiden Schneiden nach. '
         'Im breiten Parierholm sitzt der Parierblock mit Energiezelle, dahinter der lange Griff mit Achtkantknauf.',
    form='Geknickte Langklinge · Meißelspitze · Mittelrippe · Klingenwurzel · '
         'Parierblock mit Energiezelle · breite Parierstange quer · langer Griff · Achtkantknauf · kein Visier',
    op=dict(
        reload_de='Kein Magazin: Energiezelle im Parierblock mit schwerer Munition auffüllen; ihre Ladungen versorgen schwere Angriffe',
        action_de='Leichter Hieb ohne Ladung; schwerer Hieb verbraucht eine Ladung; Blocken mit quer gehaltener Klinge zieht Zellenergie',
        fire_de='Nahkampf mit Schlagfolgen und Sprungangriff; beim Blocken leuchten die geknickten Schneiden',
        reload_en='No magazine: refill the guard-block energy cell with heavy ammo; its charges power heavy attacks',
        action_en='Light swing costs no charge; heavy swing spends one; guarding with the blade held across the body drains the cell',
        fire_en='Melee swing chains and leaping strikes; the angular blade edges light up while guarding'))
