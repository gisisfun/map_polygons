ogr2ogr -f "ESRI Shapefile" ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_NSW.shp

ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_QLD.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_VIC.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_SA.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_WA.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_TAS.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_NT.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_ACT.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2016_AUST.shp ../shapefiles/MB_2016_OT.shp

ogr2ogr ../shapefiles/mb_2016_aust_pop_.shp '../vrt/mb_2016_aust_pop.vrt' -dialect sqlite -sql @../sql/mb_2016_aust_pop.sql

ogr2ogr ../shapefiles/mb_2016_aust_pop.shp '../vrt/mb_2016_aust_pop.vrt' -dialect sqlite -sql @../sql/mb_2016_aust_pop_.sql