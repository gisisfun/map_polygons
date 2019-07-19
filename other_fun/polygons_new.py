import sys
import pandas as pd
import json
from geopy.distance import distance,geodesic
from geojson import Polygon,Feature,FeatureCollection
from math import pow,sqrt
import pandas as pd
import subprocess
import urllib.request
from pyunpack import Archive
import os

#1 deg longitude is about 88 km, 1 deg latitude  is about 110 km
#http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.001July%202016?OpenDocument


def point_radial_distance(self, brng, radial):
    return geodesic(kilometers=radial).destination(point=self, bearing=brng)


def line_intersection(line1, line2):
    # source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def horizontal(east,north,west,south,hor_seq,radial):
    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
    angle = 180
    new_north = north
    #print(east,new_north,south,'\n')
    i = 0
    longitudes = []
    longitudes.append([[north,west],[north,east]])

    while new_north >= south:
        if i > 3:
            i = 0
            
        latlong = [new_north,east]
        p = point_radial_distance(latlong,angle,radial * hor_seq[i]) 
        new_north = p[0]
        longitudes.append([[p[0],west],[p[0],east]])
        i += 1
    return longitudes


def vertical(east,north,west,south,vert_seq,radial):
    print('east {0} west {1}'.format(east,west))
    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
    angle = 90

    i = 0
    new_west = west
    latitudes =[]
    latitudes.append([[north,west],[south,west]])
    while new_west <= east:
        if i > 3:
            i = 0

        latlong = [north,new_west]
        p = point_radial_distance(latlong,angle,radial*vert_seq[i])
        new_west = p[1]
        latitudes.append([[north,p[1]],[south,p[1]]])    
        i += 1
    return latitudes

##def horizontalnew(east,north,west,south,hor_seq,radial):
##    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
##    angle = 180
##    new_north = north
##    #print(east,new_north,south,'\n')
##    i = 0
##    longitudes = []
##    longitudes.append(north)
##
##    while new_north >= south:
##        if i > 3:
##            i = 0
##            
##        latlong = [new_north,east]
##        p = point_radial_distance(latlong,angle,radial * hor_seq[i]) 
##        new_north = p[0]
##        longitudes.append(p[0])
##        i += 1
##    #del longitudes[-1]
##    return longitudes
##
##
##def verticalnew(east,north,west,south,vert_seq,radial):
##    print('east {0} west {1}'.format(east,west))
##    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
##    angle = 90
##
##    i = 0
##    new_west = west
##    latitudes =[]
##    latitudes.append(west)
##    while new_west <= east:
##        if i > 3:
##            i = 0
##
##        latlong = [north,new_west]
##        p = point_radial_distance(latlong,angle,radial*vert_seq[i])
##        new_west = p[1]
##        latitudes.append(p[1])    
##        i += 1     
##    del latitudes[-1]
##    return latitudes


def intersections(hor_line_list, hor_max, vert_line_list, vert_max):
    print('\n3/7 deriving intersection point data between horizontal and \
    vertical lines')
    intersect_list = []
    for h in range(0, hor_max):
        for v in range(0, vert_max):
            intersect_point = line_intersection(hor_line_list[h],
            vert_line_list[v])
            intersect_data = [intersect_point[1], intersect_point[0]]
            intersect_list.append(intersect_data)

    print('derived {0} points of intersection'.format(len(intersect_list)))
    return intersect_list


def params(shape, north, south, east, west, radial):
    print('Making {0} hex shapes starting from {1},{2} to {3},{4} with a \
    radial length of {5} km'.format(shape, north, west, south, east, radial))

