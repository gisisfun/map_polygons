from isotiles.util_ import from_yaml, \
     to_yaml, from_geojson_file, \
     to_geojson_file, to_shp_file, \
     from_shp_file, to_kml_file

print(from_yaml('hello: world'))
json_text = from_yaml('hello: world')
print(to_yaml(json_text))

g_data = from_geojson_file('aus_hex_57km_layer')

print(len(g_data))

to_geojson_file(g_data,'test')

to_shp_file(g_data,'test_shape')
s_data = from_shp_file('test_shape')

print(len(s_data))

to_kml_file(g_data,'kml_test','Locality')
