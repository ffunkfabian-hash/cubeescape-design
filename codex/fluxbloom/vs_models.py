"""Independent Codex reconstruction of VS01–09 from the public Sight-Spec data.

Dimensions below are transcribed measurements, not imported Claude geometry.
Authoring frame: X left, Y rear, Z up, millimetres, mount at zero. Geometry is
built here as chamfered solids, hollow shells and single-surface optical panes.
"""
import numpy as np
from eng import Part, _face

# Filled by the dimensional transcription below: type/frame, window, anchors,
# tube bore, and each named component's material/channel and measured envelope.
DESIGNS = {
    1: dict(type='reflex', frame='compact',
        shape='rect', opening=(20.0, 18.0, 2.5),
        reticle=(0.0, -9.5, 26.0),
        rear=-6.0, eye=None,
        bore=None, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-10.0, -14.0, -3.0, 10.0, 14.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (10.0, -2.4, 0.2, 12.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-11.0, -15.0, 6.0, 11.0, 16.0, 15.0)),
            ('Abdeckung', 'MT_Primary', 'painted', (-12.2, -5.0, 7.5, 12.2, 13.0, 13.0)),
            ('Rahmen', 'MT_Accent', 'painted', (-12.5, -12.5, 14.5, 12.5, -6.0, 37.5)),
            ('Glas', 'MT_Detail', 'glass', (-10.6, -9.5, 16.4, 10.6, -9.5, 35.6)),
            ('Emitter', 'MT_Energy', 'lit', (-2.2, 5.0, 15.0, 2.2, 10.0, 16.4)),
            ('Bedienknopf', 'MT_Accent', 'painted', (12.2, 3.0, 8.0, 13.6, 9.0, 11.0)),
        ]),
    2: dict(type='holo', frame='open',
        shape='rect', opening=(34.0, 29.0, 3.0),
        reticle=(0.0, -18.0, 31.0),
        rear=-5.0, eye=None,
        bore=None, tint='#8FA6B8', alpha=0.2, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-11.0, -24.0, -3.0, 11.0, 24.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (11.0, -2.4, 0.2, 13.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-12.0, -28.0, 6.0, 12.0, 29.0, 14.0)),
            ('Abdeckung', 'MT_Primary', 'painted', (-13.3, 4.0, 7.5, 13.3, 28.0, 15.5)),
            ('Rahmen', 'MT_Accent', 'painted', (-19.5, -21.0, 14.0, 19.5, -5.0, 48.0)),
            ('Glas', 'MT_Detail', 'glass', (-17.6, -18.0, 15.9, 17.6, -18.0, 46.1)),
            ('Emitter', 'MT_Energy', 'lit', (-3.0, 1.0, 14.0, 3.0, 7.0, 15.6)),
            ('Bedienknopf', 'MT_Accent', 'painted', (-8.0, 19.0, 15.5, 8.0, 26.0, 16.3)),
        ]),
    3: dict(type='precision', frame='standard',
        shape='round', opening=(34.4, 34.4, 17.2),
        reticle=(0.0, -60.0, 25.0),
        rear=65.0, eye=(0.0, 58.0, 25.0),
        bore=11.9, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-11.0, -31.0, -3.0, 11.0, 31.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (11.0, -2.4, 0.2, 13.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-17.4, -45.0, 7.6, 17.4, 59.0, 42.4)),
            ('Abdeckung', 'MT_Primary', 'painted', (-15.7, -9.0, 9.3, 15.7, 13.0, 40.7)),
            ('Rahmen', 'MT_Accent', 'painted', (-21.0, -63.0, 4.0, 21.0, 44.0, 46.0)),
            ('Augenmuschel', 'MT_Secondary', 'rubber', (-16.1, 59.0, 8.9, 16.1, 65.0, 41.1)),
            ('Glas', 'MT_Detail', 'glass', (-17.5, -60.0, 7.5, 17.5, -60.0, 42.5)),
            ('Okularglas', 'MT_Detail', 'glass', (-12.8, 58.0, 12.2, 12.8, 58.0, 37.8)),
            ('Montageringe', 'MT_Metal', 'brushed', (-17.1, -25.0, 5.5, 17.1, 27.0, 42.1)),
            ('Verstellturm', 'MT_Secondary', 'painted', (-6.5, -5.5, 19.0, 23.5, 7.5, 49.5)),
            ('Turmkappe', 'MT_Accent', 'painted', (-5.5, -4.5, 20.0, 25.5, 6.5, 51.5)),
            ('Zierring', 'MT_Accent', 'painted', (-15.6, -31.0, 9.4, 15.6, -27.0, 40.6)),
            ('Entfernungsanzeige', 'MT_Secondary', 'painted', (-25.0, -29.0, 19.0, -15.0, -7.0, 33.0)),
            ('Entfernungsanzeige · Linse', 'MT_Emission', 'lit', (-22.8, -30.2, 23.2, -17.2, -29.0, 28.8)),
            ('Entfernungsanzeige · Klemme', 'MT_Metal', 'brushed', (-15.0, -26.0, 23.0, -13.5, -10.0, 29.0)),
        ]),
    4: dict(type='reflex', frame='standard',
        shape='round', opening=(41.0, 41.0, 20.5),
        reticle=(0.0, -14.0, 36.0),
        rear=1.0, eye=None,
        bore=None, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-12.0, -18.0, -3.0, 12.0, 18.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (12.0, -2.4, 0.2, 14.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-14.0, -20.0, 6.0, 14.0, 23.0, 15.0)),
            ('Abdeckung', 'MT_Primary', 'painted', (-15.3, 0.0, 7.5, 15.3, 20.0, 13.5)),
            ('Rahmen', 'MT_Accent', 'painted', (-24.5, -18.0, 11.5, 24.5, -4.0, 60.5)),
            ('Rückring', 'MT_Secondary', 'painted', (-23.0, -4.0, 13.0, 23.0, 1.0, 59.0)),
            ('Glas', 'MT_Detail', 'glass', (-21.2, -14.0, 14.8, 21.2, -14.0, 57.2)),
            ('Emitter', 'MT_Energy', 'lit', (-2.5, 7.0, 14.0, 2.5, 13.0, 15.3)),
            ('Bedienknopf', 'MT_Accent', 'painted', (-17.5, 6.4, 6.4, -14.0, 13.6, 13.6)),
        ]),
    5: dict(type='sniper', frame='standard',
        shape='round', opening=(45.400000000000006, 45.400000000000006, 22.700000000000003),
        reticle=(0.0, -103.0, 27.0),
        rear=102.0, eye=(0.0, 95.0, 27.0),
        bore=12.9, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-11.0, -54.0, -3.0, 11.0, 54.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (11.0, -2.4, 0.2, 13.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-22.9, -66.0, 4.1, 22.9, 96.0, 49.9)),
            ('Abdeckung', 'MT_Primary', 'painted', (-16.7, -24.0, 10.3, 16.7, 24.0, 43.7)),
            ('Rahmen', 'MT_Accent', 'painted', (-26.5, -106.0, 0.5, 26.5, 75.0, 53.5)),
            ('Augenmuschel', 'MT_Secondary', 'rubber', (-17.6, 96.0, 9.4, 17.6, 102.0, 44.6)),
            ('Glas', 'MT_Detail', 'glass', (-23.0, -103.0, 4.0, 23.0, -103.0, 50.0)),
            ('Okularglas', 'MT_Detail', 'glass', (-14.3, 95.0, 12.7, 14.3, 95.0, 41.3)),
            ('Montageringe', 'MT_Metal', 'brushed', (-18.1, -42.0, 5.5, 18.1, 44.0, 45.1)),
            ('Verstellturm', 'MT_Secondary', 'painted', (-6.5, -4.5, 21.0, 24.5, 8.5, 52.5)),
            ('Turmkappe', 'MT_Accent', 'painted', (-5.5, -3.5, 22.0, 26.5, 7.5, 54.5)),
            ('Zierring', 'MT_Accent', 'painted', (-16.7, -56.0, 10.3, 16.7, -52.0, 43.7)),
            ('Windkompensation', 'MT_Secondary', 'painted', (-27.0, -10.0, 18.0, -16.5, 18.0, 33.0)),
            ('Windkompensation · Linse', 'MT_Emission', 'lit', (-24.7, -11.2, 22.6, -18.8, -10.0, 28.4)),
            ('Windkompensation · Klemme', 'MT_Metal', 'brushed', (-16.5, -7.0, 22.5, -15.0, 15.0, 28.5)),
            ('Windkompensation · Rad', 'MT_Accent', 'painted', (-29.5, 4.0, 21.5, -27.0, 12.0, 29.5)),
        ]),
    6: dict(type='machine', frame='closed',
        shape='rect', opening=(35.0, 30.0, 2.5),
        reticle=(0.0, -20.5, 30.0),
        rear=7.0, eye=None,
        bore=None, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-11.0, -21.0, -3.0, 11.0, 21.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (11.0, -2.4, 0.2, 13.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-13.0, -25.0, 6.0, 13.0, 26.0, 12.0)),
            ('Abdeckung', 'MT_Primary', 'painted', (-20.5, -19.0, 12.0, 20.5, 3.0, 48.0)),
            ('Rahmen', 'MT_Accent', 'painted', (-21.1, -23.5, 11.4, 21.1, -19.0, 48.6)),
            ('Rückring', 'MT_Secondary', 'painted', (-21.1, 3.0, 11.4, 21.1, 7.0, 48.6)),
            ('Glas', 'MT_Detail', 'glass', (-18.1, -20.5, 14.4, 18.1, -20.5, 45.6)),
            ('Emitter', 'MT_Energy', 'lit', (-2.6, 10.0, 12.0, 2.6, 17.0, 13.4)),
            ('Bedienknopf', 'MT_Accent', 'painted', (-14.4, 12.0, 7.5, -13.0, 19.0, 10.5)),
        ]),
    7: dict(type='energy', frame='closed',
        shape='octagon', opening=(36.8, 28.8, 5.8999999999999995),
        reticle=(0.0, -15.5, 34.0),
        rear=-1.0, eye=None,
        bore=None, tint='#9B5CF0', alpha=0.3, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-12.0, -27.0, -3.0, 12.0, 27.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (12.0, -2.4, 0.2, 14.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-14.0, -31.0, 6.0, 14.0, 32.0, 15.9)),
            ('Abdeckung', 'MT_Primary', 'painted', (-15.3, 5.0, 7.5, 15.3, 29.0, 14.5)),
            ('Rahmen', 'MT_Accent', 'painted', (-23.5, -21.0, 14.5, 23.5, -5.0, 53.5)),
            ('Rückring', 'MT_Secondary', 'painted', (-23.0, -5.0, 15.0, 23.0, -1.0, 53.0)),
            ('Leuchtrahmen', 'MT_Energy', 'lit', (-20.1, -18.5, 17.9, 20.1, -16.5, 50.1)),
            ('Glas', 'MT_Detail', 'glass', (-20.4, -15.5, 17.6, 20.4, -15.5, 50.4)),
            ('Energiezelle', 'MT_Secondary', 'painted', (14.0, 3.0, 7.0, 21.0, 25.0, 18.4)),
            ('Ladeanzeige', 'MT_Energy', 'lit', (21.0, 7.0, 10.2, 21.8, 21.0, 15.8)),
        ]),
    8: dict(type='trace', frame='lightweight',
        shape='rect', opening=(36.4, 28.400000000000002, 2.0),
        reticle=(0.0, -12.5, 28.0),
        rear=-10.0, eye=None,
        bore=None, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-11.0, -22.0, -3.0, 11.0, 22.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (11.0, -2.4, 0.2, 13.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-12.0, -24.0, 6.0, 12.0, 27.0, 13.9)),
            ('Abdeckung', 'MT_Primary', 'painted', (-13.3, 2.0, 7.5, 13.3, 24.0, 12.7)),
            ('Rahmen', 'MT_Accent', 'painted', (-20.0, -15.0, 12.0, 20.0, -10.0, 44.0)),
            ('Stütze', 'MT_Secondary', 'painted', (-17.1, -12.0, 11.4, 17.1, 0.0, 13.6)),
            ('Glas', 'MT_Detail', 'glass', (-18.8, -12.5, 13.2, 18.8, -12.5, 42.8)),
            ('Markierungsrahmen', 'MT_Energy', 'lit', (-19.7, -15.8, 12.3, 19.7, -15.0, 43.7)),
            ('Zielmarkierung', 'MT_Secondary', 'painted', (12.0, -4.0, 3.0, 19.0, 18.0, 13.6)),
            ('Zielmarkierung · Linse', 'MT_Emission', 'lit', (13.5, -5.2, 6.3, 17.5, -4.0, 10.3)),
            ('Zielmarkierung · Klemme', 'MT_Metal', 'brushed', (10.5, -1.0, 5.3, 12.0, 15.0, 11.3)),
        ]),
    9: dict(type='rocket', frame='industrial',
        shape='rect', opening=(64.0, 32.0, 2.0),
        reticle=(0.0, -20.0, 36.0),
        rear=-1.0, eye=None,
        bore=None, tint='#3D9BEA', alpha=0.28, parts=[
            ('Halterung', 'MT_Metal', 'brushed', (-13.0, -30.0, -3.0, 13.0, 30.0, 6.0)),
            ('Klemmschraube', 'MT_Accent', 'painted', (13.0, -2.4, 0.2, 15.6, 2.4, 5.0)),
            ('Gehäuse', 'MT_Secondary', 'painted', (-17.0, -36.0, 6.0, 17.0, 37.0, 16.9)),
            ('Abdeckung', 'MT_Primary', 'painted', (-19.0, -30.0, 7.5, 19.0, 33.0, 15.6)),
            ('Rahmen', 'MT_Accent', 'painted', (-37.0, -24.0, 15.0, 37.0, -6.0, 57.0)),
            ('Rückring', 'MT_Secondary', 'painted', (-36.0, -6.0, 16.0, 36.0, -1.0, 56.0)),
            ('Glas', 'MT_Detail', 'glass', (-32.6, -20.0, 19.4, 32.6, -20.0, 52.6)),
            ('Schrauben', 'MT_Metal', 'brushed', (-36.0, -25.6, 16.0, 36.0, -24.0, 56.0)),
            ('Emitter', 'MT_Energy', 'lit', (-3.0, 12.0, 16.4, 3.0, 20.0, 18.4)),
            ('Entfernungsanzeige', 'MT_Secondary', 'painted', (-9.0, -24.0, 56.5, 9.0, -8.0, 68.0)),
            ('Entfernungsanzeige · Linse', 'MT_Emission', 'lit', (-3.2, -25.2, 59.0, 3.2, -24.0, 65.5)),
            ('Entfernungsanzeige · Klemme', 'MT_Metal', 'brushed', (-4.0, -21.0, 54.0, 4.0, -11.0, 56.5)),
        ]),
}


