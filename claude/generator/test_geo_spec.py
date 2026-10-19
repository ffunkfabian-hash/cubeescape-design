"""Test der Geo-Specs (claude/output/sheets/KXnn.geo.json, VSnn.geo.json; Format claude/docs/geometry-spec.md). Ohne numpy, ohne Bildstufe.
   python3 claude/generator/export_geo.py && python3 claude/generator/test_geo_spec.py

Prüft: Schema; Netze (Indizes, Flächen, Hüllquader); Teile, Hüllquader (±0,5 mm) und Anker gegen Weapon- bzw. Sight-Spec; Normalen nach außen
(geschlossene Hüllen mit positivem Volumen, gleicher Umlaufsinn je Teil); Aufkleber; Primitiv-Hinweise gegen das Netz; Koplanar-Befunde
(Regel mit Gegenbeweis, Zahl als Befund, kein Fehler); Dreiecke unter Toolgens Welt-Budget (data/game_budget.json, nur gelesen, sonst übersprungen).
"""
from cepaths import E3D,CLAUDE,OUT
import json,math,os,sys,unittest
sys.path.insert(0,E3D)
import export_geo as G
from test_spec import validate

def _read(fn):
    with open(fn,encoding='utf-8') as f:return f.read()
SCHEMA=json.loads(_read(os.path.join(CLAUDE,'docs','geometry-spec.schema.json')))
TOL=5e-4      # 0,5 mm
TOOLGEN=os.environ.get('TOOLGEN_ROOT',os.path.expanduser('~/Claude/cubeescape-toolgen'))
BUDGET=os.path.join(TOOLGEN,'data','game_budget.json')
_cache={}
def load(sid):
    if sid not in _cache:_cache[sid]=json.loads(_read(G.path(sid)))
    return _cache[sid]
def spec(sid):return json.loads(_read(os.path.join(OUT,f'{sid}.spec.json')))
def close(a,b,tol=TOL):return all(abs(x-y)<=tol for x,y in zip(a,b))

class Files(unittest.TestCase):
    def test_all_present(self):
        self.assertEqual(len(G.SHEETS),159)
        miss=[s for s in G.SHEETS if not os.path.exists(G.path(s))]
        self.assertEqual(miss,[],'fehlend – python3 claude/generator/export_geo.py')
        extra=sorted(f for f in os.listdir(OUT) if f.endswith('.geo.json') and f[:-9] not in G.SHEETS)
        self.assertEqual(extra,[])
    def test_current(self):
        """Stichprobe (Waffe, Bogen mit Normal-Korrektur, Röhrenvisier): Datei = Ausgabe des Exporters; vollständig: export_geo.py --check"""
        for s in ('KG02','KC10','VS05'):
            with self.subTest(sheet=s):self.assertEqual(_read(G.path(s)),G.dumps(G.build(s)),'veraltet – python3 claude/generator/export_geo.py')
    def test_schema(self):
        for s in G.SHEETS:
            with self.subTest(sheet=s):self.assertEqual(validate(load(s),SCHEMA,root=SCHEMA),[])

