#ogr2ogr ../csv/donor_feat_57km_16_G18_G21_G22.csv '../vrt/donor_feat_16.vrt' -dialect sqlite -sql @../sql/donor_feat_16_G18_G21_G22.sql
sh dbcsvfun.sh 2016Census_G18_AUS_SA1
sh dbcsvfun.sh 2016Census_G21_AUS_SA1
sh dbcsvfun.sh 2016Census_G22B_AUS_SA1
sh dbcsvfun.sh feat_aust_57km_sa1_16
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_area_57km_16_G18_G21_G22.txt
