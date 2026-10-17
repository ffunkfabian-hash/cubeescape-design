"""Portable 4800×4432 design plates built from one consistent weapon model.

Only the six orthographic cells share a camera scale. Their center and scale
are explicit in the returned record; close-ups intentionally crop the complete
base model, keeping depth occlusion intact. Skins add their geometry exactly once.
"""
from __future__ import annotations

import base64
import hashlib
import html
import io
import json
from pathlib import Path
import textwrap
import shutil

import numpy as np

from eng import bounds
from raster import render as _raster_render, rotation_matrix

WIDTH, HEIGHT = 4800, 4432
INK, MUTED, ACCENT = "#E5E9ED", "#91A3B7", "#F28C28"
PRIORITY = ("Gehäuse", "Griff", "Abzug", "Magazin", "Lauf", "Mündung", "Schaft", "Visierschiene")
PALETTES = (
    ("BASIS", None),
    ("CUBE ESCAPE", ("#ECE6DA", "#A3A7AD", "#2B2E33", "#F28C28")),
    ("ARKTIS", ("#F3F6F9", "#AEBBCA", "#3A4452", "#22D3EE")),
    ("NACHT", ("#4A4E57", "#2C2F35", "#141518", "#FF5A36")),
)
MATERIALS = (
    ("paint", "Lackiertes Metall", "MT_Primary / MT_Secondary"),
    ("metal", "Gebürstetes Metall", "MT_Metal"),
    ("rubber", "Gummierte Kontaktfläche", "MT_Detail"),
    ("plastic", "Matter Kunststoff", "MT_Detail"),
    ("light", "Funktionslicht", "MT_Energy / MT_Emission"),
)


def _e(value):
    return html.escape(str(value), quote=True)


def _vertices(model):
    return np.concatenate([np.asarray(f.vertices, dtype=float) for p in model for f in p.faces])


def _project(points, yaw, pitch):
    return np.asarray(points) @ rotation_matrix(yaw, pitch).T


def render(model, yaw=-45, pitch=35.264, size=(1000,600), scale=None, center=None, **kwargs):
    # Display panels may recenter in camera space; explicit orthographic frames
    # and construction close-ups retain their exact shared world reference.
    if scale is None and center is None:
        vertices=_vertices(model)
        rotation=rotation_matrix(yaw,pitch)
        projected=vertices @ rotation.T
        low=projected.min(axis=0);high=projected.max(axis=0)
        center=((low+high)/2) @ rotation
        span=np.maximum(high-low,1e-6)
        scale=min(size[0]*.88/span[0],size[1]*.88/span[1])
    return _raster_render(model,yaw=yaw,pitch=pitch,size=size,scale=scale,center=center,**kwargs)


def _uri(image):
    data = io.BytesIO()
    image.save(data, "WEBP", quality=60, method=4)
    return "data:image/webp;base64," + base64.b64encode(data.getvalue()).decode("ascii")


def _image(image, x, y, width=None, height=None):
    w = image.width if width is None else width
    h = image.height if height is None else height
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{_uri(image)}"/>'


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
    result += _text(x + 30, y + 56, number, 26, ACCENT, "mono")
    result += _text(x + 91, y + 56, title, 33, INK, "title")
    if subtitle:
        result += _text(x + width - 30, y + 98, subtitle, 22, MUTED, "mono", anchor="end")
    return result


def _font_css():
    result = []
    for family, name in (("Chakra", "ChakraPetch-Regular"), ("Barlow", "Barlow-Regular"), ("JetBrains", "JetBrainsMono-Regular")):
        for suffix, mime, fmt in ((".ttf", "font/ttf", "truetype"), (".woff2", "font/woff2", "woff2")):
            path = Path(__file__).parent / "fonts" / (name + suffix)
            if path.exists():
                result.append(f"@font-face{{font-family:'{family}';src:url(fonts/{path.name}) format('{fmt}');font-weight:400;font-style:normal;}}")
                break
        else:
            raise FileNotFoundError(f"Missing locally licensed sheet font: {name}")
    result.append(".title{font-family:Chakra,Arial,sans-serif}.body{font-family:Barlow,Arial,sans-serif}.mono{font-family:JetBrains,monospace}")
    return "".join(result)


