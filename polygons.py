"""
Creates a tessellating polygon data set:
counts of Coastline (Boundary), Islands and GNAF locality (Locality)
"""
import argparse
from isotiles.tiles import Tiles
from utils import ref_files_polygons, to_geojson_file, to_kml_file, to_shp_file
#from isotiles.visual import Visual


def hexagons(bounds_north, bounds_south, bounds_east, bounds_west,
             theradial):

    """
    Hexagons specific functions to create hexagon mapping layer

    """
    theshape = 'hex'
    t_mod = Tiles(shape=theshape, north=bounds_north,
                  south=bounds_south, east=bounds_east,
                  west=bounds_west, radial=theradial)
    #u_mod = Util(shape=theshape, radial=theradial)
    ref_files_polygons('datasets',t_mod.json_files_path, t_mod.slash)
    nb_aus_hex_array = t_mod.hexagons()
    to_geojson_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                    format(theshape, theradial),'geojson', t_mod.slash)
    to_kml_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                format(theshape, theradial),\
                t_mod.kml_files_path\
                ,t_mod.slash \
                ,'Active_Fires')
    to_shp_file(nb_aus_hex_array, 'aus_{}_{}km_layer'.
                format(theshape, theradial), \
                t_mod.shape_files_path, \
                t_mod.slash)

def boxes(bounds_north, bounds_south, bounds_east, bounds_west, theradial):
    """
    Boxes specific functions to create hexagon mapping
    """
    theshape = 'box'
    t_mod = Tiles(shape=theshape, north=bounds_north,
                  south=bounds_south, east=bounds_east,
                  west=bounds_west, radial=theradial)
    print(t_mod.slash)
    #u_mod = Util(shape=theshape, radial=theradial)
    ref_files_polygons('datasets', \
                       t_mod.json_files_path, \
                       t_mod.slash)
    nb_aus_box_array = t_mod.boxes()
    to_geojson_file(nb_aus_box_array, \
                    'aus_{}_{}km_layer'.format(theshape, theradial), \
                    t_mod.geojson_files_path, \
                    t_mod.slash)
    to_kml_file(nb_aus_box_array, 'aus_{}_{}km_layer'.
                format(theshape, theradial), \
                t_mod.kml_files_path, \
                t_mod.slash, \
                'Active_Fires')
    to_shp_file(nb_aus_box_array, \
                'aus_{}_{}km_layer'.format(theshape, theradial), \
                t_mod.shape_files_path, \
                t_mod.slash)


PARSER = argparse.ArgumentParser(
        prog='polygons',
        description='''
        Creates a tessellating polygon data set:
        counts of Coastline (Boundary), Islands and GNAF locality (Locality)''')

PARSER.add_argument('-bn', '--north', default=-8,
                    help="bounds north (-90 to 90)")
PARSER.add_argument('-bs', '--south', default=-45,
                    help="bounds south (-90 to 90)")
PARSER.add_argument('-be', '--east', default=169,
                    help="bounds east (-180 to 180)")
PARSER.add_argument('-bw', '--west', default=-96,
                    help="bounds west (-180 to 180)")
PARSER.add_argument('-rl', '--radial', default=57,
                    help="radial length in km")
PARSER.add_argument('-sh', '--shape', default='hex',
                    help="shape (hex or box)")


ARGS = PARSER.parse_args()
if ARGS.shape == 'hex':
    hexagons(float(ARGS.north), float(ARGS.south), float(ARGS.east),
             float(ARGS.west), float(ARGS.radial))

if ARGS.shape == "box":
    boxes(float(ARGS.north), float(ARGS.south), float(ARGS.east),
          float(ARGS.west), float(ARGS.radial))

                