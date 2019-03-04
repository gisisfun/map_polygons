ogr2igr -f 'ESRI Shapefile' ../shapefiles/agil_4326.shp ../geojson/agil.json
ogr2ogr -t_srs 'EPSG:4823' ../shapefiles/agil_4326.shp ../shapefiles/agil.shp
ogr2ogr ../shapefiles/shape_donor_feat_57km_agil_count.shp '../vrt/shape_agil.vrt' -dialect sqlite -sql @../sql/shape_agil_count.sql
#ogr2ogr -f "CSV" ../csv/shqpe_donor_feat_75km_aust_11.csv ../shapefiles/shape_donor_feat_57km_aust_11.shp
