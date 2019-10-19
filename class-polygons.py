from isotiles.thecode import test

def random_points(bounds_n,bounds_s,bounds_e,bounds_w,numpoints):
        
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
        
    print(layer_json)
    return coord_list 

#fred = test(north = -8, south = -45, east = 168, west = 96, radial = 45, shape ='hex')
fred = test()

print(fred.params())

hors = fred.horizontal()

verts = fred.vertical()

intersects = fred.intersections(hors,verts)

hexagon_array = fred.hex_array(intersects,len(hors),len(verts))
hex_points = fred.points_and_polygons(hexagon_array)

gj_hexagon = fred.to_geojson(hexagon_array)

fred.to_file(gj_hexagon)

fred.to_shp_tab()

intersect_poly = fred.intersecting(hex_points)

fred.ref_files()
