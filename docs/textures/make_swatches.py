#!/usr/bin/env python3
"""Erzeugt swatches/*.png (512 × 512) und swatches/manifest.json nur aus catalog.json.

Referenz, keine Pipeline-Logik: die Bilder zeigen, was die Parameter bedeuten; Claude und Codex lesen catalog.json, nicht die Bilder.
Abhängigkeiten: numpy, Pillow (Claudes Bild-venv: ~/Library/Caches/CubeEscape/concept-sheets-venv).
  python3 make_swatches.py            schreibt alle Musterbilder und das Manifest
  python3 make_swatches.py --sheet X  zusätzlich ein Kontaktbogen (JPEG) mit Beschriftung nach X
"""
import sys, os, json, hashlib, math, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 2   # Überabtastung, danach Mittelung


def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexs(rgb):
    return '#%02X%02X%02X' % tuple(int(round(max(0, min(1, v)) * 255)) for v in rgb)


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return hexs(tuple(A[i] * (1 - t) + B[i] * t for i in range(3)))


def lum(c, f):   # wie eng.lum
    r, g, b = hx(c); h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = l * f if f < 1 else l + (1 - l) * (f - 1) * 0.9
    return hexs(colorsys.hls_to_rgb(h, max(0, min(1, l)), s))


def rgb255(c):
    return np.array([round(v * 255) for v in hx(c)], np.float32)


def hsh(t):
    return np.sin(t * 12.9898) * 43758.5453 % 1.0


def ladder(fin, c):
    """fünf Farben: hell, mittel, schattig, dunkel, Glanzstreifen"""
    L = fin['ladder']
    if L['kind'] == 'levels':
        t = [lum(c, f) for f in L['levels']]
        return t + [t[L['highlight_level']]]
    t = [c if s['with'] is None else mix(c, s['with'], s['amount']) for s in L['steps']]
    h = L['highlight']
    return t + [h['fixed'] if 'fixed' in h else mix(c, h['with'], h['amount'])]


def finish_of(cat, fid):
    return next(f for f in cat['finishes'] if f['id'] == fid)


def level_map(cat, V):
    t = cat['swatch_setup']['lighting']['v_levels']
    return np.where(V < t[0], 0, np.where(V < t[1], 1, np.where(V < t[2], 2, 3))).astype(np.int8)


def streak_mask(cat, X, Y):
    s = cat['wear']['streak']
    d = s['direction']
    return ((X * d[0] + Y * d[1]) / s['period_rel_height']) % 1.0 < s['width_fraction']


def colorize(cat, CI, pal, L, X, Y):
    """CI: Palettenindex je Bildpunkt (−1 = leer), pal: [(Farbe, Oberfläche)], L: Stufe 0..3"""
    out = np.zeros(CI.shape + (3,), np.float32)
    sk = streak_mask(cat, X, Y)
    for j, (c, fid) in enumerate(pal):
        fin = finish_of(cat, fid)
        tn = np.stack([rgb255(x) for x in ladder(fin, c)])
        m = CI == j
        idx = L[m].astype(np.int16)
        if fin['streak']:
            idx = np.where(sk[m], 4, idx)
        out[m] = tn[idx]
    return out


def to_img(a):
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB')
    return im.resize((512, 512), Image.Resampling.BOX) if im.size[0] != 512 else im


def scale_bar(im, frac=0.25):
    d = ImageDraw.Draw(im); n = im.size[0]
    x0, y0, w = int(n * 0.06), int(n * 0.93), int(n * frac)
    d.rectangle([x0 - 2, y0 - 2, x0 + w + 2, y0 + 8], fill='#000000'); d.rectangle([x0, y0, x0 + w, y0 + 6], fill='#FFFFFF')


