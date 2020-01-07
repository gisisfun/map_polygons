"""
Wrapper script for map_polygons

"""
import argparse
import sys
from isotiles.tiles import Tiles
from isotiles.util import Util
#from isotiles.visual import Visual
parser = argparse.ArgumentParser()

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

parser.add_argument('-bn', '--north', default=-8, 
                    help="bounds north (-90 to 90)")
parser.add_argument('-bs', '--south', default=-45, 
                    help="bounds south (-90 to 90)")
parser.add_argument('-be', '--east', default=169, 
                    help="bounds east (-180 to 180)")
parser.add_argument('-bw', '--west', default=-96, 
                    help="bounds west (-180 to 180)")
parser.add_argument('-rl', '--radial', default=57, 
                    help="radial length in km")
parser.add_argument('-sh', '--shape', default='hex', 
                    help="shape (hex or box)")
        

args = parser.parse_args()
if args.shape == 'hex':
    hexagons(args.shape, float(args.north), float(args.south), float(args.east),
             float(args.west), float(args.radial))
       
if args.shape == "box":
    boxes(args.shape, float(args.north), float(args.south), float(args.east),
             float(args.west), float(args.radial))
else:
    print('shape is hex or box')
                