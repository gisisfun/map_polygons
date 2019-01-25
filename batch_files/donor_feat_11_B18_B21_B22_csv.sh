#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

#ogr2ogr -f "CSV" ../csv/donor_feat_57km_11_B18_B21_B22.csv '../vrt/donor_feat_11.vrt' -dialect sqlite -sql @../sql/donor_feat_11_B18_B21_B22.sql
sh dbcsvfun.sh 2011Census_B18_AUST_SA1_long
sh dbcsvfun.sh 2011Census_B21_AUST_SA1_long
sh dbcsvfun.sh 2011Census_B22B_AUST_SA1_long
sh dbcsvfun.sh feat_aust_57km_sa1_11
spatialite ../spatialite_db/db.sqlite < ../spatialite_db/donor_feat_57km_16_G18_G21_G22.txt
