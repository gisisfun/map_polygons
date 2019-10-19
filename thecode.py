import os
from geopy.distance import geodesic
from geojson import Polygon,Feature,FeatureCollection
from math import pow,sqrt
import subprocess
import pandas as pd
import urllib.request
from pyunpack import Archive
import shapely as shaply

from isotiles.parameters import Bounding_Box, OSVars, Offsets, DataSets, Defaults


class test():
    value = Bounding_Box.Australia()
    defaults = Defaults()
    def __init__(self, north: Bounding_Box = value.North,
                 south: Bounding_Box = value.South,
                 east: Bounding_Box = value.East,
                 west: Bounding_Box = value.West,
                 radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape):
        self.North = north
        self.South = south
        self.East = east
        self.West = west
        self.Radial = radial
        self.Shape = shape
        self.FName = self.f_name()
        
        my_os = str(os.name)
        print(my_os)
        ntValues = OSVars.nt()
        posixValues = OSVars.posix()
        offValues = Offsets()
        
        if (my_os is 'posix'):
            self.cmdText = posixValues.ogr2ogr # '/usr/bin/ogr2ogr'
            self.Slash = posixValues.Slash # '/'
        else:
            self.cmdText = ntValues.ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Slash = ntValues.Slash # '\\'
            gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(gdal_vars)

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
        """
        ...

        
        return 'Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km' \
                .format(self.Shape, self.North, self.West, self.South,
                        self.East, self.Radial)
    def f_name(self):
        """
        Construct filename string
        """
        ...

        
        print(self.Shape + '_' + str(self.Radial) + 'km')
        return self.Shape + '_' + str(self.Radial) + 'km'

    def point_radial_distance(self,coords, brng, radial):
        return geodesic(kilometers=radial).destination(point=coords, bearing=brng)

    def horizontal(self):
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
        """
        ...
        
        
        (point_list,g_array, tabular_list) = ([],[],[])
        (lat_offset,top_left, poly_row_count) = (4, 0, int(max_v / len(self.horSeq)))
        rem_lat = max_v % (lat_offset + len(self.horSeq))
        (inc_by_rem, in_adj) = (True,0)
        p_tuple = ((False, True, True, True, False, True, True, True), \
                   (0, 0, -4, 0, 0, -4, -4, -4))
    
        (inc_by_rem, inc_adj) = (p_tuple[0][rem_lat],p_tuple[1][rem_lat])

        print('\n4/7 deriving hexagon polygons from intersection data')
        (row,last_lat_row, hexagon) = (1,0,0)

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
                (vertex00, vertex01, vertex20, vertex21, vertex50, vertex51) = \
                           (intersect_list[vertex[0]][0], \
                            intersect_list[vertex[0]][1], \
                            intersect_list[vertex[2]][0], \
                            intersect_list[vertex[2]][1], \
                            intersect_list[vertex[5]][0], \
                            intersect_list[vertex[5]][1])
                centre_lat = vertex01 + (vertex51 - vertex01) / 2
                centre_lon = vertex00 + (vertex50 - vertex00) / 2

                if (centre_lat is not last_lat_row) or last_lat_row is 0:
                    (bounds_n,bounds_s, bounds_e, bounds_w) = \
                                        (vertex01, vertex21, vertex20, vertex50)
                    last_lat_row = centre_lat
                    geopoly = Polygon([poly_coords])
                    hexagon += 1
                    est_area = (((3 * sqrt(3)) / 2) * pow(self.Radial, 2)) * 0.945
                    #estimate polygon area
                    geopoly = Feature(geometry = geopoly, properties = \
                                      {"p": hexagon,"row": row, \
                                       "lat": centre_lat, "lon": centre_lon, \
                                       "N": bounds_n, "S": bounds_s, \
                                       "E": bounds_e, "W": bounds_w, \
                                       "est_area": est_area})
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
        print('created dataset of {0} derived hexagon polygons'.format(len(g_array)))
        return g_array


    def box_array(self):
        (top_left, g_array, tabular_list) = (0, [], [])  # g_array - array of geojson formatted geometry element
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
                properties = {"p": top_left, "lat": centre_lat, "lon": centre_lon, \
                              "N": bounds_n, "S": bounds_s, "E": bounds_e, "W": bounds_w})
                g_array.append(geopoly)
                #append geojson geometry definition attributes to list
                #tabular dataset
                tabular_line = [top_left, centre_lat, centre_lon, \
                                bounds_n, bounds_s, bounds_e, bounds_w]
                tabular_list.append(tabular_line)
                #array of polygon and tabular columns

            #increment values
            top_left += 1
            vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left + max_v]

        print('\n5/7 boxes geojson dataset of {0} derived polygons'.format(len(g_array)))
        return g_array

    def points_and_polygons(self,GArray):

        (point_list, num_poly) = ([], len(GArray))

        for n in range (0, num_poly):
            num_coords = len(GArray[n]['geometry']['coordinates'][0])-2
            hexagon = GArray[n]['properties']['p']
            for i in range(0, num_coords):
                point_list.append( \
                    [hexagon, str(GArray[n]['geometry']['coordinates'][0][i][0]) + \
                     str(GArray[n]['geometry']['coordinates'][0][i][1])])
        return point_list

    def to_geojson(self,gArray):
        """
        Convert Features to FeatureCollection
        """
        ...
        
        print('\n5/7 geojson dataset of {0} derived hexagon polygons' \
              .format(len(gArray)))
        return FeatureCollection(gArray)

    def to_file(self,content):
        """
        Write string to file
        """
        ...
        
        print('writing geojson formatted {shape} dataset to file: {fname}_layer.json'\
              .format(shape = self.Shape, fname = self.FName))
        myfile = open('csv/{fname}_layer.csv'.format(fname = self.FName), 'w')
        #open file for writing geojson layer in geojson format
        myfile.write(str(content))  # write geojson layer to open file
        myfile.close()  # close file


    def to_shp_tab(self):
        """
        Convert geojson file to shapfile and tab file
        """
        ...
        
        shp_fname = 'shapefiles{slash}{fname}_layer.shp'.format(\
            fname = self.FName .replace(' ', '_'), \
            slash = self.Slash)
        tab_fname = 'tabfiles{slash}{fname}_layer.tab'.format( \
            fname = self.FName.replace(' ', '_'), \
            slash = self.Slash)
        json_fname = 'geojson{slash}{fname}_layer.json'.format( \
            fname = self.FName.replace(' ', '_'), \
            slash = self.Slash)
        tab_options = [self.cmdText, '-f', 'Mapinfo file', tab_fname, \
                       '-t_srs', 'EPSG:4823', json_fname]
        shp_options = [self.cmdText, '-f', 'ESRI Shapefile', shp_fname, \
                       '-t_srs', 'EPSG:4823', json_fname]
        try:
            # record the output!
            print('\nwriting {0} shapefile {1}_layer.shp'.format(self.Shape, self.FName))
            subprocess.check_call(shp_options)
            print('\nwriting {0} shapefile {1}_layer.tab'.format(self.Shape, self.FName))
            subprocess.check_call(tab_options)
        except FileNotFoundError:
            print('No files processed')


    def intersecting(self,pointsList):
        """
        Intersecting polygons list
        """
        ...
        
        point_df = pd.DataFrame(pointsList)
        point_df.columns = ['poly', 'latlong']
        point_df.to_csv('csv{slash}{outfile}_points.csv' \
                        .format(outfile = self.FName, \
                                slash = self.Slash), sep = ',')
        point_df_a = point_df  # make copy of dataframe
        process_point_df = pd.merge(point_df, point_df_a, on = 'latlong')
        # merge columns of same dataframe on concatenated latlong
        process_point_df = process_point_df[(process_point_df['poly_x']
    != process_point_df['poly_y'])]  # remove self references
        output_point_df = process_point_df[['poly_x', 'poly_y']].copy().sort_values(by=['poly_x']).drop_duplicates()
        #just leave polygon greferences and filter output

        output_point_df.to_csv('csv{slash}{outfile}_neighbours.csv' \
                               .format(outfile = self.FName, \
                                       slash = self.Slash), \
                               sep = ',', index = False)

    def file_deploy(self,RData):
        if not os.path.isfile(RData.FilePath.format(slash = self.Slash)):
            print('Downloading {descr} file in {fmt} file format'\
                  .format(fmt = RData.Format, descr = RData.Description))
            urllib.request.urlretrieve(url, RData.DownURL.format(slash = self.Slash))
            print('Unzipping {descr} file in {fmt} file format'\
                  .format(descr = RData.Description, fmt = RData.Format ))
            Archive(RData.ZipPath.format(slash = self.Slash)).extractall(RData.ZipDir\
                                                                         .format(slash = self.Slash))
        else:
            print('{descr} file in {fmt} file format exists'\
                  .format(descr = RData.Description, fmt = RData.Format))

    def ref_files(self):
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Australia.TabFormat()
        self.file_deploy(RefData)


    def point_in_polygon(coords_list,point_x,point_y):  
        poly = shply.Polygon(coords_list)
        p1=shply.Point(point_x, point_y)
        return p1.within(poly)
        
        
    def points_in_polygon(poly_coords,poly_id,bound_points_df):
        p_count=0
        poly = shply.Polygon(poly_coords)
        i=0
        for index, row in bound_points_df.iterrows():
            #p1 = shply.Point(query_points_list[i][0],query_points_list[i][1])
            p1 = shply.Point(row['longitude'], row['latitude'])
        
            if poly.contains(p1) is True:
                p_count += 1 
            i += 1        
        return poly_id,p_count