def to_shp_tab(f_name,shape):
    my_os = os.name
    if (my_os is 'posix'):
        cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        cmd_text = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash = '\\'
        gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
        os.environ.update(gdal_vars)

    shp_fname = 'shapefiles{slash}{fname}_layer.shp'.format(fname=f_name
    .replace(' ', '_'), slash=slash)
    tab_fname = 'tabfiles{slash}{fname}_layer.tab'.format(fname=f_name
    .replace(' ', '_'), slash=slash)
    json_fname = 'geojson{slash}{fname}_layer.json'.format(fname=f_name
    .replace(' ', '_'), slash=slash)
    tab_options = [cmd_text, '-f', 'Mapinfo file', tab_fname,
    '-t_srs', 'EPSG:4823', json_fname]
    shp_options = [cmd_text, '-f', 'ESRI Shapefile', shp_fname,
    '-t_srs', 'EPSG:4823', json_fname]
    try:
        # record the output!
        print('\nwriting {0} shapefile {1}_layer.shp'.format(shape, f_name))
        subprocess.check_call(shp_options)
        print('\nwriting {0} shapefile {1}_layer.tab'.format(shape, f_name))
        subprocess.check_call(tab_options)
    except FileNotFoundError:
        print('No files processed')


def ref_files():
    my_os = os.name
    if (my_os is 'posix'):
        # cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        # cmd_text = 'C:\\OSGeo\\bin\\ogr2ogr.exe'
        slash = '\\'
    if not os.path.isfile('shapefiles{slash}AUS_2016_AUST.shp'
    .format(slash=slash)):
        print('Downloading ABS Australia file in Shape file format')
        url = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
        urllib.request.urlretrieve(url, 'shapefiles{slash}1270055001_aus_2016_aust_shape.zip'.format(slash=slash))
        print('Unzipping ABS Australia file in Shape file format')
        Archive('shapefiles{slash}1270055001_aus_2016_aust_shape.zip'.format(slash=slash)).extractall('shapefiles'.format(slash=slash))
    else:
        print('ABS Australia file in Shape file format exists')

    if not os.path.isfile('tabfiles{slash}AUS_2016_AUST.tab'
    .format(slash=slash)):
        print('Downloading ABS Australia file in Tab file format')
        url = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&F18065BF058615F9CA2581640014491B&0&July%202016&24.07.2017&Latest'
        urllib.request.urlretrieve(url, 'shapefiles{slash}1270055001_aus_2016_aust_tab.zip'.format(slash=slash))
        print('Unzipping ABS Australia file in Tab file format')
        Archive('shapefiles{slash}1270055001_aus_2016_aust_tab.zip'.format(slash=slash)).extractall('tabfiles'.format(slash=slash))
    else:
        print('ABS Australia file in Tab file format exists')


