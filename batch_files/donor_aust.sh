#Persons_Total_Has_need_for_assistance/Persons_Total_Total by region_id SA1_7DigitCODE_2011

ogr2ogr ../shapefiles/donor_aust_57km_aust.shp '../vrt/donor_aust.vrt' -dialect sqlite -sql @../sql/donor_aust.sql
