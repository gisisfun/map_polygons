from isotiles.tiles import Tiles
from isotiles.util import Util
#from isotiles.visual import Visual
import random
import sys
 

def hexagons(theshape,b_north, b_south, b_east, b_west, theradial):
    t = Tiles(shape = 'hex', north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)
    u = Util(shape = theshape, radial = theradial)
    u.ref_files_polygons()
    
    nb_poi_hex_array, nb_aus_hex_array = t.hexagons()
    u.to_geojson_file(nb_poi_hex_array,'aus_{fname}_layer')
    u.to_kml_file(nb_poi_hex_array,'aus_{fname}_layer')
    u.to_shp_file(nb_poi_hex_array,'aus_{fname}_layer')

    u.to_geojson_file(nb_aus_hex_array,'aus_{fname}_layer')
    u.to_kml_file(nb_aus_hex_array,'aus_{fname}_layer')
    u.to_shp_file(nb_aus_hex_array,'aus_{fname}_layer')

def boxes(shape,b_north,south,east,west,theradial):
    t = Tiles(shape = 'hex', north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)
    u = Util(shape = theshape, radial = theradial)
    u.ref_files_polygons()
    
    nb_poi_box_array, nb_aus_box_array = t.boxes()
    u.to_geojson_file(nb_poi_box_array,'aus_{fname}_layer')
    u.to_kml_file(nb_poi_box_array,'aus_{fname}_layer')
    u.to_shp_file(nb_poi_box_array,'aus_{fname}_layer')

    u.to_geojson_file(nb_aus_box_array,'aus_{fname}_layer')
    u.to_kml_file(nb_aus_box_array,'aus_{fname}_layer')
    u.to_shp_file(nb_aus_box_array,'aus_{fname}_layer')
    
    
print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:

    (shape, b_north, b_south, b_east, b_west, radial_d) =\
    ['hex', -8, -45, 169, 96, 57]
    #do_map('hex',radial_d)
    hexagons('hex',b_north, b_south, b_east, b_west, radial_d)
    #testing('hex',b_north, b_south, b_east, b_west, radial_d)

else:
    if (len(sys.argv) < 7 ):
        msg = """arguments are \nshape - hex or box \n bounding north\n
bounding south \n bounding east \n bounding west \n radial in km\n \
filename for output\n\nfor hexagon\n 
python3 polygons_new.py hex -8 -45 168 96 212\n\nfor boxes\n\
python3 polygons_new.py box -8 -45 168 96 212\n
"""
        sys.exit(msg)
    else:
        (blah, shape, b_north, b_south, b_east, b_west, radial_d) =\
        sys.argv
        shape=str(shape)
        print(shape)
        if shape == "hex":
            
            hexagons(float(b_north), float(b_south), float(b_east), \
                     west = float(b_west), radial = float(radial_d))
        else:
            if shape == "box":
                boxes(float(b_north), float(b_south), float(b_east), \
                      float(b_west), float(radial_d))
            else:
                print('shape is hex or box')

