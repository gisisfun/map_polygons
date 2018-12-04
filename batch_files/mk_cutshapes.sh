ogr2ogr cut_sa1.shp 'hex_aust_to_ref_layer_ESRI_Shapefile.vrt' -dialect sqlite -sql @cut_by_shape.sql
