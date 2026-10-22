"""Schema- und Stimmigkeitstest der Spec-Dateien (claude/output/sheets/KXnn.spec.json). Ohne numpy, ohne Bildstufe.
   python3 -m unittest claude/generator/test_spec.py      (oder: python3 claude/generator/test_spec.py)
"""
from cepaths import E3D,CLAUDE,OUT
import copy,json,math,os,re,sys,unittest
sys.path.insert(0,E3D)
import export_spec,sheetmodels,variants
from eng import CHANNELS,Model,rect,channel,copy_channels,split_sight
from xlroles import recolor,VARIANTS,color_roles,assign_channels

def _read(fn):
    with open(fn,encoding='utf-8') as f:return f.read()
SCHEMA=json.loads(_read(os.path.join(CLAUDE,'docs','weapon-spec.schema.json')))
TYPES={'object':dict,'array':list,'string':str,'boolean':bool,'null':type(None)}

def validate(x,s,path='$',root=SCHEMA):
    """Kleine Teilmenge von JSON Schema (siehe description im Schema); liefert Fehlertexte."""
    if '$ref' in s:
        node=root
        for k in s['$ref'][2:].split('/'):node=node[k]
        return validate(x,node,path,root)
    err=[]
    if 'type' in s:
        ts=s['type'] if isinstance(s['type'],list) else [s['type']]
        ok=any((t=='number' and isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)) or
               (t=='integer' and isinstance(x,int) and not isinstance(x,bool)) or
               (t in TYPES and isinstance(x,TYPES[t]) and not (t!='boolean' and isinstance(x,bool))) for t in ts)
        if not ok:return [f'{path}: Typ {type(x).__name__} statt {ts}']
    if 'const' in s and x!=s['const']:err.append(f'{path}: {x!r} != {s["const"]!r}')
    if 'enum' in s and x not in s['enum']:err.append(f'{path}: {x!r} nicht in {s["enum"]}')
    if isinstance(x,str) and 'pattern' in s and not re.search(s['pattern'],x):err.append(f'{path}: {x!r} passt nicht zu {s["pattern"]}')
    if isinstance(x,(int,float)) and not isinstance(x,bool) and 'minimum' in s and x<s['minimum']:err.append(f'{path}: {x} < {s["minimum"]}')
    if isinstance(x,dict):
        for k in s.get('required',[]):
            if k not in x:err.append(f'{path}: {k} fehlt')
        props=s.get('properties',{})
        for k,v in x.items():
            if k in props:err+=validate(v,props[k],f'{path}.{k}',root)
            elif s.get('additionalProperties') is False:err.append(f'{path}: unbekanntes Feld {k}')
    if isinstance(x,list):
        if len(x)<s.get('minItems',0):err.append(f'{path}: weniger als {s["minItems"]} Einträge')
        if 'maxItems' in s and len(x)>s['maxItems']:err.append(f'{path}: mehr als {s["maxItems"]} Einträge')
        if 'items' in s:
            for i,v in enumerate(x):err+=validate(v,s['items'],f'{path}[{i}]',root)
    return err

def load(sheet):return json.loads(_read(export_spec.path(sheet)))

class SpecFiles(unittest.TestCase):
    def test_all_present_and_current(self):
        """10 Dateien je Variante plus die neuen Waffentypen (claude-0.10, wtypes.NEW_SHEETS), jede gleich der Ausgabe des Exporters
        (sonst: python3 claude/generator/export_spec.py)."""
        import wtypes
        self.assertEqual(len(sheetmodels.SHEETS),10*len(variants.LETTERS)+sum(len(v) for v in wtypes.NEW_SHEETS.values()))
        stale=[s for s in sheetmodels.SHEETS if not os.path.exists(export_spec.path(s)) or
               _read(export_spec.path(s))!=export_spec.dumps(export_spec.build(s))]
        self.assertEqual(stale,[],'veraltet oder fehlend – python3 claude/generator/export_spec.py')
        extra=sorted(f for f in os.listdir(OUT) if f.startswith('K') and f.endswith('.spec.json') and f[:-10] not in sheetmodels.SHEETS)   # VSnn: Sight-Spec (test_sight_spec.py)
        self.assertEqual(extra,[])

    def test_schema(self):
        for s in sheetmodels.SHEETS:
            with self.subTest(sheet=s):self.assertEqual(validate(load(s),SCHEMA),[])

    def test_consistency(self):
        for s in sheetmodels.SHEETS:
            sp=load(s)
            with self.subTest(sheet=s):
                self.assertEqual(sp['sheet']['id'],s)
                tid,ref,el=export_spec.WEAPONS[sp['weapon']['name_de']]
                self.assertEqual((sp['weapon']['toolgen_id'],sp['element']),(tid,el))
                # Maßstab: Bezugslänge auf 0,5 mm
                d=sp['dimensions_m']['with_sight']
                got=max(d['length'],d['height'],d['width']) if tid=='bow' else d['length']
                self.assertAlmostEqual(got,ref,delta=5e-4)
                self.assertAlmostEqual(sp['units']['model_unit_m']*sp['units']['model_length_units'],ref,delta=5e-4)
                # Anker: Griff ist Ursprung, alle Werte endlich, Mündung vor dem Griff (−Y)
                a=sp['anchors']
                self.assertEqual(a['Socket_Hand']['position_m'],[0.0,0.0,0.0])
                self.assertIsNotNone(a['Socket_Muzzle']['position_m'])
                self.assertLess(a['Socket_Muzzle']['position_m'][1],0)
                for k,v in a.items():
                    if v['position_m'] is None:self.assertIsNone(v['model'])
                # Teile/Aufkleber/Visier verweisen richtig
                ids=[p['id'] for p in sp['parts']]
                self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue({dd['part'] for dd in sp['decals']}<=set(ids))
                self.assertEqual(sorted(sp['sight']['parts']),sorted(p['id'] for p in sp['parts'] if p['sight']))
                self.assertEqual(sp['sight']['present'],bool(sp['sight']['parts']))
                self.assertEqual(sp['sight']['kind'] is None,not sp['sight']['present'])
                # jeder benutzte Kanal hat in jeder Variante eine Farbe, unbenutzte keine
                used={p['channel'] for p in sp['parts']}|{dd['channel'] for dd in sp['decals']}
                self.assertEqual(sorted(used,key=CHANNELS.index),sp['channels_used'])
                for v in sp['palette']:
                    self.assertEqual(list(v['channels']),list(CHANNELS),v['id'])
                    self.assertEqual({c for c,h in v['channels'].items() if h},used,v['id'])
                    self.assertEqual(list(a),['Socket_Hand','Socket_SupportHand','Socket_Muzzle','Socket_CenterOfMass','Socket_Sight'])
                self.assertEqual([v['id'] for v in sp['palette']],export_spec.VARIANT_IDS)
                self.assertEqual([v['swatches'] for v in sp['palette'][1:]],[[c.upper() for c in p] for _,p in VARIANTS[:3]])
                # leuchtende Teile liegen auf Energie-/Leuchtkanälen, wenn nicht ausdrücklich anders gesetzt
                for p in sp['parts']:
                    if p['emissive'] and p['channel_source']!='explicit':self.assertIn(p['channel'],('MT_Energy','MT_Emission'))

