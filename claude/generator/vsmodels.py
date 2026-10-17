"""Visier-Serie VS01–VS09 (claude-0.6): ein Modell je Visier der Waffen 1–9, Zielbild der Visiere (Entscheidung des Nutzers 17.10.2026).

Ein Modell je Visier: Blatt (vsheet.py) und Sight-Spec (export_sight.py) lesen dieselben Teile, damit Ansichten und Daten
deckungsgleich sind. Ohne numpy (der Spec-Export braucht keine Bildstufe).

Modellrahmen wie bei den Waffenblättern (eng.Model): x = vorn (Blickrichtung), y = unten, z = links; Einheit 1 mm. Ursprung =
Socket_Mount (Unterkante Mitte der Halterung, liegt auf der Visierschiene der Waffe). Die Visierlinie läuft entlang x bei
(y = line_y, z = 0); keine Fläche außer Glas schneidet sie (geprüft im Spec, sight_line).

Zielbild: Cube Escape Docs/Images/EquipmentConcepts/weapon_sights_1-9.webp (Visier je Waffe) und sight_types_1-9.webp
(Visiertypen); Tabelle Docs/EQUIPMENT.md › Visiere je Waffe. Typen und Rahmen im Vokabular von claude-0.5.2 (weapon-spec.md ›
Visier-Vokabular).
"""
import math
from eng import Model,CHANNELS

# Grundfarben der Serie (Cube-Escape-Farbwelt wie Variante G und die Visier-Blätter: Creme, Anthrazit, Orange)
WHITE,DARK,METAL,ORANGE='#ECE6DA','#2B2E33','#6B7179','#F28C28'
RUBBER='#1A1C20'

# Glas-Tönungen des Visier-Blatts (Glas / Linsen Varianten): id -> (Name, sRGB, Deckkraft im Spiel)
TINTS={
 'clear':('Klar','#E4EEF5',0.08),
 'light':('Leicht getönt','#8FA6B8',0.20),
 'blue':('Blau','#3D9BEA',0.28),
 'orange':('Orange','#F2A33A',0.28),
 'red':('Rot','#E8463E',0.26),
 'green':('Grün','#3FC37A',0.26),
 'purple':('Lila','#9B5CF0',0.30),
 'mirror':('Gespiegelt','#C3D2E0',0.55),
}
# Fadenkreuze (Fadenkreuz-Varianten der Blätter): id -> Name. Nur Bild; das Fadenkreuz zeichnet Cube Escape zur Laufzeit.
RETICLES={
 'dot':'Punkt','circle':'Kreis','cross':'Kreuz','t_dot':'T-Dot','circle_cross':'Kreis-Kreuz','chevron':'Chevron',
 'target_field':'Zielfeld','fine':'Fein','mil_dot':'Mil-Dot','ballistic':'Ballistik','digital':'Digital','dynamic':'Dynamisch',
 'energy':'Energie','focus':'Fokus','tracking':'Tracking','quad':'Quad','box':'Box','lock_on':'Lock-On','grid':'Raster',
}
# Tech-Module des Visier-Blatts (optional, Stufe A höchstens eins je Visier)
MODULES={'night_vision':'Nachtsicht','rangefinder':'Entfernungsanzeige','target_marker':'Zielmarkierung','wind_compensation':'Windkompensation'}
FRAMES={'standard':'Standard','compact':'Kompakt','open':'Offen','closed':'Geschlossen','industrial':'Industrie','lightweight':'Leichtbau'}
TYPES_DE={'standard':'Standard-Visier','holo':'Holo-Visier','precision':'Präzisions-Visier','reflex':'Reflex-Visier','sniper':'Sniper-Visier',
 'machine':'Maschinenvisier','energy':'Energie-Visier','trace':'Spur-Visier','rocket':'Raketen-Visier'}

# ---------------------------------------------------------------- Bausteine
def loop(cy,cz,hh,hw,r,seg=5):
    """Umriss in der Ebene quer zur Visierlinie: Punkte (y, z) um (cy, cz), halbe Höhe hh, halbe Breite hw, Eckradius r.
    seg=1 ergibt Fasen (Achteck). Gleiche seg und gleiche Geradenlängen ergeben gleich viele Punkte (Ringe aus zwei Umrissen)."""
    r=min(r,hh,hw);pts=[]
    for q,(sz,sy) in enumerate(((1,1),(-1,1),(-1,-1),(1,-1))):
        oz,oy=cz+sz*(hw-r),cy+sy*(hh-r)
        for k in range(seg+1):
            a=math.radians(90*q+90*k/seg)
            pts.append((oy+r*math.sin(a),oz+r*math.cos(a)))
    out=[]
    for p in pts:
        if not out or abs(p[0]-out[-1][0])+abs(p[1]-out[-1][1])>1e-9:out.append(p)
    if abs(out[0][0]-out[-1][0])+abs(out[0][1]-out[-1][1])<=1e-9:out.pop()
    return out
