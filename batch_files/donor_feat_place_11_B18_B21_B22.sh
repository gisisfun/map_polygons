sh dbcsvfun.sh 2011Census_B18_AUST_SA1_long db
sh dbcsvfun.sh 2011Census_B21_AUST_SA1_long db
sh dbcsvfun.sh 2011Census_B22B_AUST_SA1_long db
sh dbshpfun.sh feat_aust_57km_sa1_11 4823 db 
sh dbshpfun.sh gis_osm_places_free_1 4823 db
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_place_11_B18_B21_B22.txt

