"""Small geometric and pixel regressions; no expensive sheet generation."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eng import Face, Part, bounds, cyl, decal, label, prism, sight, triangulate
from raster import project, render, rotation_matrix, texture_factor


class GeometryTests(unittest.TestCase):
    def test_concave_polygon_triangulation_preserves_notch_and_area(self):
        points = np.array([[0, 0, 0], [4, 0, 0], [4, 1, 0], [1, 1, 0], [1, 4, 0], [0, 4, 0]], dtype=float)
        triangles = triangulate(points)
        area = sum(np.linalg.norm(np.cross(t[1] - t[0], t[2] - t[0])) / 2 for t in triangles)
        self.assertAlmostEqual(area, 7)
        for triangle in triangles:
            center = triangle.mean(axis=0)
            self.assertTrue(center[0] <= 1 or center[1] <= 1)

    def test_closed_solids_have_outward_normals(self):
        for part in (prism([(0, 0), (4, 0), (4, 2), (0, 2)], "#ffffff", -1, 1),
                     cyl(0, 4, 0, 0, 2, "#aaaaaa")):
            center = part.vertices.mean(axis=0)
            for face in part.faces:
                self.assertGreater(np.dot(face.vertices.mean(axis=0) - center, face.normal), 0)
                self.assertAlmostEqual(np.linalg.norm(face.normal), 1)

    def test_rounding_reversing_profile_and_helpers(self):
        model = [prism([(0, 0), (0, 8), (12, 8), (12, 0)], "#ffffff", -2, 2, r=1)]
        label(model, "Gehäuse")
        sight(model)
        self.assertEqual(model[0].label, "Gehäuse")
        self.assertTrue(model[0].sight)
        lo, hi = bounds(model)
        np.testing.assert_allclose(lo, [0, 0, -2])
        np.testing.assert_allclose(hi, [12, 8, 2])
        self.assertGreater(len(model[0].faces), 6)

    def test_positive_pitch_sees_top_negative_pitch_sees_underside(self):
        self.assertGreater((rotation_matrix(0, 90) @ [0, -1, 0])[2], .999)
        self.assertGreater((rotation_matrix(0, -90) @ [0, 1, 0])[2], .999)
        self.assertGreater((rotation_matrix(-45, 35.264) @ [0, -1, 0])[2], 0)
        self.assertGreater((rotation_matrix(-28, -22) @ [0, 1, 0])[2], 0)

    def test_yaw_precedes_pitch_and_normals_follow_rotation(self):
        rotation = rotation_matrix(90, 90)
        np.testing.assert_allclose(rotation @ [1, 0, 0], [0, -1, 0], atol=1e-12)
        np.testing.assert_allclose(rotation @ [0, 0, 1], [1, 0, 0], atol=1e-12)
        np.testing.assert_allclose(rotation @ rotation.T, np.eye(3), atol=1e-12)
        face = cyl(0, 2, 0, 0, 1, "white").faces[1]
        rotated_vertices = face.vertices @ rotation.T
        geometric = np.cross(rotated_vertices[1] - rotated_vertices[0], rotated_vertices[2] - rotated_vertices[0])
        geometric /= np.linalg.norm(geometric)
        np.testing.assert_allclose(geometric, rotation @ face.normal, atol=1e-12)


class RasterTests(unittest.TestCase):
    def test_outer_weight_can_change_without_changing_interior_lines(self):
        from scipy.ndimage import binary_erosion
        model = [prism([(-10,-10),(10,-10),(10,10),(-10,10)], '#c0c0c0', -5, 5)]
        args = dict(size=(120,100), scale=3, glow=False, shadow=False)
        normal = render(model, ow=4.6, **args)
        thinner = render(model, ow=4.2, inner_width_scale=4.6/4.2, **args)
        uncompensated = render(model, ow=4.2, **args)
        a, b = np.asarray(normal.image), np.asarray(thinner.image)
        # L-infinity inset: 3.375px silhouette + 3px separable LANCZOS
        # support + 1px supersample phase reserve; round up to eight.
        # Default 4-neighbour erosion measures L1 and is too shallow diagonally.
        interior = binary_erosion(normal.part_ids>=0,structure=np.ones((3,3),bool),iterations=8)
        self.assertTrue(interior.any())
        np.testing.assert_array_equal(normal.part_ids, thinner.part_ids)
        np.testing.assert_array_equal(a[interior], b[interior])
        self.assertTrue(np.any(a[interior] != np.asarray(uncompensated.image)[interior]))
        self.assertTrue(np.any(a[:,:,3] != b[:,:,3]))

    def test_interior_weight_keeps_geometry_alpha_and_anchors(self):
        model = [prism([(-10,-10),(10,-10),(10,10),(-10,10)], '#c0c0c0', -5, 5)]
        model[0].label = 'Gehäuse'
        args = dict(size=(120,100), scale=3, glow=False, shadow=False)
        normal = render(model, **args)
        stronger = render(model, inner_width_scale=1.25, **args)
        a, b = np.asarray(normal.image), np.asarray(stronger.image)
        np.testing.assert_array_equal(normal.part_ids, stronger.part_ids)
        np.testing.assert_array_equal(a[:,:,3], b[:,:,3])
        self.assertEqual(normal.anchors, stronger.anchors)
        self.assertTrue(np.any(a[:,:,:3] != b[:,:,:3]))
        self.assertLess(int(b[:,:,:3].sum()), int(a[:,:,:3].sum()))

    def box(self, z0, z1, color, name=""):
        part = prism([(-10, -10), (10, -10), (10, 10), (-10, 10)], color, z0, z1)
        part.label = name
        return part

    def test_z_buffer_is_order_independent_and_hides_anchor(self):
        rear = self.box(-4, -2, "#ff0000", "Hinten")
        front = self.box(2, 4, "#00ff00", "Vorne")
        for model in ([rear, front], [front, rear]):
            result = render(model, yaw=0, pitch=0, size=(96, 96), scale=3, center=[0, 0, 0])
            pixel = result.image.getpixel((48, 48))
            self.assertGreater(pixel[1], pixel[0])
            self.assertEqual(set(result.anchors), {"Vorne"})
            self.assertEqual(result.part_ids[48, 48], model.index(front))

    def test_intersecting_face_depth_uses_plane_not_centroid(self):
        # A tilted surface passes in front on the right, behind on the left.
        tilted = Part([Face(np.array([[-10,-10,-4], [10,-10,4], [10,10,4], [-10,10,-4]]), [-.4,0,1])], "#ff0000")
        flat = Part([Face(np.array([[-10,-10,0], [10,-10,0], [10,10,0], [-10,10,0]]), [0,0,1])], "#00ff00")
        result = render([flat, tilted], yaw=0, pitch=0, size=(96, 96), scale=3)
        self.assertEqual(result.part_ids[48, 30], 0)
        self.assertEqual(result.part_ids[48, 66], 1)

    def test_concave_prism_notch_stays_transparent(self):
        part = prism([(0,0), (12,0), (12,3), (3,3), (3,12), (0,12)], "white", -1, 1)
        result = render([part], yaw=0, pitch=0, size=(96,96), scale=5, center=[6,6,0])
        self.assertEqual(result.part_ids[60,60], -1)
        self.assertEqual(result.image.getpixel((60,60))[3], 0)
        self.assertEqual(result.part_ids[25,60], 0)

    def test_anchors_are_visible_pixels_and_decals_excluded(self):
        box = self.box(-2, 2, "#c0c0c0", "Gehäuse")
        detail = decal("z+", 3, [(-5,-5), (5,-5), (5,5), (-5,5)], "#222222")
        detail.label = "Aufkleber"
        result = render([box, detail], yaw=0, pitch=0, size=(96,96), scale=3)
        self.assertNotIn("Aufkleber", result.anchors)
        x,y = result.anchors["Gehäuse"]
        self.assertEqual(result.part_ids[int(y), int(x)], 0)

    def test_attached_decal_cannot_supply_a_hidden_part_anchor(self):
        box = self.box(-2, 2, "#c0c0c0", "Gehäuse")
        box.decals.append(decal("z+", 3, [(-11,-11), (11,-11), (11,11), (-11,11)], "#222222"))
        result = render([box], yaw=0, pitch=0, size=(96,96), scale=3, center=[0,0,0])
        self.assertNotIn("Gehäuse", result.anchors)
        self.assertEqual(result.part_ids[48,48], -1)

    def test_orthos_honor_fixed_world_center_and_scale(self):
        part = self.box(-2, 2, "white")
        center = np.array([2., 3., 0.])
        for yaw, pitch in ((0,0), (180,0), (-90,0), (90,0), (0,90), (0,-90)):
            result = render([part], yaw=yaw, pitch=pitch, size=(96,96), scale=2, center=center)
            self.assertEqual(result.scale, 2)
            np.testing.assert_array_equal(result.center, center)
            np.testing.assert_allclose(project(center, yaw, pitch, 2, center, (96,96)), [48,48,0])

    def test_palette_does_not_mutate_model(self):
        part = self.box(-1, 1, "#ffffff")
        before = part.vertices.copy()
        result = render([part], size=(64,64), palette={"primary":"#ff0000"})
        self.assertEqual(part.color, "#ffffff")
        np.testing.assert_array_equal(part.vertices, before)
        self.assertGreater(np.asarray(result.image)[:,:,0].sum(), np.asarray(result.image)[:,:,1].sum())

    def test_texture_is_object_space_across_camera_views(self):
        points = np.array([[2.,3.,4.], [-3.,2.,1.], [5.,-4.,2.]])
        expected = texture_factor("metal", points)
        self.assertGreater(np.ptp(expected), .01)
        for yaw, pitch in ((0,0),(-45,35.264),(90,-22),(180,90)):
            rotation = rotation_matrix(yaw, pitch)
            center = np.array([3.,-2.,1.])
            projected = project(points, yaw, pitch, 7, center, (96,96))
            view = projected.copy()
            view[:,:2] = (view[:,:2] - [48,48]) / 7
            reconstructed = view @ rotation + center
            np.testing.assert_allclose(texture_factor("metal", reconstructed), expected, atol=1e-12)
        for material in ("paint", "rubber", "plastic", "light"):
            values = texture_factor(material, points)
            np.testing.assert_array_equal(values, texture_factor(material, points))
            from texture_catalog import material as catalog_material, pattern
            limits = pattern(catalog_material(material)['pattern'])['contrast']
            low, high = limits['brightness'] if limits else (1., 1.)
            self.assertTrue(np.all((values >= low) & (values <= high)))

    def test_shared_smooth_group_omits_internal_contour(self):
        vertices = [np.array([[-10,-10,1], [0,-10,1], [0,10,1], [-10,10,1]]),
                    np.array([[0,-10,1], [10,-10,1], [10,10,1], [0,10,1]])]
        smooth = Part([Face(v, [0,0,1], 1) for v in vertices], "#ffffff")
        faceted = Part([Face(v, [0,0,1]) for v in vertices], "#ffffff")
        a = render([smooth], yaw=0, pitch=0, size=(96,96), scale=3)
        b = render([faceted], yaw=0, pitch=0, size=(96,96), scale=3)
        self.assertGreater(a.image.getpixel((48,48))[0], 150)
        self.assertLess(b.image.getpixel((48,48))[0], 100)

    def test_textured_render_changes_material_without_changing_geometry(self):
        part = self.box(-2, 2, "#cccccc")
        part.material = "rubber"
        flat = render([part], yaw=-45, pitch=35.264, size=(96,96))
        textured = render([part], yaw=-45, pitch=35.264, size=(96,96), textured=True)
        np.testing.assert_array_equal(flat.part_ids, textured.part_ids)
        np.testing.assert_array_equal(np.asarray(flat.image)[:,:,3], np.asarray(textured.image)[:,:,3])
        self.assertGreater(np.abs(np.asarray(flat.image).astype(float) - np.asarray(textured.image)).sum(), 1000)

    def test_empty_model_is_transparent(self):
        result = render([], size=(32,32))
        self.assertEqual(np.asarray(result.image)[:,:,3].max(), 0)
        self.assertTrue(np.all(result.part_ids == -1))
        self.assertEqual(result.anchors, {})


if __name__ == "__main__":
    unittest.main()
