"""
Map_polygons tiles module
"""

#all
from math import pow, sqrt
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.path as mpltPath
import shapefile #to be moved to util from add_poly_poi
from geojson import Polygon, Feature #,FeatureCollection



from isotiles.parameters import BoundingBox, Offsets, Defaults
#from isotiles.poi import POI
from isotiles.util import Util

def neighbour_calc(poly, column_count):
    """
    Neighbour cell calculations
    """
    neighbour_list = {"box": {\
                              "north": (poly - (column_count*1-\
                                                (poly % column_count))-\
                                        (poly % column_count))-1, \
                              "north_east": (poly - (column_count*1-\
                                                      (poly % column_count))-\
                                              (poly % column_count)),\
                              "east": poly + 1,\
                              "south_east": (poly + (column_count*1-\
                                              (poly % column_count))+\
                                              (poly % column_count))+2,\
                              "south": (poly + (column_count*1-\
                                              (poly % column_count))+\
                                              (poly % column_count))+1,\
                              "south_west": (poly + (column_count*1-\
                                                   (poly % column_count))+\
                                                   (poly % column_count)),
                              "west": poly - 1,\
                               "north_west": (poly - (column_count*1-\
                                                   (poly % column_count))-\
                                                   (poly % column_count))-2},\
                       "hex":{\
                              "north": (poly - (column_count*2-\
                                                (poly % column_count))-\
                                                (poly % column_count)),\
                              "north_east": (poly - (column_count*1-(poly % \
                                                  column_count))-\
                                                  (poly % column_count)),\
                              "east": poly + 1,\
                              "south_east": (poly+(column_count*1-\
                                                        (poly % \
                                                         column_count))+\
                                                        (poly % column_count)),\
                              "south": (poly + (column_count*2-\
                                                (poly % column_count))+\
                                                (poly % column_count)),\
                              "south_west": (poly + (column_count*1-\
                                                          (poly % \
                                                           column_count))+\
                                                           (poly % column_count\
                                                            ))-1,\
                              "west": poly - 1,\
                              "north_west": (poly - (column_count*1-\
                                                     (poly % column_count))-\
                                                     (poly % column_count))-1\
    }}

    return neighbour_list