class Meshes(unittest.TestCase):
    def test_indices_bounds_counts(self):
        for s in G.SHEETS:
            g=load(s)
            with self.subTest(sheet=s):
                tri=fc=vc=0
                for p in g['parts']:
                    m=p['mesh'];n=len(m['vertices'])
                    self.assertEqual(len(m['hard']),len(m['faces']),p['id'])
                    for f in m['faces']:
                        self.assertTrue(all(0<=i<n for i in f),p['id']);self.assertGreaterEqual(len(set(f)),3,p['id'])
                    self.assertTrue(all(math.isfinite(c) for v in m['vertices'] for c in v))
                    self.assertEqual(p['bounds_m'],G._bb(m['vertices']),p['id'])
                    self.assertEqual(p['name'],f'SM_PG_{G.ascii_label(p["label"])}_{p["id"]}')
                    tri+=G.triangles(m);fc+=len(m['faces']);vc+=n
                c=g['counts']
                self.assertEqual((c['parts'],c['triangles'],c['faces'],c['vertices'],c['decals']),(len(g['parts']),tri,fc,vc,len(g['decals'])))
                self.assertEqual(c['dropped_faces'],0)

    def test_normals_outward(self):
        """Geschlossene Hüllen: Volumen > 0 (flache Scheiben ≈ 0); Waffenteile (ein eng-Teil je Teil): keine Kante zweimal in gleicher Richtung.
        Offene Teile (Ringhälften, Mäntel) folgen der gespeicherten Normale des Modells."""
        closed=open_=0
        for s in G.SHEETS:
            g=load(s)
            for p in g['parts']:
                V=p['mesh']['vertices'];Fs=p['mesh']['faces']
                for comp,cl in G.closed_components(Fs):
                    if not cl:open_+=1;continue
                    closed+=1;vol=G.signed_volume(V,[Fs[k] for k in comp])
                    self.assertGreater(vol,-1e-15,f'{s} {p["id"]} ({p["label"]}): Hülle mit Normalen nach innen')
                if g['sheet']['kind']=='weapon':
                    seen=set()
                    for f in Fs:
                        for i in range(len(f)):
                            e=(f[i],f[(i+1)%len(f)]);self.assertNotIn(e,seen,f'{s} {p["id"]}: Umlaufsinn uneinheitlich');seen.add(e)
        self.assertGreater(closed,open_)
        print(f'\n  Hüllen: {closed} geschlossen (Volumen > 0), {open_} offen (gespeicherte Normale)',file=sys.stderr)
    def test_orient_fixes_inward_hull(self):
        """Gegenbeweis: ein Würfel mit einer nach innen gedrehten Fläche wird gerichtet, ein ganz innen gedrehter umgedreht"""
        V=[[x,y,z] for x in (0,1) for y in (0,1) for z in (0,1)]
        cube=[[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]]
        self.assertGreater(G.signed_volume(V,cube),0)
        bad=[f[:] for f in cube];bad[2]=bad[2][::-1]
        self.assertEqual(G.orient(bad,V),1);self.assertEqual(bad,cube)
        inv=[f[::-1] for f in cube];self.assertEqual(G.orient(inv,V),6);self.assertEqual(inv,cube)

class AgainstSpecs(unittest.TestCase):
    def test_parts_and_bounds(self):
        for s in G.SHEETS:
            g=load(s);sp=spec(s)
            with self.subTest(sheet=s):
                self.assertEqual([p['id'] for p in g['parts']],[p['id'] for p in sp['parts']])
                for a,b in zip(g['parts'],sp['parts']):
                    for k in ('label','channel','material','emissive'):self.assertEqual(a[k],b[k],(a['id'],k))
                    self.assertTrue(close(a['bounds_m'][0],b['bounds_m'][0]) and close(a['bounds_m'][1],b['bounds_m'][1]),(a['id'],a['bounds_m'],b['bounds_m']))
                self.assertEqual(g['source']['weapon_spec' if s[0]=='K' else 'sight_spec']['sha256'],G.sha(_read(os.path.join(OUT,f'{s}.spec.json'))))
    def test_anchors(self):
        for s in G.SHEETS:
            g=load(s);sp=spec(s);a=g['anchors']
            with self.subTest(sheet=s):
                if s[0]=='K':
                    for k,v in sp['anchors'].items():self.assertEqual(a[k]['position_m'],v['position_m'],k)
                    self.assertEqual(a['Socket_Hand']['position_m'],[0.0,0.0,0.0])
                    ss=sp['sight'].get('sight_spec')
                    if ss:
                        self.assertTrue(close(a['Socket_Reticle']['position_m'],ss['socket_reticle_m']))
                        self.assertTrue(close(g['sight']['socket_mount_m'],ss['socket_mount_m']))
                        if ss['socket_eye_m']:self.assertTrue(close(a['Socket_Eye']['position_m'],ss['socket_eye_m']))
                        self.assertEqual(sorted(g['sight']['parts']),sorted(sp['sight']['parts']))
                    else:self.assertIsNone(a['Socket_Reticle']['position_m'])
                else:
                    for k,v in sp['anchors'].items():
                        if v:self.assertTrue(close(a[k]['position_m'],v['position_m']),k)
                    self.assertEqual(a['Socket_Mount']['position_m'],[0.0,0.0,0.0])
                if a['Socket_Eye']['position_m']:   # Auge hinter dem Fadenkreuz, auf derselben Linie
                    e,r=a['Socket_Eye']['position_m'],a['Socket_Reticle']['position_m']
                    self.assertGreater(e[1],r[1]);self.assertTrue(close([e[0],e[2]],[r[0],r[2]]))
    def test_grip_support(self):
        for s in G.SHEETS:
            if s[0]!='K':continue
            g=load(s);sp=spec(s);gr=g['grip']
            with self.subTest(sheet=s):
                self.assertEqual(gr['part'],sp['anchors']['Socket_Hand']['part'])
                b=next(p['bounds_m'] for p in g['parts'] if p['id']==gr['part'])
                for q in gr['grip_axis_m']:self.assertTrue(all(b[0][k]-1e-4<=q[k]<=b[1][k]+1e-4 for k in (1,2)),(q,b))   # Achse im Griffteil (Y, Z)
                self.assertLessEqual(abs(gr['grip_tilt_degrees']),90)
                su=g['support']
                self.assertEqual(su['part'],sp['anchors']['Socket_SupportHand']['part'])
                if su['part']:self.assertTrue(su['radius_m']['half_height_m']>0 and su['radius_m']['half_width_m']>0)
                else:self.assertIsNone(su['radius_m']);self.assertTrue(su['reason'])

