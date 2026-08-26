#!/usr/bin/env python3
"""Generate random points that fall inside a given Iranian province.

Reads ir_states_boundaries_coordinates.geojson (31 provinces, OpenStreetMap
boundaries) and returns points guaranteed to be inside the one you name.

No third-party packages. The 2016 version of this script needed GDAL, which on
Windows meant two installers, three environment variables and a Python 2 build
that no longer exists. Point-in-polygon over a few thousand vertices is about
twenty lines, so the dependency bought nothing and cost everyone the setup.

    python random_tiles.py --list
    python random_tiles.py Tehran 100
    python random_tiles.py IR-07 100 --format geojson
"""

import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "ir_states_boundaries_coordinates.geojson")


def load_provinces(path=DATA):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data["features"]


# Invisible bidi and joining controls. Written as escapes on purpose: as
# literal characters they render as nothing at all, so the line would look
# like an empty string to every reviewer and any one of them could go
# missing without anyone seeing it.
BIDI_MARKS = (
    "\u200e"  # LEFT-TO-RIGHT MARK, the one OSM leaves on 23 province names
    "\u200f"  # RIGHT-TO-LEFT MARK
    "\u202a"  # LEFT-TO-RIGHT EMBEDDING
    "\u202b"  # RIGHT-TO-LEFT EMBEDDING
    "\u202c"  # POP DIRECTIONAL FORMATTING
    "\u202d"  # LEFT-TO-RIGHT OVERRIDE
    "\u202e"  # RIGHT-TO-LEFT OVERRIDE
    "\u200c"  # ZERO WIDTH NON-JOINER, the Persian half-space
    "\u200d"  # ZERO WIDTH JOINER
)


# Arabic letters that are visually identical to the Persian ones an Iranian
# keyboard produces. Gilan is stored with the Arabic yeh, so the same word typed
# with the Persian yeh returned "no province matched" and gave no way to see
# why: on screen the two spellings are the same five letters.
#
# Codepoints, not characters. A reviewer cannot tell U+064A from U+06CC by
# looking, and an editor that helpfully normalises Arabic script would rewrite
# one side of this table and quietly turn it into a no-op.
LOOKALIKE = {
    0x064A: chr(0x06CC),  # ARABIC YEH        -> FARSI YEH
    0x0643: chr(0x06A9),  # ARABIC KAF        -> KEHEH
    0x0629: chr(0x0647),  # ARABIC TEH MARBUTA -> HEH
}


def normalise(value):
    """Fold a name to the form used for comparison.

    Two invisible differences are folded away here. OSM stores the Persian name
    with a trailing left-to-right mark on 23 of the 31 provinces, and stores
    Gilan with an Arabic yeh rather than a Persian one. Neither is visible in a
    terminal or an editor, so both produce a name that looks exactly right and
    does not match.

    Both the stored names and the user's argument go through this function.
    That symmetry is the fix: normalising only one side is what made a name
    copied out of the data fail while the same name typed by hand worked.
    """
    return value.strip().strip(BIDI_MARKS).strip().translate(LOOKALIKE).lower()


def province_names(feature):
    """Every name this province answers to, normalised."""
    props = feature["properties"]
    raw = [props.get("name:en"), props.get("name"), props.get("ISO3166-2")]
    return [normalise(value) for value in raw if value]


def find_province(features, query):
    wanted = normalise(query)
    for feature in features:
        if wanted in province_names(feature):
            return feature
    return None


def as_polygons(geometry):
    """Normalise Polygon and MultiPolygon to one list of polygons.

    A polygon is [exterior_ring, *hole_rings]. The shipped data has no holes,
    but honouring them costs one loop and means a refreshed extract with an
    enclave in it cannot start silently placing points inside the hole.
    """
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"]]
    if geometry["type"] == "MultiPolygon":
        return geometry["coordinates"]
    raise ValueError("unsupported geometry type: %s" % geometry["type"])


def ring_area(ring):
    """Unsigned shoelace area in squared degrees.

    Only ever used to compare one part against another, so leaving it in
    degrees rather than projecting to metres is fine and keeps this dependency
    free. It does mean a part near the top of the country is weighted very
    slightly differently than one in the south.
    """
    total = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def polygon_area(polygon):
    area = ring_area(polygon[0])
    for hole in polygon[1:]:
        area -= ring_area(hole)
    return max(area, 0.0)


def bounds(ring):
    xs = [point[0] for point in ring]
    ys = [point[1] for point in ring]
    return min(xs), min(ys), max(xs), max(ys)


def point_in_ring(x, y, ring):
    """Ray casting: count crossings of a ray going right from (x, y)."""
    inside = False
    count = len(ring)
    j = count - 1
    for i in range(count):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            slope = (xj - xi) / (yj - yi)
            if x < xi + (y - yi) * slope:
                inside = not inside
        j = i
    return inside


