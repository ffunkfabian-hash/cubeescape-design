# Variante F: Visier separat – Markieren, 2D-Board mit separat gezeichnetem Visier, Hilfen
import re

def clip(poly, keep):
    """Sutherland-Hodgman: keep(p)->float >=0 innen. Halbebene linear."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        fa, fb = keep(a), keep(b)
        if fa >= 0: out.append(a)
        if (fa >= 0) != (fb >= 0):
            t = fa / (fa - fb)
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    # Duplikate entfernen
    res = []
    for p in out:
        if not res or abs(p[0] - res[-1][0]) > 1e-6 or abs(p[1] - res[-1][1]) > 1e-6: res.append(p)
    if len(res) > 1 and abs(res[0][0] - res[-1][0]) < 1e-6 and abs(res[0][1] - res[-1][1]) < 1e-6: res.pop()
    return res

def xmin(x): return lambda p: p[0] - x
def xmax(x): return lambda p: x - p[0]
def ymin(y): return lambda p: p[1] - y
def ymax(y): return lambda p: y - p[1]

def clipall(poly, *fs):
    for f in fs: poly = clip(poly, f)
    return poly

def flag_parts(m, flags):
    """flags: Liste bool je Teil (gleiche Reihenfolge wie m.parts)"""
    assert len(m.parts) == len(flags), (len(m.parts), len(flags))
    for P, f in zip(m.parts, flags):
        if f: P['sight'] = True
    return m

def inject(html, clusters, rail=None, to_vb=lambda p: p, scale_sight=1.0, grow=1.22):
    """Erweitert das Haupt-SVG des 2D-Boards um ein oberes Band und zeichnet das Visier dort separat.
    sight_svg: SVG-Fragment in Modellkoordinaten, sb=(x0,y0,x1,y1) seiner Box,
    rail: Punkt (Modellkoordinaten) der Visieraufnahme auf der Waffe, to_vb: Modell->viewBox-Transform."""
    m = re.search(r'<svg viewBox="([-\d. ]+)"', html)
    x, y, W, H = map(float, m.group(1).split())
    nW, nH = W * grow, H * grow
    nx, ny = x - (nW - W) / 2, y - (nH - H) + 0.02 * H
    nH = nH + 0.02 * H
    band = (nH - H)  # Höhe des oberen Bands
    bx0, by0 = nx + 0.52 * nW, ny + 0.04 * band
    bw, bh = 0.45 * nW, band * 0.88
    fs = H * 0.032
    # Cluster (z. B. Kimme und Korn) nebeneinander anordnen, gemeinsamer Massstab
    gap = 24.0
    tw = sum(b[2] - b[0] for _, b in clusters) + gap * (len(clusters) - 1)
    th = max(b[3] - b[1] for _, b in clusters)
    sc = min((bw - 2 * fs) / tw, (bh - 3.2 * fs) / th, 3.0) * scale_sight
    cx0 = bx0 + bw / 2 - tw * sc / 2
    cyc = by0 + 2.2 * fs + (bh - 2.6 * fs) / 2
    placed = []
    for frag, b in clusters:
        tx = cx0 - b[0] * sc
        ty = cyc - (b[1] + b[3]) / 2 * sc
        placed.append(f'<g transform="translate({tx:.2f},{ty:.2f}) scale({sc:.4f})">{frag}</g>')
        cx0 += (b[2] - b[0] + gap) * sc
    g = [f'<rect x="{nx:.1f}" y="{ny:.1f}" width="{nW:.1f}" height="{nH:.1f}" fill="#111A27"/>',
         f'<rect x="{nx:.1f}" y="{ny:.1f}" width="{nW:.1f}" height="{nH:.1f}" fill="url(#GRIDID)"/>']
    over = [f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{fs*0.6:.1f}" fill="#0E1622" stroke="#4A6080" stroke-width="{fs*0.08:.2f}" stroke-dasharray="{fs*0.4:.1f} {fs*0.3:.1f}"/>',
            f'<text x="{bx0+fs*0.7:.1f}" y="{by0+fs*1.5:.1f}" font-family="Chakra Petch, sans-serif" font-size="{fs:.1f}" font-weight="600" letter-spacing="{fs*0.12:.1f}" fill="#E6ECF2">VISIER · SEPARAT</text>',
            f'<text x="{bx0+bw-fs*0.7:.1f}" y="{by0+fs*1.5:.1f}" text-anchor="end" font-family="Barlow, sans-serif" font-size="{fs*0.75:.1f}" fill="#8FA0B3">modular · auf Visierschiene</text>',
            ]+placed
    if rail is not None:
        rx, ry = to_vb(rail)
        sx, sy = bx0 + bw * 0.12, by0 + bh
        over.append(f'<path d="M{sx:.1f},{sy:.1f} L{sx:.1f},{(sy+ry)/2:.1f} L{rx:.1f},{(sy+ry)/2:.1f} L{rx:.1f},{ry-fs*0.3:.1f}" fill="none" stroke="#8FA0B3" stroke-width="{fs*0.07:.2f}" stroke-dasharray="{fs*0.3:.1f} {fs*0.25:.1f}"/>')
        over.append(f'<circle cx="{rx:.1f}" cy="{ry-fs*0.3:.1f}" r="{fs*0.18:.1f}" fill="#8FA0B3"/>')
    gid = re.search(r'<pattern id="(\w+Grid)"', html).group(1)
    g[1] = g[1].replace('GRIDID', gid)
    html = html[:m.start(1)] + f'{nx:.1f} {ny:.1f} {nW:.1f} {nH:.1f}' + html[m.end(1):]
    # Hintergrund direkt nach </defs>, Visierfeld vor </svg> des Hauptbilds
    i = html.index('</defs>', m.start()) + len('</defs>')
    html = html[:i] + '\n' + '\n'.join(g) + html[i:]
    j = html.index('</svg>', i)
    html = html[:j] + '\n'.join(over) + '\n' + html[j:]
    return html

def Sg(s):
    """flib-Spec-Eintrag als Visierteil markieren"""
    s['S'] = True
    return s

def clusters_of(items, bbox_fn, svg_fn, gapx=40):
    """Visierteile nach x-Abstand gruppieren -> [(svg, bbox)]"""
    its = sorted(items, key=lambda it: bbox_fn([it])[0])
    groups = []
    for it in its:
        b = bbox_fn([it])
        if groups and b[0] <= bbox_fn(groups[-1])[2] + gapx: groups[-1].append(it)
        else: groups.append([it])
    return [(svg_fn(g), bbox_fn(g)) for g in groups]