def contour(width, height, shape='rect', corner=1):
    """Counterclockwise X/Z contour, including cardinal extrema."""
    if shape == 'round':
        angle=np.arange(64)*2*np.pi/64
        return np.column_stack((np.cos(angle)*width/2,np.sin(angle)*height/2))
    a,b=width/2,height/2;c=min(corner,a*.8,b*.8)
    if c<=0:return np.array([[-a,-b],[a,-b],[a,b],[-a,b]])
    if shape=='rect':
        points=[]
        for cx,cz,start in ((a-c,-b+c,-90),(a-c,b-c,0),(-a+c,b-c,90),(-a+c,-b+c,180)):
            for angle in np.deg2rad(np.linspace(start,start+90,5)):
                points.append((cx+c*np.cos(angle),cz+c*np.sin(angle)))
        return np.asarray(points)
    return np.array([[-a+c,-b],[a-c,-b],[a,-b+c],[a,b-c],
                     [a-c,b],[-a+c,b],[-a,b-c],[-a,-b+c]])


def extrusion(profile, y0, y1):
    """Closed prism along Y with consistently outward Newell normals."""
    a=np.column_stack((profile[:,0],np.full(len(profile),y0),profile[:,1]))
    b=a.copy();b[:,1]=y1
    # CCW in X/Z faces toward -Y.
    faces=[_face(a),_face(b[::-1])]
    for i in range(len(a)):
        j=(i+1)%len(a);faces.append(_face([a[i],b[i],b[j],a[j]]))
    return faces


