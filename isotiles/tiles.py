#all
import os
import pandas as pd
import numpy as np
import json

#Tiles
from geopy.distance import geodesic
from geojson import Polygon,Feature,FeatureCollection
from math import pow,sqrt
import matplotlib.path as mpltPath
import shapefile #to be moved to util from add_poly_poi

from isotiles.parameters import Bounding_Box, OSVars, Offsets, Defaults
#from isotiles.poi import POI
from isotiles.datasets import DataSets
from isotiles.util import Util

class Neighbours:
    __slots_ = ("poly","row_count","g_array")
    def __init__(self,poly,g_array,row_count):
        self.poly = poly
        self.row_count = row_count
        self.g_array = g_array
        
    def row_counts(self):
        row_counts = 41
        return row_counts
                
    
    def North(self):   
        poly_N = (self.poly - (self.row_count*2-(self.poly % self.row_count))-((self.poly % self.row_count)))
        return poly_N
    
    def North_East(self):   
        poly_NE = (self.poly - (self.row_count*1-(self.poly % self.row_count))-((self.poly % self.row_count)))
        return poly_NE

    def East(self):   
        poly_E = self.poly + 1
        return poly_E
    
    def South_East(self):  
        poly_SE = (self.poly + (self.row_count*1-(self.poly % self.row_count))+((self.poly % self.row_count)))
        return poly_SE
    
    def South(self):   
        poly_S = (self.poly + (self.row_count*2-(self.poly % self.row_count))+((self.poly % self.row_count)))
        return poly_S

    def South_West(self):
        poly_SW = (self.poly + (self.row_count*1-(self.poly % self.row_count))+((self.poly % self.row_count)))-1
        return poly_SW
        
    def West(self):
        poly_W = self.poly - 1
        return poly_W
    
    def North_West(self):
        poly_NW = (self.poly - (self.row_count*1-(self.poly % self.row_count))-((self.poly % self.row_count)))-1
        return poly_NW


