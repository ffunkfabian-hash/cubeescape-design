"""Five independently designed object-space finishes and attached trim.

Patterns share one weapon-space frame, so a colour block crosses real assembly
seams. Functional optics, contact rubber, emitters and triggers are excluded.
This is a local concept renderer recipe, not an asserted Toolgen import format.
"""
from copy import deepcopy
import numpy as np
from PIL import ImageColor
from eng import bounds, decal, prism
import texture_catalog as textures

CHANNELS = ('MT_Primary', 'MT_Secondary', 'MT_Accent', 'MT_Metal',
            'MT_Energy', 'MT_Emission', 'MT_Detail')
CATALOG = textures.CodexSkinRecords()
FINISH = {'paint': 0, 'gold': 1, 'chrome': 2, 'metal': 3, 'rubber': 4, 'plastic': 5, 'light': 6,
          'polished_gold': 1, 'polished_chrome': 2, 'neon': 6}
_ROLE_CHANNEL = dict(primary='MT_Primary', medium='MT_Secondary', dark='MT_Detail', accent='MT_Accent')
_DEFAULTS = dict(zip(CHANNELS, ('#D5CCB8','#858F99','#F28C28','#858F99','#57C7CA','#9BE4DD','#303844')))


def channel_for(part):
    """Explicit seven-slot assignments win; legacy roles remain readable."""
    channel = getattr(part, 'channel', None)
    if channel in CHANNELS:
        return channel
    if part.emit:
        return 'MT_Emission'
    if part.material == 'light':
        return 'MT_Energy'
    if part.material == 'metal':
        return 'MT_Metal'
    return _ROLE_CHANNEL.get(part.role, 'MT_Primary')


def channel_palette(model, palette=None):
    """Return all seven colours; four-role palettes supply documented fallbacks."""
    result = _DEFAULTS.copy()
    seen = set()
    for part in model:
        channel = channel_for(part)
        if channel not in seen and not getattr(part, 'skin_fixed', False):
            result[channel] = part.color
            seen.add(channel)
    palette = palette or {}
    for role, channel in _ROLE_CHANNEL.items():
        if role in palette:
            result[channel] = palette[role]
    if 'medium' in palette and 'MT_Metal' not in palette:
        result['MT_Metal'] = palette['medium']
    if 'accent' in palette:
        result['MT_Energy'] = palette['accent']
        result['MT_Emission'] = palette['accent']
    result.update({key: value for key, value in palette.items() if key in CHANNELS})
    return result


def _rgb(color):
    return np.array(ImageColor.getrgb(color)[:3], dtype=float)


def _eligible(part):
    forbidden = ('abzug', 'trigger', 'sehne', 'string', 'pfeil', 'arrow', 'linse', 'lens', 'visier', 'optik')
    return (not part.sight and not part.emit and not part.is_decal
            and part.material not in ('rubber', 'light')
            and not getattr(part, 'skin_trim', False)
            and not any(word in part.label.lower() for word in forbidden))


def _contrast(requested, base, colors):
    candidate = _rgb(colors.get(requested, requested))
    if np.linalg.norm(candidate - base) < 88:
        # Guarantee contrast even when all palette slots have similar colours.
        options = [_rgb(colors['MT_Detail']), _rgb('#ECE8D9'), _rgb('#24313C')]
        candidate = max(options, key=lambda c: float(np.linalg.norm(c-base)))
    return candidate


def sample_surface(part, world, normal, skin_id=None, palette=None, *, return_materials=False):
    """Return RGB samples and finish IDs, with no camera or screen dependency.

    palette can be a resolved seven-slot mapping or a legacy four-role mapping.
    Fixed skin accents and trim do not follow palette changes. Geometry decals
    are already placed by apply_skin and are never generated during rendering.
    """
    world = np.asarray(world, dtype=float)
    shape = world.shape[:-1]
    colors = channel_palette([part], palette)
    base = _rgb(part.color if getattr(part, 'skin_fixed', False)
                else colors[channel_for(part)])
    if palette and '_base_color' in palette and not getattr(part, 'skin_fixed', False):
        base = np.asarray(palette['_base_color'], dtype=float)
    rgb = np.broadcast_to(base, shape + (3,)).copy()
    finish = np.full(shape, FINISH.get(getattr(part, 'finish', part.material), 0), dtype=np.uint8)
    materials = np.full(shape, textures.material(part.material)['id'], dtype=object)
    if skin_id is None or not _eligible(part):
        return (rgb, finish, materials) if return_materials else (rgb, finish)
    recipe = textures.skin(skin_id)
    declaration = getattr(part, 'skin_declarations', {})
    origin = np.asarray(declaration.get('origin', [0, 0, 0]), dtype=float)
    extent = np.maximum(np.asarray(declaration.get('extent', [200, 100, 35]), dtype=float), 1e-12)
    u, v, w = np.moveaxis((world-origin)/extent, -1, 0)
    axes = dict(u=u, v=v, w=w)
    accents = {slot: _rgb(value['color']) for slot, value in recipe['accents'].items()}

    def color_for(slot):
        if slot == 'base':
            return base
        if slot in accents:
            return accents[slot]
        if slot in ('MT_Detail', 'MT_Secondary'):
            return _contrast(slot, base, colors)
        return _rgb(colors.get(slot, slot))

    for layer in recipe['layers']:
        if layer['type'] == 'blend':
            mix = np.clip((axes[layer['axis']]-layer['lo'])/(layer['hi']-layer['lo']), 0, 1)
            mix = (mix*layer['strength'])[..., None]
            rgb[:] = color_for(layer['from'])*(1-mix) + color_for(layer['to'])*mix
        elif layer['type'] == 'region':
            mask = _region_mask(layer['mask'], axes)
            rgb[mask] = color_for(layer['color'])
            finish[mask] = FINISH[layer['finish']]
            if 'material' in layer:
                materials[mask] = textures.material(layer['material'])['id']
        else:
            raise ValueError(f"Unsupported Codex skin layer: {layer['type']}")
    return (rgb, finish, materials) if return_materials else (rgb, finish)