def circle(cy,cz,R,n=32):return loop(cy,cz,R,R,R,seg=n//4)

def _wall_normal(a,b,c,outward=True):
    ey,ez=b[0]-a[0],b[1]-a[1];L=math.hypot(ey,ez) or 1.0
    ny,nz=ez/L,-ey/L
    my,mz=(a[0]+b[0])/2-c[0],(a[1]+b[1])/2-c[1]
    if (ny*my+nz*mz<0)==outward:ny,nz=-ny,-nz
    return (0.0,ny,nz)

class Sight:
    """Visiermodell: Teile wie eng.Model (Raster und Ansichten der Blätter), dazu Gruppen = logische Bauteile des Specs."""
    def __init__(s):s.m=Model();s.groups={};s.order=[]
    def group(s,g,label,channel,material,col,emit=False,glass=False,role=None):
        assert channel in CHANNELS,channel
        if g not in s.groups:
            s.groups[g]=dict(id=g,label=label,channel=channel,material=material,col=col,emit=emit,glass=glass,role=role);s.order.append(g)
        return s
    def _tag(s,g,n=1):
        G=s.groups[g]
        for P in s.m.parts[-n:]:
            P.update(label=G['label'],group=g,channel=G['channel'],col=G['col'],emit=G['emit'])
            if G['glass']:P['glass']=True
        return s
    def _part(s,g,F,hull=True):
        G=s.groups[g];s.m.parts.append(dict(F=F,col=G['col'],emit=G['emit'],dec=[],hull=hull));return s._tag(g)
    # Seitenprofil (x, y), durch die Breite z0..z1 extrudiert
    def prof(s,g,pts,z0,z1,r=0):s.m.prism(pts,s.groups[g]['col'],z0,z1,r=r);return s._tag(g)
    def box(s,g,x0,x1,y0,y1,z0,z1,r=0):return s.prof(g,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1,r=r)
    def boxes_lr(s,g,x0,x1,y0,y1,z0,z1,r=0):
        """zwei gleiche Teile links (z0..z1) und gespiegelt rechts"""
        return s.box(g,x0,x1,y0,y1,z0,z1,r=r).box(g,x0,x1,y0,y1,-z1,-z0,r=r)
    # Zylinder quer: Achse z (Knöpfe seitlich), Achse y (Türme oben)
    def knob_z(s,g,x,y,R,z0,z1,n=16):
        s.m.prism([(x+R*math.cos(2*math.pi*k/n),y+R*math.sin(2*math.pi*k/n)) for k in range(n)],s.groups[g]['col'],z0,z1,smooth=True);return s._tag(g)
    def knob_y(s,g,x,z,R,y0,y1,n=16):
        ring=[(x+R*math.cos(2*math.pi*k/n),z+R*math.sin(2*math.pi*k/n)) for k in range(n)]
        F=[dict(v=[(a,y0,b) for a,b in ring],n=(0,-1,0),hard=True),dict(v=[(a,y1,b) for a,b in ring[::-1]],n=(0,1,0),hard=True)]
        for i in range(n):
            (ax,az),(bx,bz)=ring[i],ring[(i+1)%n];mx,mz=(ax+bx)/2-x,(az+bz)/2-z;L=math.hypot(mx,mz)
            F.append(dict(v=[(ax,y0,az),(bx,y0,bz),(bx,y1,bz),(ax,y1,az)],n=(mx/L,0,mz/L),hard=False))
        return s._part(g,F)
    # Ring entlang der Visierlinie (Achse x): Außen- und Innenumriss gleicher Punktzahl; vier Teile (Stirn vorn, hinten, Mantel außen, innen),
    # damit die Konturen an den Kanten liegen und nicht zwischen den Facetten
    def ring(s,g,x0,x1,outer,inner):
        assert len(outer)==len(inner),(len(outer),len(inner))
        n=len(outer);c=(sum(p[0] for p in outer)/n,sum(p[1] for p in outer)/n);h=n//2
        for x,nx in ((x1,1.0),(x0,-1.0)):
            halves=[outer[:h+1]+inner[:h+1][::-1],outer[h:]+outer[:1]+(inner[h:]+inner[:1])[::-1]]
            s._part(g,[dict(v=[(x,y,z) for y,z in hv],n=(nx,0.0,0.0),hard=False) for hv in halves])
        for L,out in ((outer,True),(inner,False)):
            F=[]
            for i in range(n):
                a,b=L[i],L[(i+1)%n]
                F.append(dict(v=[(x0,a[0],a[1]),(x0,b[0],b[1]),(x1,b[0],b[1]),(x1,a[0],a[1])],n=_wall_normal(a,b,c,out),hard=False))
            s._part(g,F)
        return s
    def tube(s,g,x0,x1,cy,R,Ri,n=32):return s.ring(g,x0,x1,circle(cy,0,R,n),circle(cy,0,Ri,n))
    # Vollkörper entlang x mit Umriss (y, z)
    def slab(s,g,x0,x1,lp,hard_walls=False):
        n=len(lp);c=(sum(p[0] for p in lp)/n,sum(p[1] for p in lp)/n)
        F=[dict(v=[(x1,y,z) for y,z in lp],n=(1.0,0,0),hard=True),dict(v=[(x0,y,z) for y,z in lp[::-1]],n=(-1.0,0,0),hard=True)]
        for i in range(n):
            a,b=lp[i],lp[(i+1)%n]
            F.append(dict(v=[(x0,a[0],a[1]),(x0,b[0],b[1]),(x1,b[0],b[1]),(x1,a[0],a[1])],n=_wall_normal(a,b,c,True),hard=hard_walls))
        return s._part(g,F)
    # Glas: dünne Scheibe quer zur Visierlinie (beidseitig sichtbar), Umriss (y, z)
    def pane(s,g,x,lp):
        return s._part(g,[dict(v=[(x,y,z) for y,z in lp],n=(1.0,0,0),hard=True),dict(v=[(x,y,z) for y,z in lp[::-1]],n=(-1.0,0,0),hard=True)])

def mount(S,x0,x1,w,jaw=True):
    """Halterung auf der Visierschiene: Block, Klemmbacken bis 3 mm unter die Schienenoberkante, Klemmschraube links."""
    S.group('mount','Halterung','MT_Metal','brushed',METAL)
    S.box('mount',x0,x1,-6,0,-w/2,w/2,r=1.2)
    if jaw:S.boxes_lr('mount',x0+4,x1-4,0,3,w/2-3,w/2,r=0.6)
    S.group('screw','Klemmschraube','MT_Accent','painted',ORANGE).knob_z('screw',(x0+x1)/2,-2.6,2.4,w/2,w/2+2.6)
    return S

# ---------------------------------------------------------------- Visiere 1–9
def b_pistol(S,E):
    mount(S,-15,13,20)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-17,-6),(14,-6),(14,-13),(10,-15),(-13,-15),(-17,-12)],-11,11,r=1.6)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    S.prof('cover',[(-14,-7.5),(4,-7.5),(4,-13),(-11,-13),(-14,-10.5)],11,12.2,r=1.2).prof('cover',[(-14,-7.5),(4,-7.5),(4,-13),(-11,-13),(-14,-10.5)],-12.2,-11,r=1.2)
    ly=-26
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',5,11.5,loop(ly,0,11.5,12.5,4.5),loop(ly,0,9,10,2.5))
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',8.5,loop(ly,0,9.6,10.6,3))
    S.group('emitter','Emitter','MT_Energy','lit',E,emit=True).box('emitter',-11,-6,-16.4,-15,-2.2,2.2,r=0.5)
    S.group('button','Bedienknopf','MT_Accent','painted',ORANGE).box('button',-10,-4,-11,-8,12.2,13.6,r=0.6)
    return dict(line_y=ly,window=dict(shape='rect',x0=5,x1=11.5,glass_x=8.5,w=20,h=18,r=2.5))

