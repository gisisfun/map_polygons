from isotiles.thecode import test
#fred = test(north = -8, south = -45, east = 168, west = 96, radial = 45, shape ='hex')
fred = test()

print(fred.params())

hors = fred.horizontal()

verts = fred.vertical()

intersects = fred.intersections(hors,verts)

(hexagon_array,hex_points) = fred.hex_array(intersects,len(hors),len(verts))

gj_hexagon = fred.to_geojson(hexagon_array)

fred.to_file(gj_hexagon)

fred.to_shp_tab()

fred.intersecting(hex_points)


