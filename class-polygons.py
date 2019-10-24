from isotiles.thecode import Tiles
from isotiles.thecode import PostProcess
import random

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

#fred = test(north = -8, south = -45, east = 168, west = 96, radial = 45, shape ='hex')
fred = Tiles()
post = PostProcess()

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

fred.to_shp_tab()

intersect_poly = fred.neighbours(hex_points)

post.ref_files()