def boxes(north, south, east, west, radial, outfile):
    params('boxes', north, south, east, west, radial)
    my_os = os.name
    if (my_os is 'posix'):
        # cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        # cmd_text = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash = '\\'
    #init bits
    # poly_list = []
    g_array = []  # array of geojson formatted geometry elements
    tabular_list = []  # array of all polygons and tabular columns
    layer_dict = {'Bounds': {'Australia': {'North': north,'South': south,
         'West': west,'East': east}}}
    layer_dict['Param'] = {}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4326
    layer_dict['Param']['shape'] = 'box'
    layer_dict['Boxes'] = {}
    layer_dict['Boxes']['long'] = 1
    hor_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'],
               layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
    vert_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'],
               layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west

    h_line_list = horizontal(east,north,west,south,vert_seq,radial)
    num_h = len(h_line_list)
    max_h = num_h - 1
    v_line_list = vertical(east,north,west,south,vert_seq,radial)
    num_v = len(v_line_list)
    max_v = num_v - 1
    intersect_list = intersections(h_line_list, max_h, v_line_list, max_v)

    print('\n4/7 deriving boxes polygons from intersection data')
    top_left = 0
    vertex = [top_left + 0, top_left + 1, top_left + max_v + 1,
        top_left + max_v]

    while (vertex[2] < (max_h) * (max_v)):
        poly_coords = [intersect_list[vertex[0]],
            intersect_list[vertex[1]], intersect_list[vertex[2]],
            intersect_list[vertex[3]], intersect_list[vertex[0]]]
        centre_lat = intersect_list[vertex[0]][1]
        + (intersect_list[vertex[2]][1] - intersect_list[vertex[0]][1]) / 2
        centre_lon = intersect_list[vertex[0]][0]
        + (intersect_list[vertex[2]][0] - intersect_list[vertex[0]][0]) / 2
        bounds_n = intersect_list[vertex[0]][1]
        bounds_s = intersect_list[vertex[3]][1]
        bounds_e = intersect_list[vertex[1]][0]
        bounds_w = intersect_list[vertex[0]][0]
        if bounds_e > bounds_w:
            geopoly = Polygon([poly_coords])
            geopoly = Feature(geometry=geopoly,
            properties={"p": top_left, "lat": centre_lat, "lon": centre_lon,
                "N": bounds_n, "S": bounds_s, "E": bounds_e, "W": bounds_w})
            g_array.append(geopoly)
            #append geojson geometry definition attributes to list
            #tabular dataset
            tabular_line = [top_left, centre_lat, centre_lon,
                            bounds_n, bounds_s, bounds_e, bounds_w]
            tabular_list  .append(tabular_line)
            #array of polygon and tabular columns

        #increment values
        top_left += 1
        vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left
        + max_v]

    print('\n5/7 boxes geojson dataset of {0} derived polygons'
    .format(len(g_array)))
    boxes_geojson = FeatureCollection(g_array)
    # convert merged geojson features
    #to geojson feature geohex_geojson
    g_array = []  # release g_array - array of geojson geometry elements

    print('writing boxes geojson formatted dataset to file: {0}.json'
    .format(outfile))
    myfile = open('geojson{slash}{outfile}_layer.json'
    .format(outfile=outfile, slash=slash), 'w')
    #open file for writing geojson layer in geojson format
    myfile.write(str(boxes_geojson))  # write geojson layer to open file
    myfile.close()  # close file

    print('\n6/7 tabular dataset of {0} lines of boxes polygon data'
    .format(len(tabular_list)))
    print('writing tabular dataset to file: {0}_dataset.csv'.format(outfile))
    tabular_df = pd.DataFrame(tabular_list)
    #convert tabular array to tabular data frame
    tabular_df.columns = ['poly', 'lat', 'long', 'N', 'S', 'E', 'W']
    layer_dict['Bounds']['Dataset'] = {}
    #update layer_dict with dataset bounds
    layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
    layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
    layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
    layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min()
    tabular_df.to_csv('csv{slash}{outfile}_dataset.csv'.format(outfile=
    outfile, slash = slash), sep = ',')


    print('\n7/7 boxes json metadata to written to file: {0}_metadata.json'
    .format(outfile))
    myfile = open('metadata{slash}{outfile}_metadata.json'.format(outfile=
    outfile, slash=slash), 'w')  # open file for writing geojson layer
    myfile.write(str(json.dumps(layer_dict)))
    #write geojson layer to open file
    myfile.close()  # close file
    to_shp_tab(outfile, 'boxes')
    ref_files()
    print('\n')
    print('The End')  # end boxes


