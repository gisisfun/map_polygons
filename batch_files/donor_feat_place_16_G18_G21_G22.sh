sh dbcsvfun.sh 2016Census_G18_AUS_SA1 db
sh dbcsvfun.sh 2016Census_G21_AUS_SA1 db
sh dbcsvfun.sh 2016Census_G22B_AUS_SA1 db
sh dbcsvfun.sh feat_aust_57km_sa1_16 db
sh dbcsvfun.sh feat_57km_16_place_wt db
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_place_16_G18_G21_G22.txt
