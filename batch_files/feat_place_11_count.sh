sh dbshpfun.sh feat_aust_57km_sa1_11 4823 db
sh dbshpfun.sh gis_osm_places_free_1 4823 db
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/feat_place_11_count.txt