def solid(box, bevel=.4):
    lo,hi=np.asarray(box).reshape(2,3);c=(lo+hi)/2
    profile=contour(hi[0]-lo[0],hi[2]-lo[2],shape='octagon',corner=bevel)+c[[0,2]]
    return extrusion(profile,lo[1],hi[1])


def shell(box, opening, shape, center, corner=1):
    """Hollow through-shell; front/rear annuli never cap the aperture."""
    lo,hi=np.asarray(box).reshape(2,3);c=(lo+hi)/2
    outer=contour(hi[0]-lo[0],hi[2]-lo[2],shape,corner)+c[[0,2]]
    inner=contour(*opening,shape,corner)+np.asarray(center)[[0,2]]
    rings=[]
    for y in (lo[1],hi[1]):
        rings.append([np.column_stack((p[:,0],np.full(len(p),y),p[:,1])) for p in (outer,inner)])
    faces=[]
    for i in range(len(outer)):
        j=(i+1)%len(outer)
        for side in (0,1):
            v=[rings[0][side][i],rings[0][side][j],rings[1][side][j],rings[1][side][i]]
            if not side:v=v[::-1]
            group=1+side if shape=='round' else 10+side*4+i//5 if shape=='rect' and i%5<4 else 0
            faces.append(_face(v,group))
        faces.append(_face([rings[0][0][i],rings[0][0][j],rings[0][1][j],rings[0][1][i]],30))
        faces.append(_face([rings[1][0][j],rings[1][0][i],rings[1][1][i],rings[1][1][j]],31))
    return faces


