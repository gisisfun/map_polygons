ogr2ogr ../shapefiles/shape_donor_feat_57km_aust_11.shp '../vrt/shape_donor_11.vrt' -dialect sqlite -sql @../sql/shape_donor_11.sql
ogr2ogr -f "CSV" ../csv/shqpe_donor_feat_75km_aust_11.csv ../shapefiles/shape_donor_feat_57km_aust_11.shp