def b_rifle(S,E):
    mount(S,-26,22,22)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-31,-6),(26,-6),(26,-14),(-27,-14),(-31,-11)],-12,12,r=2)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    for z0,z1 in ((12,13.3),(-13.3,-12)):S.prof('cover',[(-27,-7.5),(-6,-7.5),(-6,-12.6),(-24,-12.6),(-27,-10)],z0,z1,r=1.2)
    S.box('cover',-30,-14,-15.5,-14,-9,9,r=1.2)   # Batteriefach oben hinten (unter der Fensterunterkante)
    ly=-31
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',3,19,loop(ly,0,17,19.5,5),loop(ly,0,14.5,17,3))
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',16,loop(ly,0,15.1,17.6,3.4))
    S.group('emitter','Emitter','MT_Energy','lit',E,emit=True).box('emitter',-9,-3,-15.6,-14,-3,3,r=0.6)
    S.group('button','Bedienknopf','MT_Accent','painted',ORANGE)
    for z0,z1 in ((3,8),(-8,-3)):S.box('button',-28,-21,-16.3,-15.5,z0,z1,r=0.4)
    return dict(line_y=ly,window=dict(shape='rect',x0=3,x1=19,glass_x=16,w=34,h=29,r=3))

def _scope(S,E,ly,x_eye,x_tube0,x_tube1,x_obj1,R_tube,R_obj,R_eye,rings,turret_x,sleeve):
    """Röhre mit Objektiv vorn und Okular hinten: Röhre (Gehäuse), Hülse (Abdeckung), Objektiv und Augenring (Rahmen),
    Augenmuschel (Gummi), Linsen vorn und hinten (Glas). Alles hohl, die Visierlinie läuft durch die Achse."""
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.tube('housing',x_tube0,x_tube1,ly,R_tube,R_tube-2.6)
    S.tube('housing',x_tube1-4,x_tube1+4,ly,R_obj-3.6,R_tube-2.6)            # Übergang Röhre -> Objektiv
    S.tube('housing',x_eye+6,x_tube0+2,ly,R_eye,R_eye-4)                   # Okular
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE).tube('cover',sleeve[0],sleeve[1],ly,R_tube+1.2,R_tube)
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.tube('frame',x_tube1+4,x_obj1,ly,R_obj,R_obj-3.8)                    # Objektiv
    S.tube('frame',x_tube0-1,x_tube0+3,ly,R_eye+0.8,R_tube-2.6)            # Augenring
    S.group('eyecup','Augenmuschel','MT_Secondary','rubber',RUBBER).tube('eyecup',x_eye,x_eye+6,ly,R_eye-0.4,R_eye-3.4)
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',x_obj1-3,circle(ly,0,R_obj-3.5))          # Objektivlinse
    S.group('glass_eye','Okularglas','MT_Detail','glass',None,glass=True).pane('glass_eye',x_eye+7,circle(ly,0,R_eye-3.7))
    S.group('rings','Montageringe','MT_Metal','brushed',METAL)
    for xr in rings:
        S.tube('rings',xr-4,xr+4,ly,R_tube+2.6,R_tube+(1.2 if sleeve[0]<=xr<=sleeve[1] else 0))
        S.box('rings',xr-4,xr+4,ly+R_tube+1,-5.5,-6,6,r=1)
    S.group('turret','Verstellturm','MT_Secondary','painted',DARK)
    S.knob_y('turret',turret_x,0,6.5,ly-R_tube-10,ly-R_tube+0.5).knob_z('turret',turret_x,ly,6,R_tube-0.5,R_tube+9)
    S.group('cap','Turmkappe','MT_Accent','painted',ORANGE)
    S.knob_y('cap',turret_x,0,5.5,ly-R_tube-12,ly-R_tube-10).knob_z('cap',turret_x,ly,5,R_tube+9,R_tube+11)
    return dict(lens_r=R_obj-3.8,eye_r=R_eye-4,eye_x=x_eye+7,obj_x=x_obj1-3,x0=x_eye,x1=x_obj1,bore_r=R_tube-2.6)