class Tiles():
    """
    Modules for map_polygons
    """

    value = BoundingBox.Australia()
    defaults = Defaults()

    def __init__(self, north: BoundingBox = value.north,
                 south: BoundingBox = value.south,
                 east: BoundingBox = value.east,
                 west: BoundingBox = value.west,
                 radial: Defaults = defaults.radial,
                 shape: Defaults = defaults.shape,
                 kmlfiles: Defaults = defaults.kml_files_path,
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
        self.filename = self.f_name()
        self.shape_files_path = shapefiles
        self.kml_files_path = kmlfiles
        off_values = Offsets()



        if self.shape == 'hex':
            self.hor_seq = [off_values.short, off_values.short,
                            off_values.short, off_values.short]
            self.vert_seq = [off_values.short, off_values.long,
                             off_values.short, off_values.long]

        else:
            self.hor_seq = [off_values.long, off_values.long,
                            off_values.long, off_values.long]
            self.vert_seq = [off_values.long, off_values.long,
                             off_values.long, off_values.long]

    def params(self):
        """
        Construct feedback of user variables for user

        Dependencies:
        Tiles
        """

        part_1 = 'Making {0} shapes starting from {1},{2} to {3},{4} with'
        part_2 = 'a radial length of {5} km'
        parts = part_1 + part_2
        return  parts.format(self.shape, self.north, self.west, self.south,
                             self.east, self.radial)


    def metadata(self):
        """
        Not Implemented to date
#        """
#        layer_dict = {'Bounds': {'Australia': {'North': self.north, 'South': self.south, \
#                                           'West': self.west, 'East': self.east}}}
#        layer_dict['Param'] = {}
#        layer_dict['Param']['side_km'] = self.radial
#        layer_dict['Param']['epsg'] = 4326
#        layer_dict['Param']['shape'] = self.shape
#        layer_dict['Boxes'] = {}
#        layer_dict['Boxes']['long'] = 1
#        hor_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'], \
#                   layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
#        vert_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'], \
#                    layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
#
#        layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
#        layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
#        layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
#        layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min()
#
#        print('\n7/7 boxes json metadata to written to file: {0}_metadata.json' \
#              .format(outfile))
#        myfile = open('metadata{slash}{outfile}_metadata.json' \
#                      .format(outfile=outfile, slash=slash), 'w')
#        # open file for writing geojson layer
#        myfile.write(str(json.dumps(layer_dict)))
#        #write geojson layer to open file
#        myfile.close()  # close file

    def f_name(self):
        """
        Construct filename string

        Dependencies:
        Tiles
        """


        print(self.shape + '_' + str(self.radial) + 'km')
        return self.shape + '_' + str(self.radial) + 'km'

    def point_radial_distance(self, coords, brng, radial):
        """
        Calulate next point from coordinates and bearing

        Dependencies:
        None
        """
        return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

    def horizontal(self):
        """
        Horizontal Reference Points

        Dependencies:
        Tiles
        """
        #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
        (angle, new_north, i, longitudes) = (180, self.north, 0, [])
        #print(east,new_north,south,'\n')
        longitudes.append([[self.north, self.west], [self.north, self.east]])

        while new_north >= self.south:
            if i > 3:
                i = 0

            latlong = [new_north, self.east]
            p_val = self.point_radial_distance(latlong, angle, self.radial *\
                                           self.hor_seq[i])
            new_north = p_val[0]
            longitudes.append([[p_val[0], self.west], [p_val[0], self.east]])
            i += 1
        return longitudes


    def vertical(self):
        """
        #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis

        Prerequisites:
        Tiles

        Input variables:
        Provided
        """
        print('east {0} west {1}'.format(self.east, self.west))

        (angle, new_west, i, latitudes) = (90, self.west, 0, [])

        latitudes.append([[self.north, self.west], [self.south, self.west]])
        while new_west <= self.east:
            if i > 3:
                i = 0

            latlong = [self.north, new_west]
            p_val = self.point_radial_distance(latlong, angle, \
                                               self.radial*self.vert_seq[i])
            new_west = p_val[1]
            latitudes.append([[self.north, p_val[1]], [self.south, p_val[1]]])
            i += 1

        return latitudes


    def line_intersection(self, line1, line2):
        """
        source: https://stackoverflow.com/questions/20677795/
        how-do-i-compute-the-intersection-between-two-lines-in-python

        Dependencies:
        intersections,horizontal,vertical,Tiles
        """


        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a_val, b_val):
            return a_val[0] * b_val[1] - a_val[1] * b_val[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d_val = (det(*line1), det(*line2))
        (x_val, y_val) = (det(d_val, xdiff) / div, det(d_val, ydiff) / div)
        return x_val, y_val

    def intersections(self, hor_line_list, vert_line_list):
        """
        Intersecting Lines as points

        Dependencies:
        horizontal,vertical,Tiles

        Input variables:
        hor_line_list:
        vert_line_list:
        """


        print('\n3/7 deriving intersection point data between horizontal and vertical lines')
        (intersect_list, hor_max, vert_max) = ([], len(hor_line_list), \
         len(vert_line_list))
        for h_val in range(0, hor_max):
            for v_val in range(0, vert_max):
                intersect_point = self.line_intersection(hor_line_list[h_val],
                                                         vert_line_list[v_val])
                intersect_data = [intersect_point[1], intersect_point[0]]
                intersect_list.append(intersect_data)

        print('derived {0} points of intersection'.format(len(intersect_list)))
        return intersect_list



    def hex_array(self, intersect_list, max_h, max_v):
        """
        Put it all together - deriving hexagon polygons from intersection data

        Prerequisites:
        intersections, horizontal, vertical, Tiles

        Input variables:
        intersect_list:
        max_h:
        max_v:
        """


        (g_array, tabular_list) = ([], [])
        (lat_offset, top_left, poly_row_count) = \
        (4, 0, int(max_v / len(self.hor_seq)))
        rem_lat = max_v % (lat_offset + len(self.hor_seq))
        p_tuple = ((False, True, True, True, False, True, True, True), \
                   (0, 0, -4, 0, 0, -4, -4, -4))

        (inc_by_rem, inc_adj) = (p_tuple[0][rem_lat], p_tuple[1][rem_lat])

        print('\n4/7 deriving hexagon polygons from intersection data')
        (row, col, last_lat_row, poly_id) = (1, 1, 0, 0)

        while (top_left < (max_h) * (max_v)):
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
                                       "Aust": 0, "a": poly_id-1,\
                                       "p_N":-9, "p_NE":-9, \
                                       "p_E":-9, "p_SE":-9, \
                                       "p_S":-9, "p_SW":-9, \
                                       "p_W":-9, "p_NW":-9})
                    if  (bounds_e > bounds_w):
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

        Input variables:
        Provided
        """

        self.shape = 'box'
        self.filename = self.f_name()
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
                              "Aust": 0, "p_N":-9, \
                              "p_NE":-9, "p_E":-9, \
                              "p_SE":-9, "p_S":-9, \
                              "p_SW":-9, "p_W":-9, \
                              "est_area": self.radial ** 2})
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
        """
        u_mod = Util()
        # load the shapefile
        shape_file = shapefile.Reader("shapefiles/AUS_2016_AUST")

        # shapefile contains multipolygons
        shapes = shape_file.shapes()
        big_coords = shapes[0].points
        # get the query polygons

        print('Adding the Boundary/Coast Line points')
        longs = [float(item[0]) for item in big_coords]
        lats = [float(item[1]) for item in big_coords]
        coords = [(x, y) for x, y in zip(longs, lats)]

        poly_array = u_mod.points_in_polygon(g_array, coords, 'Boundary')

        print('Adding Island points')
        coords = u_mod.coords_from_csv('islands.csv', 1, 2)
        next_poly_array = u_mod.points_in_polygon(poly_array, coords, 'Island')

        print('Adding GNAF Locality points')
        coords = u_mod.coords_from_csv('aug_gnaf_2019_locality.csv', 4, 3)
        poly_array = u_mod.points_in_polygon(next_poly_array, coords, 'Locality')

        print('NASA Active fire Data MODIS C6 Australia and New Zealand 24h')
        coords = u_mod.\
                 coords_from_csv('MODIS_C6_Australia_and_New_Zealand_24h.csv',\
                                 1, 0)
        next_poly_array = u_mod.points_in_polygon(poly_array, coords, \
                                                  'Active_Fires')

        print('National Mobile Blackspot program')
        coords = u_mod.coords_from_csv_latin1('mbsp_database.csv', 6, 5)
        poly_array = u_mod.points_in_polygon(next_poly_array, coords, 'MBSP')

        print('AGIL Locations')
        coords = u_mod.coords_from_csv('agil_locations20190208.csv', 3, 2)
        next_poly_array = u_mod.points_in_polygon(poly_array, coords, 'AGIL')

        print('Polygons Centroids and Offset Vertices')
        coords = self.aus_poly_coords(next_poly_array)
        print(len(coords))
        poly_array = u_mod.points_in_polygon(next_poly_array, coords, 'Poly')
        for poly in range(0, len(poly_array)):
            poly_array[poly]['properties']['Aust'] = 0
            if poly_array[poly]['properties']['Poly'] > 0 \
               or poly_array[poly]['properties']['Island'] > 0 or \
               poly_array[poly]['properties']['Locality'] > 0 or \
               poly_array[poly]['properties']['Boundary'] > 0:
                poly_array[poly]['properties']['Aust'] = 1
                #out_array.append(poly_array[poly])

        return poly_array

    def aus_poly_coords(self, g_array):
        """
        generate coords inside map layer polygons to fill continent
        """
        # load the shapefile
        shape_file = shapefile.Reader("shapefiles/AUS_2016_AUST")
        # shapefile contains multipolygons
        shapes = shape_file.shapes()
        big_coords = shapes[0].points
        loc_poly_array = g_array
        coords = []
        for poly in range(0, len(g_array)):
            c_lon = loc_poly_array[poly]['properties']['lon']
            c_lat = loc_poly_array[poly]['properties']['lat']
            coords.append((c_lon, c_lat))
            for point in loc_poly_array[poly]['geometry']['coordinates'][0]:
                coords.append((point[0], point[1]))
            unique_coords = np.unique(coords, axis=0) # remove duplicate coordinates
        in_coords = []
        for subpolyptr in range(len(shapes[0].parts)-1):
            sub_coords = big_coords[shapes[0].parts[subpolyptr]:shapes[0].parts[subpolyptr+1]]
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


    def aus_poly_intersect(self, g_array):
        """
        Separate continental polygons from non continental
        """
        (num_poly, isect_array) = (len(g_array), [])
        a_val = 0 
        for poly in range(0, num_poly):
            if g_array[poly]['properties']['Aust'] > 0:
                g_array[poly]['properties']['a'] = a_val
                isect_array.append(g_array[poly])
                a_val += 1
        return isect_array


    def column_counts(self, g_array):
        """
        column counts for neighbour update
        """
        ref_table = []
        for record in range(0, len(g_array)):
            ref_table.append(g_array[record]['properties']['row'])

        ref_table_df = pd.DataFrame(ref_table)
        ref_table_df.columns = ['row']
        print(len(ref_table_df))

        odd_columns = ref_table.count(1)
        even_columns = ref_table.count(2)
        print(int(odd_columns), int(even_columns))
        return odd_columns, even_columns

    def update_neighbours(self, g_array, odd_columns, even_columns):
        """
        neighbour update of geojson Polygon array
        """
        ref_table = []
        for record in range(0, len(g_array)):
            g_rec = g_array[record]
            ref_table.append([g_rec['properties']['a'], \
                              g_rec['properties']['p'], \
                              g_rec['properties']['row']])

        ref_table_df = pd.DataFrame(ref_table)
        ref_table_df.columns = ['arr', 'poly', 'row']

        for g_ref in range(0, len(g_array)):
            g_poly = g_array[g_ref]['properties']['p']
