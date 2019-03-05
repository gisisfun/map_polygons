sh dbcsvfun.sh 2011Census_B18_AUST_SA1_long db
sh dbcsvfun.sh 2011Census_B21_AUST_SA1_long db
sh dbcsvfun.sh 2011Census_B22B_AUST_SA1_long db
sh dbshpfun.sh SA1_2011_AUST 4823 db 
sh dbshpfun.sh aust_hex_shape_57km 4823 db 
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_area_11_B18_B21_B22.txt
