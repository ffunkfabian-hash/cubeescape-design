"""KG18 Glefe „Wellenbrecher“ (claude-0.10): Stangenwaffe mit Klinge und Energie-Emitter (Destiny: Glaive, Spezialmunition).
Unterschied zum Schwert (KG17): zweihändige Stange mit Abzug, Emitter in der Klinge verschießt Energiegeschosse, Schildflügel am
Klingenkopf bauen beim Blocken einen Schild auf. Kein Visier (Schuss aus der Hüfte)."""
from tlib import B,trigger_group
from eng import rect,roundpoly
CR,AN,OR,CY,DK='#EDE6D6','#2B2E33','#F07A1A','#6FD8E0','#17191D'
def model():
    b=B();D=b.D
    b.C(56,84,300,15,AN,n=8,L='Knauf',cap=[(300,0,6,OR,True)])
    b.C(84,640,300,10,AN,n=8,L='Stange')
    b.P(rect(100,287,96,26),DK,-12,12,r=8,L='Griff',dec=[D(rect(110+16*i,288,7,24),AN) for i in range(5)])
    # Abzugsgehäuse mit Ladeanzeige, Abzug im Bügel
    b.P([(196,280),(262,280),(270,292),(270,318),(196,320)],CR,-15,15,r=5,L='Gehäuse',
        dec=[D(roundpoly(rect(208,288,44,7),2),CY,True)])
    trigger_group(b,212,320,OR,AN,grip_x0=196,depth=30)
    b.P(rect(392,287,90,26),DK,-12,12,r=8,L='Vordergriff',dec=[D(rect(402+16*i,288,7,24),AN) for i in range(5)])
    # Energiezelle vor dem Klingenkopf
    b.P([(556,280),(626,280),(632,292),(632,310),(626,320),(556,320)],CR,-16,16,r=5,L='Energiezelle',
        dec=[D(roundpoly(rect(566+16*i,290,9,20),2),CY,True) for i in range(4)])
    # Klingenfassung mit Schildflügeln, Klinge mit Emitter
    b.P(rect(632,264,34,72),AN,-18,18,r=5,L='Klingenfassung')
    b.Y([(636,18),(662,18),(654,64),(640,64)],OR,272,328,r=2,L='Schildflügel')
    b.Y([(636,-18),(662,-18),(654,-64),(640,-64)],OR,272,328,r=2,L='Schildflügel')
    b.P([(666,268),(744,252),(860,272),(918,300),(860,318),(720,336),(666,332)],CR,-5,5,r=2,L='Klinge',
        dec=[D([(680,326),(720,330),(858,313),(906,300),(898,299),(856,308),(720,325),(680,321)],CY,True),D(roundpoly(rect(700,292,120,16),5),DK)])
    b.C(666,904,300,5,DK,n=8,L='Emitter')
    b.F(904,922,300,5,2,CY,n=8,emit=True)          # Emitterspitze an der Klingenspitze: hier tritt das Geschoss aus
    return b.m
META=dict(num='18',name='Glefe',nick='WELLENBRECHER',col='#6FD8E0',pill='CREME · ANTHRAZIT · CYAN',
 palette=[CR,AN,CY,OR],center=(487,300,0),
 desc='Zweihändige Stangenwaffe: Vorne sitzt eine breite cremefarbene Klinge mit leuchtender Schneide und einem Emitter, der Energiegeschosse verschießt. Die Klingenfassung trägt zwei orange Schildflügel, davor steckt die Energiezelle; hinten Griff mit Abzug, in der Mitte der Vordergriff.',
 form='Lange Stange mit Knauf · hinterer Griff mit Abzug im Bügel · Vordergriff · Energiezelle · Klingenfassung mit zwei Schildflügeln · breite Klinge mit Schneide · Emitter in der Klinge · kein Visier',
 op=dict(reload_de='Energiezelle vor der Klingenfassung lädt sich durch Nahkampftreffer; Nachladen: Zelle drehen und neu einrasten (4 Schuss)',
         action_de='Abzug: Energiegeschoss aus dem Emitter; Blocken: Schildflügel klappen aus und bauen einen Schild vor der Klinge auf',
         fire_de='Hiebe mit der Klinge, Fernschuss aus der Hüfte (kein Visier), Schild hält Treffer ab',
         reload_en='the energy cell ahead of the blade mount recharges on melee hits; reload by twisting the cell until it locks (4 shots)',
         action_en='trigger fires an energy bolt from the emitter; guarding unfolds the shield wings into a shield in front of the blade',
         fire_en='blade swings, hip-fired ranged shot (no sight), shield absorbs hits'))
