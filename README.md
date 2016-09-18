# Iran-geojson-map-boundaries
Its a simple and powerfull script that can help you generate unique points within every Iranian states as much as you want.
It contains a geojson file of Iran states boundaries downloaded from [www.Mapzen.com]

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
### Installing GDAL
Now this is gonna be a little tricky. Follow the exact structions.

 - Download the appropriate  [GDAL Binary]. After downloading install GDAL with standard settings.
 - Download  [Python Bindings] for GDAL binaries and install them.
 - # Recall that we had installed Python 2.7 earlier.

# Step 4:
We need to tell Windows system where the GDAL installations are located, so we need to add some system variables.

1. Right click on "Computer" on the desktop and go to "Properties"
2. Click on Advanced System Properties
3. Select Environment Variables.
4. Under the System variables panel, find the ‘Path’ variable, then click on Edit.
5. Go to the end of the box and copy and paste the following:

 - ;C:\Program Files (x86)\GDAL
 - *Note: For 64-bit GDAL installations you would simply remove the (x86) after "Program Files" every time.*
6. In the same System variables pane, click on “New” and then add the following in the dialogue box:

 - Variable name: GDAL_DATA
 - Variable value: C:\Program Files (x86)\GDAL\gdal-data
7. Click “OK”
8. Add one more new variable by clicking “New…”
10. Add the following in the dialogue box:

 - Variable name: GDAL_DRIVER_PATH
 - Variable value: C:\Program Files (x86)\GDAL\gdalplugins
11. Click “OK”
# Testing the GDAL installation:
1. Open the Windows command line, by going to the Start Menu -> Run ->Type in cmd and press Enter.
2. Type in gdalinfo –version
3. Press Enter.
4. If you get the following result, then congratulations your GDAL installation worked smoothly!
 - GDAL 1.11.1, released 2014/09/24

# Step 5:
Install these two packages using pip command also in cmd by typing:
 
	pip install geojson
	pip install gdal ( Just for sure )
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
[Python Bindings]: <http://download.gisinternals.com/sdk/downloads/release-1500-gdal-1-11-4-mapserver-6-4-3/GDAL-1.11.4.win32-py2.7.msi>
 [GDAL Binary]: <http://download.gisinternals.com/sdk/downloads/release-1500-gdal-1-11-4-mapserver-6-4-3/gdal-111-1500-core.msi>