def b_pulse(S,E):
    mount(S,-32,30,22)
    ly=-25
    t=_scope(S,E,ly,x_eye=-66,x_tube0=-44,x_tube1=40,x_obj1=62,R_tube=14.5,R_obj=21,R_eye=16.5,rings=(-24,20),turret_x=-2,sleeve=(-14,8))
    S.group('accent','Zierring','MT_Accent','painted',ORANGE).tube('accent',26,30,ly,15.6,14.5)
    module_rangefinder(S,x0=6,x1=28,y0=ly-8,y1=ly+6,z0=-15,z1=-25,E='#FF4A3D')
    return dict(line_y=ly,window=dict(shape='round',x0=t['x0'],x1=t['x1'],glass_x=t['obj_x'],w=2*t['lens_r'],h=2*t['lens_r'],r=t['lens_r']),
                tube=dict(x0=t['x0'],x1=t['x1'],lens_r=t['lens_r'],eye_r=t['eye_r'],eye_x=t['eye_x'],bore_r=t['bore_r']))

def b_shotgun(S,E):
    mount(S,-20,16,24)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-25,-6),(18,-6),(18,-13),(-20,-15),(-25,-12)],-14,14,r=2)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    for z0,z1 in ((14,15.3),(-15.3,-14)):S.prof('cover',[(-22,-7.5),(-2,-7.5),(-2,-12.8),(-19,-13.6),(-22,-11)],z0,z1,r=1.2)
    ly=-36
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',2,16,circle(ly,0,24.5),circle(ly,0,20.5))
    S.group('bezel','Rückring','MT_Secondary','painted',DARK).ring('bezel',-3,2,circle(ly,0,23),circle(ly,0,20.5))
    S.box('housing',-1,15,-15,-11.5,-9,9,r=1.5)   # Sockel unter dem Ring
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',12,circle(ly,0,21.2))
    S.group('emitter','Emitter','MT_Energy','lit',E,emit=True).box('emitter',-15,-9,-15.3,-14,-2.5,2.5,r=0.5)
    S.group('button','Bedienknopf','MT_Accent','painted',ORANGE).knob_z('button',-12,-10,3.6,-17.5,-14)
    return dict(line_y=ly,window=dict(shape='round',x0=-3,x1=16,glass_x=12,w=41,h=41,r=20.5))

