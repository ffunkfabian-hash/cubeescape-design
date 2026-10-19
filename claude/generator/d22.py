"""KD22 „Felsenbrecher“: schwere D-Slug-Flinte mit gerundetem Laufmantel."""
from tlib import B, rail
from eng import rect, roundpoly
from dmodels import arcband
import math

P, DK, K, A, AL = '#D8DCE0', '#2A2F38', '#1C2027', '#C39A63', '#FBE4C3'


def model():
    b = B(); D = b.D
    b.P([(90,246),(170,246),(224,266),(224,326),(174,326),(108,354),(90,354)],
        DK,-26,26,r=12,L='Schaft',
        dec=[D(roundpoly(rect(108,258,84,24),9),P),D(roundpoly(rect(110,312,50,10),4),K)])
    b.P(rect(76,240,20,124),K,-29,29,r=8,L='Schaftkappe')
    b.P([(210,234),(432,228),(472,250),(472,340),(230,340),(210,320)],
        DK,-36,36,r=12,L='Gehäuse',
        dec=[D(roundpoly([(232,250),(410,244),(440,258),(440,286),(232,294)],10),P),
             D(roundpoly(rect(248,263,144,10),5),A,True),
             D(roundpoly(rect(238,314,164,12),5),K)])
    rail(b,244,408,236,K,DK,w=14)
    b.P(rect(314,288,34,14),K,34,50,r=6,L='Ladehebel',
        dec=[D(roundpoly(rect(322,291,18,7),3),A)])
    b.P([(406,336),(460,336),(472,424),(414,430)],K,-24,24,r=10,L='Magazin',
        dec=[D(roundpoly([(418,350),(450,350),(456,412),(424,414)],8),P),
             D(roundpoly(rect(424,356,24,50),6),K)]+
            [D(roundpoly(rect(426,360+14*i,20,8),3),A) for i in range(3)])
    b.P([(462,254),(586,254),(606,272),(606,316),(588,336),(462,336)],
        DK,-30,30,r=12,L='Laufmantel',
        dec=[D(roundpoly(rect(480,264,102,18),7),P)]+
            [D(roundpoly(rect(484+26*i,294,14,26),5),K) for i in range(4)]+
            [D(roundpoly(rect(486+26*i,298,10,4),2),A,True) for i in range(4)])
    b.C(598,684,294,16,K,n=12,L='Lauf')
    b.C(678,718,294,24,DK,n=12,L='Mündungsbremse',
        cap=[(294,0,11,K,False)]+
            [(294+12*math.sin(k*math.pi/3),12*math.cos(k*math.pi/3),1.7,A,False) for k in range(6)])
    for z0,z1 in ((21,25),(-25,-21)):
        strip=D(roundpoly(rect(688,286,20,6),3),K)
        b.P(rect(684,282,28,24),DK,z0,z1,r=6,L='Mündungsbremse',
            dec=[strip] if z0>0 else (),xdec=[('z-',z0,*strip)] if z0<0 else ())
    b.P([(260,338),(310,338),(330,438),(274,444)],K,-23,23,r=12,L='Griff',
        dec=[D(roundpoly([(280,358),(296,358),(311,418),(296,420)],6),DK)])
    b.P(arcband(310,392,338,68,10),DK,-8,8,L='Abzugbügel')
    b.m.parts[-1].update(nohull=True,hull=False)
    b.P([(330,339),(343,339),(355,380),(342,386)],A,-6,6,r=4,L='Abzug')
    b.P([(520,334),(556,334),(554,404),(526,410)],DK,-19,19,r=10,L='Vordergriff',
        dec=[D(roundpoly(rect(534,350,10,36),4),A,True)])
    return b.m


META=dict(num='22',name='Slug-Schrotflinte',nick='FELSENBRECHER',col=A,
 pill='RELIKT-SKIN',palette=[P,DK,A,AL],center=(398,336,0),
 desc='Eine kompakte Slug-Flinte mit tiefem Schulterblock und schwerem, weich gerundetem Laufmantel. Helle Deckplatten und sandfarbene Leuchtstreifen gliedern die dunklen Massen; das Kastenmagazin zeigt drei Slug-Köpfe, der gezogene Lauf endet in einer breiten Mündungsbremse.',
 form='Tiefer Schulterblock · breites Gehäuse mit heller Deckplatte · Ladehebel links · Kastenmagazin mit Slug-Fenster · gerundeter Laufmantel · gezogener Lauf · Mündungsbremse mit sechs Zügen · gebogener Bügel · Vordergriff',
 op=dict(reload_de='Kastenmagazin vor dem Abzug wechseln (5 Slug-Patronen), danach Ladehebel links zurückziehen.',
         action_de='Halbautomatik: ein Einzelgeschoss je Abzug; der Ladehebel spannt nach dem Magazinwechsel.',
         fire_de='Schweres Einzelgeschoss mit hoher Wucht und Präzision auf mittlere Distanz, ohne Streukegel.',
         reload_en='Swap the five-round slug box magazine ahead of the trigger, then pull the left charging handle.',
         action_en='Semi-automatic: one slug per trigger pull; use the charging handle after a magazine change.',
         fire_en='A heavy single slug delivers high impact and precision at medium range without a spread cone.'))