class Channels(unittest.TestCase):
    def _model(self):
        m=Model()
        m.prism(rect(0,0,100,40),'#DDDDDD',-10,10);m.parts[-1]['label']='Gehäuse'
        m.prism(rect(60,40,20,50),'#222222',-8,8);m.parts[-1]['label']='Griff'
        m.prism(rect(100,10,60,10),'#888888',-4,4);m.parts[-1]['label']='Lauf'
        m.prism(rect(10,4,30,6),'#FF8800',-11,11,emit=True)
        return m
    def test_explicit_wins(self):
        m=self._model();channel(m,'MT_Accent')
        role=color_roles(m);pch,_=assign_channels(m,role,lambda P:1.0,lambda d:1.0)
        self.assertEqual(pch[-1],('MT_Accent','explicit'))
        self.assertEqual(pch[0][0],'MT_Primary');self.assertEqual(pch[1][0],'MT_Detail');self.assertEqual(pch[2][0],'MT_Metal')
    def test_explicit_rejects_unknown(self):
        m=self._model()
        with self.assertRaises(AssertionError):channel(m,'MT_Glow')
    def test_copy_channels(self):
        m=self._model();copy_channels(m,[{},{'ch':'MT_Secondary'},{},{}])
        self.assertEqual(m.parts[1]['channel'],'MT_Secondary');self.assertNotIn('channel',m.parts[0])
    def test_decal_channel(self):
        """'dch' setzt den Kanal aller Aufkleber eines Teils (claude-0.15.2): KG02-Schienenquadrate MT_Metal statt Helligkeitsrolle."""
        dec={d['channel'] for d in load('KG02')['decals'] if d['part']=='p10'}
        self.assertEqual(dec,{'MT_Metal'})
        with self.assertRaises(AssertionError):copy_channels(self._model(),[{},{'dch':'MT_Glow'},{},{}])
    def test_channel_does_not_change_sheet_colors(self):
        """Ein gesetzter Kanal ändert die Farbvarianten des Blatts nicht (recolor liest ihn nicht)."""
        for s in sheetmodels.SHEETS:
            g,_=split_sight(sheetmodels.load(s)['m'])
            g2=copy.deepcopy(g)
            for P in g2.parts:P['channel']='MT_Detail'
            strip=lambda m:[{k:v for k,v in P.items() if k!='channel'} for P in m.parts]
            for _,pal in VARIANTS:
                self.assertEqual(strip(recolor(g,pal)),strip(recolor(g2,pal)),s)