def _prompts(meta, model, main_skin):
    components = list(dict.fromkeys(str(p.label) for p in model if getattr(p, "label", "")))
    name = meta.get("name", meta.get("kind", "Waffenkonzept"))
    form = str(meta.get("form", "abgeschrägte, modulare Hard-Surface-Geometrie"))
    palette = ", ".join(meta.get("palette", ("#D5CCB8", "#858F99", "#303844", "#F28C28")))
    skin = main_skin["name"]
    de = (f"Cube Escape · Variante {meta['variant']} {meta['variant_name']}: {name}. Form: {form}. "
          f"Bauteile: {', '.join(components)}. Palette: {palette}. Hauptskin: {skin}; {main_skin['description']}. "
          "Low-Poly, modulare Hard-Surface-Konstruktion mit sichtbaren Verbindungen und Haltern. "
          "Ein konsistentes 3D-Modell: große Isometrie ohne Optik und sechs Orthos im gleichen Maßstab, "
          "Hauptskin auch in vier Paletten. Optik mit Befestigung separat; Detail von Griff, Abzug/Bügel "
          "beziehungsweise Pfeilauflage und Riser in der Basisfassung. Materialansicht mit lackiertem und "
          "gebürstetem Metall, Gummi, mattem Kunststoff und kontrolliertem Funktionslicht. Fünf entworfene "
          "Skins mit Farbflächen, Glyphen, Bändern, Metallveredelung und konstruktiven Rippen. "
          "Keine schwebenden Teile, ungeplanten Durchdringungen, Unschärfe, Bloom oder Perspektivverzerrung.")
    en = (f"Cube Escape variant {meta['variant']} {meta['variant_name']}: {name}; "
          f"{meta.get('form_en', 'connected, faceted modular construction')}. Palette {palette}. "
          f"Main skin {skin}: {main_skin['description']}. Futuristic industrial low-poly hard-surface concept sheet. "
          "One consistent model: large isometric without optic and six orthographic views at one shared scale; "
          "main skin in four palettes. Detached class-specific optic with mounts. Base-model grip and trigger "
          "guard close-up, or arrow rest and riser for a bow; textured base-material overview. Painted and "
          "brushed metal, rubber contact surfaces, matte polymer and restrained functional light. Five designed "
          "skins with color blocking, glyphs, bands, metallic finishes and structural ribs. Clear connections. "
          "No floating parts, unintended intersections, bloom, blur or perspective distortion.")
    return {"de": de, "en": en}


def _view_layout(tall):
    if tall:
        return (
            ("LINKS", 0, 0, (770, 530), (3000, 650)),
            ("RECHTS", 180, 0, (770, 530), (3840, 650)),
            ("VORNE", -90, 0, (770, 530), (3000, 1250)),
            ("HINTEN", 90, 0, (770, 530), (3840, 1250)),
            ("OBEN", 0, 90, (1610, 135), (3000, 1860)),
            ("UNTEN", 0, -90, (1610, 135), (3000, 2050)),
        )
    return (
        ("LINKS", 0, 0, (770, 460), (3000, 650)),
        ("RECHTS", 180, 0, (770, 460), (3840, 650)),
        ("VORNE", -90, 0, (770, 460), (3000, 1180)),
        ("HINTEN", 90, 0, (770, 460), (3840, 1180)),
        ("OBEN", 0, 90, (770, 460), (3000, 1710)),
        ("UNTEN", 0, -90, (770, 460), (3840, 1710)),
    )


def _skin_record(skin):
    return {key: skin[key] for key in ("id", "name", "description", "accent1", "accent2")}


def _palette_roles(colors):
    """Both legacy roles and the explicit seven channels use the same palette."""
    p, m, d, a = colors[:4]
    return dict(primary=p, medium=m, dark=d, accent=a,
                MT_Primary=p, MT_Secondary=m, MT_Accent=a, MT_Metal=m,
                MT_Energy=a, MT_Emission=a, MT_Detail=d)


