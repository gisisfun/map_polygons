"""
Script used to postprocess the polygon data set
Tabular data appended to existing polygon data set:
ABS Census polygon data intersecting polygon weighted data and
OpenStreetMaps points of interest
"""
import argparse
from isotiles.postprocess import PostProcess
from utils import from_json_file, file_deploy



def area_wt(the_shape, the_radial):
    """
    Area based weighting used to post process the polygon data set

    :param: the_shape
    :param: the_radial
    """
    p_mod = PostProcess(shape=the_shape, radial=the_radial)
    #u_mod = Util(shape=the_shape, radial=the_radial)
    shape_and_size = p_mod.shape +'_' + str(p_mod.radial)
    aust_shape_file_name = 'aust_' + p_mod.shape +'_shape_' + \
                           str(p_mod.radial) +'km'
    gj_name = 'aus_' + shape_and_size + 'km_layer'
    vrt_ref = 'all_' + shape_and_size
    vrt_file = 'all_' + shape_and_size + '.vrt'
    feat_sa1_11 = 'feat_aust_' + str(p_mod.radial) +'km_sa1_11'
    feat_sa1_16 = 'feat_aust_' + str(p_mod.radial) +'km_sa1_16'
    db_name = 'db_area_' + shape_and_size
    tabular_sql_name = 'tabular_area_wt_' + shape_and_size + '.txt'
    output_shape = shape_and_size + 'km_area_11_16'
    p_mod.vrt_shape_and_size('vrt', 'template.vrt', vrt_file)
    p_mod.do_spatialite('table_goes_here.txt', db_name)
    
    datasets = from_json_file('datasets', p_mod.json_files_path, p_mod.slash)

    ref_data = datasets['DataSets']['Australia']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['StatisticalAreasLevel12011']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['StatisticalAreasLevel12016']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['AGILDataset']['CSVFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['OpenStreetMaps']['ShapeFormat']
    file_deploy(ref_data)

    print('aust_shape')
    p_mod.geojson_to_shp(gj_name, aust_shape_file_name, 4283)
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
    p_mod.shape_and_size('spatialite_db', 'tabular_area_wt.txt', \
                         tabular_sql_name)
    p_mod.do_spatialite(tabular_sql_name, db_name)

    print('shape_11_16_area')
    p_mod.sql_to_ogr('shape_11_16_area', vrt_ref, output_shape)
    p_mod.shp_to_geojson(output_shape, output_shape)
    p_mod.shp_to_kml(output_shape, output_shape)


def place_wt(the_shape, the_radial):
    """
    Place count based weighting used to post process the polygon data set
    :param: the_shape
    :param: the_radial
    """
    p_mod = PostProcess(shape=the_shape, radial=the_radial)
    #u_mod = Util(shape=the_shape, radial=the_radial)
    shape_and_size = p_mod.shape +'_' + str(p_mod.radial)
    aust_shape_file_name = 'aust_' + p_mod.shape +'_shape_' + \
                           str(p_mod.radial) +'km'
    gj_name = 'aus_' + shape_and_size + 'km_layer'
    vrt_ref = 'all_' +shape_and_size
    vrt_file = 'all_' + shape_and_size + '.vrt'
    feat_sa1_11 = 'feat_aust_' + str(p_mod.radial) +'km_sa1_11'
    feat_sa1_16 = 'feat_aust_' + str(p_mod.radial) +'km_sa1_16'
    db_name = 'db_place_' + shape_and_size
    tabular_sql_name = 'tabular_place_wt_' + shape_and_size + '.txt'
    output_shape = shape_and_size + 'km_place_11_16'
    p_mod.vrt_shape_and_size('vrt', 'template.vrt', vrt_file)
    p_mod.do_spatialite('table_goes_here.txt', db_name)
    
    datasets = from_json_file('datasets', p_mod.json_files_path, p_mod.slash)

    ref_data = datasets['DataSets']['Australia']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['StatisticalAreasLevel12011']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['StatisticalAreasLevel12016']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['AGILDataset']['CSVFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['OpenStreetMaps']['ShapeFormat']
    file_deploy(ref_data)
    
    #ref_files_poly_wt('datasets',p_mod.json_files_path, p_mod.slash)

    print('aust_shape')
    p_mod.geojson_to_shp(gj_name, aust_shape_file_name, 4283)
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

    print('shape_11_16_place')
    p_mod.sql_to_ogr('shape_11_16_place', vrt_ref, output_shape)
    p_mod.shp_to_geojson(output_shape, output_shape)
    p_mod.shp_to_kml(output_shape, output_shape)

PARSER = argparse.ArgumentParser(
        prog='poly_wt',
        description='''
        Tabular data appended to existing polygon data set:
            ABS Census polygon data intersecting polygon weighted data and
            OpenStreetMaps points of interest''')

PARSER.add_argument('-rl', '--radial', default=57, help="radial length in km")
PARSER.add_argument('-wt', '--weight', default='place',
                    help="polygon intersection weight variable (place or area)")
PARSER.add_argument('-sh', '--shape', default='hex', help="shape (hex or box)")


ARGS = PARSER.parse_args()
if ARGS.weight == 'place':
    place_wt(ARGS.shape, ARGS.radial)
if ARGS.weight == 'area':
    area_wt(ARGS.shape, ARGS.radial)
else:
    print('weight is place or area')