class SkinSpec(unittest.TestCase):
    """Feld skin (claude-0.3): fünf Skins je Blatt, Verweise, Farben je Variante, Geometrie der Aufkleber/Schmuckteile."""
    def test_skins(self):
        import skins
        heroes={}
        for s in sheetmodels.SHEETS:
            sp=load(s);sk=sp['skin']
            with self.subTest(sheet=s):
                ids=[it['id'] for it in sk['items']]
                self.assertEqual(len(set(ids)),5);self.assertTrue(set(ids)<=set(sk['catalog']))
                self.assertEqual(sk['hero'],ids[0]);self.assertEqual([it['hero'] for it in sk['items']],[True]+[False]*4)
                heroes[ids[0]]=heroes.get(ids[0],0)+1
                parts={p['id']:p for p in sp['parts']}
                lo,hi=sp['dimensions_m']['weapon']['bounds_m'];ext=max(hi[k]-lo[k] for k in range(3))
                for it in sk['items']:
                    used=set(it['slots_used'])
                    for v in sp['palette']:
                        cv=it['colors'][v['id']]
                        self.assertEqual(set(cv),used)
                        for sl,c in cv.items():
                            if sl.startswith('MT_'):
                                self.assertEqual(c['color'],v['channels'][sl] or v['swatches'][skins.SWATCH_FALLBACK[sl]],(it['id'],v['id'],sl))
                                self.assertEqual(c['source'],'channel' if v['channels'][sl] else 'swatch')
                            else:self.assertEqual(c['color'],it['accents'][sl]['color'])
                    for L in it['layers']:
                        ref=([L['slot']] if 'slot' in L else [])+L.get('slots',[])+[dd['slot'] for dd in L.get('decals',[])]
                        self.assertTrue(set(ref)<=used,(it['id'],L['type']))
                        if L['type'] in ('side_block','bands','gradient','rings','finish','edge_wear'):
                            self.assertTrue(L['parts']);self.assertTrue(set(L['parts'])<=set(parts))
                            self.assertFalse(any(parts[q]['sight'] or parts[q]['emissive'] for q in L['parts']))
                        if L['type']=='bands':self.assertGreaterEqual(L['period_m']+1e-9,L['width_m']);self.assertGreater(L['width_m'],0)
                        if L['type']=='glyphs':
                            self.assertIn(L['part'],parts)
                            for dd in L['decals']:   # flach auf der Seitenfläche (X konstant), im Hüllquader der Waffe
                                xs=[q[0] for q in dd['points_m']];self.assertLess(max(xs)-min(xs),1e-3)
                                for q in dd['points_m']:
                                    for k in range(3):self.assertTrue(lo[k]-0.02*ext<=q[k]<=hi[k]+0.02*ext,(it['id'],q))
                        if L['type']=='trim':
                            self.assertIn(L['attach'],parts);self.assertTrue(L['parts'])
                            for tp in L['parts']:
                                b=tp['bounds_m']
                                for k in range(3):self.assertTrue(lo[k]-0.12*ext<=b[0][k] and b[1][k]<=hi[k]+0.12*ext,(it['id'],b))
        # jeder Katalog-Skin ist auf mindestens drei Blättern Hauptskin
        self.assertEqual(set(heroes),{c['id'] for c in skins.CATALOG});self.assertGreaterEqual(min(heroes.values()),3)

class SkinGeometry(unittest.TestCase):
    def test_glyph_layout_and_mirror(self):
        import skins
        polys,w=skins.layout([('digit','0'),('digit','7')],20)
        self.assertEqual(len(polys),6+3);self.assertGreater(w,20)
        for poly,_ in polys:self.assertTrue(all(-1<=y<=21 for _,y in poly))
        d=sheetmodels.load('KD02');rs=skins.resolve(d['m'],'rennstreifen','KD02',d['num'],d['palette'])
        g=[L for L in rs['layers'] if L['type']=='glyphs'][0]
        x0,y0,x1,y1=g['rect'];lft=[dd for dd in g['decals'] if dd[0]=='z+'];rgt=[dd for dd in g['decals'] if dd[0]=='z-']
        self.assertEqual(len(lft),len(rgt))
        for a,b in zip(lft,rgt):   # rechte Seite = linke an der Rechteckmitte gespiegelt
            for (xa,ya),(xb,yb) in zip(a[2],b[2]):self.assertAlmostEqual(xa+xb,x0+x1,6);self.assertAlmostEqual(ya,yb,6)
        P=d['m'].parts[g['part']];poly=skins.side_face(P)[0]
        for x,y in ((x0,y0),(x1,y0),(x0,y1),(x1,y1)):self.assertTrue(skins.inside(poly,x,y))
    def test_pick_is_stable_and_distinct(self):
        import skins
        for s in ('KC01','KH10'):
            d=sheetmodels.load(s);a=skins.pick(s,d['m'],d['num'],d['palette']);b=skins.pick(s,d['m'],d['num'],d['palette'])
            self.assertEqual(a,b);self.assertEqual(len(set(a)),5)

LAYER_FIELDS={'side_block':['parts','slot','poly_yz_m'],'bands':['parts','dir','t0_m','width_m','period_m','count','slots','window_yz_m'],
 'gradient':['parts','dir','t0_m','t1_m','steps','slots'],'rings':['parts','axis','center_yz_m','r0_m','width_m','gap_m','count','slots'],
 'finish':['parts','slot','target'],'edge_wear':['parts','width_mm','coverage','color'],
 'glyphs':['part','items','content','height_m','bounds_m','decals'],'trim':['kind','attach','slot','count','parts']}
