from isotiles.thecode import PostProcess
import sys

def area_wt(theshape,theradial):
#    size='57'
#    shape='hex'
    p = PostProcess(shape = theshape, radial = theradial)
    
    vrt_file = 'all_{shape}_{size}.vrt'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    vrt_ref = 'all_{shape}_{size}'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    
    db_name = 'db_area_{shape}_{size}.vrt'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    
    p.vrt_shape_and_size ('vrt', 'template.vrt', vrt_file)
    p.do_spatialite('table_goes_here.txt', db_name)
    
    print('aust_shape')
    
    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('aust_shape', vrt_ref, fname)
    p.shp_to_db(fname,db_name,fname,4823)
    
    print('feat_aust_11_area')
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape=p.Shape,\
                  size = p.Radial)
    p.sql_to_ogr('feat_aust_11', vrt_ref, fname)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    print('feat_aust_16_area')
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    
    p.sql_to_ogr('feat_aust_16', vrt_ref, fname)
    
    p.shp_to_db(fname, db_name, fname, 4823)
    
    print('tabular_area_wt')   
    p.csv_to_db('2011Census_B18_AUST_SA1_long',db_name,\
                '2011Census_B18_AUST_SA1_long')
    p.csv_to_db('2011Census_B21_AUST_SA1_long',db_name,\
                '2011Census_B21_AUST_SA1_long')
    p.csv_to_db('2011Census_B22B_AUST_SA1_long',db_name,\
                '2011Census_B22B_AUST_SA1_long')
    p.csv_to_db('2016Census_G18_AUS_SA1',db_name,\
                '2016Census_G18_AUS_SA1')
    p.csv_to_db('2016Census_G21_AUS_SA1',db_name,\
                '2016Census_G21_AUS_SA1')
    p.csv_to_db('2016Census_G22B_AUS_SA1',db_name,\
                '2016Census_G22B_AUS_SA1')
    
    fname='aust_{shape}_shape_{size}km'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    p.shp_to_db('gis_osm_places_free_1', db_name,\
                'gis_osm_places_free_1', 4823)
    p.shp_to_db('gis_osm_roads_free_1', db_name,\
                'gis_osm_roads_free_1', 4823)
    
    p.sql_to_ogr('shape_pois_shp', vrt_ref, 'POI')
    p.shp_to_db('POI', db_name, 'POI', 4823)
    p.sql_to_ogr('shape_agil_shp', vrt_ref, 'agil')
    p.shp_to_db('agil', db_name, 'agil', 4823)
    p.sql_to_ogr('shape_mbsp_shp', vrt_ref, 'mbsp')
    p.shp_to_db('mbsp', db_name, 'mbsp', 4823)

    sqlname='tabular_area_wt_{shape}_{size}.txt'.\
             format(shape = p.Shape,\
                    size = p.Radial)
    p.shape_and_size ('spatialite_db', \
                      'tabular_area_wt.txt', sqlname)
    p.do_spatialite(sqlname, db_name)
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"
    
    
    print('shape_11_16_area')
    fname='{shape}_{size}km_area_11_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.sql_to_ogr('shape_11_16_area', vrt_ref, fname)

def place_wt(theshape, theradial):
    p = PostProcess(shape = theshape, radial = theradial)
    
    vrt_file = 'all_{shape}_{size}.vrt'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    
    vrt_ref = 'all_{shape}_{size}'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    
    db_name = 'db_area_{shape}_{size}.vrt'.\
              format(shape = p.Shape,\
                     size = p.Radial)
    
    p.vrt_shape_and_size ('vrt', 'template.vrt',vrt_file)
    p.do_spatialite('table_goes_here.txt', db_name)
    
    print('aust_shape')

    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('aust_shape', vrt_ref, fname)
    
    p.shp_to_db(fname, db_name, fname, 4823)
    
    print('feat_aust_11_area')
    fname = 'feat_aust_{size}km_sa1_11'.\
            format(size = p.Radial)
    p.sql_to_ogr('feat_aust_11', vrt_ref, fname)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    print('feat_aust_16_area')
    fname = 'feat_aust_{size}km_sa1_16'.\
            format(size = p.Radial)
    p.sql_to_ogr('feat_aust_16',vrt_ref,fname)
    p.shp_to_db(fname, db_name, fname, 4823)
    
    print('tabular_place_wt')   
    p.csv_to_db('2011Census_B18_AUST_SA1_long',\
                db_name,'2011Census_B18_AUST_SA1_long')
    p.csv_to_db('2011Census_B21_AUST_SA1_long',\
                db_name,'2011Census_B21_AUST_SA1_long')
    p.csv_to_db('2011Census_B22B_AUST_SA1_long',\
                db_name,'2011Census_B22B_AUST_SA1_long')
    p.csv_to_db('2016Census_G18_AUS_SA1',\
                db_name,'2016Census_G18_AUS_SA1')
    p.csv_to_db('2016Census_G21_AUS_SA1',\
                db_name,'2016Census_G21_AUS_SA1')
    p.csv_to_db('2016Census_G22B_AUS_SA1',\
                db_name,'2016Census_G22B_AUS_SA1')
    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    fname='feat_aust_{size}km_sa1_11'.\
           format(size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, db_name, fname, 4823)
    p.shp_to_db('gis_osm_places_free_1',\
                db_name, 'gis_osm_places_free_1', 4823)
    p.shp_to_db('gis_osm_roads_free_1',\
                db_name, 'gis_osm_roads_free_1', 4823)
    p.sql_to_ogr('shape_pois_shp', db_name, 'POI')
    p.shp_to_db('POI', db_name,'POI', 4823)
    p.sql_to_ogr('shape_agil_shp', vrt_ref, 'agil')
    p.shp_to_db('agil', db_name, 'agil', 4823)
    p.sql_to_ogr('shape_mbsp_shp', db_name, 'mbsp')
    p.shp_to_db('mbsp', db_name, 'mbsp', 4823)

    sqlname='tabular_place_wt_{shape}_{size}.txt'.\
             format(shape = p.Shape,\
                    size = p.Radial)
    p.shape_and_size ('spatialite_db',\
                      'tabular_place_wt.txt',\
                      sqlname)
    p.do_spatialite(sqlname, db_name)
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"

    print('shape_11_16_place')
    fname='{shape}_{size}km_place_11_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)

    p.sql_to_ogr('shape_11_16_place', vrt_ref, fname)



print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (wtg,shape, size) = ['place','hex', '57']
    area_wt(shape, size)
else:
    if (len(sys.argv) < 4 ):
        sys.exit("arguments are \nshape \n size (km)\n ")
    else:
        (blah, wtg, shape, size) = sys.argv
        if wtg is 'place':
            place_wt(shape, size)
        else:
            area_wt(shape,size)
