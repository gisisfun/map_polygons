"""
General file and data support for geospatial text and binary data sets
"""

import os
import csv
import urllib.request
import json
from pyunpack import Archive
import numpy as np
import shapefile
from geographiclib.geodesic import Geodesic
from pycrs.load import from_file
import simplekml
from mapclassify import EqualInterval, NaturalBreaks, MaximumBreaks, \
BoxPlot, Quantiles, Percentiles, FisherJenks, StdMean, UserDefined
import yaml
import pandas as pd
import matplotlib.path as mpltPath

from geojson import FeatureCollection, Polygon, Feature

#https://automating-gis-processes.github.io/CSC18/lessons/L1/Intro-Python-GIS.html

def polygon_area(poly):
    #geod = Geodesic(6378388, 1/297.0) # the international ellipsoid
    geod = Geodesic.WGS84
    p = geod.Polygon()

    poly = [
            [-63.1, -58], [-72.9, -74], [-71.9,-102], [-74.9,-102], [-74.3,-131],
            [-77.5,-163], [-77.4, 163], [-71.7, 172], [-65.9, 140], [-65.7, 113],
            [-66.6,  88], [-66.9,  59], [-69.8,  25], [-70.0,  -4], [-71.0, -14],
            [-77.3, -33], [-77.9, -46], [-74.7, -61]
            ]
    for pnt in poly:
        p.AddPoint(pnt[0], pnt[1])
    num, perim, area = p.Compute()
    return area

def point_radial_distance(coords, brng, radial):
    """
    Calulate next point from coordinates and bearing

    Dependencies:
    None
    """
    #geod = Geodesic(6378388, 1/297.0) # the international ellipsoid
    geod = Geodesic.WGS84
    g = geod.Direct(coords[0], coords[1], brng, radial * 1000)
    return  g['lat2'], g['lon2']

def tabular_dataframe(g_array):
    """
    Not Implemented to date

    g_array: geojson Polygon data in array
    """

    tabular_list = []
    for dict_val in iter(g_array):
        tabular_list.append(dict_val['properties'])

    tabular_data_df = pd.DataFrame(tabular_list)

    return tabular_data_df

def from_yaml(yaml_text):
    """
    Conversion of yaml format string to json format string

    input:
        string content in yaml format

    Output:
        string content in json format
    """
    json_text = yaml.safe_load(yaml_text)
    return json_text

def to_yaml(json_text):
    """
    Conversion of yaml format string to json format string

    input:
        string content in json format

    Output:
        string content in yaml format
    """
    yaml_text = yaml.dump(json_text, stream=None)
    #customise to keywords
    #help(yaml.dumper)
    #**kwds
    #default_style : indicates the style of the scalar. Possible values are None, '', '\'', '"', '|', '>'.
    #default_flow_style :  indicates if a collection is block or flow. The possible values are None, True, False.
    #canonical : if True export tag type to the output file
    #indent :  sets the preferred indentation
    #width : set the preferred line width
    #allow_unicode : allow unicode in output file
    #line_break : specify the line break you need
    #encoding : output encoding, defaults to utf-8
    #explicit_start : if True, adds an explicit start using “—”
    #explicit_end: if True, adds an explicit end using “—”
    #version : version of the YAML parser, tuple (major, minor), supports only major version 1
    #tags : I didn’t find any information about this parameter … and no time to test it ;-). Comments are welcome !
    return yaml_text


def to_geojson_fmt(g_array):
    """
    Conversion of geojson Polygon data in array to FeatureCollection

    Input:
        g_array: geojson Polygon data in array

    Output:
        Feature Collection of geojson Polygon data in array
    """

    return FeatureCollection(g_array)


def f_name(shape, radial):
    """
    Construct filename string
    Input Variables
        shape: 'hex' or 'box'
        radial: length of radial segment measures in units of km

    Output:
        Text string 'shape'_'radial'km
    """

    #print(self.shape + '_' + str(self.radial) + 'km')
    return shape + '_' + str(radial) + 'km'