class SkinFrame(unittest.TestCase):
    """Pflichtfelder je Lagentyp (das Schema prüft nur type/block) und Umrechnung Modell -> Toolgen-Rahmen."""
    def test_layer_fields(self):
        for s in sheetmodels.SHEETS:
            for it in load(s)['skin']['items']:
                for L in it['layers']:
                    with self.subTest(sheet=s,skin=it['id'],type=L['type']):
                        self.assertEqual([k for k in LAYER_FIELDS[L['type']] if k not in L],[])
                        if L['type']=='trim':
                            for tp in L['parts']:self.assertEqual(sorted(tp),['bounds_m','profile_yz_m','x_m'])
    def test_frame(self):
        import skins
        s='KD02';sp=load(s);d=sheetmodels.load(s)
        u=sp['units']['model_unit_m'];o=sp['anchors']['Socket_Hand']['model']
        M=sp['axes']['matrix_model_to_target']
        P=lambda q:[u*sum(M[r][c]*(q[c]-o[c]) for c in range(3)) for r in range(3)]
        it=[i for i in sp['skin']['items'] if i['id']=='rennstreifen'][0]
        rs=skins.resolve(d['m'],'rennstreifen',s,d['num'],d['palette'])
        gm=[L for L in rs['layers'] if L['type']=='glyphs'][0];gs=[L for L in it['layers'] if L['type']=='glyphs'][0]
        pl,val,pts,_=gm['decals'][0];exp=P((pts[0][0],pts[0][1],val))
        for k in range(3):self.assertAlmostEqual(gs['decals'][0]['points_m'][0][k],exp[k],delta=2e-4)
        self.assertEqual(gs['decals'][0]['surface'],'left');self.assertGreater(gs['decals'][0]['points_m'][0][0],0)  # links = +X
        # Seitenband: Modell y (unten) -> Toolgen −Z; t0 im Zielrahmen = u·(t_model − Socket_Hand·dir)
        bm=[L for L in rs['layers'] if L['type']=='bands' and L['dir']==(0.0,1.0,0.0)][0]
        bs=[L for L in it['layers'] if L['type']=='bands' and L['dir']==[0.0,0.0,-1.0]][0]
        self.assertAlmostEqual(bs['t0_m'],u*(bm['t0']-o[1]),delta=2e-4)
        # ein Punkt im Band liegt im Zielrahmen ebenfalls im Band
        q=(o[0],bm['t0']+bm['width']/2,o[2]);pm=P(q);t=sum(pm[k]*bs['dir'][k] for k in range(3))
        self.assertTrue(bs['t0_m']<=t<=bs['t0_m']+bs['width_m'],(t,bs['t0_m']))

class Variants(unittest.TestCase):
    """Varianten-Register (claude-0.4): Namensregel für neue Varianten, Name im Spec, Facettenkörper der Variante J."""
    def test_naming_rule(self):
        self.assertEqual(len(set(variants.LETTERS)),len(variants.LETTERS))
        for v in variants.VARIANTS:
            if v['letter'] in 'CDFGH':self.assertIsNone(v['name']);continue   # älter als die Regel
            with self.subTest(variant=v['letter']):self.assertEqual(variants.name_problems(v['letter'],v['name']),[])
        self.assertTrue(variants.name_problems('L','Black Ice'))        # vergeben
        self.assertTrue(variants.name_problems('L','Parallax'))         # Codex
        self.assertTrue(variants.name_problems('L','Flux Bloom'))       # Codex
        self.assertTrue(variants.name_problems('L','schwarzes eis'))    # Schreibweise
        self.assertTrue(variants.name_problems('L',None))
        self.assertTrue(variants.name_problems('I','Glass Fang'))       # I wird nicht vergeben
        self.assertTrue(variants.name_problems('K','Glass Fang'))       # K gehört Codex (KK01 …)
        self.assertTrue(variants.name_problems('A','Glass Fang'))       # A gehört Codex (KA01 …)
        self.assertEqual(variants.name_problems('L','Glass Fang'),[])
    def test_spec_name(self):
        for s in sheetmodels.SHEETS:
            with self.subTest(sheet=s):self.assertEqual(load(s)['sheet']['variant_name'],variants.name(s[1]))
    def test_facet_faces(self):
        import jlib
        m=jlib.model([jlib.K([(0,0),(80,0),(100,20),(80,40),(0,40)],'#222222',-10,10,b=4,bz=4)])
        F=m.parts[0]['F']
        self.assertEqual(tuple(F[0]['n']),(0,0,1));self.assertEqual(tuple(F[1]['n']),(0,0,-1))
        self.assertEqual({v[2] for v in F[0]['v']},{10});self.assertEqual({v[2] for v in F[1]['v']},{-10})
        # Seitenfläche eingerückt, Normalen Einheitslänge, je Kante Band + zwei Facetten
        xs=[v[0] for v in F[0]['v']];self.assertAlmostEqual(min(xs),4,places=6)
        self.assertEqual(len(F),2+3*5)
        for f in F:self.assertAlmostEqual(sum(c*c for c in f['n']),1,places=9)
        import skins
        self.assertIsNotNone(skins.side_face(m.parts[0]))
        with self.assertRaises(ValueError):jlib.inset([(0,0),(10,0),(10,4),(0,4)],3)   # Fase breiter als das Teil

