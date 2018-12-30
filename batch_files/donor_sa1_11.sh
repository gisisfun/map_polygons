#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr ../csv/donor_feat_57km_sa1_11.csv '../vrt/donor_feat_11.vrt' -dialect sqlite -sql @../sql/donor_sa1_11.sql
