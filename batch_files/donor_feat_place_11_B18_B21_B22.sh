sh dbcsvfun.sh 2011Census_B18_AUST_SA1_long
sh dbcsvfun.sh 2011Census_B21_AUST_SA1_long
sh dbcsvfun.sh 2011Census_B22B_AUST_SA1_long
sh dbcsvfun.sh feat_aust_57km_sa1_11
sh dbcsvfun.sh feat_57km_11_place_wt
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_place_11_B18_B21_B22.txt
