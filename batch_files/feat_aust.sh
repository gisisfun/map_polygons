ogr2ogr ../shapefiles/feat_aust_57km_sa1.shp '../vrt/feat_aust.vrt' -dialect sqlite -sql @../sql/feat_aust.sql
ogr2ogr -f "CSV" ../csv/feat_aust_57km_sa1.csv ../shapefiles/feat_aust_57km_sa1.shp