class StringBlock(unittest.TestCase):
    def test_bows_and_crossbows(self):
        """Bogen (KX10) und Armbrust (KX19): Sehne vorhanden, Spitzen außen an Wurfarm/Rolle, Nockpunkt zwischen den Spitzen in der
        Ebene der Pfeilachse und hinter der Pfeilspitze; andere Blätter ohne Block"""
        n=0
        for s in G.SHEETS:
            g=load(s);st=g['string']
            with self.subTest(sheet=s):
                if g['sheet']['name_de'] not in G.STRING_TYPES:self.assertIsNone(st);continue
                n+=1;self.assertTrue(st['present'],st);ax='XYZ'.index(st['span_axis']);a,b=st['limb_tips_m'];k=st['nock_m']
                self.assertEqual(st['kind'],'crossbow' if st['span_axis']=='X' else 'bow')
                self.assertTrue(min(a[ax],b[ax])<k[ax]<max(a[ax],b[ax]))
                labels={p['id']:p['label'] for p in g['parts']}
                self.assertTrue(all(labels[p] in G.LIMB_LABELS+G.CAM_LABELS for p in st['limb_tip_parts']))
                self.assertTrue(st['string_parts'] and all(labels[p]=='Sehne' for p in st['string_parts']))
                ar=st['arrow_axis'];ref=ar.get('rear_m') or ar['through_m']
                self.assertAlmostEqual(k[ax],ref[ax],delta=0.003)            # Nock auf der Pfeilachse (quer zur Spannachse)
                if ar.get('tip_m'):self.assertGreater(k[1],ar['tip_m'][1])  # Nock hinter der Spitze
                self.assertEqual(st['nock_behind_hand_m'],k[1])
        self.assertEqual(n,12)

class Decals(unittest.TestCase):
    def test_decals(self):
        for s in G.SHEETS:
            if s[0]!='K':continue
            g=load(s);sp=spec(s)
            with self.subTest(sheet=s):
                self.assertEqual(len(g['decals']),len(sp['decals']))
                bounds={p['id']:p['bounds_m'] for p in g['parts']}
                for a,b in zip(g['decals'],sp['decals']):
                    self.assertEqual((a['part'],a['surface'],a['channel']),(b['part'],b['surface'],b['channel']))
                    n=G.newell(a['polygon_m']);self.assertGreater(G._dot(n,a['normal']),0)
                    bb=G._bb(a['polygon_m']);self.assertTrue(close(bb[0],b['bounds_m'][0]) and close(bb[1],b['bounds_m'][1]))
                out=[i for i,a in enumerate(g['decals']) if not G.decal_on_part(a,bounds[a['part']])]
                self.assertEqual(out,g['checks']['decals_outside_part'])   # Befund im Spec (Aufkleber ragt im Blatt über sein Teil)

    def test_outside_reported(self):
        n=sum(len(load(s)['checks']['decals_outside_part']) for s in G.SHEETS if s[0]=='K')
        print(f'\n  Aufkleber über ihr Teil hinaus (Blatt, > 1 mm): {n}',file=sys.stderr)

