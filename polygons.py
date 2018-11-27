import sys
import pandas as pd
import json
from geopy.distance import distance,geodesic
from geojson import Polygon,Feature,FeatureCollection
import pandas as pd
#ogr2ogr -F "ESRI Shapefile" filename_2.shp hexagons_layer.json 
#1 deg longitude is about 88 km
#1 deg latitude  is about 110 km
def point_radial_distance(self,brng,radial):
    return geodesic(kilometers=radial).destination(point = self, bearing = brng)

def line_intersection(line1, line2):
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


def boxes(north,south,east,west,radial,outfile):
    radial = 106 #km
    north = -8
    south = -45
    west = 96
    east = 168
    #init bits
    h_line_list = []
    h_line_points = []
    v_line_list = []
    v_line_points = []
    poly_list = []
    g_array=[] #array of geojson formatted geometry elements
    tabular_list=[] #array of all polygons and tabular columns
    intersect_list=[]
    layer_dict={'Bounds':{'Australia':{'North': north,'South': south,'West': west,'East': east}}}
    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = radial
   
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west
    
    print('\n1/7 deriving horizontal longitude lines')
    #lines of latitude from north to south
    #across min and max bounds latitude
    #min and max longitude from west to east
    line = [[bounds_lat_min,bounds_lon_min],[bounds_lat_min,bounds_lon_max]]
    h_line_list.append(line)
    ref_point = [bounds_lat_min,bounds_lon_min]
    h_line_points.append([bounds_lon_min,bounds_lat_min])
    offset = point_radial_distance(ref_point,180,radial)
    h_line_points.append([offset[1],offset[0]])
    ref_lat = offset[0]
    ref_lon = offset[1]
    
    while (ref_lat > bounds_lat_max):
        line = [[ref_lat,bounds_lon_min],[ref_lat,bounds_lon_max]]
        h_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point,180,radial)
        h_line_points.append([offset[1],offset[0]])
        ref_lat = offset[0]
        ref_lon = offset[1]

    num_h = len(h_line_list)
    print('derived {0} longitudinal lines'.format(num_h))

    print('writing tabular longitudinal dataset to file: longitudinal_points.csv_dataset.csv')
    h_points_df = pd.DataFrame(h_line_points) #convert tabular array to tabular data frame
    h_points_df.columns = ['long','lat']
    h_points_df.to_csv('longitudinal_points.csv', sep=',')
    
    print('\n2/7 deriving vertical latitude lines ')
    #lines of longitude from west to east
    #across min and max bounds from longitude
    #min to max latitude north to south
    line = [[bounds_lat_min,bounds_lon_min],[bounds_lat_max,bounds_lon_min]]
    v_line_list.append(line)
    ref_point = [bounds_lat_min,bounds_lon_min]
    v_line_points.append([bounds_lon_min,bounds_lat_min])
    offset = point_radial_distance(ref_point,90,radial)
    v_line_points.append([offset[1],offset[0]])
    ref_lon = offset[1]
    ref_lat = offset[0]    
    while (ref_lon < bounds_lon_max):
        line = [[bounds_lat_min,ref_lon],[bounds_lat_max,ref_lon]]
        v_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point,90,radial)
        v_line_points.append([offset[1],offset[0]])
        ref_lon = offset[1]
        ref_lat = offset[0]
    num_v = len(v_line_list)
    print('derived {0} latitude lines'.format(num_v))    
    print('writing tabular longitudinal dataset to file: boxes_lat_points.csv_dataset.csv')
    v_points_df = pd.DataFrame(v_line_points) #convert tabular array to tabular data frame
    v_points_df.columns = ['long','lat']
    v_points_df.to_csv('boxes_lat_points.csv', sep=',')
    
    print('\n3/7 deriving intersection point data between horizontal and vertical lines')
    max_h = num_h-1
    max_v = num_v-1
    for h in range(0,max_h):
        for v in range(0,max_v):
            intersect_point=line_intersection(h_line_list[h],v_line_list[v])            
            intersect_data = [intersect_point[1],intersect_point[0]]
            intersect_list.append(intersect_data)          

    print('derived {0} points of intersection'.format(len(intersect_list)))  
    print('writing tabular intersection dataset to file: boxes_intersections.csv')
    intersect_df = pd.DataFrame(intersect_list) #convert tabular array to tabular data frame
    intersect_df.columns = ['long','lat']
    intersect_df.to_csv('boxes_intersections.csv', sep=',')        
    
    print('\n4/7 deriving polygons from intersection data')
    top_left = 0
    vertex =[top_left+0,top_left+1,top_left+max_v+1,top_left+max_v]

    while (vertex[2] < (max_h)*(max_v)):
        poly_coords = [intersect_list[vertex[0]],intersect_list[vertex[1]]\
                       ,intersect_list[vertex[2]],intersect_list[vertex[3]]\
                       ,intersect_list[vertex[0]]];
        centre_lat=intersect_list[vertex[0]][1]+(intersect_list[vertex[2]][1]-intersect_list[vertex[0]][1])/2
        centre_lon=intersect_list[vertex[0]][0]+(intersect_list[vertex[2]][0]-intersect_list[vertex[0]][0])/2

        if (int(intersect_list[vertex[3]][0]) - int(intersect_list[vertex[2]][0])) <3:
            geopoly = Polygon([poly_coords])
            bounds_n = intersect_list[vertex[0]][1]
            bounds_s = intersect_list[vertex[3]][1]
            bounds_e = intersect_list[vertex[1]][0]
            bounds_w = intersect_list[vertex[0]][0]
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
        
    print('\n5/7 geojson dataset of {0} derived polygons'.format(len(g_array)))
    boxes_geojson = FeatureCollection(g_array) #convert merged geojson features to geojson feature geohex_geojson 
    g_array=[] #release g_array - array of geojson geometry elements

    print('writing geojson formatted dataset to file: {0}.json'.format(outfile))
    file = open('{0}.json'.format(outfile), 'w') #open file for writing geojson layer in geojson format
    file.write(str(boxes_geojson)) #write geojson layer to open file
    file.close() #close file
    
    print('\n6/7 tabular dataset of {0} lines of polygon data'.format(len(tabular_list)))      
    print('writing tabular dataset to file: {0}_dataset.csv'.format(outfile))
    tabular_df = pd.DataFrame(tabular_list) #convert tabular array to tabular data frame
    tabular_df.columns = ['poly','lat','long','N','S','E','W']
    layer_dict['Bounds']['Dataset']={}#update layer_dict with dataset bounds
    layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
    layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
    layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
    layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min() 
    tabular_df.to_csv('{0}_dataset.csv'.format(outfile), sep=',')

    print('\n7/7 box json metadata to written to file: {0}_metadata.json'.format(outfile))  
    file = open('{0}_metadata.json'.format(outfile), 'w') #open file for writing geojson layer
    file.write(str(json.dumps(layer_dict))) #write geojson layer to open file
    file.close() #close file 

    print('\n')
    print('The End')
    ## end boxes