#            if self.shape == 'hex':
#                (pol_n, pol_ne, pol_e, pol_se, pol_s, pol_sw, pol_w, pol_nw) = \
#                self.neighbours(g_array, g_poly, ref_table_df, \
#                                odd_columns)
#            else:
            (pol_n, pol_ne, pol_e, pol_se, pol_s, pol_sw, pol_w, pol_nw) = \
            self.neighbours(g_array, g_poly, ref_table_df, \
                            odd_columns)                
            g_array[g_ref]['properties']['p_N'] = pol_n
            g_array[g_ref]['properties']['p_NE'] = pol_ne
            g_array[g_ref]['properties']['p_E'] = pol_e
            g_array[g_ref]['properties']['p_SE'] = pol_se
            g_array[g_ref]['properties']['p_S'] = pol_s
            g_array[g_ref]['properties']['p_SW'] = pol_sw
            g_array[g_ref]['properties']['p_W'] = pol_w
            g_array[g_ref]['properties']['p_NW'] = pol_nw
        return g_array

    def neighbours(self, g_array, poly, ref_table_df, column_count):
        """
        neighbour update of geojson hex Polygon array
        """
        (val_n, val_ne, val_e, val_se, val_s, val_sw, val_w, val_nw) = \
        (-9, -9, -9, -9, -9, -9, -9, -9)
        if self.shape == 'hex':
            poly_n = (poly - (column_count*2-(poly % column_count))-\
                          (poly % column_count))
            poly_ne = (poly - (column_count*1-(poly % column_count))-\
                       (poly % column_count))
            poly_e = poly + 1
            poly_se = (poly + (column_count*1-(poly % column_count))+\
                       (poly % column_count))
            poly_s = (poly + (column_count*2-(poly % column_count))+\
                      (poly % column_count))
            poly_sw = (poly + (column_count*1-(poly % column_count))+\
                       (poly % column_count))-1
            poly_w = poly - 1
            poly_nw = (poly - (column_count*1-(poly % column_count))-\
                      (poly % column_count))-1
        else:
            poly_n = (poly - (column_count*1-(poly % column_count))-\
                      (poly % column_count))-1
            poly_ne = (poly - (column_count*1-(poly % column_count))-\
                   (poly % column_count))
            poly_e = poly + 1
            poly_se = (poly + (column_count*1-(poly % column_count))+\
                       ((poly % column_count)))+2
            poly_s = (poly + (column_count*1-(poly % column_count))+\
                      (poly % column_count))+1
            poly_sw = (poly + (column_count*1-(poly % column_count))+\
                       (poly % column_count))
            poly_w = poly - 1
            poly_nw = (poly - (column_count*1-(poly % column_count))-\
                       (poly % column_count))-2

        # North Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_n)]
            arr_data = g_array[int(ref_q['arr'])]
            val_n = poly_n
        except IndexError:
            pass
        except TypeError:
            pass
        
        # North East Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_ne)]
            arr_data = g_array[int(ref_q['arr'])]
            val_ne = poly_ne
        except IndexError:
            pass
        except TypeError:
            pass

        # East Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_e)]
            arr_data = g_array[int(ref_q['arr'])]
            val_e = poly_e
        except IndexError:
            pass
        except TypeError:
            pass

        # South East Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_se)]
            arr_data = g_array[int(ref_q['arr'])]
            val_se = poly_se
        except IndexError:
            pass
        except TypeError:
            pass

        # South Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_s)]
            arr_data = g_array[int(ref_q['arr'])]
            val_s = poly_s
        except IndexError:
            pass
        except TypeError:
            pass

        # South West Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_sw)]
            arr_data = g_array[int(ref_q['arr'])]
            val_sw = poly_sw
        except IndexError:
            pass
        except TypeError:
            pass

        # West Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_w)]
            arr_data = g_array[int(ref_q['arr'])]
            val_w = poly_w
        except IndexError:
            pass
        except TypeError:
            pass

        # North West Neighbour
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_nw)]
            arr_data = g_array[int(ref_q['arr'])]
            val_nw = poly_nw
        except IndexError:
            pass
        except TypeError:
            pass

        return val_n, val_ne, val_e, val_se, val_s, val_sw, val_w, val_nw


    def hexagons(self):
        """
        Process geojson Polygon array
        """

        print(self.params())
        hors = self.horizontal()
        verts = self.vertical()
        intersects = self.intersections(hors, verts)
        hex_array = self.hex_array(intersects, len(hors), len(verts))
        poi_hex_array = self.add_poly_poi(hex_array)
        (odd, even) = self.column_counts(poi_hex_array)
        nb_poi_hex_array = self.update_neighbours(poi_hex_array, odd, even)
        # cut out ocean polygons
        aus_hex_array = self.aus_poly_intersect(nb_poi_hex_array)
        # add neighbouur reference data
        nb_aus_hex_array = self.update_neighbours(aus_hex_array, odd, even)
        # return output from function
        return nb_aus_hex_array

    def boxes(self):
        """
        Process geojson Polygon array
        """

        print(self.params())
        hors = self.horizontal()
        verts = self.vertical()
        intersects = self.intersections(hors, verts)
        box_array = self.box_array(intersects, len(hors), len(verts))
        poi_box_array = self.add_poly_poi(box_array)
        (odd, even) = self.column_counts(poi_box_array)
        nb_poi_box_array = self.update_neighbours(poi_box_array, odd, even)
        # cut out ocean polygons
        aus_box_array = self.aus_poly_intersect(nb_poi_box_array)
        # add neighbouur reference data
        nb_aus_box_array = self.update_neighbours(aus_box_array, odd, even)
        #print("100% progress: It's not over til it's over")
        return nb_aus_box_array
