"""Orthographic CPU toon renderer with object-space material sampling.

Rasterization is per polygon, using its exact plane depth and a 2x mask. A
separate surface-ID buffer makes seams independent of polygon triangulation.
"""
from dataclasses import dataclass
import math
import numpy as np
from PIL import Image, ImageDraw, ImageColor
from scipy.ndimage import distance_transform_edt
from eng import bounds
from skins import CATALOG, FINISH, channel_for, channel_palette, sample_surface


@dataclass
class RenderResult:
    image: Image.Image
    anchors: dict
    scale: float
    center: np.ndarray
    part_ids: np.ndarray


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


def texture_factor(material, world, normal=None):
    """Deterministic scalar modulation. No screen coordinates or random state.

    Brush marks run along x; diamond knurling crosses the grip's y/z surface.
    Analytic grain keeps samples exactly stable between all camera orientations.
    """
    world = np.asarray(world, dtype=float)
    x, y, z = np.moveaxis(world, -1, 0)
    fine = np.sin(x * 17.31 + y * 41.73 + z * 29.17) * np.sin(x * 35.13 - y * 19.31 + z * 47.77)
    if material == "metal":
        return 1 + .065 * np.sin(y * 7.7 + z * 11.3 + .1 * np.sin(x * .3)) + .025 * fine
    if material == "rubber":
        # Select a world-space surface plane: diamonds must cross both visible
        # axes instead of degenerating into bands on a constant-z grip side.
        axis = 2 if normal is None else int(np.argmax(np.abs(normal)))
        u, v = (x, y) if axis == 2 else (z, y) if axis == 0 else (x, z)
        a = np.abs(np.sin((v + u) * 1.2))
        b = np.abs(np.sin((v - u) * 1.2))
        grooves = np.minimum(a, b)
        return .88 + .15 * np.minimum(grooves * 4, 1) + .015 * fine
    if material == "plastic":
        return 1 + .045 * fine
    if material == "light":
        return np.ones_like(x)
    return 1 + .035 * np.sin(y * .09 + z * .13) + .012 * fine


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


def _finish_surface(values, colors, finishes, world, face, shade):
    """Broad studio reflections and restrained wear, with no noise highlights.

    Gold keeps a warm dark/mid/light tonal range; chrome reflects cool broad
    environmental lobes. The fixed world-space reflection is stable across all
    technical views. Wear follows actual mesh edges, never painted mask borders.
    """
    metallic = (finishes == FINISH['gold']) | (finishes == FINISH['chrome'])
    if not metallic.any():
        return values
    points = world[metallic]
    tint = colors[metallic]
    normal = face.normal
    # Soft reflection lobes combine surface orientation and long material flow.
    direction = np.array([-.28, -.68, .68])
    facing = abs(float(np.dot(normal, direction)))
    phase = points[:, 1]*.075 + points[:, 2]*.05 + points[:, 0]*.012
    lobe = (.5+.5*np.cos(phase))**3
    reflection = .36 + .36*facing + .46*lobe
    gold = finishes[metallic] == FINISH['gold']
    reflected = tint*reflection[:, None]
    # A soft coloured specular component preserves gold, avoiding white flecks.
    specular = lobe[:, None] * (.10+.08*facing)
    reflected += np.where(gold[:, None], [62.,43.,13.], [45.,52.,58.])*specular
    # Real polygon-edge distances; no treatment along decorative colour borders.
    edge_distance = np.full(len(points), np.inf)
    for a,b in zip(face.vertices, np.roll(face.vertices,-1,axis=0)):
        edge = b-a
        t = np.clip((points-a)@edge / max(float(edge@edge),1e-12),0,1)
        distance = np.linalg.norm(points-(a+t[:,None]*edge),axis=1)
        edge_distance = np.minimum(edge_distance, distance)
    irregular = .65+.35*np.sin(points[:,0]*.71+points[:,1]*.39+points[:,2]*.43)
    wear = np.clip((.45-edge_distance)/.45,0,1)*irregular*.22
    undercoat = np.where(gold[:, None], [145.,139.,118.], [130.,143.,149.])
    reflected = reflected*(1-wear[:,None])+undercoat*wear[:,None]
    values[metallic] = reflected
    return values


def render(model, yaw=-45, pitch=35.264, size=(1000, 600), scale=None,
           center=None, textured=False, palette=None, skin=None):
    """Render a model without modifying it. Scale is in final pixels/world unit.

    Explicit center and scale are honored, allowing aligned orthographic panels
    and intentionally cropped details. Transparent pixels carry part ID -1.
    """
    if skin is not None and skin not in {item["id"] for item in CATALOG}:
        raise ValueError(f"Unknown skin: {skin}")
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
    ss = 2
    w, h, factor = width * ss, height * ss, scale * ss
    depth = np.full((h, w), -np.inf, dtype=np.float32)
    face_ids = np.full((h, w), -1, dtype=np.int32)
    owner_ids = np.full((h, w), -1, dtype=np.int32)
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    detail_pixels = np.zeros((h, w), dtype=bool)
    light = np.array([-.35, -.8, .5])
    light /= np.linalg.norm(light)
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
            if normal[2] <= 1e-8:
                continue
            screen = view[:, :2] * factor + np.array([w / 2, h / 2])
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
            # Four lighting bands. Light direction is fixed in model coordinates.
            intensity = float(np.dot(face.normal, light))
            band = .58 if intensity < -.25 else .73 if intensity < .2 else .88 if intensity < .65 else 1.
            shade = 1. if part.emit or detail else band
            values = color * shade
            if skin is not None or textured or getattr(part, "finish", None):
                # Orthographic inverse: material masks are sampled in model space.
                world = np.stack((vx[visible], vy[visible], vz[visible]), axis=-1) @ rotation + center
                colors, finishes = sample_surface(part, world, face.normal, skin, part_palette)
                values = colors * shade
                if textured and not part.emit:
                    values *= texture_factor(part.material, world, face.normal)[:, None]
                if not part.emit:
                    values = _finish_surface(values, colors, finishes, world, face, shade)
            rgb[y0:y1, x0:x1][visible] = np.clip(values, 0, 255).astype(np.uint8)
    occupied = face_ids >= 0
    # Interior and silhouette transitions come solely from the face-ID buffer.
    inner = np.zeros((h, w), dtype=bool)
    silhouette = np.zeros((h, w), dtype=bool)
    for dy, dx in ((0, 1), (1, 0)):
        a = (slice(0, h - dy or None), slice(0, w - dx or None))
        b = (slice(dy, None), slice(dx, None))
        different = face_ids[a] != face_ids[b]
        solid_a, solid_b = occupied[a], occupied[b]
        seam = different & solid_a & solid_b
        edge = different & (solid_a ^ solid_b)
        inner[a] |= seam
        inner[b] |= seam
        silhouette[a] |= edge & solid_a
        silhouette[b] |= edge & solid_b
    # ~1 output pixel internal stroke, silhouette distance threshold 1.25x.
    stroke = inner.astype(float)
    if np.any(silhouette):
        # Inward silhouette stroke: 2.5 supersamples versus two at an internal seam.
        outer = np.clip(1.25 * ss - distance_transform_edt(~silhouette), 0, 1)
        stroke = np.maximum(stroke, outer * occupied)
    edged = rgb * (1 - stroke[:, :, None]) + np.array([22, 29, 38]) * stroke[:, :, None]
    rgb = edged.astype(np.uint8)
    rgba = np.dstack((rgb, occupied.astype(np.uint8) * 255))
    image = Image.fromarray(rgba, "RGBA")
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
    return RenderResult(image, anchors, scale, center, part_ids)
