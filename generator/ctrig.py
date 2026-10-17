# Variante C: gut sichtbarer Abzugsbereich (Abzug ragt deutlich unter das Gehaeuse, damit er auch in der Isometrie lesbar ist)
from eng import *
def trigger(m,xg,yb,tcol,gcol,depth=58,w=40,xr=None,zt=4,zg=5,lab=True):
    """xg: Hinterkante Abzug, yb: Gehaeuse-Unterkante, w: Buegellaenge nach vorn, xr: hinterer Buegelansatz (Griffvorderkante)"""
    xr=xg-10 if xr is None else xr
    # Abzug: geschwungenes Zuengel, leicht nach vorn geneigt
    m.prism([(xg+2,yb-2),(xg+12,yb-2),(xg+16,yb+depth*0.55),(xg+10,yb+depth*0.78),(xg+4,yb+depth*0.74),(xg+6,yb+depth*0.5)],tcol,-zt,zt,r=2)
    if lab:label(m,'Abzug')
    # Buegel: Unterkante + Vorderstrebe (konvex), hinten am Griff angesetzt
    m.prism([(xr,yb+depth),(xg+w,yb+depth),(xg+w+4,yb+depth+8),(xr,yb+depth+8)],gcol,-zg,zg,r=2)
    m.prism([(xg+w-6,yb-2),(xg+w+2,yb-2),(xg+w+4,yb+depth+8),(xg+w-4,yb+depth+8)],gcol,-zg,zg,r=2)
    return m
def rail(m,x0,x1,ytop,col,cut,z=9,h=10,slope=0.0):
    """Montageschiene (bleibt an der Waffe): Grundleiste + Querrillen"""
    m.prism([(x0,ytop),(x1,ytop+slope*(x1-x0)),(x1,ytop+h+slope*(x1-x0)),(x0,ytop+h)],col,-z,z,r=2);label(m,'Visierschiene')
    for x in range(int(x0)+6,int(x1)-4,12):
        yy=ytop+slope*(x-x0)
        m.decal('z+',z,rect(x,yy+1,6,4),cut)
    return m