def _rot(v,u,a):
    """v um die Einheitsachse u um a drehen (Rodrigues)"""
    c,s_=math.cos(a),math.sin(a);d=G._dot(u,v);x=G._cross(u,v)
    return [v[i]*c+x[i]*s_+u[i]*d*(1-c) for i in range(3)]
class Primitives(unittest.TestCase):
    """Primitive aus ihren Parametern nachbauen: jede erzeugte Ecke muss eine Ecke des Netzes sein (0,02 mm), und das Netz hat keine weiteren"""
    def _rebuild(self,pr):
        if pr['type']=='prism':
            ax='XYZ'.index(pr['axis']);o=[i for i in range(3) if i!=ax];out=[]
            for t in pr['range_m']:
                for q in pr['profile_m']:
                    v=[0.0,0.0,0.0];v[ax]=t;v[o[0]],v[o[1]]=q;out.append(v)
            return [out],2e-5
        u=G._norm([pr['end_m'][k]-pr['start_m'][k] for k in range(3)]);r_end=pr.get('radius_m') or pr['radius_end_m'];r_st=pr.get('radius_m') or pr['radius_start_m']
        r0=[pr['first_vertex_m'][k]-pr['end_m'][k] for k in range(3)];n=pr['segments']
        self.assertAlmostEqual(math.sqrt(G._dot(r0,r0)),r_end,delta=2e-5)
        sols=[]
        for sg in (1,-1):   # Drehsinn offen
            ring=[_rot(r0,u,sg*2*math.pi*k/n) for k in range(n)]
            sols.append([[pr['end_m'][i]+q[i] for i in range(3)] for q in ring]+[[pr['start_m'][i]+q[i]*r_st/r_end for i in range(3)] for q in ring])
        return sols,2e-5*max(1.0,r_st/r_end)   # Rundung der ersten Ecke (0,01 mm) wächst mit dem Radienquotienten
    def test_primitive_rebuilds_mesh(self):
        n=0
        for s in G.SHEETS:
            for p in load(s)['parts']:
                pr=p['primitive']
                if not pr:continue
                n+=1;V=p['mesh']['vertices']
                with self.subTest(sheet=s,part=p['id']):
                    ok=False;sols,tol=self._rebuild(pr)
                    for pts in sols:
                        hit=all(any(max(abs(q[k]-v[k]) for k in range(3))<=tol for v in V) for q in pts)
                        cover=all(any(max(abs(q[k]-v[k]) for k in range(3))<=tol for q in pts) for v in V)
                        ok=ok or (hit and cover)
                    self.assertTrue(ok,pr['type'])
        self.assertGreater(n,1000)
    def test_counterproof(self):
        """Gegenprobe: verschobener Zylinder, vertauschte Kegelradien, falsche Segmentzahl fallen auf"""
        g=load('KG02');p=next(p for p in g['parts'] if p['primitive'] and p['primitive']['type']=='cylinder');V=p['mesh']['vertices']
        def fits(pr):
            try:pts,_=self._rebuild(pr)
            except AssertionError:return False
            return any(all(any(max(abs(q[k]-v[k]) for k in range(3))<=2e-5 for v in V) for q in s_) and
                       all(any(max(abs(q[k]-v[k]) for k in range(3))<=2e-5 for q in s_) for v in V) for s_ in pts)
        pr=p['primitive'];self.assertTrue(fits(pr))
        self.assertFalse(fits(dict(pr,start_m=[c+0.01 for c in pr['start_m']])))
        self.assertFalse(fits(dict(pr,segments=pr['segments']+2)))
        self.assertFalse(fits(dict(pr,first_vertex_m=[c+0.003 for c in pr['first_vertex_m']])))