def b_sniper(S,E):
    mount(S,-56,52,22)
    ly=-27
    t=_scope(S,E,ly,x_eye=-104,x_tube0=-76,x_tube1=60,x_obj1=104,R_tube=15.5,R_obj=26.5,R_eye=18,rings=(-42,36),turret_x=-4,sleeve=(-26,22))
    S.group('accent','Zierring','MT_Accent','painted',ORANGE).tube('accent',50,54,ly,16.7,15.5)
    module_wind(S,x0=-20,x1=8,y0=ly-6,y1=ly+9,z0=-16.5,z1=-27,E=E)
    return dict(line_y=ly,window=dict(shape='round',x0=t['x0'],x1=t['x1'],glass_x=t['obj_x'],w=2*t['lens_r'],h=2*t['lens_r'],r=t['lens_r']),
                tube=dict(x0=t['x0'],x1=t['x1'],lens_r=t['lens_r'],eye_r=t['eye_r'],eye_x=t['eye_x'],bore_r=t['bore_r']))

def b_smg(S,E):
    mount(S,-22,20,22)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-27,-6),(24,-6),(24,-12),(-23,-12),(-27,-10)],-13,13,r=2)
    ly=-30
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    S.ring('cover',-4,18,loop(ly,0,18,20.5,4.5),loop(ly,0,15,17.5,2.5))          # Haube (geschlossener Tunnel)
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',18,22.5,loop(ly,0,18.6,21.1,5),loop(ly,0,15,17.5,2.5))
    S.group('bezel','Rückring','MT_Secondary','painted',DARK).ring('bezel',-8,-4,loop(ly,0,18.6,21.1,5),loop(ly,0,15,17.5,2.5))
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',19.5,loop(ly,0,15.6,18.1,3))
    S.group('emitter','Emitter','MT_Energy','lit',E,emit=True).box('emitter',-18,-11,-13.4,-12,-2.6,2.6,r=0.5)
    S.group('button','Bedienknopf','MT_Accent','painted',ORANGE).box('button',-20,-13,-10.5,-7.5,-14.4,-13,r=0.6)
    return dict(line_y=ly,window=dict(shape='rect',x0=-8,x1=22.5,glass_x=19.5,w=35,h=30,r=2.5))

def b_fusion(S,E):
    mount(S,-28,26,24)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-33,-6),(30,-6),(30,-14),(-28,-16),(-33,-13)],-14,14,r=2)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    for z0,z1 in ((14,15.3),(-15.3,-14)):S.prof('cover',[(-30,-7.5),(-6,-7.5),(-6,-13.6),(-27,-14.6),(-30,-12)],z0,z1,r=1.2)
    ly=-34
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',4,20,loop(ly,0,19.5,23.5,8,seg=1),loop(ly,0,16,20,6.5,seg=1))
    S.group('bezel','Rückring','MT_Secondary','painted',DARK).ring('bezel',0,4,loop(ly,0,19,23,7.8,seg=1),loop(ly,0,16,20,6.5,seg=1))
    S.group('energy_frame','Leuchtrahmen','MT_Energy','lit',E,emit=True)
    S.ring('energy_frame',15.5,17.5,loop(ly,0,16.1,20.1,6.6,seg=1),loop(ly,0,14.4,18.4,5.9,seg=1))
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',14.5,loop(ly,0,16.4,20.4,6.7,seg=1))
    S.group('cell','Energiezelle','MT_Secondary','painted',DARK).box('cell',-26,-4,-18.4,-7,14,21,r=2)   # unter der Fensterunterkante
    S.group('cell_glow','Ladeanzeige','MT_Energy','lit',E,emit=True).box('cell_glow',-22,-8,-15.8,-10.2,21,21.8,r=0.4)
    return dict(line_y=ly,window=dict(shape='octagon',x0=0,x1=20,glass_x=14.5,w=36.8,h=28.8,r=5.9))

