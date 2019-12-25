"""
Script used to postprocess the polygon data set
"""
import sys
from isotiles.postprocess import PostProcess
from isotiles.util import Util



def area_wt(the_shape, the_radial):
    """
    Area based weighting used to post process the polygon data set

    the_shape:
    the_radial:
    """
    p_mod = PostProcess(shape=the_shape, radial=the_radial)
    u_mod = Util(shape=the_shape, radial=the_radial)

    shape_and_size = p_mod.shape +'_' + p_mod.radial
    aust_shape_file_name = 'aust_' + p_mod.shape +'_shape_' + \
                           p_mod.radial +'km'
    gj_name = 'aus_' + shape_and_size + 'km_layer'
    vrt_ref = 'all_' +shape_and_size
    vrt_file = 'all_' + shape_and_size + '.vrt'
    feat_sa1_11 = 'feat_aust_' + p_mod.radial +'km_sa1_11'
    feat_sa1_16 = 'feat_aust_' + p_mod.radial +'km_sa1_16'
    db_name = 'db_area_' + shape_and_size
    tabular_sql_name = 'tabular_area_wt_' + shape_and_size + '.txt'
    output_shape = shape_and_size + 'km_area_11_16'

    p_mod.vrt_shape_and_size('vrt', 'template.vrt', vrt_file)
    p_mod.do_spatialite('table_goes_here.txt', db_name)
    u_mod.ref_files_poly_wt()

    print('aust_shape')

    p_mod.geojson_to_shp(gj_name, aust_shape_file_name, 4283)
    #p.sql_to_ogr('aust_shape', vrt_ref, fname)

    p_mod.shp_to_db(aust_shape_file_name, db_name, aust_shape_file_name, 4823)

    print('feat_aust_11_area')

    p_mod.sql_to_ogr('feat_aust_11', vrt_ref, feat_sa1_11)
    p_mod.shp_to_db(feat_sa1_11, db_name, feat_sa1_11, 4823)

    print('feat_aust_16_area')

    p_mod.sql_to_ogr('feat_aust_16', vrt_ref, feat_sa1_16)

    p_mod.shp_to_db(feat_sa1_16, db_name, feat_sa1_16, 4823)

    print('tabular_area_wt')
    p_mod.csv_to_db('2011Census_B18_AUST_SA1_long', db_name,\
                    '2011Census_B18_AUST_SA1_long')
    p_mod.csv_to_db('2011Census_B21_AUST_SA1_long', db_name,\
                    '2011Census_B21_AUST_SA1_long')
    p_mod.csv_to_db('2011Census_B22B_AUST_SA1_long', db_name,\
                    '2011Census_B22B_AUST_SA1_long')
    p_mod.csv_to_db('2016Census_G18_AUS_SA1', db_name,\
                    '2016Census_G18_AUS_SA1')
    p_mod.csv_to_db('2016Census_G21_AUS_SA1', db_name,\
                    '2016Census_G21_AUS_SA1')
    p_mod.csv_to_db('2016Census_G22B_AUS_SA1', db_name,\
                    '2016Census_G22B_AUS_SA1')

    p_mod.shp_to_db(aust_shape_file_name, db_name, aust_shape_file_name, 4823)

    p_mod.shp_to_db(feat_sa1_11, db_name, feat_sa1_11, 4823)

    p_mod.shp_to_db(feat_sa1_16, db_name, feat_sa1_16, 4823)

    p_mod.shp_to_db('gis_osm_places_free_1', db_name,\
                    'gis_osm_places_free_1', 4823)
    p_mod.shp_to_db('gis_osm_roads_free_1', db_name,\
                    'gis_osm_roads_free_1', 4823)

    p_mod.sql_to_ogr('shape_pois_shp', vrt_ref, 'POI')
    p_mod.shp_to_db('POI', db_name, 'POI', 4823)
    #p.sql_to_ogr('shape_agil_shp', vrt_ref, 'agil')
    #p.shp_to_db('agil', db_name, 'agil', 4823)
    #p.sql_to_ogr('shape_mbsp_shp', vrt_ref, 'mbsp')
    #p.shp_to_db('mbsp', db_name, 'mbsp', 4823)

    p_mod.shape_and_size('spatialite_db', 'tabular_area_wt.txt', \
                         tabular_sql_name)
    p_mod.do_spatialite(tabular_sql_name, db_name)

    # spatialite ../spatialite_db/db.sqlite "vacuum;"

    print('shape_11_16_area')

    p_mod.sql_to_ogr('shape_11_16_area', vrt_ref, output_shape)


    p_mod.shp_to_geojson(output_shape,output_shape)
    p_mod.shp_to_kml(output_shape,output_shape) 