def hexagons(north,south,east,west,radial,outfile):
    radial = 53 #km
    north = -8
    south = -45
    west = 96
    east = 168
    
    #init bits
    h_line_list = []
    h_line_points = []
    v_line_list = []
    v_line_points = []
    poly_list = []
    g_array=[] #array of geojson formatted geometry elements
    tabular_list=[] #array of all polygons and tabular columns
    intersect_list=[]
    layer_dict={'Bounds':{'Australia':{'North': north ,'South': south,'West': west,'East': east}}}

    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['shape'] = 'hexagon'
    layer_dict['Hexagon']={}
    layer_dict['Hexagon']['short'] = 0.707108
    layer_dict['Hexagon']['long'] = 1   
   
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west
    
    off_sequence =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'],\
                   layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']] 
    
    print('\n1/7 deriving horizontal longitude lines')
    #lines of latitude from north to south
    #across min and max bounds latitude
    #min and max longitude from west to east
    line = [[bounds_lat_min,bounds_lon_min],[bounds_lat_min,bounds_lon_max]]
    h_line_list.append(line)
    ref_point = [bounds_lat_min,bounds_lon_min]
    h_line_points.append([bounds_lon_min,bounds_lat_min])
    offset = point_radial_distance(ref_point,180,radial*off_sequence[0])
    h_line_points.append([offset[1],offset[0]])
    ref_lat = offset[0]
    ref_lon = offset[1]
    
    while (ref_lat > bounds_lat_max):
        line = [[ref_lat,bounds_lon_min],[ref_lat,bounds_lon_max]]
        h_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point,180,radial*off_sequence[0])
        h_line_points.append([offset[1],offset[0]])
        ref_lat = offset[0]
        ref_lon = offset[1]
    num_h = len(h_line_list)
    print('derived {0} longitudinal lines'.format(num_h))

    print('writing tabular longitudinal dataset to file: hexagons_long_points.csv_dataset.csv')
    h_points_df = pd.DataFrame(h_line_points) #convert tabular array to tabular data frame
    h_points_df.columns = ['long','lat']
    h_points_df.to_csv('hexagons_long_points.csv', sep=',')
    
    print('\n2/7 deriving vertical latitude lines ')
    #lines of longitude from west to east
    #across min and max bounds from longitude
    #min to max latitude north to south
    line = [[bounds_lat_min,bounds_lon_min],[bounds_lat_max,bounds_lon_min]]
    v_line_list.append(line)
    seq=0
    ref_point = [bounds_lat_min,bounds_lon_min]
    v_line_points.append([bounds_lon_min,bounds_lat_min,off_sequence[seq]])
    offset = point_radial_distance(ref_point,90,radial*off_sequence[seq])
    v_line_points.append([offset[1],offset[0],off_sequence[seq]])
    ref_lon = offset[1]
    ref_lat = offset[0]
    while (ref_lon < bounds_lon_max):
        if seq <3:
            seq+=1
        else:
            seq=0
        line = [[bounds_lat_min,ref_lon],[bounds_lat_max,ref_lon]]
        v_line_list.append(line)
        ref_point = [ref_lat,ref_lon]
        offset = point_radial_distance(ref_point,90,radial*off_sequence[seq])
        v_line_points.append([offset[1],offset[0],off_sequence[seq]])
        ref_lon = offset[1]
        ref_lat = offset[0]

    num_v = len(v_line_list)
    max_v = (num_v)##-1)##-((num_v-1) % 4)
    print('derived {0} latitude lines'.format(num_v))    
    print('writing tabular longitudinal dataset to file: hexagons_lat_points.csv_dataset.csv')
    v_points_df = pd.DataFrame(v_line_points) #convert tabular array to tabular data frame
    v_points_df.columns = ['long','lat','radial_mulitplier']
    v_points_df.to_csv('hexagons_lat_points.csv', sep=',')
    
    print('\n3/7 deriving intersection point data between horizontal and vertical lines')
    #Hexagon is three high and four points across
    max_h = (num_h)##-1)##-((num_h-1) % 3)

    for h in range(0,max_h):
        for v in range(0,max_v):
            intersect_point=line_intersection(h_line_list[h],v_line_list[v])            
            intersect_data = [intersect_point[1],intersect_point[0],]
            intersect_list.append(intersect_data)          

    print('derived {0} points of intersection'.format(len(intersect_list)))  
    print('writing tabular intersection dataset to file: hexagons_intersection.csv')
    intersect_df = pd.DataFrame(intersect_list) #convert tabular array to tabular data frame
    intersect_df.columns = ['long','lat']
    intersect_df.to_csv('hexagons_intersection.csv', sep=',')        
    
    print('\n4/7 deriving polygons from intersection data')
    lat_offset = 4
    top_left = 0
    row=1
    last_lat_row=0
    poly_row_count =int(max_v/ (len(off_sequence)))
    rem_lat = max_v % (lat_offset+len(off_sequence))
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
        
    print('\n5/7 geojson dataset of {0} derived polygons'.format(len(g_array)))
    boxes_geojson = FeatureCollection(g_array) #convert merged geojson features to geojson feature geohex_geojson 
    g_array=[] #release g_array - array of geojson geometry elements

    print('writing geojson formatted dataset to file: {0}.json'.format(outfile))
    file = open('{0}.json'.format(outfile), 'w') #open file for writing geojson layer in geojson format
    file.write(str(boxes_geojson)) #write geojson layer to open file
    file.close() #close file
    
    print('\n6/7 tabular dataset of {0} lines of polygon data'.format(len(tabular_list)))      
    print('writing tabular dataset to file: {0}_dataset.csv'.format(outfile))
    tabular_df = pd.DataFrame(tabular_list) #convert tabular array to tabular data frame
    tabular_df.columns = ['poly','row','lat','long','N','S','E','W']
    layer_dict['Bounds']['Dataset']={}#update layer_dict with dataset bounds
    layer_dict['Bounds']['Dataset']['North'] = tabular_df['N'].max()
    layer_dict['Bounds']['Dataset']['South'] = tabular_df['S'].min()
    layer_dict['Bounds']['Dataset']['East'] = tabular_df['E'].max()
    layer_dict['Bounds']['Dataset']['West'] = tabular_df['W'].min() 
    tabular_df.to_csv('{0}_dataset.csv'.format(outfile), sep=',')

    print('\n7/7 box json metadata to written to file: {0}_metadata.json'.format(outfile))  
    file = open('{0}_metadata.json'.format(outfile), 'w') #open file for writing geojson layer
    file.write(str(json.dumps(layer_dict))) #write geojson layer to open file
    file.close() #close file 

    print('\n')
    print('The End')
    ## boxes

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (shape,b_north,b_south,b_east,b_west,radial_d,f_name) = ['hex',-8,45,96,168,106,'hexagons_layer']
    hexagons(b_north,b_south,b_east,b_west,radial_d,f_name)
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

