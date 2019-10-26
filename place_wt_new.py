from isotiles.thecode import PostProcess

def process_sql(theshape, theradial):
    process = PostProcess(shape = theshape, radial = theradial)
    size='57'
    shape='hex'
    process.vrt_shape_and_size ('vrt', 'template.vrt', process.Shape, process.Radial, 'all_{shape}_{size}.vrt'.\
                                format(shape = process.Shape,\
                                       size = process.Radial))
    process.do_spatialite('table_goes_here.txt', 'db_place_{shape}_{size}'.\
                          format(shape = process.Shape,\
                                 size = process.Radial))
    
    print('aust_shape')

    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = process.Shape,\
                   size = process.Radial)
    process.sql_to_ogr('aust_shape', 'all', fname)
    
    process.shp_to_db(fname,'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    
    print('feat_aust_11_area')
    fname = 'feat_aust_{size}km_sa1_11'.\
            format(shape = process.Shape,\
                   size = process.Radial)
    process.sql_to_ogr('feat_aust_11','all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial\
                              ), fname)
    process.shp_to_db(fname,'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    
    print('feat_aust_16_area')
    fname = 'feat_aust_{size}km_sa1_16'.\
            format(shape = process.Shape,\
                   size = process.Radial)
    process.sql_to_ogr('feat_aust_16','all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial),\
                       fname)
    process.shp_to_db(fname,'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    
    print('tabular_place_wt')   
    process.csv_to_db('2011Census_B18_AUST_SA1_long',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2011Census_B18_AUST_SA1_long')
    process.csv_to_db('2011Census_B21_AUST_SA1_long',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2011Census_B21_AUST_SA1_long')
    process.csv_to_db('2011Census_B22B_AUST_SA1_long',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2011Census_B22B_AUST_SA1_long')
    process.csv_to_db('2016Census_G18_AUS_SA1',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2016Census_G18_AUS_SA1')
    process.csv_to_db('2016Census_G21_AUS_SA1',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2016Census_G21_AUS_SA1')
    process.csv_to_db('2016Census_G22B_AUS_SA1',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      '2016Census_G22B_AUS_SA1')
    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = process.Shape,\
                   size = process.Radial)
    process.shp_to_db(fname,\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape = process.Shape,\
                  size = process.Radial)
    process.shp_to_db(fname,'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = process.Shape,\
                  size = process.Radial)
    process.shp_to_db(fname,'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      fname, 4823)
    process.shp_to_db('gis_osm_places_free_1',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      'gis_osm_places_free_1', 4823)
    process.shp_to_db('gis_osm_roads_free_1',\
                      'db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      'gis_osm_roads_free_1', 4823)
    process.sql_to_ogr('shape_pois_shp', 'all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial), 'POI')
    process.shp_to_db('POI','db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      'POI', 4823)
    process.sql_to_ogr('shape_agil_shp',\
                       'all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial),\
                       'agil')
    process.shp_to_db('agil','db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      'agil', 4823)
    process.sql_to_ogr('shape_mbsp_shp', 'all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial), 'mbsp')
    process.shp_to_db('mbsp','db_place_{shape}_{size}'.\
                      format(shape = process.Shape,\
                             size = process.Radial),\
                      'mbsp', 4823)

    sqlname='tabular_place_wt_{shape}_{size}.txt'.\
             format(shape = process.Shape,\
                    size = process.Radial)
    process.shape_and_size ('spatialite_db',\
                            'tabular_place_wt.txt',\
                            process.Shape, process.Radial, sqlname)
    process.do_spatialite(sqlname,'db_place_{shape}_{size}'.\
                          format(shape = process.Shape,\
                                 size = process.Radial))
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"

    print('shape_11_16_place')
    fname='{shape}_{size}km_place_11_16'.\
           format(shape = process.Shape,\
                  size = process.Radial)

    process.sql_to_ogr('shape_11_16_place',\
                       'all_{shape}_{size}'.\
                       format(shape = process.Shape,\
                              size = process.Radial),\
                       fname)

process_sql("hex",57)