def b_trace(S,E):
    mount(S,-24,20,22)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-29,-6),(22,-6),(22,-12),(-24,-14),(-29,-12)],-12,12,r=2)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    for z0,z1 in ((12,13.3),(-13.3,-12)):S.prof('cover',[(-26,-7.5),(-4,-7.5),(-4,-11.6),(-22,-12.8),(-26,-11)],z0,z1,r=1.2)
    ly=-28
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',8,13,loop(ly,0,16,20,3),loop(ly,0,14.2,18.2,2))
    S.group('struts','Stütze','MT_Secondary','painted',DARK)
    for z in (15.5,-15.5):S.box('struts',-2,10,-13,-11.4,z-1.6,z+1.6,r=0.5).box('struts',-2,0,-13.6,-11.4,z-1.6,z+1.6,r=0.4)   # unter der Fensterunterkante
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',10.5,loop(ly,0,14.8,18.8,2.4))
    S.group('marker','Markierungsrahmen','MT_Energy','lit',E,emit=True)
    for sy in (1,-1):
        for sz in (1,-1):
            cy,cz=ly+sy*15.1,sz*19.1     # Ecken auf der Stirn des Rahmens (zwischen Innen- und Außenkante), nicht in der Öffnung
            S.box('marker',13,13.8,cy-0.6,cy+0.6,min(cz+sz*0.6,cz-sz*6.5),max(cz+sz*0.6,cz-sz*6.5))
            S.box('marker',13,13.8,min(cy-sy*0.6,cy-sy*6.5),max(cy-sy*0.6,cy-sy*6.5),cz-0.6,cz+0.6)
    module_marker(S,x0=-20,x1=2,y0=-13.6,y1=-3,z0=12,z1=19,E='#FF4A3D')   # unter der Fensterunterkante, verdeckt das Sichtfeld nicht
    return dict(line_y=ly,window=dict(shape='rect',x0=8,x1=13.8,glass_x=10.5,w=36.4,h=28.4,r=2))

def b_rocket(S,E):
    mount(S,-30,30,26)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK)
    S.prof('housing',[(-37,-6),(36,-6),(36,-15),(-30,-17),(-37,-14)],-17,17,r=2)
    S.group('cover','Abdeckung','MT_Primary','painted',WHITE)
    for z0,z1 in ((17,19),(-19,-17)):S.prof('cover',[(-33,-7.5),(30,-7.5),(30,-14),(-29,-15.6),(-33,-12.5)],z0,z1,r=1.4)
    ly=-36
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE)
    S.ring('frame',6,24,loop(ly,0,21,37,4),loop(ly,0,16,32,2))
    S.group('bezel','Rückring','MT_Secondary','painted',DARK).ring('bezel',1,6,loop(ly,0,20,36,3.6),loop(ly,0,16,32,2))
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',20,loop(ly,0,16.6,32.6,2.4))
    S.group('bolts','Schrauben','MT_Metal','brushed',METAL)
    for sy in (1,-1):
        for sz in (1,-1):S.box('bolts',24,25.6,ly+sy*18.5-1.5,ly+sy*18.5+1.5,sz*34.5-1.5,sz*34.5+1.5,r=0.5)
    S.group('emitter','Emitter','MT_Energy','lit',E,emit=True).box('emitter',-20,-12,-18.4,-16.4,-3,3,r=0.5)
    module_rangefinder(S,x0=8,x1=24,y0=ly-21-11,y1=ly-21+0.5,z0=-9,z1=9,E='#FF4A3D',top=True)
    return dict(line_y=ly,window=dict(shape='rect',x0=1,x1=24,glass_x=20,w=64,h=32,r=2))

# ---------------------------------------------------------------- Tech-Module (Seitenmodul an einer Klemme)
def _module_body(S,g,label,x0,x1,y0,y1,z0,z1,lens_col,top=False):
    zl,zh=min(z0,z1),max(z0,z1)
    S.group(g,label,'MT_Secondary','painted',DARK).box(g,x0,x1,y0,y1,zl,zh,r=1.6)
    S.group(g+'_lens',label+' · Linse','MT_Emission','lit',lens_col,emit=True)
    cy=(y0+y1)/2;cz=(zl+zh)/2;R=min(y1-y0,zh-zl)*0.28
    S.slab(g+'_lens',x1,x1+1.2,circle(cy,cz,R,16))
    S.group(g+'_clamp',label+' · Klemme','MT_Metal','brushed',METAL)
    if top:S.box(g+'_clamp',x0+3,x1-3,y1,y1+2.5,-4,4,r=0.5)
    else:
        zz=(zl-1.5,zl) if z0>0 or zl>0 else (zh,zh+1.5)
        S.box(g+'_clamp',x0+3,x1-3,cy-3,cy+3,*zz,r=0.4)
    return S
def module_rangefinder(S,x0,x1,y0,y1,z0,z1,E,top=False):
    S.module='rangefinder';return _module_body(S,'module','Entfernungsanzeige',x0,x1,y0,y1,z0,z1,E,top)
def module_wind(S,x0,x1,y0,y1,z0,z1,E):
    S.module='wind_compensation';_module_body(S,'module','Windkompensation',x0,x1,y0,y1,z0,z1,E)
    S.group('module_knob','Windkompensation · Rad','MT_Accent','painted',ORANGE)
    return S.knob_z('module_knob',(x0+x1)/2-4,(y0+y1)/2,4,min(z0,z1)-2.5,min(z0,z1))
