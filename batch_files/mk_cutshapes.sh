ogr2ogr ../shapefiles/cut_sa1.shp '../vrt/poly_to_shape_ESRI_Shapefile.vrt' -dialect sqlite -sql @cut_by_shape.sql
