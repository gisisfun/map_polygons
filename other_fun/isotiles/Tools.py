from geopy.distance import distance,geodesic
import os


def next_point(coords, brng, radial):
    return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

            
def to_geojson(geo_array):
        .format(len(g_array)))
        output_geojson = FeatureCollection(g_array)
        # convert merged geojson features to geojson feature geohex_geojson
    return output_geojosn


def to_file(contents,filename):
    my_os = os.name
    if (my_os is 'posix'):
        # cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        # cmd_text = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash = '\\'
    print('writing geojson formatted hexagon dataset to file: {0}.json'.format(filename))
    myfile = open(filename
        .format(slash=slash), 'w')
        #open file for writing geojson layer in geojson format
        myfile.write(str(contents))  
        myfile.close()  # close file