# ---------------------------------------------------------------- Materialien
def pattern_factor(pat, U, V):
    p = pat['params']; s = pat['size_mm']; pid = pat['id']
    if pid == 'gloss_gradient':
        f = 1.0
        for w in p['waves']:
            c = sum({'height': V, 'length': U, 'width': 0 * U}[a] for a in w['axes'])
            f = f + w['amplitude'] * np.cos(2 * np.pi * c / w['wavelength_mm'])
        return f
    if pid == 'brushed':
        f = sum(w['weight'] * np.sin(2 * np.pi * V / w['wavelength_mm'] + w['phase']) for w in p['waves'])
        return 1 + p['amplitude'] * f
    if pid == 'knurl':
        a, b = np.floor((U + V) / s), np.floor((U - V) / s)
        return 1 - p['darkening'] * (((a % 2) == 0) & ((b % 2) == 0))
    if pid == 'grain':
        c = p['hash_coefficients']
        return 1 + p['amplitude'] * (hsh(np.floor(U / s) * c[0] + np.floor(V / s) * c[1]) - 0.5)
    return np.ones_like(U)


def material_image(cat, m):
    n = 512 * SS; view = m['swatch_view_mm']
    j, i = np.mgrid[0:n, 0:n]
    U = (i + 0.5) / n * view; V = (n - 1 - j + 0.5) / n * view
    col = rgb255(m['swatch_color'])
    if m['id'] == 'energy_glass':
        r = np.hypot(i / n - 0.5, j / n - 0.5) / 0.7
        k = np.clip(r / 0.35, 0, 1); a = np.clip((r - 0.35) / 0.65, 0, 1)
        base = (rgb255('#FFFFFF')[None, None] * (1 - k[..., None]) + col * k[..., None])
        img = base * (1 - 0.55 * a[..., None])
    else:
        pat = next(p for p in cat['patterns'] if p['id'] == m['pattern'])
        img = col[None, None] * pattern_factor(pat, U, V)[..., None]
    im = to_img(img); scale_bar(im); return im


# ---------------------------------------------------------------- Oberflächen
def finish_image(cat, f):
    n = 512 * SS
    j, i = np.mgrid[0:n, 0:n]; X = (i + 0.5) / n; Y = (j + 0.5) / n
    L = level_map(cat, Y)
    CI = np.zeros((n, n), np.int16)
    out = colorize(cat, CI, [(f['swatch_color'], f['id'])], L, X * 1.6, Y)
    return to_img(out)


def wear_image(cat):
    n = 512 * SS; w = cat['wear']
    j, i = np.mgrid[0:n, 0:n]; X = (i + 0.5) / n; Y = (j + 0.5) / n
    out = np.zeros((n, n, 3), np.float32); out[:] = rgb255(cat['swatch_setup']['background'])
    paint = finish_of(cat, 'paint')
    bare = np.stack([rgb255(x) for x in ladder(paint, w['bare_metal'])])
    fill = np.stack([rgb255(x) for x in ladder(paint, '#3A4048')])
    for k, name in enumerate(('subtle', 'medium', 'strong')):
        x0, x1 = int(n * (0.04 + k * 0.32)), int(n * (0.04 + k * 0.32 + 0.28)); y0, y1 = int(n * 0.12), int(n * 0.88)
        L = level_map(cat, (j[y0:y1, x0:x1] - y0) / (y1 - y0))
        blk = fill[L]
        d = np.minimum.reduce([i[y0:y1, x0:x1] - x0, x1 - 1 - i[y0:y1, x0:x1], j[y0:y1, x0:x1] - y0, y1 - 1 - j[y0:y1, x0:x1]]).astype(np.float32)
        lv = w['levels'][name]; wpx = lv['width_rel'] * (y1 - y0) * 2.2; cell = wpx * w['cell_widths'] / 2.2
        nz = hsh(np.floor(i[y0:y1, x0:x1] / cell) * 0.37 + np.floor(j[y0:y1, x0:x1] / cell) * 1.91)
        wm = (d < wpx * (w['width_variation'][0] + (w['width_variation'][1] - w['width_variation'][0]) * nz)) & (nz > 1 - lv['coverage'])
        blk[wm] = bare[L[wm]]
        out[y0:y1, x0:x1] = blk
    return to_img(out)


