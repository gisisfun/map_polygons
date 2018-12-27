ogr2ogr ../shapefiles/feat_aust_57km_sa1_16.shp '../vrt/feat_aust_16.vrt' -dialect sqlite -sql @../sql/feat_aust_16.sql
ogr2ogr -f "CSV" ../csv/feat_aust_57km_sa1_16.csv ../shapefiles/feat_aust_57km_sa1_16.shp
