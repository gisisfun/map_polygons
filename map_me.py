import sys
from isotiles.thecode import Visual

def do_map(theshape,theradial):
    v = Visual(shape = theshape, radial = theradial)
    v.map_data()
   
print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (shape, size) = ['hex',57]
    do_map(shape, size)
else:
    if (len(sys.argv) <3 ):
        sys.exit("arguments are \nshape - hex or box \n size (in km) \n \npython3 map_me.py hex 57\n")
    else:
        (blah,shape,size) = sys.argv
        do_map(shape, size)
    



