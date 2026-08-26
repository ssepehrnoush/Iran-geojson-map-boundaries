# Licence of the boundary data

This repository holds two different things under two different licences.

| | Licence |
| --- | --- |
| The code (`random_tiles.py`, `test_random_tiles.py`) | MIT, see [LICENSE](LICENSE) |
| The boundary data (`ir_states_boundaries_coordinates.geojson`) | ODbL 1.0, see below |

## The data is OpenStreetMap

`ir_states_boundaries_coordinates.geojson` was obtained through Mapzen, whose
borders extracts were built from OpenStreetMap. The tags carried in the file
say so plainly: `name:en`, `boundary`, `admin_level`, `wikidata` and
`ISO3166-2` are OSM tags, not something a hand-drawn dataset would carry.

OpenStreetMap data is published under the
[Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
That licence travels with the data. It cannot be relicensed here, by this
repository or by anyone who forks it.

## What you have to do

**Attribute.** Anywhere you show or publish this data, credit
`© OpenStreetMap contributors` and link to
<https://www.openstreetmap.org/copyright>.

**Share alike.** If you publish a modified version of the data itself, or a
database derived from it, publish it under ODbL as well. Producing a map image,
a list of coordinates or an analysis from it does not put your own work under
ODbL, only the derived data does.

**Keep this notice with it.** If you redistribute the geojson, carry this file
along.

## Why this file exists

Until 2026-08-27 this repository had no licence at all. Under GitHub's terms
that means all rights reserved: the 13 people who starred it and the 3 who
forked it had, strictly speaking, no permission to use any of it. The code side
of that is now fixed with MIT. The data side was never the author's to license,
so the honest fix is to name the real licence rather than to pick a convenient
one.

If you need Iranian boundaries under different terms, take them from
[Natural Earth](https://www.naturalearthdata.com/), which is public domain.
