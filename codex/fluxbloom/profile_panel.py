"""Codex SVG target legend, with six tiles below the actual material samples."""
import html
import textwrap

from texture_catalog import catalog, material
from texture_profile import TILES, ENERGY_COLORS, WEAR_NAMES


def _text(x, y, value, size, color='#E5E9ED', family='body'):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" class="{family}">'
            f'{html.escape(value)}</text>')


def _swatch(key, entry, color, accent):
    """Schematic ID legend; actual object-space samples stay in the panel above."""
    result = f'<rect width="86" height="36" rx="5" fill="{color}"/>'
    if key == 'edge_wear':
        wear = catalog()['wear']
        coverage = wear['levels'][entry['level']]['coverage']
        # The sum of exposed edge-segment lengths is exactly coverage × width.
        for x in (0, 22, 44, 66):
            result += f'<rect x="{x}" width="{86*coverage/4:.3f}" height="6" fill="{wear["bare_metal"]}"/>'
        ordered = sorted(wear['levels'], key=lambda k: wear['levels'][k]['toolgen'])
        for i in range(len(ordered)):
            fill = accent if i <= ordered.index(entry['level']) else '#34475B'
            result += f'<rect x="{8+i*25}" y="24" width="19" height="5" fill="{fill}"/>'
        return result
    mid = entry['material']
    if mid == 'rubber':
        for x in range(-28, 86, 9):
            result += f'<path d="M{x},36l36,-36m-36,0l36,36" stroke="#91A3B7" stroke-width="1" opacity=".35"/>'
    elif mid == 'brushed':
        for y in range(4, 36, 4):
            result += f'<path d="M4,{y}h78" stroke="#FFFFFF" stroke-width="1" opacity=".22"/>'
    elif mid == 'rough_cast':
        for i in range(42):
            result += f'<circle cx="{3+(i*29)%80}" cy="{3+(i*13)%30}" r="1.2" fill="#050B12" opacity=".45"/>'
    elif mid == 'ceramic':
        result += '<path d="M28,0v36m29,-36v36M0,18h86" stroke="#FFFFFF" opacity=".4"/>'
    elif mid in ('polished', 'satin', 'painted', 'energy_glass'):
        width = 4 if mid == 'polished' else 17
        result += f'<path d="M35,1l16,34" stroke="#FFFFFF" stroke-width="{width}" opacity=".26"/>'
    elif mid == 'painted_matte':
        for i in range(65):
            result += f'<circle cx="{2+(i*31)%82}" cy="{2+(i*17)%32}" r=".65" fill="#FFFFFF" opacity=".16"/>'
    return result


def panel(prof, viewport, compact, colors):
    x, y, w, h = viewport
    cols, gap = (2 if compact else 3), 12
    rows = 6 // cols
    tw, th = (w-(cols-1)*gap)/cols, (h-35-(rows-1)*gap)/rows
    result = '<g id="texture-profile">'
    result += _text(x, y+19, 'TEXTURPROFIL · TYPVORGABE · WAFFEN 1–9', 17 if compact else 20, '#91A3B7', 'title')
    records = []
    for i, (key, label) in enumerate(TILES):
        tx, ty = x+(i%cols)*(tw+gap), y+35+(i//cols)*(th+gap)
        e = prof[key]
        result += f'<g data-profile-tile="{key}" transform="translate({tx},{ty})">'
        result += f'<rect width="{tw}" height="{th}" rx="7" fill="#0E1622" stroke="#30465D"/>'
        result += _text(104, 19, label, 13 if compact else 17, '#91A3B7', 'title')
        if key == 'decals':
            result += '<rect x="8" y="8" width="86" height="36" rx="5" fill="#1A2A3B"/>'
            result += _text(51, 34, 'ID', 21, colors['accent'], 'mono')
            for n, identifier in enumerate(e['toolgen']):
                result += _text(104, 35+n*13, identifier, 11 if compact else 15, family='mono')
        else:
            color = colors['housing'] if key == 'edge_wear' else colors.get(key, colors['accent'])
            if key == 'energy':
                color = ENERGY_COLORS[e['color']]
            result += f'<defs><clipPath id="profile-{key}"><rect width="86" height="36" rx="5"/></clipPath></defs><g transform="translate(8,8)" clip-path="url(#profile-{key})">{_swatch(key,e,color,colors["accent"])}</g>'
            sub = 'Stufe '+WEAR_NAMES[e['level']] if key == 'edge_wear' else material(e['material'])['name']['de'].capitalize()
            result += _text(104, 40, sub, 17 if compact else 21)
        for n, line in enumerate(textwrap.wrap('„'+e['text_de']+'“', width=31 if compact else 39,
                                                break_long_words=False, break_on_hyphens=False)):
            result += _text(8, 64+n*20, line, 17 if compact else 19, '#C7D1DC')
        result += '</g>'
        records.append(dict(key=key, viewport=[tx,ty,tw,th]))
    return result+'</g>', records
