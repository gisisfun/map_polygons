#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr ../shapefiles/donor_feat_57km_aust_16.shp '../vrt/donor_feat_16.vrt' -dialect sqlite -sql @../sql/donor_feat_16.sql