class Coplanar(unittest.TestCase):
    def _box(self,x0,x1,y0,y1,z0,z1):
        V=[[x,y,z] for x in (x0,x1) for y in (y0,y1) for z in (z0,z1)]
        return dict(vertices=V,faces=[[0,1,3,2],[4,6,7,5],[0,4,5,1],[2,3,7,6],[0,2,6,4],[1,5,7,3]],hard=[1]*6)
    def test_rule_with_counterproof(self):
        a=self._box(0,0.1,0,0.02,0,0.02)
        same=self._box(0.05,0.15,0,0.02,0,0.02)       # gleiche Seitenflächen, Abstand 0
        near=self._box(0.05,0.15,0.0003,0.0203,0.0003,0.0203)   # um 0,3 mm versetzt (unter der Regel)
        far=self._box(0.05,0.15,0.001,0.021,0.001,0.021)   # alles ≥ 1 mm versetzt
        sit=self._box(0.0,0.1,0,0.02,0.02,0.04)       # sitzt oben auf (entgegengesetzte Flächen)
        self.assertTrue(G.coplanar([('p00',a),('p01',same)]))
        self.assertEqual([f['distance_m'] for f in G.coplanar([('p00',a),('p01',near)])],[0.0003])
        self.assertEqual(G.coplanar([('p00',a),('p01',far)]),[])
        self.assertEqual(G.coplanar([('p00',a),('p01',sit)]),[])
        # Befund unabhängig von der Lage (0,3 m verschoben) und an Rundungsgrenzen der Normale (leicht gekippt)
        sh=lambda m,d:dict(m,vertices=[[v[0]+d,v[1]+d,v[2]+d] for v in m['vertices']])
        self.assertEqual([f['distance_m'] for f in G.coplanar([('p00',sh(a,0.3)),('p01',sh(near,0.3))])],[0.0003])
        t=math.radians(0.29);tilt=lambda m:dict(m,vertices=[[v[0],v[1]*math.cos(t)-v[2]*math.sin(t),v[1]*math.sin(t)+v[2]*math.cos(t)] for v in m['vertices']])
        self.assertTrue(G.coplanar([('p00',tilt(a)),('p01',tilt(near))]))
    def test_findings_reported(self):
        """Befunde stehen in checks.coplanar (Daten für Toolgen, kein Fehler); Zahl ins Protokoll"""
        tot=vis=sheets=0
        for s in G.SHEETS:
            c=load(s)['checks']['coplanar'];tot+=len(c);vis+=sum(not f['same_look'] for f in c);sheets+=bool(c)
            for f in c:self.assertLess(f['distance_m'],G.COPLANAR_M);self.assertGreaterEqual(f['overlap_m2'],G.OVERLAP_MIN_M2)
        print(f'\n  Koplanar-Befunde: {tot} Teilpaare auf {sheets} Blättern, davon {vis} mit unterschiedlichem Aussehen',file=sys.stderr)

class Budget(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(BUDGET),'Toolgen-Budget nicht gefunden (TOOLGEN_ROOT)')
    def test_world_budget(self):
        w=json.loads(_read(BUDGET))['world'];weap={k:v for k,v in w.items() if k not in ('portal_emitter','magnet_gripper','flashlight')}
        cap=max(weap.values())   # neue Typen ohne Werkzeug: größtes Waffen-Budget (Annahme, bis TG-B je Typ festlegt)
        over=[]
        for s in G.SHEETS:
            g=load(s)
            if s[0]!='K':continue
            tid=g['sheet']['toolgen_id'];b=w.get(tid) or (w.get('scout_rifle') if tid=='trace_rifle' else None) or cap
            if g['counts']['triangles']>=b:over.append((s,g['counts']['triangles'],b))
        self.assertEqual(over,[])

if __name__=='__main__':unittest.main()
