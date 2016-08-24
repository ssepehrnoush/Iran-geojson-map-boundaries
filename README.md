# Iran-geojson-map-boundaries
Its an simple and powerfull script that can help you generate as many as you want unique points within every iranian state
It contains an geojson file of Iran states boundaries downloaded from [www.Mapzen.com]

You can also see the map and the points graphically by using *[QGIS].
Note: QGIS is an official project of the Open Source Geospatial Foundation (OSGeo). It runs on Linux, Unix, Mac OSX, Windows and Android and supports numerous vector, raster, and database formats and functionalities.

### Prerequisites

	- Python 2.7
	- python-pip 
	- python-geojson
	- python-gdal

### Quick Start
This guide is based on *Python 2.7* on a *Windows 32/64bit*:

# Step 1:
Install  [Python 2.7] with the default options and directories.

# Step 2:
Download [get-pip] and run it through this command in command prompt
Goto the directory that contains get-pip.py using *cd* commmand then type:
 'python get-pip.py'

# Step 3:
Install these two packages using pip command also in cmd by typing:
 
	pip install geojson
	pip install gdal
# Congratulation
[Your Python Script] is ready to use.

 [Your Python Script]: <https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/blob/master/random_tiles.py>
 [ir_states_boundaries_coordinates.geojson]: <https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/blob/master/ir_states_boundaries_coordinates.geojson>
 [get-pip]: <https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/blob/master/get-pip.py>
 [Python 2.7]: <https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi>

With special thanks to:

[Sepehrnoush] , [xunilk]
[xunilk]: <http://gis.stackexchange.com/users/45066/xunilk>
[Sepehrnoush]: <https://github.com/sepehrnoush>
Source :
 - [www.Mapzen.com]
 - [www.GDAL.org]
 - [py-gdalogr-cookbook]
[www.Mapzen.com]: <https://mapzen.com/>
[py-gdalogr-cookbook]: <https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html>
[www.GDAL.org]: <http://www.gdal.org/classOGRGeometry.html#aa3d42b06ae6f7bbef6d1a2886da8d398>
