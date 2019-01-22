ogr2ogr ../shapefiles/feat_aust_57km_sa1_11.shp '../vrt/feat_aust_11.vrt' -dialect sqlite -sql @../sql/feat_aust_11.sql
ogr2ogr -f "CSV" ../csv/feat_aust_57km_sa1_11.csv ../shapefiles/feat_aust_57km_sa1_11.shp
