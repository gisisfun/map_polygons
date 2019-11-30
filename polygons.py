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
    t = Tiles(shape = theshape, north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)

    print(t.params())

    hors = t.horizontal()

    verts = t.vertical()

    intersects = t.intersections(hors,verts)

    hex_array = t.hex_array(intersects,len(hors),len(verts))

    poi_hex_array = t.add_poly_poi(hex_array)
    #poi_hex_array = t.from_geojson_file('{fname}_layer')
    (odd,even) = t.column_counts(poi_hex_array)
    nb_hex_array = t.update_neighbours(poi_hex_array,odd,even)
    t.to_geojson_file(nb_hex_array,'{fname}_layer')
    t.to_kml_file(nb_hex_array,'{fname}_layer')
    t.to_shp_file(nb_hex_array,'{fname}_layer')
    
    cent_hex_array = t.add_poly_cent(nb_hex_array)
    
    aus_hex_array = t.aus_poly_intersect(cent_hex_array)
    #aus_hex_array = t.from_geojson_file('aus_{fname}_layer')
    t.to_geojson_file(aus_hex_array,'aus_{fname}_layer')
    t.to_kml_file(aus_hex_array,'aus_{fname}_layer')
    t.to_shp_file(aus_hex_array,'aus_{fname}_layer')

def boxes(shape,b_north,south,east,west,theradial):
    t = Tiles(shape = 'box',north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)

    print(t.params())

    hors = t.horizontal()

    verts = t.vertical()

    intersects = t.intersections(hors,verts)

    box_array = t.box_array(intersects,len(hors),len(verts))
    
    poi_box_array = t.add_poly_poi(box_array)

    (odd,even) = t.column_counts(poi_box_array)
    nb_box_array = t.update_neighbours(poi_box_array,odd,even)
    t.to_geojson_file(nb_box_array,'{fname}_layer')
    t.to_kml_file(nb_box_array,'{fname}_layer')
    t.to_shp_file(nb_box_array,'{fname}_layer')
    
    cent_box_array = t.add_poly_cent(nb_box_array)
    
    aus_box_array = t.aus_poly_intersect(cent_box_array)
    #aus_hex_array = t.from_geojson_file('aus_{fname}_layer')
    t.to_geojson_file(aus_box_array,'aus_{fname}_layer')
    t.to_kml_file(aus_box_array,'aus_{fname}_layer')
    t.to_shp_file(aus_box_array,'aus_{fname}_layer')
    
print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:

    (shape, b_north, b_south, b_east, b_west, radial_d) =\
    ['hex', -8, -45, 169, 96, 57]
    #do_map('hex',radial_d)
    hexagons('hex',b_north, b_south, b_east, b_west, radial_d)
    #testing('hex',b_north, b_south, b_east, b_west, radial_d)

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
            
            hexagons(float(b_north), float(b_south), float(b_east), \
                     west = float(b_west), radial = float(radial_d))
        else:
            if shape == "box":
                boxes(float(b_north), float(b_south), float(b_east), \
                      float(b_west), float(radial_d))
            else:
                print('shape is hex or box')

