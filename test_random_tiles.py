"""Tests for random_tiles.py. Standard library only, like the script itself.

    python -m unittest
"""

import random
import unittest

import random_tiles as rt


def winding_number(x, y, ring):
    """Independent point-in-polygon, used only by the tests.

    The script decides containment by ray casting. Checking its output with the
    same algorithm would only prove the code is consistent with itself, so the
    tests count winding instead: different arithmetic, same question.
    """
    total = 0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        side = (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
        if y1 <= y:
            if y2 > y and side > 0:
                total += 1
        elif y2 <= y and side < 0:
            total -= 1
    return total


def inside_by_winding(x, y, polygons):
    for polygon in polygons:
        if winding_number(x, y, polygon[0]) != 0:
            if not any(winding_number(x, y, hole) != 0 for hole in polygon[1:]):
                return True
    return False


class TestData(unittest.TestCase):
    def setUp(self):
        self.features = rt.load_provinces()

    def test_all_thirty_one_provinces_are_present(self):
        self.assertEqual(len(self.features), 31)

    def test_every_province_has_an_english_name_and_iso_code(self):
        for feature in self.features:
            props = feature["properties"]
            self.assertTrue(props.get("name:en"), props)
            self.assertRegex(props.get("ISO3166-2", ""), r"^IR-\d{2}$")

    def test_iso_codes_are_unique(self):
        codes = [f["properties"]["ISO3166-2"] for f in self.features]
        self.assertEqual(len(codes), len(set(codes)))


class TestNames(unittest.TestCase):
    def setUp(self):
        self.features = rt.load_provinces()

    def test_every_stored_name_finds_its_own_province(self):
        """The regression that started this file.

        23 of the 31 Persian names carry a trailing left-to-right mark. The
        query was compared raw against names that had been stripped, so a name
        copied straight out of the data did not match itself while the same
        name typed by hand did. Nothing is visible on screen either way.
        """
        for feature in self.features:
            props = feature["properties"]
            for key in ("name:en", "name", "ISO3166-2"):
                value = props.get(key)
                if not value:
                    continue
                found = rt.find_province(self.features, value)
                self.assertIsNotNone(found, "%s via %s" % (props["name:en"], key))
                self.assertEqual(found["properties"]["name:en"], props["name:en"])

    def test_persian_yeh_finds_the_province_stored_with_an_arabic_one(self):
        """Gilan is the one province OSM spells with an Arabic yeh.

        An Iranian keyboard produces the Persian yeh, so the correct word typed
        the normal way did not match, and the two spellings are the same five
        letters on screen with nothing to hint at the difference.
        """
        arabic = "\u06af\u064a\u0644\u0627\u0646"   # Arabic yeh, U+064A
        persian = "\u06af\u06cc\u0644\u0627\u0646"  # Persian yeh, U+06CC
        self.assertNotEqual(arabic, persian)
        for spelling in (arabic, persian):
            found = rt.find_province(self.features, spelling)
            self.assertIsNotNone(found, repr(spelling))
            self.assertEqual(found["properties"]["name:en"], "Gilan")

    def test_arabic_kaf_is_folded_too(self):
        """Not triggered by today's data, but the same keyboard difference and
        the next refresh of the extract could introduce it."""
        self.assertEqual(rt.normalise("\u0643"), rt.normalise("\u06a9"))

    def test_lookup_ignores_case_and_surrounding_space(self):
        for query in ("tehran", "TEHRAN", "  Tehran  ", "ir-07"):
            found = rt.find_province(self.features, query)
            self.assertIsNotNone(found, query)
            self.assertEqual(found["properties"]["name:en"], "Tehran")

    def test_unknown_name_returns_none(self):
        self.assertIsNone(rt.find_province(self.features, "Nowhere"))


class TestSampling(unittest.TestCase):
    def setUp(self):
        self.features = rt.load_provinces()

    def test_points_really_are_inside_every_province(self):
        rng = random.Random(12345)
        for feature in self.features:
            polygons = rt.as_polygons(feature["geometry"])
            for x, y in rt.random_points(feature, 12, rng):
                self.assertTrue(
                    inside_by_winding(x, y, polygons),
                    "%s got a point outside itself at %f %f"
                    % (feature["properties"]["name:en"], x, y),
                )

    def test_a_point_belongs_to_exactly_one_province(self):
        """Provinces tile the country, so a point in two of them means the
        containment test is wrong, not that the border is shared."""
        rng = random.Random(7)
        geometries = [
            (f["properties"]["name:en"], rt.as_polygons(f["geometry"]))
            for f in self.features
        ]
        for feature in self.features[:8]:
            for x, y in rt.random_points(feature, 5, rng):
                hits = [n for n, g in geometries if inside_by_winding(x, y, g)]
                self.assertEqual(hits, [feature["properties"]["name:en"]])

    def test_many_part_province_does_not_stall(self):
        """Hormozgan is 184 parts, nearly all small islands, so its overall
        bounding box is mostly sea. Sampling that box directly is what makes a
        naive implementation appear to hang."""
        feature = rt.find_province(self.features, "Hormozgan")
        self.assertEqual(len(rt.as_polygons(feature["geometry"])), 184)
        points = rt.random_points(feature, 150, random.Random(1))
        self.assertEqual(len(points), 150)

    def test_seed_makes_the_run_repeatable(self):
        feature = rt.find_province(self.features, "Tehran")
        first = rt.random_points(feature, 20, random.Random(99))
        second = rt.random_points(feature, 20, random.Random(99))
        self.assertEqual(first, second)

    def test_count_is_honoured_exactly(self):
        feature = rt.find_province(self.features, "Qom")
        for count in (1, 5, 50):
            self.assertEqual(len(rt.random_points(feature, count, random.Random(3))), count)


class TestOutput(unittest.TestCase):
    def setUp(self):
        self.features = rt.load_provinces()
        self.feature = rt.find_province(self.features, "Tehran")
        self.points = rt.random_points(self.feature, 4, random.Random(5))

    def test_wkt_is_a_multipoint_qgis_can_read(self):
        text = rt.format_wkt(self.points)
        self.assertTrue(text.startswith("MULTIPOINT ("))
        self.assertEqual(text.count(","), 3)

    def test_csv_has_a_header_and_one_row_per_point(self):
        rows = rt.format_csv(self.points).splitlines()
        self.assertEqual(rows[0], "lon,lat")
        self.assertEqual(len(rows), 5)

    def test_geojson_round_trips_and_keeps_lon_lat_order(self):
        import json

        data = json.loads(rt.format_geojson(self.points, self.feature))
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertEqual(len(data["features"]), 4)
        lon, lat = data["features"][0]["geometry"]["coordinates"]
        self.assertGreater(lon, 40)
        self.assertLess(lat, 40)


if __name__ == "__main__":
    unittest.main()
