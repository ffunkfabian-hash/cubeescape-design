"""KG17 Schwert „Kantenlicht“ (claude-0.10): Energieschwert für den Nahkampf (Destiny: Sword, schwere Munition).
Keine Feuerwaffe: Klinge mit leuchtender Schneide, Parierstange mit Energiezelle (Ladungen), langer Griff, Knauf. Kein Visier, keine Schiene."""
from tlib import B
from eng import rect,roundpoly,circ
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.C(120,146,300,17,AN,n=8,L='Knauf',cap=[(300,0,7,OR,True)])
    b.P(rect(146,286,126,28),DK,-13,13,r=8,L='Griff',dec=[D(rect(160+18*i,287,8,26),AN) for i in range(6)])
    # Parierblock mit Energiezelle, Parierstange quer
    b.P([(268,258),(318,262),(318,338),(268,342)],CR,-22,22,r=6,L='Parierblock',
        dec=[D(roundpoly(rect(278,280,30,40),4),AN)])
    b.P(rect(282,284,22,32),CY,-24,24,r=3,emit=True,L='Energiezelle')
    b.Y([(272,-62),(300,-48),(314,-48),(314,48),(300,48),(272,62)],AN,284,316,r=3,L='Parierstange')
    # Klinge: Mittelrippe, flache Klinge mit leuchtender Schneide, Spitze
    b.P([(318,276),(760,270),(872,300),(760,330),(318,324)],CR,-4,4,r=2,L='Klinge',
        dec=[D([(330,318),(760,323),(856,300),(866,300),(760,328),(330,322)],CY,True),
             D(roundpoly(rect(360,296,300,8),3),AN)])
    b.P([(318,290),(700,292),(740,300),(700,308),(318,310)],AN,-7,7,r=2,L='Mittelrippe')
    b.P(rect(330,280,40,40),OR,-8,8,r=4)          # Klingenwurzel
    return b.m
META=dict(num='17',name='Schwert',nick='KANTENLICHT',col='#6FD8E0',pill='CREME · ANTHRAZIT · CYAN',
 palette=[CR,AN,CY,OR],center=(496,300,0),
 desc='Energieschwert für den Nahkampf: Die lange cremefarbene Klinge hat eine anthrazitfarbene Mittelrippe und eine cyan leuchtende Schneide. Im Parierblock steckt die Energiezelle für die Ladungen, quer darüber liegt die Parierstange; hinten ein langer umwickelter Griff mit Knauf.',
 form='Lange Klinge mit Mittelrippe · leuchtende Schneide · Klingenwurzel · Parierblock mit Energiezelle · Parierstange quer · umwickelter Griff · Knauf · kein Visier',
 op=dict(reload_de='kein Magazin: die Energiezelle im Parierblock hält die Ladungen für schwere Angriffe und wird mit schwerer Munition aufgefüllt',
         action_de='leichter Schlag ohne Ladung, schwerer Schlag verbraucht eine Ladung; Blocken mit der Klinge quer zieht Energie aus der Zelle',
         fire_de='Nahkampf: Schlagkombinationen, Sprungangriff; die Schneide leuchtet beim Blocken',
         reload_en='no magazine: the energy cell in the guard block holds the heavy-attack charges, refilled from heavy ammo',
         action_en='light swing without charge, heavy swing spends one charge; guarding with the blade drains the cell',
         fire_en='melee: swing combos, leaping strike; the edge lights up while guarding'))
