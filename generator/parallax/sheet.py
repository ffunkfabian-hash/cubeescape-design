"""Self-contained, fixed-size editorial concept sheets from one shared model.

The six reference views deliberately share a world center and pixels/unit scale.
The trigger detail renders the complete weapon before the viewport clips it, so
parts in front of the selected region still take part in depth testing.
"""
from __future__ import annotations

import base64
import hashlib
import html
import io
from pathlib import Path
import textwrap

import numpy as np
from PIL import Image, ImageDraw

from eng import bounds
from raster import render, rotation_matrix


WIDTH, HEIGHT = 4800, 3400
INK = "#E5E9ED"
MUTED = "#91A3B7"
ACCENT = "#F28C28"
PRIORITY = ("Gehäuse", "Griff", "Abzug", "Magazin", "Lauf", "Mündung", "Schaft", "Visierschiene")
VIEWS = (
    ("LINKS", 0, 0, (2130, 280), (2480, 590)),
    ("RECHTS", 180, 0, (2130, 280), (2480, 915)),
    ("OBEN", 0, 90, (2130, 180), (2480, 1240)),
    ("UNTEN", 0, -90, (2130, 180), (2480, 1465)),
    ("VORNE", -90, 0, (1000, 300), (2480, 1710)),
    ("HINTEN", 90, 0, (1000, 300), (3610, 1710)),
)
PALETTES = (
    ("BASIS", None),
    ("CUBE ESCAPE STANDARD", ("#ECE6DA", "#A3A7AD", "#2B2E33", "#F28C28")),
    ("ARKTIS", ("#F3F6F9", "#AEBBCA", "#3A4452", "#22D3EE")),
    ("NACHT", ("#4A4E57", "#2C2F35", "#141518", "#FF5A36")),
)


def _e(value):
    return html.escape(str(value), quote=True)


def _vertices(model):
    return np.concatenate([np.asarray(face.vertices, dtype=float) for part in model for face in part.faces], axis=0)


def _project(points, yaw, pitch):
    return np.asarray(points) @ rotation_matrix(yaw, pitch).T


def _uri(image):
    data = io.BytesIO()
    image.save(data, "WEBP", lossless=True, method=4)
    return "data:image/webp;base64," + base64.b64encode(data.getvalue()).decode("ascii")


def _image(image, x, y, width=None, height=None):
    width = image.width if width is None else width
    height = image.height if height is None else height
    return f'<image x="{x}" y="{y}" width="{width}" height="{height}" href="{_uri(image)}"/>'


def _text(x, y, value, size=32, color=INK, family="body", weight="normal", anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" class="{family}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{_e(value)}</text>'


def _wrapped(x, y, value, width=74, size=29, leading=40, color=MUTED, max_lines=None):
    lines = textwrap.wrap(str(value), width=width, break_long_words=False, break_on_hyphens=False)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,") + " …"
    return "".join(_text(x, y + i * leading, line, size, color) for i, line in enumerate(lines))


def _panel(x, y, width, height, number, title, subtitle=""):
    result = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" fill="#111E2D" stroke="#26384C" stroke-width="2"/>'
    result += _text(x + 34, y + 57, number, 27, ACCENT, "mono")
    result += _text(x + 98, y + 57, title, 34, INK, "title")
    if subtitle:
        result += _text(x + width - 34, y + 57, subtitle, 23, MUTED, "mono", anchor="end")
    return result


def _font_css():
    result = []
    for family, name in (("Chakra", "ChakraPetch-Regular"), ("Barlow", "Barlow-Regular"), ("JetBrains", "JetBrainsMono-Regular")):
        for suffix, mime, fmt in ((".ttf", "font/ttf", "truetype"), (".woff2", "font/woff2", "woff2")):
            path = Path(__file__).parent / "fonts" / (name + suffix)
            if path.exists():
                encoded = base64.b64encode(path.read_bytes()).decode("ascii")
                result.append(f"@font-face{{font-family:'{family}';src:url(data:{mime};base64,{encoded}) format('{fmt}');font-weight:100 900;}}")
                break
    result.append(".title{font-family:Chakra,Arial,sans-serif}.body{font-family:Barlow,Arial,sans-serif}.mono{font-family:JetBrains,monospace}")
    return "".join(result)


def _swatch(kind, color, size=(160, 78)):
    """Object-independent close-up samples of the five renderer materials."""
    rng = np.random.default_rng(801 + kind)
    w, h = size
    yy, xx = np.mgrid[:h, :w]
    rgb = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], dtype=float)
    noise = rng.normal(0, 1, (h, w))
    if kind == 0:
        shade = 0.88 + 0.13 * (1 - yy / h) + noise * 0.006
    elif kind == 1:
        shade = 0.80 + 0.18 * (1 - yy / h) + rng.normal(0, 0.045, (h, 1)) + noise * 0.012
    elif kind == 2:
        diamond = np.minimum((xx + yy) % 16, (-xx + yy) % 16)
        shade = 0.76 + (diamond < 2) * 0.23 + noise * 0.025
    elif kind == 3:
        shade = 0.88 + noise * 0.05
    else:
        shade = 0.79 + 0.20 * np.sin(np.pi * yy / h) + noise * 0.004
    pixels = np.uint8(np.clip(rgb[None, None, :] * shade[:, :, None], 0, 255))
    image = Image.fromarray(pixels, "RGB").convert("RGBA")
    draw = ImageDraw.Draw(image)
    draw.line((0, 0, w - 1, 0), fill=(255, 255, 255, 90), width=2)
    return image


