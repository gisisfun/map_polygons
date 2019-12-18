import os
import urllib.request
from pyunpack import Archive
import numpy as np
import shapefile
import simplekml
import csv

from isotiles.parameters import Bounding_Box, OSVars, Offsets, Defaults
from isotiles.datasets import DataSets
from geojson import FeatureCollection

class Util():
    """
    Generic Geospatial funcionality
    """
    defaults = Defaults()

    def __init__(self,radial: Defaults = defaults.Radial,
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
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.Radial = radial
        self.Shape = shape
        self.Charset = 'CP1252'

        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.ImagesPath = images
        self.MetaDataPath = metadata
        self.ShapefilesPath = shapefiles
        self.GeoJSONPath = geojson
        self.KMLfilesPath = kmlfiles
        self.VRTPath = vrt
        self.CSVPath = csv 
        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.FName = self.f_name()
        self.Ogr2ogr = ogr2ogr_com
        self.Slash = slash 
        self.Extn = extn
        self.Spatialite = spatialite_com

    def f_name(self):
        """
        Construct filename string
        
        """
        ...

        
        print(self.Shape + '_' + str(self.Radial) + 'km')
        return self.Shape + '_' + str(self.Radial) + 'km'
 
    def file_deploy(self,RData):
        """
        Deploy downloaded files
        
        Prerequisites:
        ref_files
        
        Input variables:
        """

        if not os.path.isfile(RData.FilePath.format(slash = self.Slash)):
            print('Downloading {descr} file in {fmt} file format'\
                  .format(fmt = RData.Format, descr = RData.Description))
            
            urllib.request.urlretrieve(RData.DownURL, RData.ZipPath.format(slash = self.Slash))
            if RData.ZipPath.endswith('zip') is True:
                print('Unzipping {descr} file in {fmt} file format'\
                    .format(descr = RData.Description, fmt = RData.Format ))
                print('extracting files')
                Archive(RData.ZipPath.format(slash = self.Slash)).extractall(RData.ZipDir\
                                                                         .format(slash = self.Slash))
        else:
            print('{descr} file in {fmt} file format exists'\
                  .format(descr = RData.Description, fmt = RData.Format))


    
    def ref_files_polygons(self):
        """
        Get reference files
        Prerequisites:
        
        Input variables:
        """
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.AGIL_Dataset.CSVFormat()
        self.file_deploy(RefData)

        RefData = DataSets.MBSP.CSVFormat()
        self.file_deploy(RefData)

        RefData = DataSets.NASA_Active_Fire_Data.Modis_C6_1km.CSVFormat()
        self.file_deploy(RefData)

    def ref_files_poly_wt(self):
        """
        Get reference files
        Prerequisites:
        
        Input variables:
        """
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2011.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2016.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.AGIL_Dataset.CSVFormat()
        self.file_deploy(RefData)

        RefData = DataSets.OpenStreetMaps.ShapeFormat()
        self.file_deploy(RefData)

    def coords_from_csv_latin1(self,fname,lon_c,lat_c):

        csv.register_dialect(
            'mydialect',
            delimiter = ',',
            quotechar = '\'',
            doublequote = True,
            skipinitialspace = True,
            lineterminator = '\r\n',
            quoting = csv.QUOTE_MINIMAL)

        with open('{csvpath}{slash}{fname}'.format(csvpath = self.CSVPath, fname = fname, slash = self.Slash), encoding='latin1') as csvfile:
            data = list(csv.reader(csvfile, dialect='mydialect'))

        longs = []
        lats = []

        for i in range(1,len(data)-1):
            print('')
            try:
                longs.append(float(data[i][lon_c]))
                lats.append(float(data[i][lat_c]))
            except:
                print('error')

        coords = [(x,y) for x,y in zip(longs,lats)]
        return coords

    def coords_from_csv(self,fname,lon_c,lat_c):

        #csv.Sniffer
        csv.register_dialect(
            'mydialect',
            delimiter = ',',
            quotechar = '\'',
            doublequote = True,
            skipinitialspace = True,
            lineterminator = '\r\n',
            quoting = csv.QUOTE_MINIMAL)


        with open('{csvpath}{slash}{fname}'.format(csvpath = self.CSVPath, fname = fname, slash = self.Slash), newline='', encoding='utf-8') as csvfile:
            data = list(csv.reader(csvfile, dialect='mydialect'))

        longs = [float(item[lon_c]) for item in data[1:]]
        lats = [float(item[lat_c]) for item in data[1:]]
        coords = [(x,y) for x,y in zip(longs,lats)]
        return coords
    
    def from_geojson_file(self,fNameTempl):
        """
        Read GeoJSON from file
        
        Prerequisites:
        
        Input variables:
        """
        ...

        msg = 'reading geojson formatted dataset from file:' + fNameTempl +'.json'
        print(msg.format(shape = self.Shape, fname = self.FName))
        fName = 'geojson{slash}'+fNameTempl+'.json'
        myfile = open(fName.format(fname = self.FName,slash = self.Slash), 'r')
        #open file for reading geojson layer in geojson format
        gj_data = myfile.read()  # read geojson layer to open file
        gj_dict = json.loads(gj_data)
        g_array = []
        for i in range(len(gj_dict['features'])):
            g_array.append(gj_dict['features'][i])
        myfile.close()  # close file
        return g_array

    def to_geojson_file(self,g_array,fNameTempl):
        """
        Write string to file
        
        Prerequisites:
        to_geojson, hex_array or box_array, horizontal, vertical, Tiles
        
        Input variables:
        """
        ...
        content = FeatureCollection(g_array)
        msg = 'writing geojson formatted {shape} dataset to file:' + fNameTempl +'.json'
        print(msg.format(shape = self.Shape, fname = self.FName))
        fName = 'geojson{slash}'+fNameTempl+'.json'
        myfile = open(fName.format(fname = self.FName,slash = self.Slash), 'w')
        #open file for writing geojson layer in geojson format
        myfile.write(str(content))  # write geojson layer to open file
        myfile.close()  # close file
        
    def from_shp_file(self,sfName,sfPath): #fName,fPath
        #tabular_list = []
        
        fPath = '{fPath}{slash}{fName}'.format(slash = self.Slash,
                             sfPath = sfPath,
                             fName = sfName)
        prjPath = fPath + '.prj'
        sf = shapefile.Reader(fPath) # , shapeType=3)
        shapes = sf.shapes()
        #how many empty and real polgons and subpolygons
        shapes_list= []
        [shapes_list.append([len(x.points),len(x.parts)]) for x in shapes]

        # add a row_id reference
        shapes_list_with_row_id = []
        [shapes_list_with_row_id.append([x,shapes_list[x][0],shapes_list[x][1]]) for x in range(len(shapes_list))]

        # drop all array rows ith 0 parts
        shapes_list_no_null = [a for a in shapes_list_with_row_id if a[2] not in [0]]

        #get the fields
        fields = sf.fields
        column_list = []
        [column_list.append(x[0]) for x in fields]


        #for x in fields: column_dict[x[0]] = ''
        tab_data = sf.records()
        tab_data_val = []
        for tab_row in range(len(shapes_list_no_null)): # all rows
            #for column_name in column_list:
            row_data = [0]
            for tab_val in tab_data[shapes_list_no_null[tab_row][0]]: # each row of tab data (y)
                row_data.append(tab_val)
            #column_dict[column_name] = str(tab_col)
            tab_data_val.append(row_data) # column_dict)
    
        geojson_list = []
        for tab_row in tab_data_val:
            dataset_dict_row = {}
            for i in range(len(column_list)-1):
                dataset_dict_row[column_list[i]] = tab_row[i]
            geojson_list.append(dataset_dict_row)
        
        # make a parts list
        parts_list = []
        for geom_data in shapes:
            if len(geom_data.parts) > 0:
                parts_list.append(geom_data.parts)
                
        sf.close()

    def to_shp_file(self,g_array,fNameTempl):
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
        props_dict = g_array[0]['properties']
        (i, props_list) = 0, []
        for key in props_dict:
            if i < 2 or i > 8:
                w.field(key, 'N')
            else:
                w.field(key, 'N', decimal = 10)
            i = i + 1

        (point_list, num_poly) = ([], len(g_array))
        for n in range (0, num_poly):
            props_dict_rec = g_array[n]['properties']
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
                    
            #print([g_array[n]['geometry']['coordinates'][0]]) 
            w.poly([g_array[n]['geometry']['coordinates'][0]])
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

    def to_kml_file(self,g_array,fNameTempl):
        fName = '{kPath}{slash}'+fNameTempl+'.kml'
        fPath = fName.format(kPath = self.KMLfilesPath,
                             shape = self.Shape,
                             size = self.Radial,
                             slash = self.Slash,
                             fname = self.FName)
        kml = simplekml.Kml()
        #setup columns
        props_dict = g_array[0]['properties']
        
        key_names_array = []
        for key in props_dict:
            key_names_array.append(key)
            

        (point_list, num_poly) = ([], len(g_array))
        for poly in range (0, num_poly):
            
            props_dict_rec = g_array[poly]['properties']
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
            for points in g_array[poly]['geometry']['coordinates'][0]:
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


    def points_and_polygons(self,g_array):
        """
        Neighbouring Polygons derivation
        
        Prerequisites:
        hex_array or box_array, horizontal, vertical ,Tiles
        
        Input variables:
        g_array
        """
        ...
        
        (point_list, num_poly) = ([], len(g_array))

        for n in range (0, num_poly):
            num_coords = len(g_array[n]['geometry']['coordinates'][0])-2
            poly_id = g_array[n]['properties']['p']
            for i in range(0, num_coords):
                point_list.append( \
                    [poly_id, str(g_array[n]['geometry']['coordinates'][0][i][0]) + \
                     str(g_array[n]['geometry']['coordinates'][0][i][1])])
        return point_list


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
        
        
    def random_points_in_polygon(self,poly):
        #path_contains_path, path_contains_points Doh! did not know about this
        np.arr = np.array(poly)
        arr_min = np.min(np_arr,axis=0)
        arr_max = np.max(np.arr,axis=0)
        min_x, min_y, max_x, max_y = (arr_min[0],arr_min[1],arr_max[0],arr_max[1])
        
        longs = np.arrange(min_x,max_x,0.002)
        lats = np.arrange(min_y,max_y,0.002)
        
        longs = np.tile(longs,3).ravel()
        lats - np.repeat(lats,3).ravel()
        
        coords = np.array([(x,y) for x,y in zip(longs,lats)])
        
        path = mpltPath.Path(poly)
        r_coords = []
        for coord in coords:
            if path.contains_point([coord[0],coord[1]]) is True:
                r_coords.append([coord[0],coord[1]])
                
        return r_coords
