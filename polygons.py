import sys
import pandas as pd
import json
from geopy.distance import distance,geodesic
from geojson import Polygon,Feature,FeatureCollection
import pandas as pd
import subprocess
#ogr2ogr -F "ESRI Shapefile" filename_2.shp hexagons_layer.json 
#1 deg longitude is about 88 km
#1 deg latitude  is about 110 km
def point_radial_distance(self,brng,radial):
    return geodesic(kilometers=radial).destination(point = self, bearing = brng)

def line_intersection(line1, line2):
    #source:
    #https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
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

def horizontal_lines(b_lat_min, b_lat_max, b_lon_min, b_lon_max, hor_seq,radial):
    print('\n1/7 deriving horizontal longitude lines')
    #lines of latitude from north to south
    #across min and max bounds latitude
    #min and max longitude from west to east
    hor_line_list=[]
    hor_line_points=[]
    seq=0
    line = [[b_lat_min, b_lon_min],[b_lat_min, b_lon_max]]
    hor_line_list.append(line)
    ref_point = [b_lat_min,b_lon_min]
    hor_line_points.append([b_lon_min, b_lat_min])
    offset = point_radial_distance(ref_point,180,radial * hor_seq[0])
    hor_line_points.append([offset[1], offset[0]])
    ref_lat = offset[0]
    ref_lon = offset[1]    
    while (ref_lat > b_lat_max):
        if seq <3:
            seq+=1
        else:
            seq=0
        line = [[ref_lat, b_lon_min],[ref_lat, b_lon_max]]
        hor_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point, 180, radial * hor_seq[seq])
        hor_line_points.append([offset[1],offset[0]])
        ref_lat = offset[0]
        ref_lon = offset[1]
    num_h = len(hor_line_list)
    print('derived {0} longitudinal lines'.format(num_h))
    return hor_line_list
    
def vertical_lines(b_lat_min, b_lat_max, b_lon_min, b_lon_max, vert_seq,radial):    
    print('\n2/7 deriving vertical latitude lines ')
    #lines of longitude from west to east
    #across min and max bounds from longitude
    #min to max latitude north to south
    vert_line_list = []
    vert_line_points = []
    line = [[b_lat_min, b_lon_min],[b_lat_max, b_lon_min]]
    vert_line_list.append(line)
    seq=0
    ref_point = [b_lat_min,b_lon_min]
    vert_line_points.append([b_lon_min,b_lat_min,vert_seq[seq]])
    offset = point_radial_distance(ref_point, 90, radial * vert_seq[seq])
    vert_line_points.append([offset[1], offset[0], vert_seq[seq]])
    ref_lon = offset[1]
    ref_lat = offset[0]
    while (ref_lon < b_lon_max):
        if seq <3:
            seq+=1
        else:
            seq=0
        line = [[b_lat_min,ref_lon],[b_lat_max, ref_lon]]
        vert_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point, 90, radial * vert_seq[seq])
        vert_line_points.append([offset[1],offset[0],vert_seq[seq]])
        ref_lon = offset[1]
        ref_lat = offset[0]

    num_v = len(vert_line_list)
    max_v = (num_v)##-1)##-((num_v-1) % 4)
    print('derived {0} latitude lines'.format(num_v))    
    return vert_line_list

def intersections(hor_line_list,hor_max,vert_line_list,vert_max):
    print('\n3/7 deriving intersection point data between horizontal and vertical lines')
    intersect_list=[]
    for h in range(0,hor_max):
        for v in range(0,vert_max):
            intersect_point=line_intersection(hor_line_list[h],vert_line_list[v])            
            intersect_data = [intersect_point[1],intersect_point[0]]
            intersect_list.append(intersect_data)          

    print('derived {0} points of intersection'.format(len(intersect_list)))  
    return intersect_list

def params(shape,north,south,east,west,radial):
    print('Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km'.format(shape, north, west, south, east, radial))

def to_shp_tab(f_name,shape):    
    shp_fname='{0}_layer.shp'.format(f_name)
    tab_fname='{0}_layer.tab'.format(f_name)
    json_fname='{0}_layer.json'.format(f_name)
    tab_options = ['/usr/bin/ogr2ogr','-f', 'Mapinfo file', tab_fname, json_fname]
    shp_options = ['/usr/bin/ogr2ogr','-f', 'ESRI Shapefile', shp_fname, json_fname]
    try:
        # record the output!
        print('\nwriting {0} shapefile {1}_layer.shp'.format(shape,f_name))
        subprocess.check_call(shp_options)
        write_vrt_file(f_name,shape,'shp','ESRI Shapefile')    
        print('\nwriting {0} shapefile {1}_layer.tab'.format(shape,f_name))
        subprocess.check_call(tab_options)
        write_vrt_file(f_name,shape,'tab','Mapinfo file')        
    except FileNotFoundError:
        print('No files processed')

