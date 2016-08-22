import json
import geojson
import random
from osgeo import ogr


def my_main():
    #
    with open('Source\ir_states_boundaries_coordinates.geojson') as f:
        data = json.load(f)

    print("\n\nName your state from this list\n\n")
    for feature in data['features']:
        print(feature['properties']['name:en'])
    state_name = raw_input("\n")
    user_num = raw_input("\nHow many points do you need at the moment\n\n")

    for feature in data['features']:


        if feature['properties']['name:en'] == state_name:

            geom = feature['geometry']
            geom = json.dumps(geom)
            polygon = ogr.CreateGeometryFromJson(geom)

    env = polygon.GetEnvelope()
    xmin, ymin, xmax, ymax = env[0],env[2],env[1],env[3]

    num_points = user_num

    counter = 0

    multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    num_points = int(num_points)
    for i in range(num_points):
        while counter < num_points:

            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(random.uniform(xmin, xmax),
                           random.uniform(ymin, ymax))

            if point.Within(polygon):

                multipoint.AddGeometry(point)

                counter += 1

    print(multipoint.ExportToWkt())
if __name__=='__main__':
    try:
        my_main()
    except:
        my_main()