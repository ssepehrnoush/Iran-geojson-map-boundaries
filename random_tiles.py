import json
import geojson
import random
from osgeo import ogr


def main():
    with open('ir_states_boundaries_coordinates.geojson') as f:
        data = json.load(f)
    # open geojson source file as an object
    print("\n\nName your state from this list\n\n")
    for feature in data['features']:  # print a list of valid state names
        print(feature['properties']['name:en'])
    state_name = raw_input("\n")
    user_num = raw_input("\nHow many points do you need at the moment\n\n")
    try:
        user_num = int(user_num)
    except:
        main()  # check the user input to be an integer

    for feature in data['features']:
        # read every feature elements 1 by 1 which in this case is every state
        if feature['properties']['name:en'] == state_name:

            geom = feature['geometry']
            # read the boundaries of that specific state and save it into a var
            geom = json.dumps(geom)
            # convert it to a string
            polygon = ogr.CreateGeometryFromJson(geom)
            # create geometry polygon from geojson data
            env = polygon.GetEnvelope()
            xmin, ymin, xmax, ymax = env[0], env[2], env[1], env[3]
# computes and returns the bounding envelope in the passed psEnvelope structure
            counter = 0
            multipoint = ogr.Geometry(ogr.wkbMultiPoint)
            # create a multipoint
            user_num = int(user_num)
            for i in range(user_num):
                while counter < user_num:

                    point = ogr.Geometry(ogr.wkbPoint)
                    # it creates a point in memory that we can give it value
                    point.AddPoint(random.uniform(xmin, xmax),
                                   random.uniform(ymin, ymax))
                    # choose a random point within a sqare around the state
                    if point.Within(polygon):
                        # check if its inside the state boundaries
                        multipoint.AddGeometry(point)
# add it if it fits
                        counter += 1

            print(multipoint.ExportToWkt())
# print the WKT format so it can be used in QGIS
            raise SystemExit
    main()
main()