def write_vrt_file(f_name,shape,ext,ext_label):
##    pnt_template = """    <OGRVRTDataSource>
##     <OGRVRTLayer name="{0}">
##         <SrcDataSource>{1}.csv</SrcDataSource>
##             <GeometryType>wkbPoint</GeometryType>
##             <LayerSRS>EPSG:4326</LayerSRS>
##             <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude"/>
##        </OGRVRTLayer>
##    </OGRVRTDataSource>"""
    
    vrt_template = """    <OGRVRTDataSource>
        <OGRVRTLayer name="{0}">
            <SrcDataSource>{0}_layer_{1}.json</SrcDataSource>
                <SrcLayer>{0}_layer</SrcLayer>
                <GeometryType>wkbPolygon</GeometryType>
            <LayerSRS>EPSG:4326</LayerSRS>
        </OGRVRTLayer>
    </OGRVRTDataSource>"""
    vrt_content = vrt_template.format(f_name,ext)
    
    print('\n {0} vrt for {1} file to written to file: {2}_layer_{3}.vrt'.format(shape,ext_label,f_name,ext))  
    file = open('{0}_layer_{1}.vrt'.format(f_name,ext_label), 'w') #open file for writing geojson layer
    file.write(vrt_content) #write vrt layer to open file
    file.close() #close file 

    #to check
    #ogrinfo -ro -al box_106km_layer.vrt
      
