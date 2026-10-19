"""KC18 „Kelchwacht“: kelchförmiger Klingenkopf mit geschwungenen Schildflügeln."""
from eng import rect, roundpoly
from tlib import B, trigger_group

PF, ME, AP, DK = '#713E68', '#B69A58', '#C3EC82', '#241F2D'


def model():
    b = B()
    D = b.D
    b.C(55,83,300,17,ME,n=12,L='Knauf',cap=[(300,0,7,AP,True)])
    b.C(81,636,300,9,DK,n=12,L='Stange')
    b.P([(97,285),(126,280),(173,281),(199,291),(196,311),
         (168,318),(122,319),(97,313)],PF,-14,14,r=8,L='Griff',
        dec=[D(roundpoly(rect(110+16*i,287,7,26),3),DK) for i in range(5)])
    b.P([(194,282),(222,268),(253,272),(274,288),(275,309),
         (250,325),(197,321)],PF,-17,17,r=8,L='Gehäuse',
        dec=[D(roundpoly([(209,285),(231,280),(253,286),(251,292),(211,294)],3),AP,True)])
    trigger_group(b,213,310,ME,PF,grip_x0=195,depth=30)
    b.P([(385,289),(406,280),(453,281),(483,289),(485,310),
         (458,321),(405,321),(385,313)],PF,-14,14,r=8,L='Vordergriff',
        dec=[D(roundpoly(rect(402+16*i,288,7,25),3),DK) for i in range(5)])
    b.P([(546,285),(572,270),(612,272),(637,288),(637,312),
         (612,328),(573,330),(546,314)],ME,-19,19,r=8,L='Energiezelle',
        dec=[D(roundpoly(rect(562+16*i,288,9,25),3),AP,True) for i in range(4)])
    # Der Kelchstiel verbindet die Stange mit zwei auseinanderlaufenden Fassungsarmen.
    b.P([(628,285),(655,279),(681,291),(686,306),(655,321),
         (628,314)],PF,-22,22,r=8,L='Klingenfassung')
    b.P([(654,287),(674,263),(703,245),(739,234),(770,237),
         (770,250),(739,249),(711,258),(688,278),(676,297)],ME,-15,15,r=8,L='Klingenfassung')
    b.P([(654,313),(675,337),(706,356),(741,366),(773,362),
         (771,349),(740,351),(714,341),(689,323),(676,303)],ME,-15,15,r=8,L='Klingenfassung')
    # Quer aufgespannte, symmetrische Schildflügel: beide zusammenhängenden Teile tragen ihr Motion-Label.
    for s in (-1,1):
        b.Y([(648,20*s),(662,45*s),(666,77*s),(687,105*s),
             (718,123*s),(748,119*s),(767,100*s),(751,93*s),
             (730,103*s),(712,99*s),(694,80*s),(686,50*s),
             (677,18*s)],PF,282,318,r=9,L='Schildflügel',
            dec=[D(roundpoly([(662,28*s),(675,48*s),(681,77*s),
                              (700,99*s),(722,110*s),(741,107*s),
                              (731,114*s),(711,113*s),(690,100*s),
                              (674,78*s),(670,50*s)],4),AP,True)])
    # Die schmale Wurzel weitet sich erst vor dem Kelch zur Schneide; beidseits bleiben echte Fenster.
    b.P([(670,288),(722,272),(765,251),(812,245),(854,258),
         (899,283),(928,300),(898,319),(853,344),(812,355),
         (765,349),(721,328),(670,312)],PF,-6,6,r=9,L='Klinge',
        dec=[D(roundpoly([(728,323),(769,342),(811,349),(851,338),
                          (896,314),(916,300),(907,301),(893,308),
                          (846,329),(810,340),(772,334),(733,316)],4),AP,True),
             D(roundpoly([(750,278),(793,261),(821,261),(851,271),
                          (824,273),(794,270),(757,286)],4),ME)])
    b.C(668,911,300,5,DK,n=10,L='Emitter')
    b.F(907,930,300,6,2,AP,n=10,emit=True)
    return b.m


META = dict(
    num='18', name='Glefe', nick='KELCHWACHT', col=AP,
    pill='PFLAUME · MESSING · APFEL', palette=[PF,ME,AP,DK], center=(493,313,0),
    desc='Ein messingfarbener Kelch öffnet sich um die pflaumenfarbene Klinge. Die schmale Klingenwurzel lässt zwei Fenster in der '
         'Fassung frei; symmetrisch geschwungene Schildflügel spreizen sich quer zur Stange, apfelgrün leuchtet ihre Funktionskante.',
    form='Zweihändige Stange mit Knauf · hinterer Griff mit Abzug im Bügel · Vordergriff · Energiezelle · offene Kelchfassung · '
         'zwei geschwungene Schildflügel · breite Klinge mit leuchtender Schneide · Emitter mit Spitze',
    op=dict(
        reload_de='Nahkampftreffer laden die Energiezelle vor der Fassung; zum Nachladen Zelle drehen und für vier Schuss neu einrasten',
        action_de='Der Abzug löst ein Energiegeschoss aus; beim Blocken klappen beide Schildflügel aus und bilden den Schild',
        fire_de='Klingenhiebe, Energiegeschosse aus der Hüfte und ein Schild zum Abfangen von Treffern',
        reload_en='melee hits recharge the cell ahead of the mount; reload by twisting the cell until it locks for four shots',
        action_en='the trigger fires an energy bolt; guarding unfolds both shield wings to form a shield',
        fire_en='blade swings, hip-fired energy bolts and a shield that absorbs hits'))