def _region_mask(mask, axes):
    kind = mask['kind']
    if kind in ('all', 'any'):
        children = [_region_mask(child, axes) for child in mask['of']]
        return np.logical_and.reduce(children) if kind == 'all' else np.logical_or.reduce(children)
    if kind == 'ellipse_rings':
        radius = np.sqrt(sum(((axes[axis]-center)*scale)**2
                             for axis, center, scale in zip(('u','v'),mask['center'],mask['scale'])))
        return np.logical_or.reduce([(radius > lo) & (radius < hi) for lo,hi in mask['ranges']])
    if kind == 'diagonal':
        value = axes['u'] + mask['k']*axes['v']
    elif kind == 'sawtooth':
        value = np.mod(axes['u']*mask['fu']+axes['v']*mask['fv'], 1.)
    elif kind in axes:
        value = axes[kind]
    else:
        raise ValueError(f'Unknown catalogue mask kind: {kind}')
    result = np.ones_like(value, dtype=bool)
    if mask.get('lo') is not None:
        result &= value > mask['lo']
    if mask.get('hi') is not None:
        result &= value < mask['hi']
    return result


def _inside(points, polygon):
    """Vectorised even/odd test, including concave side plates."""
    points, polygon = np.asarray(points), np.asarray(polygon)
    x, y = points[:, 0], points[:, 1]
    inside = np.zeros(len(points), dtype=bool)
    for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
        crossing = ((a[1] > y) != (b[1] > y))
        denom = b[1]-a[1]
        if abs(denom) > 1e-10:
            inside ^= crossing & (x < (b[0]-a[0])*(y-a[1])/denom+a[0])
    return inside


def _free_patch(model, side, glyph=True):
    """Fit a real rectangle within a visible planar side face, away from holes.

    All faces participate in the visibility check, including functional blockers.
    No successful fit is an explicit omission, never floating fallback geometry.
    """
    candidates = []
    blockers = []
    for owner, part in enumerate(model):
        if getattr(part, 'skin_trim', False):
            continue
        for face in part.faces:
            if abs(face.normal[2]) < 1e-6:
                continue
            poly = face.vertices[:, :2]
            blockers.append((face, poly))
            if _eligible(part) and face.normal[2]*side > .999:
                area = abs(np.sum(poly[:, 0]*np.roll(poly[:, 1], -1)-poly[:, 1]*np.roll(poly[:, 0], -1)))/2
                candidates.append((area, owner, face, poly))
    for _, owner, face, poly in sorted(candidates, key=lambda row: -row[0]):
        low, high = poly.min(axis=0), poly.max(axis=0)
        for shrink in (1., .76, .53):
            width = min(34., (high[0]-low[0])*.58)*shrink
            height = min(17., (high[1]-low[1])*.48)*shrink
            if width < 9 or height < 5:
                continue
            for cx in np.linspace(low[0]+width*.56, high[0]-width*.56, 5):
                for cy in np.linspace(low[1]+height*.56, high[1]-height*.56, 5):
                    # Dense perimeter/interior validation plus a margin.
                    xx, yy = np.meshgrid(np.linspace(cx-width*.53,cx+width*.53,7),
                                         np.linspace(cy-height*.53,cy+height*.53,5))
                    xy = np.column_stack((xx.ravel(), yy.ravel()))
                    if not _inside(xy, poly).all():
                        continue
                    z = float(face.vertices[0,2])
                    occluded = False
                    for other, other_poly in blockers:
                        if other is face:
                            continue
                        oz = (np.dot(other.normal, other.vertices[0])-xy@other.normal[:2])/other.normal[2]
                        if np.any((side*(oz-z) > .015) & _inside(xy, other_poly)):
                            occluded = True
                            break
                    if not occluded:
                        return owner, side, z, cx, cy, width, height
    return None


