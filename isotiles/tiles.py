#all
import os
import pandas as pd

#Tiles
from geopy.distance import geodesic
from geojson import Polygon,Feature,FeatureCollection
from math import pow,sqrt
import matplotlib.path as mpltPath
import shapefile
import simplekml

from isotiles.parameters import Bounding_Box, OSVars, Offsets, Defaults
from isotiles.data import DataSets, POI

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
        (row,last_lat_row, poly_id) = (1,0,0)

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
            row = int(1 + int(poly_id / poly_row_count))
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
        """
        Neighbouring Polygons derivation
        
        Prerequisites:
        hex_array or box_array, horizontal, vertical ,Tiles
        
        Input variables:
        GArray
        """
        ...
        
        (point_list, num_poly) = ([], len(GArray))

        for n in range (0, num_poly):
            num_coords = len(GArray[n]['geometry']['coordinates'][0])-2
            poly_id = GArray[n]['properties']['p']
            for i in range(0, num_coords):
                point_list.append( \
                    [poly_id, str(GArray[n]['geometry']['coordinates'][0][i][0]) + \
                     str(GArray[n]['geometry']['coordinates'][0][i][1])])
        return point_list

    def tabular_dataframe(self,GArray):
        tabular_list = []
        (point_list, num_poly) = ([], len(GArray))
        num_coords = len(GArray[n]['geometry']['coordinates'][0])-2
        for i in range(0, num_coords):
            poly = GArray[n]['properties']['p']
            centre_lat =  GArray[n]['properties']['lat']
            centre_lon =  GArray[n]['properties']['long']
            bounds_n =  GArray[n]['properties']['N']
            bounds_s =  GArray[n]['properties']['S']
            bounds_e =  GArray[n]['properties']['E']                
            bounds_w =  GArray[n]['properties']['W']
            tabular_line =[poly, centre_lat, centre_lon, \
                           bounds_n, bounds_s, bounds_e, bounds_w]
            tabular_list.append(tabular_line)
        
        tabular_df = pd.DataFrame(tabular_list)
        #convert tabular array to tabular data frame
        tabular_df.columns = ['poly', 'lat', 'long', 'N', 'S', 'E', 'W']
        tabular_df.to_csv('csv{slash}{outfile}_dataset.csv' \
                          .format(outfile = outfile, slash = slash), \
                          sep = ',')
        return tabular_df

    def to_shp_file(self,GArray,fNameTempl):
        #tabular_list = []
        fName = 'shapefiles{slash}'+fNameTempl
        fPath = fName.format(shape = self.Shape,
                             size = self.Radial,
                             slash = self.Slash,
                             sfPath = self.ShapefilesPath,
                             fname = self.FName)
        prjPath = fPath + '.prj'
        w = shapefile.Writer(fPath) # , shapeType=3)
        #setup columns
        props_dict = GArray[0]['properties']
        (i, props_list) = 0, []
        for key in props_dict:
            if i < 2 or i > 8:
                w.field(key, 'N')
            else:
                w.field(key, 'N', decimal = 10)
            i = i + 1

        (point_list, num_poly) = ([], len(GArray))
        for n in range (0, num_poly):
            props_dict_rec = GArray[n]['properties']
            rec_str = "w.record("
            i = 0
            #print('props_list',len(props_dict))
            for key in props_dict_rec:
                
                rec_str = rec_str + key + ' = ' + str(props_dict_rec[key])
                
                if i is not len(props_dict)-1:
                     rec_str = rec_str + ','
                i = i +1
                
            rec_str = rec_str + ' )' 
            #print(rec_str)
            eval(rec_str)
                    
            #print([GArray[n]['geometry']['coordinates'][0]]) 
            w.poly([GArray[n]['geometry']['coordinates'][0]])
            #w.record(n)
        w.close()    
        # create the PRJ file
        msg = 'writing shapefile formatted {shape} dataset to file:' + fNameTempl +'.shp'
        print(msg.format(shape = self.Shape, fname = self.FName))  
        prj = open(prjPath, "w")
        epsg = 'GEOGCS["WGS 84",'
        epsg += 'DATUM["WGS_1984",'
        epsg += 'SPHEROID["WGS 84",6378137,298.257223563]]'
        epsg += ',PRIMEM["Greenwich",0],'
        epsg += 'UNIT["degree",0.0174532925199433]]'
        prj.write(epsg)
        prj.close()

    def to_kml_file(self,GArray,fNameTempl):
        fName = '{kPath}{slash}'+fNameTempl+'.kml'
        fPath = fName.format(kPath = self.KMLfilesPath,
                             shape = self.Shape,
                             size = self.Radial,
                             slash = self.Slash,
                             fname = self.FName)
        kml = simplekml.Kml()
        #setup columns
        props_dict = GArray[0]['properties']
        
        key_names_array = []
        for key in props_dict:
            key_names_array.append(key)
            

        (point_list, num_poly) = ([], len(GArray))
        for poly in range (0, num_poly):
            
            props_dict_rec = GArray[poly]['properties']
            (i,key_values_array) = (0,[])
            rec_descr = ""
            for key in props_dict:
                key_values_array.append(props_dict_rec[key])
                
                if i is not len(props_dict)-1:
                    rec_descr = rec_descr + key + ' = ' + str(props_dict_rec[key]) + '\n'
                else:
                    rec_descr = rec_descr + key + ' = ' + str(props_dict_rec[key]) + '\n'
                i =+ 1
            ev_str = 'pol = kml.newpolygon(name ="'    
            points_str = "["
            points_t=[]
            for points in GArray[poly]['geometry']['coordinates'][0]:
                points_t.append(tuple(points))
                points_str = points_str + "("\
                             + str(points[0]) + ","\
                             + str(points[1]) + "), "
            #print(points_t)
            #print(points_str)
            pol = kml.newpolygon(name = str(key_values_array[0]))
            pol.outerboundaryis=points_t
            pol.innerpoundaryis=points_t
            #outer = '",outerboundaryis=' + str(points_t) + ", "
            #inner = "innerboundaryis=" + str(points_t) + ")"
            #ev_str = ev_str + str(key_values_array[0]) + outer + inner
            #eval(ev_str)
            pol.description = rec_descr
            pol.style.polystyle.fill = 0
            
        msg = 'writing kml formatted {shape} dataset to file:' + fNameTempl +'.kml'
        print(msg.format(shape = self.Shape, fname = self.FName))       
        kml.save(fPath)

    def to_geojson_fmt(self,gArray):
        return FeatureCollection(gArray) 

    def to_geojson_file(self,gArray,fNameTempl):
        """
        Write string to file
        
        Prerequisites:
        to_geojson, hex_array or box_array, horizontal, vertical, Tiles
        
        Input variables:
        """
        ...
        content = FeatureCollection(gArray)
        msg = 'writing geojson formatted {shape} dataset to file:' + fNameTempl +'.json'
        print(msg.format(shape = self.Shape, fname = self.FName))
        fName = 'geojson{slash}'+fNameTempl+'.json'
        myfile = open(fName.format(fname = self.FName,slash = self.Slash), 'w')
        #open file for writing geojson layer in geojson format
        myfile.write(str(content))  # write geojson layer to open file
        myfile.close()  # close file

    def neighbours(self,pointsList):
        """
        Intersecting polygons list
        
        Prerequisites:
        hex_array or box_array, horizontal, vertical, Tiles
        
        Input variables:
        pointslist: array of points and metadata defining polygon shapes 
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

  
    def points_in_polygon(self, gArray, lat_longs, gLabel):
        """
        Counts for lat_longs generated
        """
        ...
        
        (point_list, num_poly) = ([], len(gArray))
        lat_longs_df=pd.DataFrame(lat_longs)
        lat_longs_df.columns = ['longitude','latitude']
        for poly in range (0, num_poly):
            poly_id = gArray[poly]['properties']['p']
            p_count = 0
            bound_points_df = lat_longs_df[(lat_longs_df['latitude'] >=\
                                            gArray[poly]['properties']['S']) & \
                                           (lat_longs_df['latitude'] <=\
                                            gArray[poly]['properties']['N']) & \
                                           (lat_longs_df['longitude'] <=\
                                            gArray[poly]['properties']['E']) & \
                                           (lat_longs_df['longitude'] >=\
                                            gArray[poly]['properties']['W'])]
            #this is dodgy but it works for now
            if bound_points_df.size is 2:
                bound_points_df.append(bound_points_df)

            if (bound_points_df.size > 0):
                poly_coords = []
                num_coords = len(gArray[poly]['geometry']['coordinates'][0])-2
                for coord in range(0, num_coords):
                    poly_coords.append( \
                        [gArray[poly]['geometry']['coordinates'][0][coord][0], \
                         gArray[poly]['geometry']['coordinates'][0][coord][1]])
                path = mpltPath.Path(poly_coords)

                for index, row in bound_points_df.iterrows():
                    if path.contains_point([row['longitude'],row['latitude']]) is True:
                        p_count += 1 
                                    
            gArray[poly]['properties'][gLabel] = float(p_count)
                
        return gArray


    def aus_poly_intersect(self,gArray):
        # load the shapefile
        sf = shapefile.Reader("shapefiles/AUS_2016_AUST")
        thePoints = POI.Islands()
        # shapefile contains multipolygons
        shapes = sf.shapes()
        big_coords = shapes[0].points
        last_progress = -999
        hcount = 0
        # get the query polygons
        (point_list, num_poly,isectArray) = ([], len(gArray),[])

        print('Adding the Boundary/Coast Line points')
        points = []
        for point in big_coords:
            points.append([point[0],point[1]])

        bdy_poly_array = self.points_in_polygon(gArray,points,'Boundary')

        print('Adding Island points')

        islands_list = thePoints.Coords
        points = []
        for island in islands_list:
           points.append([island[1],island[2]])

        isl_poly_array = self.points_in_polygon(bdy_poly_array,points,'Island')
        
        print('Adding GNAF Locality points')
        thePoints = POI.GNAFLocalities()
        localities_list = thePoints.Coords
        points = []
        for locality in localities_list:
           points.append([locality[4],locality[3]])

        loc_poly_array = self.points_in_polygon(isl_poly_array,points,'Locality')

        (poi_progress, cent_progress, poly_progress, omit_progress) = ([],[],[],[])
        for poly in range (0, num_poly):
            inPoly = False
            progress = int((poly/num_poly)*100)
            #loc_poly_array[poly]['properties']['Aust'] = 0
            # get the reference sub polygons
            #try centroid
            c_lon = loc_poly_array[poly]['properties']['lon']
            c_lat = loc_poly_array[poly]['properties']['lat']
            if loc_poly_array[poly]['properties']['Island'] > 0 or loc_poly_array[poly]['properties']['Locality'] > 0 or loc_poly_array[poly]['properties']['Boundary'] > 0:
                inPoly = True
                isectArray.append(loc_poly_array[poly])
                poi_progress.append(loc_poly_array[poly]['properties']['p'])
                hcount += 1
            else:
                
                for point in loc_poly_array[poly]['geometry']['coordinates'][0]:
                    for subpolyptr in range(len(shapes[0].parts)-1):
                        sub_coords = big_coords[shapes[0].parts[subpolyptr]:shapes[0].parts[subpolyptr+1]]
                        path = mpltPath.Path(sub_coords)
                                                  
                        if inPoly is False:
                            if path.contains_point([c_lon,c_lat]) is True:
                                inPoly = True
                                isectArray.append(loc_poly_array[poly])
                                cent_progress.append(loc_poly_array[poly]['properties']['p'])
                                hcount += 1
                            
                        if inPoly is False: 
                            if path.contains_point([point[0],point[1]]) is True:
                                inPoly = True
                                isectArray.append(loc_poly_array[poly])
                                poly_progress.append(loc_poly_array[poly]['properties']['p'])
                                hcount += 1

            if inPoly is False:
                omit_progress.append(loc_poly_array[poly]['properties']['p'])
                            
            if progress is not last_progress:
                print(progress,'% progress:',poly,'polygons processed for',hcount,'intersections for output')
                print('1. poi:',poi_progress)
                print('2. centroid:',cent_progress)
                print('3. poly:',poly_progress)
                print('4. Omitted:',len(omit_progress), 'polygons')
                
                
                last_progress = progress
                (poi_progress, cent_progress, poly_progress, omit_progress) = ([],[],[],[])
        #return loc_poly_array
        return isectArray
