"""
General file and data suport for geospatial text and binary data
"""

import os
import csv
import urllib.request
import json
from pyunpack import Archive
import numpy as np
import shapefile
import simplekml


import pandas as pd
import matplotlib.path as mpltPath

from isotiles.parameters import Defaults
from isotiles.datasets import DataSets
from geojson import FeatureCollection, Polygon, Feature

class Util():
    """
    Generic Geospatial funcionality
    """
    defaults = Defaults()

    def __init__(self, radial: Defaults = defaults.radial,
                 shape: Defaults = defaults.shape,
                 images: Defaults = defaults.images_path,
                 metadata: Defaults = defaults.metadata_path,
                 logfiles: Defaults = defaults.log_files_path,
                 kmlfiles: Defaults = defaults.kml_files_path,
                 shapefiles: Defaults = defaults.shape_files_path,
                 geojson: Defaults = defaults.geojson_path,
                 vrt: Defaults = defaults.vrt_files_path,
                 csv: Defaults = defaults.csv_files_path,
                 spatialite: Defaults = defaults.spatialite_path,
                 sql: Defaults = defaults.sql_files_path,
                 slash: Defaults = defaults.slash,
                 ogr2ogr_com: Defaults = defaults.ogr2ogr,
                 spatialite_com: Defaults = defaults.spatialite,
                 extn: Defaults = defaults.extn):
        #posixvars = OSVars.posix()
        #ntvars = OSVars.nt()
        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.radial = radial
        self.shape = shape
        self.charset = 'CP1252'

        self.spatialite_path = spatialite
        self.sql_path = sql
        self.images_path = images
        self.metadata_path = metadata
        self.shape_files_path = shapefiles
        self.geojson_path = geojson
        self.kml_files_path = kmlfiles
        self.vrt_path = vrt
        self.csv_files_path = csv
        self.spatialite_files_path = spatialite
        self.sql_files_path = sql
        self.filename = self.f_name()
        self.ogr2ogr = ogr2ogr_com
        self.slash = slash
        self.extn = extn
        self.spatialite = spatialite_com

    def f_name(self):
        """
        Construct filename string
        """

        print(self.shape + '_' + str(self.radial) + 'km')
        return self.shape + '_' + str(self.radial) + 'km'

    def file_deploy(self, resource_data):
        """
        Deploy downloaded files

        Prerequisites:
        ref_files

        Input variables:
        """

        if not os.path.isfile(resource_data.file_path.format(slash=self.slash)):
            print('Downloading {descr} file in {fmt} file format'\
                  .format(fmt=resource_data.format, \
                          descr=resource_data.description))

            urllib.request.urlretrieve(resource_data.down_url,
                                       resource_data.zip_path.\
                                       format(slash=self.slash))
            if resource_data.zip_path.endswith('zip') is True:
                print('Unzipping {descr} file in {fmt} file format'\
                    .format(descr=resource_data.description, \
                            fmt=resource_data.format))
                print('extracting files')
                Archive(\
                        resource_data.zip_path.format(\
                                             slash=\
                                             self.slash)).\
                        extractall(resource_data.zip_dir\
                                             .format(slash=self.slash))
        else:
            print('{descr} file in {fmt} file format exists'\
                  .format(descr=resource_data.description, \
                          fmt=resource_data.format))


    def ref_files_polygons(self):
        """
        Get reference files
        Prerequisites:

        Input variables:
        """
        ref_data = DataSets.Australia.ShapeFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.AGILDataset.CSVFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.MBSP.CSVFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.NASAActiveFireData.ModisC61km.CSVFormat()
        self.file_deploy(ref_data)

    def ref_files_poly_wt(self):
        """
        Get reference files
        Prerequisites:

        Input variables:
        """
        ref_data = DataSets.Australia.ShapeFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.StatisticalAreasLevel12011.ShapeFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.StatisticalAreasLevel12016.ShapeFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.AGILDataset.CSVFormat()
        self.file_deploy(ref_data)

        ref_data = DataSets.OpenStreetMaps.ShapeFormat()
        self.file_deploy(ref_data)

    def coords_from_csv_latin1(self, file_name, lon_c, lat_c):
        """
        Reads files with illegal characters causing errors
        """

        csv.register_dialect(
            'mydialect',
            delimiter=',',
            quotechar='\'',
            doublequote=True,
            skipinitialspace=True,
            lineterminator='\r\n',
            quoting=csv.QUOTE_MINIMAL)

        with open('{csvpath}{slash}{fname}'.format(csvpath=self.csv_files_path, \
                  fname=file_name, slash=self.slash), encoding='latin1') as csvfile:
            data = list(csv.reader(csvfile, dialect='mydialect'))

        longs = []
        lats = []

        for i in range(1, len(data)-1):
            #print('')
            try:
                longs.append(float(data[i][lon_c]))
                lats.append(float(data[i][lat_c]))
            except:
                pass

        coords = [(x, y) for x, y in zip(longs, lats)]
        return coords

    def coords_from_csv(self, file_name, lon_c, lat_c):
        """
        Reads standard csv files
        """

        #csv.Sniffer
        csv.register_dialect(
            'mydialect',
            delimiter=',',
            quotechar='\'',
            doublequote=True,
            skipinitialspace=True,
            lineterminator='\r\n',
            quoting=csv.QUOTE_MINIMAL)


        with open('{csvpath}{slash}{fname}'.\
                  format(csvpath=self.csv_files_path, fname=file_name, \
                         slash=self.slash), newline='', encoding='utf-8') \
                  as csvfile:
            data = list(csv.reader(csvfile, dialect='mydialect'))

        longs = [float(item[lon_c]) for item in data[1:]]
        lats = [float(item[lat_c]) for item in data[1:]]
        coords = [(x, y) for x, y in zip(longs, lats)]
        return coords


    def points_in_polygon(self, g_array, lat_longs, g_label):
        """
        Counts for lat_longs generated
        """

        num_poly = len(g_array)
        lat_longs_df = pd.DataFrame(lat_longs)
        lat_longs_df.columns = ['longitude', 'latitude']
        for poly in range(0, num_poly):
            #poly_id=g_array[poly]['properties']['p']
            p_count = 0
            bound_points_df = lat_longs_df[(lat_longs_df['latitude'] >=\
                                            g_array[poly]['properties']['S']) & \
                                           (lat_longs_df['latitude'] <=\
                                            g_array[poly]['properties']['N']) & \
                                           (lat_longs_df['longitude'] <=\
                                            g_array[poly]['properties']['E']) & \
                                           (lat_longs_df['longitude'] >=\
                                            g_array[poly]['properties']['W'])]
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
                    if path.contains_point([row['longitude'], row['latitude']]) is True:
                        p_count += 1

            g_array[poly]['properties'][g_label] = float(p_count)

        return g_array

    def from_geojson_file(self, file_name):
        """
        Read GeoJSON from file

        Prerequisites:

        Input variables:
        """

        msg = 'reading geojson formatted dataset from file:' + file_name +'.json'
        print(msg.format(shape=self.shape, fname=self.filename))
        full_file_templ = '{geojson}{slash}' + file_name + '.json'
        my_file = open(full_file_templ.format(fname=file_name, \
                                             slash=self.slash,\
                                             geojson=self.geojson_path), 'r')
        #open file for reading geojson layer in geojson format
        gj_data = my_file.read()  # read geojson layer to open file
        gj_dict = json.loads(gj_data)
        g_array = []
        for i in range(len(gj_dict['features'])):
            g_array.append(gj_dict['features'][i])
        my_file.close()  # close file
        return g_array

    def to_geojson_file(self, g_array, file_name):
        """
        Write string to file

        Prerequisites:
        to_geojson, hex_array or box_array, horizontal, vertical, Tiles

        Input variables:
        """
        content = FeatureCollection(g_array)
        msg = 'writing geojson formatted {shape} dataset to file:' +\
               file_name +'.json'
        print(msg.format(shape=self.shape, fname=self.filename))
        file_path_templ = '{geojson}{slash}'+file_name+'.json'
        my_file = open(file_path_templ.format(fname=self.filename, \
                                              slash=self.slash, \
                                              geojson=self.geojson_path), 'w')
        #open file for writing geojson layer in geojson format
        my_file.write(str(content))  # write geojson layer to open file
        my_file.close()  # close file

    def from_shp_file(self, shape_file_name, shape_file_path):
        """
        Reads shapefile Polgon or Multipolygon into a Polygon based Geojson arry

        """

        #fName,fPath
        #tabular_list = []

        shape_file_full_path = '{fPath}{slash}{fName}'.\
                                format(slash=self.slash, \
                                       fPath=shape_file_path, \
                                       fName=shape_file_name)
        #prjPath = fPath + '.prj'
        shape_file = shapefile.Reader(shape_file_full_path) # , shapeType=3)
        shapes = shape_file.shapes()
        #how many empty and real polgons and subpolygons
        shapes_list = []
        [shapes_list.append([len(x.points), len(x.parts)]) for x in shapes]

        # add a row_id reference
        shapes_list_with_row_id = []
        [shapes_list_with_row_id.\
         append([x, shapes_list[x][0], \
                 shapes_list[x][1]]) \
                 for x in range(len(shapes_list))]

        # drop all array rows ith 0 parts
        shapes_list_no_null = [a for a in shapes_list_with_row_id if a[2] not in [0]]

        #get the field names
        fields = shape_file.fields
        column_list = []
        [column_list.append(x[0]) for x in fields[1:]]

        # data values with null geography
        tab_data = shape_file.records()

        tab_data_val = []
        row_ref = []
        i = 0
        for tab_row in range(len(shapes_list_no_null)): # all rows
            #for column_name in column_list:
            row_data = [] #shapes_list_no_null[tab_row][0]]

            for tab_val in tab_data[shapes_list_no_null[tab_row][0]]: # each row of tab data (y)
                row_ref.append(i)
                row_data.append(tab_val) #,len(shapes[tab_row].points)])
                #column_dict[column_name] = str(tab_col)
            i += 1
            tab_data_val.append(row_data) # column_dict)

        geojson_properties_list = []
        for tab_row in tab_data_val:
            dataset_dict_row = {}
            for i in range(0, len(column_list)):
                #print(i)
                dataset_dict_row[column_list[i]] = tab_row[i]
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
        for i in range(len(geojson_properties_list)):
            parts_list[i].append(points_len[i])
            shapes_ref = row_ref[i]
            #thing.append([geojson_properties_list[i],parts_count[i],parts_list[i]])

            for j in range(0, parts_count[i]):
                #geojson_polygon = {}

                geopoly = Polygon([shapes[shapes_ref].\
                                   points[parts_list[i][j]:parts_list[i][j+1]]])
                geopoly = Feature(geometry=geopoly, \
                                  properties=geojson_properties_list[i])

                g_array.append(geopoly)
        return g_array


    def to_shp_file(self, g_array, file_name):
        """
        Write geojson Polygon array to shapefile
        """

        #tabular_list = []
        file_path_templ = '{shapefiles}{slash}'+file_name
        full_file_path = file_path_templ.format(shape=self.shape,
                                                size=self.radial,
                                                slash=self.slash,
                                                shapefiles=self.shape_files_path,
                                                fname=self.filename)
        prj_path = full_file_path + '.prj'
        w_file = shapefile.Writer(full_file_path) # , shapeType=3)
        #setup columns
        props_dict = g_array[0]['properties']
        i = 0
        for key in props_dict:
            if i < 2 or i > 8:
                w_file.field(key, 'N')
            else:
                w_file.field(key, 'N', decimal=10)
            i = i + 1

        num_poly = len(g_array)
        for n_val in range(0, num_poly):
            props_dict_rec = g_array[n_val]['properties']
            rec_str = "w_file.record("
            i = 0
            #print('props_list',len(props_dict))
            for key in props_dict_rec:

                rec_str = rec_str + key + ' = ' + str(props_dict_rec[key])

                if i is not len(props_dict)-1:
                    rec_str = rec_str + ','
                i = i + 1

            rec_str = rec_str + ' )'
            eval(rec_str)

            w_file.poly([g_array[n_val]['geometry']['coordinates'][0]])
            #w.record(n)
        w_file.close()
        # create the PRJ file
        msg = 'writing shapefile formatted {shape} dataset to file:' + full_file_path +'.shp'
        print(msg.format(shape=self.shape, fname=self.filename))
        prj = open(prj_path, "w")
        epsg = 'GEOGCS["WGS 84",'
        epsg += 'DATUM["WGS_1984",'
        epsg += 'SPHEROID["WGS 84",6378137,298.257223563]]'
        epsg += ',PRIMEM["Greenwich",0],'
        epsg += 'UNIT["degree",0.0174532925199433]]'
        prj.write(epsg)
        prj.close()

    def to_kml_file(self, g_array, file_name):
        """
        Writes geojson Polygon array to kml file
        """

        file_name_templ = '{kPath}{slash}'+file_name+'.kml'
        full_file_path = file_name_templ.format(kPath=self.kml_files_path,
                                                shape=self.shape,
                                                size=self.radial,
                                                slash=self.slash,
                                                fname=self.filename)
        kml = simplekml.Kml()
        #setup columns
        props_dict = g_array[0]['properties']

        key_names_array = []
        for key in props_dict:
            key_names_array.append(key)

        for poly in range(0, len(g_array)):
            props_dict_rec = g_array[poly]['properties']
            (i, key_values_array) = (0, [])
            rec_descr = ""
            for key in props_dict:
                key_values_array.append(props_dict_rec[key])

                if i is not len(props_dict)-1:
                    rec_descr = rec_descr + key + ' = ' \
                    + str(props_dict_rec[key]) + '\n'
                else:
                    rec_descr = rec_descr + key + ' = ' \
                    + str(props_dict_rec[key]) + '\n'
                i += 1
            #ev_str = 'pol = kml.newpolygon(name ="'
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
            pol.style.polystyle.fill = 0

        msg = 'writing kml formatted {shape} dataset to file:' + file_name +'.kml'
        print(msg.format(shape=self.shape, fname=self.filename))
        kml.save(full_file_path)


    def points_and_polygons(self, g_array):
        """
        Neighbouring Polygons derivation

        Prerequisites:
        hex_array or box_array, horizontal, vertical ,Tiles

        Input variables:
        g_array
        """

        (point_list, num_poly) = ([], len(g_array))

        for poly in range(0, num_poly):
            num_coords = len(g_array[poly]['geometry']['coordinates'][0])-2
            poly_id = g_array[poly]['properties']['p']
            for i in range(0, num_coords):
                point_list.append( \
                    [poly_id, str(g_array[poly]['geometry']['coordinates'][0][i][0]) + \
                     str(g_array[poly]['geometry']['coordinates'][0][i][1])])
        return point_list


    def neighbours(self, points_list):
        """
        Intersecting polygons list

        Prerequisites:
        hex_array or box_array, horizontal, vertical, Tiles

        Input variables:
        pointslist: array of points and metadata defining polygon shapes
        """

        point_df = pd.DataFrame(points_list)
        point_df.columns = ['poly', 'latlong']
        point_df.to_csv('{csv}{slash}{outfile}_points.csv' \
                        .format(outfile=self.filename, \
                                slash=self.slash,
                                csv=self.csv_files_path), sep=',')
        point_df_a = point_df  # make copy of dataframe
        process_point_df = pd.merge(point_df, point_df_a, on='latlong')
        # merge columns of same dataframe on concatenated latlong
        process_point_df = process_point_df[(process_point_df['poly_x']
                                             != process_point_df['poly_y'])]
        # remove self references
        output_point_df = process_point_df[['poly_x', 'poly_y']].\
                          copy().sort_values(by=['poly_x']).drop_duplicates()
        #just leave polygon greferences and filter output

        output_point_df.to_csv('{csv}{slash}{outfile}_neighbours.csv' \
                               .format(outfile=self.filename, \
                                slash=self.slash,
                                       csv=self.csv_files_path), \
                               sep=',', index=False)


