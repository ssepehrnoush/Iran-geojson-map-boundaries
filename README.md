# Iran GeoJSON province boundaries

[![ci](https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/actions/workflows/ci.yml/badge.svg)](https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/actions/workflows/ci.yml)
[![code MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![data ODbL](https://img.shields.io/badge/data-ODbL%201.0-orange.svg)](DATA-LICENSE.md)
[![python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)](https://www.python.org/)

Boundaries for all **31 provinces of Iran** as a single GeoJSON file, plus a
small script that returns random coordinates guaranteed to fall inside any
province you name.

```bash
python random_tiles.py Tehran 100
python random_tiles.py IR-23 50 --format geojson
python random_tiles.py تهران 10 --format csv
```

No packages to install. Python 3.9 or newer, standard library only.

## Install

There is nothing to install, and no package to add to a requirements file.

```bash
git clone https://github.com/ssepehrnoush/Iran-geojson-map-boundaries.git
cd Iran-geojson-map-boundaries
python random_tiles.py --list
```

If you only want the boundaries and not the script, take the one file:

```bash
curl -O https://raw.githubusercontent.com/ssepehrnoush/Iran-geojson-map-boundaries/master/ir_states_boundaries_coordinates.geojson
```

## The data

`ir_states_boundaries_coordinates.geojson` is a `FeatureCollection` of 31
features. Every feature is a `MultiPolygon` in WGS 84 (`lon, lat`) and carries
the OpenStreetMap tags it was extracted with, including `name`, `name:en`,
`ISO3166-2`, `wikidata` and `admin_level`.

Most provinces are a single ring. The ones with islands and river deltas are
not: Hormozgan is 184 separate parts, Khuzestan 20, Bushehr 5, Mazandaran 2.
Anything consuming this file has to handle `MultiPolygon`, not just `Polygon`.

### Provinces

| ISO 3166-2 | Name | نام | Parts |
| --- | --- | --- | --- |
| `IR-01` | East Azerbaijan | آذربایجان شرقی | 1 |
| `IR-02` | West Azerbaijan | آذربایجان غربی | 1 |
| `IR-03` | Ardabil | اردبیل | 1 |
| `IR-04` | Isfahan | اصفهان | 1 |
| `IR-05` | Ilam | ایلام | 1 |
| `IR-06` | Bushehr | بوشهر | 5 |
| `IR-07` | Tehran | تهران | 1 |
| `IR-08` | Chaharmahal and Bakhtiari | چهارمحال و بختیاری | 1 |
| `IR-09` | Alborz | البرز | 1 |
| `IR-10` | Khuzestan | خوزستان | 20 |
| `IR-11` | Zanjan | زنجان | 1 |
| `IR-12` | Semnan | سمنان | 1 |
| `IR-13` | Sistan and Baluchestan | سیستان و بلوچستان | 1 |
| `IR-14` | Fars | فارس | 1 |
| `IR-15` | Kerman | کرمان | 1 |
| `IR-16` | Kurdistan | کردستان | 1 |
| `IR-17` | Kermanshah | کرمانشاه | 1 |
| `IR-18` | Kohgiluyeh and Boyer-Ahmad | کهگیلویه و بویر احمد | 1 |
| `IR-19` | Gilan | گيلان | 1 |
| `IR-20` | Lorestan | لرستان | 1 |
| `IR-21` | Mazandaran | مازندران | 2 |
| `IR-22` | Markazi | مرکزی | 1 |
| `IR-23` | Hormozgan | هرمزگان | 184 |
| `IR-24` | Hamadan | همدان | 1 |
| `IR-25` | Yazd | یزد | 1 |
| `IR-26` | Qom | قم | 1 |
| `IR-27` | Golestan | گلستان | 1 |
| `IR-28` | Qazvin | قزوین | 1 |
| `IR-29` | South Khorasan | خراسان جنوبی | 1 |
| `IR-30` | Razavi Khorasan | خراسان رضوی | 1 |
| `IR-31` | North Khorasan | خراسان شمالی | 1 |
## Random points inside a province

The original use for this data: generate sample coordinates that land inside a
given province and nowhere else, for seeding test data, distributing markers,
or picking survey locations.

```
python random_tiles.py --list                    list every province and its code
python random_tiles.py Tehran 100                100 points, WKT for QGIS
python random_tiles.py Fars 50 --format csv      lon,lat rows
python random_tiles.py IR-23 20 --format geojson a FeatureCollection
python random_tiles.py Qom 10 --seed 42          same 10 points every run
```

A province can be given by its English name, its Persian name, or its ISO
3166-2 code, in any case.

Points are spread uniformly by area across every part of the province, which
matters more than it sounds. Sampling the bounding box of Hormozgan and
throwing away misses is the obvious approach and it barely terminates, because
that box is mostly the Persian Gulf. Picking a part first, weighted by its
area, keeps it fast and stops the small islands from being over-represented.

To see the result on a map, paste the WKT output into QGIS with
*Layer > Add Layer > Add Delimited Text Layer*, or open the GeoJSON output
directly.

## Tests

```bash
python -m unittest
```

14 tests, no dependencies. Containment is checked with a winding number
implementation rather than the ray casting the script uses, so a test passing
means two different algorithms agree, not that the code agrees with itself.

## Licence

The code is MIT. **The data is not.**

`ir_states_boundaries_coordinates.geojson` came from OpenStreetMap by way of
Mapzen and stays under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
Using it means crediting `© OpenStreetMap contributors` and linking to
<https://www.openstreetmap.org/copyright>. Full terms and what share-alike
does and does not cover: [DATA-LICENSE.md](DATA-LICENSE.md).

If you need Iranian boundaries under looser terms, [Natural Earth](https://www.naturalearthdata.com/)
is public domain.

## مرزهای استان‌های ایران

مختصات جغرافیایی مرزهای هر ۳۱ استان ایران در یک فایل GeoJSON، به‌همراه اسکریپتی
که هر تعداد نقطهٔ تصادفی داخل استان دلخواه تولید می‌کند. بدون هیچ وابستگی، فقط
پایتون ۳.

نام استان را می‌شود انگلیسی، فارسی، یا با کد ISO داد:

```bash
python random_tiles.py تهران 100
```

داده از OpenStreetMap گرفته شده و تحت ODbL است، پس هر جا استفاده شد باید
`© OpenStreetMap contributors` ذکر شود.

## History

Written in 2016 against Python 2.7 and GDAL, which meant two Windows
installers, three environment variables and a Python build that no longer
exists. Rewritten in 2026 to need nothing but the standard library. The data
file is unchanged.

Thanks to [xunilk](http://gis.stackexchange.com/users/45066/xunilk) for the
original point-in-polygon approach, and to
[Mapzen](https://en.wikipedia.org/wiki/Mapzen) for the extract.