def module_marker(S,x0,x1,y0,y1,z0,z1,E):
    S.module='target_marker';return _module_body(S,'module','Zielmarkierung',x0,x1,y0,y1,z0,z1,E)

# ---------------------------------------------------------------- Serie
# num, Waffe (Toolgen-Id), Typ, Rahmen, Glas, Leucht-/Fadenkreuzfarbe, Fadenkreuze (Reihenfolge wie im Visier-Blatt), Bau, Kurztext
SERIES=[
 dict(num='01',weapon='Pistole',tid='pistol',type='reflex',frame='compact',tint='blue',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['dot','circle','cross','t_dot'],build=b_pistol,
      title='Kompaktes Reflex-Visier',desc='Kompaktes Reflex-Visier mit offenem Fenster: Rahmen vorn, hinten offen, Emitter auf dem Gehäuse unter der Visierlinie.'),
 dict(num='02',weapon='Sturmgewehr',tid='assault_rifle',type='holo',frame='open',tint='light',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['circle','circle_cross','chevron','dot'],build=b_rifle,
      title='Offenes Holo-Visier',desc='Offenes Holo-Visier: großer Rahmen mit Scheibe vorn, beidseitig offen, Projektor hinten im Gehäuse, Batteriefach oben.'),
 dict(num='03',weapon='Impulsgewehr',tid='pulse_rifle',type='precision',frame='standard',tint='blue',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['circle','dot','circle_cross','target_field'],build=b_pulse,
      title='Präzisions-Röhre mit Linse',desc='Präzisions-Visier für mittlere Distanz: hohle Röhre mit Objektiv und Okular, zwei Montageringe, Entfernungsanzeige rechts.'),
 dict(num='04',weapon='Schrotflinte',tid='shotgun',type='reflex',frame='standard',tint='blue',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['fine','mil_dot','ballistic','digital'],build=b_shotgun,
      title='Weitwinkel-Reflex-Visier',desc='Weitwinkel-Reflex-Visier: großes rundes Fenster auf kurzem Gehäuse, Rückring, Emitter unter der Visierlinie.'),
 dict(num='05',weapon='Scharfschützengewehr',tid='sniper_rifle',type='sniper',frame='standard',tint='blue',energy='#5CC8FF',hud='#FF8A2A',
      reticles=['fine','mil_dot','ballistic','digital'],build=b_sniper,
      title='Hochpräzisions-Röhre',desc='Hochpräzisions-Visier: lange Röhre mit großem Objektiv, Verstelltürme oben und links, Windkompensation rechts.'),
 dict(num='06',weapon='Maschinenpistole',tid='smg',type='machine',frame='closed',tint='blue',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['dot','circle','chevron','dynamic'],build=b_smg,
      title='Maschinenvisier',desc='Maschinenvisier, kompakt und schnell: geschlossene Haube als Tunnel mit erweitertem Sichtfeld, Scheibe vorn.'),
 dict(num='07',weapon='Fusionsgewehr',tid='fusion_rifle',type='energy',frame='closed',tint='purple',energy='#5CC8FF',hud='#5CC8FF',
      reticles=['digital','circle','energy','focus'],build=b_fusion,
      title='Energie-Visier mit Energierahmen',desc='Energie-Visier: breites Achteck-Fenster mit aktivem Leuchtrahmen, Energiezelle links.'),
 dict(num='08',weapon='Spurgewehr',tid='scout_rifle',type='trace',frame='lightweight',tint='blue',energy='#5CC8FF',hud='#7FD8FF',
      reticles=['tracking','quad','circle','box'],build=b_trace,
      title='Fenster mit Markierungsrahmen',desc='Zielverfolgungs-Visier ohne Röhre (Entscheidung des Nutzers): Leichtbau-Rahmen, vier Markierungsecken, Zielmarkierung links.'),
 dict(num='09',weapon='Raketenwerfer',tid='rocket_launcher',type='rocket',frame='industrial',tint='blue',energy='#FF8A2A',hud='#FF8A2A',
      reticles=['target_field','circle','lock_on','grid'],build=b_rocket,
      title='Weitbereichs-Visier',desc='Weitbereichs-Visier: breites Fenster im verschraubten Industrie-Rahmen, Entfernungsanzeige oben.'),
]
IDS=[f'VS{s["num"]}' for s in SERIES]
BY_ID={f'VS{s["num"]}':s for s in SERIES}