def build_sheet(meta, model, output: Path, number: int) -> dict:
    """Write one self-contained HTML plate and return its measurable references."""
    from skins import CATALOG, apply_skin

    if len(CATALOG) != 5 or len({s["id"] for s in CATALOG}) != 5:
        raise ValueError("Concept plates require five uniquely identified skins")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    font_dir=output/"fonts"
    font_dir.mkdir(exist_ok=True)
    for font_file in (Path(__file__).parent/"fonts").iterdir():
        if font_file.is_file():shutil.copy2(font_file,font_dir/font_file.name)
    slug = str(meta["slug"])
    if not slug or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in slug):
        raise ValueError("Sheet slug must contain lowercase ASCII letters, digits, '_' or '-'")
    weapon = [p for p in model if not getattr(p, "sight", False)]
    optics = [p for p in model if getattr(p, "sight", False)]
    if not weapon:
        raise ValueError("A sheet needs weapon geometry")
    main_skin = _skin_record(CATALOG[0])
    skin_models = {s["id"]: apply_skin(weapon, s["id"]) for s in CATALOG}
    dressed = skin_models[main_skin["id"]]
    lo, hi = (np.asarray(v) for v in bounds(weapon))
    center = (lo + hi) / 2
    # Reference the unchanged base bbox; include attached trim when fitting cells.
    vertices = _vertices(dressed)
    tall = (hi - lo)[1] > (hi - lo)[0]
    views = _view_layout(tall)
    scales = []
    for _, yaw, pitch, (w, h), _ in views:
        projected = _project(vertices - center, yaw, pitch)
        extent = np.maximum(np.abs(projected[:, :2]).max(axis=0) * 2, 1e-6)
        scales.append(min((w - 60) / extent[0], (h - 32) / extent[1]))
    common_scale = float(min(scales))
    palette = list(meta.get("palette", ("#D5CCB8", "#858F99", "#303844", "#F28C28")))
    while len(palette) < 4:
        palette.append("#858F99")
    prompts = _prompts(meta, model, main_skin)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{_e(meta.get("name", slug))} – Konzeptblatt">']
    parts.append('<defs><pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#152334" stroke-width="1"/></pattern></defs>')
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0E1622"/><rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>')
    parts.append(_text(140, 230, f"{number:02d}", 164, ACCENT, "title"))
    parts.append(_text(395, 119, "CUBE ESCAPE  /  DESIGN ARCHIVE", 28, MUTED, "mono"))
    parts.append(_text(395, 180, f"VARIANTE {meta['variant']} · {meta['variant_name'].upper()} / {meta.get('kind', '').upper()}", 40, INK, "title"))
    name = str(meta.get("name", slug))
    parts.append(_text(395, 284, name.upper(), min(92, 2400 / max(len(name), 1) * 1.45), INK, "title"))
    parts.append(_text(145, 359, "FORM", 25, ACCENT, "mono"))
    parts.append(_wrapped(255, 359, meta.get("form", "Modulare Hard-Surface-Konstruktion"), width=132, size=28, max_lines=1))
    parts.append(_text(4660, 115, f"HAUPTSKIN / {main_skin['name'].upper()}", 27, ACCENT, "mono", anchor="end"))
    for i, color in enumerate(palette[:4]):
        x = 3735 + i * 215
        parts.append(f'<rect x="{x}" y="172" width="180" height="64" rx="6" fill="{_e(color)}"/>')
        parts.append(_text(x, 274, str(color).upper(), 23, MUTED, "mono"))
    parts.append(_text(4660, 335, "7 MT_-KANÄLE + 2 FESTE SKIN-AKZENTE", 23, MUTED, "mono", anchor="end"))

    parts.append(_panel(140, 430, 2780, 1770, "01", "HAUPTANSICHT · ISOMETRIE", f"{main_skin['name'].upper()} · −45° / +35.264° · OHNE OPTIK"))
    hero_x, hero_y = 185, 670
    hero = render(dressed, yaw=-45, pitch=35.264, size=(2690, 1260), textured=True, skin=main_skin["id"])
    parts.append(_image(hero.image, hero_x, hero_y))
    anchors = getattr(hero, "anchors", {})
    priorities = (("Oberer Wurfarm", "Unterer Wurfarm", "Sehne", "Pfeilauflage", "Gehäuse", "Griff", "Abzug", "Magazin") if tall else PRIORITY)
    chosen = [(key, anchors[key]) for key in priorities if key in anchors][:8]
    by_height = sorted(chosen, key=lambda item: item[1][1])
    split = (len(by_height) + 1) // 2
    label_records = []
    for lane, values in (("top", by_height[:split]), ("bottom", by_height[split:])):
        values = sorted(values, key=lambda item: item[1][0])
        for index, (label, anchor) in enumerate(values):
            label_x = 235 + (index + .5) * 2590 / max(len(values), 1)
            label_y = 626 if lane == "top" else 2070
            ax, ay = float(anchor[0]) + hero_x, float(anchor[1]) + hero_y
            elbow_y = 651 if lane == "top" else 2017
            end_y = label_y + 14 if lane == "top" else label_y - 35
            parts.append(f'<path d="M{ax:.2f},{ay:.2f}L{ax:.2f},{elbow_y}L{label_x:.2f},{end_y}" stroke="#7D94A9" stroke-width="2.2" fill="none"/>')
            parts.append(f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r="5" fill="{ACCENT}"/>')
            parts.append(_text(label_x, label_y, label.upper(), 27, INK, "mono", anchor="middle"))
            label_records.append({"label": label, "anchor": [ax, ay], "position": [label_x, label_y], "lane": lane})
    all_labels = list(dict.fromkeys(str(p.label) for p in weapon if getattr(p, "label", "")))
    others = [label for label in all_labels if label not in {item[0] for item in chosen}]
    parts.append(_wrapped(180, 2130, "Weitere Bauteile: " + (" · ".join(others) if others else "Alle Hauptbauteile beschriftet"), width=158, size=22, leading=27, max_lines=2))

    parts.append(_panel(2960, 430, 1700, 1770, "02", "SECHS ORTHOGRAFISCHE REFERENZEN", "EIN MODELL · EIN MASSSTAB · EIN BEZUGSPUNKT"))
    parts.append(_text(3000, 581, "+X Mündung · +Y unten · +Z links", 23, MUTED, "mono"))
    view_records = []
    for view_name, yaw, pitch, size, position in views:
        x, y = position
        w, h = size
        parts.append(_text(x, y - 17, view_name, 25, INK, "mono"))
        parts.append(f'<path d="M{x},{y+h/2}H{x+w}M{x+w/2},{y}V{y+h}" stroke="#36506B" stroke-width="1.5" stroke-dasharray="12 10"/>')
        result = render(dressed, yaw=yaw, pitch=pitch, size=size, scale=common_scale, center=center, textured=True, skin=main_skin["id"])
        parts.append(_image(result.image, x, y))
        view_records.append({"name": view_name.lower(), "yaw": yaw, "pitch": pitch, "scale": common_scale, "center": center.tolist(), "viewport": [x, y, w, h], "skin": main_skin["id"]})

    # Construction details deliberately show the original, undecorated weapon.
    is_bow = tall or "bogen" in str(meta.get("kind", "")).lower() or slug == "bow"
    detail_title = "GRIFF & PFEILAUFLAGE" if is_bow else "GRIFF & ABZUGSBEREICH"
    detail_yaw=152 if is_bow else -28
    detail_pitch=-22
    detail_subtitle="BASIS · GEGENÜBERLIEGENDE SEITE · OHNE SKIN" if is_bow else "BASIS · −28° / −22° · OHNE SKIN"
    parts.append(_panel(140, 2240, 1040, 960, "03", detail_title, detail_subtitle))
    detail_names = ("Abzug", "Griff", "Magazin", "Bügel", "Abzugsbügel", "Pfeilauflage", "Riser", "Riserbrücke", "Führungssockel") if is_bow else ("Abzug", "Griff", "Magazin", "Bügel", "Abzugsbügel")
    selected = [p for p in weapon if getattr(p, "label", "") in detail_names] or weapon
    detail_lo, detail_hi = bounds(selected)
    detail_center = (np.asarray(detail_lo) + np.asarray(detail_hi)) / 2
    selected_projected = _project(_vertices(selected) - detail_center, detail_yaw, detail_pitch)
    detail_extent = np.maximum(np.abs(selected_projected[:, :2]).max(axis=0) * 2, 1e-6)
    detail_scale = float(min(850 / detail_extent[0], 550 / detail_extent[1]))
    detail = render(weapon, yaw=detail_yaw, pitch=detail_pitch, size=(960, 630), scale=detail_scale, center=detail_center, textured=True)
    parts.append(_image(detail.image, 180, 2390))
    parts.append(_wrapped(180, 3070, "Pfeilauflage · Riser · Kontaktgriff · Auslösung" if is_bow else "Kontaktgriff · freier Abzug · Bügel · eingesetzte Zelle", width=57, size=27, leading=34, max_lines=2))
    parts.append(_text(180, 3162, "Komplettes Modell im Tiefentest", 23, MUTED, "mono"))

    parts.append(_panel(1220, 2240, 1040, 960, "04", "OPTIK · SEPARAT", "BASIS · INKLUSIVE HALTER / KLEMME"))
    sight_type = str(meta.get("sight_type", "Klassenbezogene Moduloptik"))
    if optics:
        optic_iso = render(optics, yaw=-45, pitch=35.264, size=(960, 390), textured=True)
        optic_side = render(optics, yaw=0, pitch=0, size=(960, 270), textured=True)
        parts.append(_image(optic_iso.image, 1260, 2390))
        parts.append(_image(optic_side.image, 1260, 2810))
        parts.append(_text(1260, 2788, "ISOMETRIE", 22, MUTED, "mono"))
        parts.append(_text(1260, 3116, "SEITE / AUFNAHME", 22, MUTED, "mono"))
    else:
        parts.append(_wrapped(1280, 2550, "Keine separate Optik im Modell. Aufnahme und Ausrichtung an der Waffe bleiben sichtbar.", width=45, size=31, leading=41))
    parts.append(_wrapped(1260, 3162, sight_type, width=57, size=24, leading=29, max_lines=1))

    parts.append(_panel(2300, 2240, 1300, 960, "05", "MATERIAL & OBJEKTTEXTUR", "BASIS · TATSÄCHLICHE MODELLTEILE"))
    textured = render(weapon, yaw=-45, pitch=35.264, size=(1220, 440), textured=True)
    parts.append(_image(textured.image, 2340, 2370))
    material_records = []
    for i, (key, material_name, fallback_channel) in enumerate(MATERIALS):
        x, y = 2340 + (i % 2) * 620, 2830 + (i // 2) * 110
        candidates = [p for p in weapon if getattr(p, "material", "paint") == key]
        if key == "light":
            candidates = [p for p in weapon if getattr(p, "emit", False)] or candidates
        # The sample is an actual labelled component, using the same shader and
        # world coordinates as the full base view; no decorative texture mockup.
        sample = next((p for p in candidates if getattr(p, "label", "")), candidates[0] if candidates else None)
        parts.append(f'<rect x="{x}" y="{y}" width="145" height="94" rx="6" fill="#1A2A3B" stroke="#30465D"/>')
        if sample is not None:
            patch = render([sample], yaw=-28, pitch=22, size=(145, 94), textured=True)
            parts.append(_image(patch.image, x, y))
            source = str(getattr(sample, "label", "") or "Unbenanntes Bauteil")
            channel = str(getattr(sample, "channel", "") or fallback_channel)
            material_records.append({"material": key, "label": source, "channel": channel, "color": sample.color, "sample": "actual_model_component"})
        else:
            source = "Im Basismodell nicht verwendet"
            channel = "—"
            material_records.append({"material": key, "label": None, "channel": None, "reason": "not_present"})
        parts.append(_text(x + 162, y + 26, material_name, 25, INK))
        parts.append(_wrapped(x + 162, y + 56, source, width=33, size=22, leading=24, max_lines=1))
        parts.append(_wrapped(x + 162, y + 83, channel, width=35, size=18, leading=20, max_lines=1))
    parts.append(_wrapped(2960, 3090, "Objektfeste Körnung und Bürstung. Kontrollierte Lichtflächen; kein Bloom.", width=40, size=25, leading=31, max_lines=3))

    parts.append(_panel(3640, 2240, 1020, 960, "06", "VIER FARBVARIANTEN", "HAUPTSKIN · FESTE AKZENTE BLEIBEN"))
    palette_records = []
    for i, (palette_name, colors) in enumerate(PALETTES):
        x, y = 3680+(i%2)*470, 2410+(i//2)*370
        actual = palette[:4] if colors is None else list(colors)
        result = render(dressed, yaw=-45, pitch=35.264, size=(450, 270), textured=True, palette=_palette_roles(actual), skin=main_skin["id"])
        parts.append(_text(x, y, palette_name, 25, INK, "mono"))
        for j, color in enumerate(actual):
            parts.append(f'<rect x="{x+250+j*42}" y="{y-22}" width="30" height="25" rx="3" fill="{_e(color)}"/>')
        parts.append(_image(result.image, x, y + 9))
        palette_records.append({"name": palette_name, "colors": list(actual), "skin": main_skin["id"], "channels": _palette_roles(actual)})

    parts.append(_panel(140, 3240, 4520, 740, "07", "SKIN / MUSTER · FÜNF ENTWORFENE AUSFÜHRUNGEN", "FARBFLÄCHEN · GLYPHEN · BÄNDER · METALLVEREDELUNG · RIPPEN"))
    skin_records = []
    for i, skin in enumerate(CATALOG):
        x = 180 + i * 900
        if i:
            parts.append(f'<path d="M{x-20} 3375V3940" stroke="#2B4056" stroke-width="2"/>')
        parts.append(_text(x, 3405, f"{i+1:02d} / {skin['name'].upper()}", 29, INK, "title"))
        for j, key in enumerate(("accent1", "accent2")):
            parts.append(f'<rect x="{x+731+j*49}" y="3380" width="34" height="26" rx="3" fill="{_e(skin[key])}"/>')
        preview = render(skin_models[skin["id"]], yaw=-45, pitch=35.264, size=(840, 360), textured=True, skin=skin["id"])
        parts.append(_image(preview.image, x, 3440))
        parts.append(_wrapped(x, 3842, skin["description"], width=58, size=25, leading=31, max_lines=3))
        parts.append(_text(x, 3950, "7 MT-SLOTS + 2 AKZENTE / LACK · METALL · GUMMI · POLYMER", 19, MUTED, "mono"))
        record = _skin_record(skin)
        record.update(main=i == 0, viewport=[x, 3440, 840, 360], parts=len(skin_models[skin["id"]]),
                      material_channels="seven_MT_channels_plus_two_fixed_accents",
                      slots=["MT_Primary", "MT_Secondary", "MT_Accent", "MT_Metal", "MT_Energy", "MT_Emission", "MT_Detail"],
                      fixed_accents=[skin["accent1"], skin["accent2"]],
                      materials=sorted({str(getattr(p, "material", "paint")) for p in skin_models[skin["id"]]}),
                      finishes=sorted({str(getattr(p, "finish", "")) for p in skin_models[skin["id"]] if getattr(p, "finish", "")}))
        skin_records.append(record)

    parts.append(_panel(140, 4020, 4520, 240, "08", "REFERENZPROMPTS · DE / EN", "VOLLSTÄNDIG IM HTML UND ALS TEXTDATEI"))
    parts.append('<path d="M2395 4130V4225" stroke="#2B4056" stroke-width="2"/>')
    preview_de = (f"{meta['variant']} {meta['variant_name']} · {name} · Hauptskin {main_skin['name']}. {meta.get('form', '')} "
                  "Low-Poly; sichtbare Halter und Funktionsbereiche. Große Isometrie ohne Optik; sechs Orthos mit gleichem Maßstab. "
                  "Optik separat, Griff-/Abzugsdetail bzw. Pfeilauflage in Basisfassung. Lack, Bürstmetall, Gummi, Kunststoff, "
                  "kontrolliertes Funktionslicht. Vier Paletten und fünf Skins. Keine schwebenden Teile, Unschärfe oder Bloom.")
    preview_en = (f"{meta['variant']} {meta['variant_name']} · {name} · main skin {main_skin['name']}. "
                  "Industrial low-poly hard-surface model with connected modules. Large isometric without optic; six orthographic "
                  "views at one scale; detached class-specific optic with mounts. Base grip/trigger or arrow-rest detail. "
                  "Painted / brushed metal, rubber, matte polymer, functional light. Four palettes and five skins; no floating parts or bloom.")
    parts.append(_wrapped(180, 4150, "DE / " + preview_de, width=147, size=23, leading=26, max_lines=3))
    parts.append(_wrapped(2440, 4150, "EN / " + preview_en, width=143, size=23, leading=26, max_lines=3))
    parts.append('<path d="M140 4305H4660" stroke="#34475B" stroke-width="2"/>')
    parts.append(_text(140, 4355, "Alle sechs Orthos: ein Hauptskin, ein Modell, gleicher Maßstab und Bounding-Box-Bezug. Gestalterische Referenz, keine Fertigungszeichnung.", 26, MUTED))
    parts.append(_text(4660, 4400, f"K{meta['variant']}{number:02d} / {meta['variant_name'].upper()} / {slug.upper()} · WEBP Q60", 23, MUTED, "mono", anchor="end"))
    parts.append("</svg>")
    digest = hashlib.sha256()
    for part in model:
        for face in part.faces:
            digest.update(np.asarray(face.vertices, dtype="<f8").tobytes())
        digest.update(str(getattr(part, "label", "")).encode("utf8"))
    prompt_json = json.dumps(prompts, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    filename = f"K{meta['variant']}{number:02d}.html"
    document = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width={WIDTH}, initial-scale=1"><title>{_e(name)} · {_e(meta["variant_name"])} · {_e(main_skin["name"])} · Cube Escape</title>'
                '<style>' + _font_css() + f'html,body{{margin:0;width:{WIDTH}px;height:{HEIGHT}px;background:#0E1622;overflow:hidden}}svg{{display:block}}'
                '</style></head><body>' + "".join(parts) + '<script type="application/json" id="reference-prompts">' + prompt_json + '</script></body></html>')
    (output / filename).write_text(document, encoding="utf8")
    return {"filename": filename, "slug": slug, "number": number, "width": WIDTH, "height": HEIGHT,
            "canvas": {"width": WIDTH, "height": HEIGHT}, "main_skin": main_skin, "skins": skin_records,
            "variant": meta["variant"], "variant_name": meta["variant_name"], "geometry_sha256": digest.hexdigest(), "weapon_parts": len(weapon),
            "optic_parts": len(optics), "orthographic_scale": common_scale,
            "orthographic_center": center.tolist(), "orthographic_views": view_records,
            "model_bounds": {"min": lo.tolist(), "max": hi.tolist(), "center": center.tolist()},
            "hero_labels": label_records, "other_components": others, "prompts": prompts,
            "detail": {"yaw": detail_yaw, "pitch": detail_pitch, "scale": detail_scale, "center": detail_center.tolist(),
                       "full_weapon_rendered": True, "skin": None, "selected_labels": list(dict.fromkeys(getattr(p, "label", "") for p in selected))},
            "material_samples": material_records, "palette_variants": palette_records}