class Direction(unittest.TestCase):
    """Richtungstest (claude-0.5, Fenster ab 0.5.2 an der Funktionsfläche; Cubegen docs/DEVELOPER.md 9.17): Mündung vorn auf der
    Laufachse (−Y), Griff um Socket_Hand, Visier oben, Durchsicht jedes Fensters entlang −Y; bekannte Querfenster KNOWN_CROSS_WINDOWS. Gegenbeweis: mit gespiegelter oder vertauschter Achse im Exporter schlägt er an."""
    def test_sheets(self):
        import spec_checks
        for s in sheetmodels.SHEETS:
            pr=spec_checks.direction_problems(load(s))
            with self.subTest(sheet=s):
                self.assertTrue(spec_checks.known_ok(s,pr),f'{s}: Befunde weichen von KNOWN_CROSS_WINDOWS ab: {pr}')
        self.assertEqual(spec_checks.KNOWN_CROSS_WINDOWS,{})   # 23 Querfenster (0.5.2) mit der Visier-Serie behoben (claude-0.7)
        self.assertTrue(set(spec_checks.KNOWN_CROSS_WINDOWS)<=set(sheetmodels.SHEETS))
    def test_window_cases(self):
        """Gegenbeweis je Fall an der Funktionsfläche: Seitenscheibe, Scheibe/Ring quer, Leuchtteil oben quer, falsche Achse – und
        die richtigen Gegenstücke ohne Befund. Ein neues Querfenster auf einem sauberen Blatt macht den Blatttest rot."""
        import spec_checks as C
        B=lambda ex:[[0,0,0.1],ex]
        decals=[dict(bounds_m=B([0.0,0.02,0.11])),dict(bounds_m=B([0.02,0.0,0.11]))]          # flach in X (Seite) / in Y (vorn)
        parts={'pA':dict(bounds_m=B([0.005,0.04,0.14])),'pB':dict(bounds_m=B([0.04,0.005,0.14])),'pC':dict(bounds_m=B([0.04,0.03,0.105]))}
        def el(typ,ax,decal=None,part='pA'):return dict(type=typ,decal=decal,part=part,emissive=False,view_axis_m=ax,center_m=[0,0,0.1])
        quer=lambda es:C.cross_windows(C.window_problems(es,parts,decals,hand_z=0.0))
        self.assertEqual(quer([el('decal',[-1,0,0],0)]),['d0'])                 # Seitenscheibe
        self.assertEqual(C.window_problems([el('decal',[0,-1,0],1)],parts,decals,hand_z=0.0),[])   # Scheibe vorn
        self.assertEqual(quer([el('disc',[-1,0,0],part='pA')]),['pA'])           # Ring/Platte quer
        self.assertEqual(C.window_problems([el('disc',[0,-1,0],part='pB')],parts,decals,hand_z=0.0),[])
        self.assertEqual(quer([el('part',[0,0,-1],part='pC')]),['pC'])           # Leuchtteil flach oben
        pr=C.window_problems([el('decal',[-1,0,0],1)],parts,decals,hand_z=0.0)    # Achse widerspricht der Geometrie
        self.assertTrue(any(p.startswith('Fensterachse [d1]') for p in pr))
        sp=load('KC03');self.assertEqual(C.direction_problems(sp),[])            # neues Querfenster auf sauberem Blatt (Glasscheibe gedreht)
        e=sp['sight']['window_geometry']['elements'][0];parts={p['id']:p for p in sp['parts']};b=parts[e['part']]['bounds_m']
        b[1][0],b[1][1]=b[0][0],b[0][1]+0.02;e['view_axis_m']=[-1.0,0.0,0.0]
        self.assertFalse(C.known_ok('KC03',C.direction_problems(sp)))
        # Exporter: Seitenaufkleber ab PANE_MIN_FRACTION ist Fenster, kleine Punkte nicht (seit claude-0.7 ohne Blatt mit Seitenscheibe:
        # Modell im Test, Teil 20 × 20 × 10 mit Aufkleber 8 × 8 = 16 % bzw. 2 × 2 = 1 %)
        F=export_spec.Frame(0.001,(0,0,0))
        def frac(w):
            m=Model();m.prism(rect(0,0,20,20),'#808080',-5,5);m.decal('z+',5,rect(6,6,w,w),'#FFFFFF',both=False)
            g,_=export_spec.window_geometry('glass',[(0,m.parts[0])],['p00'],F,{(0,0):0})
            return [x['face_fraction'] for x in (g or {}).get('elements',[])]
        self.assertTrue(frac(8) and frac(8)[0]>=export_spec.PANE_MIN_FRACTION)
        self.assertEqual(frac(2),[])
    def test_counterproof_mirrored_axes(self):
        import spec_checks
        sample=['KC01','KD02','KF03','KG04','KH05','KJ06','KC07','KD08','KF09','KG10']   # jeder Waffentyp einmal
        bad={'Y gespiegelt (vorn +Y)':[[0,0,1],[1,0,0],[0,-1,0]],'Z gespiegelt (oben −Z)':[[0,0,1],[-1,0,0],[0,1,0]],
             'X/Y vertauscht':[[-1,0,0],[0,0,1],[0,-1,0]]}
        # je Achse schlägt die zuständige Prüfung an: Y -> Mündung, Z -> Visier oben, X/Y -> Fenster (Blätter mit richtigem Fenster;
        # bei bekannten Querfenstern dreht der Tausch die Seitenscheibe in −Y, dort fängt die Mündungsprüfung)
        expect={'Y gespiegelt (vorn +Y)':'Socket_Muzzle nicht vor dem Griff','Z gespiegelt (oben −Z)':'Visier nicht über der Mündungsachse',
                'X/Y vertauscht':'Fenster'}
        old=export_spec.M2B
        try:
            for name,M in bad.items():
                export_spec.M2B=M
                for s in sample:
                    sp=json.loads(export_spec.dumps(export_spec.build(s)));pr=spec_checks.direction_problems(sp)
                    with self.subTest(axes=name,sheet=s):
                        self.assertTrue(pr)
                        if name!='X/Y vertauscht' or (sp['sight']['window_geometry'] and s not in spec_checks.KNOWN_CROSS_WINDOWS):
                            self.assertTrue(any(p.startswith(expect[name]) for p in pr),pr)
        finally:export_spec.M2B=old
        self.assertEqual(spec_checks.direction_problems(load('KC01')),[])
    def test_muzzle_extension(self):
        """Mündung über unbezeichnete Teile auf der Achse verlängert (Pfeilspitze, Kappe), Rakete im Rohr zählt nicht."""
        sp=load('KD10');self.assertIn('verlängert über p14',sp['anchors']['Socket_Muzzle']['source'])
        sp=load('KC09');src=sp['anchors']['Socket_Muzzle']['source']   # Kappe p18, Rakete p21 mit Heck p19 (bis 0.6: p24, p27, p25)
        self.assertIn('p18',src);self.assertNotIn('p19',src);self.assertNotIn('p21',src)
        self.assertEqual(sp['anchors']['Socket_Muzzle']['part'],'p09')