# ---------------------------------------------------------------- Skins
class Mock:
    def __init__(self, cat, skin):
        S = cat['swatch_setup']; self.cat = cat; self.skin = skin; n = 512 * SS; self.n = n
        x0, y0, x1, y1 = [v * SS for v in S['mock']['rect_px']]; self.rect = (x0, y0, x1, y1)
        j, i = np.mgrid[0:n, 0:n]; self.i, self.j = i, j
        self.U = (i + 0.5 - x0) / (x1 - x0); self.V = (j + 0.5 - y0) / (y1 - y0); self.H = y1 - y0; self.W = x1 - x0
        inside = (self.U >= 0) & (self.U <= 1) & (self.V >= 0) & (self.V <= 1)
        bu = S['mock']['body_u_max']; bv = S['mock']['barrel_v']
        self.body = inside & (self.U <= bu)
        self.barrel = inside & (self.U > bu) & (self.V >= bv[0]) & (self.V <= bv[1])
        self.pal = []; self.CI = np.full((n, n), -1, np.int16)
        self.cols = {k: (v, 'paint') for k, v in S['palette'].items()}
        for k, v in skin['accents'].items():
            self.cols[k] = (v['color'], v['finish'])
        self.cols['base'] = self.cols[S['skin_base']]
        self.set(self.body, S['skin_base']); self.set(self.barrel, S['skin_barrel'])
        self.over = []   # Vektor-Overlays (Polygon, Farbe)

    def idx(self, c, fin):
        if (c, fin) not in self.pal:
            self.pal.append((c, fin))
        return self.pal.index((c, fin))

    def set(self, m, slot, fin=None):
        c, f = self.cols[slot] if slot in self.cols else (slot, 'paint')
        self.CI[m] = self.idx(c, fin or f)

    def px(self, u, v):
        x0, y0, _, _ = self.rect
        return (x0 + u * self.W, y0 + v * self.H)

    def poly(self, pts, slot):
        c, f = self.cols.get(slot, (slot, 'paint'))
        im = Image.new('L', (self.n, self.n), 0); ImageDraw.Draw(im).polygon([self.px(*p) for p in pts], fill=255)
        m = np.array(im) > 0
        self.CI[m & (self.body | self.barrel)] = self.idx(c, f)

    # ---- Ziffern, Runen, Embleme
    def glyph_polys(self, kind, val, ox, oy, sc):
        G = self.cat['glyphs']; sl = G['slant']; t = G['thickness']
        def sl_(x, y): return (ox + (x + (2 - y) * sl) * sc, oy + y * sc)
        out = []
        def bar(p, q):
            (x0, y0), (x1, y1) = p, q; L = math.hypot(x1 - x0, y1 - y0) or 1
            nx, ny = -(y1 - y0) / L * t / 2, (x1 - x0) / L * t / 2
            return [sl_(x0 + nx, y0 + ny), sl_(x1 + nx, y1 + ny), sl_(x1 - nx, y1 - ny), sl_(x0 - nx, y0 - ny)]
        if kind == 'digit':
            for s in G['digits'][val]:
                p, q = G['segments'][s]; out.append((bar(p, q), 0))
        elif kind == 'rune':
            for p, q in G['runes'][val]:
                out.append((bar(p, q), 0))
        return out

    def draw_glyph_row(self, items, height, at, slots):
        # Glyphen sind 2 Einheiten hoch; Zeilenmitte bei at
        sc = height * self.H / 2 / self.W   # in u-Einheiten je Zeicheneinheit
        total = 0; seq = []
        for kind, val in items:
            w = 2.0 if kind == 'emblem' else 1.0; seq.append((kind, val, total, w)); total += w + 0.45
        total -= 0.45
        ox = at[0] - total * sc / 2; oy = at[1] - sc * self.W / self.H   # v: Höhe 2·sc·W/H
        ratio = self.W / self.H
        for kind, val, off, w in seq:
            if kind == 'emblem':
                for pts, ci in self.emblem(val, ox + off * sc, oy, sc, ratio):
                    self.poly(pts, slots[min(ci, len(slots) - 1)])
            else:
                for pts, ci in self.glyph_polys(kind, val, 0, 0, 1):
                    P = [((ox + off * sc + x * sc), (oy + y * sc * ratio)) for x, y in pts]
                    self.poly(P, slots[0])

    def emblem(self, kind, ox, oy, sc, ratio):
        def T(pts): return [(ox + x * sc, oy + y * sc * ratio) for x, y in pts]
        if kind == 'cube':
            s = 0.866; c = (1, 1)
            return [(T([(1, 0), (1 + s, .5), c, (1 - s, .5)]), 0), (T([(1 - s, .5), c, (1, 2), (1 - s, 1.5)]), 1), (T([c, (1 + s, .5), (1 + s, 1.5), (1, 2)]), 2)]
        if kind in ('chevron', 'split_chevron'):
            return [(T([(o, 0), (o + .34, 0), (o + .9, 1), (o + .34, 2), (o, 2), (o + .56, 1)]), 0) for o in (0, .55, 1.1)]
        pts = [(1 + math.cos(a / 14 * math.pi), 1 + math.sin(a / 14 * math.pi)) for a in range(28)]
        return [(T(pts), 0)]

    def items(self, spec):
        seed = 7
        if spec == 'num': return [('digit', c) for c in '07']
        if spec == 'cube': return [('emblem', 'cube')]
        if spec == 'chevron+num': return [('emblem', 'chevron')] + [('digit', c) for c in '07']
        if spec.startswith('runes'):
            return [('rune', (seed * 7 + k * 5 + (k * k) % 3) % len(self.cat['glyphs']['runes'])) for k in range(int(spec[5:]))]
        return []

    # ---- Lagen
    def mask_eval(self, mk):
        U, V = self.U, self.V; k = mk['kind']
        def rng(a, lo, hi):
            m = np.ones(a.shape, bool)
            if lo is not None: m &= a > lo
            if hi is not None: m &= a < hi
            return m
        if k == 'diagonal': return rng(U + mk['k'] * V, mk['lo'], mk['hi'])
        if k == 'u': return rng(U, mk['lo'], mk['hi'])
        if k == 'v': return rng(V, mk['lo'], mk['hi'])
        if k == 'sawtooth': return rng(np.mod(U * mk['fu'] + V * mk['fv'], 1.0), mk['lo'], mk['hi'])
        if k == 'ellipse_rings':
            r = np.sqrt(((U - mk['center'][0]) * mk['scale'][0]) ** 2 + ((V - mk['center'][1]) * mk['scale'][1]) ** 2)
            m = np.zeros(U.shape, bool)
            for a, b in mk['ranges']: m |= (r > a) & (r < b)
            return m
        subs = [self.mask_eval(s) for s in mk['of']]
        return np.logical_and.reduce(subs) if k == 'all' else np.logical_or.reduce(subs)

    def apply(self):
        sk = self.skin; S = self.cat['swatch_setup']
        for L in sk['layers']:
            t = L['type']
            if t == 'region':
                m = self.mask_eval(L['mask']) & self.body; self.set(m, L['color'], L['finish'])
            elif t == 'blend':
                a = self.cols[S['skin_base'] if L['from'] == 'base' else L['from']][0]; b = self.cols[L['to']][0]
                w = L['strength'] * np.clip((self.U - L['lo']) / (L['hi'] - L['lo']), 0, 1)
                q = np.round(w / L['strength'] * 7).astype(int)
                for kk in range(8):
                    self.set(self.body & (q == kk), mix(a, b, L['strength'] * kk / 7) if kk else a)
            elif t == 'side_block':
                self.poly(L['poly'], L['slot'])
            elif t == 'finish':
                self.set(self.barrel if L['target'] == 'metal' else self.body, L['slot'])
            elif t == 'bands':
                self.bands(L)
            elif t == 'gradient':
                d = L['dir']; tt = (self.U * d[0] + self.V * d[1]); s = np.clip((tt - L['start']) / (L['end'] - L['start']), 0, 0.9999)
                st = (s * L['steps']).astype(int); a = self.cols[L['slots'][0]][0]; b = self.cols[L['slots'][1]][0]
                for kk in range(L['steps']):
                    self.set(self.body & (st == kk), mix(a, b, kk / max(1, L['steps'] - 1)))
            elif t == 'rings':
                r = np.hypot((self.U - L['center'][0]) * self.W, (self.V - L['center'][1]) * self.H) / self.H - L['r0']
                per = L['width'] + L['gap']; k = np.floor(r / per)
                inr = self.body & (r >= 0) & ((r - k * per) < L['width']) & (k < L['count'])
                for jx, sl in enumerate(L['slots']): self.set(inr & ((k % len(L['slots'])) == jx), sl)
            elif t == 'glyphs':
                if L.get('band'):
                    h = L['height'] * 1.6
                    self.poly([(0.04, L['at'][1] - h / 2), (0.96, L['at'][1] - h / 2), (0.96, L['at'][1] + h / 2), (0.04, L['at'][1] + h / 2)], L['band'])
                self.draw_glyph_row(self.items(L['items']), L['height'], L['at'], L['slots'])
            elif t == 'trim':
                self.trim(L['kind'], L['count'], L['slot'], L['at'])
            elif t == 'edge_wear':
                self.wear(L['width'], L['coverage'])
        dc = sk.get('decor')
        if dc:
            self.poly([(0.16, 0.50), (0.46, 0.50), (0.46, 0.74), (0.16, 0.74)], dc['badge']['color'])
            self.draw_glyph_row([('digit', c) for c in dc['number']], 0.15, (0.26, 0.60), ['SK_Accent2'])
            self.draw_glyph_row([('emblem', 'split_chevron')], 0.15, (0.39, 0.62), ['SK_Accent1'])
            self.trim(dc['trim']['kind'], dc['trim']['count'], 'SK_Accent1', (0.55, 0.30), fin=dc['trim']['finish'])

    def bands(self, L):
        d = L.get('dir')
        if 'along' in L:
            (u0, v0), (u1, v1) = L['along']
            du, dv = (u1 - u0) * self.W, (v1 - v0) * self.H; ln = math.hypot(du, dv)
            dist = np.abs((self.U - u0) * self.W * dv - (self.V - v0) * self.H * du) / ln
            m = self.body & (dist < L['width'] * self.H / 2 * 2); self.set(m, L['slots'][0]); return
        if d[0] == 0 and d[1] == 0:   # quer über die Breite: in der Seitenansicht nur als Randstreifen der Oberseite gezeigt
            for k in range(L['count']):
                u0 = L['at'] + k * (L.get('period') or L['width'])
                self.poly([(u0, 0), (u0 + L['width'] * 0.5, 0), (u0 + L['width'] * 0.5, 0.07), (u0, 0.07)], L['slots'][k % len(L['slots'])])
            return
        tt = self.U * d[0] + self.V * d[1]
        lo, hi = min(0, d[0]) + min(0, d[1]), max(0, d[0]) + max(0, d[1])
        tn = (tt - lo) / (hi - lo)
        per = L.get('period') or L['width']; k = np.floor((tn - L['at']) / per)
        inb = self.body & (tn >= L['at']) & (((tn - L['at']) - k * per) < L['width']) & (k < L['count'])
        if L.get('window'):
            w = L['window']; inb &= (self.U > w[0][0])
        for jx, sl in enumerate(L['slots']): self.set(inb & ((k % len(L['slots'])) == jx), sl)

    def trim(self, kind, count, slot, at, fin=None):
        c, f = self.cols[slot]; f = fin or f
        if kind == 'ribs' or kind == 'rib':
            u0 = at[0] if isinstance(at, (list, tuple)) else 0.3; v0 = at[1] if isinstance(at, (list, tuple)) else 0.3
            for k in range(count):
                u = u0 + k * 0.045
                self.poly_fin([(u, v0), (u + 0.02, v0), (u + 0.02, v0 + 0.2), (u, v0 + 0.2)], c, f)
        else:
            u0 = at if not isinstance(at, (list, tuple)) else at[0]
            for k in range(count):
                u = u0 - k * 0.05
                self.poly_fin([(u, 0.0), (u + 0.035, 0.0), (u + 0.035, -0.07), (u + 0.01, -0.07)], c, f)

    def poly_fin(self, pts, c, f):
        im = Image.new('L', (self.n, self.n), 0); ImageDraw.Draw(im).polygon([self.px(*p) for p in pts], fill=255)
        m = np.array(im) > 0
        self.CI[m] = self.idx(c, f)

    def wear(self, width, cov):
        w = self.cat['wear']
        d = np.minimum.reduce([self.U * self.W, (1 - self.U) * self.W, self.V * self.H, (1 - self.V) * self.H])
        wpx = width * self.H; cell = wpx * w['cell_widths']
        nz = hsh(np.floor(self.i / cell) * 0.37 + np.floor(self.j / cell) * 1.91)
        m = (self.body | self.barrel) & (d < wpx * (w['width_variation'][0] + 0.4 * nz) * 1.6) & (nz > 1 - cov)
        self.set(m, w['bare_metal'])

    def image(self):
        L = level_map(self.cat, np.clip(self.V, 0, 1))
        X = self.U * 1.6; Y = self.V
        out = np.zeros((self.n, self.n, 3), np.float32); out[:] = rgb255(self.cat['swatch_setup']['background'])
        sh = colorize(self.cat, self.CI, self.pal, L, X, Y)
        m = self.CI >= 0
        out[m] = sh[m]
        return to_img(out)