def point_in_polygon(x, y, polygon):
    if not point_in_ring(x, y, polygon[0]):
        return False
    for hole in polygon[1:]:
        if point_in_ring(x, y, hole):
            return False
    return True


def random_points(feature, count, rng):
    """Sample points uniformly by area across every part of the province.

    Rejection sampling inside the bounding box of the whole geometry is the
    obvious approach and it is unusable here. Hormozgan is 184 separate parts,
    most of them small islands in the Persian Gulf, so its overall box is
    mostly sea and almost every candidate is thrown away. Picking a part first,
    weighted by its area, keeps the hit rate high no matter how the province is
    shaped, and weighting by area is also what makes the result uniform rather
    than biased towards the small islands.
    """
    polygons = as_polygons(feature["geometry"])
    weights = [polygon_area(polygon) for polygon in polygons]
    total = sum(weights)
    if total <= 0:
        raise ValueError("province has no area")

    boxes = [bounds(polygon[0]) for polygon in polygons]

    cumulative = []
    running = 0.0
    for weight in weights:
        running += weight
        cumulative.append(running)

    def pick_polygon():
        target = rng.uniform(0, total)
        for index, edge in enumerate(cumulative):
            if target <= edge:
                return index
        return len(polygons) - 1

    points = []
    # A part can be far thinner than its box, so allow generous retries before
    # giving up. Without a ceiling a degenerate ring would hang here forever.
    budget = count * 10000
    while len(points) < count:
        budget -= 1
        if budget <= 0:
            raise RuntimeError(
                "gave up after too many attempts, the geometry may be degenerate"
            )
        index = pick_polygon()
        xmin, ymin, xmax, ymax = boxes[index]
        x = rng.uniform(xmin, xmax)
        y = rng.uniform(ymin, ymax)
        if point_in_polygon(x, y, polygons[index]):
            points.append((x, y))
    return points


def format_wkt(points):
    inner = ", ".join("%.6f %.6f" % (x, y) for x, y in points)
    return "MULTIPOINT (%s)" % inner


def format_csv(points):
    lines = ["lon,lat"]
    lines.extend("%.6f,%.6f" % (x, y) for x, y in points)
    return "\n".join(lines)


def format_geojson(points, feature):
    name = feature["properties"].get("name:en")
    collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(x, 6), round(y, 6)]},
                "properties": {"province": name},
            }
            for x, y in points
        ],
    }
    return json.dumps(collection, ensure_ascii=False, indent=2)


def print_list(features):
    rows = sorted(features, key=lambda f: f["properties"].get("name:en") or "")
    print("%-28s %-10s %s" % ("NAME", "ISO", "PARTS"))
    for feature in rows:
        props = feature["properties"]
        parts = len(as_polygons(feature["geometry"]))
        print(
            "%-28s %-10s %d"
            % (props.get("name:en"), props.get("ISO3166-2") or "", parts)
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Random points inside an Iranian province.",
        epilog="Province may be the English name, the Persian name, "
        "or the ISO 3166-2 code. Run --list to see them all.",
    )
    parser.add_argument("province", nargs="?", help="e.g. Tehran, \u062a\u0647\u0631\u0627\u0646, IR-07")
    parser.add_argument("count", nargs="?", type=int, default=10,
                        help="how many points (default 10)")
    parser.add_argument("--format", choices=["wkt", "geojson", "csv"], default="wkt",
                        help="wkt pastes straight into QGIS (default)")
    parser.add_argument("--seed", type=int,
                        help="fix the seed to get the same points again")
    parser.add_argument("--list", action="store_true",
                        help="list the provinces and exit")
    parser.add_argument("--data", default=DATA, help="path to the geojson file")
    args = parser.parse_args(argv)

    # Persian province names cannot survive the Windows console default.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        features = load_provinces(args.data)
    except FileNotFoundError:
        parser.error("data file not found: %s" % args.data)

    if args.list:
        print_list(features)
        return 0

    if not args.province:
        parser.error("name a province, or pass --list to see them")

    if args.count < 1:
        parser.error("count must be at least 1")

    feature = find_province(features, args.province)
    if feature is None:
        parser.error(
            "no province matched %r. Run --list to see the accepted names."
            % args.province
        )

    rng = random.Random(args.seed)
    points = random_points(feature, args.count, rng)

    if args.format == "wkt":
        print(format_wkt(points))
    elif args.format == "csv":
        print(format_csv(points))
    else:
        print(format_geojson(points, feature))
    return 0


if __name__ == "__main__":
    sys.exit(main())
