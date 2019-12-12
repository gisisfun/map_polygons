import sys
from isotiles.visual import Visual

def do_map(theshape,theradial,theweight):
    v = Visual(shape = theshape, radial = theradial, weight= theweight)
    v.map_data()
   
print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (shape, size, weight) = ['hex',57,'place']
    do_map(shape, size, weight )
else:
    if (len(sys.argv) <4 ):
        sys.exit("arguments are \nshape - hex or box \n size (in km)\nweight - area or place \n \npython3 map_me.py hex 57\n")
    else:
        (blah,shape,size) = sys.argv
        do_map(shape, size)
    



