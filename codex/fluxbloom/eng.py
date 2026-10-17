"""Small, dependency-free solid model vocabulary for the concept-sheet renderer.

Coordinates are x forward, y down, z toward the weapon's left side. All faces
carry outward unit normals; profiles may be concave, but must not self-intersect.
"""
from dataclasses import dataclass, field
import math
import numpy as np


@dataclass(eq=False)
class Face:
    vertices: np.ndarray
    normal: np.ndarray
    smooth_group: int = 0

    def __post_init__(self):
        self.vertices = np.asarray(self.vertices, dtype=float)
        self.normal = np.asarray(self.normal, dtype=float)
        if self.vertices.ndim != 2 or self.vertices.shape[1] != 3 or len(self.vertices) < 3:
            raise ValueError("A face needs at least three 3D vertices")
        length = np.linalg.norm(self.normal)
        if length < 1e-10:
            raise ValueError("Face normal must be nonzero")
        self.normal = self.normal / length


@dataclass(eq=False)
class Part:
    faces: list[Face]
    color: str
    emit: bool = False
    label: str = ""
    sight: bool = False
    decals: list = field(default_factory=list)
    material: str = "paint"
    role: str = "primary"
    is_decal: bool = False

    @property
    def vertices(self):
        return np.concatenate([face.vertices for face in self.faces])


def _face(vertices, smooth_group=0):
    vertices = np.asarray(vertices, dtype=float)
    # Newell's formula works for concave polygons and collinear first edges.
    normal = np.sum(np.cross(vertices, np.roll(vertices, -1, axis=0)), axis=0)
    return Face(vertices, normal, smooth_group)


def _profile(points, radius):
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 3:
        raise ValueError("A profile needs at least three 2D points")
    if np.allclose(points[0], points[-1]):
        points = points[:-1]
    # Remove consecutive duplicates, which otherwise create zero-area sides.
    points = points[np.linalg.norm(points - np.roll(points, 1, axis=0), axis=1) > 1e-9]
    if len(points) < 3:
        raise ValueError("Degenerate profile")
    area = np.sum(points[:, 0] * np.roll(points[:, 1], -1) - points[:, 1] * np.roll(points[:, 0], -1))
    if abs(area) < 1e-9:
        raise ValueError("Profile has no area")
    if area < 0:
        points = points[::-1]
    if radius <= 0:
        return points
    rounded = []
    for i, corner in enumerate(points):
        previous, following = points[i - 1], points[(i + 1) % len(points)]
        before, after = previous - corner, following - corner
        distance = min(radius, np.linalg.norm(before) * .35, np.linalg.norm(after) * .35)
        a = corner + before / np.linalg.norm(before) * distance
        b = corner + after / np.linalg.norm(after) * distance
        for t in (0., .3333333333, .6666666667, 1.):
            rounded.append((1 - t) ** 2 * a + 2 * (1 - t) * t * corner + t * t * b)
    return np.asarray(rounded)


def prism(profile_xy, color, z0, z1, r=0):
    """Extrude a simple, possibly concave side profile, with optional soft corners."""
    profile = _profile(profile_xy, r)
    z0, z1 = sorted((float(z0), float(z1)))
    if z1 - z0 < 1e-9:
        raise ValueError("Prism must have nonzero width")
    back = np.column_stack((profile, np.full(len(profile), z0)))
    front = np.column_stack((profile, np.full(len(profile), z1)))
    faces = [_face(back[::-1]), _face(front)]
    for i in range(len(profile)):
        j = (i + 1) % len(profile)
        # Curved corner facets share their edge identity, straight walls do not.
        group = 1 + i // 4 if r > 0 and i % 4 != 3 else 0
        faces.append(_face([back[i], back[j], front[j], front[i]], group))
    return Part(faces, color)


def cyl(x0, x1, y, z, radius, color):
    """Twelve-sided tube solid along x; side facets share one contour group."""
    if radius <= 0 or abs(x1 - x0) < 1e-9:
        raise ValueError("Cylinder radius and length must be nonzero")
    x0, x1 = sorted((float(x0), float(x1)))
    angle = np.arange(12) * 2 * math.pi / 12
    yz = np.column_stack((y + radius * np.cos(angle), z + radius * np.sin(angle)))
    left = np.column_stack((np.full(12, x0), yz))
    right = np.column_stack((np.full(12, x1), yz))
    faces = [_face(left[::-1]), _face(right)]
    for i in range(12):
        j = (i + 1) % 12
        faces.append(_face([left[i], left[j], right[j], right[i]], 1))
    return Part(faces, color, material="metal", role="medium")


def decal(plane, value, points, color, emit=False):
    """Make an unlit planar detail. Plane accepts z+/z-/x+/x-/y+/y-."""
    axis = str(plane)[0].lower()
    if axis not in "xyz":
        raise ValueError("Unknown decal plane")
    indices = [i for i in range(3) if i != "xyz".index(axis)]
    points = np.asarray(points, dtype=float)
    vertices = np.full((len(points), 3), float(value))
    vertices[:, indices] = points
    normal = np.zeros(3)
    normal["xyz".index(axis)] = -1 if "-" in str(plane) else 1
    face = _face(vertices)
    if np.dot(face.normal, normal) < 0:
        face = _face(vertices[::-1])
    return Part([face], color, emit=emit, material="light" if emit else "paint",
                role="accent" if emit else "medium", is_decal=True)


def label(model, text):
    model[-1].label = text
    return model[-1]


def sight(model):
    model[-1].sight = True
    return model[-1]


def bounds(model):
    vertices = [part.vertices for part in model if part.faces]
    if not vertices:
        return np.zeros(3), np.zeros(3)
    vertices = np.concatenate(vertices)
    return vertices.min(axis=0), vertices.max(axis=0)


def triangulate(vertices):
    """Ear-clip any simple planar polygon; never fill a concave notch as a fan."""
    vertices = np.asarray(vertices, dtype=float)
    normal = np.sum(np.cross(vertices, np.roll(vertices, -1, axis=0)), axis=0)
    points = np.delete(vertices, np.argmax(np.abs(normal)), axis=1)
    area = np.sum(points[:, 0] * np.roll(points[:, 1], -1) - points[:, 1] * np.roll(points[:, 0], -1))
    direction = 1 if area >= 0 else -1
    remaining = list(range(len(points)))
    triangles = []
    def cross(a, b):
        return float(a[0] * b[1] - a[1] * b[0])
    while len(remaining) > 3:
        found = False
        for at, current in enumerate(remaining):
            prev, nxt = remaining[at - 1], remaining[(at + 1) % len(remaining)]
            a, b, c = points[[prev, current, nxt]]
            turn = cross(b - a, c - b) * direction
            if turn <= 1e-10:
                continue
            inside = False
            for candidate in remaining:
                if candidate in (prev, current, nxt):
                    continue
                p = points[candidate]
                if min(cross(b - a, p - a) * direction,
                       cross(c - b, p - b) * direction,
                       cross(a - c, p - c) * direction) >= -1e-10:
                    inside = True
                    break
            if inside:
                continue
            triangles.append(vertices[[prev, current, nxt]])
            del remaining[at]
            found = True
            break
        if not found:
            # Collinear vertices can prevent every ear from being strictly convex.
            for at, current in enumerate(remaining):
                a, b, c = points[[remaining[at - 1], current, remaining[(at + 1) % len(remaining)]]]
                if abs(cross(b - a, c - b)) < 1e-10:
                    del remaining[at]
                    found = True
                    break
            if not found:
                raise ValueError("Polygon is not simple or planar")
    if len(remaining) == 3:
        triangles.append(vertices[remaining])
    return triangles