def place_wt(the_shape, the_radial):
    """
    Place count based weighting used to post process the polygon data set
    the_shape:
    the_radial:
    """
    p_mod = PostProcess(shape=the_shape, radial=the_radial)
    u_mod = Util(shape=the_shape, radial=the_radial)

    shape_and_size = p_mod.shape +'_' + p_mod.radial
    aust_shape_file_name = 'aust_' + p_mod.shape +'_shape_' + \
                           p_mod.radial +'km'
    gj_name = 'aus_' + shape_and_size + 'km_layer'
    vrt_ref = 'all_' +shape_and_size
    vrt_file = 'all_' + shape_and_size + '.vrt'
    feat_sa1_11 = 'feat_aust_' + p_mod.radial +'km_sa1_11'
    feat_sa1_16 = 'feat_aust_' + p_mod.radial +'km_sa1_16'
    db_name = 'db_place_' + shape_and_size
    tabular_sql_name = 'tabular_place_wt_' + shape_and_size + '.txt'
    output_shape = shape_and_size + 'km_place_11_16'


    p_mod.vrt_shape_and_size('vrt', 'template.vrt', vrt_file)
    p_mod.do_spatialite('table_goes_here.txt', db_name)
    u_mod.ref_files_poly_wt()


    print('aust_shape')
    p_mod.geojson_to_shp(gj_name, aust_shape_file_name, 4283)
    #p.sql_to_ogr('aust_shape', vrt_ref, fname)

    p_mod.shp_to_db(aust_shape_file_name, db_name, aust_shape_file_name, 4823)

    print('feat_aust_11_area')
    p_mod.sql_to_ogr('feat_aust_11', vrt_ref, feat_sa1_11)
    p_mod.shp_to_db(feat_sa1_11, db_name, feat_sa1_11, 4823)

    print('feat_aust_16_area')
    p_mod.sql_to_ogr('feat_aust_16', vrt_ref, feat_sa1_16)
    p_mod.shp_to_db(feat_sa1_16, db_name, feat_sa1_16, 4823)

    print('tabular_place_wt')
    p_mod.csv_to_db('2011Census_B18_AUST_SA1_long',\
                    db_name, '2011Census_B18_AUST_SA1_long')
    p_mod.csv_to_db('2011Census_B21_AUST_SA1_long',\
                    db_name, '2011Census_B21_AUST_SA1_long')
    p_mod.csv_to_db('2011Census_B22B_AUST_SA1_long',\
                    db_name, '2011Census_B22B_AUST_SA1_long')
    p_mod.csv_to_db('2016Census_G18_AUS_SA1',\
                    db_name, '2016Census_G18_AUS_SA1')
    p_mod.csv_to_db('2016Census_G21_AUS_SA1',\
                    db_name, '2016Census_G21_AUS_SA1')
    p_mod.csv_to_db('2016Census_G22B_AUS_SA1',\
                    db_name, '2016Census_G22B_AUS_SA1')
    file_name = 'aust_{shape}_shape_{size}km'.\
                 format(shape=p_mod.shape,\
                   size=p_mod.radial)
    p_mod.shp_to_db(file_name, db_name, file_name, 4823)

    p_mod.shp_to_db(feat_sa1_11, db_name, feat_sa1_11, 4823)

    p_mod.shp_to_db(feat_sa1_16, db_name, feat_sa1_16, 4823)
    p_mod.shp_to_db('gis_osm_places_free_1',\
                    db_name, 'gis_osm_places_free_1', 4823)
    p_mod.shp_to_db('gis_osm_roads_free_1',\
                    db_name, 'gis_osm_roads_free_1', 4823)
    p_mod.sql_to_ogr('shape_pois_shp', vrt_ref, 'POI')
    p_mod.shp_to_db('POI', db_name, 'POI', 4823)

    p_mod.shape_and_size('spatialite_db', 'tabular_place_wt.txt',\
                         tabular_sql_name)
    p_mod.do_spatialite(tabular_sql_name, db_name)

    # spatialite ../spatialite_db/db.sqlite "vacuum;"

    print('shape_11_16_place')

    p_mod.sql_to_ogr('shape_11_16_place', vrt_ref, output_shape)


    p_mod.shp_to_geojson(output_shape,output_shape)
    p_mod.shp_to_kml(output_shape,output_shape) 


print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) == 1:
    (WEIGHT_FACTOR, THE_SHAPE, THE_SIZE) = ['place', 'hex', '57']
    place_wt(THE_SHAPE, THE_SIZE)
else:
    if len(sys.argv) < 4:
        sys.exit("arguments are \nshape \n size (km)\n ")
    else:
        (THE_SCRIPT, WEIGHT_FACTOR, THE_SHAPE, THE_SIZE) = sys.argv
        if WEIGHT_FACTOR == 'place':
            place_wt(THE_SHAPE, THE_SIZE)
        else:
            area_wt(THE_SHAPE, THE_SIZE)
