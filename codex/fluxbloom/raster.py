"""Orthographic CPU toon renderer with object-space material sampling.

Rasterization is per polygon, using its exact plane depth and a 2x mask. A
separate surface-ID buffer makes seams independent of polygon triangulation.
"""
from dataclasses import dataclass
import math
import numpy as np
from PIL import Image, ImageDraw, ImageColor, ImageFilter
from scipy.ndimage import distance_transform_edt
from eng import bounds
import texture_catalog as textures
from skins import CATALOG, FINISH, channel_for, channel_palette, sample_surface


@dataclass
class RenderResult:
    image: Image.Image
    anchors: dict
    scale: float
    center: np.ndarray
    part_ids: np.ndarray
    model_bbox: tuple | None = None
    model_unit_m: float | None = None
    texture_scale_source: str | None = None


OUTLINE = (10, 10, 13)
LIGHT = np.array([-.35, -.8, .5])
LIGHT /= np.linalg.norm(LIGHT)


def shade_factor(normal):
    """Four contract bands, with the normal expressed in camera coordinates."""
    d = float(np.dot(normal, LIGHT))
    levels = textures.finish('paint')['ladder']['levels']
    return levels[0] if d > .75 else levels[1] if d > .45 else levels[2] if d > .1 else levels[3]


def shade_hls(colors, factor):
    """Adjust HLS lightness only, retaining the source hue and saturation."""
    rgb = np.clip(np.asarray(colors, dtype=float) / 255., 0, 1)
    lightness = (rgb.max(axis=-1) + rgb.min(axis=-1)) / 2
    target = lightness * factor if factor < 1 else lightness + (1-lightness)*(factor-1)*.9
    chroma = 1 - np.abs(2*lightness-1)
    ratio = np.divide(1-np.abs(2*target-1), chroma, out=np.zeros_like(chroma), where=chroma > 1e-12)
    return np.clip((rgb-lightness[..., None])*ratio[..., None]+target[..., None], 0, 1)*255


def rotation_matrix(yaw=0, pitch=0):
    """Yaw around y, then camera pitch around x in the y-down convention.

    Positive pitch looks down onto top surfaces (outward world normal y-).
    """
    yaw, pitch = math.radians(yaw), math.radians(pitch)
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rx = np.array([[1, 0, 0], [0, cp, sp], [0, -sp, cp]])
    return rx @ ry


def project(points, yaw=0, pitch=0, scale=1, center=None, size=(0, 0)):
    """Return screen x/y and view depth; greater depth is closer to camera."""
    points = np.asarray(points, dtype=float)
    center = np.zeros(3) if center is None else np.asarray(center, dtype=float)
    view = (points - center) @ rotation_matrix(yaw, pitch).T
    projected = view.copy()
    projected[..., 0] = view[..., 0] * scale + size[0] / 2
    projected[..., 1] = view[..., 1] * scale + size[1] / 2
    return projected


def _cell_hash(value):
    # Stable numerical hash, shared semantically with catalogue swatch cells.
    return np.mod(np.sin(value*12.9898)*43758.5453, 1.)


