#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr ../csv/donor_feat_57km_16_G18_G21_G22.csv '../vrt/donor_feat_16.vrt' -dialect sqlite -sql @../sql/donor_feat_16_G18_G21_G22.sql
