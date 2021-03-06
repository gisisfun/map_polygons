"""
Map_polygons tiles module
"""
import os
import sys
from math import sqrt
import pandas as pd
import numpy as np
import matplotlib.path as mpltPath
import shapefile #to be moved to util from add_poly_poi

from isotiles.__init__ import Defaults
from utils import points_in_polygon, coords_from_csv, \
coords_from_csv_latin1, point_radial_distance, poly_drop, \
path_slash
#all

from geojson import Polygon, Feature #,FeatureCollection


sys.path.append('..')

def column_counts(g_array):
    """
    column counts for neighbour update
    :param g_array: geojson Polygon data in array
        
    :Retuen (odd_columns, even_columns):
    """
    ref_table = []
    for g_rec in iter(g_array):
        ref_table.append(g_rec['properties']['row'])

        ref_table_df = pd.DataFrame(ref_table)
        ref_table_df.columns = ['row']
        #print(len(ref_table_df))

    odd_columns = ref_table.count(1)
    even_columns = ref_table.count(2)
    #print(int(odd_columns), int(even_columns))
    return odd_columns, even_columns


class Tiles():
    """
    Modules for map_polygons
    """

    defaults = Defaults()

    def __init__(self, north: Defaults = defaults.north,
                 south: Defaults = defaults.south,
                 east: Defaults = defaults.east,
                 west: Defaults = defaults.west,
                 radial: Defaults = defaults.radial,
                 shape: Defaults = defaults.shape,
                 shapefiles: Defaults = defaults.shape_files_path):
        """
        supply variables for map_polygons
        """
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.radial = radial
        self.shape = shape
        #self.shape_files_path = shapefiles


    @property
    def inc_adj(self):
        """
        Increment offset for next hexagon
        increment values fot cxceptions of unused count of latitudes values
        """
        return  [False, True, True, True, False, True, True, True]

    @property
    def inc_by_rem(self):
        """
        Increment offset for next hexagon
        increment values fot cxceptions of unused count of latitudes values
        """
        return [0, 0, -4, 0, 0, -4, -4, -4]

    @property
    def short(self):
        """
        Short interval to next reference point
        """
        return .7071

    @property
    def long(self):
        """
        Long interval to next reference point
        """

        return 1

    @property
    def slash(self):
        """
        OS dependant path slash character.
        """
        my_os = str(os.name)
        os_dict = {"posix":{"slash": "/"}, "nt":{"slash": '\\'}}
        return os_dict[my_os]['slash'] # '/'

    @property
    def shape_files_path(self):
        """
        Shape filespath
        """
        return "files/shapefiles"

    @property
    def kml_files_path(self):
        """
        Shape filespath
        """
        return "files/kmlfiles"

    @property
    def csv_files_path(self):
        """
        Shape filespath
        """
        return "files/csv"

    @property
    def json_files_path(self):
        """
        Shape filespath
        """
        return "files/jsonfiles"

    @property
    def geojson_files_path(self):
        """
        Shape filespath
        """
        return "files/geojson"

    @property
    def hor_seq(self):
        """
        Long interval to next reference point
        """
        if self.shape == 'hex':
            hor_seq = [self.short, self.short,
                       self.short, self.short]
        else:
            hor_seq = [self.long, self.long,
                       self.long, self.long]
        return hor_seq

    @property
    def vert_seq(self):
        """
        Long interval to next reference point
        """
        if self.shape == 'hex':
            vert_seq = [self.short, self.long,
                        self.short, self.long]
        else:
            vert_seq = [self.long, self.long,
                        self.long, self.long]
        return vert_seq
    
    @property
    def filename(self):
        """
        Construct filename string
        """
        return '{}_{}km'.format(self.shape, self.radial)

    def params(self):
        """
        Construct feedback of user variables for user
        """
        msg = """Making {0} shapes starting from {1},{2} to {3},{4} with
 a radial length of {5} km.""" # Odd rows: {6} polygons, Even number rows: {7}
# polygons, remainder points: {8)"""
        return  msg.format(self.shape, self.north, self.west, self.south,
                           self.east, self.radial) #, self.odd, self.even,