def random_points_in_polygon(self, poly):
    """
    Creates random points as defined by a polygon
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

def tabular_dataframe(g_array):
    """
    Not Implemented to date

    """

#    tabular_list = []
#    #num_coords = len(g_array[n]['geometry']['coordinates'][0])-2
#    for i in range(0, num_coords):
#        poly = g_array[n]['properties']['p']
#        centre_lat = g_array[n]['properties']['lat']
#        centre_lon = g_array[n]['properties']['long']
#        bounds_n = g_array[n]['properties']['N']
#        bounds_s = g_array[n]['properties']['S']
#        bounds_e = g_array[n]['properties']['E']
#        bounds_w = g_array[n]['properties']['W']
#        tabular_line =[poly, centre_lat, centre_lon, \
#                       bounds_n, bounds_s, bounds_e, bounds_w]
#        tabular_list.append(tabular_line)
#
#    tabular_df = pd.DataFrame(tabular_list)
#    #convert tabular array to tabular data frame
#    tabular_df.columns = ['poly', 'lat', 'long', 'N', 'S', 'E', 'W']
#    tabular_df.to_csv('csv{slash}{outfile}_dataset.csv' \
#                      .format(outfile = outfile, slash = slash), \
#                      sep = ',')
#    return tabular_df
    return g_array



def to_geojson_fmt(g_array):
    """
    converts geojson Polygon data in array to FeatureCollection
    """

    return FeatureCollection(g_array)