class MovingParts(unittest.TestCase):
    """moving_parts (claude-0.5): Arten und Achsen wie Toolgens Use-Clip, Wurzel fest, Zuordnung nur über Bezeichnungen."""
    def test_moving(self):
        for s in sheetmodels.SHEETS:
            sp=load(s);mv=sp['moving_parts'];import wtypes;tid=wtypes.key(sp['weapon']['name_de'])
            with self.subTest(sheet=s):
                self.assertIs(mv['root_moves'],False)
                self.assertEqual([e['kind'] for e in mv['items']],export_spec.WEAPON_MOTIONS[tid])
                self.assertEqual(all(e.get('proposed') for e in mv['items']),True if sp['weapon']['toolgen_id'] is None else not mv['items'])
                self.assertEqual(mv['note'] is None,bool(mv['items']))
                per={p['id']:p['moving'] for p in sp['parts']}
                for e in mv['items']:
                    M=export_spec.MOTIONS[e['kind']]
                    self.assertEqual([(m['type'],m['axis']) for m in e['motions']],[(t,a) for t,a in M['motions']])
                    for m in e['motions']:self.assertEqual(sorted(abs(c) for c in m['axis']),[0,0,1])
                    if e['parts'] is None:self.assertIsNone(e['match']);self.assertIn('nicht ableitbar',e['source'])
                    else:
                        labs=M['labels'] if e['match']=='label' else M['similar']
                        for q in e['parts']:
                            p=[p for p in sp['parts'] if p['id']==q][0]
                            self.assertIn(p['label'],labs);self.assertFalse(p['sight']);self.assertEqual(per[q],e['kind'])
                self.assertEqual({q for q,k in per.items() if k},{q for e in mv['items'] for q in (e['parts'] or [])})
    def test_known_labels(self):
        self.assertEqual(load('KG01')['moving_parts']['items'][0]['parts'],['p06'])        # Schlitten
        self.assertEqual(load('KF04')['moving_parts']['items'][0]['match'],'label')         # Pumpgriff
        mv=load('KG02')['moving_parts']['items'][0]                                         # Ladehebel (claude-0.15)
        self.assertEqual((mv['parts'],mv['match'],mv['labels']),(['p32'],'label',['Ladehebel']))
        self.assertIsNone(load('KC02')['moving_parts']['items'][0]['parts'])               # Verschluss nicht gezeichnet
        self.assertEqual(load('KC10')['moving_parts']['items'],[])                          # Bogen

class Operation(unittest.TestCase):
    """Feld BEDIENUNG (claude-0.10 neue Typen, ab 0.11 alle Waffenblätter): jedes Blatt hat operation; Texte kurz genug für die Kachel;
    bestehende Blätter aus ops.OPS, neue aus META['op']; neue Typen in allen Varianten (claude-0.11) mit allen beweglichen Teilen im Modell."""
    def test_all_sheets(self):
        import ops,wtypes
        self.assertEqual(set(ops.OPS),{f'K{v}{n}' for v in variants.LETTERS for n in sheetmodels.NUMS})
        for s in sheetmodels.SHEETS:
            sp=load(s);o=sp.get('operation')
            with self.subTest(sheet=s):
                self.assertIsNotNone(o)
                for k in ('reload','action','fire'):
                    for lang in ('de','en'):self.assertTrue(0<len(o[k][lang])<=ops.MAXLEN,(k,lang,len(o[k][lang])))
                self.assertIn('ops.OPS' if s[2:] in sheetmodels.NUMS else "META['op']",o['source'])
                if wtypes.is_new(sp['weapon']['name_de']):
                    for e in sp['moving_parts']['items']:self.assertIsNotNone(e['parts'],e['kind'])
    def test_moving_header(self):
        import ops
        for s,o in ops.OPS.items():
            with self.subTest(sheet=s):self.assertIsInstance(o['moving'],list)
    def test_new_sheet_nicks(self):
        """Nick je Variante eindeutig; neue Blätter eines Typs in allen Varianten mit demselben Typnamen"""
        for v in variants.LETTERS:
            nicks=[load(s)['sheet']['nick'] for s in sheetmodels.SHEETS if s[1]==v]
            with self.subTest(variant=v):self.assertEqual(len(nicks),len(set(nicks)) if v!='H' else len(set(nicks))+1)   # KH05/KH08 „Messlatte“ (Bestand)

