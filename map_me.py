"""
"""
import argparse
from isotiles.visual import Visual
parser = argparse.ArgumentParser()

def do_map(the_shape, the_size, the_weight):
    """
    """
    v_mod = Visual(shape=the_shape, radial=the_size, weight=the_weight)
    v_mod.map_data()
    
    
parser.add_argument('-rl', '--radial', default=57, help="radial length in km")
parser.add_argument('-wt', '--weight', default='place', 
                    help="polygon intersection weight variable (place or area)")
parser.add_argument('-sh', '--shape', default='hex', help="shape (hex or box)")
        

args = parser.parse_args()

do_map(args.shape, args.radial, args.weight)
