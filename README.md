# Iran-geojson-map-boundaries
این برنامه شامل دیتا بیسی از اطلاهات مرزبندی شده ی نقشه ی استانهای ایران است که میتوانید با نرم افزار 
# QGIS
آنرا باز کنید و به صورت یک نقشه ی جغرافیایی مشاهده و ادیت کنید
همچنین بوسیله ی اسکریپت پایتون موجود در فایل ها میتوانید به هر تعداد نقطه با طول و عرض جغرافیایی به دقت 15 رقم اعشار در هر استان به صورت تصادفی تولید کنید

### Prerequisites

	- QGIS
	- Python 2.7
	- GDAL Module
	- python-pip
	- python-geojson

### Quick Start
This guide is based on *Python 2.7 - QGIS Desktop 2.14.5* on an *Windows 32/64bit*:
# Step 1:
Download one of * [QGIS 2.14.5 32bit] / * [QGIS 2.14.5 64bit] and install it with the default options.
Install  [Python 2.7] also with the default options and directories.
# Step 2:
### Installing GDAL
Now this is gonna be a little tricky. Follow the exact structions.

 - Download the appropriate  [GDAL Binary]. After downloading install GDAL with standard settings.
 - Download  [Python Bindings] for GDAL binaries and install them.
 - # Recall that we had installed Python 2.7 earlier.

# Step 3:
We need to tell Windows system where the GDAL installations are located, so we need to add some system variables.

1. Right click on "Computer" on the desktop and go to "Properties"
2. Click on Advanced System Properties
3. Select Environment Variables.
4. Under the System variables panel, find the ‘Path’ variable, then click on Edit.
5. Go to the end of the box and copy and paste the following:

 - ;C:\Program Files (x86)\GDAL
Note: For 64-bit GDAL installations you would simply remove the (x86) after Program Files.
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

# Step 4:
Installing QuickWKT plugin for QGIS for displaying the WKT multi point format printed at the Python Console of QGIS
 - Run QGIS Desktop
 - Goto Plugins menu
 - Manage and Install Plugins...
 - It should take a few seconds
 - Scroll down and find QuickWKT 
 - On the right side click on Install plugin
 - After that the program is ready to use for our purpose, You just have to drag and drop [ir_states_boundaries_coordinates.geojson] into the software and the map will shown itself.
 
### Generating Random points within any state
 - Run cmd as administrator and goto your downloaded * [Python-pip] directory.
 - type python python-pip.py
 Note: Remember you must have saved python-pip as py file and it must be $/python-pip.py
 - Now you can geojson through pip, Type:
 - pip install geojson
 
# Congratulation
[Your Random Points Generator Python Script] is ready to use.
You can Copy the result of the script (the codes that it gives you as many as you want) and paste it in QGIS Desktop to see them on the map, 
Remember draging and droping our geojson source into QGIS ? after that in the middle of the left section you see the geojson file name as *ir_states_boundaries_coordinates OGRGeoJSON MultiPolygon*
On the top right you will see the QuickWKT plugin icon, Click on it and paste your result from *Random_tiles.py* .
Its Done !




 [Your Random Points Generator Python Script]: <https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/blob/master/random_tiles.py>
 [ir_states_boundaries_coordinates.geojson]: <https://github.com/ssepehrnoush/Iran-geojson-map-boundaries/blob/master/Source/ir_states_boundaries_coordinates.geojson>
 [Python Bindings]: <http://download.gisinternals.com/sdk/downloads/release-1500-gdal-1-11-4-mapserver-6-4-3/GDAL-1.11.4.win32-py2.7.msi>
 [GDAL Binary]: <http://download.gisinternals.com/sdk/downloads/release-1500-gdal-1-11-4-mapserver-6-4-3/gdal-111-1500-core.msi>
 [Python 2.7]: <https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi>
 [QGIS 2.14.5 32bit]: <http://qgis.org/downloads/QGIS-OSGeo4W-2.14.5-1-Setup-x86.exe>
 [QGIS 2.14.5 64bit]: <http://qgis.org/downloads/QGIS-OSGeo4W-2.14.5-1-Setup-x86_64.exe>
