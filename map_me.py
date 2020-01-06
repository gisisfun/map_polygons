"""
"""
import sys
from isotiles.visual import Visual

def do_map(the_shape, the_size, the_weight):
    """
    """
    v_mod = Visual(shape=the_shape, radial=the_size, weight=the_weight)
    v_mod.map_data()

THE_LEN = len(sys.argv)
print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if THE_LEN == 1:
    (THE_SHAPE, THE_SIZE, THE_WEIGHT) = ['hex', 57, 'place']
    do_map(THE_SHAPE, THE_SIZE, THE_WEIGHT)
else:
    if THE_LEN < 4:
        sys.exit("""arguments are \nshape - hex or box \n\
size (in km)\nweight - area or place \n\
\npython3 map_me.py hex 57 place\n""")
    else:
        (THE_SCRIPT, THE_SHAPE, THE_SIZE, THE_WEIGHT) = sys.argv
        do_map(THE_SHAPE, THE_SIZE, THE_WEIGHT)