def file_deploy(resource_data, slash='/'):
    """
    Deploy downloaded files

    Input:
        resource_data: dictionary string containing file configuration data
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    Output:
        files dwonloaded if necessary and deployed to file system with
        reference to os dependant slash
    """

    if not os.path.isfile(resource_data['file_path'].replace('/', slash)):
        print('Downloading {} file in {} file format'\
              .format(resource_data['format'], resource_data['description']))

        try:
            urllib.request.urlretrieve(resource_data['down_url'],
                                       resource_data['zip_path'].\
                                       replace('/', slash))
        except urllib.error.HTTPError:
            print("URL not found")
        if resource_data['zip_path'].endswith('zip') is True:
            print('Unzipping {} file in {} file format'\
                .format(resource_data['description'], resource_data['format']))
            print('extracting files')
            Archive(resource_data['zip_path'].replace('/', slash)).\
                    extractall(resource_data['zip_dir'].replace('/', slash))
    else:
        print('{} file in {} file format exists'\
              .format(resource_data['description'], resource_data['format']))



def ref_files_polygons(def_file, path_datasets='jsonfiles', slash='/'):
    """
    Get reference files for polygons.py

    Input:
        json_files_path: path to diectory with json formatted files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
        file_name: name of defintions file in 'json' format with .json' extension

    Output:
        files dwonloaded if necessary and deployed to file system
    """
    def_file = 'datasets'
    datasets = from_json_file(def_file, path_datasets, slash)
    ref_data = datasets['DataSets']['Australia']['ShapeFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['AGILDataset']['CSVFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['MBSP']['CSVFormat']
    file_deploy(ref_data)

    ref_data = datasets['DataSets']['NASAActiveFireData']['ModisC61km']['CSVFormat']
    file_deploy(ref_data)


def ref_files_poly_wt(file_name='datasets', json_files_path='jsonfiles', slash='/'):
    """
    Get reference files for poly_wt.py

    Input:
        json_files_path: path to diectory with json formatted files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
        file_name: name of defintions file in 'json' format with .json' extension

    Output:
        files dwonloaded if necessary and deployed to file system
    """
    #def_file = 'datasets'
    datasets = from_json_file(file_name, json_files_path, slash)

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

def coords_from_csv_latin1(file_name, lon_col, lat_col, csv_files_path='csv',\
                           slash='/'):
    """
    Reads files with illegal characters causing errors

    Input:
        file_name: name of csv file with '.csv' extension
        lon_col: number of column starting fron 0 holding x or longitude values
        lat_col: number of column starting fron 0 holding y or latitude values
        csv_files_path: path to location of csv files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    Output:
        coords: array of x and y values
    """

    csv.register_dialect(
        'mydialect',
        delimiter=',',
        quotechar='\'',
        doublequote=True,
        skipinitialspace=True,
        lineterminator='\r\n',
        quoting=csv.QUOTE_MINIMAL)

    with open('{}{}{}'.format(csv_files_path, slash, file_name),
              encoding='latin1') as csvfile:
        data = list(csv.reader(csvfile, dialect='mydialect'))

    longs = []
    lats = []

    for i in range(1, len(data)-1):
        #print('')
        try:
            longs.append(float(data[i][lon_col]))
            lats.append(float(data[i][lat_col]))
        except IndexError:
            pass
        except ValueError:
            pass

    coords = [(x, y) for x, y in zip(longs, lats)]
    return coords

def coords_from_csv(file_name, lon_col, lat_col, csv_files_path='csv', slash='/'):
    """
    Reads standard csv files

    Input:
        file_name: name of csv file without '.csv' extension
        lon_col: number of column starting fron 0 holding x or longitude values
        lat_col: number of column starting fron 0 holding y or latitude values
        csv_files_path: path to location of csv files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'

    Output:
        coords: array of x and y values
    """

    csv.register_dialect(
        'mydialect',
        delimiter=',',
        quotechar='\'',
        doublequote=True,
        skipinitialspace=True,
        lineterminator='\r\n',
        quoting=csv.QUOTE_MINIMAL)


    with open('{}{}{}'.format(csv_files_path, slash, file_name),
              newline='', encoding='utf-8') \
              as csvfile:
        data = list(csv.reader(csvfile, dialect='mydialect'))

    longs = [float(item[lon_col]) for item in data[1:]]
    lats = [float(item[lat_col]) for item in data[1:]]
    coords = [(x, y) for x, y in zip(longs, lats)]
    return coords

def from_json_file(file_name, json_files_path='jsonfiles', slash='/'):
    """
    Reads 'json' formated file from file source

    Input variables:
        file_name: name of json format file with '.json' extension
        json_files_path: path to location of json files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'

    Output:
        json_dict: disctionary string with configuration data
    """

    full_file_path = '{}{}{}.json'.format(json_files_path, slash, file_name)
    json_file = open(full_file_path, "r")
    json_file_text = json_file.read()
    json_dict = json.loads(json_file_text)
    json_file.close()
    return json_dict

def points_in_polygon(g_array, lat_longs, g_label):
    """
    Points in polygon counts for list of supplied coordinates generated

    Input:
        g_array: array of geojson polygon data
        lat_longs: list of supplied coordinates as x or longitude, y or latitude
        g_label: name of coumn to be appended to each polygon record

    Output:
        g_array: array of geojson polygon data with new data item
    """

    lat_longs_df = pd.DataFrame(lat_longs)
    lat_longs_df.columns = ['longitude', 'latitude']
    for poly, poly_data in enumerate(g_array):
        p_count = 0
        bound_points_df = lat_longs_df[(lat_longs_df['latitude'] >=\
                                        poly_data['properties']['S']) & \
                                       (lat_longs_df['latitude'] <=\
                                        poly_data['properties']['N']) & \
                                       (lat_longs_df['longitude'] <=\
                                        poly_data['properties']['E']) & \
                                       (lat_longs_df['longitude'] >=\
                                        poly_data['properties']['W'])]
        #this is dodgy but it works for now
        if bound_points_df.size == 2:
            bound_points_df.append(bound_points_df)

        if bound_points_df.size > 0:
            poly_coords = []
            #num_coords = len(g_array[poly]['geometry']['coordinates'][0])-2
            coords_list = g_array[poly]['geometry']['coordinates'][0]
            longs = [item[0] for item in coords_list]
            lats = [item[1] for item in coords_list]
            poly_coords = [(x, y) for x, y in zip(longs, lats)]
            path = mpltPath.Path(poly_coords)

            for index, row in bound_points_df.iterrows():
                if path.contains_point([row['longitude'], \
                                        row['latitude']]) is True:
                    p_count += 1

        poly_data['properties'][g_label] = float(p_count)

    return g_array

def get_geojson_crs(file_name, geojson_files_path='geojson', slash='/'):
    """
    Reads CRS value for geojson file

    Input variables:
        file_name: name of shape file with '.json' extension
        geojson_path: path to location of geojson files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    """
    full_file_path = "{}{}{}.json".format(geojson_files_path, slash, file_name)
    return from_file(full_file_path)


def from_geojson_file(file_name, geojson_files_path='geojson', slash='/'):
    """
    Reads GeoJSON data set from file

    Input:
        file_name: name of gejson file with '.json' extension
        geojson_files_path: path to location of geojson files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    Output:
        g_array: array of geojson polygon data sourced from
                 file system geojson file
    """

    print('reading geojson formatted dataset from file:{}.json'.
          format(file_name))
    my_file = open('{}{}{}.json'.format(geojson_files_path, slash, file_name), 'r')
    #open file for reading geojson layer in geojson format
    gj_data = my_file.read()
    # read geojson layer to open file
    gj_dict = json.loads(gj_data)
    print(gj_dict)
    g_array = []
    for row_data in iter(gj_dict['features']):
        g_array.append(row_data)
    my_file.close()  # close file
    return g_array


def to_geojson_file(g_array, file_name, geojson_files_path='geojson', \
                    slash='/'):
    """
    Write string to file

    Prerequisites:
    to_geojson, hex_array or box_array, horizontal, vertical, Tiles

    Input variables:
        g_array: array of geojson polygon data
        file_name: filename without ',json' extension
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
        geojson_files_path: path to locationo of geojson files

    Output:
        geojson file written to file system
    """
    content = FeatureCollection(g_array)
    print('writing geojson formatted dataset to file:' +\
           file_name +'.json')
    my_file = open('{}{}{}.json'.format(geojson_files_path, slash,
                                        file_name), 'w')
    #open file for writing geojson layer in geojson format
    my_file.write(str(content))  # write geojson layer to open file
    my_file.close()  # close file


def get_shapefile_crs(file_name, shapefile_files_path='shapefiles', slash='/'):
    """
    Reads CRS value for shapefile

    Input variables:
        file_name: name of shape file with '.shp' extension
        shape_file_path: path to location of shapefiles
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    """
    full_file_path = "{}{}{}.prj".format(shapefile_files_path, slash, file_name)
    return from_file(full_file_path)


def from_shp_file(file_name, shape_files_path='shapefiles', slash='/'):
    """
    Reads shapefile Polgon or Multipolygon into a Polygon based Geojson arry

    Assumes WGS84 epsg 4326

    Input variables:
        file_name: name of shape file with '.shp' extension
        shape_file_path: path to location of shapefiles
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'

    Output:
        g_array: array of geojson polygon data
    """

    #fName,fPath
    #tabular_list = []

    shape_file_full_path = '{}{}{}'.format(shape_files_path, slash, file_name)
    shape_file = shapefile.Reader(shape_file_full_path)
    shapes = shape_file.shapes()
    #how many empty and real polgons and subpolygons
    shapes_list = []
    for i, poly in enumerate(shapes):
        shapes_list.append([len(poly.points), len(poly.parts)])
    #[shapes_list.append([len(x.points), len(x.parts)]) for x in shapes]

    # add a row_id reference
    shapes_list_with_row_id = []
    for row, row_data in enumerate(shapes_list):
        shapes_list_with_row_id.append([row, row_data[0], row_data[1]])

    # drop all array rows ith 0 parts
    shapes_list_no_null = []
    for row, row_data in enumerate(shapes_list_with_row_id):
        if row_data[2] > 0:
            shapes_list_no_null.append(row_data)

    #get the field names
    fields = shape_file.fields
    column_list = []
    for field_data in iter(fields[1:]):
        column_list.append(field_data[0])

    # data values with null geography
    tab_data = shape_file.records()

    tab_data_val = []
    row_ref = []

    for tab_row, row_data in enumerate(shapes_list_no_null):
        # all rows    #for column_name in column_list:
        row_data_list = [] #shapes_list_no_null[tab_row][0]]

        for tab_val in tab_data[row_data[0]]:
            # each row of tab data (y)
            row_ref.append(tab_row)
            row_data_list.append(tab_val) #,len(shapes[tab_row].points)])

        tab_data_val.append(row_data_list)

    geojson_properties_list = []
    for tab_row, row_data in enumerate(tab_data_val):
        dataset_dict_row = {}
        for column, column_data in enumerate(column_list):
            dataset_dict_row[column_data] = row_data[column]
        geojson_properties_list.append(dataset_dict_row)

    # make a parts list find numbers of points
    parts_list = []
    parts_count = []
    points_len = []
    for i  in range(len(tab_data_val)):
        the_list = shapes[row_ref[i]].parts
        parts_list.append(the_list)
        the_list = shapes[row_ref[i]].parts
        parts_count.append(len(shapes[row_ref[i]].parts))
        points_len.append(len(shapes[row_ref[i]].points))

    g_array = []
    for i, gj_prop_val in enumerate(geojson_properties_list):
        parts_list[i].append(points_len[i])
        shapes_ref = row_ref[i]
        #thing.append([geojson_properties_list[i],parts_count[i],parts_list[i]])

        for j in range(0, parts_count[i]):
            geopoly = Polygon([shapes[shapes_ref].\
                               points[parts_list[i][j]:parts_list[i][j+1]]])
            geopoly = Feature(geometry=geopoly, \
                              properties=gj_prop_val)

            g_array.append(geopoly)
    return g_array


def to_shp_file(g_array, file_name, shape_files_path='shapefiles', slash='/'):
    """
    Write geojson Polygon array to shapefile format

    Assumes WGS 84 epsg 4326 projection

    input:
        g_array: array of geojson polygon data
        file_name: shape file file name without extension
        shape_files_path: path to location of shape files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'

    Output:
        files written to file system in shapefile format
    """

    #tabular_list = []
    shp_path = shape_files_path + slash + file_name
    prj_path = shp_path + '.prj'
    w_file = shapefile.Writer(shp_path) # , shapeType=3)
    #setup columns
    for key in iter(g_array[0]['properties']):

        if isinstance(g_array[0]['properties'][key], int):
            w_file.field(key, 'N')
        if isinstance(g_array[0]['properties'][key], float):
            if int(g_array[0]['properties'][key]) != \
            g_array[0]['properties'][key]:
                w_file.field(key, 'F', decimal=10)
            else:
                w_file.field(key, 'N')
        if isinstance(g_array[0]['properties'][key], str):
            w_file.field(key, 'C')

    for row, dict_val in enumerate(g_array):
        myargs = {}
        #print('props_list',len(props_dict))
        for key in iter(dict_val['properties']):
            myargs[key] = str(dict_val['properties'][key])

        w_file.record(**myargs)
        w_file.poly([g_array[row]['geometry']['coordinates'][0]])
    w_file.close()
    # create the PRJ file
    msg = 'writing shapefile formatted dataset to file:' + \
    shp_path +'.shp'
    print(msg)
    prj = open(prj_path, "w")
    epsg = 'GEOGCS["WGS 84",'
    epsg += 'DATUM["WGS_1984",'
    epsg += 'SPHEROID["WGS 84",6378137,298.257223563]]'
    epsg += ',PRIMEM["Greenwich",0],'
    epsg += 'UNIT["degree",0.0174532925199433]]'
    prj.write(epsg)
    prj.close()


def apply_classification(g_array, ref_col):
    """
    Apply cloreplath colour classification range to array of geojson polygon data

    Input:
        g_array: array of geojson polygon data
        ref_col: column of array used as reference for chloreplath colour values

    Output:
        colour_breaks: array of colour values for each chloreplath break value
        customised for each data value in column
    """
    #get the values_list
    values_list = []
    for val in iter(g_array):
        values_list.append(val['properties'][ref_col])

    the_breaks = NaturalBreaks(values_list, 5)
    print(the_breaks, '\n', the_breaks.bins, '\n')

    break_list = []
    for list_value in iter(values_list):
        classed = False
        the_breaks_ref = 0
        for break_value in iter(the_breaks.bins):
            if list_value >= break_value and classed is False:
                the_breaks_ref = break_value
                classed = True
        break_list.append(the_breaks_ref)
        #old
        #break_list.append(classify(the_breaks.bins, val))

    # kml alpha format #AABBGGRR
    c_hex_a_ref = ['ZZ000099', 'ZZ001AA6', 'ZZ0033B3', 'ZZ004DBF', 'ZZ004DCC',
                   'ZZ0066CC', 'ZZ0080D9', 'ZZ0099E6', 'ZZ0320FB', 'ZZ00CCFF']
    c_hex_a = []
    for val in iter(c_hex_a_ref):
        c_hex_a.append(val.replace('ZZ', 'FF'))

    break_distinct = list(dict.fromkeys(break_list))

    #values_break = []
    old_val = []
    colour_breaks = []
    for val in iter(values_list):
        new_val = values_list.index(val) #[i for i, e in enumerate(values_n) if e is val]
        if new_val != old_val:
            #look up rgb colour values
            color_index = break_distinct.index(break_list[new_val])

            old_val = new_val
        #rgb_breaks.append(c_rgb[color_index])
        colour_breaks.append(c_hex_a[color_index])
    return colour_breaks


def to_kml_file(g_array, file_name, \
                kml_files_path='kmlfiles', slash='/', \
                the_key="No_Key"):
    """
    Writes geojson Polygon array to kml file

    Input:
        g_array: array of geojson polygon data
        file_name: name of kml file without '.kml' extension
        the_key: name of coulmn used for thematic data processing
        kml_files_path: path to location of kml files
        slash: os dependant directory delimiter:
               forward slash '/' - 'posix'
               backwards slash '\\' - 'nt'
    Output:
        KML filw wriiten to file system
     """
    ###
    # Start New Bit
    if the_key != "No_Key":
        poly_list = apply_classification(g_array, the_key)

    # End New Bit
    ###
    full_file_path = '{}{}{}.kml'.format(kml_files_path, slash, file_name)
    kml = simplekml.Kml()

    #setup columns
    props_dict = g_array[0]['properties']

    key_names_array = []
    for key in props_dict:
        key_names_array.append(key)

    for poly, val in enumerate(g_array):
        (i, key_values_array) = (0, [])
        rec_descr = ""
        for key in props_dict:
            key_values_array.append(val['properties'][key])

            if i is not len(props_dict)-1:
                rec_descr = rec_descr + key + ' = ' \
                + str(val['properties'][key]) + '\n'
            else:
                rec_descr = rec_descr + key + ' = ' \
                + str(val['properties'][key]) + '\n'
            i += 1

        (points_str, points_t) = ("[", [])
        for points in g_array[poly]['geometry']['coordinates'][0]:
            points_t.append(tuple(points))
            points_str = points_str + "("\
                         + str(points[0]) + ","\
                         + str(points[1]) + "), "

        pol = kml.newpolygon(name=str(key_values_array[0]))
        pol.outerboundaryis = points_t
        pol.innerpoundaryis = points_t

        pol.description = rec_descr
        #pol.style.polystyle.fill = 0 # fill is off
        ###
        # Start Bit Start
        # transparency yes
        pol.style.polystyle.outline = 1 # outline is visible
        pol.style.polystyle.fill = 0 # fill is not visible
        if the_key != "No_Key":
            if val['properties'][the_key] == 0:
                pol.style.polystyle.outline = 0 # outline is not visible
                pol.style.polystyle.fill = 0 # fill is not visible
            else:
                pol.style.polystyle.outline = 1 # outline is visible
                pol.style.polystyle.fill = 1 # fill is visible

            pol.style.polystyle.color = simplekml.Color.hexa(poly_list[poly])

        # End Bit Start
        ###

    msg = 'writing kml formatted {} dataset to file:' + file_name +'.kml'
    the_shape = 'None'
    print(msg.format(the_shape))
    kml.save(full_file_path)


def points_and_polygons(g_array):
    """
    Neighbouring Polygons derivation

    Prerequisites:
    hex_array or box_array, horizontal, vertical ,Tiles

    Input variables:
        g_array: array of geojson polygon data

    Output:
        point_list: array of points with id, x and y values
    """

    point_list = []

    for poly in iter(g_array):
        #num_coords = len(poly['geometry']['coordinates'][0])-2
        poly_id = poly['properties']['p']
        #for i in range(0, num_coords):
        for i in iter(poly['geometry']['coordinates'][0][:-2]):
            point_list.append( \
                [poly_id,
                 str(poly['geometry']['coordinates'][0][i][0]) + \
                 str(poly['geometry']['coordinates'][0][i][1])])
    return point_list


def add_poly_nb(g_array, poly_col):
    """
    Intersecting polygons list



    Input variables:
    g_array: array of points with id, x and y values

    Output:
    list of neighbouring polygons wrtten to file system
    """
    points_list = []
    for poly_data in iter(g_array):
        poly = poly_data['properties'][poly_col]
        for point in iter(poly_data['geometry']['coordinates'][0]):
            latlong = str(point[0]) + str(point[1])
            points_list.append([poly, latlong])

    point_df = pd.DataFrame(points_list)

    point_df.columns = ['poly', 'latlong']
#    point_df.to_csv('{}{}{}_points.csv'.format(csv_files_path,
#                                               slash, file_name), sep=',')
    point_df_copy = point_df  # make copy of dataframe
    process_point_df = pd.merge(point_df, point_df_copy, on='latlong')
    # merge columns of same dataframe on concatenated latlong
    process_point_df = process_point_df[(process_point_df['poly_x']
                                         != process_point_df['poly_y'])]
    # remove self references
    output_point_df = process_point_df[['poly_x', 'poly_y']].\
                        copy().sort_values(by=['poly_x']).drop_duplicates()

    for g_rec, poly_data in enumerate(g_array):
        is_poly = output_point_df['poly_x'] == \
        poly_data['properties'][poly_col]
        poly_df = output_point_df[is_poly]
        neighbours = ""
        for index, row in poly_df.iterrows():
            neighbours = neighbours + str(row['poly_y']) + "|"
        g_array[g_rec]['properties']['p_NB'] = neighbours[:-1]
    #just leave polygon greferences and filter output

#    output_point_df.to_csv('{}{}{}_neighbours.csv' \
#                           .format(csv_files_path, slash,\
#                                   file_name),\
#                           sep=',', \
#                           index=False)
    return g_array

def poly_drop(g_array,key):
    """
    Drop polygons by condition
    
    Input:
    Input variables:
        g_array: array of geojson polygon data
        key: dictionary key for geojson polygon used to drop records
        
    Output:
        isect_array: array of geojson polygon data with selected array rows        
    """
    isect_array = []

    for poly_data in iter(g_array):
        if poly_data['properties'][key] > 0:
            isect_array.append(poly_data)
    return isect_array

def random_points_in_polygon(poly):
    """
    Creates random points as defined by a polygon

    Input:
        poly: points definition of a polygon

    Output:
        r_coords: array of x and y coordinates contained in a polygon
    """

    #path_contains_path, path_contains_points Doh! did not know about this
    np_arr = np.array(poly)
    arr_min = np.min(np_arr, axis=0)
    arr_max = np.max(np_arr, axis=0)
    min_x, min_y, max_x, max_y = (arr_min[0], arr_min[1], \
                                  arr_max[0], arr_max[1])

    longs = np.arange(min_x, max_x, 0.002)
    lats = np.arange(min_y, max_y, 0.002)

    longs = np.tile(longs, 3).ravel()
    lats = np.repeat(lats, 3).ravel()

    coords = np.array([(x, y) for x, y in zip(longs, lats)])

    path = mpltPath.Path(poly)
    r_coords = []
    for coord in coords:
        if path.contains_point([coord[0], coord[1]]) is True:
            r_coords.append([coord[0], coord[1]])

    return r_coords
