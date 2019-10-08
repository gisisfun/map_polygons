from geopy.distance import distance,geodesic
import os
from geojson import FeatureCollection, Polygon
def next_point(coords, brng, radial):
    return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

    
def to_geojson(geo_array):
    output_geojson = FeatureCollection(geo_array)
    # convert merged geojson features to geojson feature geohex_geojson
    return output_geojosn


def to_file(prompt,contents,filename):
    my_os = os.name
    if (my_os is 'posix'):
        slash = '/'
    else:
        slash = '\\'
    print(prompt,filename)
    myfile = open(filename.format(slash=slash), 'w')
    #open file for writing
    myfile.write(str(contents))  
    myfile.close()  # close file
        