def texture_factor(material, world, normal=None, *, model_unit_m=None, long_axis=0):
    """Catalogue patterns at physical millimetre pitch, fixed to object space.

    Missing Specs explicitly use the catalogue start scale; sheet renders always
    pass the design/Weapon-Spec scale. Pattern axes follow the unchanged model.
    """
    world = np.asarray(world, dtype=float)*textures.model_unit_m(model_unit_m)*1000
    coords = dict(zip(('length','height','width'),np.moveaxis(world,-1,0)))
    entry = textures.material(material)
    if not entry['sheet_pattern'] or entry['pattern'] is None:
        return np.ones(world.shape[:-1])
    pattern = textures.pattern(entry['pattern'])
    pid, params = pattern['id'], pattern['params']
    if pid == 'none' or not pattern['used_by_sheets']:
        return np.ones(world.shape[:-1])
    if pid == 'gloss_gradient':
        result = np.ones(world.shape[:-1])
        for wave in params['waves']:
            phase = sum(coords[axis] for axis in wave['axes'])
            result += wave['amplitude']*np.cos(2*np.pi*phase/wave['wavelength_mm'])
    elif pid == 'brushed':
        cross = sum(world[..., axis] for axis in range(3) if axis != long_axis)
        waves = sum(wave['weight']*np.sin(2*np.pi*cross/wave['wavelength_mm']+wave['phase'])
                    for wave in params['waves'])
        result = 1+params['amplitude']*waves
    elif pid == 'knurl':
        axis = 2 if normal is None else int(np.argmax(np.abs(normal)))
        u,v = (world[..., i] for i in range(3) if i != axis)
        slope = np.tan(np.deg2rad(params['angle_deg']))
        a = np.floor((u+v*slope)/pattern['size_mm'])
        b = np.floor((u-v*slope)/pattern['size_mm'])
        result = 1-params['darkening']*((a % 2 == 0)&(b % 2 == 0))
    elif pid == 'grain':
        cells = np.floor(world/pattern['size_mm'])
        hashed = _cell_hash(cells @ np.asarray(params['hash_coefficients']))
        result = 1+params['amplitude']*(hashed-.5)
    else:
        raise ValueError(f'Unsupported catalogue sheet pattern: {pid}')
    contrast = pattern.get('contrast')
    return np.clip(result,*contrast['brightness']) if contrast else result


def _rgb(color):
    return np.asarray(ImageColor.getrgb(color)[:3], dtype=float)


def _flatten(model):
    flattened = []
    for owner, part in enumerate(model):
        flattened.append((owner, part, part.is_decal))
        for detail in part.decals:
            if hasattr(detail, "faces"):
                flattened.append((owner, detail, True))
    return flattened


def _finish_surface(values, colors, finishes, world, face, shade, *, body_height=None,
                    origin=None, wear_level='subtle'):
    """Catalogue tone ladders, highlight stripes and real-edge wear.

    Tone selection follows the approved camera-space four-band lighting. Stripe
    and patch placement are in weapon space; painted region borders never wear.
    The five existing Codex recipes use subtle wear on polished regions because
    they have no explicit edge_wear layer. Unpolished regions retain their style.
    """
    data = textures.catalog()
    paint_levels = textures.finish('paint')['ladder']['levels']
    level = int(np.argmin(np.abs(np.asarray(paint_levels)-shade)))
    extent = np.ptp(face.vertices, axis=0)
    height = max(float(extent[1] if body_height is None else body_height),1e-12)
    origin = np.zeros(3) if origin is None else np.asarray(origin)
    for identifier, code in (('polished_gold',FINISH['gold']),
                             ('polished_chrome',FINISH['chrome'])):
        selected = finishes == code
        if not selected.any():
            continue
        recipe = textures.finish(identifier)
        points, tint = world[selected], colors[selected]
        ladder = recipe['ladder']
        step = ladder['steps'][level]
        tone = tint.copy() if step['with'] is None else tint*(1-step['amount'])+_rgb(step['with'])*step['amount']
        streak = data['wear']['streak']
        if recipe['streak'] and identifier in streak['applies']:
            phase = ((points-origin) @ np.asarray(streak['direction']))/(height*streak['period_rel_height'])
            highlight = np.mod(phase,1.) < streak['width_fraction']
            peak = ladder['highlight']
            if 'fixed' in peak:
                tone[highlight] = _rgb(peak['fixed'])
            else:
                tone[highlight] = tint[highlight]*(1-peak['amount'])+_rgb(peak['with'])*peak['amount']
        # Distance to original polygon edges, never skin masks or triangles.
        distance = np.full(len(points), np.inf)
        for a,b in zip(face.vertices,np.roll(face.vertices,-1,axis=0)):
            edge = b-a
            t = np.clip((points-a)@edge/max(float(edge@edge),1e-12),0,1)
            distance = np.minimum(distance,np.linalg.norm(points-(a+t[:,None]*edge),axis=1))
        wear = data['wear']
        settings = wear['levels'][wear_level]
        width = height*settings['width_rel']
        cells = np.floor((points-origin)/(width*wear['cell_widths']))
        hashed = _cell_hash(cells @ np.array([1.,2.,3.]))
        low,high = wear['width_variation']
        variation = low+(high-low)*_cell_hash(cells @ np.array([3.,1.,2.]))
        worn = (distance < width*variation)&(hashed < settings['coverage'])
        tone[worn] = shade_hls(_rgb(wear['bare_metal']),shade)
        values[selected] = tone
    return values