def hexagons(north, south, east, west, radial, outfile):

    params('heagons', north, south, east, west, radial)
    my_os = os.name
    if (my_os is 'posix'):
        # cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        # cmd_text = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash = '\\'
    # init bits
    point_list = []
    g_array = []  # array of geojson formatted geometry elements
    tabular_list = []  # array of all polygons and tabular columns
    layer_dict = {'Bounds': {'Australia': {'North': north, 'South': south,
        'West': west, 'East': east}}}
    layer_dict['Param'] = {}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4326
    layer_dict['Param']['shape'] = 'hexagon'
    layer_dict['Hexagon'] = {}
    layer_dict['Hexagon']['short'] = 0.707108
    layer_dict['Hexagon']['long'] = 1

    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west

    hor_seq = [layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'],
    layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short']]

    vert_seq = [layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'],
    layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']]

    h_line_list = horizontal(east, north,
                            west, south,
                            hor_seq, radial)
    max_h = len(h_line_list)

    v_line_list = vertical(east, north,
                              west, south,
                              vert_seq, radial)
    max_v = len(v_line_list)

    intersect_list = intersections(h_line_list, max_h, v_line_list, max_v)
    
    lat_offset = 4
    top_left = 0
    poly_row_count = int(max_v / (len(hor_seq)))
    rem_lat = max_v % (lat_offset + len(hor_seq))
    layer_dict['Row_1'] = {}
    layer_dict['Row_1']['lat_offset'] = lat_offset
    layer_dict['Row_1']['poly_row_count'] = poly_row_count
    layer_dict['Row_1']['remain_lat'] = rem_lat

    print('first row starting from {0}, {1} hexagons, {2} \
    latitude line(s) remaining'.format(top_left, poly_row_count, rem_lat))

    inc_by_rem = True
    inc_adj = 0
    if rem_lat is 0 or rem_lat is 1 or rem_lat is 2 or rem_lat is 3 \
    or rem_lat is 4 or rem_lat is 5 or rem_lat is 6 or rem_lat is 7:

        if rem_lat is 2 or rem_lat is 5 or rem_lat is 6 or rem_lat is 7:
            inc_by_rem = True
            inc_adj = -4
        if rem_lat is 1 or rem_lat is 3:
            inc_by_rem = True
            inc_adj = 0
        if rem_lat is 0 or rem_lat is 4:
            inc_by_rem = False
            inc_adj = 0

        print('\n4/7 deriving hexagon polygons from intersection data')
        row = 1
        last_lat_row = 0
        hexagon = 0
        row = 1
        while (top_left < (max_h) * (max_v)):
            vertex = [1 + top_left, 2 + top_left, max_v + 3 + top_left,
            (max_v * 2) + 2 + top_left, (max_v * 2) + 1 + top_left, max_v +
             top_left]
            try:
                poly_coords = [intersect_list[vertex[0]],
                intersect_list[vertex[1]], intersect_list[vertex[2]],
                intersect_list[vertex[3]], intersect_list[vertex[4]],
                intersect_list[vertex[5]], intersect_list[vertex[0]]]
                centre_lat = intersect_list[vertex[0]][1]
                + (intersect_list[vertex[5]][1]
                   - intersect_list[vertex[0]][1]) / 2
                centre_lon = intersect_list[vertex[0]][0]
                + (intersect_list[vertex[5]][0] -
                intersect_list[vertex[0]][0]) / 2

                if (centre_lat is not last_lat_row) or last_lat_row is 0:
                    bounds_n = intersect_list[vertex[0]][1]
                    bounds_s = intersect_list[vertex[2]][1]
                    bounds_e = intersect_list[vertex[2]][0]
                    bounds_w = intersect_list[vertex[5]][0]
                    last_lat_row = centre_lat
                    geopoly = Polygon([poly_coords])
                    hexagon += 1
                    # start = (intersect_list[vertex[0]][1],
                    # intersect_list[vertex[0]][0])
                    # end = (intersect_list[vertex[1]][1],
                    # intersect_list[vertex[1]][0])
                    # len_radial = geodesic(start,end).km
                    est_area = (((3 * sqrt(3)) / 2) * pow(radial, 2)) * 0.945
                    #estimate polygon area
                    geopoly = Feature(geometry = geopoly, properties =
                    {"p": hexagon,"row": row, "lat": centre_lat
                    , "lon": centre_lon, "N": bounds_n, "S": bounds_s
                    , "E": bounds_e, "W": bounds_w, "est_area": est_area})
                    if  (bounds_e > bounds_w):
                        for i in range(0, 5):
                            point_list.append(
                                [hexagon, str(intersect_list[vertex[i]][0])
                                + str(intersect_list[vertex[i]][1])])
                        g_array.append(geopoly)
                        #append geojson geometry definition attributes to list
                        #tabular dataset
                        tabular_line = [top_left, row, centre_lat, centre_lon,
                        bounds_n, bounds_s, bounds_e, bounds_w, est_area]
                        tabular_list.append(tabular_line)
                        #array of polygon and tabular columns
                else:
                    donothing = True

            except IndexError:
                donothing = True

            last_row = row
            last_lat_row = centre_lat
            row = int(1 + int(hexagon / poly_row_count))
            top_left += lat_offset
            if row is not last_row:
                top_left += inc_adj
                if inc_by_rem:
                    top_left += rem_lat
                if row % 2 is 0:
                    top_left += 2
                if row & 1:
                    top_left += -2

        print('\n5/7 geojson dataset of {0} derived hexagon polygons'
        .format(len(g_array)))
        boxes_geojson = FeatureCollection(g_array)
        # convert merged geojson features to geojson feature geohex_geojson
        g_array = []  # release g_array - array of geojson geometry elements

        print('writing geojson formatted hexagon dataset to file: {0}.json'
        .format(outfile))
        myfile = open('geojson{slash}{outfile}_layer.json'
        .format(outfile=outfile, slash=slash), 'w')
        #open file for writing geojson layer in geojson format
        myfile.write(str(boxes_geojson))  # write geojson layer to open file
        myfile.close()  # close file

        print('\n6/7 tabular dataset of {0} lines of hexagon polygon data'
        .format(len(tabular_list)))
        print('writing tabular dataset to file: {0}_dataset.csv'
        .format(outfile))
        point_df = pd.DataFrame(point_list)
        point_df.columns = ['poly', 'latlong']
        point_df.to_csv('csv{slash}{outfile}_points.csv'
        .format(outfile=outfile, slash=slash), sep=',')
        point_df_a = point_df  # make copy of dataframe
        process_point_df = pd.merge(point_df, point_df_a, on='latlong')
        # merge columns of same dataframe on concatenated latlong
        process_point_df = process_point_df[(process_point_df['poly_x']
        != process_point_df['poly_y'])]  # remove self references
        output_point_df = process_point_df[['poly_x', 'poly_y']].copy().sort_values(by=['poly_x']).drop_duplicates()
        #just leave polygon greferences and filter output

        output_point_df.to_csv('csv{slash}{outfile}_neighbours.csv'.format(outfile=outfile, slash=slash), sep=',', index = False)
        #print(output_point_df['poly_y',0])


        tabular_df = pd.DataFrame(tabular_list)
        #convert tabular array to tabular data frame
        tabular_df.columns = ['poly', 'row', 'lat', 'long', 'N',
        'S', 'E', 'W', 'area']
        layer_dict['Bounds']['Dataset'] = {}
        #update layer_dict with dataset bounds
        layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
        layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
        layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
        layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min()
        tabular_df.to_csv('csv{slash}{outfile}_dataset.csv'.format(outfile=outfile,slash=slash), sep=',', index = False)

        print('\n7/7 hexagons json metadata to written to file:\
         {0}_metadata.json'.format(outfile))
        myfile = open('metadata{slash}{outfile}_metadata.json'
        .format(outfile=outfile, slash=slash), 'w')
        #open file for writing geojson layer
        myfile.write(str(json.dumps(layer_dict)))
        #write geojson layer to open file
        myfile.close()  #close file

        to_shp_tab(outfile, 'hexagons')
        ref_files()

    print('\n')
    print('The End')  # hexagons


print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
#    (shape, b_north, b_south, b_east, b_west, radial_d, f_name) =
#    ['box', -8, -45, 168, 96, 55, 'box_55km']
#    boxes(b_north, b_south, b_east, b_west, radial_d, f_name)
    (shape, b_north, b_south, b_east, b_west, radial_d, f_name) =\
    ['hex', -8, -45, 168, 96, 57, 'hex_57km']
    hexagons(b_north, b_south, b_east, b_west, radial_d, f_name)
else:
    if (len(sys.argv) < 8 ):
        sys.exit("arguments are \nshape - hex or box \n bounding north\n \
        bounding south \n bounding east \n bounding west \n radial in km\n \
        filename for output\n\nfor hexagon\n\
        python3 polygons.py hex -8 -45 168 96 212 hex_212km\n\nfor boxes\n\
        python3 polygons.py box -8 -45 168 96 212 box_212km\n")
    else:
        (blah, shape, b_north, b_south, b_east, b_west, radial_d, f_name) =\
        sys.argv
        shape=str(shape)
        print(shape)
        if shape == "hex":
            hexagons(float(b_north), float(b_south), float(b_east),
            float(b_west), float(radial_d), f_name)
        else:
            if shape == "box":
                boxes(float(b_north), float(b_south), float(b_east),
                float(b_west), float(radial_d), f_name)
            else:
                print('shape is hex or box')