def load(vid):
    """Modell und Daten eines Visiers: dict(S=Sight, info=Serie-Eintrag, geo=Fenster/Röhre/Visierlinie)."""
    info=BY_ID[vid];S=Sight();S.module=None
    geo=info['build'](S,info['energy'])
    set_tint(S,info['tint'])
    # Ursprung = Mitte der Halterung (längs): Modell und Fensterdaten um deren x-Mitte verschieben
    mb=[q[0] for P in S.m.parts if P['group']=='mount' for f in P['F'] for q in f['v']];dx=(min(mb)+max(mb))/2
    if abs(dx)>1e-9:
        for P in S.m.parts:
            for f in P['F']:f['v']=[(x-dx,y,z) for x,y,z in f['v']]
        for k in ('x0','x1','glass_x'):geo['window'][k]-=dx
        if geo.get('tube'):
            for k in ('x0','x1','eye_x'):geo['tube'][k]-=dx
    return dict(S=S,info=info,geo=geo,id=vid)
def set_tint(S,tint):
    """Glasfarbe (Zeichnung) = Farbe der Tönung"""
    c=TINTS[tint][1]
    for P in S.m.parts:
        if P.get('glass'):P['col']=c
    for G in S.groups.values():
        if G['glass']:G['col']=c
    return S

def aperture_loop(geo,margin=0.3):
    """freie Öffnung quer zur Visierlinie (y, z), um margin mm verkleinert; Röhre: Bohrung (engste Stelle der hohlen Röhre)"""
    ly=geo['line_y'];w=geo['window']
    if geo.get('tube'):return circle(ly,0,geo['tube']['bore_r']-margin)
    if w['shape']=='round':return circle(ly,0,w['w']/2-margin)
    return loop(ly,0,w['h']/2-margin,w['w']/2-margin,max(0.0,w['r']-margin),seg=1 if w['shape']=='octagon' else 5)

# ---------------------------------------------------------------- Bausteine-Felder des Blatts (keine Spec-Daten)
def frame_variant(style,shape='rect'):
    """Rahmen-Variante als kleines Modell für das Feld „Bausteine · Rahmen“ (gleiche Fensterform wie das Blatt)."""
    S=Sight();S.module=None
    t,dep={'standard':(3,8),'compact':(2.6,6),'open':(2,5),'closed':(3.2,20),'industrial':(4.6,12),'lightweight':(1.4,4)}[style]
    hh,hw=(14,14) if shape=='round' else (12,15) if shape!='octagon' else (12,15)
    r,seg=(14,8) if shape=='round' else (5,1) if shape=='octagon' else (3,5)
    mount(S,-12,12,18,jaw=False)
    S.group('housing','Gehäuse','MT_Secondary','painted',DARK).box('housing',-14,14,-11,-6,-10,10,r=1.5)
    ly=-11-hh
    S.group('frame','Rahmen','MT_Accent','painted',ORANGE if style!='lightweight' else WHITE)
    S.ring('frame',0,dep,loop(ly,0,hh,hw,r,seg),loop(ly,0,hh-t,hw-t,max(0.8,r-t) if shape!='round' else hh-t,seg))
    if style in ('closed','industrial'):
        S.group('cover','Abdeckung','MT_Primary','painted',WHITE).boxes_lr('cover',-12,0,-10.5,-6.5,10,11.4,r=0.8)
    if style=='industrial':
        S.group('bolts','Schrauben','MT_Metal','brushed',METAL)
        for sy in (1,-1):
            for sz in (1,-1):S.box('bolts',dep,dep+1.4,ly+sy*(hh-t/2)-1.2,ly+sy*(hh-t/2)+1.2,sz*(hw-t/2)-1.2,sz*(hw-t/2)+1.2,r=0.4)
    S.group('glass','Glas','MT_Detail','glass',None,glass=True).pane('glass',dep*0.6,loop(ly,0,hh-t+0.6,hw-t+0.6,max(0.8,r-t+0.6) if shape!='round' else hh-t+0.6,seg))
    return set_tint(S,'blue')

def module_model(mid):
    """Tech-Modul allein (Feld „Bausteine · Module“)."""
    S=Sight();S.module=None
    lens={'night_vision':'#4BE38A','rangefinder':'#FF4A3D','target_marker':'#FF8A2A','wind_compensation':'#5CC8FF'}[mid]
    _module_body(S,'module',MODULES[mid],-12,12,-16,0,-8,8,lens)
    if mid=='night_vision':S.group('hood','Blende','MT_Accent','painted',ORANGE).ring('hood',12,16,circle(-8,0,5.6,16),circle(-8,0,4.6,16))
    if mid=='wind_compensation':S.group('knob','Rad','MT_Accent','painted',ORANGE).knob_z('knob',-2,-8,4,8,10.5)
    if mid=='target_marker':S.group('fin','Antenne','MT_Accent','painted',ORANGE).box('fin',-8,-2,-21,-16,-1,1,r=0.4)
    if mid=='rangefinder':S.group('lcd','Anzeige','MT_Emission','lit','#FF4A3D',emit=True).box('lcd',-9,3,-17,-16,-5,5,r=0.4)
    return S
