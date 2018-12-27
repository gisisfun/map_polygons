#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id 

ogr2ogr ../shapefiles/donor_src_SA1_aust_16.shp '../vrt/donor_src_16.vrt' -dialect sqlite -sql @../sql/donor_src_16.sql
