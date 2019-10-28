from isotiles.thecode import Tiles, PostProcess, Visual
import random
import sys

def random_points(bounds_n,bounds_s,bounds_e,bounds_w,numpoints):
    """
    Create an array of random points
    """
    
    ns_range = bounds_n - bounds_s
    ew_range = bounds_e - bounds_w
    coord_list=[]

    x_coords_list=[]
    y_coords_list=[]
    
    for i in range(0,numpoints):
        y_coord = bounds_s+random.randrange(0, ns_range*10000)/10000
        x_coord = bounds_w+random.randrange(0, ew_range*10000)/10000
        coord=[x_coord,y_coord]
        coord_list.append(coord)
        x_coords_list.append(x_coord)
        y_coords_list.append(y_coord)
        
        #print(layer_json)
        return coord_list 

def do_map(theshape,theradial):
    v = Visual(shape = theshape, radial = theradial)
    v.map_data()

def area_wt(theshape,theradial):
#    size='57'
#    shape='hex'
    p = PostProcess(shape = theshape, radial = theradial)
    p.shape_and_size('vrt', 'template.vrt',\
                     'all_{shape}_{size}.vrt'.\
                     format(shape = p.Shape,\
                            size =p.Radial))
    p.do_spatialite('table_goes_here.txt',\
                  'db_{shape}_{size}'.\
                  format(shape = p.Shape,\
                         size = p.Radial))
    print('aust_shape')
    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('aust_shape', 'all',fname)
    p.shp_to_db(fname,'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname,4823)
    
    print('feat_aust_11_area')
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape=p.Shape,\
                  size = p.Radial)
    p.sql_to_ogr('feat_aust_11',\
                 'all_{shape}_{size}'.\
                 format(shape=p.Shape,\
                        size = p.Radial),\
                 fname)
    p.shp_to_db(fname,'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    
    print('feat_aust_16_area')
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p,sql_to_ogr('feat_aust_16',\
                 'all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                 fname)
    p.shp_to_db(fname,'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    
    print('tabular_area_wt')   
    p.csv_to_db('2011Census_B18_AUST_SA1_long',\
                'db','2011Census_B18_AUST_SA1_long')
    p.csv_to_db('2011Census_B21_AUST_SA1_long','db',\
                '2011Census_B21_AUST_SA1_long')
    p.csv_to_db('2011Census_B22B_AUST_SA1_long','db',\
                '2011Census_B22B_AUST_SA1_long')
    p.csv_to_db('2016Census_G18_AUS_SA1','db',\
                '2016Census_G18_AUS_SA1')
    p.csv_to_db('2016Census_G21_AUS_SA1','db',\
                '2016Census_G21_AUS_SA1')
    p.csv_to_db('2016Census_G22B_AUS_SA1','db',\
                '2016Census_G22B_AUS_SA1')
    fname='aust_{shape}_shape_{size}km'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, 'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname, 'db_{shape}_{size}'.\
                format(shape=p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname,'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    p.shp_to_db('gis_osm_places_free_1', 'db',\
                'gis_osm_places_free_1', 4823)
    p.shp_to_db('gis_osm_roads_free_1', 'db',\
                'gis_osm_roads_free_1', 4823)
    p.sql_to_ogr('shape_pois_shp', 'all', 'POI')
    p.shp_to_db('POI','db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'POI', 4823)
    p.geojson_to_shp ('AGIL', 'agil', 4823)
    p,shp_to_db('agil', 'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'agil', 4823)
    p,sql_to_ogr('shape_mbsp_shp', 'all', 'mbsp')
    p.shp_to_db('mbsp', 'db_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'mbsp', 4823)

    sqlname='tabular_area_wt_{shape}_{size}.txt'.\
             format(shape = p.Shape,\
                    size = p.Radial)
    p.shape_and_size ('spatialite_db',\
                      'tabular_area_wt.txt',\
                      sqlname)
    p.do_spatialite(sqlname, 'db_{shape}_{size}'.\
                  format(shape = p.Shape,\
                         size = p.Radial))
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"
    
    
    print('shape_11_16_area')
    fname='shape_{size}km_area_11_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.sql_to_ogr('shape_11_16_area',\
                 'all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                 fname)

def place_wt(theshape, theradial):
    p = PostProcess(shape = theshape, radial = theradial)

    p.vrt_shape_and_size ('vrt', 'template.vrt', \
                          'all_{shape}_{size}.vrt'.\
                          format(shape = p.Shape,\
                                 size = p.Radial))
    p.do_spatialite('table_goes_here.txt', \
                    'db_place_{shape}_{size}'.\
                    format(shape = p.Shape,\
                           size = p.Radial))
    
    print('aust_shape')

    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('aust_shape', 'all', fname)
    
    p.shp_to_db(fname,'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                      fname, 4823)
    
    print('feat_aust_11_area')
    fname = 'feat_aust_{size}km_sa1_11'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('feat_aust_11','all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                 fname)
    p.shp_to_db(fname,'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    
    print('feat_aust_16_area')
    fname = 'feat_aust_{size}km_sa1_16'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.sql_to_ogr('feat_aust_16','all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                 fname)
    p.shp_to_db(fname,'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                      fname, 4823)
    
    print('tabular_place_wt')   
    p.csv_to_db('2011Census_B18_AUST_SA1_long',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2011Census_B18_AUST_SA1_long')
    p.csv_to_db('2011Census_B21_AUST_SA1_long',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2011Census_B21_AUST_SA1_long')
    p.csv_to_db('2011Census_B22B_AUST_SA1_long',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2011Census_B22B_AUST_SA1_long')
    p.csv_to_db('2016Census_G18_AUS_SA1',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2016Census_G18_AUS_SA1')
    p.csv_to_db('2016Census_G21_AUS_SA1',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2016Census_G21_AUS_SA1')
    p.csv_to_db('2016Census_G22B_AUS_SA1',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                '2016Census_G22B_AUS_SA1')
    fname = 'aust_{shape}_shape_{size}km'.\
            format(shape = p.Shape,\
                   size = p.Radial)
    p.shp_to_db(fname,\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    fname='feat_aust_{size}km_sa1_11'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname,'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                size = p.Radial),\
                fname, 4823)
    fname='feat_aust_{size}km_sa1_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)
    p.shp_to_db(fname,'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                fname, 4823)
    p.shp_to_db('gis_osm_places_free_1',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'gis_osm_places_free_1', 4823)
    p.shp_to_db('gis_osm_roads_free_1',\
                'db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                        size = p.Radial),\
                'gis_osm_roads_free_1', 4823)
    p.sql_to_ogr('shape_pois_shp', 'all_{shape}_{size}'.\
                format(shape = p.Shape,\
                        size = p.Radial), 'POI')
    p.shp_to_db('POI','db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'POI', 4823)
    p.sql_to_ogr('shape_agil_shp',\
                 'all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                'agil')
    p.shp_to_db('agil','db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'agil', 4823)
    p.sql_to_ogr('shape_mbsp_shp', 'all_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                 'mbsp')
    p.shp_to_db('mbsp','db_place_{shape}_{size}'.\
                format(shape = p.Shape,\
                       size = p.Radial),\
                'mbsp', 4823)

    sqlname='tabular_place_wt_{shape}_{size}.txt'.\
             format(shape = p.Shape,\
                    size = p.Radial)
    p.shape_and_size ('spatialite_db',\
                      'tabular_place_wt.txt',\
                      p.Shape, p.Radial, sqlname)
    p.do_spatialite(sqlname,'db_place_{shape}_{size}'.\
                    format(shape = p.Shape,\
                           size = p.Radial))
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"

    print('shape_11_16_place')
    fname='{shape}_{size}km_place_11_16'.\
           format(shape = p.Shape,\
                  size = p.Radial)

    p.sql_to_ogr('shape_11_16_place',\
                 'all_{shape}_{size}'.\
                 format(shape = p.Shape,\
                        size = p.Radial),\
                 fname)

def hexagons(theshape,b_north, b_south, b_east, b_west, theradial):
    fred = Tiles(shape = theshape, north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)
    post = PostProcess()

    print(fred.params())

    hors = fred.horizontal()

    verts = fred.vertical()

    intersects = fred.intersections(hors,verts)

    hexagon_array = fred.hex_array(intersects,len(hors),len(verts))
    hex_points = fred.points_and_polygons(hexagon_array)

    points = random_points(-8, -45, 168, 96,10)

    new_hex_array = fred.points_in_polygon(hexagon_array,points,'Test')

    gj_hexagon = fred.to_geojson(new_hex_array)

    fred.geojson_to_file(gj_hexagon)

    fred.to_shp_tab()

    intersect_poly = fred.neighbours(hex_points)

    post.ref_files()


def boxes(shape,b_north,south,east,west,theradial):
    fred = Tiles(shape = 'box',north = b_north ,
                 south = b_south, east = b_east,
                 west = b_west, radial = theradial)
    post = PostProcess()

    print(fred.params())

    hors = fred.horizontal()

    verts = fred.vertical()

    intersects = fred.intersections(hors,verts)

    box_array = fred.box_array(intersects,len(hors),len(verts))
    box_points = fred.points_and_polygons(box_array)

    points = random_points(-8, -45, 168, 96,10)

    new_box_array = fred.points_in_polygon(box_array,points,'Test')

    gj_box = fred.to_geojson(new_box_array)

    fred.geojson_to_file(gj_box)

    fred.to_shp_tab()

    intersect_poly = fred.neighbours(box_points)

    post.ref_files()



print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:

    (shape, b_north, b_south, b_east, b_west, radial_d) =\
    ['hex', -8, -45, 168, 96, 57]
    do_map('hex',radial_d)
    #hexagons('hex',b_north, b_south, b_east, b_west, radial_d)
else:
    if (len(sys.argv) < 7 ):
        msg = """arguments are \nshape - hex or box \n bounding north\n
bounding south \n bounding east \n bounding west \n radial in km\n \
filename for output\n\nfor hexagon\n 
python3 polygons_new.py hex -8 -45 168 96 212\n\nfor boxes\n\
python3 polygons_new.py box -8 -45 168 96 212\n
"""
        sys.exit(msg)
    else:
        (blah, shape, b_north, b_south, b_east, b_west, radial_d) =\
        sys.argv
        shape=str(shape)
        print(shape)
        if shape == "hex":
            
            fred.hexagons(float(b_north), float(b_south), float(b_east), \
                     west = float(b_west), radial = float(radial_d))
        else:
            if shape == "box":
                boxes(float(b_north), float(b_south), float(b_east), \
                      float(b_west), float(radial_d))
            else:
                print('shape is hex or box')