def _join(*items):return [face for faces in items for face in faces]


def build_sight(number):
    """Return independent physical geometry in the Sight-Spec millimetre frame."""
    d=DESIGNS[number];parts=[];center=d['reticle'];w,h,corner=d['opening']
    for index,(label,channel,material,box) in enumerate(d['parts']):
        lo,hi=np.asarray(box).reshape(2,3);extent=hi-lo
        shape=d['shape'];opening=(w,h)
        if material=='glass':
            profile=contour(extent[0],extent[2],shape,corner)+(lo+hi)[[0,2]]/2
            vertices=np.column_stack((profile[:,0],np.full(len(profile),lo[1]),profile[:,1]))
            faces=[_face(vertices)]
        elif label=='Halterung':
            # 14 mm rail slot; only the two jaws extend 3 mm below the mount.
            top=lo.copy();top[2]=0
            left_hi=hi.copy();left_hi[0]=-7;left_hi[2]=0
            right_lo=lo.copy();right_lo[0]=7
            right_hi=hi.copy();right_hi[2]=0
            faces=_join(solid([*top,*hi]),solid([*lo,*left_hi],0),solid([*right_lo,*right_hi],0))
        elif d['bore'] and label in ('Gehäuse','Abdeckung','Rahmen','Augenmuschel','Montageringe','Zierring'):
            # The tube is open at both ends; objective collar is flared locally.
            bore=d['bore']
            if label=='Rahmen':
                front_end=d['parts'][2][3][1]  # exact front of the housing
                first_hi=hi.copy();first_hi[1]=front_end
                rear_lo=lo.copy();rear_lo[1]=hi[1]-4
                neck=d['bore']+3.7
                rear_lo[0]=-neck;rear_lo[2]=center[2]-neck
                rear_hi=hi.copy();rear_hi[0]=neck;rear_hi[2]=center[2]+neck
                # Objective collar and rear adjustment collar share one named
                # part; the independently modelled housing joins them.
                faces=_join(shell([*lo,*first_hi],(w,h),'round',center),
                            shell([*rear_lo,*rear_hi],(bore*2,bore*2),'round',center))
            else:
                faces=shell(box,(bore*2,bore*2),'round',center)
        elif label in ('Verstellturm','Turmkappe'):
            # Orthogonal adjustment turrets form a connected L outside the bore.
            border=d['bore']+.6
            z=center[2]+border
            profile=np.array([(lo[0],z),(border,z),(border,lo[2]),
                              (hi[0],lo[2]),(hi[0],hi[2]),(lo[0],hi[2])])
            faces=extrusion(profile,lo[1],hi[1])
        elif label in ('Rahmen','Rückring','Leuchtrahmen') or (number==6 and label=='Abdeckung'):
            faces=shell(box,opening,shape,center,corner)
        elif label in ('Markierungsrahmen','Schrauben'):
            # Four separate corner pieces, grouped under the one Spec label.
            faces=[];thickness=.65 if label=='Markierungsrahmen' else 1.8
            for x in (lo[0],hi[0]-thickness):
                for z in (lo[2],hi[2]-thickness):
                    faces+=solid((x,lo[1],z,x+thickness,hi[1],z+thickness),.1)
        else:faces=solid(box)
        p=Part(faces,d['tint'] if material=='glass' else '#808080',
               label=label,sight=True,material={'painted':'paint','brushed':'metal','lit':'light'}.get(material,material),
               emit=material=='lit',role='medium')
        p.channel=channel;p.vs_part=index
        if material=='glass':
            p.glass_alpha=d['alpha'];p.sight_window=True
        parts.append(p)
    return parts
