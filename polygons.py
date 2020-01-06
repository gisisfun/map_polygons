"""
Wrapper script for map_polygons

"""
import sys
from isotiles.tiles import Tiles
from isotiles.util import Util
#from isotiles.visual import Visual


def hexagons(theshape, bounds_north, bounds_south, bounds_east, bounds_west, theradial):

    """
    Hexagons specific functions to create hexagon mapping layer

    """

    t_mod = Tiles(shape=theshape, north=bounds_north,
                  south=bounds_south, east=bounds_east,
                  west=bounds_west, radial=theradial)
    u_mod = Util(shape=theshape, radial=theradial)
    u_mod.ref_files_polygons()
    nb_aus_hex_array = t_mod.hexagons()
    u_mod.to_geojson_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial))
    u_mod.to_kml_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial),'Active_Fires')
    u_mod.to_shp_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial))

def boxes(theshape, bounds_north, bounds_south, bounds_east, bounds_west, theradial):
    """
    Boxes specific functions to create hexagon mapping
    """
    t_mod = Tiles(shape=theshape, north=bounds_north,
                  south=bounds_south, east=bounds_east,
                  west=bounds_west, radial=theradial)
    u_mod = Util(shape=theshape, radial=theradial)
    u_mod.ref_files_polygons()
    nb_aus_box_array = t_mod.boxes()
    u_mod.to_geojson_file(nb_aus_box_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial))
    u_mod.to_kml_file(nb_aus_box_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial),'Active_Fires')
    u_mod.to_shp_file(nb_aus_box_array, 'aus_{}_{}km_layer'.
                          format(theshape, theradial))
        
ARGS = sys.argv
LEN_ARGS = len(ARGS)
print('Number of arguments: {0} arguments.'.format(LEN_ARGS))
print('Argument List: {0}'.format(str(ARGS)))
if LEN_ARGS == 1:
    (THE_SHAPE, BOUNDS_NORTH, BOUNDS_SOUTH, BOUNDS_EAST, BOUNDS_WEST, \
     THE_RADIAL) =\
    ['hex', -8, -45, 169, 96, 57]
    hexagons(THE_SHAPE, BOUNDS_NORTH, BOUNDS_SOUTH, BOUNDS_EAST, BOUNDS_WEST, \
          THE_RADIAL)

else:
    if LEN_ARGS < 7:
        MSG = """arguments are \nshape - hex or box \n bounding north\n
bounding south \n bounding east \n bounding west \n radial in km\n \
filename for output\n\nfor hexagon\n 
python3 polygons_new.py hex -8 -45 168 96 212\n\nfor boxes\n\
python3 polygons_new.py box -8 -45 168 96 212\n
"""
        sys.exit(MSG)
    else:
        (BLAH, THE_SHAPE, BOUNDS_NORTH, BOUNDS_SOUTH, BOUNDS_EAST, \
         BOUNDS_WEST, THE_RADIAL) = sys.argv
        SHAPE = str(THE_SHAPE)
        print(THE_SHAPE)
        if SHAPE == "hex":
            hexagons(THE_SHAPE, float(BOUNDS_NORTH), float(BOUNDS_SOUTH), \
                     float(BOUNDS_EAST), float(BOUNDS_WEST), \
                     float(THE_RADIAL))
        else:
            if SHAPE == "box":
                boxes(THE_SHAPE, float(BOUNDS_NORTH), float(BOUNDS_SOUTH), \
                      float(BOUNDS_EAST), float(BOUNDS_WEST), \
                      float(THE_RADIAL))
            else:
                print('shape is hex or box')
                