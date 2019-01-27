ogr2ogr ../shapefiles/feat_57km_11_place_count.shp '../vrt/shape_place.vrt' -dialect sqlite -sql @../sql/feat_aust_11_places.sql
ogr2ogr -f "CSV" ../csv/feat_57km_11_place_count.csv ../shapefiles/feat_57km_11_place_count.shp
