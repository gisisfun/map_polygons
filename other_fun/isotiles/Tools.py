from geopy.distance import distance,geodesic
import os
from geojson import FeatureCollection, Polygon, Feature

def next_point(coords, brng, radial):
    return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

    
def to_geojson_FeatureCollection(GeoArray):
    return FeatureCollection(GeoArray)


def to_geojson_Polygon(PolyCoords):
    return Polygon(PolyCoords)


def to_geojson_Feature(PolyCoords,PolyDict):
    return Feature(geometry = PolyCoords, properties = PolyDict)


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
        
