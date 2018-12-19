ogr2ogr ../shapefiles/aust_hex_shape_57km.shp '../vrt/aust_shape.vrt' -dialect sqlite -sql @../sql/aust_shape.sql
ogr2ogr -f "CSV" ../csv/aust_hex_shape_57km.csv ../shapefiles/aust_hex_shape_57km.shp
