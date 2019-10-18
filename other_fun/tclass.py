from testclass.thecode import test
#fred = test(north = -8, south = -45, east = 168, west = 96, radial = 45, shape ='hex')
fred = test()

print(fred.params())

hors = fred.horizontal()

verts = fred.vertical()

intersects = fred.intersections(hors,verts)

(hexagon_array,point_list) = fred.hex_array(intersects,len(hors),len(verts))

gj_hexagon = fred.to_geojson(hexagon_array)

prompt = 'writing geojson formatted hexagon dataset to file: hex_57km_layer.json'
path = 'geojson/hex_57km_layer.json'
fred.to_file(prompt,gj_hexagon,path)
fred.to_shp_tab()
fred.intersecting(point_list)


