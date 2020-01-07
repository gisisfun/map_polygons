"""
Creates a png format map of an existing polygon data set
"""
import argparse
from isotiles.visual import Visual
parser = argparse.ArgumentParser()

def do_map(the_shape, the_size, the_weight):
    """
    """
    v_mod = Visual(shape=the_shape, radial=the_size, weight=the_weight)
    v_mod.map_data()
    
PARSER = argparse.ArgumentParser(
        prog='map_me',
        description='Creates a png format map of an existing polygon data set')    
    
PARSER.add_argument('-rl', '--radial', default=57, help="radial length in km")
PARSER.add_argument('-wt', '--weight', default='place', 
                    help="polygon intersection weight variable (place or area)")
PARSER.add_argument('-sh', '--shape', default='hex', help="shape (hex or box)")
        

ARGS = PARSER.parse_args()

do_map(ARGS.shape, ARGS.radial, ARGS.weight)
