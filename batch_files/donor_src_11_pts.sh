#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr ../shapefiles/donor_src_SA1_pts_11.shp '../vrt/donor_feat_11.vrt' -dialect sqlite -sql @../sql/donor_src_11_pts.sql
