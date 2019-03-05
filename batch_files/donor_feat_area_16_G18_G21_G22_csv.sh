#ogr2ogr ../csv/donor_feat_57km_16_G18_G21_G22.csv '../vrt/donor_feat_16.vrt' -dialect sqlite -sql @../sql/donor_feat_16_G18_G21_G22.sql
sh dbcsvfun.sh 2016Census_G18_AUS_SA1 db
sh dbcsvfun.sh 2016Census_G21_AUS_SA1 db
sh dbcsvfun.sh 2016Census_G22B_AUS_SA1 db
sh dbcsvfun.sh feat_aust_57km_sa1_16 db
sh dbshpfun.sh SA1_2016_AUST 4823 db 
sh dbshpfun.sh aust_hex_shape_57km 4823 db 
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_area_16_G18_G21_G22.txt
