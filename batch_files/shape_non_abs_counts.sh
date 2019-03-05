sh dbshpfun.sh gis_osm_places_free_1 4823 db
sh dbshpfun.sh gis_osm_roads_free_1 4823 db
sh dbshpfun.sh gis_osm_pois_free_1 4823 db

ogr2ogr -f 'ESRI Shapefile' ../shapefiles/agil_4326.shp  ../geojson/AGIL.json 
ogr2ogr -t_srs 'EPSG:4823' ../shapefiles/agil.shp ../shapefiles/agil_4326.shp 
sh dbshpfun.sh agil 4823 db

sh dbshpfun.sh aust_hex_shape_57km 4823 db

ogr2ogr ../shapefiles/mbsp.shp '../vrt/shape_mbsp.vrt' -dialect sqlite -sql @../sql/shape_mbsp_shp.sql
sh dbshpfun.sh mbsp 4823 db

spatialite ../spatialite_db/db.sqlite < ../spatialite_db/shape_nonabs_counts.txt