def render(model, yaw=-45, pitch=35.264, size=(1000, 600), scale=None,
           center=None, textured=False, palette=None, skin=None, ow=3.0,
           shadow=False, glow=True, display_units=1.0, *, model_unit_m=None):
    """Render a model without modifying it. Scale is in final pixels/world unit.

    Explicit center and scale are honored, allowing aligned orthographic panels
    and intentionally cropped details. ow is in final sheet pixels; shadow and
    glow affect only composition, never depth IDs or anchors. Transparent pixels
    outside the geometry carry part ID -1, including glow and shadow pixels.
    """
    if skin is not None and skin not in {item["id"] for item in CATALOG}:
        raise ValueError(f"Unknown skin: {skin}")
    physical_unit = textures.model_unit_m(model_unit_m)
    resolved_palette = channel_palette(model, palette)
    width, height = map(int, size)
    if min(width, height) < 1:
        raise ValueError("Render size must be positive")
    lo, hi = bounds(model)
    center = (lo + hi) / 2 if center is None else np.asarray(center, dtype=float).copy()
    rotation = rotation_matrix(yaw, pitch)
    flattened = _flatten(model)
    if scale is None:
        vertices = [part.vertices for _, part, _ in flattened if part.faces]
        if vertices:
            view = (np.concatenate(vertices) - center) @ rotation.T
            # Fitting around the requested center, not a camera-dependent center.
            extent = np.maximum(np.max(np.abs(view[:, :2]), axis=0), 1e-6)
            scale = min(width * .44 / extent[0], height * .44 / extent[1])
        else:
            scale = 1.
    scale = float(scale)
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("Render scale must be finite and positive")
    display_units = float(display_units)
    if not math.isfinite(display_units) or display_units <= 0:
        raise ValueError("Display-unit conversion must be finite and positive")
    ow = float(ow)
    if not math.isfinite(ow) or ow < 0:
        raise ValueError("Outline width must be finite and nonnegative")
    ss = 2
    w, h, factor = width * ss, height * ss, scale * ss
    depth = np.full((h, w), -np.inf, dtype=np.float32)
    face_ids = np.full((h, w), -1, dtype=np.int32)
    owner_ids = np.full((h, w), -1, dtype=np.int32)
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    detail_pixels = np.zeros((h, w), dtype=bool)
    emission = np.zeros((h, w, 3), dtype=np.uint8)
    surface_id = 0
    for owner, part, detail in flattened:
        groups = {}
        mapped = (palette or {}).get(channel_for(part), (palette or {}).get(part.role, part.color))
        color = _rgb(part.color if getattr(part, "skin_fixed", False) else mapped)
        part_palette = dict(resolved_palette, _base_color=color)
        for face in part.faces:
            view = (face.vertices - center) @ rotation.T
            normal = rotation @ face.normal
            # Outward normals are validated by eng; decals are single-sided too.
            # Rounded camera angles can leave an edge-on chamfer with a tiny
            # positive facing cosine. A polygon fill then invents a pixel-wide
            # sliver; dividing by that cosine extrapolates its plane in front
            # of unrelated geometry. Reject numerically edge-on faces, and
            # projected areas below half a supersample pixel.
            if normal[2] <= 1e-4:
                continue
            screen = view[:, :2] * factor + np.array([w / 2, h / 2])
            projected_area = .5*abs(np.sum(screen[:, 0]*np.roll(screen[:, 1], -1)
                                         - screen[:, 1]*np.roll(screen[:, 0], -1)))
            if projected_area < .5:
                continue
            x0 = max(0, int(math.floor(screen[:, 0].min())) - 1)
            x1 = min(w, int(math.ceil(screen[:, 0].max())) + 2)
            y0 = max(0, int(math.floor(screen[:, 1].min())) - 1)
            y1 = min(h, int(math.ceil(screen[:, 1].max())) + 2)
            if x1 <= x0 or y1 <= y0:
                continue
            # Pillow fills concave polygons directly, avoiding incorrect fan fill.
            mask_image = Image.new("1", (x1 - x0, y1 - y0))
            ImageDraw.Draw(mask_image).polygon([tuple(p) for p in screen - [x0, y0]], fill=1)
            mask = np.asarray(mask_image, dtype=bool)
            yy, xx = np.mgrid[y0:y1, x0:x1]
            vx, vy = (xx + .5 - w / 2) / factor, (yy + .5 - h / 2) / factor
            plane = float(np.dot(normal, view[0]))
            vz = (plane - normal[0] * vx - normal[1] * vy) / normal[2]
            local_depth = depth[y0:y1, x0:x1]
            visible = mask & (vz > local_depth + 1e-6)
            if not np.any(visible):
                continue
            local_depth[visible] = vz[visible]
            if face.smooth_group:
                if face.smooth_group not in groups:
                    surface_id += 1
                    groups[face.smooth_group] = surface_id
                identity = groups[face.smooth_group]
            else:
                surface_id += 1
                identity = surface_id
            face_ids[y0:y1, x0:x1][visible] = identity
            owner_ids[y0:y1, x0:x1][visible] = -1 if detail else owner
            detail_pixels[y0:y1, x0:x1][visible] = detail
            # The same upper-left studio light follows every orthographic camera.
            shade = 1. if part.emit or detail else shade_factor(normal)
            values = shade_hls(color, shade)
            if skin is not None or textured or getattr(part, "finish", None):
                # Orthographic inverse: material masks are sampled in model space.
                world = np.stack((vx[visible], vy[visible], vz[visible]), axis=-1) @ rotation + center
                colors, finishes, materials = sample_surface(part, world, face.normal, skin, part_palette, return_materials=True)
                values = shade_hls(colors, shade)
                if textured and not part.emit:
                    long_axis = int(np.argmax(np.ptp(part.vertices,axis=0)))
                    for material in np.unique(materials):
                        selected = materials == material
                        values[selected] *= texture_factor(material, world[selected], face.normal,
                                                           model_unit_m=physical_unit,long_axis=long_axis)[:,None]
                if not part.emit:
                    declaration = getattr(part,'skin_declarations',{})
                    body_height = declaration.get('extent',(hi-lo).tolist())[1]
                    values = _finish_surface(values, colors, finishes, world, face, shade,
                                             body_height=body_height,origin=declaration.get('origin',lo))
            rgb[y0:y1, x0:x1][visible] = np.clip(values, 0, 255).astype(np.uint8)
            # Replacing on every depth win keeps hidden emitters out of the halo.
            emission[y0:y1, x0:x1][visible] = np.clip(values, 0, 255).astype(np.uint8) if part.emit else 0
    occupied = face_ids >= 0
    # IDs identify actual faces (or one smooth surface), not triangulation or
    # colour masks. Expand an interior seam to 0.8*ow; the silhouette is centred
    # on the geometry boundary, reaching half of 1.25*ow outside the model.
    inner = np.zeros((h, w), dtype=bool)
    for dy, dx in ((0, 1), (1, 0)):
        a = (slice(0, h-dy or None), slice(0, w-dx or None))
        b = (slice(dy, None), slice(dx, None))
        seam = (face_ids[a] != face_ids[b]) & occupied[a] & occupied[b]
        inner[a] |= seam
        inner[b] |= seam
    stroke = np.zeros((h, w), dtype=np.float32)
    if ow > 0 and occupied.any():
        if inner.any():
            stroke = np.clip(ow*.4*ss-distance_transform_edt(~inner), 0, 1)*occupied
        # A pixel centre directly beside the boundary has distance 0.5.
        boundary_distance = np.where(occupied, distance_transform_edt(occupied),
                                     distance_transform_edt(~occupied))-.5
        silhouette = np.clip(ow*.625*ss+.5-boundary_distance, 0, 1)
        stroke = np.maximum(stroke, silhouette)
    edged = rgb*(1-stroke[:, :, None]) + np.asarray(OUTLINE)*stroke[:, :, None]
    alpha = np.maximum(occupied.astype(float), stroke)
    image = Image.fromarray(np.dstack((edged.astype(np.uint8), (alpha*255).astype(np.uint8))), "RGBA")
    yy, xx = np.nonzero(occupied)
    model_bbox = None
    if len(xx):
        model_bbox = (float(xx.min()/ss), float(yy.min()/ss),
                      float((xx.max()+1)/ss), float((yy.max()+1)/ss))
    if shadow or glow:
        behind = Image.new("RGBA", (w, h))
        if shadow and model_bbox is not None:
            x0, y0, x1, y1 = model_bbox
            cx, cy = (x0+x1)/2, y1+14
            rx, ry = .45*(x1-x0), max(8., 14*scale/display_units)
            ImageDraw.Draw(behind).ellipse(((cx-rx)*ss, (cy-ry)*ss,
                                           (cx+rx)*ss, (cy+ry)*ss), fill=(0, 0, 0, 82))
        if glow and emission.any():
            halo_rgb = Image.fromarray(emission, "RGB").filter(ImageFilter.GaussianBlur(4*ss))
            # A maximum 0.3 alpha is independent of the emitter colour value.
            emit_mask = Image.fromarray((emission.max(axis=2)>0).astype(np.uint8)*255, "L")
            halo_alpha = emit_mask.filter(ImageFilter.GaussianBlur(4*ss)).point(lambda a: round(a*.3))
            # Blur premultiplied light colour then unpremultiply to avoid dark halos.
            blurred = np.asarray(halo_rgb, dtype=float)
            coverage = np.asarray(emit_mask.filter(ImageFilter.GaussianBlur(4*ss)), dtype=float)/255
            halo_colors = np.divide(blurred, coverage[:, :, None], out=np.zeros_like(blurred),
                                    where=coverage[:, :, None]>0)
            halo = Image.fromarray(np.clip(halo_colors, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
            halo.putalpha(halo_alpha)
            behind = Image.alpha_composite(behind, halo)
        image = Image.alpha_composite(behind, image)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    part_ids = owner_ids[ss // 2::ss, ss // 2::ss].copy()
    anchors = {}
    for owner, part in enumerate(model):
        if not part.label or part.is_decal:
            continue
        yy, xx = np.nonzero((part_ids == owner) & ~detail_pixels[ss // 2::ss, ss // 2::ss])
        if not len(xx):
            continue
        centroid = part.vertices.mean(axis=0)
        target = project(centroid, yaw, pitch, scale, center, (width, height))
        nearest = np.argmin((xx + .5 - target[0]) ** 2 + (yy + .5 - target[1]) ** 2)
        # One named anchor per component name; first visible component wins.
        anchors.setdefault(part.label, (float(xx[nearest]) + .5, float(yy[nearest]) + .5))
    return RenderResult(image, anchors, scale, center, part_ids, model_bbox, physical_unit,
                        'catalog_start_value_missing_spec' if model_unit_m is None else 'Weapon-Spec units.model_unit_m')