# Original slanted open-segment numerals; no external game glyphs/fonts.
_DIGITS = {
    '0': ('a','b','c','d','e','f'), '1': ('b','c'), '2': ('a','b','g','e','d'),
    '3': ('a','b','g','c','d'), '7': ('a','b','c'), '8': ('a','b','c','d','e','f','g'),
}
_SEGMENTS = dict(a=((.18,0),(.8,0)), b=((.88,.09),(.80,.43)),
                 c=((.77,.57),(.69,.91)), d=((.09,1),(.69,1)),
                 e=((.02,.57),(.10,.91)), f=((.11,.09),(.03,.43)),
                 g=((.13,.5),(.74,.5)))


def _trim(part, recipe, host, kind, finish='paint', fixed=True):
    part.skin_trim = True
    part.skin_fixed = fixed
    part.skin_id = recipe['id']
    part.skin_host = host
    part.skin_kind = kind
    part.finish = finish
    part.channel = 'MT_Detail' if kind == 'badge' else 'MT_Metal'
    part.label = ''
    return part


def _attach(model, patch, recipe):
    owner, side, z, cx, cy, width, height = patch
    host = model[owner]
    # Opposite side uses a reflected local x basis: the number reads outward on
    # BOTH sides instead of becoming mirrored in the right orthographic view.
    def polygon(points, offset=.045, color='#24313C', kind='glyph'):
        xy = [(cx+side*x*width, cy+y*height) for x,y in points]
        item = decal('z+' if side > 0 else 'z-', z+side*offset, xy, color)
        host.decals.append(_trim(item, recipe, owner, kind))
    decor = textures.skin(recipe['id'])['decor']
    polygon([(-.49,-.46),(.49,-.46),(.49,.20),(-.49,.20)], .025, decor['badge']['color'], 'badge')
    number = decor['number']
    for at, digit in enumerate(number):
        for segment in _DIGITS[digit]:
            a,b = np.asarray(_SEGMENTS[segment])
            d = b-a
            n = np.array([-d[1],d[0]])/np.linalg.norm(d)*.044
            points = [a+n,b+n,b-n,a-n]
            points = [((p[0]+at)*.31-.35, p[1]*.50-.39) for p in points]
            polygon(points, .05, recipe['accent2'])
    # A compact split-chevron emblem is the family's own design signature.
    if decor['emblem'] != 'split_chevron':
        raise ValueError(f"Unknown catalogue emblem: {decor['emblem']}")
    polygon([(.29,-.37),(.43,-.17),(.29,.03),(.32,-.17)], .05, recipe['accent1'])
    rib_count = decor['trim']['count']
    for at in range(rib_count):
        x = cx + (at-(rib_count-1)/2)*width*.135
        w = width*.047
        y0, y1 = cy+height*.29, cy+height*.45
        profile = [(x-w,y0),(x+w,y0),(x+w,y1),(x-w,y1)]
        # Rib's root penetrates its actual supporting surface by .02 units.
        depth = min(.95, height*.075)
        item = prism(profile, recipe['accent1'], z-side*.02, z+side*depth)
        item.material = 'metal'
        item.role = 'medium'
        item = _trim(item, recipe, owner, decor['trim']['kind'], decor['trim']['finish'])
        model.append(item)


def apply_skin(model, skin_id):
    """Copy all geometry, declare masks and safely attach badges/ribs to faces."""
    if skin_id not in {row['id'] for row in textures.codex_skins()}:
        raise ValueError(f'Unknown Codex skin: {skin_id}')
    recipe = textures.skin_record(textures.skin(skin_id))
    result = deepcopy([part for part in model if not getattr(part, 'skin_trim', False)])
    # Reapplying a skin is idempotent: discard only our old attached details.
    for part in result:
        part.decals = [d for d in part.decals if not getattr(d, 'skin_trim', False)]
    lo, hi = bounds([part for part in result if not part.sight])
    for part in result:
        part.channel = channel_for(part)
        part.skin_id = skin_id
        part.skin_declarations = dict(id=skin_id, origin=lo.tolist(), extent=(hi-lo).tolist(),
                                      eligible=_eligible(part), frame='weapon_model_units',
                                      fixed_accents=[recipe['accent1'],recipe['accent2']])
    for side in (1, -1):
        patch = _free_patch(result, side)
        if patch is not None:
            _attach(result, patch, recipe)
    return result
