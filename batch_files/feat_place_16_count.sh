sh dbshpfun.sh feat_aust_57km_sa1_16
sh dbshpfun.sh shape_57km_place_count
sh dbshpfun.sh gis_osm_places_free_1
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/feat_place_16_count.txt
