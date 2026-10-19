"""Bauhelfer der neuen Waffentypen (claude-0.10, Blätter KG11 … KG22; Modelle g11.py … g22.py).

Wie flib (Variante G 06–10), aber direkt auf eng.Model, damit auch Teile quer zur Waffe gehen (Wurfarme, Parierstange: prism_y)
und Kegel/Zylinder versetzt liegen können. Jede Bau-Funktion hängt genau ein Teil an; Bezeichnung (L), Visierteil (S) und Kanal (ch)
gelten für dieses Teil. Koordinaten wie überall: x = vorn (Mündung), y = unten, z = links.

Modelldatei: model() -> eng.Model, META mit num, name, nick, col, pill, palette, center, desc, form und op (Bedienung, de/en).
"""
from eng import Model,rect,circ,roundpoly,CHANNELS
import ext

class B:
    def __init__(s):s.m=Model()
    def _set(s,L=None,S=False,ch=None):
        P=s.m.parts[-1]
        if L:P['label']=L
        if S:P['sight']=True
        if ch:assert ch in CHANNELS,ch;P['channel']=ch
        return P
    def P(s,prof,col,z0,z1,r=0,emit=False,L=None,dec=(),xdec=(),S=False,ch=None):
        """Seitenprofil (x, y) von z0 bis z1; dec: Aufkleber (Punkte x, y, Farbe, leuchtend) auf z1, bei symmetrischer Lage auch auf z0"""
        s.m.prism(prof,col,z0,z1,r=r,emit=emit)
        for pts,c,e in dec:
            s.m.decal('z+',z1,pts,c,emit=e,both=False)
            if abs(z0+z1)<1e-9:s.m.decal('z-',z0,pts,c,emit=e,both=False)
        for plane,val,pts,c,e in xdec:s.m.decal(plane,val,pts,c,emit=e,both=False)
        return s._set(L,S,ch)
    def C(s,x0,x1,cy,R,col,n=8,cz=0,emit=False,L=None,cap=(),S=False,ch=None):
        """Zylinder entlang x; cap: Aufkleber auf der Vorderfläche (y, z, Radius, Farbe, leuchtend)"""
        s.m.cyl(x0,x1,cy,cz,R,col,n=n,emit=emit)
        for y,z,r,c,e in cap:s.m.decal('x+',x1,circ(y,z,r,max(8,n)),c,emit=e,both=False)
        return s._set(L,S,ch)
    def F(s,x0,x1,cy,R0,R1,col,n=8,cz=0,emit=False,L=None,ch=None):
        """Kegelstumpf entlang x"""
        ext.frustum(s.m,x0,x1,cy,cz,R0,R1,col,n=n,emit=emit)
        return s._set(L,False,ch)
    def Y(s,poly,col,y0,y1,r=0,emit=False,L=None,dec=(),ch=None):
        """Grundriss (x, z) von y0 (oben) bis y1 extrudiert; dec: Aufkleber auf der Oberseite (Punkte x, z)"""
        ext.prism_y(s.m,poly,col,y0,y1,r=r,emit=emit,winding=True)   # hohle Grundrisse richtig schattiert (claude-0.11)
        for pts,c,e in dec:s.m.parts[-1]['dec'].append(('y-',y0,pts,c,e))
        P=s.m.parts[-1];P.setdefault('hull',True)
        return s._set(L,False,ch)
    def D(s,pts,col,emit=False):return (pts,col,emit)

def trigger_group(b,x,y,col_trig,col_guard,grip_x0,depth=44):
    """Abzug mit Bügel vor einem Griff: Abzug ab Unterkante y bei x, Bügel unten bis grip_x0 zurück, vorne senkrecht hoch"""
    b.P([(x,y+1),(x+12,y+1),(x+24,y+depth*0.93),(x+12,y+depth*1.02)],col_trig,-6,6,r=2,L='Abzug')
    b.P(rect(grip_x0,y+depth*1.4,x+64-grip_x0,9),col_guard,-7,7,r=3)
    b.P(rect(x+56,y,9,depth*1.4+9),col_guard,-7,7,r=3)

def grip(b,x0,y0,col,col_dec,h=96,w=50,lean=14,L='Griff',z=18):
    """Pistolengriff mit Rillen; (x0, y0) vordere obere Ecke ist hinten oben am Griff"""
    b.P([(x0,y0),(x0+w,y0),(x0+w-10,y0+h),(x0-lean,y0+h)],col,-z,z,r=6,L=L,
        dec=[b.D(roundpoly(rect(x0+2-lean*0.15*(i+1),y0+20+12*i,w-14,5),2),col_dec) for i in range(int((h-30)/12))])

def rail(b,x0,x1,y,col,col_dec,w=10,L='Visierschiene'):
    """Visierschiene oben (Oberkante y-10): Schiene mit Querrillen, reicht 6 Einheiten in das Gehäuse (schräge Oberseiten); bleibt auf der
    Waffe, das Visier setzt vsmount darauf"""
    b.P(rect(x0,y-10,x1-x0,16),col,-w,w,r=2,L=L,dec=[b.D(rect(xx,y-8,6,4),col_dec) for xx in range(int(x0)+8,int(x1)-8,14)])
