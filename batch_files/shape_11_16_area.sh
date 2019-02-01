ogr2ogr ../shapefiles/shape_57km_area_11_16.shp '../vrt/shape_11_16.vrt' -dialect sqlite -sql @../sql/shape_11_16_area.sql
ogr2ogr -f "CSV" ../csv/shape_57km_area_11_16.csv ../shapefiles/shape_57km_area_11_16.shp
