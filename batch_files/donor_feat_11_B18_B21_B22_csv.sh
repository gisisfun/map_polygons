#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr -f "CSV" ../csv/donor_feat_57km_11_B18_B21_B22.csv '../vrt/donor_feat_11.vrt' -dialect sqlite -sql @../sql/donor_feat_11_B18_B21_B22.sql
