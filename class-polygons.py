from isotiles.thecode import test
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