def _prompts(meta, model):
    components = list(dict.fromkeys(str(p.label) for p in model if getattr(p, "label", "")))
    name = meta.get("name", meta.get("kind", "Waffenkonzept"))
    form = str(meta.get("form", "abgeschrägte, modulare Hard-Surface-Geometrie"))
    palette = ", ".join(meta.get("palette", ("#D5CCB8", "#858F99", "#303844", "#F28C28")))
    de = (f"Cube Escape: {name}. Form: {form}. Bauteile: {', '.join(components)}. "
          f"Palette: {palette}. Low-Poly, modulare Hard-Surface-Konstruktion; lackiertes und gebürstetes Metall, "
          "Gummi, matter Kunststoff, sparsame funktionale Leuchtelemente. Ein einziges konsistentes 3D-Modell: "
          "Isometrie ohne Optik; sechs orthografische Ansichten im gleichen Maßstab; Optik separat mit Halterung; "
          "Abzugsdetail. Klare Verbindungen und sichtbarer Abzug mit Bügel. Keine schwebenden Teile, "
          "keine ungewollten Durchdringungen, kein Bloom, keine Perspektivverzerrung.")
    en = (f"Cube Escape {name}; {form}. Palette {palette}. Futuristic industrial low-poly hard-surface concept sheet. "
          "One consistent 3D model: stock, receiver, grip, trigger with guard, seated magazine or energy cell, "
          "visible barrel, muzzle and rail. Isometric without optic; six orthographic views at one shared scale; "
          "detached modular optic with mounts, trigger detail. Painted and brushed metal, rubber grip, matte "
          "polymer, restrained emissive accents. Clear physical connections and silhouette. No floating parts, "
          "unintended intersections, bloom, blur, perspective distortion or changing geometry.")
    return {"de": de, "en": en}