def boxes(north,south,east,west,radial,outfile):
    params('boxes',north,south,east,west,radial)

    #init bits
    poly_list = []
    g_array=[] #array of geojson formatted geometry elements
    tabular_list=[] #array of all polygons and tabular columns
    layer_dict={'Bounds':{'Australia':{'North': north,'South': south,'West': west,'East': east}}}
    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4823
    layer_dict['Param']['shape'] = 'box'
   
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west
    
    layer_dict['Boxes']={}
    layer_dict['Boxes']['long'] = 1     
    hor_seq =[layer_dict['Boxes']['long'], layer_dict['Boxes']['long'],\
               layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
    
    vert_seq =[layer_dict['Boxes']['long'], layer_dict['Boxes']['long'],\
               layer_dict['Boxes']['long'], layer_dict['Boxes']['long']]
    
    h_line_list = horizontal_lines(bounds_lat_min, bounds_lat_max, bounds_lon_min, bounds_lon_max, hor_seq,radial)
    num_h = len(h_line_list)
    max_h = num_h-1
    
    v_line_list = vertical_lines(bounds_lat_min, bounds_lat_max, bounds_lon_min, bounds_lon_max, vert_seq,radial)    
    num_v = len(v_line_list)
    max_v = num_v-1
    
    intersect_list = intersections(h_line_list,max_h,v_line_list,max_v)     
    
    print('\n4/7 deriving boxes polygons from intersection data')
    top_left = 0
    vertex =[top_left+0,top_left+1,top_left+max_v+1,top_left+max_v]

    while (vertex[2] < (max_h)*(max_v)):
        poly_coords = [intersect_list[vertex[0]],intersect_list[vertex[1]]\
                       ,intersect_list[vertex[2]],intersect_list[vertex[3]]\
                       ,intersect_list[vertex[0]]];
        centre_lat=intersect_list[vertex[0]][1]+(intersect_list[vertex[2]][1]-intersect_list[vertex[0]][1])/2
        centre_lon=intersect_list[vertex[0]][0]+(intersect_list[vertex[2]][0]-intersect_list[vertex[0]][0])/2
        bounds_n = intersect_list[vertex[0]][1]
        bounds_s = intersect_list[vertex[3]][1]
        bounds_e = intersect_list[vertex[1]][0]
        bounds_w = intersect_list[vertex[0]][0]
        if bounds_e > bounds_w:
            geopoly = Polygon([poly_coords])            
            geopoly = Feature(geometry=geopoly, properties={"p": top_left,"lat": centre_lat,"lon": centre_lon,\
                                                            "N": bounds_n,"S": bounds_s,"E": bounds_e,"W": bounds_w})
            g_array.append(geopoly) #append geojson geometry definition attributes to list
            #tabular dataset
            tabular_line = [top_left,centre_lat,centre_lon,\
                            bounds_n,bounds_s,bounds_e,bounds_w]
            tabular_list.append(tabular_line) #array of polygon and tabular columns

        #increment values       
        top_left+=1
        vertex =[top_left+0,top_left+1,top_left+max_v+1,top_left+max_v]
        
    print('\n5/7 boxes geojson dataset of {0} derived polygons'.format(len(g_array)))
    boxes_geojson = FeatureCollection(g_array) #convert merged geojson features to geojson feature geohex_geojson 
    g_array=[] #release g_array - array of geojson geometry elements

    print('writing boxes geojson formatted dataset to file: {0}.json'.format(outfile))
    file = open('{0}_layer.json'.format(outfile), 'w') #open file for writing geojson layer in geojson format
    file.write(str(boxes_geojson)) #write geojson layer to open file
    file.close() #close file
    
    print('\n6/7 tabular dataset of {0} lines of boxes polygon data'.format(len(tabular_list)))      
    print('writing tabular dataset to file: {0}_dataset.csv'.format(outfile))
    tabular_df = pd.DataFrame(tabular_list) #convert tabular array to tabular data frame
    tabular_df.columns = ['poly','lat','long','N','S','E','W']
    layer_dict['Bounds']['Dataset']={}#update layer_dict with dataset bounds
    layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
    layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
    layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
    layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min() 
    tabular_df.to_csv('{0}_dataset.csv'.format(outfile), sep=',')

    print('\n7/7 boxes json metadata to written to file: {0}_metadata.json'.format(outfile))  
    file = open('{0}_metadata.json'.format(outfile), 'w') #open file for writing geojson layer
    file.write(str(json.dumps(layer_dict))) #write geojson layer to open file
    file.close() #close file
    write_vrt_file(outfile,'boxes','json','geojson')    
    to_shp_tab(outfile,'boxes')
    print('\n')
    print('The End')
    ## end boxes

def hexagons(north,south,east,west,radial,outfile):
    params('hexagons',north,south,east,west,radial)   
    #init bits
    poly_list = []
    g_array=[] #array of geojson formatted geometry elements
    tabular_list=[] #array of all polygons and tabular columns
    layer_dict={'Bounds':{'Australia':{'North': north ,'South': south,'West': west,'East': east}}}
    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4823
    layer_dict['Param']['shape'] = 'hexagon'
    layer_dict['Param']['epsg'] = 4823    
    layer_dict['Hexagon']={}
    layer_dict['Hexagon']['short'] = 0.707108
    layer_dict['Hexagon']['long'] = 1
    
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west
    
    hor_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'],\
               layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short']]
    
    vert_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'],\
               layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']]
    
    h_line_list = horizontal_lines(bounds_lat_min, bounds_lat_max, bounds_lon_min, bounds_lon_max, hor_seq,radial)
    num_h = len(h_line_list)
    max_h = (num_h)##-1)##-((num_v-1) % 4)
    
    v_line_list = vertical_lines(bounds_lat_min, bounds_lat_max, bounds_lon_min, bounds_lon_max, vert_seq,radial)    
    num_v = len(v_line_list)
    max_v = (num_v)##-1)##-((num_v-1) % 4)
   
    intersect_list = intersections(h_line_list,max_h,v_line_list,max_v)          
    
    print('\n4/7 deriving polygons from intersection data')
    lat_offset = 4
    top_left = 0
    row=1
    last_lat_row=0
    poly_row_count =int(max_v/ (len(hor_seq)))
    rem_lat = max_v % (lat_offset+len(hor_seq))
    layer_dict['Row_1']={}
    layer_dict['Row_1']['lat_offset'] = lat_offset
    layer_dict['Row_1']['poly_row_count'] = poly_row_count
    layer_dict['Row_1']['remain_lat'] = rem_lat
    
    print('first row of hexagons starting from {0}, {1} hexagons, {2} latitude line(s) remaining'.format(top_left,poly_row_count,rem_lat))
    hexagon=0
    row = 1
    while (top_left < (max_h)*(max_v)):
        vertex = [1+top_left, 2+top_left, max_v+3+top_left, (max_v*2)+2+top_left, (max_v*2)+1+top_left, max_v+top_left]
        try:
            poly_coords = [intersect_list[vertex[0]], intersect_list[vertex[1]], intersect_list[vertex[2]], intersect_list[vertex[3]], intersect_list[vertex[4]], intersect_list[vertex[5]], intersect_list[vertex[0]]]
            centre_lat=intersect_list[vertex[0]][1] + (intersect_list[vertex[5]][1 ] - intersect_list[vertex[0]][1])/2
            centre_lon=intersect_list[vertex[0]][0] + (intersect_list[vertex[5]][0] - intersect_list[vertex[0]][0])/2
            
            if (centre_lat is not last_lat_row) or last_lat_row is 0:
                bounds_n = intersect_list[vertex[0]][1]
                bounds_s = intersect_list[vertex[2]][1]
                bounds_e = intersect_list[vertex[3]][0]
                bounds_w = intersect_list[vertex[0]][0]
                last_lat_row=centre_lat
                geopoly = Polygon([poly_coords])       
                hexagon+=1
                geopoly = Feature(geometry=geopoly, properties={"p": hexagon,"row": row, "lat": centre_lat, "lon": centre_lon, "N": bounds_n, "S": bounds_s, "E": bounds_e, "W": bounds_w})                                                                
                if  (bounds_e>bounds_w):
                    g_array.append(geopoly)     #append geojson geometry definition attributes to list
                    #tabular dataset
                    tabular_line = [top_left,row,centre_lat,centre_lon,\
                            bounds_n,bounds_s,bounds_e,bounds_w]
                    tabular_list.append(tabular_line) #array of polygon and tabular columns
            else:
                donothing=True

        except IndexError:
            donothing=True
            ##print('off the end {0} '.format(top_left))
            
        last_row = row
        last_lat_row=centre_lat
        row=int(1+int(hexagon/poly_row_count))
        if row % 2 is 0:
            if row is not last_row:
                top_left +=2
            else:
                 top_left += 0 
        if row & 1:
            if row is not last_row:
                top_left = top_left -2
            else:
                top_left += 0
        top_left += lat_offset
        
    print('\n5/7 geojson dataset of {0} derived hexagon polygons'.format(len(g_array)))
    boxes_geojson = FeatureCollection(g_array) #convert merged geojson features to geojson feature geohex_geojson 
    g_array=[] #release g_array - array of geojson geometry elements

    print('writing geojson formatted hexagon dataset to file: {0}.json'.format(outfile))
    file = open('{0}_layer.json'.format(outfile), 'w') #open file for writing geojson layer in geojson format
    file.write(str(boxes_geojson)) #write geojson layer to open file
    file.close() #close file
    
    print('\n6/7 tabular dataset of {0} lines of hexagon polygon data'.format(len(tabular_list)))      
    print('writing tabular dataset to file: {0}_dataset.csv'.format(outfile))
    tabular_df = pd.DataFrame(tabular_list) #convert tabular array to tabular data frame
    tabular_df.columns = ['poly','row','lat','long','N','S','E','W']
    layer_dict['Bounds']['Dataset']={}#update layer_dict with dataset bounds
    layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
    layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
    layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
    layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min() 
    tabular_df.to_csv('{0}_dataset.csv'.format(outfile), sep=',')

    print('\n7/7 hexagon json metadata to written to file: {0}_metadata.json'.format(outfile))  
    file = open('{0}_metadata.json'.format(outfile), 'w') #open file for writing geojson layer
    file.write(str(json.dumps(layer_dict))) #write geojson layer to open file
    file.close() #close file
    
    write_vrt_file(outfile,'hexagons','json','geojson')
    to_shp_tab(outfile,'hexagons')

    print('\n')
    print('The End')
    ## boxes

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
#    (shape, b_north, b_south, b_east, b_west, radial_d, f_name) = ['box', -8, -45, 168, 96, 106, 'box_106km']
#    boxes(b_north, b_south, b_east, b_west, radial_d, f_name)
    (shape, b_north, b_south, b_east, b_west, radial_d, f_name) = ['hex', -8, -45, 168, 96, 212, 'hex_212km']
    hexagons(b_north, b_south, b_east, b_west, radial_d, f_name)
else:
    if (len(sys.argv) <8 ):
        sys.exit("arguments are \nshape - hex or box \n bounding north\n bounding south \n bounding east \n bounding west \n radius in km\n filename for output\n\nfor hexagon\npython3 polygons.py hex -8 -45 96 168 212\n\nfor boxes\npython3 polygons.py box -8 -45 96 168 212\n")
    else:
        (blah,shape,b_north,b_south,b_east,b_west,radial_d,f_name) = sys.argv
        shape=str(shape)
        print(shape)
        if shape == "hex":
            hexagons(b_north,b_south,b_east,b_west,radial_d,f_name)
        else:
            if shape == "box":
                boxes(b_north,b_south,b_east,b_west,radial_d,f_name)
            else:
                print('shape is hex or box')