class SightVocabulary(unittest.TestCase):
    """sight.type/frame und parts[].toolgen_material (claude-0.5.2): kind folgt aus type, Zieltypen im Vokabular, Toolgen-Materialien."""
    def test_vocabulary(self):
        import spec_checks
        for s in sheetmodels.SHEETS:
            sp=load(s);si=sp['sight']
            with self.subTest(sheet=s):
                if not si['present']:self.assertIsNone(si['type']);self.assertIsNone(si['frame']);continue
                self.assertIn(si['type'],export_spec.SIGHT_TYPES)
                k,w=export_spec.SIGHT_TYPES[si['type']]
                self.assertEqual(si['kind'],k)
                if w:self.assertEqual(si['window'],w)
                self.assertEqual(si['frame'] is None,si['window']=='none')
                if si['frame']:self.assertIn(si['frame'],export_spec.SIGHT_FRAMES)
                for p in sp['parts']:self.assertEqual(p['toolgen_material'],export_spec.TOOLGEN_MATERIAL[p['material']])
        self.assertTrue({t[5] for t in spec_checks.CE_SIGHTS.values()}<=set(export_spec.SIGHT_TYPES))
        self.assertEqual(len({t[5] for t in spec_checks.CE_SIGHTS.values()}),7)   # Pistole/Schrotflinte reflex, Sturm-/Impulsgewehr holo (CE 0.111.1)
    def test_toolgen_materials(self):
        fn=os.path.expanduser('~/Claude/cubeescape-toolgen/data/surface_recipes.json')
        if not os.path.exists(fn):self.skipTest('Toolgen-Repo nicht vorhanden')
        with open(fn,encoding='utf-8') as f:mats=json.load(f)['materials']
        self.assertTrue(set(export_spec.TOOLGEN_MATERIAL.values())-{None}<=set(mats))   # None: Klarglas, in Toolgen noch kein Material

class RobotFit(unittest.TestCase):
    """robot_fit (claude-0.5.1): Zielzahlen mit Quelle, Pistole und Bogen ausgenommen, Messung am auf Ziellänge skalierten Blatt."""
    def test_robot_fit(self):
        for s in sheetmodels.SHEETS:
            sp=load(s);r=sp['robot_fit'];tid=sp['weapon']['toolgen_id']
            with self.subTest(sheet=s):
                self.assertIs(r['concept_sheets'],False)
                self.assertEqual([r['robot'][k]['value'] for k in ('height_m','hand_m','arm_m')],[1.5,0.09,0.42])
                if tid is None:   # neue Typen (claude-0.10): nicht im Waffensatz von Cube Escape
                    self.assertFalse(r['applies']);self.assertIn('neuer Designtyp',r['reason']);self.assertIsNone(r['targets']);continue
                if tid in ('pistol','bow'):
                    self.assertFalse(r['applies']);self.assertTrue(r['reason']);self.assertIsNone(r['sheet_at_target'])
                    if tid=='pistol':self.assertEqual(r['targets']['length_min_m']['value'],0.24)
                    continue
                self.assertTrue(r['applies']);t=r['targets']
                for k,v in t.items():self.assertTrue(v['source'].startswith('Cube Escape'),k)
                self.assertEqual(t['length_m']['value'],export_spec.ROBOT_LENGTH[tid])
                self.assertEqual((t['support_hand_max_forward_m']['value'],t['stock_max_behind_m']['value'],t['barrel_min_m']['value'],
                                  t['receiver_min_height_m']['value']),(0.10,0.12,0.03,0.08))
                m=r['sheet_at_target']
                self.assertAlmostEqual(m['scale']*sp['dimensions_m']['with_sight']['length'],t['length_m']['value'],delta=1e-3)
                self.assertAlmostEqual(m['stock_behind_m'],m['scale']*sp['dimensions_m']['with_sight']['bounds_m'][1][1],delta=2e-4)
                self.assertEqual(m['ok']['stock_behind'],m['stock_behind_m']<=0.12)
                sup=sp['anchors']['Socket_SupportHand']['position_m']
                self.assertEqual(m['support_forward_m'] is None,sup is None)

class SightTargets(unittest.TestCase):
    """Visier gegen das CE-Zielbild: nur Hinweise (kein Fehler); die Tabelle hier muss zu Cube Escape passen."""
    def test_hints_are_hints(self):
        import spec_checks
        self.assertEqual(set(spec_checks.CE_SIGHTS),{t for t,_,_ in export_spec.WEAPONS.values()}-{'bow',None})
        for s in sheetmodels.SHEETS:
            h=spec_checks.sight_target_hints(load(s))
            self.assertIsInstance(h,list);self.assertLessEqual(len(h),1)
            self.assertEqual(h,[],s)   # seit claude-0.7 tragen alle Blätter das Visier der Visier-Serie (Hinweise bis 0.6: 41)
        sp=load('KC08');sp['sight'].update(kind='scope',window='lens',type='precision')
        self.assertTrue(spec_checks.sight_target_hints(sp))                                # Gegenbeweis: Spurgewehr mit Röhre
    def test_table_matches_ce(self):
        import spec_checks
        fn=spec_checks.ce_equipment_path()
        if not os.path.exists(fn):self.skipTest('Cube-Escape-Repo nicht vorhanden ('+fn+')')
        ce=spec_checks.ce_table(fn)
        self.assertEqual({nr:(v,d) for nr,v,d,*_ in spec_checks.CE_SIGHTS.values()},ce,
                         'CE-Tabelle „Visiere je Waffe“ geändert – CE_SIGHTS in spec_checks.py nachziehen')

