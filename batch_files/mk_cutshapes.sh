ogr2ogr ../shapefiles/cut_sa1.shp '../vrt/hex_aust_to_ref_layer_ESRI_Shapefile.vrt' -dialect sqlite -sql @cut_by_shape.sql