class Tiles():
    """
    Modules for map_polygons
    """
    ...
    
    value = Bounding_Box.Australia()
    defaults = Defaults()
    
    def __init__(self, north: Bounding_Box = value.North,
                 south: Bounding_Box = value.South,
                 east: Bounding_Box = value.East,
                 west: Bounding_Box = value.West,
                 radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 metadata: Defaults = defaults.MetaDataPath,
                 logfiles: Defaults = defaults.LogfilesPath,
                 kmlfiles: Defaults = defaults.KMLfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath,
                 geojson: Defaults = defaults.GeoJSONPath,
                 vrt: Defaults = defaults.VRTPath,
                 csv: Defaults = defaults.CSVPath,
                 spatialite: Defaults = defaults.SpatialitePath,
                 sql: Defaults = defaults.SQLPath,
                 slash: Defaults = defaults.Slash,
                 ogr2ogr_com: Defaults = defaults.Ogr2ogr,
                 spatialite_com: Defaults = defaults.Spatialite,
                 extn: Defaults = defaults.Extn):
        """
        supply variables for map_polygons
        """
        self.North = north
        self.South = south
        self.East = east
        self.West = west
        self.Radial = radial
        self.Shape = shape
        self.FName = self.f_name()
        self.ShapefilesPath = shapefiles
        self.KMLfilesPath = kmlfiles
        
        offValues = Offsets()
        self.Ogr2ogr = ogr2ogr_com # '/usr/bin/ogr2ogr'
        self.Slash = slash # '/'
        self.Extn = extn
        self.Spatialite = spatialite_com

        if self.Shape is 'hex':
            self.horSeq = [offValues.Short, offValues.Short,
                           offValues.Short, offValues.Short]
            self.vertSeq = [offValues.Short, offValues.Long,
                           offValues.Short, offValues.Long]
            
        else:
            self.horSeq = [offValues.Long, offValues.Long,
                           offValues.Long, offValues.Long]
            self.vertSeq = [offValues.Long, offValues.Long,
                            offValues.Long, offValues.Long]

    def params(self):
        """
        Construct feedback of user variables for user
        
        Dependencies:
        Tiles
        """
        ...
        
        return 'Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km' \
                .format(self.Shape, self.North, self.West, self.South,
                        self.East, self.Radial)

    def params(self):
        """
        Construct feedback of user variables for user
        
        Dependencies:
        Tiles
        """
        ...

        
        return 'Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km' \
                .format(self.Shape, self.North, self.West, self.South,
                        self.East, self.Radial)
    def metadata(self):
        layer_dict = {'Bounds': {'Australia': {'North': self.North,'South': self.South, \
                                           'West': self.West,'East': self.East}}}
        layer_dict['Param'] = {}
        layer_dict['Param']['side_km'] = radial
        layer_dict['Param']['epsg'] = 4326
        layer_dict['Param']['shape'] = self.Shape
        layer_dict['Boxes'] = {}
        layer_dict['Boxes']['long'] = 1
        hor_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'], \
                   layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
        vert_seq = [layer_dict['Boxes']['long'], layer_dict['Boxes']['long'], \
                    layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
    
        layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
        layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
        layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
        layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min()
    
        print('\n7/7 boxes json metadata to written to file: {0}_metadata.json' \
              .format(outfile))
        myfile = open('metadata{slash}{outfile}_metadata.json' \
                      .format(outfile = outfile, slash = slash), 'w')  # open file for writing geojson layer
        myfile.write(str(json.dumps(layer_dict)))
        #write geojson layer to open file
        myfile.close()  # close file
        
    def f_name(self):
        """
        Construct filename string
        
        Dependencies:
        Tiles
        """
        ...

        
        print(self.Shape + '_' + str(self.Radial) + 'km')
        return self.Shape + '_' + str(self.Radial) + 'km'

    def point_radial_distance(self,coords, brng, radial):
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
        (angle, new_north, i, longitudes) = (180, self.North, 0, [])
        #print(east,new_north,south,'\n')
        longitudes.append([[self.North,self.West],[self.North,self.East]])

        while new_north >= self.South:
            if i > 3:
                i = 0
            
            latlong = [new_north,self.East]
            p = self.point_radial_distance(latlong,angle,self.Radial * self.horSeq[i]) 
            new_north = p[0]
            longitudes.append([[p[0],self.West],[p[0],self.East]])
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
        print('east {0} west {1}'.format(self.East,self.West))

        (angle, new_west, i, latitudes) = (90, self.West, 0, [])

        latitudes.append([[self.North,self.West],[self.South,self.West]])
        while new_west <= self.East:
            if i > 3:
                i = 0

            latlong = [self.North,new_west]
            p = self.point_radial_distance(latlong,angle, self.Radial*self.vertSeq[i])
            new_west = p[1]
            latitudes.append([[self.North,p[1]],[self.South,p[1]]])    
            i += 1
            
        return latitudes


    def line_intersection(self,line1, line2):
        """
        source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
        
        Dependencies:
        intersections,horizontal,vertical,Tiles
        """
        ...
        
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        (x, y) = (det(d, xdiff) / div, det(d, ydiff) / div)
        return x, y
    
    def intersections(self,hor_line_list, vert_line_list):
        """
        Intersecting Lines as points
        
        Dependencies:
        horizontal,vertical,Tiles
        
        Input variables:
        hor_line_list:
        vert_line_list:
        """
        ...
        
        print('\n3/7 deriving intersection point data between horizontal and vertical lines')
        (intersect_list, hor_max, vert_max) = ([],len(hor_line_list), len(vert_line_list))
        for h in range(0, hor_max):
            for v in range(0, vert_max):
                intersect_point = self.line_intersection(hor_line_list[h],
                vert_line_list[v])
                intersect_data = [intersect_point[1], intersect_point[0]]
                intersect_list.append(intersect_data)

        print('derived {0} points of intersection'.format(len(intersect_list)))
        return intersect_list
    

    def hex_array(self,intersect_list,max_h, max_v):
        """
        Put it all together - deriving hexagon polygons from intersection data
        
        
        Prerequisites:
        intersections, horizontal, vertical, Tiles
        
        Input variables:
        intersect_list:
        max_h:
        max_v:
        """
        ...
        self.Shape = 'hex'
        self.FName = self.f_name()
        
        (point_list,g_array, tabular_list) = ([],[],[])
        (lat_offset,top_left, poly_row_count) = (4, 0, int(max_v / len(self.horSeq)))
        rem_lat = max_v % (lat_offset + len(self.horSeq))
        (inc_by_rem, in_adj) = (True,0)
        p_tuple = ((False, True, True, True, False, True, True, True), \
                   (0, 0, -4, 0, 0, -4, -4, -4))
    
        (inc_by_rem, inc_adj) = (p_tuple[0][rem_lat],p_tuple[1][rem_lat])

        print('\n4/7 deriving hexagon polygons from intersection data')
        (row,col,last_lat_row, poly_id) = (1,1,0,0)

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
                (vertex00, vertex01, vertex20, vertex21,vertex30, vertex31, vertex50, vertex51) = \
                           (intersect_list[vertex[0]][0], intersect_list[vertex[0]][1], \
                            intersect_list[vertex[2]][0], intersect_list[vertex[2]][1], \
                            intersect_list[vertex[3]][0], intersect_list[vertex[3]][1], \
                            intersect_list[vertex[5]][0], intersect_list[vertex[5]][1])
                centre_lat = vertex01 + (vertex51 - vertex01) / 2
                centre_lon = vertex00 + (vertex50 - vertex00) / 2

                if (centre_lat is not last_lat_row) or last_lat_row is 0:
                    (bounds_n,bounds_s, bounds_e, bounds_w) = \
                                        (vertex01, vertex31, vertex20, vertex50)
                    last_lat_row = centre_lat
                    geopoly = Polygon([poly_coords])
                    poly_id += 1
                    est_area = (((3 * sqrt(3)) / 2) * pow(self.Radial, 2)) * 0.945
                    #estimate polygon area
                    geopoly = Feature(geometry = geopoly, properties = \
                                      {"p": poly_id,"row": row, \
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
                    donothing = True

            except IndexError:
                donothing = True

            (last_row, last_lat_row) = (row, centre_lat)
            row = int(1 + int(poly_id / poly_row_count))
            top_left += lat_offset
            if row is not last_row:
                col = 1
                top_left += inc_adj
                if inc_by_rem:
                    top_left += rem_lat
                if row % 2 is 0:
                    top_left += 2
                if row & 1:
                    top_left += -2
            else:
                col += 1
        print('created dataset of {0} derived hexagon polygons'.format(len(g_array)))
        return g_array

    def box_array(self,intersect_list,max_h, max_v):
        """
        Create array of box shaped polygons
        
        Prerequisites:
        horizontal, vertical, Tiles
        
        Input variables:
        Provided
        """
        ...
        self.Shape = 'box'
        self.FName = self.f_name()
        
        (top_left, g_array, col, row) = (0, [], 1, 1)  # g_array - array of geojson formatted geometry element
        print('\n4/7 deriving boxes polygons from intersection data')
        vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left + max_v]

        while (vertex[2] < (max_h) * (max_v)):
            poly_coords = [intersect_list[vertex[0]] , \
                           intersect_list[vertex[1]], intersect_list[vertex[2]], \
                           intersect_list[vertex[3]], intersect_list[vertex[0]]]
            (vertex00, vertex01, vertex10, vertex11, vertex20, vertex21, vertex30, vertex31) = \
                       (intersect_list[vertex[0]][0], intersect_list[vertex[0]][1], \
                        intersect_list[vertex[1]][0], intersect_list[vertex[1]][1], \
                        intersect_list[vertex[2]][0], intersect_list[vertex[2]][1],
                        intersect_list[vertex[3]][0], intersect_list[vertex[3]][1])
            centre_lat = vertex01 + (vertex21 - vertex01) / 2
            centre_lon = vertex00 + (vertex20 - vertex00) / 2
            bounds_n = vertex01
            bounds_s = vertex31
            bounds_e = vertex10
            bounds_w = vertex00
            if bounds_e > bounds_w:
                geopoly = Polygon([poly_coords])
                geopoly = Feature(geometry=geopoly, \
                properties = {"p": top_left, "a": poly_id-1, \
                              "lat": centre_lat, "lon": centre_lon, \
                              "N": bounds_n, "S": bounds_s, \
                              "E": bounds_e, "W": bounds_w, \
                              "row": row, "col": col, \
                              "Aust": 0,"p_N":-9, \
                              "p_NE":-9, "p_E":-9, \
                              "p_SE":-9, "p_S":-9, \
                              "p_SW":-9, "p_W":-9})
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


    def update_poly_array_ref(self,g_array):
        for g_ref in range(0,len(self.g_array)):
            g_array[g_ref]['properties']['a'] = g_ref
        return g_array
    

    def add_poly_poi(self,g_array):
        u = Util() 
        # load the shapefile
        sf = shapefile.Reader("shapefiles/AUS_2016_AUST")
        
        # shapefile contains multipolygons
        shapes = sf.shapes()
        big_coords = shapes[0].points
        # get the query polygons
        (point_list, num_poly,isectArray) = ([], len(g_array),[])

        print('Adding the Boundary/Coast Line points')
        points = []
        longs = [float(item[0]) for item in big_coords]
        lats = [float(item[1]) for item in big_coords]
        coords = [(x,y) for x,y in zip(longs,lats)]

        poly_array = u.points_in_polygon(g_array,coords,'Boundary')

        print('Adding Island points')
        coords = u.coords_from_csv('islands.csv',1,2)       
        next_poly_array = u.points_in_polygon(poly_array,coords,'Island')
        
        print('Adding GNAF Locality points')
        coords = u.coords_from_csv('aug_gnaf_2019_locality.csv',4,3)
        poly_array = u.points_in_polygon(next_poly_array,coords,'Locality')

        print('NASA Active fire Data MODIS C6 Australia and New Zealand 24h')
        coords = u.coords_from_csv('MODIS_C6_Australia_and_New_Zealand_24h.csv',1,0)
        next_poly_array = u.points_in_polygon(poly_array,coords,'Active_Fires')

        print('National Mobile Blackspot program')
        coords = u.coords_from_csv_latin1('mbsp_database.csv',6,5)
        poly_array = u.points_in_polygon(next_poly_array,coords,'MBSP')

        print('AGIL Locations')
        coords = u.coords_from_csv('agil_locations20190208.csv',3,2)
        next_poly_array = u.points_in_polygon(poly_array,coords,'AGIL')
        
        print('Polygons Centroids and Offset Vertices')
        coords = self.aus_poly_coords(next_poly_array)
        poly_array = u.points_in_polygon(next_poly_array,coords,'Fred')
        out_array = []
        for poly in range (0, len(poly_array)):
            poly_array[poly]['properties']['Aust'] = 0
            if poly_array[poly]['properties']['Fred'] > 0 \
               or poly_array[poly]['properties']['Island'] > 0 or \
               poly_array[poly]['properties']['Locality'] > 0 or \
               poly_array[poly]['properties']['Boundary'] > 0:
                poly_array[poly]['properties']['Aust'] = 1
                #out_array.append(poly_array[poly])
            
        return poly_array

    def aus_poly_coords(self,g_array):
        # load the shapefile
        sf = shapefile.Reader("shapefiles/AUS_2016_AUST")
        # shapefile contains multipolygons
        shapes = sf.shapes()
        big_coords = shapes[0].points
        loc_poly_array = g_array
        coords = []
        for poly in range (0, len(g_array)):
            c_lon = loc_poly_array[poly]['properties']['lon']
            c_lat = loc_poly_array[poly]['properties']['lat']
            coords.append((c_lon,c_lat))
            for point in loc_poly_array[poly]['geometry']['coordinates'][0]:
                coords.append((point[0],point[1]))
            unique_coords = np.unique(coords, axis = 0) # remove duplicate coordinates
        in_coords = []
        for subpolyptr in range(len(shapes[0].parts)-1):
            sub_coords = big_coords[shapes[0].parts[subpolyptr]:shapes[0].parts[subpolyptr+1]]
            path = mpltPath.Path(sub_coords)
            np_arr = np.array(sub_coords)
            (arr_min, arr_max) = (np.min(np_arr,axis=0),np.max(np_arr,axis=0))
            (bounds_N,bounds_S, bounds_E, bounds_W) = (arr_max[1], arr_min[1], arr_max[0], arr_min[0])
            inBBox = False                       
            for point in unique_coords:
                if point[1] < bounds_N and point[1] > bounds_S and point[0] < bounds_E and point[0] > bounds_W:
                    inBBox = True
                if inBBox is True:
                    if path.contains_point([point[0],point[1]-0.0001]) is True:
                        in_coords.append((point[0],point[1]-0.0001))
        return in_coords


    def aus_poly_intersect(self,g_array):
        (num_poly,isectArray) = (len(g_array),[])

        for poly in range (0, num_poly):
            if g_array[poly]['properties']['Aust'] > 0:
                isectArray.append(g_array[poly])
        return isectArray

    
    def column_counts(self,g_array):
        ref_table = []
        for record in range(0,len(g_array)):
            ref_table.append(g_array[record]['properties']['row'])
        
        ref_table_df = pd.DataFrame(ref_table)
        ref_table_df.columns = ['row']
        print(len(ref_table_df))        
        
        odd_columns = ref_table.count(1)
        even_columns = ref_table.count(2)
        print(int(odd_columns),int(even_columns))
        return odd_columns,even_columns
        
    def update_neighbours(self,g_array,odd_columns,even_columns):
        ref_table = []
        for record in range(0,len(g_array)):
            g_rec = g_array[record]
            ref_table.append([g_rec['properties']['a'],g_rec['properties']['p'],g_rec['properties']['row']])
        
        ref_table_df = pd.DataFrame(ref_table)
        ref_table_df.columns = ['arr', 'poly','row']        

        for g_ref in range(0,len(g_array)):
            g_poly = g_array[g_ref]['properties']['p']
            (pol_N,pol_NE,pol_E,pol_SE,pol_S,pol_SW,pol_W,pol_NW) = self.neighbours_hex(g_array,g_poly,ref_table_df,odd_columns)
            g_array[g_ref]['properties']['p_N'] = pol_N
            g_array[g_ref]['properties']['p_NE'] = pol_NE
            g_array[g_ref]['properties']['p_E'] = pol_E
            g_array[g_ref]['properties']['p_SE'] = pol_SE
            g_array[g_ref]['properties']['p_S'] = pol_S
            g_array[g_ref]['properties']['p_SW'] = pol_SW
            g_array[g_ref]['properties']['p_W'] = pol_W
            g_array[g_ref]['properties']['p_NW'] = pol_NW            
        return g_array 

    def neighbours_hex(self, g_array,poly,ref_table_df,column_count):
        
        # North Neighbour
        try:
            poly_N = (poly - (column_count*2-(poly % column_count))-((poly % column_count)))
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_N)]
            arr_data = g_array[int(ref_q['arr'])]
            val_N = poly_N
        except:
            val_N = -9
            
        # North East Neighbour
        poly_NE = (poly - (column_count*1-(poly % column_count))-((poly % column_count)))
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_NE)]
            arr_data = g_array[int(ref_q['arr'])]
            val_NE = poly_NE
        except:
            val_NE = -9
            
        # East Neighbour
        poly_E = poly + 1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_E)]
            arr_data = g_array[int(ref_q['arr'])]
            val_E = poly_E
        except:
            val_E = -9
            
        # South East Neighbour
        poly_SE = (poly + (column_count*1-(poly % column_count))+((poly % column_count)))
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_SE)]
            arr_data = g_array[int(ref_q['arr'])]
            val_SE = poly_SE
        except:
            val_SE = -9
            
        # South Neighbour
        poly_S = (poly + (column_count*2-(poly % column_count))+((poly % column_count)))
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_S)]
            arr_data = g_array[int(ref_q['arr'])]
            val_S = poly_S
        except:
            val_S = -9
        
        # South West Neighbour
        poly_SW = (poly + (column_count*1-(poly % column_count))+((poly % column_count)))-1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_SW)]
            arr_data = g_array[int(ref_q['arr'])]
            val_SW = poly_SW
        except:
            val_SW = -9
            
        # West Neighbour
        poly_W = poly - 1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_W)]
            arr_data = g_array[int(ref_q['arr'])]
            val_W = poly_W
        except:
            val_W = -9
            
        # North West Neighbour
        poly_NW = (poly - (column_count*1-(poly % column_count))-((poly % column_count)))-1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_NW)]
            arr_data = g_array[int(ref_q['arr'])]
            val_NW = poly_NW
        except:
            val_NW = -9
        
        return val_N,val_NE,val_E,val_SE,val_S,val_SW,val_W,val_NW

    def neighbours_box(self, g_array,poly,ref_table_df,column_count):
        
        # North Neighbour
        poly_N = (poly - (column_count*1-(poly % column_count))-((poly % column_count)))
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_N)]
            arr_data = g_array[int(ref_q['arr'])]
            val_N = poly_N
        except:
            val_N = -9
            
        # North East Neighbour
        poly_NE = (poly - (column_count*1-(poly % column_count))-((poly % column_count)))+1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_NE)]
            arr_data = g_array[int(ref_q['arr'])]
            val_NE = poly_NE
        except:
            val_NE = -9
            
        # East Neighbour
        poly_E = poly + 1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_E)]
            arr_data = g_array[int(ref_q['arr'])]
            val_E = poly_E
        except:
            val_E = -9
            
        # South East Neighbour
        poly_SE = (poly + (column_count*1-(poly % column_count))+((poly % column_count)))+1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_SE)]
            arr_data = g_array[int(ref_q['arr'])]
            val_SE = poly_SE
        except:
            val_SE = -9
            
        # South Neighbour
        poly_S = (poly + (column_count*1-(poly % column_count))+((poly % column_count)))
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_S)]
            arr_data = g_array[int(ref_q['arr'])]
            val_S = poly_S
        except:
            val_S = -9
        
        # South West Neighbour
        poly_SW = (poly + (column_count*1-(poly % column_count))+((poly % column_count)))-1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_SW)]
            arr_data = g_array[int(ref_q['arr'])]
            val_SW = poly_SW
        except:
            val_SW = -9
            
        # West Neighbour
        poly_W = poly - 1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_W)]
            arr_data = g_array[int(ref_q['arr'])]
            val_W = poly_W
        except:
            val_W = -9
            
        # North West Neighbour
        poly_NW = (poly - (column_count*1-(poly % column_count))-((poly % column_count)))-1
        try:
            ref_q = ref_table_df[(ref_table_df['poly'] == poly_NW)]
            arr_data = g_array[int(ref_q['arr'])]
            val_NW = poly_NW
        except:
            val_NW = -9
        
        return val_N,val_NE,val_E,val_SE,val_S,val_SW,val_W,val_NW


    def hexagons(self):
        print(self.params())
        hors = self.horizontal()
        verts = self.vertical()
        intersects = self.intersections(hors,verts)
        hex_array = self.hex_array(intersects,len(hors),len(verts))
        poi_hex_array = self.add_poly_poi(hex_array)
        
        (odd,even) = self.column_counts(poi_hex_array)
        nb_poi_hex_array = self.update_neighbours(poi_hex_array,odd,even)    
        # cut out ocean polygons
        aus_hex_array = self.aus_poly_intersect(nb_poi_hex_array)
        # add neighbouur reference data
        nb_aus_hex_array = self.update_neighbours(aus_hex_array,odd,even)
        # return output from function
        return nb_aus_hex_array

    def boxes(self):
        print(self.params())
        hors = self.horizontal()
        verts = self.vertical()
        intersects = self.intersections(hors,verts)
        box_array = self.box_array(intersects,len(hors),len(verts))

        poi_box_array = self.add_poly_poi(box_array)
        (odd,even) = self.column_counts(poi_box_array)
        nb_poi_box_array = self.update_neighbours(poi_box_array,odd,even)
    
        # cut out ocean polygons
        aus_box_array = self.aus_poly_intersect(nb_poi_box_array)
        # add neighbouur reference data
        nb_aus_box_array = self.update_neighbours(aus_box_array,odd,even)
        #print("100% progress: It's not over til it's over")
        return nb_aus_box_array
