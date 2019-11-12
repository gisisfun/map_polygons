from isotiles.tiles import Tiles
#from isotiles.visual import Visual
import random
import sys

def random_points(bounds_n,bounds_s,bounds_e,bounds_w,numpoints):
    """
    Create an array of random points
    """
    
    ns_range = bounds_n - bounds_s
    ew_range = bounds_e - bounds_w
    coord_list=[]

    x_coords_list=[]
    y_coords_list=[]
    
    for i in range(0,numpoints):
        y_coord = bounds_s+random.randrange(0, ns_range*10000)/10000
        x_coord = bounds_w+random.randrange(0, ew_range*10000)/10000
        coord=[x_coord,y_coord]
        coord_list.append(coord)
        x_coords_list.append(x_coord)
        y_coords_list.append(y_coord)
        
        #print(layer_json)
        return coord_list 

def hexagons(theshape,b_north, b_south, b_east, b_west, theradial):
    fred = Tiles(shape = theshape, north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)

    print(fred.params())

    hors = fred.horizontal()

    verts = fred.vertical()

    intersects = fred.intersections(hors,verts)

    hexagon_array = fred.hex_array(intersects,len(hors),len(verts))
    hex_points = fred.points_and_polygons(hexagon_array)

    points = random_points(-8, -45, 168, 96,10)

    new_hex_array = fred.points_in_polygon(hexagon_array,points,'Test')

    gj_hexagon = fred.to_geojson(new_hex_array)

    fred.geojson_to_file(gj_hexagon)

    fred.to_shp_file(new_hex_array)

    intersect_poly = fred.neighbours(hex_points)



def boxes(shape,b_north,south,east,west,theradial):
    fred = Tiles(shape = 'box',north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)
    post = PostProcess()

    print(fred.params())

    hors = fred.horizontal()

    verts = fred.vertical()

    intersects = fred.intersections(hors,verts)

    box_array = fred.box_array(intersects,len(hors),len(verts))
    box_points = fred.points_and_polygons(box_array)

    points = random_points(-8, -45, 168, 96,10)

    new_box_array = fred.points_in_polygon(box_array,points,'Test')

    gj_box = fred.to_geojson(new_box_array)

    fred.geojson_to_file(gj_box)

    fred.to_shp_file(new_hex_array)

    intersect_poly = fred.neighbours(box_points)

    


print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:

    (shape, b_north, b_south, b_east, b_west, radial_d) =\
    ['hex', -8, -45, 168, 96, 57]
    #do_map('hex',radial_d)
    hexagons('hex',b_north, b_south, b_east, b_west, radial_d)
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
            
            fred.hexagons(float(b_north), float(b_south), float(b_east), \
                     west = float(b_west), radial = float(radial_d))
        else:
            if shape == "box":
                boxes(float(b_north), float(b_south), float(b_east), \
                      float(b_west), float(radial_d))
            else:
                print('shape is hex or box')