#                           self.rem_lat)


    def metadata(self):
        """
        Not Implemented to date
#        """
        layer_dict = {'Bounds': {'Australia': {'North': self.north,
                                               'South': self.south,
                                               'West': self.west,
                                               'East': self.east}}}
        layer_dict['Param'] = {}
        layer_dict['Param']['side_km'] = self.radial
        layer_dict['Param']['epsg'] = 4326
        return layer_dict


    def hor(self):
        """
        Horizontal Reference Points
        """
        #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
        (angle, new_north, i, longitudes) = (180, self.north, 0, [])
        #print(east,new_north,south,'\n')
        longitudes.append(self.north)

        while new_north >= self.south:
            if i > 3:
                i = 0

            latlong = [new_north, self.east]
            p_val = point_radial_distance(latlong, angle, self.radial *\
                                           self.hor_seq[i])
            new_north = p_val[0]
            longitudes.append(p_val[0])
            i += 1
        return longitudes


    def vert(self):
        """
        derivation of horizontal list of reference points 
        from east to west for latitudes or y axis
        """
        print('east {0} west {1}'.format(self.east, self.west))

        (angle, new_west, i, latitudes) = (90, self.west, 0, [])

        latitudes.append(self.west)
        while new_west <= self.east:
            if i > 3:
                i = 0

            latlong = [self.north, new_west]
            p_val = point_radial_distance(latlong, angle, \
                                               self.radial*self.vert_seq[i])
            new_west = p_val[1]
            latitudes.append(p_val[1])
            i += 1

        return latitudes

    def hor_vert(self, hor, vert):
        """
        horizontal and vertical 1D array

        :param hor: horizontal (columns, longitudes)
        :param vert: vertical (rows, latitudes)
        
        :return coords:
        """
        coords = []
        for y_coord in iter(hor):
            for  x_coord in iter(vert):
                coords.append([x_coord, y_coord])
        return coords

    def hor_vert_matrix(self, hor, vert):
        """
        horizontal and vertical  matrix array

        :param hor: horizontal (columns, longitudes)
        :param vert: vertical (rows, latitudes)
        
        :return rows_and_columns:
        """
        rows_and_columns = []
        for y_coord in iter(hor):
            columns = []
            for x_coord in iter(vert):
                columns.append([x_coord, y_coord])
            rows_and_columns.append(columns)
        return rows_and_columns

    def hex_array(self, intersect_list, max_h, max_v):
        """
        Put it all together - deriving hexagon polygons from intersection data


        :param intersect_list:
        :param max_h: 
        :param max_v:
            
        :return g_array: geojson Polygon data in array
        """

        (g_array, tabular_list) = ([], [])
        (lat_offset, top_left, poly_row_count) = \
        (4, 0, int(max_v / len(self.hor_seq)))
        rem_lat = max_v % (lat_offset + len(self.hor_seq))
