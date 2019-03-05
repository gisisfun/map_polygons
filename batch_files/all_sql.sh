#aust_shape
#ogr2ogr ../shapefiles/aust_hex_shape_57km.shp '../vrt/aust_shape.vrt' -dialect sqlite -sql @../sql/aust_shape.sql
#ogr2ogr -f "CSV" ../csv/aust_hex_shape_57km.csv ../shapefiles/aust_hex_shape_57km.shp

#feat_aust_11
#ogr2ogr ../shapefiles/feat_aust_57km_sa1_11.shp '../vrt/feat_aust_11.vrt' -dialect sqlite -sql @../sql/feat_aust_11.sql
#ogr2ogr -f "CSV" ../csv/feat_aust_57km_sa1_11.csv ../shapefiles/feat_aust_57km_sa1_11.shp

#feat_aust_16
#ogr2ogr ../shapefiles/feat_aust_57km_sa1_16.shp '../vrt/feat_aust_16.vrt' -dialect sqlite -sql @../sql/feat_aust_16.sql
#ogr2ogr -f "CSV" ../csv/feat_aust_57km_sa1_16.csv ../shapefiles/feat_aust_57km_sa1_16.shp

#donor_feat_area_11_B18_B21_B22_csv
#sh dbcsvfun.sh 2011Census_B18_AUST_SA1_long db
#sh dbcsvfun.sh 2011Census_B21_AUST_SA1_long db
#sh dbcsvfun.sh 2011Census_B22B_AUST_SA1_long db
#sh dbcsvfun.sh feat_aust_57km_sa1_11 db
#spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_area_11_B18_B21_B22.txt

#donor_feat_area_16_G18_G21_G22_csv
#sh dbcsvfun.sh 2016Census_G18_AUS_SA1 db
#sh dbcsvfun.sh 2016Census_G21_AUS_SA1 db
#sh dbcsvfun.sh 2016Census_G22B_AUS_SA1 db
#sh dbcsvfun.sh feat_aust_57km_sa1_16 db
#spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_area_16_G18_G21_G22.txt

#feat_place_11_count
#sh dbshpfun.sh feat_aust_57km_sa1_11 4823 db
#sh dbshpfun.sh gis_osm_places_free_1 4823 db
#spatialite ../spatialite_db/db.sqlite < ../spatialite_db/feat_place_11_count.txt

#feat_place_16_count
#sh dbshpfun.sh feat_aust_57km_sa1_16 db
#sh dbshpfun.sh gis_osm_places_free_1 db
#spatialite ../spatialite_db/db.sqlite < ../spatialite_db/feat_place_16_count.txt

#shape_place_count
#ogr2ogr ../shapefiles/shape_57km_place_count.shp '../vrt/shape_place.vrt' -dialect sqlite -sql @../sql/shape_place_count.sql

#shape_agil_count
#ogr2ogr -f 'ESRI Shapefile' ../shapefiles/agil_4326.shp  ../geojson/AGIL.json 
#ogr2ogr -t_srs 'EPSG:4823' ../shapefiles/agil.shp ../shapefiles/agil_4326.shp 
#ogr2ogr ../shapefiles/shape_donor_feat_57km_agil_count.shp '../vrt/shape_agil.vrt' -dialect sqlite -sql @../sql/shape_agil_count.sql


#shape_pois_bstations_count (shape_bstation_count)
#ogr2ogr ../shapefiles/shape_57km_mbsp_count.shp '../vrt/shape_mbsp.vrt' -dialect sqlite -sql @../sql/shape_mbsp_count.sql

#shape_pois_service_count (shape_service_count)
#ogr2ogr ../shapefiles/shape_57km_services_count.shp '../vrt/shape_pois.vrt' -dialect sqlite -sql @../sql/shape_services_count.sql

#shape_road_count
#ogr2ogr ../shapefiles/shape_57km_road_count.shp '../vrt/shape_road.vrt' -dialect sqlite -sql @../sql/shape_road_count.sql

#shape_11_16_area
#ogr2ogr ../shapefiles/shape_57km_area_11_16.shp '../vrt/shape_11_16.vrt' -dialect sqlite -sql @../sql/shape_11_16_area.sql
#ogr2ogr -f "CSV" ../csv/shape_57km_area_11_16.csv ../shapefiles/shape_57km_area_11_16.shp

#shape_11_16_place
#ogr2ogr ../shapefiles/shape_57km_place_11_16.shp '../vrt/shape_11_16.vrt' -dialect sqlite -sql @../sql/shape_11_16_place.sql
#ogr2ogr -f "CSV" ../csv/shape_57km_place_11_16.csv ../shapefiles/shape_57km_place_11_16.shp

