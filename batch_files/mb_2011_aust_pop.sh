ogr2ogr -f "ESRI Shapefile" ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_NSW.shp

ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_QLD.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_VIC.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_SA.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_WA.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_TAS.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_NT.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_ACT.shp
ogr2ogr -f "ESRI Shapefile" -update -append ../shapefiles/MB_2011_AUST.shp ../shapefiles/MB_2011_OT.shp

ogr2ogr ../shapefiles/mb_2011_aust_pop_.shp '../vrt/mb_2011_aust_pop.vrt' -dialect sqlite -sql @../sql/mb_2011_aust_pop.sql

ogr2ogr ../shapefiles/mb_2011_aust_pop.shp '../vrt/mb_2011_aust_pop.vrt' -dialect sqlite -sql @../sql/mb_2011_aust_pop_.sql