def build_sheet(meta, model, output: Path, number: int) -> dict:
    """Write one portable SVG-backed HTML sheet and return verifiable metadata."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    slug = str(meta["slug"])
    if not slug or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in slug):
        raise ValueError("Sheet slug must contain lowercase ASCII letters, digits, '_' or '-'")
    weapon = [p for p in model if not getattr(p, "sight", False)]
    optics = [p for p in model if getattr(p, "sight", False)]
    if not weapon:
        raise ValueError("A sheet needs weapon geometry")
    lo, hi = bounds(weapon)
    lo, hi = np.asarray(lo), np.asarray(hi)
    center = (lo + hi) / 2
    vertices = _vertices(weapon)
    views = VIEWS
    if (hi - lo)[1] > (hi - lo)[0]:
        # Tall silhouettes use four upright cells instead of short wide strips.
        views = (
            ("LINKS", 0, 0, (1000, 500), (2480, 590)),
            ("RECHTS", 180, 0, (1000, 500), (3610, 590)),
            ("VORNE", -90, 0, (1000, 500), (2480, 1180)),
            ("HINTEN", 90, 0, (1000, 500), (3610, 1180)),
            ("OBEN", 0, 90, (2130, 100), (2480, 1790)),
            ("UNTEN", 0, -90, (2130, 100), (2480, 1950)),
        )
    # Center is fixed even for asymmetric silhouettes. Symmetric projected
    # extents keep every view inside its own viewport at the shared scale.
    scales = []
    for _, yaw, pitch, (w, h), _ in views:
        projected = _project(vertices - center, yaw, pitch)
        extent = np.maximum(np.abs(projected[:, :2]).max(axis=0) * 2, 1)
        scales.append(min((w - 100) / extent[0], (h - 50) / extent[1]))
    common_scale = float(min(scales))
    palette = list(meta.get("palette", ("#D5CCB8", "#858F99", "#303844", "#F28C28")))
    while len(palette) < 4:
        palette.append("#858F99")
    prompts = _prompts(meta, model)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{_e(meta.get("name", slug))} – Konzeptblatt">']
    parts.append('<defs><pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#152334" stroke-width="1"/></pattern></defs>')
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0E1622"/><rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>')
    parts.append(_text(140, 233, f"{number:02d}", 168, ACCENT, "title"))
    parts.append(_text(395, 128, "CUBE ESCAPE  /  DESIGN ARCHIVE", 28, MUTED, "mono"))
    parts.append(_text(395, 197, f"WAFFE · VARIANTE A / {meta.get('kind', '').upper()}", 42, INK, "title"))
    name = str(meta.get("name", slug))
    parts.append(_text(395, 296, name.upper(), min(88, 1410 / max(len(name), 1) * 1.65), INK, "title"))
    parts.append(_text(145, 367, "FORM", 27, ACCENT, "mono"))
    parts.append(_wrapped(265, 367, meta.get("form", "Modulare Hard-Surface-Konstruktion"), width=105, size=29, leading=36, max_lines=1))
    parts.append(_text(4595, 115, "KONSTRUKTION VOR OPTIK", 27, MUTED, "mono", anchor="end"))
    for i, color in enumerate(palette[:4]):
        x = 3735 + i * 215
        parts.append(f'<rect x="{x}" y="172" width="180" height="64" rx="6" fill="{_e(color)}"/>')
        parts.append(_text(x, 274, str(color).upper(), 23, MUTED, "mono"))
    parts.append('<rect x="3735" y="308" width="825" height="58" rx="29" fill="#223247"/>')
    parts.append(_text(4148, 347, meta.get("palette_name", "KERAMIK / GRAPHIT / SIGNALORANGE"), 25, INK, "mono", anchor="middle"))

    parts.append(_panel(140, 430, 2200, 1250, "01", "ISOMETRIE", "−45° / +35.264° · OHNE OPTIK"))
    hero = render(weapon, yaw=-45, pitch=35.264, size=(2130, 900))
    hero_x, hero_y = 175, 620
    parts.append(_image(hero.image, hero_x, hero_y))
    anchors = getattr(hero, "anchors", {})
    chosen = [(key, anchors[key]) for key in PRIORITY if key in anchors][:8]
    by_height = sorted(chosen, key=lambda item: item[1][1])
    split = (len(by_height) + 1) // 2
    label_records = []
    for lane, values in (("top", by_height[:split]), ("bottom", by_height[split:])):
        values = sorted(values, key=lambda item: item[1][0])
        for index, (label, anchor) in enumerate(values):
            label_x = 255 + (index + 0.5) * 1960 / max(len(values), 1)
            label_y = 566 if lane == "top" else 1597
            ax, ay = float(anchor[0]) + hero_x, float(anchor[1]) + hero_y
            elbow_y = 596 if lane == "top" else 1540
            end_y = label_y + 13 if lane == "top" else label_y - 35
            parts.append(f'<path d="M{ax:.2f},{ay:.2f} L{ax:.2f},{elbow_y} L{label_x:.2f},{end_y}" stroke="#7D94A9" stroke-width="2.2" fill="none"/>')
            parts.append(f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r="5" fill="{ACCENT}"/>')
            parts.append(_text(label_x, label_y, label.upper(), 27, INK, "mono", anchor="middle"))
            label_records.append({"label": label, "anchor": [ax, ay], "position": [label_x, label_y], "lane": lane})
    all_labels = list(dict.fromkeys(str(p.label) for p in weapon if getattr(p, "label", "")))
    others = [label for label in all_labels if label not in {item[0] for item in chosen}]
    parts.append(_wrapped(180, 1640, "Weitere Bauteile: " + (" · ".join(others) if others else "Alle Hauptbauteile beschriftet"), width=170, size=20, leading=24, max_lines=2))

    parts.append(_panel(2410, 430, 2250, 1660, "02", "ORTHOGRAFISCHE REFERENZEN", "GEMEINSAMER MASSSTAB"))
    parts.append(_text(2450, 543, "Mündung +X  ·  Y nach unten  ·  Z+ links  /  Bezug: Bounding-Box-Mitte", 23, MUTED, "mono"))
    view_records = []
    for name, yaw, pitch, size, position in views:
        x, y = position
        w, h = size
        parts.append(_text(x, y - 11, name, 24, INK, "mono"))
        parts.append(f'<path d="M{x},{y + h / 2}H{x + w} M{x + w / 2},{y}V{y + h}" stroke="#36506B" stroke-width="1.5" stroke-dasharray="12 10"/>')
        result = render(weapon, yaw=yaw, pitch=pitch, size=size, scale=common_scale, center=center)
        parts.append(_image(result.image, x, y))
        view_records.append({"name": name.lower(), "yaw": yaw, "pitch": pitch, "scale": common_scale, "center": center.tolist(), "viewport": [x, y, w, h]})

    parts.append(_panel(140, 1720, 1080, 600, "03", "ABZUGSBEREICH", "−28° / −22°"))
    selected = [p for p in weapon if getattr(p, "label", "") in ("Abzug", "Griff", "Magazin", "Bügel", "Abzugsbügel")]
    if not selected:
        selected = weapon
    detail_lo, detail_hi = bounds(selected)
    detail_center = (np.asarray(detail_lo) + np.asarray(detail_hi)) / 2
    selected_projected = _project(_vertices(selected) - detail_center, -28, -22)
    detail_extent = np.maximum(np.abs(selected_projected[:, :2]).max(axis=0) * 2, 1)
    detail_scale = float(min(870 / detail_extent[0], 350 / detail_extent[1]))
    detail = render(weapon, yaw=-28, pitch=-22, size=(1010, 425), scale=detail_scale, center=detail_center)
    parts.append(_image(detail.image, 175, 1810))
    parts.append(_text(180, 2284, "Griff · Abzug mit Bügel · Magazinschacht", 25, MUTED))

    parts.append(_panel(1260, 1720, 1080, 600, "04", "VISIER · SEPARAT", "MODULAR AUF SCHIENE"))
    if optics:
        optic_iso = render(optics, yaw=-45, pitch=35.264, size=(610, 360))
        optic_side = render(optics, yaw=0, pitch=0, size=(420, 280))
        parts.append(_image(optic_iso.image, 1285, 1850))
        parts.append(_image(optic_side.image, 1895, 1880))
        parts.append(_text(1575, 2250, "ISOMETRIE", 23, MUTED, "mono", anchor="middle"))
        parts.append(_text(2105, 2250, "SEITE", 23, MUTED, "mono", anchor="middle"))
    else:
        parts.append(_wrapped(1320, 1940, "Keine separate Optik im Modell. Die modulare Schiene bleibt an der Waffe.", width=44, size=34))

    parts.append(_panel(140, 2360, 2200, 800, "05", "MATERIAL & TEXTUREN", "OBJEKTRAUM · TOON"))
    textured = render(weapon, yaw=-45, pitch=35.264, size=(1340, 585), textured=True)
    parts.append(_image(textured.image, 170, 2470))
    materials = (("Lackiertes Metall", "Gehäuse / Schaft", palette[0]), ("Gebürstetes Metall", "Lauf / Verbindung", palette[1]), ("Gummierter Griff", "Griff / Kontaktfläche", palette[2]), ("Matter Kunststoff", "Magazin / Schutzteile", palette[2]), ("Beleuchtetes Element", "Funktion / Status", palette[3]))
    for i, (name, use, color) in enumerate(materials):
        y = 2475 + i * 119
        parts.append(_image(_swatch(i, color), 1535, y))
        parts.append(_text(1720, y + 29, name, 28, INK))
        parts.append(_text(1720, y + 65, use, 22, MUTED))
    parts.append(_text(180, 3123, "Flache Schattierung · kontrollierte Leuchtflächen · keine Form verschleiernden Effekte", 24, MUTED))

    parts.append(_panel(2410, 2130, 2250, 580, "06", "FARBVARIANTEN", "IDENTISCHE GEOMETRIE"))
    for i, (name, colors) in enumerate(PALETTES):
        x = 2450 + (i % 2) * 1100
        y = 2230 + (i // 2) * 236
        actual = palette[:4] if colors is None else colors
        roles = dict(zip(("primary", "medium", "dark", "accent"), actual))
        result = render(weapon, yaw=-45, pitch=35.264, size=(1035, 178), palette=roles)
        parts.append(_image(result.image, x, y + 26))
        parts.append(_text(x + 10, y + 15, name, 24, INK, "mono"))
        for j, color in enumerate(actual):
            parts.append(f'<rect x="{x + 810 + j * 49}" y="{y - 6}" width="34" height="21" rx="3" fill="{_e(color)}"/>')

    parts.append(_panel(2410, 2750, 2250, 410, "07", "GENERIERTE REFERENZPROMPTS", "DE / EN"))
    parts.append(_text(2450, 2852, "DEUTSCH", 22, ACCENT, "mono"))
    parts.append(_text(3550, 2852, "ENGLISH", 22, ACCENT, "mono"))
    parts.append('<path d="M3510 2840V3120" stroke="#2B4056" stroke-width="2"/>')
    # Short visible excerpts keep the sheet readable; complete prompts are
    # embedded as accessible metadata and returned for plain-text export.
    preview_de = (f"{meta.get('name', slug)} · {meta.get('form', '')}. Palette {', '.join(palette[:4])}. "
                  "Low-Poly, modulare Konstruktion; lackiertes / gebürstetes Metall, Gummi, matter Kunststoff. "
                  "Gehäuse, Schaft, Griff, Abzug mit Bügel, Magazin, Lauf und Schiene klar verbunden. "
                  "Ein Modell, sechs Orthos mit gleichem Maßstab, Isometrie ohne Optik; Optik separat. "
                  "Keine schwebenden Teile, Durchdringungen, Unschärfe oder Bloom.")
    preview_en = (f"Cube Escape {meta.get('name', slug)}. Futuristic industrial low-poly hard-surface design. "
                  f"Palette {', '.join(palette[:4])}. Painted / brushed metal, rubber, matte polymer, restrained emissive accents. "
                  "One model: six orthographic views at shared scale, isometric without optic, detached modular optic. "
                  "Clear stock, grip, trigger guard, seated magazine, visible barrel and rail. "
                  "No floating parts, intersections, blur, bloom or perspective distortion.")
    parts.append(_wrapped(2450, 2894, preview_de, width=70, size=26, leading=33, max_lines=8))
    parts.append(_wrapped(3550, 2894, preview_en, width=70, size=26, leading=33, max_lines=8))
    parts.append('<path d="M140 3240H4660" stroke="#34475B" stroke-width="2"/>')
    parts.append(_text(140, 3300, "Alle Ansichten aus demselben 3D-Modell, orthografisch, gleicher Maßstab. Gestalterische Referenz, keine Fertigungszeichnung.", 28, MUTED))
    parts.append(_text(4660, 3350, f"CE / {number:02d} / {slug.upper()} / A", 23, MUTED, "mono", anchor="end"))
    parts.append("</svg>")
    digest = hashlib.sha256()
    for part in model:
        for face in part.faces:
            digest.update(np.asarray(face.vertices, dtype="<f8").tobytes())
        digest.update(str(getattr(part, "label", "")).encode("utf8"))
    import json
    prompt_json = json.dumps(prompts, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    filename = slug + ".html"
    document = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width={WIDTH}, initial-scale=1"><title>{_e(meta.get("name", slug))} · Cube Escape</title>'
                '<style>' + _font_css() + f'html,body{{margin:0;width:{WIDTH}px;height:{HEIGHT}px;background:#0E1622;overflow:hidden}}svg{{display:block}}'
                '</style></head><body>' + "".join(parts) + '<script type="application/json" id="reference-prompts">' + prompt_json + '</script></body></html>')
    (output / filename).write_text(document, encoding="utf8")
    return {"filename": filename, "slug": slug, "number": number, "width": WIDTH, "height": HEIGHT,
            "variant": "A", "geometry_sha256": digest.hexdigest(), "weapon_parts": len(weapon),
            "optic_parts": len(optics), "orthographic_scale": common_scale,
            "orthographic_center": center.tolist(), "orthographic_views": view_records,
            "hero_labels": label_records, "other_components": others, "prompts": prompts,
            "detail": {"yaw": -28, "pitch": -22, "scale": detail_scale, "center": detail_center.tolist(),
                       "full_weapon_rendered": True, "selected_labels": list(dict.fromkeys(getattr(p, "label", "") for p in selected))},
            "palette_variants": [{"name": name, "colors": list(palette[:4] if colors is None else colors)} for name, colors in PALETTES]}