class VisierSerie(unittest.TestCase):
    """Waffen 1–9 tragen das Standardvisier der Visier-Serie VS01–VS09 (claude-0.7, vsmount.py): Lage, Anker und Typ wie im Sight-Spec,
    Glas als Fenster, Visierlinie frei von der Waffe, kein Visierteil in der Waffe, Farben aus den Kanälen der Waffe; Bögen ohne VS."""
    def test_sheets(self):
        import spec_checks
        for s in sheetmodels.SHEETS:
            sp=load(s)
            with self.subTest(sheet=s):
                self.assertEqual(spec_checks.vs_problems(sp),[])
                if sp['weapon']['toolgen_id']=='bow' or not sp['sight']['present']:self.assertNotIn('sight_spec',sp['sight']);continue   # Bogen, Nahkampf (0.10)
                d=sp['dimensions_m'];self.assertEqual(d['with_sight']['length'],d['weapon']['length'])   # Maßstab bleibt der Waffe
                self.assertNotIn('Kimme',sp['sight']['labels']);self.assertNotIn('Korn',sp['sight']['labels'])
    def test_models(self):
        import vsmount,wtypes
        for s in sheetmodels.SHEETS:
            d=sheetmodels.load(s);v=d['vs']
            with self.subTest(sheet=s):
                if d['name']=='Bogen' or d['name'] in wtypes.MELEE:self.assertIsNone(v);continue   # Schwert/Glefe (claude-0.10): kein Visier
                gun=[P for P in d['m'].parts if not P.get('sight')];sight=[P for P in d['m'].parts if P.get('sight')]
                self.assertEqual(sum(1 for P in gun if P.get('label')=='Visierschiene'),1)
                rail=d['m'].parts[v['rail_part']];self.assertEqual(rail.get('label'),'Visierschiene')
                GW=vsmount.Faces([P for P in gun if P is not rail]);RF=vsmount.Faces([rail]);k=v['k'];deep=[0.0,0.0]
                for P in sight:   # kein Visierteil in der Waffe; in die Schiene greifen nur die Klemmbacken der Halterung
                    for f in P['F']:
                        for q in f['v']:
                            for n,(FF,skip) in enumerate(((GW,False),(RF,P['vs_group']=='mount'))):
                                t=None if skip else vsmount.top_y(FF,q[0],q[2])
                                if t is not None:deep[n]=max(deep[n],(q[1]-t)/k)
                self.assertLessEqual(deep[0],0.3,f'Visierteil {deep[0]:.1f} mm in der Waffe')
                self.assertLessEqual(deep[1],0.3,f'Visierteil {deep[1]:.1f} mm in der Schiene')
                for P in sight:   # Leuchtteile bleiben auf Energie-Kanälen (weapon-spec.md › Kanäle)
                    if P['emit']:self.assertIn(P['channel'],('MT_Energy','MT_Emission'),P['label'])
                ch=v['channels']   # Kanalfarben der Waffe (Basis-Palette)
                for P in sight:
                    if P.get('glass'):continue
                    if ch.get(P['channel']):self.assertEqual(P['col'],ch[P['channel']],(P['label'],P['channel']))
                    elif P['emit'] and ch.get('MT_Accent'):self.assertEqual(P['col'],ch['MT_Accent'],P['label'])   # Waffe ohne Leuchtkanal
                    else:self.assertFalse(any(ch.get(c) for c in (P['channel'],)+vsmount.FALLBACK.get(P['channel'],())),P['label'])
    def test_counterproof(self):
        import spec_checks
        sp=load('KF03');self.assertEqual(spec_checks.vs_problems(sp),[])
        b=copy.deepcopy(sp);b['sight']['sight_spec']['socket_mount_m'][2]+=0.01;self.assertTrue(spec_checks.vs_problems(b))
        b=copy.deepcopy(sp);b['sight']['sight_spec']['id']='VS03';self.assertTrue(spec_checks.vs_problems(b))   # Röhre statt Holo (Typregel 0.15.2)
        b=copy.deepcopy(sp);b['sight']['sight_spec']['socket_reticle_m'][1]+=0.01;self.assertTrue(spec_checks.vs_problems(b))
        b=copy.deepcopy(sp);b['sight']['sight_spec']['line_clear_of_weapon']=False;self.assertTrue(spec_checks.vs_problems(b))
        b=copy.deepcopy(sp);b['sight']['sight_spec']['file']='VS04.spec.json';self.assertTrue(spec_checks.vs_problems(b))
        b=copy.deepcopy(sp);del b['sight']['sight_spec'];self.assertEqual(spec_checks.vs_problems(b),['kein Visier der Visier-Serie (VS02)'])

if __name__=='__main__':unittest.main()
