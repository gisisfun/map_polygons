ogr2ogr ../shapefiles/shape_57km_mbsp_count.shp '../vrt/shape_mbsp.vrt' -dialect sqlite -sql @../sql/shape_mbsp_count.sql
#ogr2ogr -f "CSV" ../csv/shqpe_donor_feat_75km_aust_11.csv ../shapefiles/shape_donor_feat_57km_aust_11.shp