#        self.rem_lat = rem_lat
        p_tuple = ((False, True, True, True, False, True, True, True), \
                   (0, 0, -4, 0, 0, -4, -4, -4))

        (inc_by_rem, inc_adj) = (p_tuple[0][rem_lat], p_tuple[1][rem_lat])

        print('\n4/7 deriving hexagon polygons from intersection data')
        (row, col, last_lat_row, poly_id) = (1, 1, 0, 0)

        while top_left < max_h * max_v:
            vertex = [1 + top_left, 2 + top_left, max_v + 3 + top_left, \
                      (max_v * 2) + 2 + top_left, (max_v * 2) + \
                      1 + top_left, max_v + top_left]
            try:
                poly_coords = [intersect_list[vertex[0]], \
                               intersect_list[vertex[1]], \
                               intersect_list[vertex[2]], \
                               intersect_list[vertex[3]], \
                               intersect_list[vertex[4]], \
                               intersect_list[vertex[5]], \
                               intersect_list[vertex[0]]]
                (vertex00, vertex01, vertex20, vertex31, vertex50, vertex51) = \
                           (intersect_list[vertex[0]][0], \
                            intersect_list[vertex[0]][1], \
                            intersect_list[vertex[2]][0], \
                            intersect_list[vertex[3]][1], \
                            intersect_list[vertex[5]][0], \
                            intersect_list[vertex[5]][1])
                centre_lat = vertex01 + (vertex51 - vertex01) / 2
                centre_lon = vertex00 + (vertex50 - vertex00) / 2

                if (centre_lat is not last_lat_row) or last_lat_row is 0:
                    (bounds_n, bounds_s, bounds_e, bounds_w) = \
                                        (vertex01, vertex31, vertex20, vertex50)
                    last_lat_row = centre_lat
                    geopoly = Polygon([poly_coords])
                    poly_id += 1
                    est_area = (((3 * sqrt(3)) / 2) * pow(self.radial, 2)) * \
                    0.945
                    #estimate polygon area
                    geopoly = Feature(geometry=geopoly, properties= \
                                      {"p": poly_id, "row": row, \
                                       "col": col, "lat": centre_lat, \
                                       "lon": centre_lon, "N": bounds_n, \
                                       "S": bounds_s, "E": bounds_e, \
                                       "W": bounds_w, "est_area": est_area, \
                                       "Aust": 0})
                    if  bounds_e > bounds_w:
                        g_array.append(geopoly)
                        #append geojson geometry definition attributes to list
                        #tabular dataset
                        tabular_line = [top_left, row, centre_lat, centre_lon, \
                                        bounds_n, bounds_s, bounds_e, bounds_w, \
                                        est_area]
                        tabular_list.append(tabular_line)
                        #array of polygon and tabular columns
                else:
                    pass

            except IndexError:
                pass

            (last_row, last_lat_row) = (row, centre_lat)
            row = int(1 + int(poly_id / poly_row_count))
            top_left += lat_offset
            if row is not last_row:
                col = 1
                top_left += inc_adj
                if inc_by_rem:
                    top_left += rem_lat
                if row % 2 == 0:
                    top_left += 2
                if row & 1:
                    top_left += -2
            else:
                col += 1
        print('created dataset of {0} derived hexagon polygons'.\
              format(len(g_array)))
        return g_array


    def box_array(self, intersect_list, max_h, max_v):
        """
        Create array of box shaped polygons

        Prerequisites:
        horizontal, vertical, Tiles

        :param intersect_list: 
        :param max_h:
        :param max_v:
            
        :return g_array: geojson Polygon data in array
            
        >>> box_array(intersect_list, max_h, max_v)
        
        """
        self.shape = 'box'
        poly_id = 0
        (top_left, g_array, col, row) = (0, [], 1, 1)
        # g_array - array of geojson formatted geometry element
        print('\n4/7 deriving boxes polygons from intersection data')
        vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left + max_v]

        while vertex[2] < max_h * max_v:
            poly_coords = [intersect_list[vertex[0]], \
                           intersect_list[vertex[1]], \
                           intersect_list[vertex[2]], \
                           intersect_list[vertex[3]], \
                           intersect_list[vertex[0]]]
            (vertex00, vertex01, vertex10, vertex20, vertex21, vertex31) = \
                       (intersect_list[vertex[0]][0], \
                        intersect_list[vertex[0]][1], \
                        intersect_list[vertex[1]][0], \
                        intersect_list[vertex[2]][0], \
                        intersect_list[vertex[2]][1], \
                        intersect_list[vertex[3]][1])
            centre_lat = vertex01 + (vertex21 - vertex01) / 2
            centre_lon = vertex00 + (vertex20 - vertex00) / 2
            bounds_n = vertex01
            bounds_s = vertex31
            bounds_e = vertex10
            bounds_w = vertex00
            if bounds_e > bounds_w:
                geopoly = Polygon([poly_coords])
                poly_id += 1
                geopoly = Feature(geometry=geopoly, \
                properties={"p": top_left, "a": poly_id-1, \
                              "lat": centre_lat, "lon": centre_lon, \
                              "N": bounds_n, "S": bounds_s, \
                              "E": bounds_e, "W": bounds_w, \
                              "row": row, "col": col, \
                              "Aust": 0, "est_area": self.radial ** 2, })
                g_array.append(geopoly)
                #append geojson geometry definition attributes to list
            else:
                row += 1
                col = 0

            #increment values
            top_left += 1
            col += 1
            vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left + max_v]

        print('\n5/7 boxes geojson dataset of {0} derived polygons'.format(len(g_array)))
        return g_array

    def add_poly_poi(self, g_array):
        """
        Polulates polygons with poi to identifiy contental features without gdal
        :param g_array: geojson Polygon data in array
            
        :return g_array: geojson Polygon data in array
        >>> add_poly_poi(g_array)
        """
        #u_mod = Util()
        # load the shapefile
        shape_file = shapefile.Reader("files/shapefiles/AUS_2016_AUST")

        # shapefile contains multipolygons
        shapes = shape_file.shapes()
        #print(len(shapes))
        big_coords = shapes[0].points
        # get the query polygons

        print('Adding the Boundary/Coast Line points')
        longs = [float(item[0]) for item in big_coords]
        lats = [float(item[1]) for item in big_coords]
        coords = [(x, y) for x, y in zip(longs, lats)]

        poly_array = points_in_polygon(g_array, coords, 'Boundary')

        print('Adding Island points')
        coords = coords_from_csv('islands.csv', 1, 2,self.csv_files_path)
        next_poly_array = points_in_polygon(poly_array, coords, 'Island')

        print('Adding GNAF Locality points')
        coords = coords_from_csv('aug_gnaf_2019_locality.csv', 4, 3, \
                                 self.csv_files_path)
        poly_array = points_in_polygon(next_poly_array, coords, 'Locality')

        print('NASA Active fire Data MODIS C6 Australia and New Zealand 24h')
        coords = coords_from_csv('MODIS_C6_Australia_and_New_Zealand_24h.csv',\
                                 1, 0, self.csv_files_path)
        next_poly_array = points_in_polygon(poly_array, coords, \
                                                  'Active_Fires')

        print('National Mobile Blackspot program')
        coords = coords_from_csv_latin1('mbsp_database.csv', 6, 5, \
                                        self.csv_files_path)
        poly_array = points_in_polygon(next_poly_array, coords, 'MBSP')

        print('AGIL Locations')
        coords = coords_from_csv('agil_locations20190208.csv', 3, 2, \
                                 self.csv_files_path)
        next_poly_array = points_in_polygon(poly_array, coords, 'AGIL')

        print('Polygons Centroids and Offset Vertices')
        coords = self.aus_poly_coords(next_poly_array)
        #print(len(coords))
        poly_array = points_in_polygon(next_poly_array, coords, 'P_POI')
        for poly_data in iter(poly_array):
            poly_data['properties']['Aust'] = 0
            if poly_data['properties']['P_POI'] > 0 \
               or poly_data['properties']['Island'] > 0 or \
               poly_data['properties']['Locality'] > 0 or \
               poly_data['properties']['Boundary'] > 0:
                poly_data['properties']['Aust'] = 1
                #out_array.append(poly_array[poly])

        return poly_array


    def aus_poly_coords(self, g_array):
        """
        generate coords inside map layer polygons to fill continent
        :param g_array: geojson Polygon data in array
            
        :return g_array: geojson Polygon data in array
        """
        # load the shapefile
        shape_file = shapefile.Reader(\
                                      path_slash(self.shape_files_path,\
                                                 '/',self.slash) + \
                                                 self.slash +\
                                                 "AUS_2016_AUST")
        # shapefile contains multipolygons
        shapes = shape_file.shapes()
        big_coords = shapes[0].points
        loc_poly_array = g_array
        coords = []
        for poly, poly_val in enumerate(loc_poly_array):
            c_lon = poly_val['properties']['lon']
            c_lat = poly_val['properties']['lat']
            coords.append((c_lon, c_lat))
            for point in loc_poly_array[poly]['geometry']['coordinates'][0]:
                coords.append((point[0], point[1]))
            unique_coords = np.unique(coords, axis=0) # remove duplicate coordinates
        in_coords = []
        len_parts = len(shapes[0].parts[:-1])
        #print(len_parts)
        for subpoly in range(len_parts):
            sub_coords = big_coords[shapes[0].parts[subpoly]:shapes[0].parts[subpoly+1]]
            path = mpltPath.Path(sub_coords)
            np_arr = np.array(sub_coords)
            (arr_min, arr_max) = (np.min(np_arr, axis=0), np.max(np_arr, \
                                 axis=0))
            (bounds_n, bounds_s, bounds_e, bounds_w) = (arr_max[1], \
            arr_min[1], arr_max[0], arr_min[0])
            in_bbox = False
            for point in unique_coords:
                if point[1] < bounds_n and point[1] > bounds_s and \
                   point[0] < bounds_e and point[0] > bounds_w:
                    in_bbox = True
                if in_bbox is True:
                    if path.contains_point([point[0], point[1]-0.0001]) is True:
                        in_coords.append((point[0], point[1]-0.0001))
        return in_coords

    def hexagons(self):
        """
        Process geojson Polygon array
        """
        print(self.params())
        hors = self.hor()
        verts = self.vert()
        the_coords = self.hor_vert(hors, verts)
        hex_array = self.hex_array(the_coords, len(hors), len(verts))

        odd = len(verts)//4
        even = (len(verts)-3)//4

        print("across (odd rows)", odd, "across (even rows)", even)
        
        poi_hex_array = self.add_poly_poi(hex_array)
        (odd, even) = column_counts(poi_hex_array)
        
        print('odd', odd, 'even', even)

        aus_hex_array = poly_drop(poi_hex_array,'Aust')

        return aus_hex_array


    def boxes(self):
        """
        Process geojson Polygon array
        """
        print(self.params())
        hors = self.hor()
        verts = self.vert()
        the_coords = self.hor_vert(hors, verts)
        box_array = self.box_array(the_coords, len(hors), len(verts))
        poi_box_array = self.add_poly_poi(box_array)
        (odd, even) = column_counts(poi_box_array)

        aus_box_array = poly_drop(poi_box_array)
        # add neighbouur reference data
        nb_aus_box_array = self.update_neighbours(aus_box_array, odd, even)
        #print("100% progress: It's not over til it's over")
        return nb_aus_box_array