def skin_image(cat, sk):
    mk = Mock(cat, sk); mk.apply(); return mk.image()


# ---------------------------------------------------------------- Lauf
def build(cat):
    """liefert {Dateiname: PIL-Bild}"""
    out = {}
    for m in cat['materials']:
        if m.get('swatch'): out[os.path.basename(m['swatch'])] = material_image(cat, m)
    for f in cat['finishes']: out[os.path.basename(f['swatch'])] = finish_image(cat, f)
    out[os.path.basename(cat['wear']['swatch'])] = wear_image(cat)
    for sk in cat['skins']: out[os.path.basename(sk['swatch'])] = skin_image(cat, sk)
    return out


def save_png(im, path):
    im.save(path, format='PNG', optimize=False, compress_level=6)


def sha_file(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def sha_pixels(im):
    return hashlib.sha256(np.asarray(im.convert('RGB')).tobytes()).hexdigest()


def catalog_sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    cpath = os.path.join(HERE, 'catalog.json')
    cat = json.load(open(cpath, encoding='utf-8'))
    imgs = build(cat)
    d = os.path.join(HERE, 'swatches'); os.makedirs(d, exist_ok=True)
    man = {'catalog_sha256': catalog_sha(cpath), 'size': 512, 'files': {}}
    for name in sorted(imgs):
        p = os.path.join(d, name); save_png(imgs[name], p)
        man['files'][name] = {'sha256': sha_file(p), 'pixels_sha256': sha_pixels(imgs[name])}
    json.dump(man, open(os.path.join(d, 'manifest.json'), 'w'), indent=1)
    print(f'{len(imgs)} Musterbilder in {d}')
    if '--sheet' in sys.argv:
        out = sys.argv[sys.argv.index('--sheet') + 1]
        names = sorted(imgs); cols = 6; cell = 256; rows = math.ceil(len(names) / cols)
        sheet = Image.new('RGB', (cols * cell, rows * (cell + 16)), '#0A0C10'); dr = ImageDraw.Draw(sheet); ft = ImageFont.load_default()
        for k, nm in enumerate(names):
            x, y = (k % cols) * cell, (k // cols) * (cell + 16)
            sheet.paste(imgs[nm].resize((cell, cell), Image.Resampling.LANCZOS), (x, y + 16)); dr.text((x + 4, y + 2), nm[:-4], fill='#C7D1DC', font=ft)
        sheet.save(out, quality=88); print('Kontaktbogen', out)


if __name__ == '__main__':
    main()
